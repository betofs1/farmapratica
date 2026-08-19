/*
 * FarmaPrática — rastreador leve de tempo de uso por ferramenta.
 * Inclua no final do <body> de cada ferramenta:
 *   <script src="../assets/tempo-uso.js" data-tool="guia"></script>
 * Contabiliza apenas o tempo em que a aba está visível E com foco
 * (Page Visibility API), evitando contar abas em segundo plano.
 * Os dados ficam em localStorage (mesma origem do hub), agrupados por dia:
 *   fp_tempo_uso_v1 = { "2026-08-19": { guia: 812, medinter: 340, ... }, ... }
 * O hub lê essa chave para somar o dia atual ou a semana atual (seg–dom).
 */
(function(){
  var scriptEl = document.currentScript;
  var TOOL_KEY = (scriptEl && scriptEl.getAttribute('data-tool')) || 'outro';
  var STORAGE_KEY = 'fp_tempo_uso_v1';
  var FLUSH_MS = 5000;

  var accumulated = 0;   // segundos acumulados desde o último flush
  var lastTick = null;
  var isActive = (document.visibilityState === 'visible') && document.hasFocus();

  function todayKey(d){
    d = d || new Date();
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  }
  function loadData(){
    try{ return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; }catch(e){ return {}; }
  }
  function saveData(data){
    try{ localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); }catch(e){}
  }
  function flush(){
    if(accumulated < 1) return;
    var data = loadData();
    var day = todayKey();
    data[day] = data[day] || {};
    data[day][TOOL_KEY] = Math.round((data[day][TOOL_KEY] || 0) + accumulated);
    saveData(data);
    accumulated = 0;
  }
  function tick(){
    if(isActive){
      var now = Date.now();
      if(lastTick) accumulated += (now - lastTick) / 1000;
      lastTick = now;
    }else{
      lastTick = null;
    }
  }
  function setActive(active){
    if(active && !isActive){ lastTick = Date.now(); }
    if(!active && isActive){ tick(); flush(); }
    isActive = active;
  }

  setInterval(tick, 1000);
  setInterval(flush, FLUSH_MS);
  document.addEventListener('visibilitychange', function(){
    setActive(document.visibilityState === 'visible' && document.hasFocus());
  });
  window.addEventListener('focus', function(){ setActive(document.visibilityState === 'visible'); });
  window.addEventListener('blur', function(){ setActive(false); });
  window.addEventListener('pagehide', flush);
  window.addEventListener('beforeunload', flush);
})();
