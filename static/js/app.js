(() => {
  const body = document.body;
  const toggleButtons = document.querySelectorAll("[data-sidebar-toggle]");
  const overlay = document.querySelector("[data-sidebar-overlay]");
  const sidebarLinks = document.querySelectorAll(".sidebar a");
  const desktopMedia = window.matchMedia("(min-width: 981px)");
  const storageKey = "lf-sidebar-collapsed";

  const syncButtonState = () => {
    const expanded = desktopMedia.matches ? !body.classList.contains("sidebar-collapsed") : body.classList.contains("sidebar-open-mobile");
    toggleButtons.forEach((button) => {
      button.setAttribute("aria-expanded", String(expanded));
      button.setAttribute("aria-label", expanded ? "收起导航栏" : "展开导航栏");
      button.setAttribute("title", expanded ? "收起导航栏" : "展开导航栏");
    });
  };

  const closeMobileSidebar = () => {
    body.classList.remove("sidebar-open-mobile");
    syncButtonState();
  };

  const applyDesktopPreference = () => {
    if (!desktopMedia.matches) {
      body.classList.remove("sidebar-collapsed");
      return;
    }

    if (window.localStorage.getItem(storageKey) === "1") {
      body.classList.add("sidebar-collapsed");
    } else {
      body.classList.remove("sidebar-collapsed");
    }
  };

  applyDesktopPreference();
  syncButtonState();

  toggleButtons.forEach((button) => {
    button.addEventListener("click", () => {
      if (desktopMedia.matches) {
        body.classList.toggle("sidebar-collapsed");
        window.localStorage.setItem(storageKey, body.classList.contains("sidebar-collapsed") ? "1" : "0");
      } else {
        body.classList.toggle("sidebar-open-mobile");
      }
      syncButtonState();
    });
  });

  if (overlay) {
    overlay.addEventListener("click", closeMobileSidebar);
  }

  sidebarLinks.forEach((link) => {
    link.addEventListener("click", () => {
      if (!desktopMedia.matches) {
        closeMobileSidebar();
      }
    });
  });

  desktopMedia.addEventListener("change", () => {
    body.classList.remove("sidebar-open-mobile");
    applyDesktopPreference();
    syncButtonState();
  });
})();
