
function setTheme(theme){
  localStorage.setItem('theme', theme);
}

function getTheme(){
  if(localStorage.getItem('theme')){
    return localStorage.getItem('theme');
  }
  if(window.matchMedia('(prefers-color-scheme: dark)').matches){
    return 'dark';
  }
  return 'light';
}

function toggleTheme(transition){
  if(transition)
    document.body.classList.add('theme-change');
  let result = document.body.classList.toggle('dark');

  if(result){
    setTheme('dark');
  } else {
    setTheme('light');
  }
  if(transition){
    window.setTimeout(
      () => document.body.classList.remove('theme-change'),
      500
    );
  }
}

window.onload = (event) => {
  if(getTheme()=='dark'){
    toggleTheme(false);
  }
};
