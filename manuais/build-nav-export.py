#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build-nav-export.py — nav (breadcrumb + indice de paginas), indice de secoes
sticky com scroll suave, export PDF pagina-unica (print nativo), e max-width +25%.

Idempotente: marcadores <!--NAVEXPORT--> (HTML) e /* NAVEXPORT */ (CSS).
Roda in-place nos .html deste diretorio quantas vezes quiser.

Uso:  python3 build-nav-export.py
"""
import os, re, base64

HERE = os.path.dirname(os.path.abspath(__file__))       # .../manuais
ROOT = os.path.dirname(HERE)                            # raiz do repo (nexfar.github.io)
IC_DIR = os.path.join(ROOT, "ic")                       # /ic (manuais IC, slugs limpos)
ASSETS = os.path.join(HERE, "assets")

def nexfar_logo_img():
    with open(os.path.join(ASSETS, "nexfar-logo.svg"), "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return ('<img src="data:image/svg+xml;base64,' + b64 +
            '" alt="Nexfar" style="height:30px;width:auto;display:block;margin-bottom:18px">')

# slug -> (label curto p/ dropdown, old_maxwidth, new_maxwidth, onepage_print_width)
# arquivo = /ic/<slug>.html ; URL de producao = /ic/<slug> (GitHub Pages serve .html)
MANUALS = [
    ("objetivos-e-sugestoes",          "Objetivos · Com meta",  900, 1125, 1157),
    ("objetivos-e-sugestoes-sem-meta",  "Objetivos · Sem meta",  900, 1125, 1157),
    ("cotacao-agil",                    "Cotação Ágil", 1125, 1125, 1157),
    ("catalogo-digital",                "Catálogo · Com preço", 1125, 1125, 1157),
    ("catalogo-digital-sem-preco",      "Catálogo · Sem preço", 1125, 1125, 1157),
]

MARK = "<!--NAVEXPORT-->"
CSS_MARK = "/* NAVEXPORT */"

SVG_BACK   = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></svg>'
SVG_EXPORT = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12m0 0l-4-4m4 4l4-4M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/></svg>'
SVG_CHEVRON = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>'

def manual_css(onepage_w):
    return (CSS_MARK + """
html{scroll-behavior:smooth}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
.header-inner{position:relative}
.header{padding:30px 24px 34px}
.header-inner>img{height:24px}
.header-title{font-size:24px;margin:8px 0 8px}
.header-desc{margin-bottom:0;font-size:13.5px;line-height:1.5;max-width:760px}
footer{margin-top:0}
.hero-top{position:absolute;top:0;right:0;display:flex;align-items:center;gap:10px;z-index:2}
@media(max-width:560px){.hero-top{position:static;margin-top:12px}.header-title{margin-top:14px}}
.to-top{position:fixed;right:22px;bottom:22px;width:46px;height:46px;border-radius:50%;background:#753bbd;color:#fff;border:none;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 8px 24px rgba(76,29,143,.34);opacity:0;visibility:hidden;transform:translateY(10px);transition:opacity .28s cubic-bezier(.16,1,.3,1),transform .28s cubic-bezier(.16,1,.3,1),visibility .28s,background .2s;z-index:70}
.to-top.show{opacity:1;visibility:visible;transform:translateY(0)}
.to-top:hover{background:#5b2da0}
@media(prefers-reduced-motion:reduce){.to-top{transition:opacity .01s,visibility .01s}}
.hero-export{font-family:inherit;font-size:13px;font-weight:600;color:#fff;display:inline-flex;align-items:center;gap:8px;padding:9px 15px;border-radius:9px;border:1px solid rgba(255,255,255,.38);background:rgba(255,255,255,.15);cursor:pointer;transition:background .25s ease,border-color .25s ease}
.hero-export:hover{background:rgba(255,255,255,.26);border-color:rgba(255,255,255,.65)}
.hero-export:active{transform:translateY(1px)}
.flow-bar-inner{display:grid;grid-template-columns:auto 1fr;align-items:center;gap:20px}
.flow-steps{display:flex;align-items:center;justify-content:flex-end;overflow-x:auto;min-width:0}
.crumb{display:flex;align-items:center;gap:9px;flex-shrink:0}
.crumb-home{display:inline-flex;align-items:center;gap:4px;font-size:13px;font-weight:600;color:#6b7280;padding:6px 8px;border-radius:7px}
.crumb-home:hover{background:#f3eefb;color:#753bbd}
.crumb-sep{color:#d1d5db}
.crumb-current{position:relative}
.crumb-btn{font-family:inherit;font-size:14px;font-weight:700;color:#5b2da0;background:#ede9f8;border:1px solid #dcc9f5;border-radius:8px;padding:6px 10px 6px 12px;display:inline-flex;align-items:center;gap:7px;cursor:pointer;white-space:nowrap;transition:background .2s ease}
.crumb-btn:hover{background:#e3d6f7}
.crumb-btn svg{transition:transform .2s ease}
.crumb-current.open .crumb-btn svg{transform:rotate(180deg)}
.crumb-menu{position:absolute;left:0;top:calc(100% + 8px);background:#fff;border:1px solid #e5e7eb;border-radius:10px;box-shadow:0 14px 34px rgba(17,24,39,.16);padding:6px;min-width:250px;display:none;z-index:60}
.crumb-current.open .crumb-menu{display:block}
.crumb-menu a{display:block;padding:9px 12px;border-radius:7px;font-size:13px;font-weight:500;color:#374151}
.crumb-menu a:hover{background:#f3eefb;color:#753bbd}
.crumb-menu a.current{background:#ede9f8;color:#5b2da0;font-weight:700}
@media(max-width:720px){.flow-bar-inner{grid-template-columns:1fr;gap:10px;padding:8px 0}.flow-steps{justify-content:flex-start}.crumb{flex-wrap:wrap}}
@media print{
  .hero-top,.flow-bar,.to-top{display:none!important}
  html{scroll-behavior:auto!important}
  body{background:#fff}
  .container{max-width:none!important}
  .section-card{break-inside:avoid;page-break-inside:avoid;box-shadow:none!important}
  .step,.callout,.faq-item,.shot-item,.phone-frame,.highlight,.case-box,.price-card,.flow-diagram{break-inside:avoid;page-break-inside:avoid}
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
body.printing{width:__OPWpx;margin:0 auto;overflow:visible}
body.printing .hero-top,body.printing .flow-bar{display:none!important}
""".replace("__OPW", str(onepage_w)))

def manual_js(onepage_w):
    return (MARK + """
<button class="to-top" type="button" aria-label="Voltar ao topo" onclick="scrollToTop()"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M6 11l6-6 6 6"/></svg></button>
<script>
(function(){
  var W=__OPW;""".replace("__OPW", str(onepage_w)) + """
  var btn=document.querySelector('.to-top');
  window.scrollToTop=function(){window.scrollTo({top:0,behavior:'smooth'});};
  window.crumbToggle=function(e){e.stopPropagation();var c=document.getElementById('crumbCurrent');if(c)c.classList.toggle('open');};
  document.addEventListener('click',function(){var c=document.getElementById('crumbCurrent');if(c)c.classList.remove('open');});
  window.addEventListener('scroll',function(){
    if(window.scrollY>600) btn.classList.add('show'); else btn.classList.remove('show');
  },{passive:true});
  window.exportPDF=function(){
    document.body.classList.add('printing');
    requestAnimationFrame(function(){requestAnimationFrame(function(){
      var h=Math.ceil(document.body.scrollHeight)+48;
      var st=document.getElementById('onepage-size')||document.createElement('style');
      st.id='onepage-size';
      if(h<=14000){st.textContent='@page{size:'+W+'px '+h+'px;margin:0}';}
      else{st.textContent='@page{size:auto;margin:12mm}';}   /* fallback: pagina normal, sem corte no meio de bloco */
      document.head.appendChild(st);
      window.print();
    });});
  };
  window.addEventListener('afterprint',function(){
    document.body.classList.remove('printing');
    var st=document.getElementById('onepage-size'); if(st) st.remove();
  });
})();
(function(){
  /* indice de secoes: ativa a secao clicada NA HORA e trava o spy durante o scroll
     suave (senao ele passa por todas as secoes intermediarias e causa estranhamento) */
  var steps=[].slice.call(document.querySelectorAll('.flow-step'));
  var map=steps.map(function(s){return{step:s,sec:document.getElementById((s.getAttribute('href')||'').slice(1))};}).filter(function(m){return m.sec;});
  var lock=false, lockT=null;
  function setActive(step){steps.forEach(function(s){s.classList.remove('active');});if(step)step.classList.add('active');}
  function onScroll(){
    if(lock) return;
    var pos=window.scrollY+120,cur=map[0];
    for(var i=0;i<map.length;i++){if(map[i].sec.offsetTop<=pos)cur=map[i];}
    setActive(cur?cur.step:null);
  }
  map.forEach(function(m){m.step.addEventListener('click',function(){
    setActive(m.step);                 // ativa imediatamente
    lock=true; clearTimeout(lockT);
    lockT=setTimeout(function(){lock=false;onScroll();},1400);   // fallback
  });});
  window.addEventListener('scrollend',function(){lock=false;onScroll();});
  window.addEventListener('scroll',onScroll,{passive:true});
  onScroll();
})();
</script>
""")

def hero_top():
    return (MARK + """
    <div class="hero-top">
      <button class="hero-export" type="button" onclick="exportPDF()">""" + SVG_EXPORT + """ Exportar PDF</button>
    </div>
    """)

def breadcrumb(current):
    menu = ""
    cur_label = current
    for slug, label, _o, _n, _w in MANUALS:
        if slug == current:
            cur_label = label
        cls = ' class="current"' if slug == current else ""
        menu += '          <a href="/ic/%s"%s>%s</a>\n' % (slug, cls, label)
    return (MARK + '''    <div class="crumb">
      <a class="crumb-home" href="/manuais/">''' + SVG_BACK + ''' Manuais</a>
      <span class="crumb-sep">/</span>
      <div class="crumb-current" id="crumbCurrent">
        <button class="crumb-btn" type="button" onclick="crumbToggle(event)">''' + cur_label + ' ' + SVG_CHEVRON + '''</button>
        <div class="crumb-menu">
''' + menu + '''        </div>
      </div>
    </div>
''')

def patch_manual(path, fn, label, old_mw, new_mw, onepage_w):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if MARK in html or CSS_MARK in html:
        return "skip (ja injetado)"

    # 1) max-width +25% (header-inner, container, flow-bar-inner)
    html = html.replace("max-width:%dpx" % old_mw, "max-width:%dpx" % new_mw)

    # 1b) barra de versao: tira do topo, joga pro footer (border-bottom -> border-top)
    banner = ('<div style="background:#ede9f8;border-bottom:1px solid #c4aeef;color:#5b2da0;'
              'padding:9px 24px;font-size:13px;text-align:center;font-weight:600">'
              '✓ Este manual está atualizado de acordo com a versão 0.5.2</div>')
    assert banner in html, "banner de versao nao encontrado em " + fn
    html = html.replace(banner, "", 1)
    assert "<footer>" in html
    html = html.replace("<footer>", banner.replace("border-bottom", "border-top") + "\n<footer>", 1)

    # 2) indice de secoes sticky + scroll suave (objetivos nao tinham)
    html = html.replace(
        ".flow-bar{background:#fff;border-bottom:1px solid #e5e7eb;padding:0 24px;overflow-x:auto;white-space:nowrap}",
        ".flow-bar{background:#fff;border-bottom:1px solid #e5e7eb;padding:0 24px;overflow-x:auto;white-space:nowrap;position:sticky;top:0;z-index:50;box-shadow:0 2px 8px rgba(0,0,0,.04)}")
    html = html.replace(
        ".section-card{background:#fff;border:1px solid #e5e7eb;border-radius:16px;margin-bottom:28px;overflow:hidden}",
        ".section-card{background:#fff;border:1px solid #e5e7eb;border-radius:16px;margin-bottom:28px;overflow:hidden;scroll-margin-top:64px}")

    # 3) CSS antes de </style>
    assert html.count("</style>") == 1, "style tags inesperados em " + fn
    css = manual_css(onepage_w).replace("__MW__", str(new_mw))
    html = html.replace("</style>", css + "</style>", 1)

    # 4) hero-top antes do titulo
    assert html.count('<div class="header-title">') == 1
    html = html.replace('<div class="header-title">', hero_top() + '<div class="header-title">', 1)

    # 5) breadcrumb (home + atual-dropdown) na mesma linha das secoes;
    #    tira overflow do flow-bar (senao dropdown corta) e poe num wrapper de steps
    html = html.replace("overflow-x:auto;white-space:nowrap", "white-space:nowrap")
    fbinner = '<div class="flow-bar-inner">\n'
    i = html.find(fbinner)
    assert i != -1, "flow-bar-inner nao encontrado em " + fn
    after = i + len(fbinner)
    close = '\n  </div>\n</div>'
    j = html.find(close, after)
    assert j != -1, "fechamento do flow-bar nao encontrado em " + fn
    steps_html = html[after:j]
    html = (html[:after] + breadcrumb(fn) + '    <div class="flow-steps">\n'
            + steps_html + '\n    </div>' + html[j:])

    # 6) remove o scrollspy original (so existe em cotacao/catalogo) p/ nao brigar
    #    com o unificado; injeta o JS (com scrollspy melhorado) antes de </body>
    html = re.sub(r"<script>\s*\(function\(\)\{.*?window\.scrollY\+120.*?\}\)\(\);\s*</script>",
                  "", html, count=1, flags=re.S)
    assert html.count("</body>") == 1
    html = html.replace("</body>", manual_js(onepage_w) + "</body>", 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return "ok"

# ---------------------------------------------------------------- pagina pai
INDEX_CSS = CSS_MARK + """
.var-grid.single{grid-template-columns:1fr}
.vbanner{border-top:1px solid #c4aeef}
.product-block{margin-bottom:40px}
.product-head{padding-bottom:14px;margin-bottom:22px;border-bottom:2px solid #ede9f8}
.product-name{font-size:20px;font-weight:800;color:#111827}
.product-badge{display:inline-block;font-size:12px;font-weight:700;color:#5b2da0;background:#ede9f8;border:1px solid #dcc9f5;border-radius:999px;padding:2px 9px;vertical-align:middle;margin-left:8px}
.product-desc{font-size:13px;color:#6b7280;margin-top:3px}
.header-inner{position:relative}
.hbtn{position:absolute;top:0;right:0;display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.38);color:#fff;font-family:inherit;font-size:13px;font-weight:600;padding:9px 15px;border-radius:9px;cursor:pointer;transition:background .25s ease,border-color .25s ease}
.hbtn:hover{background:rgba(255,255,255,.26);border-color:rgba(255,255,255,.65)}
@media(max-width:560px){.hbtn{position:static;margin-top:18px}}
.modal-ov{position:fixed;inset:0;background:rgba(17,24,39,.55);display:none;align-items:center;justify-content:center;z-index:100;padding:20px}
.modal-ov.open{display:flex}
.modal{background:#fff;border-radius:16px;max-width:470px;width:100%;padding:24px;box-shadow:0 24px 60px rgba(0,0,0,.3);max-height:85vh;overflow:auto}
.modal h3{font-size:18px;font-weight:800;color:#111827;margin-bottom:4px}
.modal-sub{font-size:13px;color:#6b7280;margin-bottom:16px;line-height:1.5}
.modal-list label{display:flex;gap:10px;align-items:flex-start;padding:11px 12px;border:1px solid #e5e7eb;border-radius:10px;margin-bottom:8px;cursor:pointer;font-size:14px;color:#1f2937}
.modal-list label:hover{border-color:#c4aeef;background:#faf7ff}
.modal-list input{margin-top:2px;accent-color:#753bbd;width:16px;height:16px;flex-shrink:0}
.modal-actions{display:flex;gap:10px;justify-content:flex-end;margin-top:18px}
.mbtn{font-family:inherit;font-size:14px;font-weight:600;border-radius:9px;padding:10px 16px;cursor:pointer;border:1px solid transparent}
.mbtn.ghost{background:#fff;border-color:#e5e7eb;color:#374151}
.mbtn.ghost:hover{border-color:#c4aeef;color:#753bbd}
.mbtn.primary{background:#753bbd;color:#fff}
.mbtn.primary:hover{background:#5b2da0}
"""

def index_modal_html():
    items = ""
    for slug, label, _o, _n, _w in MANUALS:
        items += '      <label><input type="checkbox" value="/ic/%s.html" checked> %s</label>\n' % (slug, label)
    return (MARK + """
<div class="modal-ov" id="pdfModal">
  <div class="modal">
    <h3>Exportar manuais em PDF</h3>
    <p class="modal-sub">Selecione os manuais. Saem em um &uacute;nico PDF, cada manual come&ccedil;ando em nova p&aacute;gina e sem cortes no meio do conte&uacute;do.</p>
    <div class="modal-list">
""" + items + """    </div>
    <div class="modal-actions">
      <button class="mbtn ghost" type="button" onclick="pdfClose()">Cancelar</button>
      <button class="mbtn primary" type="button" onclick="pdfExport()">Exportar selecionados</button>
    </div>
  </div>
</div>
<script>
function pdfOpen(){document.getElementById('pdfModal').classList.add('open');}
function pdfClose(){document.getElementById('pdfModal').classList.remove('open');}
document.getElementById('pdfModal').addEventListener('click',function(e){if(e.target===this)pdfClose();});
async function pdfExport(){
  var checks=[].slice.call(document.querySelectorAll('#pdfModal input:checked'));
  if(!checks.length){alert('Selecione ao menos um manual.');return;}
  var win=window.open('','_blank');
  if(!win){alert('Permita pop-ups para exportar o PDF.');return;}
  win.document.write('<!DOCTYPE html><meta charset="UTF-8"><title>Gerando PDF...</title><body style="font-family:sans-serif;padding:40px;color:#374151">Gerando PDF, aguarde...</body>');
  win.document.close();
  var styles='',bodies='';
  for(var i=0;i<checks.length;i++){
    try{
      var r=await fetch(checks[i].value,{cache:'no-store'});
      var doc=new DOMParser().parseFromString(await r.text(),'text/html');
      var st=doc.querySelector('style'); if(st) styles+=st.textContent+'\\n';
      ['.hero-top','.page-index','.flow-bar'].forEach(function(s){var el=doc.querySelector(s);if(el)el.remove();});
      doc.querySelectorAll('script').forEach(function(s){s.remove();});
      bodies+='<section class="manual-doc"'+(i>0?' style="break-before:page;page-break-before:always"':'')+'>'+doc.body.innerHTML+'</section>';
    }catch(e){}
  }
  var out='<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
    +'<title>Manuais IC &mdash; Nexfar</title><style>'+styles
    +' @page{size:auto;margin:14mm} html{scroll-behavior:auto} body{background:#fff}'
    +' .hero-top,.page-index,.flow-bar{display:none!important}'
    +' .section-card{break-inside:avoid;page-break-inside:avoid;box-shadow:none}'
    +' .step,.callout,.faq-item,.shot-item,.phone-frame,.highlight,.case-box,.price-card,.flow-diagram{break-inside:avoid;page-break-inside:avoid}'
    +' *{-webkit-print-color-adjust:exact;print-color-adjust:exact}</style></head><body>'
    +bodies
    +'<scr'+'ipt>window.onload=function(){setTimeout(function(){window.focus();window.print();},500);};</scr'+'ipt>'
    +'</body></html>';
  win.document.open();win.document.write(out);win.document.close();
  pdfClose();
}
</script>
""")

def patch_index(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if MARK in html or CSS_MARK in html:
        return "skip (ja injetado)"
    # largura padronizada (1000 -> 1125, mesmo padrao dos manuais)
    html = html.replace("max-width:1000px", "max-width:1125px")

    # logo da home = Nexfar (multi-produto), no lugar do logo IC
    html = re.sub(r'<img src="data:image/svg\+xml;base64,[^>]*>', nexfar_logo_img(), html, count=1)

    # copy generica (nao mais IC-especifica)
    html = html.replace(
        'Guias passo a passo das ferramentas da Inteligência Comercial. Escolha o manual pela ferramenta que você quer usar.',
        'Guias de uso dos produtos Nexfar. Escolha o produto e abra o manual da ferramenta.')

    # Cotacao: bloco solo -> mesmo padrao das demais categorias (cat-head + var-grid)
    solo_block = (
        '  <div class="cat-block">\n'
        '    <a class="card solo" target="_top" href="manual-cotacao-agil.html">\n'
        '      <div class="solo-top"><div class="solo-ic"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"/></svg></div><div class="solo-title">Cotação Ágil</div></div>\n'
        '      <div class="card-desc">Monte pedidos em segundos. A Inteligência Comercial identifica os itens, escolhe o equivalente mais barato disponível em estoque e adapta o resultado à regional do distribuidor, com ou sem ST.</div>\n'
        '      <div class="solo-cta">Abrir manual <svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>\n'
        '    </a>\n'
        '  </div>'
    )
    new_block = (
        '  <div class="cat-block">\n'
        '    <div class="cat-head"><div class="cat-icon"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"/></svg></div><div>\n'
        '      <div class="cat-title">Cotação Ágil</div>\n'
        '      <div class="cat-sub">Monte pedidos em segundos com a Inteligência Comercial.</div></div></div>\n'
        '    <div class="var-grid single">\n'
        '      <a class="card" target="_top" href="manual-cotacao-agil.html"><div class="card-label">Abrir manual <svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div><div class="card-desc">A IC identifica os itens, escolhe o equivalente mais barato em estoque e adapta à regional do distribuidor, com ou sem ST.</div></a>\n'
        '    </div>\n'
        '  </div>'
    )
    assert solo_block in html, "bloco solo da Cotacao nao encontrado (markup mudou?)"
    html = html.replace(solo_block, new_block, 1)

    # IC vira uma SECAO de produto (pronto p/ outros produtos como secoes irmas)
    product_open = ('  <div class="product-block">\n'
        '    <div class="product-head">\n'
        '      <div class="product-name">Inteligência Comercial <span class="product-badge">v0.5.2</span></div>\n'
        '      <div class="product-desc">Ferramentas de apoio à venda no PDV — objetivos, cotação e catálogo.</div>\n'
        '    </div>\n')
    assert '  <div class="cat-block">' in html
    html = html.replace('  <div class="cat-block">', product_open + '  <div class="cat-block">', 1)
    assert '</div>\n<div class="foot"' in html, "fechamento do container nao encontrado"
    html = html.replace('</div>\n<div class="foot"', '  </div>\n</div>\n<div class="foot"', 1)

    assert html.count("</style>") == 1
    html = html.replace("</style>", INDEX_CSS + "</style>", 1)
    btn = '<button class="hbtn" type="button" onclick="pdfOpen()">' + SVG_EXPORT + ' Exportar PDF</button>\n'
    anchor = '</div></div>\n<div class="vbanner"'
    assert anchor in html, "anchor do header nao encontrado"
    html = html.replace(anchor, btn + anchor, 1)
    # home nao tem indicador de versao (a versao vira badge ao lado do titulo do produto)
    vbanner = '<div class="vbanner">✓ Documentação atualizada de acordo com a versão 0.5.2</div>'
    html = html.replace(vbanner + "\n", "", 1)
    html = html.replace(vbanner, "", 1)
    # footer generico (multi-produto, sem versao IC-especifica)
    html = html.replace(
        '<div class="foot">Nexfar Inteligência Comercial · versão 0.5.2</div>',
        '<div class="foot">Nexfar · Central de Manuais</div>')
    assert html.count("</body>") == 1
    html = html.replace("</body>", index_modal_html() + "</body>", 1)

    # links da home -> URLs de producao /ic/<slug> (nav) ; fetch do export usa .html
    slugmap = {
        'manual-objetivos-sugestoes.html':          'objetivos-e-sugestoes',
        'manual-objetivos-sugestoes-sem-meta.html':  'objetivos-e-sugestoes-sem-meta',
        'manual-cotacao-agil.html':                  'cotacao-agil',
        'manual-catalogo-digital.html':              'catalogo-digital',
        'manual-catalogo-digital-sem-preco.html':    'catalogo-digital-sem-preco',
    }
    for old, slug in slugmap.items():
        html = html.replace('href="' + old + '"',  'href="/ic/' + slug + '"')
        html = html.replace('value="' + old + '"', 'value="/ic/' + slug + '.html"')

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return "ok"

def main():
    print("== manuais ==")
    for slug, label, old_mw, new_mw, w in MANUALS:
        p = os.path.join(IC_DIR, slug + ".html")
        if not os.path.exists(p):
            print("  MISSING", slug); continue
        print("  %-34s %s" % (slug, patch_manual(p, slug, label, old_mw, new_mw, w)))
    print("== pagina pai ==")
    print("  %-42s %s" % ("index.html", patch_index(os.path.join(HERE, "index.html"))))

if __name__ == "__main__":
    main()
