import pandas as pd
import json

f = 'Sales Ledger 2026.xlsx'

def to_num(s):
    try: return float(str(s).replace(',','').replace(' ',''))
    except: return 0.0

def safe_str(v): return str(v).strip() if v and str(v).strip() not in ['nan','None',''] else ''

MN = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}

# INVOICES
inv = pd.read_excel(f, sheet_name='B-Invoices')
inv.columns = [str(c).strip().lower() for c in inv.columns]
inv = inv.dropna(how='all')
tot_rev = inv['total'].apply(to_num).sum()
tot_col = inv['payment'].apply(to_num).sum()
tot_out = inv['balance'].apply(to_num).sum()
coll_rate = round(tot_col/tot_rev*100,1) if tot_rev else 0
out_rate  = round(100-coll_rate,1)
cust_rev = inv.groupby('customer name')['total'].apply(lambda x: x.apply(to_num).sum())
cust_pay = inv.groupby('customer name')['payment'].apply(lambda x: x.apply(to_num).sum())
cust_bal = inv.groupby('customer name')['balance'].apply(lambda x: x.apply(to_num).sum())
rep_rev  = inv.groupby('sales person')['total'].apply(lambda x: x.apply(to_num).sum()).sort_values(ascending=False)
mode_s   = inv['payment mode'].dropna().astype(str).str.strip()
mode_s   = mode_s[mode_s.str.lower() != 'nan']
mode_cnt = mode_s.value_counts()

# ORDERS
ord_ = pd.read_excel(f, sheet_name='A-Sales Orders')
ord_.columns = [str(c).strip().lower() for c in ord_.columns]
ord_ = ord_.dropna(subset=['sales order id'])
total_orders = ord_['sales order id'].nunique()
aov = round(tot_rev/total_orders,2) if total_orders else 0
ord_['order date'] = pd.to_datetime(ord_['order date'], errors='coerce')
ord_['month'] = ord_['order date'].dt.month
ord_['sub_n'] = ord_['subtotal'].apply(to_num)
monthly = ord_.groupby('month')['sub_n'].sum().sort_index()
reg_col = [c for c in ord_.columns if 'region' in c][0]
merged_reg = ord_.groupby(ord_[reg_col].str.strip())['sub_n'].sum().sort_values(ascending=False).head(10)
products = ord_.groupby('item name')['sub_n'].sum().sort_values(ascending=False)
freq_orders = ord_.groupby('customer name')['sales order id'].nunique()
freq_rev    = ord_.groupby('customer name')['sub_n'].sum()
freq_df = pd.DataFrame({'orders': freq_orders, 'revenue': freq_rev})
freq_df['aov'] = (freq_df['revenue']/freq_df['orders']).round(0).astype(int)
freq_df = freq_df.sort_values('orders',ascending=False).head(20).reset_index()

# CUSTOMERS
cust_s = pd.read_excel(f, sheet_name='Customers')
cust_s.columns = [str(c).strip().lower() for c in cust_s.columns]
cust_s = cust_s.dropna(how='all')
nm_c = [c for c in cust_s.columns if 'customer name' in c][0]
st_c = [c for c in cust_s.columns if 'status' in c][0]
rg_c = [c for c in cust_s.columns if 'region' in c][0]
ry_c = [c for c in cust_s.columns if 'revenue' in c and 'ytd' in c][0]
er_c = [c for c in cust_s.columns if 'expected' in c][0]
pc_c = [c for c in cust_s.columns if 'purchase' in c or 'number of' in c][0]
cust_s = cust_s[cust_s[nm_c].apply(lambda x: safe_str(x) != '')]
act_mask = cust_s[st_c].astype(str).str.lower().str.contains('active') & ~cust_s[st_c].astype(str).str.lower().str.contains('not')
act_c = int(act_mask.sum()); inact_c = len(cust_s) - act_c
cust_rg_ytd = cust_s.groupby(cust_s[rg_c].str.strip())[ry_c].apply(lambda x: x.apply(to_num).sum()).sort_values(ascending=False).head(10)
exp_map = {safe_str(r[nm_c]): to_num(r[er_c]) for _,r in cust_s.iterrows()}
rg_map  = {safe_str(r[nm_c]): safe_str(r[rg_c]) for _,r in cust_s.iterrows()}
st_map  = {safe_str(r[nm_c]): safe_str(r[st_c]) for _,r in cust_s.iterrows()}
pc_map  = {safe_str(r[nm_c]): int(to_num(r[pc_c])) for _,r in cust_s.iterrows()}

# WEEKLY
wk = pd.read_excel(f, sheet_name='Weekly Sales & Targets')
wk.columns = [str(c).strip().lower() for c in wk.columns]
wk['week number'] = pd.to_numeric(wk['week number'], errors='coerce')
wk['value ghs']   = wk['value ghs'].apply(to_num)
wk = wk[(wk['week number']>0)&(wk['week number']<100)&(wk['value ghs']>0)].sort_values('week number')

# DISEASE MONTHLY (from Reports sheet — units delivered by vaccine/disease)
DISEASE_MAP = {
    'Newcastle (Poultry)': ['Lasota','HB1','Newcavac','Lasota + IB','I2 ND-VAC 500D','Newcavac + EDS + IB'],
    'Gumboro (Poultry)':   ['Gumboro Intermediate'],
    'Fowlpox (Poultry)':   ['Fowl Pox'],
    'AI (Poultry)':        [],
    'PPR (Goats & Sheep)': [],
    'CBPP (Cattle)':       [],
}
MONTH_ABBR = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
rep = pd.read_excel(f, sheet_name='Reports')
rep.columns = [str(c).strip() for c in rep.columns]
units_df = rep.iloc[0:8].copy()
units_df = units_df.rename(columns={units_df.columns[0]: 'Product'})
units_df = units_df[units_df['Product'].notna()].reset_index(drop=True)
# Identify which month columns exist
month_cols = [c for c in units_df.columns if any(c.strip().startswith(m) for m in MONTH_ABBR)]
disease_labels = [m for m in MONTH_ABBR if any(c.strip().startswith(m) for c in month_cols)]
disease_datasets = []
for disease, products_list in DISEASE_MAP.items():
    monthly_units = []
    for mc in month_cols:
        total = 0
        for prod in products_list:
            row = units_df[units_df['Product'].str.strip() == prod]
            if not row.empty:
                total += to_num(row[mc].values[0])
        monthly_units.append(int(total))
    disease_datasets.append({'label': disease, 'data': monthly_units})

# DELIVERY
deliv = pd.read_excel(f, sheet_name='Delivery Time Tracker')
deliv.columns = [str(c).strip().lower() for c in deliv.columns]
cu_c = [c for c in deliv.columns if 'customer' in c][0]
zo_c = [c for c in deliv.columns if 'zone' in c][0]
dr_c = [c for c in deliv.columns if 'drop' in c][0]
ti_c = [c for c in deliv.columns if 'total time' in c][0]
ty_c = [c for c in deliv.columns if 'status' in c][0]
deliv = deliv[deliv[cu_c].apply(lambda x: safe_str(x) != '')]
zone_cnt = deliv[zo_c].value_counts()
type_cnt = deliv[ty_c].value_counts()

# BUILD DATA OBJECT
top_cust_rev = cust_rev.sort_values(ascending=False)
top_prods    = products.head(3)
cust_top10   = top_cust_rev.head(10)

cust_table = []
for nm,rv in cust_top10.items():
    nm = safe_str(nm)
    cust_table.append({'name':nm,'region':rg_map.get(nm,''),'status':st_map.get(nm,''),
        'purchases':pc_map.get(nm,0),'revenue':round(rv),'expected':round(exp_map.get(nm,0))})

out_arr = []
for nm,bal in cust_bal.sort_values(ascending=False).items():
    nm = safe_str(nm); bal = round(bal)
    if bal > 0:
        inv_t = round(cust_rev.get(nm,0)); col = round(cust_pay.get(nm,0))
        rate = round(col/inv_t*100,1) if inv_t else 0
        out_arr.append({'name':nm,'invoice':inv_t,'collected':col,'outstanding':bal,'rate':rate})

freq_arr = []
for _,r in freq_df.iterrows():
    nm = safe_str(r['customer name'])
    freq_arr.append({'name':nm,'orders':int(r['orders']),'revenue':int(r['revenue']),'aov':int(r['aov'])})

deliv_table = []
for _,r in deliv.head(30).iterrows():
    deliv_table.append({'customer':safe_str(r[cu_c]),'zone':safe_str(r[zo_c]),
        'drop':safe_str(r[dr_c]),'time':safe_str(r[ti_c]),'type':safe_str(r[ty_c])})

DATA = {
    'scorecards': {
        'totalRevenue': round(tot_rev,2), 'collected': round(tot_col,2),
        'outstanding': round(tot_out,2), 'collRate': coll_rate, 'outRate': out_rate,
        'totalOrders': total_orders, 'deliveredOrders': total_orders,
        'fulfRate': 100, 'aov': aov, 'activeCust': act_c, 'totalCust': len(cust_s),
        'topCust': {'name': safe_str(top_cust_rev.index[0]), 'revenue': round(top_cust_rev.iloc[0])},
        'prod1': {'name': safe_str(top_prods.index[0]), 'revenue': round(top_prods.iloc[0])},
        'prod2': {'name': safe_str(top_prods.index[1]), 'revenue': round(top_prods.iloc[1])},
        'prod3': {'name': safe_str(top_prods.index[2]), 'revenue': round(top_prods.iloc[2])},
        'topPayMode': {'name': mode_cnt.index[0], 'count': int(mode_cnt.iloc[0]), 'share': round(mode_cnt.iloc[0]/mode_cnt.sum()*100,1)}
    },
    'monthly': {'labels':[MN[m] for m in monthly.index], 'revenue':[round(v) for v in monthly.values], 'targets':[0]*len(monthly)},
    'weekly': {
        'labels':['W'+str(int(n)) for n in wk['week number']],
        'revenue':[round(to_num(v)) for v in wk['value ghs']],
        'targets':[round(to_num(v)) for v in wk['weekly targets']],
        'aov':[round(to_num(v)) for v in wk['aov']],
        'orders':[round(to_num(v)) for v in wk['orders']]
    },
    'regions': {'labels':list(merged_reg.index), 'values':[round(v) for v in merged_reg.values]},
    'products': {'labels':list(products.head(10).index), 'values':[round(v) for v in products.head(10).values]},
    'customers': {
        'labels':list(cust_top10.index),
        'revenue':[round(v) for v in cust_top10.values],
        'expected':[round(exp_map.get(safe_str(n),0)) for n in cust_top10.index]
    },
    'salesperson': {'labels':list(rep_rev.index), 'revenue':[round(v) for v in rep_rev.values]},
    'paymentMode': {'labels':list(mode_cnt.index), 'values':[int(v) for v in mode_cnt.values]},
    'customerStatus': {'labels':['Active','Inactive'], 'values':[act_c, inact_c]},
    'custRegion': {'labels':list(cust_rg_ytd.index), 'values':[round(v) for v in cust_rg_ytd.values]},
    'delivZone': {'labels':list(zone_cnt.index), 'values':[int(v) for v in zone_cnt.values]},
    'delivType': {'labels':list(type_cnt.index), 'values':[int(v) for v in type_cnt.values]},
    'diseaseMonthly': {'labels': disease_labels, 'datasets': disease_datasets},
    'freqTable': freq_arr,
    'outstandingTable': out_arr,
    'custTable': cust_table,
    'delivTable': deliv_table
}

print(json.dumps(DATA))
