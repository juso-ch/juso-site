function toggleClass(element, cls){
  element.classList.toggle(cls);
  return false;
}

function toggleClassOther(id, cls){
  document.getElementById(id).classList.toggle(cls);
  return false;
}

if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/service-worker.js');
  });
}
