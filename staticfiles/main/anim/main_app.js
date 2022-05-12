// Ce fichier gère toutes les animations présentes sur la page d'accueil de notre site

const controller = new ScrollMagic.Controller();

// Fonction décrivant la courbe d'augmentation des nombres sur la page d'accueil
const easeOutExpo = function (t, b, c, d) {
    return c * (-Math.pow(2, -10 * t / d) + 1) * 1024 / 1023 + b;
}

// Cette fonction crée l'animation des nombres de la page d'accueil 
// grâce à la librairie CountUp.js
let demos = []
try{ 
    for(let i = 0; i < 4; i++) {
        let demo = new CountUp("purecounter" + i, $("#purecounter" + i).attr("data-purecounter-end"), {
            duration: 2,
            smartEasingThreshold: 999,
            smartEasingAmount: 333,
            useEasing : true,
            useGrouping : true,
            separator : '&#8239;',
            // easingFn: easeOutExpo
        });
        demos.push(demo)
        $("#purecounter" + i).parent().attr("style", "font-size: " + (16 / $("#purecounter" + i).attr("data-purecounter-end").toString().length) + "rem !important")
    }
} catch(e) {
    console.log(e.message)
}
    

var path = document.querySelector('.path');
var length = path.getTotalLength();
console.log(length) // 1506

// Détecte quand tous les nombres ont terminé leur animation
let countUpDone = new Array(demos.length).fill(false);

// Cette fonction crée l'animation du chemin dans la Roadmap
$(window).on("scroll", () => {
    for(let i = 0; i < 4; i++) {
        if(!countUpDone[i] && $(window).scrollTop() + $(window).height() - 120 > $("#purecounter" + i).offset().top) {
            countUpDone[i] = true;
            demos[i].start(() => { console.log("Pas bienzz") });
        }
    }


    // Crée l'animation de la liogne
    let curScroll = ($(window).scrollTop() + $(window).height() - 300) - ($(".roadmap").offset().top);
    console.log(curScroll)
    $(".path").attr("style", "stroke-dashoffset: " + (length - Math.min(length, (length / 800) * curScroll)))

    //Crée l'animation des icones de destination
    if($(window).scrollTop() + $(window).height() > $(".destination.d1").offset().top + 220) {
        $(".destination.d1").addClass("active")
    } else $(".destination.d1").removeClass("active")

    if($(window).scrollTop() + $(window).height() > $(".destination.d2").offset().top + 200) {
        $(".destination.d2").addClass("active")
    } else $(".destination.d2").removeClass("active")

    if($(window).scrollTop() + $(window).height() > $(".destination.d3").offset().top + 100) {
        $(".destination.d3").addClass("active")
    } else $(".destination.d3").removeClass("active")

    if($(window).scrollTop() + $(window).height() > $(".destination.d4").offset().top + 130) {
        $(".destination.d4").addClass("active")
    } else $(".destination.d4").removeClass("active")
})

// console.log($(".big").children(".purecounter").html().length)




gsap.registerPlugin(MotionPathPlugin);

gsap.set("#pen", { xPercent: -50, yPercent: -50 })

// Permet d'ignorer la hauteur de la barre de navigation dans le template
$('.top-bar').on("click", e => {
    e.stopPropagation();
});