"use strict";

/*! matchMedia() polyfill - Test a CSS media type/query in JS. Authors & copyright (c) 2012: Scott Jehl, Paul Irish, Nicholas Zakas, David Knight. Dual MIT/BSD license */
window.matchMedia||(window.matchMedia=function(){"use strict";var e=window.styleMedia||window.media;if(!e){var t=document.createElement("style"),n=document.getElementsByTagName("script")[0],r=null;t.type="text/css";t.id="matchmediajs-test";n.parentNode.insertBefore(t,n);r="getComputedStyle"in window&&window.getComputedStyle(t,null)||t.currentStyle;e={matchMedium:function(e){var n="@media "+e+"{ #matchmediajs-test { width: 1px; } }";if(t.styleSheet){t.styleSheet.cssText=n}else{t.textContent=n}return r.width==="1px"}}}return function(t){return{matches:e.matchMedium(t||"all"),media:t||"all"}}}());

(function() {
    window.T.Analytics = flight.component(init);
    function init() {
        this.reach_goal = function(name) {
            if (window.T.settings.debug) {
                return;
            }
            if (typeof(window.yaCounter22301035) != 'undefined') {
                window.yaCounter22301035.reachGoal(name);
            }
            // TODO: Google analytics goals
        };

        this.goal_cart = function() {
            this.reach_goal('goal_cart');
        }

        this.after('initialize', function() {
            this.on('cart:updated', this.goal_cart);
        });
    }
})();
$(function() {
    window.T.Analytics.attachTo(document);
});


$(function() {

    $(document).ajaxStart(function() {
        NProgress.start();
    });
    $(document).ajaxStop(function() {
        NProgress.done();
    });

    $('.header-auth .header-auth-login').click(function(event) {
        event.preventDefault();
        $('#login').modal();
        $('#login-email').focus();
    });

    // Навигация в меню категорий
    $('.categories-navigation ul').menuAim({
        submenuDirection: 'below',
        activationDelay: 100,
        activate: function(li) {
            li = $(li);
            li.addClass('active');
            var el = li.find('.children');
            var list_right = li.parent().offset().left + li.parent().outerWidth();
            var offset = el.offset();
            if (typeof(offset) == 'undefined')
                return;

            el.css({
                display: 'block',
                visibility: 'hidden'
            });
            var width = 5;  // Небольшой отступ, чтобы влезли все блоки
            el.find('.col').each(function(idx, child) {
                child = $(child);
                width += child.outerWidth();
            });
            el.css('width', width + 'px');

            // Находим левую координату блока
            var left = parseInt(el.data('left'), 10);
            if (isNaN(left))
                left = 0;
            var right = el.offset().left + el.outerWidth();
            if (right > list_right) {
                left = list_right - right - 6;
            }
            el.attr('data-left', left.toString());

            el.css({
                display: 'block',
                visibility: 'visible',
                position: 'absolute',
                left: left + 'px',
                top: (li.outerHeight() + 3) + 'px'  // высота + небольшой отступ снизу
            });
            if (typeof(el.data('height-computed')) != 'undefined') {
                return;
            }

            var first_row_col_idx = 0,
                columns = el.find('.col'),
                rows = Math.ceil(columns.length / 5);

            for (var i=0; i<rows; i++) {
                var col_height = 0;
                var header_height = 0;
                var cols = columns.slice(i*5, i*5+5);
                cols.each(function(idx, col) {
                    var h = $(col).outerHeight();
                    var hh = $(col).find('h5').outerHeight();
                    if (h > col_height) {
                        col_height = h;
                    }
                    if (hh > header_height) {
                        header_height = hh;
                    }
                });
                cols.each(function(idx, col) {
                    col = $(col);
                    col.css('height', (col_height + 10) + 'px');
                    col.find('h5').css('height', (header_height + 0) + 'px');
                    if (idx == 4) {
                        col.addClass('last-row-child');
                    }
                });
            }

            el.attr('data-height-computed', 'true');
        },
        deactivate: function(el) {
            el = $(el);
            el.removeClass('active');
            el.find('.children').hide();
        },
        exitMenu: function() {
            return true;
        }
    });

    // TODO: заменить на flight.component
    // Сабмит формы сортировки в списке товаров
    $('.nodes-tools form select').change(function(event) {
        var form = $(this).parents('form');
        form.submit();
    });

    // Выравнивание высот колонок
    if (window.matchMedia('screen').matches) {
        $('.col-content,.col-sidebar').equalHeightColumns();
    }

    // Прелоадинг фоновых изображений
    $('*[data-image-preload]').each(function(idx, el) {
        var image = new Image();
        image.src = el.getAttribute('data-image-preload');
    });

    // Запускаем все карусели
    $('.carousel').carousel('cycle');

    $('.complementary-list li').bind('mouseenter mouseleave', function() {
        var img = $(this).find('img');
        var old_url = img.attr('src');
        var new_url = img.attr('data-image-preload');
        if (new_url.length == 0) {
            return;
        }
        img.attr('src', new_url).attr('data-image-preload', old_url);
    });

    $('header .search-block input[type="search"]').typeahead({
        name: 'search',
        remote: '/search/ajax/?query=%QUERY',
        template: '<img src="{{image}}" alt=""><div><span>{{title}}</span></div>',
        limit: 5,
        engine: Hogan
    });
    $(document).on('typeahead:selected', function(e, obj) {
        window.location = obj.url;
    });

    $('.fast-view').click(function(e) {
        e.preventDefault();
        var self = $(this);
        var image_url = self.data('image');
        var url = self.data('url');
        var title = self.parents('li').find('h6 a').text();
        var image = $('<img/>').attr('src', image_url);
        var view = $('#fastview');
        view.find('.image').empty().append(image);
        view.find('.modal-title').text(title);
        $.get(url, function(content) {
            view.find('.content').html(content);
        });
        view.modal();
    });

    // Настраиваем CSRF токены
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    });

});
