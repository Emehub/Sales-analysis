// ============================================================
//  SALES ANALYSIS DASHBOARD - Google Apps Script Web App
//  Paste this into: Google Sheets > Extensions > Apps Script
//  Then: Deploy > New Deployment > Web App > Anyone > Deploy
// ============================================================

function doGet(e) {
  try {
    var ss = SpreadsheetApp.openById('1kDStST-tcRZqB8OXfjtuoNqcTtYVv6W5ew0w0eZaPsI');
    var data = computeAllData(ss);
    return ContentService
      .createTextOutput(JSON.stringify(data))
      .setMimeType(ContentService.MimeType.JSON);
  } catch(err) {
    return ContentService
      .createTextOutput(JSON.stringify({ error: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function getSheetData(ss, name) {
  var sheet = ss.getSheetByName(name);
  if (!sheet) return { headers: [], rows: [] };
  var v = sheet.getDataRange().getValues();
  if (v.length < 2) return { headers: [], rows: [] };
  var headers = v[0].map(function(h){ return String(h).trim().toLowerCase(); });
  var rows = v.slice(1).filter(function(r){ return r.some(function(c){ return c !== '' && c !== null; }); });
  return { headers: headers, rows: rows };
}

function ci(headers, kw) {
  for (var i=0;i<headers.length;i++) if (headers[i].indexOf(kw.toLowerCase())!==-1) return i;
  return -1;
}

function toNum(v) { var n=parseFloat(String(v).replace(/,/g,'')); return isNaN(n)?0:n; }

function gSum(rows,ki,vi) {
  var m={};
  rows.forEach(function(r){
    var k=String(r[ki]||'').trim();
    if(k) m[k]=(m[k]||0)+toNum(r[vi]);
  });
  return m;
}

function gCount(rows,ki) {
  var m={};
  rows.forEach(function(r){
    var k=String(r[ki]||'').trim();
    if(k) m[k]=(m[k]||0)+1;
  });
  return m;
}

function sorted(map,top) {
  var a=Object.keys(map).map(function(k){return[k,map[k]];});
  a.sort(function(a,b){return b[1]-a[1];});
  return top?a.slice(0,top):a;
}

function getM(d) {
  if(!d) return -1;
  var dt=new Date(d);
  return isNaN(dt.getTime())?-1:dt.getMonth();
}

function computeAllData(ss) {
  var MN=['January','February','March','April','May','June','July','August','September','October','November','December'];

  var orders   = getSheetData(ss,'A-Sales Orders');
  var invoices = getSheetData(ss,'B-Invoices');
  var weekly   = getSheetData(ss,'Weekly Sales & Targets');
  var cust_s   = getSheetData(ss,'Customers');
  var deliv    = getSheetData(ss,'Delivery Time Tracker');

  // INVOICES
  var iCust=ci(invoices.headers,'customer name');
  var iTotal=ci(invoices.headers,'total');
  var iPay=ci(invoices.headers,'payment');
  var iBal=ci(invoices.headers,'balance');
  var iSales=ci(invoices.headers,'sales person');
  var iMode=ci(invoices.headers,'payment mode');

  var totRev=0,totCol=0,totOut=0;
  var cRevM={},cPayM={},cBalM={},repM={},modeM={};

  invoices.rows.forEach(function(r){
    totRev+=toNum(r[iTotal]);
    totCol+=toNum(r[iPay]);
    totOut+=toNum(r[iBal]);
    var c=String(r[iCust]||'').trim();
    if(c){cRevM[c]=(cRevM[c]||0)+toNum(r[iTotal]);cPayM[c]=(cPayM[c]||0)+toNum(r[iPay]);cBalM[c]=(cBalM[c]||0)+toNum(r[iBal]);}
    var rp=String(r[iSales]||'').trim();
    if(rp) repM[rp]=(repM[rp]||0)+toNum(r[iTotal]);
    var md=String(r[iMode]||'').trim();
    if(md) modeM[md]=(modeM[md]||0)+1;
  });

  // SALES ORDERS
  var oID=ci(orders.headers,'sales order id');
  var oDate=ci(orders.headers,'order date');
  var oReg=ci(orders.headers,'region');
  var oCust=ci(orders.headers,'customer name');
  var oItem=ci(orders.headers,'item name');
  var oSub=ci(orders.headers,'subtotal');

  var uIDs={},monM={},regM={},prodM={},coM={},crM={};

  orders.rows.forEach(function(r){
    var id=r[oID]; if(!id) return;
    uIDs[id]=1;
    var m=getM(r[oDate]); if(m>=0) monM[m]=(monM[m]||0)+toNum(r[oSub]);
    var rg=String(r[oReg]||'').trim(); if(rg) regM[rg]=(regM[rg]||0)+toNum(r[oSub]);
    var it=String(r[oItem]||'').trim(); if(it) prodM[it]=(prodM[it]||0)+toNum(r[oSub]);
    var ct=String(r[oCust]||'').trim();
    if(ct){if(!coM[ct])coM[ct]={};coM[ct][id]=1;crM[ct]=(crM[ct]||0)+toNum(r[oSub]);}
  });

  var totalOrders=Object.keys(uIDs).length;

  var monNums=Object.keys(monM).map(Number).sort(function(a,b){return a-b;});
  var monthLabels=monNums.map(function(m){return MN[m];});
  var monthRevenue=monNums.map(function(m){return Math.round(monM[m]);});

  var mergedReg={};
  Object.keys(regM).forEach(function(k){var kk=k.trim();mergedReg[kk]=(mergedReg[kk]||0)+regM[k];});
  var regS=sorted(mergedReg,10);

  var prodAllS=sorted(prodM);
  var prodS=prodAllS.slice(0,10);

  var freqArr=Object.keys(coM).map(function(n){
    var cnt=Object.keys(coM[n]).length;
    var rv=crM[n]||0;
    return{name:n,orders:cnt,revenue:Math.round(rv),aov:Math.round(rv/cnt)};
  }).sort(function(a,b){return b.orders-a.orders;}).slice(0,20);

  // WEEKLY
  var wN=ci(weekly.headers,'week number');
  var wV=ci(weekly.headers,'value ghs');
  var wT=ci(weekly.headers,'weekly targets');
  var wA=ci(weekly.headers,'aov');
  var wO=ci(weekly.headers,'orders');

  var vW=weekly.rows.filter(function(r){var n=toNum(r[wN]);var v=toNum(r[wV]);return n>0&&n<100&&v>0;})
    .sort(function(a,b){return toNum(a[wN])-toNum(b[wN]);});

  // CUSTOMERS
  var cN=ci(cust_s.headers,'customer name');
  var cR=ci(cust_s.headers,'region');
  var cSt=ci(cust_s.headers,'status');
  var cRY=ci(cust_s.headers,'revenue ytd');
  var cER=ci(cust_s.headers,'expected revenue');
  var cP=ci(cust_s.headers,'number of purchases');

  var vC=cust_s.rows.filter(function(r){return r[cN]&&r[cN]!=='';});
  var actC=0,inactC=0,crRM={},expM={};

  vC.forEach(function(r){
    var st=String(r[cSt]||'').toLowerCase();
    if(st.indexOf('active')!==-1&&st.indexOf('not')===-1) actC++; else inactC++;
    var rg=String(r[cR]||'').trim();
    if(rg) crRM[rg]=(crRM[rg]||0)+toNum(r[cRY]);
    expM[String(r[cN]).trim()]=toNum(r[cER]);
  });

  var cRS=sorted(cRevM,10);
  var custLabels=cRS.map(function(e){return e[0];});
  var custRev=cRS.map(function(e){return Math.round(e[1]);});
  var custExp=custLabels.map(function(n){return Math.round(expM[n]||0);});

  var outArr=sorted(cBalM).filter(function(e){return e[1]>0;}).map(function(e){
    var inv=cRevM[e[0]]||0; var col=cPayM[e[0]]||0;
    return{name:e[0],invoice:Math.round(inv),collected:Math.round(col),outstanding:Math.round(e[1]),rate:inv>0?Math.round(col/inv*1000)/10:0};
  });

  var custTableArr=cRS.map(function(e){
    var row=null;
    for(var i=0;i<vC.length;i++){if(String(vC[i][cN]).trim()===e[0]){row=vC[i];break;}}
    return{name:e[0],region:row?String(row[cR]||''):'',status:row?String(row[cSt]||''):'',purchases:row?Math.round(toNum(row[cP])):0,revenue:Math.round(e[1]),expected:Math.round(expM[e[0]]||0)};
  });

  // DELIVERY
  var dCu=ci(deliv.headers,'customer name');
  var dZo=ci(deliv.headers,'sales zone');
  var dDr=ci(deliv.headers,'drop site');
  var dTi=ci(deliv.headers,'total time');
  var dTy=ci(deliv.headers,'status');

  var vD=deliv.rows.filter(function(r){return r[dCu]&&r[dCu]!=='';});
  var zM=gCount(vD,dZo);
  var tyM=gCount(vD,dTy);
  var zS=sorted(zM); var tyS=sorted(tyM);

  var dTable=vD.slice(0,30).map(function(r){
    return{customer:String(r[dCu]||''),zone:String(r[dZo]||''),drop:String(r[dDr]||''),time:String(r[dTi]||''),type:String(r[dTy]||'')};
  });

  // COMPUTED SCORECARD FIELDS
  var collRate=totRev>0?Math.round(totCol/totRev*1000)/10:0;
  var outRate=Math.round((100-collRate)*10)/10;
  var aov=totalOrders>0?Math.round(totRev/totalOrders*100)/100:0;
  var repS=sorted(repM);

  // Top customer by revenue
  var custRevSorted=sorted(cRevM);
  var topCust=custRevSorted.length>0?{name:custRevSorted[0][0],revenue:Math.round(custRevSorted[0][1])}:null;

  // Top 3 products
  function makeProd(i){return prodAllS.length>i?{name:prodAllS[i][0],revenue:Math.round(prodAllS[i][1])}:null;}

  // Top payment mode
  var modeTotl=Object.keys(modeM).reduce(function(a,k){return a+modeM[k];},0);
  var modeTop=sorted(modeM);
  var topPayMode=modeTop.length>0?{name:modeTop[0][0],count:modeTop[0][1],share:modeTotl>0?Math.round(modeTop[0][1]/modeTotl*1000)/10:0}:null;

  return {
    lastUpdated: Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "dd MMM yyyy, HH:mm"),
    scorecards:{
      totalRevenue:  Math.round(totRev*100)/100,
      collected:     Math.round(totCol*100)/100,
      outstanding:   Math.round(totOut*100)/100,
      collRate:      collRate,
      outRate:       outRate,
      totalOrders:   totalOrders,
      deliveredOrders: totalOrders,
      fulfRate:      100,
      aov:           aov,
      activeCust:    actC,
      totalCust:     vC.length,
      topCust:       topCust,
      prod1:         makeProd(0),
      prod2:         makeProd(1),
      prod3:         makeProd(2),
      topPayMode:    topPayMode
    },
    monthly:{labels:monthLabels,revenue:monthRevenue,targets:monthLabels.map(function(){return 0;})},
    weekly:{labels:vW.map(function(r){return 'W'+Math.round(toNum(r[wN]));}),revenue:vW.map(function(r){return Math.round(toNum(r[wV]));}),targets:vW.map(function(r){return Math.round(toNum(r[wT]));}),aov:vW.map(function(r){return Math.round(toNum(r[wA]));}),orders:vW.map(function(r){return Math.round(toNum(r[wO]));})},
    regions:{labels:regS.map(function(e){return e[0];}),values:regS.map(function(e){return Math.round(e[1]);})},
    products:{labels:prodS.map(function(e){return e[0];}),values:prodS.map(function(e){return Math.round(e[1]);})},
    customers:{labels:custLabels,revenue:custRev,expected:custExp},
    salesperson:{labels:repS.map(function(e){return e[0];}),revenue:repS.map(function(e){return Math.round(e[1]);})},
    paymentMode:{labels:Object.keys(modeM),values:Object.values(modeM)},
    customerStatus:{labels:['Active','Inactive'],values:[actC,inactC]},
    custRegion:{labels:sorted(crRM,10).map(function(e){return e[0];}),values:sorted(crRM,10).map(function(e){return Math.round(e[1]);})},
    delivZone:{labels:zS.map(function(e){return e[0];}),values:zS.map(function(e){return e[1];})},
    delivType:{labels:tyS.map(function(e){return e[0];}),values:tyS.map(function(e){return e[1];})},
    freqTable:freqArr,
    outstandingTable:outArr,
    custTable:custTableArr,
    delivTable:dTable
  };
}
