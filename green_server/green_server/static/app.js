// drop mobile navigation
function mobileNav() {
    var burger = document.getElementById("burger");
    var nav = document.querySelector("nav");
    var navContainer = document.querySelector(".nav-container");

    // transform burger to/ from X
    function activeBurger() {
        var bar1 = document.getElementById("bar1");
        var bar2 = document.getElementById("bar2");
        var bar3 = document.getElementById("bar3");

        bar1.classList.toggle("bar1-active");
        bar2.classList.toggle("bar2-active");
        bar3.classList.toggle("bar3-active");
    }

    burger.addEventListener('click', () => {
        activeBurger();
        nav.classList.toggle("drop-nav");
        navContainer.classList.toggle("nav-container-active");
    });
}

// change style for active page
function activeNav() {
    var navLinks = document.querySelectorAll(".nav-link");
    var currentPage = window.location.href;

    for (i=0; i < navLinks.length; i++) {
        if (currentPage == navLinks[i].href) {
            navLinks[i].classList.toggle("nav-link-active");
        }
    }

}

const app = () => {
    mobileNav();
    activeNav();
}