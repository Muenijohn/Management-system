import pandas as pd
import re
from database import SessionLocal
from models import Product

def generate_sku(name, category, index):
    prefix = "LAB" if "LAB" in category.upper() else "BKS"
    cleaned_name = re.sub(r'[^A-Za-z0-9]', '', str(name)).upper()[:6]
    return f"{prefix}-{cleaned_name}-{index:04d}"

def clean_price(val):
    if pd.isna(val) or val is None or val == "":
        return 0.0
    val_str = re.sub(r'[^\d.]', '', str(val))
    return float(val_str) if val_str else 0.0

def import_inventory(file_path="inventory.xlsx"):
    db = SessionLocal()
    xl = pd.ExcelFile(file_path)
    total_added = 0

    for sheet_name in xl.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        if df.empty:
            continue

        df.columns = [str(col).strip() for col in df.columns]
        sheet_category = "LAB_SUPPLY" if any(k in sheet_name.upper() for k in ["CHEM", "LAB"]) else "BOOKSHOP"

        for idx, row in df.iterrows():
            name_col = next((col for col in df.columns if any(k in col.upper() for k in ["NAME", "EQUIPMENT", "ITEM", "DESCRIPTION"])), df.columns[0])
            item_name = str(row[name_col]).strip()
            if not item_name or item_name.lower() == "nan":
                continue

            # Append size/spec if in second column
            spec = ""
            if len(df.columns) > 1 and df.columns[1] not in ["PRICE", "sku", name_col]:
                spec_val = str(row[df.columns[1]]).strip()
                if spec_val and spec_val.lower() != "nan":
                    spec = f" ({spec_val})"
            full_name = f"{item_name}{spec}"

            category = str(row.get("category", sheet_category)).strip().upper()
            sku = str(row["sku"]).strip() if "sku" in row and pd.notna(row["sku"]) else generate_sku(item_name, category, idx + 1)

            price_col = next((col for col in df.columns if "PRICE" in col.upper()), None)
            unit_price = clean_price(row[price_col]) if price_col else clean_price(row.get("unit_price", 0.0))
            cost_price = clean_price(row.get("cost_price", unit_price * 0.75))

            total_stock = int(row["total_stock"]) if "total_stock" in row and pd.notna(row["total_stock"]) else 10
            requires_batch = bool(row["requires_batch"]) if "requires_batch" in row and pd.notna(row["requires_batch"]) else (category == "LAB_SUPPLY")

            product = db.query(Product).filter(Product.sku == sku).first()
            if not product:
                product = Product(
                    sku=sku,
                    name=full_name,
                    category=category,
                    unit_price=unit_price,
                    cost_price=cost_price,
                    total_stock=total_stock,
                    reorder_level=5,
                    requires_batch=requires_batch,
                    hazard_info=str(row.get("hazard_info")) if pd.notna(row.get("hazard_info")) else None
                )
                db.add(product)
                total_added += 1

    db.commit()
    db.close()
    print(f"Ingestion complete! Successfully imported {total_added} products into PostgreSQL.")

if __name__ == "__main__":
    import_inventory()