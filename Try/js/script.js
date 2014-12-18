$( window ).resize(function(){
  makeDiv();
});


function makeDiv(){
   
   var elemCount = $("input[name=elemQ]").val();
   var left = $(".random_box").offset().left;

  //$(".random_box").width() = $("input[name=width]").val();
  //$(".random_box").height() = $("input[name=height]").val();
  var width = $(".random_box").width();
  var height = $(".random_box").height();
  //var count_divs = $(".random_box").children().length;

  //for (var j = 0, limit = count_divs; j < limit; j++) {
 // }

$(".random_box").children().remove();

    if (elemCount == 1){
  var divsize = height/2;
  var posx = width/2 - divsize/2 + left;
  var posy = height/2 - divsize/3;
  DrawElement(divsize, posx, posy);
    }

    if (elemCount == 2){
  var divsize = (height/2);
  for (var i = 0, limit = elemCount; i < limit; i++) {
  var posx = (width/3)*(i+1) - (divsize/2) + left;
  var posy = height/2 - divsize/3;
  DrawElement(divsize, posx, posy);
      }

    }

    if (elemCount == 3){
  var divsize = height/2;
  for (var i = 0, limit = elemCount; i < limit; i++) {
    var posx = (width/4)*(i+1) - (divsize/2) + left;
    if (i%2==0){
      var posy = height/2 - divsize/1.2;
      DrawElement(divsize, posx, posy);
        }
    if (i%2!=0){
  var posy = height/2;
  DrawElement(divsize, posx, posy);
        }
      }
    }

    if (elemCount == 4){
  var divsize = height/2.4;
  for (var i = 0, limit = elemCount; i < limit; i++) {
    var posx = (width/5)*(i+1) - (divsize/2) + left;
    if (i%2==0){
      var posy = height/2 - divsize/1.2;
      DrawElement(divsize, posx, posy);
        }
    if (i%2!=0){
      var posy = height/2 + divsize/4;
      DrawElement(divsize, posx, posy);
        }
      }
    }

    if (elemCount == 5){
  var divsize = height/2.4;
  for (var i = 0, limit = elemCount; i < limit; i++) {
    var posx = (width/6)*(i+1) - (divsize/2) + left;
    if (i%2==0){
      var posy = height/2 - divsize/2;
      DrawElement(divsize, posx, posy);
        }
    if (i%2!=0){
      var posy = height/2 + divsize/4;
      DrawElement(divsize, posx, posy);
        }
      }
    }

    if (elemCount == 6){
  var divsize = height/2.4;
  for (var i = 0, limit = elemCount; i < limit; i++) {
    var posx = (width/7)*(i+1) - (divsize/2) + left;
    if (i%2==0){
      var posy = height/2 - divsize;
      DrawElement(divsize, posx, posy);
        }
    if (i%2!=0){
      var posy = height/2;
      DrawElement(divsize, posx, posy);
        }
      }
    }

  if (elemCount == 7){
  var divsize = height/2.8;
  for (var i = 0, limit = elemCount; i < limit; i++) {
    if ((i==1) || (i==4)){
      var posx = (width/3)*(i-1) - (divsize/2) + left;
      var posy = height/3 - divsize;
      DrawElement(divsize, posx, posy);
        }
    if ((i==0) || (i==2) || (i==5)){
      var posx = (width/4)*(i1) - (divsize/2) + left;
      var posy = height/3;
      DrawElement(divsize, posx, posy);
        }
    if ((i==3) || (i==6)){
      var posx = (width/3)*(i-2) - (divsize/2) + left;
      var posy = height/3 + divsize;
      DrawElement(divsize, posx, posy);
        }
      }
    }


};

function DrawElement(blockSize, posx, posy){
var color = '#ffffff';
$newdiv = $('<div/>').css({
            'border-radius': '50%',
            'width':blockSize+'px',
            'height':blockSize+'px',
            'background-color': color
             });

    $newdiv.css({
        'position':'absolute',
        'left':posx + 'px',
        'top':posy+'px'
    }).appendTo( '.random_box' );
  };