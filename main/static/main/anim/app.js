// Ce fichier gère toutes les animations présentes dans la barre de navigation 
// de la version mobile de chacune des pages du site

var divId;

// Fonction jquery permettant de cacher le menu déroulant lorsqu'une option est choisie
$('.nav-link').on("click", function() {
    toggleSubmenu = false;
    $(".top-bar.s2").removeClass("visible"); 
    divId = $(this).attr('href');
    $('html, body').animate({
        scrollTop: $(divId).offset().top - 100
    }, 200, "swing");
});

// Détecte si la souris est au-dessus d'une des option du menu
$(".sbar-container").on("mouseenter", () => {
    $(".sbar-container").children().addClass("hover")
})

// Détecte si la souris n'est plus au-dessus d'une des option du menu
$(".sbar-container").on("mouseleave", () => {
    $(".sbar-container").children().removeClass("hover")
})

let toggleSubmenu = false;

// Fonction jquery permettan de montrer/cacher le menu déroulant
$(".sbar-container").on("click", () => {
    toggleSubmenu = !toggleSubmenu;
    if(toggleSubmenu) {
        $(".top-bar.s2").addClass("visible");
    } else {
        $(".top-bar.s2").removeClass("visible");
    }
})

// Fonction jquery permettant de cacher le menu déroulant si on clique n'import où d'autre
$(window).on("click", () => {
    toggleSubmenu = false;
    $(".top-bar.s2").removeClass("visible"); 
});


