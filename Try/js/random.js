for (var i = 0, limit = elemCount; i < limit; i++) {
        var color = '#'+ Math.round(0xffffff * Math.random()).toString(16);
    
    
        $newdiv = $('<div/>').css({
            'border-radius': '50%',
            'width':divsize+'px',
            'height':divsize+'px',
            'background-color': color
             });

   var posx =(Math.random() * ($(".random_box").width() - divsize) + $(".random_box").offset().left).toFixed();
   var posy =(Math.random() * ($(".random_box").height() - divsize) + divsize/2.7).toFixed();

        $newdiv.css({
        'position':'absolute',
        'left':posx + 'px',
        'top':posy+'px'
    }).appendTo( '.random_box' );

    }