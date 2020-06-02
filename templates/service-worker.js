
importScripts('/static/workbox/workbox-sw.js');

workbox.setConfig({
  modulePathPrefix: '/static/workbox/',
  debug: false,
});


const {CacheFirst, StaleWhileRevalidate, NetworkFirst, NetworkOnly} = workbox.strategies;
const {registerRoute, setCatchHandler, setDefaultHandler} = workbox.routing;
const {ExpirationPlugin} = workbox.expiration;

const CACHE_NAME = 'offline-html';

const FALLBACK_HTML_URL = '/offline.html';

self.addEventListener('install', async (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
    .then((cache) => cache.add(FALLBACK_HTML_URL))
  );
  event.waitUntil(
    caches.open(CACHE_NAME)
    .then((cache) => cache.add('/static/sanitize.css'))
  );
  event.waitUntil(
    caches.open(CACHE_NAME)
    .then((cache) => cache.add('/static/montserrat.css'))
  );
  event.waitUntil(
    caches.open(CACHE_NAME)
    .then((cache) => cache.add('/static/klima.css'))
  );
});


registerRoute(
  ({request}) => request.destination === 'document',
  new NetworkFirst({
    cacheName: 'documents',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 10 * 24 * 60 * 60,
      }),
    ],
  })
);

registerRoute(
  ({request}) => request.destination === 'font',
  new CacheFirst({
    cacheName: 'fonts',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 Days
      }),
    ],
  })
);

registerRoute(
  ({request}) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 Days
      }),
    ],
  })
);

registerRoute(
  ({request}) => request.destination === 'script' ||
  request.destination === 'style',
  new StaleWhileRevalidate({
    cacheName: 'static-resources',
  })
);

registerRoute(
  ({url}) => url.pathname.startsWith('/admin/'),
  new NetworkOnly()
);

registerRoute(
  ({url}) => url.pathname === 'manifest.webmanifest',
  new NetworkFirst()
);

setCatchHandler(({event}) => {
  switch (event.request.destination) {
    case 'document':
      return caches.match(FALLBACK_HTML_URL);
      break;

    default:
      return Response.error();
  }
});


self.addEventListener('push', function(e) {
  let data = e.data.json();
  var options = {
    body: data.tagline,
    icon: data.icon,
    image: data.image,
    badge: data.badge,
    vibrate: [200, 100, 300],
    data: {
      dateOfArrival: data.publication_date,
      url: data.url,
    }
  };
  e.waitUntil(
    caches.open('documents')
    .then((cache) => cache.add(data.url))
    .then(self.registration.showNotification(data.title, options))
  );
});

self.addEventListener('notificationclick', function(event) {
  const clickedNotification = event.notification;
  const url = event.notification.data.url;
  console.log(url);
  clickedNotification.close();

  const promiseChain = clients.openWindow(url);
  event.waitUntil(promiseChain);
});
