"use strict";

// Первым делом ставим хук на отлавливание всех js ошибок
Modernizr.load({
    test: !window.T.settings.debug,
    yep: '//d3nslu0hdya83q.cloudfront.net/dist/1.0/raven.min.js',
    complete: function() {
        if (typeof(Raven) == 'undefined') return; // shit happens :(
        Raven.config(window.T.settings.raven_uri, {
            whitelistUrls: [/tomat-podarky\.ru/, /www\.tomat-podarky\.ru/]
        }).install();
        if (window.T.user) {
            Raven.setUser({
                id: window.T.user
            });
        }
    }
});

// Google analytics
Modernizr.load({
    test: !window.T.settings.debug,
    yep: 'http://www.google-analytics.com/ga.js',
    complete: function() {
        window._gaq = window._gaq || [];
        window._gaq.push(['_setAccount', window.T.settings.google_analytics_id]);
        window._gaq.push(['_trackPageview']);
    }
});

// Yandex metrika
Modernizr.load({
    test: !window.T.settings.debug,
    yep: 'http://mc.yandex.ru/metrika/watch.js',
    complete: function() {
        try {
            window.yaCounter22301035 = new Ya.Metrika({
                id: window.T.settings.yandex_metrika_id,
                webvisor: true,
                clickmap: true,
                trackLinks: true,
                accurateTrackBounce: true
            });
        } catch(e) {}
    }
});

function googleTranslateElementInit() {
    new google.translate.TranslateElement({pageLanguage: 'ru', includedLanguages: 'be,de,en,es,fr,it,ja,ko,uk,zh-CN,zh-TW,ru', layout: google.translate.TranslateElement.FloatPosition.BOTTOM_RIGHT, gaTrack: true, gaId: window.T.settings.google_analytics_id}, 'google_translate_element');
}
Modernizr.load('//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit');
