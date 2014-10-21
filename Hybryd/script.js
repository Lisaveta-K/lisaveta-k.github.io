 $( document ).ready( function(){
 
 $(document).click(function() {
            // Simply hide the submenu on any click. Again, this is just a hacked
            // together menu/submenu structure to show the use of jQuery-menu-aim.
            $(".popover").css("display", "none");
            $("a.maintainHover").removeClass("maintainHover");
        });
 
var $menu = $(".navmenu--list");

        // jQuery-menu-aim: <meaningful part of the example>
        // Hook up events to be fired on menu row activation.
        $menu.hover(function(){
        $menu.menuAim({
            activate: activateSubmenu,
            deactivate: deactivateSubmenu
        });
        });
 
       function activateSubmenu(row) {
            var $row = $(row),
			$submenu=$row.children(".popover"); 
			
            // Show the submenu
            $submenu.css({
                "opacity": "1",
                "left": "100%",
    			"pointer-events": "all"
            });
                    
            $row.find("a").addClass("maintainHover");
        }
        
function deactivateSubmenu(row) {
        var $row = $(row),
		$submenu=$row.children(".popover"); 
            
            $submenu.css({
                "opacity": "0",
				"left": "0",
    			"pointer-events": "none"
            });
        
            
            $row.find("a").removeClass("maintainHover");
        }
   } );
