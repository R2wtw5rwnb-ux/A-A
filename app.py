from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import json
import re
import ssl
import urllib.parse
import urllib.request
import html as html_lib
from datetime import datetime, timezone

app = FastAPI()
HTML = '<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="theme-color" content="#0b0c0f">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n<title>Tesla Model S 全国试驾车 · 车辆档案版</title>\n<style>\n:root{color-scheme:dark;--bg:#0b0c0f;--panel:#14161a;--panel2:#101216;--line:#292d34;--text:#f5f7fa;--muted:#9aa1ab;--green:#57d792;--red:#ff7373;--amber:#ffd166;--blue:#86b7ff}\n*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 90% -10%,rgba(255,255,255,.08),transparent 30rem),var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","SF Pro Display","Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}\nbutton,input,select{font:inherit}.app{max-width:1120px;margin:auto;padding:max(22px,env(safe-area-inset-top)) 16px calc(44px + env(safe-area-inset-bottom))}\nheader{display:flex;justify-content:space-between;gap:14px;align-items:flex-start}.eyebrow{font-size:11px;letter-spacing:.15em;color:var(--muted);font-weight:700}h1{margin:8px 0 6px;font-size:clamp(28px,6vw,44px);letter-spacing:-.04em}.sub{margin:0;color:var(--muted);font-size:13px;line-height:1.55;max-width:720px}\n.btn{border:1px solid var(--line);background:#1a1d22;color:var(--text);border-radius:13px;min-height:44px;padding:0 15px;font-weight:700;cursor:pointer}.btn.loading{opacity:.65}.status{display:flex;align-items:center;gap:8px;margin:18px 0 12px;color:var(--muted);font-size:12px}.dot{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 0 4px rgba(87,215,146,.09)}.status.error .dot{background:var(--red);box-shadow:0 0 0 4px rgba(255,115,115,.09)}#updated{margin-left:auto}\n.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.metric{background:var(--panel);border:1px solid var(--line);border-radius:17px;padding:15px;min-height:105px}.mlabel{font-size:11px;color:var(--muted)}.mvalue{font-size:29px;font-weight:800;letter-spacing:-.04em;margin-top:9px}.mvalue.small{font-size:21px}.mfoot{font-size:10px;color:var(--muted);margin-top:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}\n.toolbar{margin-top:12px;background:var(--panel);border:1px solid var(--line);border-radius:17px;padding:15px}.toolbar-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}.toolbar h2{font-size:16px;margin:0}.toolbar small{color:var(--muted)}\n.filters{display:grid;grid-template-columns:repeat(6,1fr);gap:9px}.filters label{display:flex;flex-direction:column;gap:5px}.filters span{font-size:10px;color:var(--muted)}input,select{min-height:41px;width:100%;border:1px solid var(--line);background:var(--panel2);color:var(--text);border-radius:10px;padding:0 10px;outline:none}\n.result-head{display:flex;justify-content:space-between;align-items:end;gap:10px;margin:22px 2px 10px}.result-head h2{margin:0;font-size:17px}.result-head p{margin:4px 0 0;color:var(--muted);font-size:11px}\n.list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:11px}.card{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:15px}.card.drop{border-color:rgba(87,215,146,.42)}.top{display:flex;justify-content:space-between;gap:12px}.badges{display:flex;gap:5px;flex-wrap:wrap}.badge{display:inline-flex;align-items:center;min-height:22px;padding:0 8px;border-radius:99px;background:#24282e;font-size:10px;font-weight:700}.badge.demo{background:#f4f5f6;color:#0b0c0f}.badge.good{background:rgba(87,215,146,.1);color:var(--green)}.badge.warn{background:rgba(255,209,102,.1);color:var(--amber)}.badge.bad{background:rgba(255,115,115,.1);color:var(--red)}.badge.info{background:rgba(134,183,255,.1);color:var(--blue)}\n.title{font-size:18px;font-weight:800;margin:9px 0 4px}.loc{font-size:11px;color:var(--muted)}.price{text-align:right;flex:0 0 auto}.price strong{font-size:22px;letter-spacing:-.04em}.change{font-size:10px;color:var(--muted);margin-top:5px}.change.down{color:var(--green);font-weight:700}.change.up{color:var(--red);font-weight:700}\n.specs{display:grid;grid-template-columns:repeat(4,1fr);margin-top:14px;border:1px solid #23272d;border-radius:12px;overflow:hidden;background:var(--panel2)}.spec{padding:10px 8px;border-right:1px solid #23272d}.spec:last-child{border-right:0}.spec span{display:block;font-size:9px;color:var(--muted);margin-bottom:4px}.spec b{display:block;font-size:11px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}\n.archive{margin-top:12px;border:1px solid #252a31;border-radius:12px;background:#111318;overflow:hidden}.archive summary{list-style:none;cursor:pointer;padding:12px;display:flex;justify-content:space-between;align-items:center;font-size:12px;font-weight:750}.archive summary::-webkit-details-marker{display:none}.archive summary:after{content:"＋";color:var(--muted);font-size:16px}.archive[open] summary:after{content:"－"}.archive-body{border-top:1px solid #252a31;padding:12px}.archive-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}.row{background:#0d0f12;border:1px solid #20242a;border-radius:10px;padding:9px}.row span{display:block;color:var(--muted);font-size:9px;margin-bottom:4px}.row b{font-size:11px;word-break:break-word}\n.docs{margin-top:10px}.docs-title{font-size:11px;font-weight:800;margin-bottom:7px}.doclink{display:block;color:#dce8ff;text-decoration:none;background:#101722;border:1px solid #22334f;border-radius:9px;padding:9px 10px;margin-top:6px;font-size:11px;word-break:break-all}.searchlink{display:inline-block;margin-top:8px;color:var(--blue);font-size:11px;text-decoration:none}.note{margin-top:9px;color:#727985;font-size:9px;line-height:1.55}\n.bottom{margin-top:11px;display:flex;justify-content:space-between;gap:10px;align-items:center}.vin{font:9px ui-monospace,SFMono-Regular,Menlo,monospace;color:#757c87;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.tesla{color:#fff;text-decoration:none;font-size:11px;font-weight:800;white-space:nowrap}\n.empty{border:1px dashed #343941;border-radius:17px;padding:42px 18px;text-align:center;color:var(--muted);margin-top:12px}.empty h3{color:#fff;margin:0 0 8px}.empty p{font-size:12px;line-height:1.6;margin:0 auto;max-width:580px}.hidden{display:none!important}.footer{margin:20px 3px 0;color:#646b75;font-size:9px;line-height:1.6}\n@media(max-width:840px){.metrics{grid-template-columns:repeat(2,1fr)}.filters{grid-template-columns:repeat(3,1fr)}.list{grid-template-columns:1fr}}\n@media(max-width:560px){.app{padding-left:13px;padding-right:13px}.btn .txt{display:none}.btn{width:44px;padding:0}.filters{grid-template-columns:repeat(2,1fr)}.filters .wide{grid-column:span 2}.specs{grid-template-columns:repeat(2,1fr)}.spec:nth-child(2){border-right:0}.spec:nth-child(-n+2){border-bottom:1px solid #23272d}.archive-grid{grid-template-columns:1fr}.metric{min-height:98px}}\n</style>\n</head>\n<body>\n<div class="app">\n<header>\n  <div><div class="eyebrow">TESLA CHINA · INVENTORY + VEHICLE ARCHIVE</div><h1>Model S 全国试驾车</h1><p class="sub">价格、里程、地区与 Tesla 库存接口公开的车辆历史/损伤披露/整备状态等字段放在同一页。仅展示公开信息，不访问车主账号或内部维修系统。</p></div>\n  <button class="btn" id="refresh">↻ <span class="txt">刷新</span></button>\n</header>\n\n<div class="status"><span class="dot"></span><span id="statusText">准备查询…</span><span id="updated">—</span></div>\n\n<section class="metrics">\n  <div class="metric"><div class="mlabel">全国试驾车</div><div class="mvalue" id="mCount">—</div><div class="mfoot">当前查询结果</div></div>\n  <div class="metric"><div class="mlabel">最低价格</div><div class="mvalue small" id="mLow">—</div><div class="mfoot" id="mLowCity">—</div></div>\n  <div class="metric"><div class="mlabel">本次降价</div><div class="mvalue" id="mDrops">—</div><div class="mfoot">与本机上次记录相比</div></div>\n  <div class="metric"><div class="mlabel">有车况披露</div><div class="mvalue" id="mDisclosure">—</div><div class="mfoot">损伤披露/非 CLEAN/公开记录</div></div>\n</section>\n\n<section class="toolbar">\n  <div class="toolbar-top"><div><h2>筛选</h2><small>车辆档案字段来自 Tesla 当前公开库存返回</small></div><button class="btn" id="reset">重置</button></div>\n  <div class="filters">\n    <label><span>省份</span><select id="province"><option value="">全部</option></select></label>\n    <label class="wide"><span>城市</span><input id="city" placeholder="输入城市"></label>\n    <label><span>车况</span><select id="history"><option value="">全部</option><option value="disclosure">有披露/非 CLEAN</option><option value="clean">CLEAN</option><option value="docs">有公开文件链接</option></select></label>\n    <label><span>最高价格</span><input id="maxPrice" inputmode="numeric" placeholder="例如 600000"></label>\n    <label><span>最高里程</span><input id="maxKm" inputmode="numeric" placeholder="例如 5000"></label>\n    <label><span>排序</span><select id="sort"><option value="price">价格最低</option><option value="drop">降价最多</option><option value="km">里程最低</option><option value="history">有披露优先</option></select></label>\n  </div>\n</section>\n\n<div class="result-head"><div><h2>车辆列表</h2><p id="resultText">—</p></div><div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end"><button class="btn" id="workorders">整理≤50万工单</button><button class="btn" id="csv">CSV</button></div></div>\n<div id="list" class="list"></div>\n<div id="empty" class="empty hidden"><h3>没有匹配车辆</h3><p>可能当前没有 Model S 试驾车，或筛选条件过窄。也可能 Tesla 临时限制了库存接口。</p></div>\n<div id="error" class="empty hidden"><h3>暂时无法读取 Tesla 库存</h3><p id="errorText"></p></div>\n\n<div class="footer">说明：VehicleHistory、DamageDisclosure、DamageDisclosureStatus、CPORefurbishmentStatus 等为 Tesla 公开库存接口字段。它们不等同于完整维修历史。完整车主服务历史/内部工单通常需要经过 Tesla 账号授权，本页面不会尝试绕过权限获取。</div>\n</div>\n\n<template id="cardTpl">\n<article class="card">\n  <div class="top">\n    <div><div class="badges"></div><div class="title"></div><div class="loc"></div></div>\n    <div class="price"><strong></strong><div class="change"></div></div>\n  </div>\n  <div class="specs">\n    <div class="spec"><span>里程</span><b class="km"></b></div>\n    <div class="spec"><span>年份</span><b class="year"></b></div>\n    <div class="spec"><span>外观</span><b class="paint"></b></div>\n    <div class="spec"><span>内饰</span><b class="interior"></b></div>\n  </div>\n  <details class="archive">\n    <summary>车辆档案 / 公开车况字段</summary>\n    <div class="archive-body">\n      <div class="archive-grid"></div>\n      <div class="docs"></div>\n      <div class="note">“未发现公开字段/文件”不代表车辆从未维修；这里只表示当前 Tesla 公开库存数据未提供相应信息。</div>\n    </div>\n  </details>\n  <div class="bottom"><div class="vin"></div><a class="tesla" target="_blank" rel="noopener">Tesla 官网详情 →</a></div>\n</article>\n</template>\n\n<script>\nconst $=id=>document.getElementById(id);\nconst state={cars:[],filtered:[],prev:JSON.parse(localStorage.getItem(\'tesla_ms_archive_prices\')||\'{}\'),workLoading:false};\nconst yuan=n=>Number.isFinite(Number(n))?\'¥\'+Math.round(Number(n)).toLocaleString(\'zh-CN\'):\'—\';\nconst val=v=>(v===null||v===undefined||v===\'\')?\'—\':String(v);\nconst bool=v=>v===true?\'是\':v===false?\'否\':\'—\';\nfunction dt(v){if(!v)return\'—\';const d=new Date(v);return isNaN(d)?String(v):d.toLocaleDateString(\'zh-CN\')}\nfunction histLabel(v){if(!v)return\'未提供\';const s=String(v).toUpperCase();if(s===\'CLEAN\')return\'CLEAN\';return String(v)}\nfunction hasDisclosure(c){return c.damageDisclosure===true || (c.vehicleHistory && String(c.vehicleHistory).toUpperCase()!==\'CLEAN\') || (c.publicDocs||[]).length>0 || (c.workOrderLinks||[]).length>0}\nfunction badge(el,text,cls=\'\'){const s=document.createElement(\'span\');s.className=\'badge \'+cls;s.textContent=text;el.appendChild(s)}\nfunction historyClass(c){if(c.damageDisclosure===true || (c.vehicleHistory && String(c.vehicleHistory).toUpperCase()!==\'CLEAN\'))return\'bad\';if(String(c.vehicleHistory||\'\').toUpperCase()===\'CLEAN\')return\'good\';return\'info\'}\n\nasync function load(){\n  $(\'refresh\').classList.add(\'loading\'); document.querySelector(\'.status\').classList.remove(\'error\'); $(\'statusText\').textContent=\'正在读取 Tesla 中国公开库存…\';\n  $(\'error\').classList.add(\'hidden\');\n  try{\n    const r=await fetch(\'/api/inventory\',{cache:\'no-store\'}); const data=await r.json();\n    if(!r.ok||!data.ok) throw new Error(data.error||data.hint||\'请求失败\');\n    const newPrev={};\n    state.cars=(data.cars||[]).map(c=>{\n      const p=Number(c.price); const old=Number(state.prev[c.vin]);\n      c.change=(Number.isFinite(p)&&Number.isFinite(old))?p-old:0;\n      c.isNew=!(c.vin in state.prev);\n      if(Number.isFinite(p))newPrev[c.vin]=p;\n      return c;\n    });\n    localStorage.setItem(\'tesla_ms_archive_prices\',JSON.stringify(newPrev)); state.prev=newPrev;\n    fillProvince(); apply(); $(\'statusText\').textContent=`已读取 ${state.cars.length} 辆 Model S 试驾车 · ${data.source||\'Tesla\'}`;\n    $(\'updated\').textContent=new Date(data.fetchedAt||Date.now()).toLocaleTimeString(\'zh-CN\',{hour:\'2-digit\',minute:\'2-digit\'});\n  }catch(e){\n    state.cars=[]; render(); document.querySelector(\'.status\').classList.add(\'error\'); $(\'statusText\').textContent=\'读取失败\';\n    $(\'errorText\').textContent=e.message+\'。如果网页能打开但长期无法读取，可能是 Tesla 对云服务器请求做了临时限制。\'; $(\'error\').classList.remove(\'hidden\');\n  }finally{$(\'refresh\').classList.remove(\'loading\')}\n}\nfunction fillProvince(){\n  const cur=$(\'province\').value; const ps=[...new Set(state.cars.map(c=>c.province).filter(Boolean))].sort();\n  $(\'province\').innerHTML=\'<option value="">全部</option>\'+ps.map(p=>`<option>${escapeHtml(p)}</option>`).join(\'\'); $(\'province\').value=ps.includes(cur)?cur:\'\';\n}\nfunction apply(){\n  const p=$(\'province\').value,city=$(\'city\').value.trim().toLowerCase(),h=$(\'history\').value,maxP=Number($(\'maxPrice\').value)||Infinity,maxK=Number($(\'maxKm\').value)||Infinity;\n  let arr=state.cars.filter(c=>{\n    if(p&&c.province!==p)return false;\n    if(city&&!String(c.city||\'\').toLowerCase().includes(city))return false;\n    if(Number(c.price)>maxP)return false;\n    if(Number(c.odometer)>maxK)return false;\n    if(h===\'disclosure\'&&!hasDisclosure(c))return false;\n    if(h===\'clean\'&&String(c.vehicleHistory||\'\').toUpperCase()!==\'CLEAN\')return false;\n    if(h===\'docs\'&&!(c.publicDocs||[]).length)return false;\n    return true;\n  });\n  const s=$(\'sort\').value;\n  if(s===\'price\')arr.sort((a,b)=>(a.price??1e18)-(b.price??1e18));\n  if(s===\'drop\')arr.sort((a,b)=>(a.change||0)-(b.change||0));\n  if(s===\'km\')arr.sort((a,b)=>(a.odometer??1e18)-(b.odometer??1e18));\n  if(s===\'history\')arr.sort((a,b)=>(hasDisclosure(b)?1:0)-(hasDisclosure(a)?1:0)||(a.price??1e18)-(b.price??1e18));\n  state.filtered=arr; render();\n}\nfunction render(){\n  const list=$(\'list\'); list.innerHTML=\'\'; $(\'empty\').classList.toggle(\'hidden\',state.filtered.length>0||state.cars.length===0);\n  const drops=state.cars.filter(c=>c.change<0).length; const disclosed=state.cars.filter(hasDisclosure).length; const low=[...state.cars].filter(c=>Number.isFinite(Number(c.price))).sort((a,b)=>a.price-b.price)[0];\n  $(\'mCount\').textContent=state.cars.length||\'0\'; $(\'mDrops\').textContent=drops; $(\'mDisclosure\').textContent=disclosed; $(\'mLow\').textContent=low?yuan(low.price):\'—\'; $(\'mLowCity\').textContent=low?[low.province,low.city].filter(Boolean).join(\' · \')||\'—\':\'—\';\n  $(\'resultText\').textContent=`显示 ${state.filtered.length} / ${state.cars.length} 辆`;\n  for(const c of state.filtered){\n    const n=$(\'cardTpl\').content.firstElementChild.cloneNode(true); if(c.change<0)n.classList.add(\'drop\');\n    const bs=n.querySelector(\'.badges\'); badge(bs,\'试驾车\',\'demo\');\n    if(c.isNew)badge(bs,\'新车源\',\'warn\');\n    if(c.change<0)badge(bs,\'降价\',\'good\');\n    if(c.vehicleHistory)badge(bs,histLabel(c.vehicleHistory),historyClass(c));\n    if(c.damageDisclosure===true)badge(bs,\'损伤披露\',\'bad\');\n    if((c.publicDocs||[]).length)badge(bs,`公开文件 ${c.publicDocs.length}`,\'info\');\n    if((c.workOrderLinks||[]).length)badge(bs,`工单 ${(c.workOrderLinks||[]).length}`,\'good\');\n    n.querySelector(\'.title\').textContent=c.trim||\'Model S\'; n.querySelector(\'.loc\').textContent=[c.province,c.city].filter(Boolean).join(\' · \')||\'地区未提供\';\n    n.querySelector(\'.price strong\').textContent=yuan(c.price); const ch=n.querySelector(\'.change\');\n    if(c.change<0){ch.textContent=`↓ ${yuan(Math.abs(c.change))}`;ch.classList.add(\'down\')}else if(c.change>0){ch.textContent=`↑ ${yuan(c.change)}`;ch.classList.add(\'up\')}else ch.textContent=c.listedReduction>0?`官网优惠 ${yuan(c.listedReduction)}`:\'—\';\n    n.querySelector(\'.km\').textContent=Number.isFinite(Number(c.odometer))?`${Math.round(c.odometer).toLocaleString()} ${c.odometerUnit||\'km\'}`:\'—\'; n.querySelector(\'.year\').textContent=val(c.year); n.querySelector(\'.paint\').textContent=val(c.paint); n.querySelector(\'.interior\').textContent=val(c.interior);\n    const ag=n.querySelector(\'.archive-grid\');\n    const rows=[\n      [\'车辆历史\',histLabel(c.vehicleHistory)],[\'损伤披露\',bool(c.damageDisclosure)],\n      [\'披露状态\',val(c.damageDisclosureStatus)],[\'官方整备状态\',val(c.cpoRefurbishmentStatus)],\n      [\'是否有损伤照片\',bool(c.hasDamagePhotos)],[\'车辆子类型\',val(c.vehicleSubType)],\n      [\'车辆来源\',val(c.acquisitionSubType)],[\'是否车队车\',bool(c.fleetVehicle)],\n      [\'产权类型\',val(c.titleSubtype)],[\'出厂/下线日期\',dt(c.factoryGatedDate)],\n      [\'首次登记日期\',dt(c.firstRegistrationDate)],[\'公开续航\',Number.isFinite(Number(c.actualRange))?`${Math.round(c.actualRange)} ${c.actualRangeUnit||\'\'}`:\'—\'],\n      [\'整车保修\',c.warrantyVehicleYear?`${c.warrantyVehicleYear} 年 / ${Number(c.warrantyMile||0).toLocaleString()} ${c.odometerUnit||\'km\'}`:\'—\'],\n      [\'电池保修\',c.warrantyBatteryYear?`${c.warrantyBatteryYear} 年 / ${Number(c.warrantyBatteryMile||0).toLocaleString()} ${c.odometerUnit||\'km\'}`:\'—\']\n    ];\n    rows.forEach(([k,v])=>{const d=document.createElement(\'div\');d.className=\'row\';d.innerHTML=`<span>${escapeHtml(k)}</span><b>${escapeHtml(v)}</b>`;ag.appendChild(d)});\n    const docs=n.querySelector(\'.docs\'); docs.innerHTML=\'<div class="docs-title">Tesla 公开工单 / 披露文件</div>\';\n    (c.workOrderLinks||[]).forEach((u,i)=>{const a=document.createElement(\'a\');a.className=\'doclink\';a.target=\'_blank\';a.rel=\'noopener\';a.href=u;a.textContent=`工单 ${i+1}`;docs.appendChild(a)});\n    if(c.workOrderError){const e=document.createElement(\'div\');e.className=\'note\';e.textContent=\'工单读取提示：\'+c.workOrderError;docs.appendChild(e)}\n    (c.publicDocs||[]).filter(d=>!(c.workOrderLinks||[]).includes(d.url)).forEach((d,i)=>{const a=document.createElement(\'a\');a.className=\'doclink\';a.target=\'_blank\';a.rel=\'noopener\';a.href=d.url;a.textContent=d.label||`公开文件 ${i+1}`;docs.appendChild(a)});\n    const search=document.createElement(\'a\');search.className=\'searchlink\';search.target=\'_blank\';search.rel=\'noopener\';search.href=c.officialSearchUrl;search.textContent=\'按 VIN 搜索 Tesla 官方公开文件 →\';docs.appendChild(search);\n    n.querySelector(\'.vin\').textContent=c.vin?`VIN · ${c.vin}`:\'VIN 未提供\'; const a=n.querySelector(\'.tesla\');a.href=c.url||\'https://www.tesla.cn/inventory/new/ms\';\n    list.appendChild(n);\n  }\n}\nfunction escapeHtml(v){return String(v??\'\').replace(/[&<>\'"]/g,ch=>({\'&\':\'&amp;\',\'<\':\'&lt;\',\'>\':\'&gt;\',"\'":\'&#39;\',\'"\':\'&quot;\'}[ch]))}\nfunction reset(){[\'province\',\'city\',\'history\',\'maxPrice\',\'maxKm\'].forEach(id=>$(id).value=\'\');$(\'sort\').value=\'price\';apply()}\nasync function loadWorkorders(){\n  if(state.workLoading)return;\n  const targets=state.cars.filter(c=>Number(c.price)<500000);\n  if(!targets.length){alert(\'当前没有50万元以下车辆\');return}\n  state.workLoading=true; const btn=$(\'workorders\');btn.classList.add(\'loading\');btn.textContent=\'正在整理工单…\';\n  let directCars=0,directLinks=0;\n  for(const c of targets){\n    const current=[...(c.workOrderLinks||[])];\n    const fromDocs=(c.publicDocs||[]).map(d=>d.url).filter(u=>/\\/files\\/[0-9a-f-]{36}/i.test(String(u||\'\')));\n    c.workOrderLinks=[...new Set([...current,...fromDocs])];\n    if(c.workOrderLinks.length){directCars++; directLinks+=c.workOrderLinks.length}\n  }\n  apply();\n  $(\'statusText\').textContent=`库存原始字段：${directCars}/${targets.length} 辆发现 ${directLinks} 张公开文件；正在尝试详情页补充…`;\n  let done=0,extraCars=0,idx=0;\n  async function worker(){\n    while(true){\n      const i=idx++; if(i>=targets.length)break; const c=targets[i];\n      try{\n        const r=await fetch(\'/api/workorders?vin=\'+encodeURIComponent(c.vin),{cache:\'no-store\'}); const d=await r.json();\n        if(r.ok&&d.ok){\n          const before=(c.workOrderLinks||[]).length;\n          c.workOrderLinks=[...new Set([...(c.workOrderLinks||[]),...(d.links||[])])];\n          if(c.workOrderLinks.length>before)extraCars++;\n          c.workOrderSource=d.source||\'\'; c.workOrderError=\'\';\n        }else{c.workOrderError=d.error||\'详情页未返回可解析工单\'}\n      }catch(e){c.workOrderError=e.message||String(e)}\n      done++; $(\'statusText\').textContent=`工单整理 ${done}/${targets.length} · 库存字段 ${directCars} 辆 / ${directLinks} 张 · 详情页新增 ${extraCars} 辆`;\n      if(done%3===0||done===targets.length)apply();\n    }\n  }\n  await Promise.all([worker(),worker(),worker()]);\n  const finalCars=targets.filter(c=>(c.workOrderLinks||[]).length).length;\n  const finalLinks=targets.reduce((n,c)=>n+(c.workOrderLinks||[]).length,0);\n  state.workLoading=false;btn.classList.remove(\'loading\');btn.textContent=\'重新整理≤50万工单\';\n  if(finalLinks===0){\n    $(\'statusText\').textContent=\'24辆均未从服务器侧拿到工单链接。请直接导出CSV给我；V5会把Tesla原始披露/GUID字段一起导出用于定位。\';\n  }else{\n    $(\'statusText\').textContent=`工单整理完成：${finalCars}/${targets.length} 辆，共 ${finalLinks} 张公开工单/文件`;\n  }\n}\nfunction csv(){\n  const head=[\'省份\',\'城市\',\'版本\',\'年份\',\'里程\',\'当前价格\',\'价格变化\',\'VehicleHistory\',\'DamageDisclosure\',\'DamageDisclosureStatus\',\'CPORefurbishmentStatus\',\'HasDamagePhotos\',\'VehicleSubType\',\'AcquisitionSubType\',\'FleetVehicle\',\'TitleSubtype\',\'FactoryGatedDate\',\'FirstRegistrationDate\',\'VIN\',\'DamageDisclosureGuids\',\'InspectionDocumentGuid\',\'工单数量\',\'工单链接\',\'Tesla原始工单相关字段\',\'官网链接\'];\n  const rows=state.filtered.map(c=>[c.province,c.city,c.trim,c.year,c.odometer,c.price,c.change,c.vehicleHistory,c.damageDisclosure,c.damageDisclosureStatus,c.cpoRefurbishmentStatus,c.hasDamagePhotos,c.vehicleSubType,c.acquisitionSubType,c.fleetVehicle,c.titleSubtype,c.factoryGatedDate,c.firstRegistrationDate,c.vin,(c.damageDisclosureGuids||[]).join(\' | \'),c.inspectionDocumentGuid||\'\',(c.workOrderLinks||[]).length,(c.workOrderLinks||[]).join(\' | \'),JSON.stringify(c.rawWorkorderFields||{}),c.url]);\n  const out=\'\\ufeff\'+[head,...rows].map(r=>r.map(v=>`"${String(v??\'\').replace(/"/g,\'""\')}"`).join(\',\')).join(\'\\n\');const b=new Blob([out],{type:\'text/csv;charset=utf-8\'});const u=URL.createObjectURL(b);const a=document.createElement(\'a\');a.href=u;a.download=`Tesla_Model_S_车辆档案_${new Date().toISOString().slice(0,10)}.csv`;a.click();URL.revokeObjectURL(u)\n}\n[\'province\',\'history\',\'sort\'].forEach(id=>$(id).addEventListener(\'change\',apply));[\'city\',\'maxPrice\',\'maxKm\'].forEach(id=>$(id).addEventListener(\'input\',apply));$(\'refresh\').onclick=load;$(\'reset\').onclick=reset;$(\'workorders\').onclick=loadWorkorders;$(\'csv\').onclick=csv;load();\n</script>\n</body>\n</html>'

ENDPOINTS = [
    "https://www.tesla.cn/inventory/api/v4/inventory-results",
    "https://www.tesla.cn/inventory/api/v1/inventory-results",
]
HEADERS = {
    "Accept": "application/json,text/plain,*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.7",
    "Referer": "https://www.tesla.cn/inventory/new/ms?Province=CN&FleetSalesRegions=CN",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
}
UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
RECORD_KEYWORDS = ("damage","disclosure","repair","service","document","file","attachment","inspection","history","condition","refurb")
DETAIL_KEYWORDS = ("工单","damage","disclosure","repair","service","workorder","work order","settlement","inspection")
VIN_SAFE_RE = re.compile(r"^[A-Za-z0-9_-]{6,80}$")

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML

@app.get("/api/inventory")
def inventory():
    last_error = None
    for endpoint in ENDPOINTS:
        try:
            raw = fetch_all_pages(endpoint)
            cars = [normalize(x) for x in raw if is_demo(x)]
            cars = [x for x in cars if x.get("vin")]
            cars.sort(key=lambda x: x.get("price") if isinstance(x.get("price"), (int, float)) else 10**20)
            return {
                "ok": True,
                "source": "Tesla China inventory v4" if "/v4/" in endpoint else "Tesla China inventory v1",
                "fetchedAt": datetime.now(timezone.utc).isoformat(),
                "totalFetched": len(raw),
                "cars": cars,
            }
        except Exception as e:
            last_error = str(e)
    return JSONResponse(status_code=502, content={"ok": False, "error": last_error or "Tesla inventory request failed"})

@app.get("/api/workorders")
def workorders(vin: str = ""):
    vin = (vin or "").strip()
    if not VIN_SAFE_RE.match(vin):
        return JSONResponse(status_code=400, content={"ok": False, "error": "车辆标识格式不正确"})
    url = f"https://www.tesla.cn/ms/order/{urllib.parse.quote(vin)}?titleStatus=new&redirect=no"
    try:
        page = fetch_detail_page(url)
        links = extract_workorder_links_from_detail(page)
        return {"ok": True, "vin": vin, "source": "Tesla 车辆详情页", "detailUrl": url, "links": links, "count": len(links)}
    except Exception as e:
        return JSONResponse(status_code=502, content={"ok": False, "error": str(e), "detailUrl": url})

def fetch_detail_page(url):
    headers = dict(HEADERS)
    headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.tesla.cn/inventory/new/ms?Province=CN&FleetSalesRegions=CN",
        "Cache-Control": "no-cache",
    })
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context()) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        if getattr(resp, "status", 200) >= 400:
            raise RuntimeError(f"Tesla 详情页返回 HTTP {resp.status}")
    return body

def extract_workorder_links_from_detail(page):
    # Tesla 详情页里的公开工单有时直接出现在 HTML，有时存在脚本 JSON 中。
    text = html_lib.unescape(page or "").replace("\\/", "/")
    links, seen = [], set()

    def add_guid(guid):
        guid = str(guid).strip()
        if not UUID_RE.match(guid):
            return
        url = "https://www.tesla.cn/configurator/api/v4/files/" + guid
        if url not in seen:
            seen.add(url)
            links.append(url)

    def add_url(url):
        url = str(url).strip().rstrip('"\'<>),;')
        if not url.startswith("http"):
            return
        try:
            host = urllib.parse.urlparse(url).netloc.lower()
        except Exception:
            return
        if not (host.endswith("tesla.cn") or host.endswith("tesla.com")):
            return
        if "/files/" not in url:
            return
        if url not in seen:
            seen.add(url)
            links.append(url)

    # 直接文件链接。
    url_re = re.compile(r"https?://[^\\s\\\"'<>]+/(?:configurator|inventory)/api/v\\d+/files/[0-9a-fA-F-]{36}", re.I)
    for m in url_re.finditer(text):
        add_url(m.group(0))
    rel_re = re.compile(r"/(?:configurator|inventory)/api/v\\d+/files/([0-9a-fA-F-]{36})", re.I)
    for m in rel_re.finditer(text):
        add_guid(m.group(1))

    # 常见披露字段中的 GUID / GUID 数组。
    field_pat = r"(?:DamageDisclosureGuids?|InspectionDocumentGuid|Repair(?:Order)?Guids?|WorkOrderGuids?)"
    arr_re = re.compile(field_pat + r"[^\\[]*\\[([^\\]]{0,5000})\\]", re.I)
    uuid_re = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
    for m in arr_re.finditer(text):
        for guid in uuid_re.findall(m.group(1)):
            add_guid(guid)
    single_re = re.compile(field_pat + r"[^0-9a-fA-F]{0,100}([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})", re.I)
    for m in single_re.finditer(text):
        add_guid(m.group(1))

    # 字段名变化时，仅从工单/维修/披露关键词附近兜底提取 UUID。
    lower = text.lower()
    for keyword in DETAIL_KEYWORDS:
        start = 0
        key = keyword.lower()
        while True:
            pos = lower.find(key, start)
            if pos < 0:
                break
            chunk = text[max(0, pos-800): min(len(text), pos+4000)]
            for guid in uuid_re.findall(chunk):
                add_guid(guid)
            start = pos + max(1, len(key))
    return links[:30]

def fetch_all_pages(endpoint):
    size = 50
    first = fetch_page(endpoint, 0, size)
    results = extract_results(first)
    total = extract_total(first, len(results))
    out = list(results)
    offset = size
    while offset < min(max(total, len(results)), 300):
        data = fetch_page(endpoint, offset, size)
        rows = extract_results(data)
        if not rows:
            break
        out.extend(rows)
        if len(rows) < size:
            break
        offset += size
    unique = {}
    for item in out:
        key = item.get("VIN") or item.get("vin") or json.dumps(item, ensure_ascii=False)[:160]
        unique.setdefault(key, item)
    return list(unique.values())

def fetch_page(endpoint, offset, count):
    q = {
        "query": {
            "model": "ms",
            "condition": "new",
            "options": {"FleetSalesRegions": ["CN"]},
            "arrangeby": "Price",
            "order": "asc",
            "market": "CN",
            "language": "zh",
            "super_region": "north america",
            "lng": "",
            "lat": "",
            "zip": "",
            "range": 0,
        },
        "offset": offset,
        "count": count,
        "outsideOffset": 0,
        "outsideSearch": False,
        "isFalconDeliverySelectionEnabled": False,
        "version": 0,
    }
    url = endpoint + "?query=" + urllib.parse.quote(json.dumps(q, separators=(",", ":")))
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    with urllib.request.urlopen(req, timeout=15, context=ssl.create_default_context()) as resp:
        text = resp.read().decode("utf-8", errors="replace")
        if getattr(resp, "status", 200) >= 400:
            raise RuntimeError(f"Tesla returned HTTP {resp.status}")
    try:
        return json.loads(text)
    except Exception:
        raise RuntimeError("Tesla returned non-JSON data")

def extract_results(data):
    if isinstance(data, dict):
        if isinstance(data.get("results"), list): return data["results"]
        if isinstance(data.get("data"), dict) and isinstance(data["data"].get("results"), list): return data["data"]["results"]
        if isinstance(data.get("vehicles"), list): return data["vehicles"]
    return []

def extract_total(data, fallback):
    vals = []
    if isinstance(data, dict):
        vals += [data.get("total_matches_found"), data.get("totalMatchesFound"), data.get("total")]
        if isinstance(data.get("data"), dict): vals.append(data["data"].get("total_matches_found"))
    for v in vals:
        try: return int(v)
        except (TypeError, ValueError): pass
    return fallback

def is_demo(car):
    v = car.get("IsDemo")
    subtype = str(car.get("VehicleSubType") or "").lower()
    return v is True or str(v).lower() == "true" or car.get("InventoryType") == "DEMO" or "test" in subtype or "demo" in subtype

def first_number(*vals):
    for v in vals:
        try:
            if v is not None and v != "": return float(v)
        except (TypeError, ValueError): pass
    return None

def option_name(car, group):
    data = car.get("OptionCodeData") if isinstance(car.get("OptionCodeData"), list) else []
    for x in data:
        if isinstance(x, dict) and str(x.get("group","")).upper() == group.upper():
            return x.get("name") or x.get("long_name") or x.get("description") or ""
    v = car.get(group)
    if isinstance(v, list): return " / ".join(str(x) for x in v)
    return v if isinstance(v, str) else ""

def extract_public_docs(car):
    docs, seen = [], set()
    def add(url, label):
        if not isinstance(url, str): return
        if not url.startswith("http"): return
        host = urllib.parse.urlparse(url).netloc.lower()
        if not (host.endswith("tesla.cn") or host.endswith("tesla.com")): return
        if url in seen: return
        seen.add(url); docs.append({"url": url, "label": label[:80]})
    def walk(obj, path=""):
        if isinstance(obj, dict):
            for k,v in obj.items():
                kp = f"{path}.{k}" if path else str(k)
                key_low = str(k).lower()
                relevant = any(w in key_low or w in kp.lower() for w in RECORD_KEYWORDS)
                if isinstance(v, str):
                    if relevant and v.startswith("http"): add(v, str(k))
                    if relevant and UUID_RE.match(v):
                        add("https://www.tesla.cn/configurator/api/v4/files/" + v, str(k))
                walk(v, kp)
        elif isinstance(obj, list):
            for i,v in enumerate(obj): walk(v, f"{path}[{i}]")
    walk(car)
    return docs[:10]

def extract_workorder_links_from_car(car):
    guids, urls, seen_g, seen_u = [], [], set(), set()

    def add_guid(value):
        if isinstance(value, str):
            value = value.strip()
            if UUID_RE.match(value) and value not in seen_g:
                seen_g.add(value)
                guids.append(value)

    def add_url(value):
        if not isinstance(value, str) or not value.startswith("http"):
            return
        try:
            host = urllib.parse.urlparse(value).netloc.lower()
        except Exception:
            return
        if (host.endswith("tesla.cn") or host.endswith("tesla.com")) and "/files/" in value and value not in seen_u:
            seen_u.add(value)
            urls.append(value)

    def walk(obj, keypath=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                path = (keypath + "." + str(key)).lower()
                relevant = any(term in path for term in ("damagedisclosureguid", "inspectiondocumentguid", "repairguid", "workorderguid", "serviceguid"))
                if relevant:
                    if isinstance(value, str):
                        add_guid(value); add_url(value)
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, str):
                                add_guid(item); add_url(item)
                walk(value, path)
        elif isinstance(obj, list):
            for item in obj:
                walk(item, keypath)

    walk(car)
    out = list(urls)
    for guid in guids:
        url = "https://www.tesla.cn/configurator/api/v4/files/" + guid
        if url not in out:
            out.append(url)
    return out[:30]

def extract_relevant_workorder_fields(car):
    """Keep public inventory fields related to disclosure/document GUIDs for diagnosis."""
    out = {}
    def compact(v):
        if isinstance(v, (str, int, float, bool)) or v is None:
            return v
        if isinstance(v, list):
            return v[:30]
        if isinstance(v, dict):
            return {str(k): compact(x) for k, x in list(v.items())[:30]}
        return str(v)
    def walk(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                kp = f"{path}.{k}" if path else str(k)
                low = kp.lower()
                if any(t in low for t in ("damage", "disclosure", "guid", "inspection", "document", "repair", "service", "workorder", "work_order", "file")):
                    out[kp] = compact(v)
                if isinstance(v, (dict, list)):
                    walk(v, kp)
        elif isinstance(obj, list):
            for i, v in enumerate(obj[:50]):
                if isinstance(v, (dict, list)):
                    walk(v, f"{path}[{i}]")
    walk(car)
    return out

def normalize_guid_list(value):
    vals = [value] if isinstance(value, str) else (value if isinstance(value, list) else [])
    out = []
    for x in vals:
        if isinstance(x, str) and UUID_RE.match(x.strip()):
            out.append(x.strip())
    return out

def normalize(car):
    vin = car.get("VIN") or car.get("vin") or ""
    price = first_number(car.get("InventoryPrice"), car.get("TotalPrice"), car.get("Price"), car.get("PurchasePrice"))
    original = first_number(car.get("OriginalPrice"), car.get("MSRP"), car.get("ListPrice"), car.get("PriceBeforeDiscount"))
    listed_reduction = first_number(car.get("PriceAdjustmentUsed"), car.get("Discount")) or 0
    if original is not None and price is not None and original > price:
        listed_reduction = max(listed_reduction, original-price)

    warranty = car.get("WarrantyData") if isinstance(car.get("WarrantyData"), dict) else {}
    province = car.get("StateProvince") or car.get("Province") or car.get("State") or car.get("DeliveryProvince") or ""
    city = car.get("City") or car.get("MetroName") or car.get("DeliveryCity") or car.get("DeliveryLocation") or car.get("VrlName") or ""
    docs = extract_public_docs(car)
    work_orders = extract_workorder_links_from_car(car)
    damage_guids = normalize_guid_list(car.get("DamageDisclosureGuids") or car.get("DamageDisclosureGUIDs") or car.get("DamageDisclosureGuid"))
    inspection_guid = car.get("InspectionDocumentGuid") or car.get("InspectionDocumentGUID") or ""
    raw_workorder_fields = extract_relevant_workorder_fields(car)

    # Search is intentionally restricted to Tesla-owned public file paths; this does not access private account data.
    search_q = f'site:tesla.cn/inventory/api/v4/files "{vin}"'
    return {
        "vin": vin,
        "trim": car.get("TrimName") or car.get("Trim") or car.get("TrimVariant") or "Model S",
        "year": car.get("Year") or "",
        "price": price,
        "listedReduction": listed_reduction,
        "odometer": first_number(car.get("Odometer"), car.get("odometer")),
        "odometerUnit": car.get("OdometerTypeShort") or car.get("OdometerType") or "km",
        "province": province,
        "city": city,
        "paint": option_name(car, "PAINT"),
        "interior": option_name(car, "INTERIOR"),
        "wheels": option_name(car, "WHEELS"),
        "vehicleHistory": car.get("VehicleHistory"),
        "damageDisclosure": car.get("DamageDisclosure"),
        "damageDisclosureStatus": car.get("DamageDisclosureStatus"),
        "cpoRefurbishmentStatus": car.get("CPORefurbishmentStatus"),
        "hasDamagePhotos": car.get("HasDamagePhotos"),
        "vehicleSubType": car.get("VehicleSubType"),
        "acquisitionSubType": car.get("AcquisitionSubType"),
        "fleetVehicle": car.get("FleetVehicle"),
        "titleSubtype": car.get("TitleSubtype"),
        "factoryGatedDate": car.get("FactoryGatedDate") or car.get("ActualGAInDate"),
        "firstRegistrationDate": car.get("FirstRegistrationDate"),
        "actualRange": first_number(car.get("ActualRange")),
        "actualRangeUnit": car.get("ActualRangeUnit") or car.get("OdometerTypeShort") or "",
        "warrantyVehicleYear": warranty.get("WarrantyYear") or car.get("WarrantyYear"),
        "warrantyMile": warranty.get("WarrantyMile") or car.get("WarrantyMile"),
        "warrantyBatteryYear": warranty.get("WarrantyBatteryYear") or car.get("WarrantyBatteryYear"),
        "warrantyBatteryMile": warranty.get("WarrantyBatteryMile") or car.get("WarrantyBatteryMile"),
        "publicDocs": docs,
        "damageDisclosureGuids": damage_guids,
        "inspectionDocumentGuid": inspection_guid,
        "rawWorkorderFields": raw_workorder_fields,
        "workOrderLinks": work_orders,
        "officialSearchUrl": "https://www.google.com/search?q=" + urllib.parse.quote(search_q),
        "url": f"https://www.tesla.cn/ms/order/{urllib.parse.quote(str(vin))}?titleStatus=new&redirect=no#overview" if vin else "https://www.tesla.cn/inventory/new/ms",
    }
