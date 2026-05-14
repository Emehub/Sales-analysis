from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

output = r'd:\Sales insights\Sales_Analysis_Presentation.pdf'

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
WHITE  = colors.white

body = ParagraphStyle('body', fontSize=10.5, fontName='Helvetica',
    textColor=DARK, leading=16, spaceAfter=5, alignment=TA_JUSTIFY)
bold_body = ParagraphStyle('bold_body', fontSize=10.5, fontName='Helvetica-Bold',
    textColor=DARK, leading=16, spaceAfter=4)
section_title = ParagraphStyle('section_title', fontSize=14, fontName='Helvetica-Bold',
    textColor=PURPLE, spaceBefore=18, spaceAfter=6, leading=18)
cover_title = ParagraphStyle('cover_title', fontSize=26, fontName='Helvetica-Bold',
    textColor=WHITE, alignment=TA_CENTER, leading=32, spaceAfter=6)
cover_sub = ParagraphStyle('cover_sub', fontSize=12, fontName='Helvetica',
    textColor=colors.HexColor('#dde2f0'), alignment=TA_CENTER, leading=17)
cover_meta = ParagraphStyle('cover_meta', fontSize=10, fontName='Helvetica',
    textColor=colors.HexColor('#a29bfe'), alignment=TA_CENTER, leading=14)
insight_style = ParagraphStyle('insight', fontSize=10.5, fontName='Helvetica',
    textColor=DARK, leading=15, spaceAfter=4, leftIndent=14, alignment=TA_JUSTIFY)
small_grey = ParagraphStyle('small_grey', fontSize=9, fontName='Helvetica',
    textColor=GREY, leading=13, spaceAfter=2)

W = 16.6*cm

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
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, colors.HexColor('#f5f7fc')]),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#dde2f0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

def highlight_box(para, bg=colors.HexColor('#f0f3fa'), border=PURPLE):
    t = Table([[para]], colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LINEBEFORE', (0,0), (0,-1), 3, border),
        ('TOPPADDING', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 9),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

def insight_box(title, text, col):
    para = Paragraph('<b>' + title + '</b><br/>' + text, insight_style)
    t = Table([[para]], colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f5f7fc')),
        ('LINEBEFORE', (0,0), (0,-1), 4, col),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

story = []

# COVER
cover = Table([[Paragraph('Sales Analysis Dashboard 2026', cover_title)]], colWidths=[W])
cover.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), PURPLE),
    ('TOPPADDING', (0,0), (-1,-1), 38),
    ('BOTTOMPADDING', (0,0), (-1,-1), 38),
    ('LEFTPADDING', (0,0), (-1,-1), 18),
    ('RIGHTPADDING', (0,0), (-1,-1), 18),
]))
story.append(cover)
story.append(Spacer(1, 0.35*cm))

sub = Table([[Paragraph('Veterinary Vaccine Distribution — Ghana Operations', cover_sub)]], colWidths=[W])
sub.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), DARK),
    ('TOPPADDING', (0,0), (-1,-1), 12),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
]))
story.append(sub)
story.append(Spacer(1, 0.45*cm))
story.append(Paragraph('Presented by: Emelia Awin', cover_meta))
story.append(Paragraph('Period: January - May 2026', cover_meta))
story.append(Paragraph('Date: May 2026', cover_meta))
story.append(Spacer(1, 0.8*cm))
story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#dde2f0')))
story.append(Spacer(1, 0.5*cm))

# INTRODUCTION
story.append(Paragraph('Introduction', section_title))
story.append(highlight_box(Paragraph(
    'I built an interactive business intelligence dashboard for our operations using data from our 2026 Sales Ledger. '
    'I extracted, cleaned, and analysed over 13,500 records from 8 data sheets and turned them into a fully interactive '
    'web dashboard that any team member can open in any browser with no software required. The dashboard is live online.',
    body)))
story.append(Spacer(1, 0.25*cm))
story.append(Paragraph('Live Dashboard (now connected to Google Sheets): https://emehub.github.io/Sales-analysis/Sales_Dashboard.html', small_grey))
story.append(Spacer(1, 0.35*cm))

# DATA
story.append(Paragraph('Data I Worked With', section_title))
story.append(Paragraph('I pulled and analysed data from the following sheets in our Sales Ledger workbook:', body))
story.append(make_table(
    ['Sheet', 'Records', 'What I Used It For'],
    [
        ['A-Sales Orders', '1,919 rows', 'Revenue, products, regions, salesperson performance'],
        ['B-Invoices', '2,962 rows', 'Total invoiced, payments collected, outstanding balances'],
        ['C-Payment Receipts', '1,897 rows', 'Cash collection and payment mode tracking'],
        ['Customers', '57 rows', 'Customer status, revenue YTD, expected revenue'],
        ['Weekly Sales & Targets', '143 rows', 'Weekly performance vs weekly targets'],
        ['Delivery Time Tracker', '82 rows', 'Drone delivery zone and time analysis'],
        ['Reports', 'Monthly', 'Product unit sales by month'],
        ['Inventory', '997 rows', 'Stock movement overview'],
    ],
    [4.8*cm, 2.5*cm, 9.3*cm]
))
story.append(Spacer(1, 0.35*cm))

# WHAT I BUILT
story.append(Paragraph('What I Built', section_title))
story.append(Paragraph(
    'I designed and built a 6-section interactive dashboard with animated scorecards, charts, and searchable tables. '
    'Each section is accessible through a clickable sidebar menu:', body))
story.append(Spacer(1, 0.15*cm))

sections = [
    ('1.  Overview',
     'I created 8 animated scorecards giving a full business snapshot the moment the dashboard loads. '
     'I included monthly revenue vs target, regional revenue, salesperson performance, and a collection vs outstanding breakdown.'),
    ('2.  Sales Performance',
     'I tracked every week from Week 2 to Week 18 and plotted actual revenue against weekly targets. '
     'I added toggles so you can switch between Revenue, Average Order Value, and Order count views. '
     'I also built a colour-coded target achievement chart showing green, amber, and red weeks.'),
    ('3.  Products',
     'I analysed all vaccine products by revenue and built a bar chart and a donut chart showing the product mix. '
     'I included a full breakdown table with each product\'s value and percentage share.'),
    ('4.  Customers',
     'I built three layers of customer intelligence: a leaderboard ranked by revenue, a frequency analysis '
     'showing who orders most often, and an outstanding balances tracker for every customer with unpaid invoices. '
     'All three tables are searchable.'),
    ('5.  Payments and Collections',
     'I analysed how money is coming in by payment mode, by collection status, and by salesperson. '
     'I placed all three charts side by side so they can be compared at a glance.'),
    ('6.  Delivery Tracking',
     'I analysed our drone delivery data by zone and by recipient type. '
     'I included a searchable delivery records table showing customer, zone, drop site, and total delivery time.'),
]
for title, text in sections:
    story.append(Paragraph(title, bold_body))
    story.append(Paragraph(text, insight_style))
    story.append(Spacer(1, 0.12*cm))

# KEY NUMBERS
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph('Key Numbers I Found', section_title))
story.append(make_table(
    ['Metric', 'Value'],
    [
        ['Total Revenue Invoiced (Jan-May 2026)', 'GHS 2,403,787.00'],
        ['Total Cash Collected', 'GHS 1,693,810.00'],
        ['Total Outstanding Balance', 'GHS 709,977.00'],
        ['Collection Rate', '70.5%'],
        ['Total Orders Placed', '331'],
        ['Order Fulfillment Rate', '100%'],
        ['Average Order Value', 'GHS 7,262.20'],
        ['Active Customers', '42 out of 57 (73.7%)'],
        ['Top Revenue Customer', 'Birikwart Ventures - GHS 244,860'],
        ['Most Frequent Orderer', 'Razz Asaana Ent - 90 orders'],
    ],
    [9*cm, 7.6*cm]
))
story.append(Spacer(1, 0.35*cm))

# PRODUCTS
story.append(Paragraph('Product Revenue Breakdown', section_title))
story.append(make_table(
    ['Rank', 'Product', 'Revenue (GHS)', 'Share of Total'],
    [
        ['1', 'VIRSIN 121L (NewCavac)', '925,470', '38.5%'],
        ['2', 'VIR 102 (Fowl Pox)', '462,188', '19.2%'],
        ['3', 'VIR 114 (Gumboro Intermediate)', '377,625', '15.7%'],
        ['4', 'VIR 116 (Lasota)', '363,825', '15.1%'],
        ['5', 'VIR 105 (HB1)', '165,848', '6.9%'],
    ],
    [1.5*cm, 7.1*cm, 4.5*cm, 3.5*cm]
))
story.append(Spacer(1, 0.35*cm))

# KEY INSIGHTS
story.append(Paragraph('Key Insights I Want to Highlight', section_title))
insights = [
    (GREEN,  '1.  Collections Have Improved Significantly',
             'Our collection rate has risen from 52.3% to 70.5% — meaning we have now collected GHS 1,693,810 '
             'of the GHS 2,403,787 invoiced. Outstanding balances have dropped from GHS 979,423 to GHS 709,977. '
             '28 customers still have unpaid invoices, with Birikwart Ventures owing the most at GHS 114,910.'),
    (AMBER,  '2.  One Salesperson is Carrying the Entire Business',
             'I found that Righteous Kamoah generated 95.6% of our total revenue (GHS 2,298,469). '
             'This is a concentration risk. If that person is unavailable, our revenue is severely exposed.'),
    (PURPLE, '3.  We Are Dependent on One Product',
             'I found that NewCavac (VIRSIN 121L) alone accounts for 38.5% of all revenue (GHS 925,470). '
             'Any supply issue or demand shift for this product would significantly impact our numbers.'),
    (GREEN,  '4.  We Have a Perfect Fulfillment Record',
             'I confirmed that every single order — all 331 of them — was successfully delivered. '
             'This is a strong operational achievement and something I believe we should communicate to our customers.'),
    (AMBER,  '5.  Some Customers Remain Inactive',
             'I found that 15 out of 57 customers (26.3%) are currently inactive — a slight improvement from 16 last month. '
             'Re-engaging these customers is an immediate revenue opportunity that does not require finding new clients.'),
    (GREEN,  '6.  April Was Our Strongest Month Yet',
             'April delivered GHS 701,192 — our highest monthly revenue so far in 2026, '
             'a 67% increase over March. May is showing GHS 232,598 so far and is still in progress.'),
]
for col, title, text in insights:
    story.append(insight_box(title, text, col))
    story.append(Spacer(1, 0.18*cm))

# CLOSING
story.append(Spacer(1, 0.25*cm))
story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#dde2f0')))
story.append(Spacer(1, 0.25*cm))
story.append(Paragraph('Closing Note', section_title))
story.append(highlight_box(Paragraph(
    'Everything I have presented here is available live on the dashboard at any time. '
    'The charts are interactive — you can click through each section, toggle between views, and search through the tables. '
    'I am happy to walk through any section in more detail during this meeting.',
    body)))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    'Presented by Emelia Awin  |  May 2026  |  Ghana Veterinary Vaccine Distribution',
    small_grey))

doc.build(story)
print('PDF created:', output)
