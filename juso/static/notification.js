document.getElementById('subscribe-button').addEventListener('click', enableNotifications);
document.getElementById('unsubscribe-button').addEventListener('click', disableNotifications);

if ('Notification' in window && navigator.serviceWorker) {
  if (Notification.permission === "blocked") {
    document.getElementById('notification-area').remove();
  } else if (Notification.permission === 'granted') {
    navigator.serviceWorker.ready.then(reg => {
      reg.pushManager.getSubscription().then(sub => {
        if(sub){
          toggleButtons(true);
          var csrftoken = Cookies.get('csrftoken');
          console.log(sub);
          fetch('is-subscribed/', {
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, *cors, same-origin
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, *same-origin, omit
            headers: {
              "X-CSRFToken": csrftoken,
              "Content-Type": 'application/json',
            },
            redirect: 'error', // manual, *follow, error
            referrerPolicy: 'no-referrer', // no-referrer, *client
            body: JSON.stringify(sub) // body data type must match "Content-Type" header
          }).then(response => response.json())
            .then(json => {
              toggleButtons(json.subscribed);
            });
        } else {
          toggleButtons(false);
        }
      });
    });
  } else {
    toggleButtons(false);
  }
} else {
  document.getElementById('notification-area').remove();
}

function toggleButtons(subscribed){
  if (subscribed) {
    document.getElementById('subscribe-button').style.display = 'none';
    document.getElementById('unsubscribe-button').style.display = '';
  } else {
    document.getElementById('subscribe-button').style.display = '';
    document.getElementById('unsubscribe-button').style.display = 'none';
  }
}

function disableNotifications() {
  navigator.serviceWorker.ready.then(function(reg) {
    reg.pushManager.getSubscription().then(function(subscription) {
      subscription.unsubscribe().then(function(successful) {
        var csrftoken = Cookies.get('csrftoken');
        console.log(subscription);
        fetch('unsubscribe/', {
          method: 'POST', // *GET, POST, PUT, DELETE, etc.
          mode: 'cors', // no-cors, *cors, same-origin
          cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
          credentials: 'same-origin', // include, *same-origin, omit
          headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": 'application/json',
          },
          redirect: 'error', // manual, *follow, error
          referrerPolicy: 'no-referrer', // no-referrer, *client
          body: JSON.stringify(subscription) // body data type must match "Content-Type" header
        }).then(response => response.json())
          .then(json => {
            toggleButtons(false);
          });
      }).catch(function(e) {
        console.log(e);
      })
    })        
  });
}

function enableNotifications() {
  Notification.requestPermission(function(status) {
    console.log('Notification permission status:', status);
    navigator.serviceWorker.ready.then(function(reg) {
      reg.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: document.getElementById('vapid_public_key').value
      }).then(function(sub) {
        var csrftoken = Cookies.get('csrftoken');
        fetch('subscribe/', {
          method: 'POST', // *GET, POST, PUT, DELETE, etc.
          mode: 'cors', // no-cors, *cors, same-origin
          cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
          credentials: 'same-origin', // include, *same-origin, omit
          headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": 'application/json',
          },
          redirect: 'error', // manual, *follow, error
          referrerPolicy: 'no-referrer', // no-referrer, *client
          body: JSON.stringify(sub) // body data type must match "Content-Type" header
        }).then(response => response.json()).then( json => {
          toggleButtons(true);
        });
      }).catch(function(e) {
        if (Notification.permission === 'denied') {
          console.warn('Permission for notifications was denied');
        } else {
          console.error('Unable to subscribe to push', e);
        }
      });
    })
  });
}

