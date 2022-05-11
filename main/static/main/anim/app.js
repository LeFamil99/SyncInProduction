//$(document).foundation();

const controller = new ScrollMagic.Controller();

/*new ScrollMagic.Scene({
    triggerElement: "#parallax",
    triggerHook: "onEnter",
})
.duration("200%")
.setTween("#parallax", {
    backgroundPosition: "50% 1000%",
    ease: Linear.easeNone
})
.addIndicators()
.addTo(controller)*/
var divId;

$('.nav-link').on("click", function() {
    toggleSubmenu = false;
    $(".top-bar.s2").removeClass("visible"); 
    divId = $(this).attr('href');
    $('html, body').animate({
        scrollTop: $(divId).offset().top - 100
    }, 200, "swing");
});

