"use strict";

(function() {
    window.T.CartWidget = flight.component(init);
    function init() {
        // Обновление данных виджета корзины
        this.reload = function() {
            var self = this;
            $.get(this.$node.attr('data-reload-url'), {from: window.location.pathname}, function(response) {
                self.$node.replaceWith(response);
                // Ребиндим компонент, потому что после .replaceWith мы полностью заменяем ноду
                window.T.CartWidget.teardownAll();
                window.T.CartWidget.attachTo('header .cart-block');
            });
        };

        this.after('initialize', function() {
            this.on(document, 'cart:updated', this.reload)
        });
    }

})();

(function() {

    var CartFormMixin = function() {

        this.submit = function(event) {
            event.preventDefault();
            var params = this.get_request_params();
            this.$node.find('input').each(function(idx, el) {
                params[el.name] = el.value;
            });
            var self = this;
            $.post(this.$node.attr('action'), params, function(response) {
                self.post_request(response);
                self.trigger('cart:updated');
            });

        };

        this.after('initialize', function() {
            this.on('submit', this.submit);
        });

    };

    // Форма добавления в корзину для отдельных товаров в списке
    window.T.CartFormSmall = flight.component(init_small, CartFormMixin);
    function init_small() {
        this.get_request_params = function() {
            return {
                source: 'form-small',
                replace: false
            };
        };

        this.post_request = function(response) {
            this.$node.find('.in-cart').remove();
            this.$node.append(response);
        }
    }

    // Форма добавления в корзину на странице товара
    window.T.CartForm = flight.component(init, CartFormMixin);
    function init() {
        this.get_request_params = function() {
            return {
                replace: false
            }
        };
        this.post_request = function(response) {
            if (this.$node.find('.cart-status').length == 0) {
                this.$node.append(response);
                this.$node.find('.cart-status').animate({
                    height: '100px'
                });
            } else {
                // TODO: fadeOut + fadeIn анимация
                this.$node.find('.cart-status').replaceWith(response);
            }
        };
    }
})();

// Компоненты для страницы с корзиной /cart/
(function() {
    window.T.CartRow = flight.component(init_row);
    function init_row() {

        this.change_timeout = null;

        this.changed = function(event) {
            var self = this;

            if (this.change_timeout != null) {
                window.clearTimeout(this.change_timeout);
            }

            this.change_timeout = window.setTimeout(function() {
                // Значение не изменилось, нет смысла отправлять запрос
                if (parseInt(self.input.attr('data-old-value'), 10) == parseInt(self.input.val(), 10)) {
                    return;
                }

                self.status.animate({
                    opacity: 1.0,
                    delay: 100
                });
                self.submit.button('loading');

                var url = self.$node.parents('table').attr('data-row-update-url');
                $.post(url, {
                    source: 'cart',
                    product: self.$node.attr('data-id'),
                    quantity: self.input.val(),
                    replace: true
                }, function(response) {
                    self.$node.find('td.item-price').text(response.item_total);
                    $('.cart-summary .cart-total-net span:first-child').text(response.net);
                    $('.cart-summary .coupon-state span.value').text(response.coupon);

                    self.trigger('cart:updated');
                    self.submit.button('reset');
                    self.input.attr('data-old-value', self.input.val());

                    self.status.animate({
                        opacity: 0.0,
                        delay: 100
                    });
                });
            }, 1000);
        };

        this.after('initialize', function() {
            this.submit = this.$node.parents('.col-content').find('button');
            this.status = this.$node.find('.cart-actions-refresh');
            this.input = this.$node.find('input');

            this.on(this.input, 'keypress keydown change', this.changed);
            this.input.attr('data-old-value', this.input.val());
        });
    }

    window.T.CartPage = flight.component(init_page);
    function init_page() {
        this.after('initialize', function() {});
    }
})();

$(function() {
    window.T.CartWidget.attachTo('header .cart-block');
    window.T.CartForm.attachTo('form.product-cart-form');
    window.T.CartFormSmall.attachTo('form.product-cart-form-small');
    //window.T.CartPage.attachTo('body.cart-list .col-content');
    window.T.CartRow.attachTo('body.cart-list .col-content table tr');
});
