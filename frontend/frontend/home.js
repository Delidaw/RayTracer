"use strict";


/* =========================================================
   PHOTON FORGE HOMEPAGE

   This page intentionally does NOT run the WebGL renderer.
   It only fetches small physics values from Flask.
   ========================================================= */


const horizonElement =
  document.getElementById(
    "homeHorizon"
  );


const iscoElement =
  document.getElementById(
    "homeIsco"
  );


const photonElement =
  document.getElementById(
    "homePhoton"
  );


const ergosphereElement =
  document.getElementById(
    "homeErgosphere"
  );


const backendDot =
  document.getElementById(
    "homeBackendDot"
  );


const backendStatus =
  document.getElementById(
    "homeBackendStatus"
  );


function formatRadius(
  value
) {

  if (
    value === null ||
    value === undefined
  ) {

    return "—";

  }


  return (
    Number(
      value
    ).toFixed(3) +
    " M"
  );

}


async function loadHomepagePhysics() {

  try {

    const response =
      await fetch(
        "/api/black-hole-properties" +
        "?mode=kerr" +
        "&mass=1" +
        "&spin=0.9"
      );


    if (
      !response.ok
    ) {

      throw new Error(
        "API unavailable"
      );

    }


    const result =
      await response.json();


    horizonElement.textContent =
      formatRadius(
        result.event_horizon
      );


    iscoElement.textContent =
      formatRadius(
        result.isco
      );


    photonElement.textContent =
      formatRadius(
        result.photon_sphere
      );


    ergosphereElement.textContent =
      formatRadius(
        result.ergosphere
      );


    backendDot.classList.add(
      "connected"
    );


    backendStatus.textContent =
      "Physics values from Flask backend";

  }

  catch (
    error
  ) {

    backendStatus.textContent =
      "Using cached reference values";

  }

}


loadHomepagePhysics();