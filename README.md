# Dual-Inventory POS & Retail Management System

A self-hosted management and point-of-sale system built with FastAPI and PostgreSQL to handle dual-sector operations:
standard retail bookshop goods and batch-tracked science laboratory supplies.

## Core Objectives

Dual Inventory: Seamlessly handles standard retail goods (BOOKSHOP) and lot-controlled, hazardous reagents (LAB_SUPPLY) in a single unified system.

Batch & Expiry Control: Direct support for First-Expired, First-Out (FEFO) stock rotation, expiration dates, and chemical hazard labels.

B2B Invoicing: Designed to process everyday walk-in retail transactions as well as institutional credit orders and quotations for schools.

### Tech Stack
Backend: Python (FastAPI), SQLAlchemy 2.0

Database: PostgreSQL 18

Data ETL: Pandas, OpenPyXL

Environment: VS Code, Windows PowerShell

### Database Architecture (school_supplies_db)
products: Central catalog storing SKUs, item names, category tags, pricing, stock levels, reorder thresholds, and safety classifications.

batches: Granular tracking table for chemical lots, expiration dates, and lot quantities.

invoices: Sales header capturing transaction IDs, timestamps, payment methods (Cash, M-Pesa, Card), and totals.

invoice_items: Line items linking products and specific chemical batches to parent invoices.
