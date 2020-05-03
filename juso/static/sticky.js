// When the user scrolls the page, execute myFunction
window.onscroll = function() {checkSticky()};

// Get the header
var header = document.getElementById("mainNavigation");

// Get the offset position of the navbar
var sticky = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--navbar-offset'));

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function checkSticky() {
  if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
  } else {
    header.classList.remove("sticky");
  }
} 

checkSticky();
