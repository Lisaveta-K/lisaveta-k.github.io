 $(document).click(function() {
            // Simply hide the submenu on any click. Again, this is just a hacked
            // together menu/submenu structure to show the use of jQuery-menu-aim.
            $(".popover").css("display", "none");
            $("a.maintainHover").removeClass("maintainHover");
        });
$( document ).ready( function(){
var $menu = $(".navmenu--list");

        // jQuery-menu-aim: <meaningful part of the example>
        // Hook up events to be fired on menu row activation.
        $menu.hover(function(){
        $menu.menuAim({
            activate: activateSubmenu,
            deactivate: deactivateSubmenu
        });
        });
        // jQuery-menu-aim: </meaningful part of the example>

        // jQuery-menu-aim: the following JS is used to show and hide the submenu
        // contents. Again, this can be done in any number of ways. jQuery-menu-aim
        // doesn't care how you do this, it just fires the activate and deactivate
        // events at the right times so you know when to show and hide your submenus.
        
       function activateSubmenu(row) {
            var $row = $(row),
			$submenu=$row.children(".submenu"); 
			
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
		$submenu=$row.children(".submenu"); 
            
            $submenu.css({
                "opacity": "0",
				"left": "0",
    			"pointer-events": "none"
            });
        
            
            $row.find("a").removeClass("maintainHover");
        }
   } );
