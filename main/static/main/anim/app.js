//$(document).foundation();



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

$(".sbar-container").on("mouseenter", () => {
    $(".sbar-container").children().addClass("hover")
})

$(".sbar-container").on("mouseleave", () => {
    $(".sbar-container").children().removeClass("hover")
})

let toggleSubmenu = false;

$(".sbar-container").on("click", () => {
    toggleSubmenu = !toggleSubmenu;
    if(toggleSubmenu) {
        $(".top-bar.s2").addClass("visible");
    } else {
        $(".top-bar.s2").removeClass("visible");
    }
})

$(window).on("click", () => {
    toggleSubmenu = false;
    $(".top-bar.s2").removeClass("visible"); 
});


