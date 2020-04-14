async function submitForm(form){
  let formData = new FormData(form);
  var csrftoken = Cookies.get('csrftoken');

  fetch(form.action, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      "X-CSRFToken": csrftoken
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'error', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *client
    body: formData // body data type must match "Content-Type" header
  }).then(response => {
    if(response.status == 201){
      document.location = response.headers.get('URL');
    } else if(response.ok) {
      response.text().then(text => {
        form.parentElement.innerHTML = text;
      });
    }
  });


}

window.addEventListener("load", function(event){
  var search = new URLSearchParams(location.search);
  for(let [k, v] of search){
    if(document.getElementById('id_' + k)){
      document.getElementById('id_' + k).setAttribute('value', v);
    }
  }
});
