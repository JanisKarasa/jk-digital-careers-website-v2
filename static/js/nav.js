// JavaScript
document.addEventListener("DOMContentLoaded", function () {
  // Get the current page URL
  let currentPage = window.location.pathname;

  // Define the IDs of the navigation links
  let aboutLink = document.getElementById("aboutLink");
  let homeLink = document.getElementById("homeLink");
  let adminLink = document.getElementById("adminLink");

  // Check the current page URL and set the "active" class and aria-current attribute
  if (currentPage.includes("/about")) {
    aboutLink.classList.add("active");
    // homeLink.classList.remove("active");
    // adminLink.classList.remove("active");
    aboutLink.setAttribute("aria-current", "true");
  } else if (currentPage === "/" || currentPage === "") {
    homeLink.classList.add("active");
    // aboutLink.classList.remove("active");
    // adminLink.classList.remove("active");
    homeLink.setAttribute("aria-current", "true");
  } else if (currentPage.includes("/admin")) {
    adminLink.classList.add("active");
    // aboutLink.classList.remove("active");
    // homeLink.classList.remove("active");
    adminLink.setAttribute("aria-current", "true");
  }
});
