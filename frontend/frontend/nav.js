"use strict";


const NAV_LINKS = [

  {
    href: "index.html",
    label: "Home"
  },

  {
    href: "engine.html",
    label: "Simulation"
  },

  {
    href: "explorer.html",
    label: "Explorer"
  },

  {
    href: "theory.html",
    label: "Visual Theory"
  },

  {
    href: "validation.html",
    label: "Validation"
  },

  {
    href: "about.html",
    label: "About"
  }

];


function buildNavigation() {

  const root =
    document.getElementById(
      "nav-root"
    );


  if (!root) {
    return;
  }


  const currentPage =
    window.location.pathname
      .split("/")
      .pop()
      ||
      "index.html";


  const nav =
    document.createElement(
      "nav"
    );


  nav.className =
    "site-nav";


  /* =====================================================
     BRAND
     ===================================================== */

  const brand =
    document.createElement(
      "a"
    );


  brand.href =
    "index.html";


  brand.className =
    "nav-brand";


  brand.innerHTML =
    `
      <span class="nav-black-hole"></span>

      <span class="nav-brand-text">
        PHOTON FORGE
      </span>
    `;


  nav.appendChild(
    brand
  );


  /* =====================================================
     LINKS
     ===================================================== */

  const links =
    document.createElement(
      "div"
    );


  links.className =
    "nav-links";


  NAV_LINKS.forEach(
    item => {

      const anchor =
        document.createElement(
          "a"
        );


      anchor.href =
        item.href;


      anchor.textContent =
        item.label;


      if (
        currentPage ===
        item.href
      ) {

        anchor.classList.add(
          "active"
        );

      }


      links.appendChild(
        anchor
      );

    }
  );


  nav.appendChild(
    links
  );


  root.appendChild(
    nav
  );

}


buildNavigation();