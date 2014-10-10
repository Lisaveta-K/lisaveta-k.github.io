

       var $menu = $(".navmenu--list st-opened");

        // jQuery-menu-aim: <meaningful part of the example>
        // Hook up events to be fired on menu row activation.
        $menu.menuAim({
            rowSelector: "li.navmenu--list_item",
            activate: activateSubmenu,
            deactivate: deactivateSubmenu
        });
 
        function activateSubmenu() {
            $(".navmenu--list_item").hover(
  function() {
    $( ".popover" ).css("opacity","1");
  }  
 );
        }

        function deactivateSubmenu() {
            $(".navmenu--list_item").mouseleave(
  function() {
    $( ".popover" ).css("opacity","0");
  }  
);
        }

       