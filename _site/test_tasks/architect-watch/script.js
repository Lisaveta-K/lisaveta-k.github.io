$(document).ready(function(){
// Получаем текущие значения времени (в цифровом формате)
    var secNow = new Date().getSeconds(); //Секунды
    var minNow = new Date().getMinutes(); //Минуты
    var hourNow = new Date().getHours(); //Часы
//Поскольку часы аналоговые, значения в цифровом формате перевдим в градусы.
//Получаем углы наклона стрелок.
    var secPos = secNow*6-90; //Секундная стрелка
    var minPos = minNow*6+secNow*0.1-90; //Минутная стрелка
    var hourPos = hourNow*30+minNow*0.5-90; //Часовая стрелка
    
//Задаём начальное положение каждой из стрелок
//Используя свойство transform rotate, поворачиваем стрелки на значение градусов, уже хранящееся в переменных secPos, minPos, hourPos.

//Секундная стрелка

//Свойство transform в каждом случае, прописано для различных браузеров

    $('.second').css('-moz-transform', 'rotate('+secPos+'deg)') //Firefox
        .css('-ms-transform', 'rotate('+secPos+'deg)') //IE
        .css('-webkit-transform', 'rotate('+secPos+'deg)') //Safari, Chrome, iOS
        .css('-o-transform', 'rotate('+secPos+'deg)') //Opera
        .css('transform', 'rotate('+secPos+'deg)') //css3
        .removeClass('hidden'); //После того, как положение стрелки задано, она становится видимой

//Минутная стрелка
    $('.minute').css('-moz-transform', 'rotate('+minPos+'deg)')
        .css('-ms-transform', 'rotate('+minPos+'deg)')
        .css('-webkit-transform', 'rotate('+minPos+'deg)')
        .css('-o-transform', 'rotate('+minPos+'deg)')
        .css('transform', 'rotate('+minPos+'deg)')
        .removeClass('hidden');

//Часовая стрелка
    $('.hour').css('-moz-transform', 'rotate('+hourPos+'deg)')
        .css('-ms-transform', 'rotate('+hourPos+'deg)')
        .css('-webkit-transform', 'rotate('+hourPos+'deg)')
        .css('-o-transform', 'rotate('+hourPos+'deg)')
        .css('transform', 'rotate('+hourPos+'deg)')
        .removeClass('hidden');
        
//Объемная фигура имеет 12 граней, помимо стрелок, являющихся основными, добавляем еще 9 граней        



    $('.second .pseudo-minute').css('-moz-transform', 'rotate('+(-secPos+minPos)+'deg)')
        .css('-ms-transform', 'rotate('+(-secPos+minPos)+'deg)')
        .css('-webkit-transform', 'rotate('+(-secPos+minPos)+'deg)')
        .css('-o-transform', 'rotate('+(-secPos+minPos)+'deg)')
        .css('transform', 'rotate('+(-secPos+minPos)+'deg)');

    $('.second .pseudo-hour').css('-moz-transform', 'rotate('+(-secPos+hourPos)+'deg)')
        .css('-ms-transform', 'rotate('+(-secPos+hourPos)+'deg)')
        .css('-webkit-transform', 'rotate('+(-secPos+hourPos)+'deg)')
        .css('-o-transform', 'rotate('+(-secPos+hourPos)+'deg)')
        .css('transform', 'rotate('+(-secPos+hourPos)+'deg)');

    $('.second .pseudo-hour .pseudo-minute').css('-moz-transform', 'rotate('+(-hourPos+minPos)+'deg)')
        .css('-ms-transform', 'rotate('+(-hourPos+minPos)+'deg)')
        .css('-webkit-transform', 'rotate('+(-hourPos+minPos)+'deg)')
        .css('-o-transform', 'rotate('+(-hourPos+minPos)+'deg)')
        .css('transform', 'rotate('+(-hourPos+minPos)+'deg)');



    $('.minute .pseudo-second').css('-moz-transform', 'rotate('+(-minPos+secPos)+'deg)')
        .css('-ms-transform', 'rotate('+(-minPos+secPos)+'deg)')
        .css('-webkit-transform', 'rotate('+(-minPos+secPos)+'deg)')
        .css('-o-transform', 'rotate('+(-minPos+secPos)+'deg)')
        .css('transform', 'rotate('+(-minPos+secPos)+'deg)');

    $('.minute .pseudo-hour').css('-moz-transform', 'rotate('+(-minPos+hourPos)+'deg)')
        .css('-ms-transform', 'rotate('+(-minPos+hourPos)+'deg)')
        .css('-webkit-transform', 'rotate('+(-minPos+hourPos)+'deg)')
        .css('-o-transform', 'rotate('+(-minPos+hourPos)+'deg)')
        .css('transform', 'rotate('+(-minPos+hourPos)+'deg)');

    $('.minute .pseudo-second .pseudo-hour').css('-moz-transform', 'rotate('+(-secPos+hourPos)+'deg)')
        .css('-ms-transform', 'rotate('+(-secPos+hourPos)+'deg)')
        .css('-webkit-transform', 'rotate('+(-secPos+hourPos)+'deg)')
        .css('-o-transform', 'rotate('+(-secPos+hourPos)+'deg)')
        .css('transform', 'rotate('+(-secPos+hourPos)+'deg)');



    $('.hour .pseudo-minute').css('-moz-transform', 'rotate('+(-hourPos+minPos)+'deg)')
        .css('-ms-transform', 'rotate('+(-hourPos+minPos)+'deg)')
        .css('-webkit-transform', 'rotate('+(-hourPos+minPos)+'deg)')
        .css('-o-transform', 'rotate('+(-hourPos+minPos)+'deg)')
        .css('transform', 'rotate('+(-hourPos+minPos)+'deg)');

    $('.hour .pseudo-second').css('-moz-transform', 'rotate('+(-hourPos+secPos)+'deg)')
        .css('-ms-transform', 'rotate('+(-hourPos+secPos)+'deg)')
        .css('-webkit-transform', 'rotate('+(-hourPos+secPos)+'deg)')
        .css('-o-transform', 'rotate('+(-hourPos+secPos)+'deg)')
        .css('transform', 'rotate('+(-hourPos+secPos)+'deg)');

    $('.hour .pseudo-minute .pseudo-second').css('-moz-transform', 'rotate('+(-minPos+secPos)+'deg)')
        .css('-ms-transform', 'rotate('+(-minPos+secPos)+'deg)')
        .css('-webkit-transform', 'rotate('+(-minPos+secPos)+'deg)')
        .css('-o-transform', 'rotate('+(-minPos+secPos)+'deg)')
        .css('transform', 'rotate('+(-minPos+secPos)+'deg)');

//Задаём изменение положения стрелки, изменяя переменную secPos
//Когда секундная стрелка совершает полный оборот, возвращаем значение градусов к нулевой отметке

    window.secTimer = setInterval(function(){
        secPos+=0.06;
        if (secPos >= 360) secPos-=360;

        $('.second').css('-moz-transform', 'rotate('+secPos+'deg)')
            .css('-ms-transform', 'rotate('+secPos+'deg)')
            .css('-webkit-transform', 'rotate('+secPos+'deg)')
            .css('-o-transform', 'rotate('+secPos+'deg)')
            .css('transform', 'rotate('+secPos+'deg)');


//Перемещаем грани фигуры, не являющиеся основными стрелками в соответствии с новым положением секундной стрелки

        $('.second .pseudo-minute').css('-moz-transform', 'rotate('+(-secPos+minPos)+'deg)')
            .css('-ms-transform', 'rotate('+(-secPos+minPos)+'deg)')
            .css('-webkit-transform', 'rotate('+(-secPos+minPos)+'deg)')
            .css('-o-transform', 'rotate('+(-secPos+minPos)+'deg)')
            .css('transform', 'rotate('+(-secPos+minPos)+'deg)');

        $('.second .pseudo-hour').css('-moz-transform', 'rotate('+(-secPos+hourPos)+'deg)')
            .css('-ms-transform', 'rotate('+(-secPos+hourPos)+'deg)')
            .css('-webkit-transform', 'rotate('+(-secPos+hourPos)+'deg)')
            .css('-o-transform', 'rotate('+(-secPos+hourPos)+'deg)')
            .css('transform', 'rotate('+(-secPos+hourPos)+'deg)');

        $('.second .pseudo-hour .pseudo-minute').css('-moz-transform', 'rotate('+(-hourPos+minPos)+'deg)')
            .css('-ms-transform', 'rotate('+(-hourPos+minPos)+'deg)')
            .css('-webkit-transform', 'rotate('+(-hourPos+minPos)+'deg)')
            .css('-o-transform', 'rotate('+(-hourPos+minPos)+'deg)')
            .css('transform', 'rotate('+(-hourPos+minPos)+'deg)');



        $('.minute .pseudo-second').css('-moz-transform', 'rotate('+(-minPos+secPos)+'deg)')
            .css('-ms-transform', 'rotate('+(-minPos+secPos)+'deg)')
            .css('-webkit-transform', 'rotate('+(-minPos+secPos)+'deg)')
            .css('-o-transform', 'rotate('+(-minPos+secPos)+'deg)')
            .css('transform', 'rotate('+(-minPos+secPos)+'deg)');

        $('.minute .pseudo-hour').css('-moz-transform', 'rotate('+(-minPos+hourPos)+'deg)')
            .css('-ms-transform', 'rotate('+(-minPos+hourPos)+'deg)')
            .css('-webkit-transform', 'rotate('+(-minPos+hourPos)+'deg)')
            .css('-o-transform', 'rotate('+(-minPos+hourPos)+'deg)')
            .css('transform', 'rotate('+(-minPos+hourPos)+'deg)');

        $('.minute .pseudo-second .pseudo-hour').css('-moz-transform', 'rotate('+(-secPos+hourPos)+'deg)')
            .css('-ms-transform', 'rotate('+(-secPos+hourPos)+'deg)')
            .css('-webkit-transform', 'rotate('+(-secPos+hourPos)+'deg)')
            .css('-o-transform', 'rotate('+(-secPos+hourPos)+'deg)')
            .css('transform', 'rotate('+(-secPos+hourPos)+'deg)');


        $('.hour .pseudo-minute').css('-moz-transform', 'rotate('+(-hourPos+minPos)+'deg)')
            .css('-ms-transform', 'rotate('+(-hourPos+minPos)+'deg)')
            .css('-webkit-transform', 'rotate('+(-hourPos+minPos)+'deg)')
            .css('-o-transform', 'rotate('+(-hourPos+minPos)+'deg)')
            .css('transform', 'rotate('+(-hourPos+minPos)+'deg)');

        $('.hour .pseudo-second').css('-moz-transform', 'rotate('+(-hourPos+secPos)+'deg)')
            .css('-ms-transform', 'rotate('+(-hourPos+secPos)+'deg)')
            .css('-webkit-transform', 'rotate('+(-hourPos+secPos)+'deg)')
            .css('-o-transform', 'rotate('+(-hourPos+secPos)+'deg)')
            .css('transform', 'rotate('+(-hourPos+secPos)+'deg)');

        $('.hour .pseudo-minute .pseudo-second').css('-moz-transform', 'rotate('+(-minPos+secPos)+'deg)')
            .css('-ms-transform', 'rotate('+(-minPos+secPos)+'deg)')
            .css('-webkit-transform', 'rotate('+(-minPos+secPos)+'deg)')
            .css('-o-transform', 'rotate('+(-minPos+secPos)+'deg)')
            .css('transform', 'rotate('+(-minPos+secPos)+'deg)');
    },10);


//Задаём поворот минутной стрелки
    window.minTimer = setInterval(function(){
        secNow = new Date().getSeconds();
        minNow = new Date().getMinutes();
        minPos = minNow*6+secNow*0.1-90;

        minPos+=0.06;
        if (minPos >= 360) minPos-=360;

        $('.minute').css('-moz-transform', 'rotate('+minPos+'deg)')
            .css('-ms-transform', 'rotate('+minPos+'deg)')
            .css('-webkit-transform', 'rotate('+minPos+'deg)')
            .css('-o-transform', 'rotate('+minPos+'deg)')
            .css('transform', 'rotate('+minPos+'deg)');
    },600);
    
    
//Задаём поворот часовой стрелки


    window.hourTimer = setInterval(function(){
        minNow = new Date().getMinutes();
        hourNow = new Date().getHours();
        hourPos = hourNow*30+minNow*0.5-90;

        hourPos+=0.06;
        if (hourPos >= 360) hourPos-=360;

        $('.hour').css('-moz-transform', 'rotate('+hourPos+'deg)')
            .css('-ms-transform', 'rotate('+hourPos+'deg)')
            .css('-webkit-transform', 'rotate('+hourPos+'deg)')
            .css('-o-transform', 'rotate('+hourPos+'deg)')
            .css('transform', 'rotate('+hourPos+'deg)');
    },14400);
    /*for (var i=0; i<360; i+=30) {
        $('.dial').append('<div class="label" style="-moz-transform: rotate('+i+'deg); -ms-transform: rotate('+i+'deg); -webkit-transform: rotate('+i+'deg);  -o-transform: rotate('+i+'deg); transform: rotate('+i+'deg); "></div>');
    }*/
});