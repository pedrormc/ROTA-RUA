/* =========================================================================
   AÇOUGUE T-BONE — comportamento
   Sem dependências, sem build. Tudo degrada: se este arquivo não carregar,
   o site continua sendo um catálogo legível com botões de WhatsApp.
   ========================================================================= */
(function () {
  'use strict';

  var FONE = '5561983703338';
  var KEY = 'tbone.comanda.v1';

  var $  = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // A comanda vive no localStorage, que qualquer um pode editar no navegador.
  // Tudo que volta de lá passa por aqui antes de virar HTML.
  function esc(v) {
    return String(v == null ? '' : v)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  /* ---------------------------------------------------------------------
     Horário de funcionamento — fonte única
     --------------------------------------------------------------------- */
  // domingo = 0
  var HORAS = [
    { abre: 510, fecha: 780 },  // dom  08:30–13:00
    { abre: 510, fecha: 1140 }, // seg  08:30–19:00
    { abre: 510, fecha: 1140 },
    { abre: 510, fecha: 1140 },
    { abre: 510, fecha: 1140 },
    { abre: 510, fecha: 1140 }, // sex
    { abre: 510, fecha: 780 }   // sáb  08:30–13:00
  ];

  function hhmm(min) {
    var h = Math.floor(min / 60), m = min % 60;
    return m === 0 ? h + 'h' : h + 'h' + (m < 10 ? '0' + m : m);
  }

  function pintaStatus() {
    var el = $('#status'), txt = $('#status-txt');
    if (!el || !txt) return;
    var agora = new Date();
    var d = agora.getDay();
    var min = agora.getHours() * 60 + agora.getMinutes();
    var hoje = HORAS[d];
    el.hidden = false;

    if (min >= hoje.abre && min < hoje.fecha) {
      el.classList.add('is-open');
      el.classList.remove('is-closed');
      txt.textContent = 'Aberto agora · fecha às ' + hhmm(hoje.fecha);
    } else {
      el.classList.add('is-closed');
      el.classList.remove('is-open');
      if (min < hoje.abre) {
        txt.textContent = 'Fechado · abre às ' + hhmm(hoje.abre);
      } else {
        var amanha = HORAS[(d + 1) % 7];
        txt.textContent = 'Fechado · abre amanhã às ' + hhmm(amanha.abre);
      }
    }

    // marca a linha de hoje na tabela de horários
    var alvo = d === 0 ? '0' : (d === 6 ? '6' : '1');
    $$('#hours li').forEach(function (li) {
      li.classList.toggle('is-today', li.getAttribute('data-d') === alvo);
    });
  }

  /* ---------------------------------------------------------------------
     Menu no celular
     --------------------------------------------------------------------- */
  var burger = $('#burger'), mnav = $('#mnav');
  if (burger && mnav) {
    burger.addEventListener('click', function () {
      var aberto = mnav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', String(aberto));
      burger.setAttribute('aria-label', aberto ? 'Fechar menu' : 'Abrir menu');
    });
    mnav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        mnav.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---------------------------------------------------------------------
     Comanda — estado
     --------------------------------------------------------------------- */
  var comanda = [];
  var entrega = 'Retirar na loja';
  var obs = '';

  try {
    var salvo = JSON.parse(localStorage.getItem(KEY) || '{}');
    if (Array.isArray(salvo.itens)) comanda = salvo.itens;
    if (salvo.entrega) entrega = salvo.entrega;
    if (salvo.obs) obs = salvo.obs;
  } catch (e) { /* armazenamento indisponível: segue sem persistir */ }

  function salva() {
    try {
      localStorage.setItem(KEY, JSON.stringify({ itens: comanda, entrega: entrega, obs: obs }));
    } catch (e) { /* modo privativo: o pedido ainda funciona nesta visita */ }
  }

  function fmt(unidade, v) {
    if (unidade === 'un') return v + (v === 1 ? ' un' : ' un');
    if (v < 1000) return v + ' g';
    var kg = v / 1000;
    return (kg % 1 === 0 ? String(kg) : kg.toFixed(1).replace('.', ',')) + ' kg';
  }

  function passo(unidade) { return unidade === 'un' ? 1 : 500; }

  function chave(item) { return item.nome + '|' + item.prep; }

  function adiciona(item) {
    var achou = null;
    for (var i = 0; i < comanda.length; i++) {
      if (chave(comanda[i]) === chave(item)) { achou = comanda[i]; break; }
    }
    if (achou) achou.qtd += item.qtd;
    else comanda.push(item);
    salva();
    pinta();
    aviso(item.nome + ' entrou na comanda');
  }

  function aviso(msg) {
    var t = $('#toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('is-on');
    clearTimeout(aviso._t);
    aviso._t = setTimeout(function () { t.classList.remove('is-on'); }, 2200);
  }

  /* ---------------------------------------------------------------------
     Comanda — painel dentro do card
     --------------------------------------------------------------------- */
  var QTD_KG = [500, 1000, 1500, 2000, 3000];
  var QTD_UN = [1, 2, 3, 4, 6, 10];

  function montaPainel(cut) {
    var unidade = cut.getAttribute('data-unit') || 'kg';
    var preps = (cut.getAttribute('data-prep') || (cut.closest('.cat') && cut.closest('.cat').getAttribute('data-prep')) || 'Como está').split('|');
    var qtds = unidade === 'un' ? QTD_UN : QTD_KG;

    var painel = document.createElement('div');
    painel.className = 'cut__panel';

    var htmlQtd = qtds.map(function (v, i) {
      return '<button class="chip" type="button" data-qtd="' + v + '" aria-pressed="' + (i === (unidade === 'un' ? 0 : 1)) + '">' + fmt(unidade, v) + '</button>';
    }).join('');

    var htmlPrep = preps.map(function (p, i) {
      return '<button class="chip" type="button" data-prep="' + p + '" aria-pressed="' + (i === 0) + '">' + p + '</button>';
    }).join('');

    painel.innerHTML =
      '<div class="field"><span>Quanto</span><div class="chips" role="group" aria-label="Quantidade">' + htmlQtd + '</div></div>' +
      (preps.length > 1 ? '<div class="field"><span>Como cortar</span><div class="chips" role="group" aria-label="Preparo">' + htmlPrep + '</div></div>' : '') +
      '<div class="cut__confirm">' +
        '<button class="btn btn--ghost btn--sm" type="button" data-act="cancelar">Cancelar</button>' +
        '<button class="btn btn--sm" type="button" data-act="ok">Adicionar</button>' +
      '</div>';

    // seleção exclusiva dentro de cada grupo
    painel.addEventListener('click', function (e) {
      var chip = e.target.closest('.chip');
      if (chip) {
        $$('.chip', chip.parentNode).forEach(function (c) { c.setAttribute('aria-pressed', 'false'); });
        chip.setAttribute('aria-pressed', 'true');
        return;
      }
      var btn = e.target.closest('[data-act]');
      if (!btn) return;
      if (btn.getAttribute('data-act') === 'cancelar') { fecha(cut); return; }

      var qtdSel = $('.chip[data-qtd][aria-pressed="true"]', painel);
      var prepSel = $('.chip[data-prep][aria-pressed="true"]', painel);
      adiciona({
        nome: cut.getAttribute('data-name'),
        prep: prepSel ? prepSel.getAttribute('data-prep') : (preps[0] || ''),
        qtd: qtdSel ? parseInt(qtdSel.getAttribute('data-qtd'), 10) : qtds[0],
        un: unidade
      });
      fecha(cut);
    });

    return painel;
  }

  function fecha(cut) {
    cut.classList.remove('is-open');
    var p = $('.cut__panel', cut);
    if (p) p.remove();
    var b = $('.cut__add', cut);
    if (b) b.focus();
  }

  $$('.cut').forEach(function (cut) {
    var btn = $('.cut__add', cut);
    if (!btn) return;
    btn.addEventListener('click', function () {
      // fecha qualquer outro painel aberto
      $$('.cut.is-open').forEach(function (o) { if (o !== cut) fecha(o); });
      cut.classList.add('is-open');
      var painel = montaPainel(cut);
      $('.cut__body', cut).appendChild(painel);
      var primeiro = $('.chip', painel);
      if (primeiro) primeiro.focus();
    });
  });

  /* ---------------------------------------------------------------------
     Comanda — barra e gaveta
     --------------------------------------------------------------------- */
  var bar = $('#bar'), sheet = $('#sheet'), corpo = $('#sheet-body');

  function total() {
    return comanda.reduce(function (s, i) { return s + 1; }, 0);
  }

  function pinta() {
    if (!bar) return;
    var n = total();
    bar.hidden = n === 0;
    requestAnimationFrame(function () { bar.classList.toggle('is-up', n > 0); });

    $('#bar-count').textContent = n === 1 ? '1 item na comanda' : n + ' itens na comanda';
    $('#bar-items').textContent = comanda.map(function (i) { return i.nome; }).join(', ');

    if (!corpo) return;
    if (n === 0) {
      corpo.innerHTML =
        '<div class="sheet__empty">' +
        '<svg width="40" height="40" aria-hidden="true"><use href="#i-basket"/></svg>' +
        '<p>Sua comanda está vazia.<br>Escolha os cortes e eles aparecem aqui.</p></div>';
      return;
    }

    var linhas = comanda.map(function (item, idx) {
      var nome = esc(item.nome), prep = esc(item.prep);
      return '<div class="line">' +
        '<div><b>' + nome + '</b>' + (item.prep && item.prep !== 'Como está' ? '<span>' + prep + '</span>' : '') + '</div>' +
        '<div class="line__ctrl">' +
          '<button type="button" data-menos="' + idx + '" aria-label="Diminuir ' + nome + '">−</button>' +
          '<span class="line__qt">' + esc(fmt(item.un, item.qtd)) + '</span>' +
          '<button type="button" data-mais="' + idx + '" aria-label="Aumentar ' + nome + '">+</button>' +
        '</div>' +
        '<button class="line__rm" type="button" data-rm="' + idx + '">remover</button>' +
      '</div>';
    }).join('');

    corpo.innerHTML =
      linhas +
      '<div class="field" style="margin-top:1.3rem"><span>Como você prefere receber</span>' +
        '<div class="chips" role="group" aria-label="Forma de entrega">' +
          ['Retirar na loja', 'Entrega na Asa Norte'].map(function (o) {
            return '<button class="chip" type="button" data-ent="' + o + '" aria-pressed="' + (o === entrega) + '">' + o + '</button>';
          }).join('') +
        '</div>' +
      '</div>' +
      '<div class="obs"><label for="obs">Alguma observação?</label>' +
      '<textarea id="obs" placeholder="Ex.: bife fininho, sem gordura, entregar depois das 18h">' + esc(obs) + '</textarea></div>';
  }

  if (corpo) {
    corpo.addEventListener('click', function (e) {
      var el = e.target.closest('[data-mais],[data-menos],[data-rm],[data-ent]');
      if (!el) return;
      if (el.hasAttribute('data-ent')) {
        entrega = el.getAttribute('data-ent');
        salva(); pinta(); return;
      }
      var i;
      if (el.hasAttribute('data-mais')) {
        i = +el.getAttribute('data-mais');
        comanda[i].qtd += passo(comanda[i].un);
      } else if (el.hasAttribute('data-menos')) {
        i = +el.getAttribute('data-menos');
        var p = passo(comanda[i].un);
        comanda[i].qtd = Math.max(p, comanda[i].qtd - p);
      } else {
        i = +el.getAttribute('data-rm');
        comanda.splice(i, 1);
      }
      salva();
      pinta();
      if (comanda.length === 0 && sheet && sheet.open) sheet.close();
    });

    corpo.addEventListener('input', function (e) {
      if (e.target.id === 'obs') { obs = e.target.value; salva(); }
    });
  }

  function abreGaveta() {
    if (!sheet) return;
    if (typeof sheet.showModal === 'function') sheet.showModal();
    else sheet.setAttribute('open', '');
  }

  var abrir = $('#bar-open'), fecharSheet = $('#sheet-close'), limpar = $('#sheet-clear');
  if (abrir) abrir.addEventListener('click', abreGaveta);
  if (fecharSheet) fecharSheet.addEventListener('click', function () { sheet.close(); });
  if (sheet) {
    sheet.addEventListener('click', function (e) {
      if (e.target === sheet) sheet.close(); // clique no fundo
    });
  }
  if (limpar) limpar.addEventListener('click', function () {
    comanda = []; obs = ''; salva(); pinta(); sheet.close();
    aviso('Comanda limpa');
  });

  /* ---------------------------------------------------------------------
     Monta a mensagem e abre o WhatsApp
     --------------------------------------------------------------------- */
  function mensagem() {
    var linhas = comanda.map(function (i) {
      return '• ' + fmt(i.un, i.qtd) + ' — ' + i.nome + (i.prep && i.prep !== 'Como está' ? ' (' + i.prep.toLowerCase() + ')' : '');
    }).join('\n');

    var txt = 'Olá! Vim pelo site e queria fazer este pedido:\n\n' + linhas + '\n\n' + entrega + '.';
    if (obs.trim()) txt += '\n\nObservação: ' + obs.trim();
    txt += '\n\nPode confirmar o que tem e o valor?';
    return txt;
  }

  function envia() {
    if (comanda.length === 0) { aviso('Adicione algum corte primeiro'); return; }
    window.open('https://wa.me/' + FONE + '?text=' + encodeURIComponent(mensagem()), '_blank', 'noopener');
  }

  var envBar = $('#bar-send'), envSheet = $('#sheet-send');
  if (envBar) envBar.addEventListener('click', envia);
  if (envSheet) envSheet.addEventListener('click', envia);

  /* ---------------------------------------------------------------------
     Clube do balcão → WhatsApp
     PONTO DE TROCA: para gravar em CRM/planilha, envie também um fetch()
     para o endpoint do formulário aqui antes do window.open.
     --------------------------------------------------------------------- */
  var form = $('#form-base');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var d = new FormData(form);
      var txt = 'Olá! Quero entrar no clube do balcão do T-Bone.\n\n' +
        'Nome: ' + (d.get('nome') || '') + '\n' +
        'WhatsApp: ' + (d.get('fone') || '') + '\n' +
        'Mês do aniversário: ' + (d.get('mes') || '');
      window.open('https://wa.me/' + FONE + '?text=' + encodeURIComponent(txt), '_blank', 'noopener');
      form.reset();
      aviso('Abrindo o WhatsApp com seus dados');
    });
  }

  /* ---------------------------------------------------------------------
     Trilho de categorias — marca onde você está
     --------------------------------------------------------------------- */
  var cats = $$('.cat');
  var links = $$('.catrail a');
  if (cats.length && links.length && 'IntersectionObserver' in window) {
    var obs2 = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (!en.isIntersecting) return;
        var id = '#' + en.target.id;
        links.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('href') === id); });
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    cats.forEach(function (c) { obs2.observe(c); });
  }

  /* ---------------------------------------------------------------------
     Revelação discreta
     --------------------------------------------------------------------- */
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var alvos = $$('.sec-head, .steps, .kits, .split, .figs, .tl, .revs, .birth, .visit__grid, .pets__grid, .cult__top');
    alvos.forEach(function (el) { el.classList.add('rise'); });
    var obs3 = new IntersectionObserver(function (ens) {
      ens.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); obs3.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    alvos.forEach(function (el) { obs3.observe(el); });
  }

  /* --------------------------------------------------------------------- */
  var ano = $('#ano');
  if (ano) ano.textContent = String(new Date().getFullYear());

  pintaStatus();
  setInterval(pintaStatus, 60000);
  pinta();
})();
