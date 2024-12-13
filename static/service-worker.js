self.addEventListener('install', (event) => {
    event.waitUntil(
      caches.open('app-cache').then((cache) => {
        return cache.addAll([
          '/',
          '/styles.css',
          '/script.js',
          '/icons/logo256.png',
          '/icons/logo128.png',
          '/icons/logo64.png',
          '/icons/logo32.png',        
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', (event) => {
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request);
      })
    );
  });
  