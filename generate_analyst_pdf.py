from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

output = r'd:\Sales insights\Analyst_Report_Dashboard.pdf'

doc = SimpleDocTemplate(
    output, pagesize=A4,
    rightMargin=2.2*cm, leftMargin=2.2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm
)

PURPLE = colors.HexColor('#6c63ff')
DARK   = colors.HexColor('#1e2235')
GREY   = colors.HexColor('#6b7280')
GREEN  = colors.HexColor('#00856f')
RED    = colors.HexColor('#e74c3c')
AMBER  = colors.HexColor('#f39c12')
BLUE   = colors.HexColor('#54a0ff')
WHITE  = colors.white
LIGHT  = colors.HexColor('#f0f3fa')
LIGHT2 = colors.HexColor('#f5f7fc')

W = 16.6*cm

body = ParagraphStyle('body', fontSize=10.5, fontName='Helvetica',
    textColor=DARK, leading=16.5, spaceAfter=6, alignment=TA_JUSTIFY)
bold_body = ParagraphStyle('bold_body', fontSize=10.5, fontName='Helvetica-Bold',
    textColor=DARK, leading=16, spaceAfter=3)
section_title = ParagraphStyle('section_title', fontSize=14, fontName='Helvetica-Bold',
    textColor=PURPLE, spaceBefore=20, spaceAfter=7, leading=18)
sub_section = ParagraphStyle('sub_section', fontSize=11, fontName='Helvetica-Bold',
    textColor=DARK, spaceBefore=10, spaceAfter=4, leading=15)
cover_title = ParagraphStyle('cover_title', fontSize=24, fontName='Helvetica-Bold',
    textColor=WHITE, alignment=TA_CENTER, leading=30)
cover_role = ParagraphStyle('cover_role', fontSize=13, fontName='Helvetica-Bold',
    textColor=colors.HexColor('#a29bfe'), alignment=TA_CENTER, leading=18)
cover_sub = ParagraphStyle('cover_sub', fontSize=11, fontName='Helvetica',
    textColor=colors.HexColor('#dde2f0'), alignment=TA_CENTER, leading=16)
cover_meta = ParagraphStyle('cover_meta', fontSize=10, fontName='Helvetica',
    textColor=colors.HexColor('#9aa3c8'), alignment=TA_CENTER, leading=14)
bullet_p = ParagraphStyle('bullet_p', fontSize=10.5, fontName='Helvetica',
    textColor=DARK, leading=15, spaceAfter=4, leftIndent=16)
small_grey = ParagraphStyle('small_grey', fontSize=9, fontName='Helvetica',
    textColor=GREY, leading=13)
tag_style = ParagraphStyle('tag', fontSize=9, fontName='Helvetica-Bold',
    textColor=WHITE, alignment=TA_CENTER)

def make_table(headers, rows, col_widths):
    data = [headers] + rows
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PURPLE),
        ('TEXTCOLOR',  (0,0), (-1,0), WHITE),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 9),
        ('FONTNAME',   (0,1), (-1,-1), 'Helvetica'),
        ('TEXTCOLOR',  (0,1), (-1,-1), DARK),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT2]),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#dde2f0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

def side_box(para, border_color=PURPLE, bg=LIGHT):
    t = Table([[para]], colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LINEBEFORE', (0,0), (0,-1), 3, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 9),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

def step_box(number, title, text, col=PURPLE):
    num_para = Paragraph(f'<b>{number}</b>', ParagraphStyle('num', fontSize=13,
        fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_CENTER))
    content = Paragraph(f'<b>{title}</b><br/>{text}', bullet_p)
    t = Table([[num_para, content]], colWidths=[1.1*cm, 15.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), col),
        ('BACKGROUND', (1,0), (1,-1), LIGHT2),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (0,-1), 4),
        ('LEFTPADDING', (1,0), (1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#dde2f0')),
    ]))
    return t

def future_box(phase, title, items, col):
    rows = [[Paragraph(f'<b>{phase}</b>', ParagraphStyle('ph', fontSize=9,
        fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_CENTER))]]
    phase_cell = Table(rows, colWidths=[2.2*cm])
    phase_cell.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), col),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    content_text = f'<b>{title}</b><br/>' + '<br/>'.join([f'  -  {i}' for i in items])
    content = Paragraph(content_text, ParagraphStyle('fc', fontSize=10,
        fontName='Helvetica', textColor=DARK, leading=15, leftIndent=4))
    t = Table([[phase_cell, content]], colWidths=[2.4*cm, 14.2*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (1,0), (1,-1), LIGHT2),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (1,0), (1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#dde2f0')),
        ('LINEBEFORE', (1,0), (1,-1), 2, col),
    ]))
    return t

story = []

# ===== COVER =====
cover = Table([[Paragraph('Analyst Report', cover_role),
               ]], colWidths=[W])
cover.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), DARK),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
]))
story.append(cover)
story.append(Spacer(1, 0.3*cm))

main_cover = Table([[Paragraph(
    'Sales Intelligence Dashboard\nDevelopment and Roadmap Report', cover_title)]], colWidths=[W])
main_cover.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), PURPLE),
    ('TOPPADDING', (0,0), (-1,-1), 36),
    ('BOTTOMPADDING', (0,0), (-1,-1), 36),
    ('LEFTPADDING', (0,0), (-1,-1), 16),
    ('RIGHTPADDING', (0,0), (-1,-1), 16),
]))
story.append(main_cover)
story.append(Spacer(1, 0.35*cm))

sub = Table([[Paragraph('How I Built It and Where I Am Taking It Next', cover_sub)]], colWidths=[W])
sub.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#22263a')),
    ('TOPPADDING', (0,0), (-1,-1), 11),
    ('BOTTOMPADDING', (0,0), (-1,-1), 11),
]))
story.append(sub)
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('Analyst: Emelia Awin', cover_meta))
story.append(Paragraph('Organisation: Ghana Veterinary Vaccine Distribution', cover_meta))
story.append(Paragraph('Period Covered: January - May 2026', cover_meta))
story.append(Paragraph('Report Date: May 2026', cover_meta))
story.append(Spacer(1, 0.8*cm))
story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#dde2f0')))
story.append(Spacer(1, 0.5*cm))

# ===== 1. BACKGROUND =====
story.append(Paragraph('1. Background and Problem Statement', section_title))
story.append(side_box(Paragraph(
    'As the data analyst for this organisation, I identified a critical gap: our sales, invoice, payment, '
    'customer, and delivery data was being tracked across 13 separate Excel sheets with no unified view. '
    'Management had no quick way to see how the business was performing, where collections were failing, '
    'which products were driving revenue, or how customers were behaving. '
    'I took it upon myself to solve this by building a live, interactive business intelligence dashboard '
    'that consolidates everything into one accessible place.', body), PURPLE, LIGHT))
story.append(Spacer(1, 0.3*cm))

# ===== 2. DATA COLLECTION =====
story.append(Paragraph('2. Data Collection and Preparation', section_title))
story.append(Paragraph(
    'The first thing I did was audit the full data structure of our Sales Ledger workbook. '
    'I identified 8 usable sheets containing over 13,500 rows of operational data. '
    'I then carried out the following preparation steps:', body))
story.append(Spacer(1, 0.2*cm))
story.append(step_box('1', 'Data Audit',
    'I reviewed all 13 sheets and identified which ones contained structured, usable data '
    'versus template or empty sheets. I selected 8 sheets for analysis.', PURPLE))
story.append(step_box('2', 'Data Extraction',
    'I wrote Python scripts using the Pandas and OpenPyXL libraries to extract data from each sheet. '
    'I automated the reading of column names, data types, and row counts.', BLUE))
story.append(step_box('3', 'Data Cleaning',
    'I stripped whitespace from all column headers, converted numeric fields that were stored as text, '
    'handled missing values, parsed date columns into proper datetime format, '
    'and removed rows with null primary keys (Order ID, Invoice Number, etc.).', AMBER))
story.append(step_box('4', 'Data Aggregation',
    'I grouped and aggregated data across multiple dimensions — by customer, by region, by product, '
    'by week, by month, and by salesperson — to produce the summary metrics used in the dashboard.', GREEN))
story.append(step_box('5', 'Validation',
    'I cross-referenced totals across sheets to verify consistency. For example, I confirmed that '
    'invoice totals aligned with sales order subtotals, and that payment receipts matched invoice payment columns.', RED))
story.append(Spacer(1, 0.35*cm))

# ===== 3. ANALYTICAL METHODOLOGY =====
story.append(Paragraph('3. Analytical Methodology', section_title))
story.append(Paragraph(
    'Once the data was clean and aggregated, I applied the following analytical approaches '
    'to extract meaningful business intelligence:', body))
story.append(Spacer(1, 0.15*cm))

methods = [
    ('Revenue Analysis',
     'I computed total invoiced revenue, collected revenue, and outstanding balances per customer, per region, '
     'per product, and per salesperson. I used these to build collection rate metrics and identify where cash flow risk is highest.'),
    ('Trend Analysis',
     'I analysed week-over-week and month-over-month revenue patterns against set targets. '
     'I calculated percentage target achievement for each week and colour-coded performance into three bands: '
     'above target (green), 70-99% of target (amber), and below 70% (red).'),
    ('Customer Segmentation',
     'I segmented customers by revenue contribution, order frequency, and payment behaviour. '
     'I computed average order values and identified high-value low-frequency customers versus '
     'high-frequency low-value customers — two very different customer profiles requiring different strategies.'),
    ('Product Mix Analysis',
     'I calculated the revenue share of each vaccine product and identified concentration risk '
     'where a single product (NewCavac) accounts for over 40% of all revenue.'),
    ('Delivery Performance Analysis',
     'I parsed delivery time data across zones and recipient types, identifying which zones handle '
     'the highest delivery volumes and how the split between farmer and agrovet deliveries looks operationally.'),
    ('Outstanding Balance Profiling',
     'I built a full receivables profile by customer, calculating collection rates and classifying '
     'each customer as high-risk (below 40% collected), medium-risk (40-69%), or low-risk (70%+).'),
]
for title, text in methods:
    story.append(Paragraph(title, sub_section))
    story.append(Paragraph(text, body))

# ===== 4. TOOLS =====
story.append(Paragraph('4. Tools and Technologies I Used', section_title))
story.append(make_table(
    ['Tool / Technology', 'Purpose', 'Why I Chose It'],
    [
        ['Python 3.13', 'Data extraction, cleaning, aggregation', 'Powerful, fast, and handles large Excel files reliably'],
        ['Pandas 3.0', 'Data manipulation and analysis', 'Industry-standard library for structured data analysis'],
        ['OpenPyXL 3.1', 'Reading .xlsx Excel files', 'Direct Excel support without converting file formats'],
        ['Chart.js 4.4', 'Interactive dashboard charts', 'Lightweight, browser-native, no server required'],
        ['HTML / CSS / JavaScript', 'Dashboard interface', 'Runs in any browser with no installation needed'],
        ['GitHub Pages', 'Live hosting and version control', 'Free, reliable hosting with full version history'],
        ['ReportLab', 'PDF report generation', 'Professional PDF creation directly from Python'],
    ],
    [3.8*cm, 5.2*cm, 7.6*cm]
))
story.append(Spacer(1, 0.35*cm))

# ===== 5. DASHBOARD ARCHITECTURE =====
story.append(Paragraph('5. How I Structured the Dashboard', section_title))
story.append(Paragraph(
    'I initially embedded the analysed data directly into the HTML file as JavaScript constants for speed. '
    'I have since upgraded the architecture to connect the dashboard live to Google Sheets via a Google Apps Script Web App — '
    'so data now refreshes automatically every 5 minutes without any manual updates. The full structure is:', body))
story.append(Spacer(1, 0.15*cm))
story.append(make_table(
    ['Layer', 'Technology', 'What It Does'],
    [
        ['Data Layer', 'Google Apps Script + Google Sheets', 'Live data fetched via Web App API on every load'],
        ['Visualisation Layer', 'Chart.js', 'Renders 18 interactive charts with tooltips and toggles'],
        ['Navigation Layer', 'Vanilla JavaScript', 'Handles 6-page routing and active state management'],
        ['Animation Layer', 'CSS + JS', 'Counter animations on scorecard numbers on page load'],
        ['Interaction Layer', 'JavaScript', 'Toggle buttons, search filters, and chart view switching'],
        ['Presentation Layer', 'CSS Variables', 'Light mode theming applied consistently across all components'],
        ['Hosting Layer', 'GitHub Pages', 'Deploys automatically on every git push to main branch'],
    ],
    [3.8*cm, 3.8*cm, 9*cm]
))
story.append(Spacer(1, 0.35*cm))

# ===== 6. KEY ANALYTICAL FINDINGS =====
story.append(Paragraph('6. Key Analytical Findings', section_title))
findings = [
    (GREEN,  'Finding 1: Collection Performance Has Significantly Improved',
             'The collection rate has risen from 52.3% to 70.5% — an 18-point improvement in one month. '
             'Outstanding balances have dropped from GHS 979,423 to GHS 709,977. '
             '28 customers still have unpaid invoices, with Birikwart Ventures holding the highest balance at GHS 114,910. '
             '2 customers have made zero payments and require immediate follow-up.'),
    (AMBER,  'Finding 2: Single-Point-of-Failure in Sales',
             'One salesperson — Righteous Kamoah — is responsible for 95.6% of all revenue (GHS 2,298,469). '
             'This is not a sales strength; it is an operational risk. '
             'A departure, illness, or performance change from this individual would be catastrophic for revenue.'),
    (PURPLE, 'Finding 3: Product Revenue Concentration',
             'Five products account for 95.4% of all revenue, with NewCavac alone at 38.5% (GHS 925,470). '
             'The bottom three products contributed less than 5% combined. '
             'There is an opportunity to either grow the underperforming products or rationalise the portfolio.'),
    (GREEN,  'Finding 4: Operational Excellence in Fulfillment',
             'A 100% fulfillment rate across 331 orders is a standout metric. '
             'This demonstrates that the logistics and drone delivery infrastructure is performing at a high level '
             'and can be used as a competitive differentiator when acquiring new customers.'),
    (BLUE,   'Finding 5: Customer Frequency vs Value Disconnect',
             'Razz Asaana Ent placed 90 orders but at a low average order value. '
             'Birikwart Ventures placed fewer orders but generated GHS 244,860 — the highest revenue of any customer. '
             'These two customers require fundamentally different account management strategies.'),
    (AMBER,  'Finding 6: 26.3% Customer Churn',
             '15 of our 57 customers are currently inactive — a slight improvement from 16 last month. '
             'If even half of these were reactivated at the average revenue per active customer, '
             'that represents significant additional revenue without acquiring a single new customer.'),
]
for col, title, text in findings:
    story.append(side_box(Paragraph(f'<b>{title}</b><br/>{text}', body), col, LIGHT2))
    story.append(Spacer(1, 0.15*cm))

# ===== 7. FUTURE ROADMAP =====
story.append(Paragraph('7. What I Am Adding Next — Roadmap for Organisational Growth', section_title))
story.append(Paragraph(
    'The dashboard now covers January to May 2026 with live Google Sheets integration. '
    'Below is my phased roadmap for expanding it into a full organisational intelligence platform:', body))
story.append(Spacer(1, 0.2*cm))

roadmap = [
    (GREEN, 'Phase 1', 'COMPLETED — Live Google Sheets Integration', [
        'Connected the dashboard directly to Google Sheets via a Google Apps Script Web App',
        'Dashboard now fetches live data automatically every 5 minutes with no manual updates required',
        'Added a live status badge and last-updated timestamp visible in the dashboard topbar',
        'May 2026 data (GHS 232,598 so far) is now live and updating in real time',
    ]),
    (BLUE, 'Phase 2', 'Q3 2026 — Customer Intelligence Expansion', [
        'Build a Customer Health Score combining payment rate, order frequency, and recency into a single score',
        'Add a Churn Risk Flag that automatically highlights customers who have not ordered in 60+ days',
        'Create a Collections Priority List ranked by outstanding balance and days overdue',
        'Add customer-level profitability analysis including delivery cost per order',
    ]),
    (GREEN, 'Phase 3', 'Q3 2026 — Sales Team Performance Module', [
        'Expand the salesperson analysis beyond Righteous Kamoah to track all reps individually',
        'Add individual sales targets and personal achievement rates per rep',
        'Build a territory map showing which districts each rep covers and their revenue density',
        'Create a pipeline tracker for pre-orders and forecasted revenue',
    ]),
    (AMBER, 'Phase 4', 'Q4 2026 — Inventory and Supply Chain Analytics', [
        'Integrate the Inventory sheet to track stock levels against sales velocity',
        'Add a Stockout Risk Alert when closing stock falls below a defined threshold',
        'Build demand forecasting for each vaccine based on historical weekly sales patterns',
        'Track supplier performance and lead times for restocking',
    ]),
    (RED, 'Phase 5', 'Q1 2027 — Executive Reporting and Automation', [
        'Build an automated weekly email report that sends key metrics to management every Monday',
        'Add year-over-year comparison once 2025 data is loaded',
        'Create a mobile-optimised version of the dashboard for field access',
        'Integrate Google Sheets as a live data backend to eliminate manual Excel updates entirely',
    ]),
]
for col, phase, title, items in roadmap:
    story.append(future_box(phase, title, items, col))
    story.append(Spacer(1, 0.15*cm))

# ===== 8. VALUE TO THE ORGANISATION =====
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph('8. Value This Work Delivers to the Organisation', section_title))
story.append(make_table(
    ['Area', 'Current State', 'With This Dashboard'],
    [
        ['Decision Speed', 'Hours reviewing multiple Excel sheets', 'Seconds — one click to any metric'],
        ['Collections Visibility', 'No real-time view of who owes what', 'Full outstanding profile for all 28 customers'],
        ['Sales Accountability', 'No individual performance tracking', 'Revenue, AOV, and target rate per rep'],
        ['Product Strategy', 'No revenue share visibility', 'Instant product mix and concentration view'],
        ['Customer Retention', 'Churn discovered late', 'Inactive customers visible at a glance'],
        ['Meeting Readiness', 'Manual report preparation', 'Live dashboard and PDF reports on demand'],
        ['Data Accessibility', 'Only on local Excel file', 'Live online — accessible from any device anywhere'],
    ],
    [3.6*cm, 5.5*cm, 7.5*cm]
))
story.append(Spacer(1, 0.4*cm))

# ===== 9. KPIs =====
story.append(Paragraph('9. My Key Performance Indicators (KPIs)', section_title))
story.append(Paragraph(
    'Based on the data I analysed and the dashboard I built, below are the KPIs I will be tracking '
    'on an ongoing basis to measure the health and growth of the organisation. '
    'I have grouped them into six categories:', body))
story.append(Spacer(1, 0.2*cm))

kpi_categories = [
    (PURPLE, 'Revenue KPIs', [
        ['Total Revenue (GHS)',          'Sum of all invoiced sales',                              'GHS 2,403,787.00',  'Monthly'],
        ['Monthly Revenue Growth Rate',  'Month-over-month % change in revenue',                  'Apr: +67% vs Mar',  'Monthly'],
        ['Revenue vs Target Rate',       '% of monthly/weekly target achieved',                   'Varies by week',    'Weekly'],
        ['Average Order Value (AOV)',     'Total revenue divided by number of orders',             'GHS 7,262.20',      'Weekly'],
        ['Cumulative YTD Revenue',        'Running total of revenue for the year',                'GHS 2,403,787.00',  'Monthly'],
    ]),
    (GREEN, 'Collections and Cash Flow KPIs', [
        ['Collection Rate',              '% of invoiced revenue that has been collected',         '70.5%',             'Weekly'],
        ['Total Outstanding Balance',    'Total unpaid invoices across all customers',            'GHS 709,977.00',    'Weekly'],
        ['Customers at Zero Payment',    'Number of customers who have paid nothing',             '2 customers',       'Weekly'],
        ['High-Risk Customers',          'Customers with collection rate below 40%',              'Monitored',         'Weekly'],
        ['Average Collection Rate',      'Mean collection rate across all active customers',      '70.5%',             'Monthly'],
    ]),
    (BLUE, 'Sales Operations KPIs', [
        ['Total Orders Placed',          'Count of unique sales orders',                          '331',               'Weekly'],
        ['Order Fulfillment Rate',        '% of orders successfully delivered',                   '100%',              'Weekly'],
        ['Weekly Orders Count',          'Number of new orders placed each week',                 'Avg 19/week',       'Weekly'],
        ['Revenue per Salesperson',       'Total revenue attributed to each sales rep',           'Tracked per rep',   'Monthly'],
        ['Salesperson Target Achievement','% of individual target met per rep',                   'Tracked per rep',   'Monthly'],
    ]),
    (AMBER, 'Customer KPIs', [
        ['Active Customer Rate',         '% of customers who ordered at least once YTD',          '73.7% (42/57)',     'Monthly'],
        ['Customer Churn Rate',          '% of customers who have gone inactive',                 '26.3% (15/57)',     'Monthly'],
        ['Average Revenue per Customer', 'Total revenue divided by active customers',             'GHS 57,233',        'Monthly'],
        ['Customer Order Frequency',     'Average number of orders placed per customer',          'Tracked per cust',  'Monthly'],
        ['Top Customer Revenue Share',   '% of total revenue from top 5 customers',              'Monitored',         'Monthly'],
        ['Reactivated Customers',         'Inactive customers who placed a new order',            'Target: 8 per qtr', 'Quarterly'],
    ]),
    (RED, 'Product KPIs', [
        ['Revenue by Product',           'GHS revenue per vaccine product',                       'Tracked per SKU',   'Monthly'],
        ['Top Product Revenue Share',    '% of total revenue from the #1 product (NewCavac)',     '38.5%',             'Monthly'],
        ['Product Concentration Risk',   'No. of products accounting for 80% of revenue',         '3 products',        'Monthly'],
        ['Units Sold per Product',        'Quantity of each vaccine sold per period',             'Tracked per SKU',   'Monthly'],
        ['Bottom Product Revenue',        'Revenue from the lowest-performing products',          'Monitored',         'Monthly'],
    ]),
    (colors.HexColor('#4ecdc4'), 'Delivery KPIs', [
        ['Drone Delivery Fulfillment Rate','% of delivery requests successfully completed',       '100%',              'Weekly'],
        ['Average Delivery Time',          'Mean time from order to delivery per zone',           'Tracked per zone',  'Weekly'],
        ['Deliveries by Zone',             'Count of deliveries per sales zone',                  'Anum Zone: 72%',    'Monthly'],
        ['Farmer vs Agrovet Split',        '% of deliveries to farmers vs agrovet stores',        '82.9% / 13.4%',     'Monthly'],
        ['Active Delivery Zones',          'Number of zones receiving deliveries',                '5 zones',           'Monthly'],
    ]),
]

for col, category, kpis in kpi_categories:
    # Category header bar
    hdr = Table([[Paragraph(f'<b>{category}</b>', ParagraphStyle('kpi_hdr',
        fontSize=11, fontName='Helvetica-Bold', textColor=WHITE))]], colWidths=[W])
    hdr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), col),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(hdr)
    kpi_data = [['KPI', 'Definition', 'Current Value', 'Frequency']]
    for row in kpis:
        kpi_data.append(row)
    t = Table(kpi_data, colWidths=[4.2*cm, 6.0*cm, 3.8*cm, 2.6*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f5f7fc')),
        ('TEXTCOLOR',  (0,0), (-1,0), GREY),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 8.5),
        ('FONTNAME',   (0,1), (-1,-1), 'Helvetica'),
        ('TEXTCOLOR',  (0,1), (-1,-1), DARK),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, colors.HexColor('#f9fafc')]),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#dde2f0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME',   (0,1), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR',  (0,1), (0,-1), col),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.25*cm))

story.append(Spacer(1, 0.15*cm))
story.append(side_box(Paragraph(
    '<b>Total KPIs being tracked: 31 across 6 categories.</b> '
    'These will be reviewed weekly for operational KPIs and monthly for strategic KPIs. '
    'As the roadmap progresses, I will add KPIs for inventory turnover, customer lifetime value, '
    'demand forecast accuracy, and salesperson pipeline conversion rate.',
    body), PURPLE, LIGHT))
story.append(Spacer(1, 0.4*cm))

# ===== CLOSING =====
story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#dde2f0')))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('Analyst Statement', section_title))
story.append(side_box(Paragraph(
    'Every decision I made in this project — from the data I selected, to the metrics I calculated, '
    'to the way I structured the dashboard — was guided by one goal: giving this organisation the '
    'visibility it needs to grow. The work I have done in Phase 1 is the foundation. '
    'The roadmap I have laid out will transform this from a reporting tool into a true '
    'decision-making engine for the business. I am committed to seeing that through.',
    body), PURPLE, LIGHT))
story.append(Spacer(1, 0.45*cm))
story.append(Paragraph(
    'Emelia Awin  |  Data Analyst  |  Ghana Veterinary Vaccine Distribution  |  May 2026',
    small_grey))

doc.build(story)
print('Analyst PDF created:', output)
