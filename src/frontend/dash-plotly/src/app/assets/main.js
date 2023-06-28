(() => {
  const sidebarNavWrapper = document.getElementById("sidebar-nav-wrapper");
  const mainWrapper = document.querySelector(".main-wrapper");
  const menuToggleButton = document.querySelector("#menu-toggle");
  const menuToggleButtonIcon = document.querySelector("#menu-toggle i");

  console.log("Sidebar ", sidebarNavWrapper);
  menuToggleButton.addEventListener("click", () => {
    sidebarNavWrapper.classList.toggle("active");
    // overlay.classList.add("active");
    mainWrapper.classList.toggle("active");
  });
})();
