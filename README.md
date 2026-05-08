# Sales Analysis Dashboard 2026
### Veterinary Vaccine Distribution — Ghana Operations

---

## Overview

This is an interactive web-based business intelligence dashboard built from the company's 2026 Sales Ledger. It transforms raw Excel data across 13 sheets and over 13,500 records into clear, clickable visuals and scorecards for management decision-making.

The dashboard runs directly in any browser — no software installation required.

**Live Link:** https://emehub.github.io/Sales-analysis/Sales_Dashboard.html

---

## Data Sources

All data was extracted from **Copy of Sales Ledger 2026.xlsx**, which contains:

| Sheet | Records | Description |
|---|---|---|
| A-Sales Orders | 1,919 rows | All sales transactions |
| B-Invoices | 2,962 rows | Invoice and payment tracking |
| C-Payment Receipts | 1,897 rows | Cash collection records |
| Customers | 57 rows | Customer master list |
| Weekly Sales & Targets | 143 rows | Weekly performance vs targets |
| Inventory | 997 rows | Stock movement data |
| Delivery Time Tracker | 82 rows | Drone delivery records |
| Reports | Product monthly unit sales | |

---

## Dashboard Sections

The dashboard has **6 clickable menu sections** in the left sidebar:

---

### 1. Overview
A high-level snapshot of the entire business with 8 animated scorecards:

| Metric | Value |
|---|---|
| Total Revenue (Invoiced) | GHS 2,054,114.50 |
| Total Collected | GHS 1,074,691.00 |
| Outstanding Balance | GHS 979,423.50 |
| Collection Rate | 52.3% |
| Total Orders | 289 |
| Fulfillment Rate | 100% |
| Average Order Value | GHS 7,107.66 |
| Active Customers | 41 of 57 |

Visuals include:
- Monthly Revenue vs Target (bar/line toggle)
- Revenue by Region (donut chart)
- Sales by Salesperson (horizontal bar)
- Collection vs Outstanding (donut chart)

---

### 2. Sales Performance
Tracks weekly and monthly sales trends against targets.

- Monthly scorecards for January through April 2026
- Weekly Revenue vs Target chart (Weeks 2-18) with toggles for Revenue, AOV, and Orders
- Target Achievement Rate bar chart (colour-coded: green above 100%, amber above 70%, red below)
- Monthly Revenue Comparison line chart

**Key finding:** January was the strongest month at GHS 628,783. April recovered strongly at GHS 594,257 after a dip in February and March.

---

### 3. Products
Analyses revenue performance across all vaccine products.

- Revenue by Product bar chart (vertical/horizontal toggle)
- Product revenue mix donut chart
- Full product breakdown table with revenue share and progress bars

| Rank | Product | Revenue (GHS) | Share |
|---|---|---|---|
| 1 | VIRSIN 121L (NewCavac) | 829,080 | 40.2% |
| 2 | VIR 102 (Fowl Pox) | 390,938 | 19.0% |
| 3 | VIR 114 (Gumboro Intermediate) | 311,700 | 15.1% |
| 4 | VIR 116 (Lasota) | 298,708 | 14.5% |
| 5 | VIR 105 (HB1) | 139,038 | 6.7% |

**Key finding:** All revenue comes from vaccines. NewCavac alone accounts for 40% of total sales.

---

### 4. Customers
Three layers of customer intelligence:

**Customer Leaderboard**
Top customers ranked by YTD revenue with region, status, purchase count, and achievement rate against expected revenue. Searchable.

**Top Customers by Order Frequency**
- Bar chart of top 15 customers by number of orders placed (toggle: Orders / Avg Order Value)
- Dual-axis chart comparing order frequency vs total revenue (top 10)
- Full table with order count, revenue, average order value, and order share

**Customers with Outstanding Balances**
- 36 customers with unpaid invoices
- Columns: Customer, Invoice Total, Amount Collected, Outstanding Balance, Collection Rate
- Collection rate colour-coded: green (70%+), amber (40-69%), red (below 40%)
- Searchable

**Key findings:**
- Birikwart Ventures is the top revenue customer at GHS 207,660 with 11 orders
- Razz Asaana Ent placed the most orders (74) but at low average value (GHS 1,206)
- Birikwart Ventures has the highest outstanding balance at GHS 116,410
- 3 customers (Good God Pet Shop, Veterinary Drug House, Vic K Ventures) have made zero payments

---

### 5. Payments & Collections
Three side-by-side charts analysing cash flow:

- Payment Mode Distribution — MoMo Transfer dominates at 77.4% of transactions (113 of 145)
- Collection Performance — GHS 1.07M collected vs GHS 979K still outstanding
- Salesperson Collection Performance — Righteous Kamoah accounts for 95.7% of all revenue (GHS 1,966,047)

---

### 6. Delivery Tracking
Analyses drone delivery operations across sales zones.

- 82 total tracked deliveries
- 82.9% delivered to farmers, 13.4% to agrovets
- Anum Sales Zone handles 72% of all deliveries (59 of 82)
- Delivery records table with customer, zone, drop site, total time, and recipient type. Searchable.

---

## Key Business Insights

1. **Collection rate is 52.3%** — nearly half of all invoiced revenue (GHS 979K) remains uncollected. This is the most critical area requiring management attention.

2. **One salesperson drives the business** — Righteous Kamoah generated 95.7% of total revenue. This is a significant concentration risk.

3. **NewCavac is the revenue engine** — a single product generates 40% of all revenue. Any supply or demand disruption would have a major impact.

4. **100% fulfillment rate** — every single order placed (289 of 289) was delivered. This is an exceptional operational achievement.

5. **28.1% customer churn** — 16 of 57 customers are inactive. Re-engagement of these customers represents untapped revenue potential.

6. **April recovery is promising** — after a 34% drop in February, April revenue of GHS 594,257 signals a positive trend heading into Q2.

---

## Technical Details

- Built with HTML, CSS, and JavaScript — runs in any modern browser
- Charts powered by Chart.js 4.4
- Data embedded directly from the Excel source
- Hosted on GitHub Pages
- Repository: https://github.com/Emehub/Sales-analysis

---

*Dashboard prepared by Claude (Anthropic) — April 2026*
