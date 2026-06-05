from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

output = r'd:\Sales insights\April_Report_2026.pdf'

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
note_style = ParagraphStyle('note', fontSize=9.5, fontName='Helvetica-Oblique',
    textColor=GREY, leading=14, spaceAfter=2, alignment=TA_CENTER)

# Paragraph styles for inside table cells
th_style = ParagraphStyle('th', fontSize=9, fontName='Helvetica-Bold',
    textColor=WHITE, leading=13, alignment=TA_CENTER)
td_style = ParagraphStyle('td', fontSize=9, fontName='Helvetica',
    textColor=DARK, leading=13, alignment=TA_LEFT)
td_center = ParagraphStyle('td_c', fontSize=9, fontName='Helvetica',
    textColor=DARK, leading=13, alignment=TA_CENTER)

W = 16.6*cm

def P(text, style=None):
    return Paragraph(text, style or td_style)

def make_table(headers, rows, col_widths):
    hdr_cells = [Paragraph(h, th_style) for h in headers]
    body_rows = []
    for row in rows:
        body_rows.append([Paragraph(str(cell), td_style) for cell in row])
    data = [hdr_cells] + body_rows
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),  (-1,0),  PURPLE),
        ('ROWBACKGROUNDS',(0,1),  (-1,-1), [WHITE, colors.HexColor('#f5f7fc')]),
        ('GRID',          (0,0),  (-1,-1), 0.4, colors.HexColor('#dde2f0')),
        ('TOPPADDING',    (0,0),  (-1,-1), 6),
        ('BOTTOMPADDING', (0,0),  (-1,-1), 6),
        ('LEFTPADDING',   (0,0),  (-1,-1), 8),
        ('RIGHTPADDING',  (0,0),  (-1,-1), 8),
        ('VALIGN',        (0,0),  (-1,-1), 'MIDDLE'),
    ]))
    return t

def highlight_box(para, bg=colors.HexColor('#f0f3fa'), border=PURPLE):
    t = Table([[para]], colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LINEBEFORE',  (0,0), (0,-1), 3, border),
        ('TOPPADDING',  (0,0), (-1,-1), 9),
        ('BOTTOMPADDING',(0,0),(-1,-1), 9),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING',(0,0), (-1,-1), 12),
    ]))
    return t

def insight_box(title, text, col):
    para = Paragraph('<b>' + title + '</b><br/>' + text, insight_style)
    t = Table([[para]], colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), colors.HexColor('#f5f7fc')),
        ('LINEBEFORE',   (0,0), (0,-1), 4, col),
        ('TOPPADDING',   (0,0), (-1,-1), 8),
        ('BOTTOMPADDING',(0,0), (-1,-1), 8),
        ('LEFTPADDING',  (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

story = []

# ── COVER ──────────────────────────────────────────────────────────────────
cover = Table([[Paragraph('April 2026 Monthly Report', cover_title)]], colWidths=[W])
cover.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (-1,-1), PURPLE),
    ('TOPPADDING',   (0,0), (-1,-1), 38),
    ('BOTTOMPADDING',(0,0), (-1,-1), 38),
    ('LEFTPADDING',  (0,0), (-1,-1), 18),
    ('RIGHTPADDING', (0,0), (-1,-1), 18),
]))
story.append(cover)
story.append(Spacer(1, 0.35*cm))

sub = Table([[Paragraph('Veterinary Vaccine Distribution — Ghana Operations', cover_sub)]], colWidths=[W])
sub.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (-1,-1), DARK),
    ('TOPPADDING',   (0,0), (-1,-1), 12),
    ('BOTTOMPADDING',(0,0), (-1,-1), 12),
]))
story.append(sub)
story.append(Spacer(1, 0.45*cm))
story.append(Paragraph('Presented by: Emelia Awin', cover_meta))
story.append(Paragraph('Period: April 2026 (in context of January – May 2026)', cover_meta))
story.append(Paragraph('Date: May 2026', cover_meta))
story.append(Spacer(1, 0.8*cm))
story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#dde2f0')))
story.append(Spacer(1, 0.5*cm))

# ── SECTION 1 — NEW AGROVETS ───────────────────────────────────────────────
story.append(Paragraph('1.  New Agrovets Signed In — April 2026', section_title))
story.append(highlight_box(Paragraph(
    'In April 2026, <b>2 new Agrovets were onboarded</b> for the first time, bringing new revenue into the business. '
    'These customers placed their first recorded invoices during April and were not present in any prior month.',
    body)))
story.append(Spacer(1, 0.3*cm))

# col widths: 0.6 + 5.2 + 3.2 + 3.8 + 3.8 = 16.6
story.append(make_table(
    ['#', 'Agrovet Name', 'First Invoice Date', 'April Revenue', 'Notes'],
    [
        ['1', 'Vic Jeaf Enterprise', '10 Apr 2026', 'GHS 14,400', 'New customer — first order in April'],
        ['2', 'Vetpoint',            '29 Apr 2026', 'GHS 9,950',  'New customer — first order in April'],
    ],
    [0.6*cm, 5.2*cm, 3.2*cm, 3.8*cm, 3.8*cm]
))
story.append(Spacer(1, 0.25*cm))
story.append(insight_box(
    'Total Agrovets Served in April',
    'Across all invoices raised in April 2026, <b>31 unique Agrovets</b> were served — meaning 31 distinct customers '
    'placed or received at least one invoice during the month. This includes the 2 newly onboarded customers listed above.',
    GREEN))
story.append(Spacer(1, 0.3*cm))

# ── SECTION 2 — INCOME GROWTH ─────────────────────────────────────────────
story.append(Paragraph('2.  Percentage Growth in Income — Month-on-Month', section_title))
story.append(Paragraph(
    'The table below tracks total invoiced revenue for each month from January to May 2026, '
    'along with the percentage change relative to the prior month.', body))
story.append(Spacer(1, 0.15*cm))

# col widths: 3.2 + 3.6 + 3.2 + 6.6 = 16.6
story.append(make_table(
    ['Month', 'Revenue (GHS)', 'vs Prev Month', 'Commentary'],
    [
        ['January 2026',  'GHS 628,783', '— (baseline)', 'Strongest opening month of the year'],
        ['February 2026', 'GHS 417,194', '−33.7%',       'Sharp post-January dip'],
        ['March 2026',    'GHS 420,180', '+0.7%',         'Recovery begins; growth nearly flat'],
        ['April 2026',    'GHS 701,192', '+67.0%',        'Best month of the year so far'],
        ['May 2026 *',    'GHS 232,598', 'In progress',   'Partial month — data still open'],
    ],
    [3.2*cm, 3.6*cm, 3.2*cm, 6.6*cm]
))
story.append(Spacer(1, 0.15*cm))
story.append(Paragraph('* May 2026 figures are as at 26 May 2026 and are not yet complete.', note_style))
story.append(Spacer(1, 0.25*cm))

story.append(insight_box(
    'April Was Our Best Month in 2026',
    'April delivered GHS 701,192 — a <b>67.0% increase</b> over March and the highest single-month revenue '
    'recorded so far in 2026. It also exceeds January by 11.5%, which had previously been the strongest month. '
    'April broke the two-month plateau seen in February and March.',
    GREEN))
story.append(Spacer(1, 0.15*cm))
story.append(insight_box(
    'Watch the February Dip',
    'February recorded a 33.7% drop from January. This seasonal pattern is worth monitoring — '
    'if a similar dip occurs in 2027, proactive order scheduling or targeted outreach in January '
    'could help smooth the revenue curve.',
    AMBER))
story.append(Spacer(1, 0.3*cm))

# ── SECTION 3 — CASH VS DEBT ──────────────────────────────────────────────
story.append(Paragraph('3.  Revenue Generated in Cash vs Debt — by Month', section_title))
story.append(Paragraph(
    "The table below breaks down each month's total invoiced revenue into the portion "
    "already collected in cash and the portion still outstanding as debt.", body))
story.append(Spacer(1, 0.15*cm))

# col widths: 2.4 + 3.3 + 3.3 + 3.8 + 3.8 = 16.6
story.append(make_table(
    ['Month', 'Total Invoiced', 'Collected (Cash)', 'Outstanding (Debt)', 'Coll. Rate'],
    [
        ['January',   'GHS 628,783', 'GHS 625,353', 'GHS 3,430',   '99.5%'],
        ['February',  'GHS 417,194', 'GHS 395,323', 'GHS 21,872',  '94.8%'],
        ['March',     'GHS 420,180', 'GHS 296,790', 'GHS 123,390', '70.6%'],
        ['April',     'GHS 701,192', 'GHS 376,344', 'GHS 324,848', '53.7%'],
        ['May *',     'GHS 236,438', 'GHS 0',       'GHS 236,438', '— *'],
    ],
    [2.4*cm, 3.3*cm, 3.3*cm, 3.8*cm, 3.8*cm]
))
story.append(Spacer(1, 0.15*cm))
story.append(Paragraph(
    '* May collections are not yet recorded. Cash figures will update as payments come in.',
    note_style))
story.append(Spacer(1, 0.3*cm))

story.append(insight_box(
    'January Collections Were Almost Perfect',
    'January had a 99.5% collection rate — virtually all revenue invoiced was paid in the same month. '
    'This set a strong cash foundation for the year.',
    GREEN))
story.append(Spacer(1, 0.15*cm))
story.append(insight_box(
    'April Debt Is the Largest Single-Month Balance',
    'April has GHS 324,848 outstanding — the largest debt balance of any single month in 2026. '
    'With a collection rate of 53.7%, roughly half of April\'s revenue has not yet been received. '
    'Prioritising April follow-ups now will significantly reduce the total outstanding balance.',
    RED))
story.append(Spacer(1, 0.15*cm))
story.append(insight_box(
    'Overall Collection Rate: 70.5%',
    'Across all five months, total invoiced revenue is GHS 2,403,787. Of this, GHS 1,693,810 has been '
    'collected in cash and GHS 709,977 remains as outstanding debt. The overall collection rate is 70.5%, '
    'up from 52.3% as of the previous review — a strong improvement driven by January and February clearances.',
    PURPLE))
story.append(Spacer(1, 0.4*cm))

# ── CLOSING ────────────────────────────────────────────────────────────────
story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#dde2f0')))
story.append(Spacer(1, 0.25*cm))
story.append(Paragraph(
    'Prepared by Emelia Awin  |  May 2026  |  Ghana Veterinary Vaccine Distribution',
    small_grey))

doc.build(story)
print('PDF created:', output)
