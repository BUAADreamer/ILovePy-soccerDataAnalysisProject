// JavaScript Document
$(document).ready(function(){
    $(window).scroll(function(){
        
		if( $(this).scrollTop() > 600 ) {$(".backtotop").fadeIn(800)}
		if( $(this).scrollTop() < 600 ) {$(".backtotop").fadeOut(800)}
        
	});
});



$(document).ready(function(){
    $("#solid").click(function(event){
        event.preventDefault();
        $("body,html").animate({
            scrollTop:0
        })
        $(this).fadeOut(1);
        
        $("#cover").animate({
            opacity:1.0,
            bottom:700
        })
        $("#cover").animate({
            opacity:0
        })
        $("#cover").animate({
            bottom:50
        })
        $(this).delay(1000).fadeIn(1);
    })
})
