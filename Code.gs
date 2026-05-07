// ============================================================
//  SALES LEDGER → DASHBOARD  |  Google Apps Script
//  Paste this entire file into Extensions → Apps Script,
//  then Deploy → New deployment → Web App
//  (Execute as: Me | Who has access: Anyone)
// ============================================================

// ⬇ Paste the original sheet's ID here (from the URL between /d/ and /edit)
const ORIGINAL_SHEET_ID = '1kDStST-tcRZqB8OXfjtuoNqcTtYVv6W5ew0w0eZaPsI';

function doGet(e) {
  try {
    const ss = SpreadsheetApp.openById(ORIGINAL_SHEET_ID);

    // Find sheets by name (case-insensitive fallback)
    function getSheet(name) {
      let sh = ss.getSheetByName(name);
      if (!sh) {
        // Try case-insensitive match
        const all = ss.getSheets();
        sh = all.find(s => s.getName().toLowerCase() === name.toLowerCase()) || null;
      }
      if (!sh) throw new Error('Sheet not found: "' + name + '". Available sheets: ' + ss.getSheets().map(s => s.getName()).join(', '));
      return sh;
    }

    const salesSheet   = getSheet('A-Sales Orders');
    const invoiceSheet = getSheet('B-Invoices');
    const custSheet    = getSheet('Customers');
    const weeklySheet  = getSheet('Weekly Sales & Targets');
    const delivSheet   = getSheet('Delivery Time Tracker');

    const salesData   = salesSheet.getDataRange().getValues();
    const invoiceData = invoiceSheet.getDataRange().getValues();
    const custData    = custSheet.getDataRange().getValues();
    const weeklyData  = weeklySheet.getDataRange().getValues();
    const delivData   = delivSheet.getDataRange().getValues();

    // ── Column indexes (0-based, row 0 = header) ──────────────
    // A-Sales Orders:  [1]OrderDate [3]Status [4]Channel [5]Region
    //   [7]CustomerName [8]ItemName [12]WarehouseName [17]InvoiceTotal
    //   [18]SalesPerson [21]WeekNum
    // B-Invoices:      [5]Total [6]Payment [7]Balance [10]PaymentMode
    //   [2]CustomerName
    // Customers:       [2]CustomerName [3]SalesZone [4]Region [5]Status
    //   [6]Purchases [7]RevenueYTD [8]ExpectedRevenue
    // Weekly S&T:      [0]Date [1]WeekNum [2]Orders [4]ValueGHS
    //   [6]AOV [7]WeeklyTargets
    // Delivery Tracker:[0]CustomerName [1]SalesZone [2]DropSite
    //   [6]TotalTime [9]Status

    const MONTHS = ['January','February','March','April','May','June',
                    'July','August','September','October','November','December'];

    // ── Helpers ───────────────────────────────────────────────
    function toDate(v) {
      if (v instanceof Date) return v;
      if (typeof v === 'number' && v > 20000) {
        // Excel serial date → JS Date (days since 1900-01-00, accounting for Excel's leap year bug)
        return new Date((v - 25569) * 86400 * 1000);
      }
      const d = new Date(v);
      return isNaN(d.getTime()) ? null : d;
    }
    function sortDesc(obj) {
      return Object.entries(obj).sort((a, b) => b[1] - a[1]);
    }
    function round(v) { return Math.round(parseFloat(v) || 0); }

    // ── 1. MONTHLY revenue & targets ─────────────────────────
    const monthRev = {}, monthTgt = {};
    let totalOrders = 0, deliveredOrders = 0;

    for (let i = 1; i < salesData.length; i++) {
      const r = salesData[i];
      if (!r[7] || !r[17]) continue;
      const d = toDate(r[1]);
      if (!d) continue;
      const m = MONTHS[d.getMonth()];
      monthRev[m] = (monthRev[m] || 0) + (parseFloat(r[17]) || 0);
      totalOrders++;
      if ((r[3] || '').toString().trim() === 'Delivered') deliveredOrders++;
    }
    for (let i = 1; i < weeklyData.length; i++) {
      const r = weeklyData[i];
      if (!r[0]) continue;
      const d = toDate(r[0]);
      if (!d) continue;
      const m = MONTHS[d.getMonth()];
      monthTgt[m] = (monthTgt[m] || 0) + (parseFloat(r[7]) || 0);
    }
    const monthLabels = Object.keys(monthRev).sort((a, b) => MONTHS.indexOf(a) - MONTHS.indexOf(b));

    // ── 2. WEEKLY data ────────────────────────────────────────
    const wLabels = [], wRev = [], wTgt = [], wAov = [], wOrders = [];
    for (let i = 1; i < weeklyData.length; i++) {
      const r = weeklyData[i];
      if (r[1] === '' || r[1] === null || r[1] === undefined || !r[4] && r[4] !== 0) continue;
      wLabels.push('W' + r[1]);
      wRev.push(round(r[4]));
      wTgt.push(round(r[7]));
      wAov.push(Math.round((parseFloat(r[6]) || 0) * 10) / 10);
      wOrders.push(parseInt(r[2]) || 0);
    }

    // ── 3. REGIONAL revenue ───────────────────────────────────
    const regionRev = {};
    for (let i = 1; i < salesData.length; i++) {
      const r = salesData[i];
      if (!r[5] || !r[17]) continue;
      const k = r[5].toString().trim();
      if (k) regionRev[k] = (regionRev[k] || 0) + (parseFloat(r[17]) || 0);
    }
    const sortedRegions = sortDesc(regionRev).slice(0, 10);

    // ── 4. PRODUCT revenue ────────────────────────────────────
    const prodRev = {};
    for (let i = 1; i < salesData.length; i++) {
      const r = salesData[i];
      if (!r[8] || !r[17]) continue;
      const k = r[8].toString().trim();
      if (k) prodRev[k] = (prodRev[k] || 0) + (parseFloat(r[17]) || 0);
    }
    const sortedProds = sortDesc(prodRev).slice(0, 10);

    // ── 5. CUSTOMER data ──────────────────────────────────────
    const custMap = {};
    for (let i = 1; i < custData.length; i++) {
      const r = custData[i];
      if (!r[2]) continue;
      const name = r[2].toString().trim();
      if (!name) continue;
      custMap[name] = {
        name,
        zone:      (r[3] || '').toString().trim(),
        region:    (r[4] || '').toString().trim(),
        status:    (r[5] || '').toString().trim(),
        purchases: parseInt(r[6]) || 0,
        revenue:   parseFloat(r[7]) || 0,
        expected:  parseFloat(r[8]) || 0
      };
    }
    const custArr = Object.values(custMap).sort((a, b) => b.revenue - a.revenue);
    const top10   = custArr.slice(0, 10);
    const active  = custArr.filter(c => c.status === 'Active').length;
    const inactive = custArr.filter(c => c.status === 'Inactive').length;

    const custRegionRev = {};
    for (const c of custArr) {
      const k = c.region || 'Unknown';
      custRegionRev[k] = (custRegionRev[k] || 0) + c.revenue;
    }
    const sortedCustRegion = sortDesc(custRegionRev).slice(0, 10);

    // ── 6. SALESPERSON revenue ────────────────────────────────
    const spRev = {};
    for (let i = 1; i < salesData.length; i++) {
      const r = salesData[i];
      if (!r[18] || !r[17]) continue;
      const k = r[18].toString().trim();
      if (k) spRev[k] = (spRev[k] || 0) + (parseFloat(r[17]) || 0);
    }
    const sortedSP = sortDesc(spRev);

    // ── 7. INVOICE totals & outstanding ──────────────────────
    let totalInvoiced = 0, totalCollected = 0, totalOutstanding = 0;
    const outMap = {};
    const payModes = {};
    for (let i = 1; i < invoiceData.length; i++) {
      const r = invoiceData[i];
      if (!r[5]) continue;
      totalInvoiced    += parseFloat(r[5]) || 0;
      totalCollected   += parseFloat(r[6]) || 0;
      const bal = parseFloat(r[7]) || 0;
      totalOutstanding += bal;
      if (bal > 0 && r[2]) {
        const name = r[2].toString().trim();
        if (!outMap[name]) outMap[name] = { name, invoice: 0, collected: 0, outstanding: 0 };
        outMap[name].invoice    += parseFloat(r[5]) || 0;
        outMap[name].collected  += parseFloat(r[6]) || 0;
        outMap[name].outstanding += bal;
      }
      if (r[10]) {
        const mode = r[10].toString().trim();
        if (mode) payModes[mode] = (payModes[mode] || 0) + 1;
      }
    }
    const sortedPay = sortDesc(payModes);
    const totalPayTxns = sortedPay.reduce((s, p) => s + p[1], 0);
    const outstandingTable = Object.values(outMap)
      .sort((a, b) => b.outstanding - a.outstanding)
      .slice(0, 30)
      .map(o => ({ ...o,
        invoice:     round(o.invoice),
        collected:   round(o.collected),
        outstanding: round(o.outstanding),
        rate: o.invoice > 0 ? Math.round((o.collected / o.invoice) * 1000) / 10 : 0
      }));

    // ── 8. DELIVERY data ──────────────────────────────────────
    const delivZone = {}, delivType = { Farmer: 0, Agrovet: 0 };
    for (let i = 1; i < salesData.length; i++) {
      const r = salesData[i];
      const wh = (r[12] || '').toString().trim();
      if (wh) delivZone[wh] = (delivZone[wh] || 0) + 1;
      const ch = (r[4] || '').toString().trim();
      if (ch === 'Farmer') delivType.Farmer++;
      else if (ch === 'Agrovet') delivType.Agrovet++;
    }
    const sortedDelivZone = sortDesc(delivZone).slice(0, 8);

    const delivTable = [];
    for (let i = 1; i < delivData.length && delivTable.length < 30; i++) {
      const r = delivData[i];
      if (!r[0]) continue;
      delivTable.push({
        customer: r[0].toString().trim(),
        zone:     (r[1] || '').toString().trim(),
        drop:     (r[2] || '').toString().trim(),
        time:     (r[6] || '').toString().trim(),
        type:     (r[9] || '').toString().trim()
      });
    }

    // ── 9. ORDER FREQUENCY table ──────────────────────────────
    const orderCount = {}, lastOrderDate = {};
    for (let i = 1; i < salesData.length; i++) {
      const r = salesData[i];
      if (!r[7]) continue;
      const name = r[7].toString().trim();
      orderCount[name] = (orderCount[name] || 0) + 1;
      const d = toDate(r[1]);
      if (d && (!lastOrderDate[name] || d > lastOrderDate[name])) lastOrderDate[name] = d;
    }
    const freqTable = Object.entries(orderCount)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 25)
      .map(([name, orders]) => {
        const c = custMap[name] || {};
        const revenue = round(c.revenue || 0);
        const lastD   = lastOrderDate[name];
        const last    = lastD
          ? lastD.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
          : '';
        return { name, orders, revenue, aov: orders > 0 ? Math.round(revenue / orders) : 0, last };
      });

    // ── 10. CUSTOMER table ────────────────────────────────────
    const custTable = custArr.slice(0, 25).map(c => ({
      name:      c.name,
      region:    c.region,
      status:    c.status,
      purchases: c.purchases,
      revenue:   round(c.revenue),
      expected:  round(c.expected)
    }));

    // ── 11. SCORECARDS ────────────────────────────────────────
    const collRate  = totalInvoiced > 0 ? Math.round((totalCollected / totalInvoiced) * 1000) / 10 : 0;
    const outRate   = 100 - collRate;
    const aov       = totalOrders > 0 ? Math.round(totalInvoiced / totalOrders * 100) / 100 : 0;
    const fulfRate  = totalOrders > 0 ? Math.round((deliveredOrders / totalOrders) * 100) : 0;
    const topCust   = custArr[0] || null;
    const topPay    = sortedPay[0] || null;
    const topPayShare = topPay && totalPayTxns > 0
      ? Math.round((topPay[1] / totalPayTxns) * 1000) / 10 : 0;
    const prod1 = sortedProds[0] || null;
    const prod2 = sortedProds[1] || null;
    const prod3 = sortedProds[2] || null;

    // ── Build response ────────────────────────────────────────
    const result = {
      scorecards: {
        totalRevenue:   round(totalInvoiced),
        collected:      round(totalCollected),
        outstanding:    round(totalOutstanding),
        collRate,
        outRate,
        totalOrders,
        deliveredOrders,
        aov:            Math.round(aov * 100) / 100,
        activeCust:     active,
        totalCust:      active + inactive,
        fulfRate,
        topCust:        topCust ? { name: topCust.name, revenue: round(topCust.revenue) } : null,
        topPayMode:     topPay  ? { name: topPay[0], count: topPay[1], share: topPayShare } : null,
        prod1: prod1 ? { name: prod1[0], revenue: round(prod1[1]) } : null,
        prod2: prod2 ? { name: prod2[0], revenue: round(prod2[1]) } : null,
        prod3: prod3 ? { name: prod3[0], revenue: round(prod3[1]) } : null
      },
      monthly: {
        labels:  monthLabels,
        revenue: monthLabels.map(m => round(monthRev[m] || 0)),
        targets: monthLabels.map(m => round(monthTgt[m] || 0))
      },
      weekly:  { labels: wLabels, revenue: wRev, targets: wTgt, aov: wAov, orders: wOrders },
      regions: { labels: sortedRegions.map(r => r[0]), values: sortedRegions.map(r => round(r[1])) },
      products:{ labels: sortedProds.map(p => p[0]),   values: sortedProds.map(p => round(p[1]))   },
      customers: {
        labels:    top10.map(c => c.name),
        revenue:   top10.map(c => round(c.revenue)),
        expected:  top10.map(c => round(c.expected)),
        salesZone: top10.map(c => c.zone)
      },
      salesperson: { labels: sortedSP.map(s => s[0]), revenue: sortedSP.map(s => round(s[1])) },
      paymentMode: { labels: sortedPay.map(p => p[0]), values: sortedPay.map(p => p[1]) },
      customerStatus: { labels: ['Active', 'Inactive'], values: [active, inactive] },
      custRegion: {
        labels: sortedCustRegion.map(r => r[0]),
        values: sortedCustRegion.map(r => round(r[1]))
      },
      delivZone: {
        labels: sortedDelivZone.map(d => d[0]),
        values: sortedDelivZone.map(d => d[1])
      },
      delivType:       { labels: ['Farmer', 'Agrovet'], values: [delivType.Farmer, delivType.Agrovet] },
      freqTable,
      outstandingTable,
      custTable,
      delivTable
    };

    const jsonStr = JSON.stringify(result);
    const cb = e && e.parameter && e.parameter.callback;
    if (cb) {
      return ContentService
        .createTextOutput(cb + '(' + jsonStr + ')')
        .setMimeType(ContentService.MimeType.JAVASCRIPT);
    }
    return ContentService
      .createTextOutput(jsonStr)
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    const errJson = JSON.stringify({ error: err.toString(), stack: err.stack });
    const cb = e && e.parameter && e.parameter.callback;
    if (cb) {
      return ContentService
        .createTextOutput(cb + '(' + errJson + ')')
        .setMimeType(ContentService.MimeType.JAVASCRIPT);
    }
    return ContentService
      .createTextOutput(errJson)
      .setMimeType(ContentService.MimeType.JSON);
  }
}
