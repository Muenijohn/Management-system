from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), index=True, nullable=False)
    category = Column(String(50), nullable=False)  # "BOOKSHOP" or "LAB_SUPPLY"
    unit_price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=False)
    total_stock = Column(Integer, default=0)
    reorder_level = Column(Integer, default=5)
    requires_batch = Column(Boolean, default=False)
    hazard_info = Column(String(100), nullable=True)

    batches = relationship("Batch", back_populates="product")
    invoice_items = relationship("InvoiceItem", back_populates="product")

class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    batch_number = Column(String(50), nullable=False)
    expiry_date = Column(DateTime, nullable=True)
    quantity = Column(Integer, default=0)

    product = relationship("Product", back_populates="batches")
    invoice_items = relationship("InvoiceItem", back_populates="batch")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), unique=True, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    cashier_id = Column(Integer, nullable=False)
    customer_name = Column(String(150), default="Walk-in Customer")
    payment_method = Column(String(30), nullable=False)  # Cash, M-Pesa, Card
    subtotal = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    total = Column(Float, default=0.0)

    items = relationship("InvoiceItem", back_populates="invoice")

class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    line_total = Column(Float, nullable=False)

    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product", back_populates="invoice_items")
    batch = relationship("Batch", back_populates="invoice_items")