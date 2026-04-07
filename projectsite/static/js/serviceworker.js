self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open('hangarin-cache-v1').then(function(cache) {
            return cache.addAll([
                '/',
                '/static/css/sb-admin-2.min.css',
                '/static/js/sb-admin-2.js',
            ]);
        })
    );
});
self.addEventListener('fetch', function(e) {
    // Only intercept GET requests
    if (e.request.method !== 'GET') {
        return; // let non-GET requests go to network
    }

    e.respondWith(
        caches.match(e.request).then(function(response) {
            return response || fetch(e.request);
        })
    );
});