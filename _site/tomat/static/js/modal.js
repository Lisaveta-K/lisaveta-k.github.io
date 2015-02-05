$(document).ready(function(){
    var my_cookie = $.cookie('social-modal');
    var socialModal = $('#social-modal');
    if (!my_cookie || my_cookie !== "true") {
        socialModal.modal('show');
    }
    socialModal.on('hidden.bs.modal', function () {
        $.cookie('social-modal', 'true', {
            path: '/',
            expires: 365
        });
    });
});
