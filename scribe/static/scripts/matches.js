jQuery(document).ready(function($) {
    $(".course").click(function() {
    	var url = "notes/"+$(this).attr('id');
        window.location = url;
    });
});