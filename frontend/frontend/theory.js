"use strict";


/* =========================================================
   PHOTON FORGE — VISUAL THEORY EXPLORER
   ========================================================= */


/* =========================================================
   ELEMENTS
   ========================================================= */

const schwarzschildButton =
  document.getElementById(
    "schwarzschildMode"
  );

const kerrButton =
  document.getElementById(
    "kerrMode"
  );


const metricLabel =
  document.getElementById(
    "metricLabel"
  );


const eventHorizon =
  document.getElementById(
    "eventHorizon"
  );

const photonSphere =
  document.getElementById(
    "photonSphere"
  );

const iscoRing =
  document.getElementById(
    "iscoRing"
  );

const ergosphereGroup =
  document.getElementById(
    "ergosphereGroup"
  );

const ergosphereLabel =
  document.getElementById(
    "ergosphereLabel"
  );

const rotationAxis =
  document.getElementById(
    "rotationAxis"
  );


const structureTitle =
  document.getElementById(
    "structureTitle"
  );

const structureTag =
  document.getElementById(
    "structureTag"
  );

const structureDescription =
  document.getElementById(
    "structureDescription"
  );

const structureEquation =
  document.getElementById(
    "structureEquation"
  );

const structureSimulation =
  document.getElementById(
    "structureSimulation"
  );


const backendValue =
  document.getElementById(
    "backendValue"
  );

const backendStatus =
  document.getElementById(
    "backendStatusTheory"
  );


const horizonRadiusLabel =
  document.getElementById(
    "horizonRadiusLabel"
  );

const photonRadiusLabel =
  document.getElementById(
    "photonRadiusLabel"
  );

const iscoRadiusLabel =
  document.getElementById(
    "iscoRadiusLabel"
  );


const massReadout =
  document.getElementById(
    "massReadout"
  );


const structureSvg =
  document.getElementById(
    "structureSvg"
  );


/* =========================================================
   APPLICATION STATE
   ========================================================= */

const state = {

  metric: "schwarzschild",

  mass: 1.0,

  spin: 0.9,

  selected:
    "event-horizon",

  zoom: 1.0,

  values: {

    event_horizon: 2.0,

    photon_sphere: 3.0,

    isco: 6.0,

    ergosphere: null

  }

};


/* =========================================================
   THEORY CONTENT
   ========================================================= */

const theoryContent = {

  "event-horizon": {

    title:
      "Event Horizon",

    schwarzschild: {

      tag:
        "Schwarzschild · r = 2M",

      description:
        "The event horizon is the causal boundary of the black hole. Once a future-directed light ray crosses this surface, it cannot return to a distant observer.",

      equation:
        "rₛ = 2M",

      simulation:
        "In the Photon Forge ray tracer, photons crossing the horizon are classified as captured and tracing for that ray is terminated."

    },

    kerr: {

      tag:
        "Kerr · outer horizon r₊",

      description:
        "A rotating Kerr black hole possesses an outer event horizon whose radius depends on both mass and angular momentum.",

      equation:
        "r₊ = M + √(M² − a²)",

      simulation:
        "Kerr rays that cross the outer horizon are marked captured. The horizon becomes smaller as the dimensionless spin approaches its extremal value."

    }

  },


  "photon-sphere": {

    title:
      "Photon Sphere",

    schwarzschild: {

      tag:
        "Schwarzschild · r = 3M",

      description:
        "The photon sphere is the radius at which photons can follow unstable circular null orbits. Even a very small perturbation makes the photon either escape or fall into the black hole.",

      equation:
        "rₚₕ = 3M",

      simulation:
        "Photon Forge validates photon trajectories near r = 3M and uses the region to identify strongly lensed rays and photon-ring behaviour."

    },

    kerr: {

      tag:
        "Kerr · photon region",

      description:
        "Rotation destroys the single spherical photon-orbit radius. Kerr spacetime instead contains a photon region with different prograde and retrograde orbit radii.",

      equation:
        "rₚₕ depends on spin and orbit direction",

      simulation:
        "The visual explorer displays the prograde equatorial photon orbit as a representative radius. The full Kerr photon region is more complex than a single circle."

    }

  },


  "isco": {

    title:
      "ISCO",

    schwarzschild: {

      tag:
        "Innermost Stable Circular Orbit",

      description:
        "ISCO is the smallest radius at which a massive particle can remain on a stable circular orbit around a Schwarzschild black hole.",

      equation:
        "rISCO = 6M",

      simulation:
        "ISCO provides a physically useful reference for the inner structure of an accretion flow and for validating orbital dynamics."

    },

    kerr: {

      tag:
        "Kerr · prograde ISCO",

      description:
        "Frame dragging allows prograde material to orbit closer to a rotating black hole. The ISCO therefore moves inward as positive spin increases.",

      equation:
        "rISCO = rISCO(M, a)",

      simulation:
        "Photon Forge calculates the Kerr ISCO from the black hole spin and uses it as an important orbital reference."

    }

  },


  "ergosphere": {

    title:
      "Ergosphere",

    schwarzschild: {

      tag:
        "Not present",

      description:
        "A non-rotating Schwarzschild black hole has no ergosphere because there is no frame dragging.",

      equation:
        "a = 0 → no ergosphere",

      simulation:
        "This structure becomes available when Kerr mode is selected."

    },

    kerr: {

      tag:
        "Kerr only · frame-dragging region",

      description:
        "The ergosphere lies outside the event horizon. Within it, frame dragging is so strong that no observer can remain stationary relative to infinity.",

      equation:
        "rₑ(θ) = M + √(M² − a²cos²θ)",

      simulation:
        "Photo Forge visualizes the ergosphere and models frame-dragging effects in the Kerr spacetime."

    }

  },


  "accretion-disk": {

    title:
      "Accretion Disk",

    schwarzschild: {

      tag:
        "Hot orbiting matter",

      description:
        "An accretion disk consists of gas and plasma orbiting the black hole. Friction, compression and magnetic processes can heat the material until it radiates strongly.",

      equation:
        "T = T(r)",

      simulation:
        "The renderer checks photon intersections with the disk and applies radial emission, temperature colouring, gravitational redshift and Doppler beaming."

    },

    kerr: {

      tag:
        "Relativistic rotating plasma",

      description:
        "Around a Kerr black hole, disk motion is strongly affected by frame dragging and the spin-dependent ISCO.",

      equation:
        "rinner ≈ rISCO",

      simulation:
        "The GPU preview adds volumetric plasma emission while the Python renderer provides the higher-accuracy reference path."

    }

  },


  "shadow": {

    title:
      "Black Hole Shadow",

    schwarzschild: {

      tag:
        "Apparent capture region",

      description:
        "The black-hole shadow is not the event horizon itself. It is the dark apparent region created because rays launched from those directions are captured by the black hole.",

      equation:
        "bcrit = 3√3 M",

      simulation:
        "Photon Forge classifies captured and escaping photon trajectories to construct the shadow."

    },

    kerr: {

      tag:
        "Spin-distorted shadow",

      description:
        "For a rotating black hole the apparent shadow becomes asymmetric because frame dragging changes photon trajectories differently on the prograde and retrograde sides.",

      equation:
        "shadow shape = f(M, a, inclination)",

      simulation:
        "The Kerr ray tracer uses spin-dependent geodesics to generate the rotating black-hole shadow."

    }

  }

};


/* =========================================================
   LOCAL PHYSICS FORMULAS

   These are used immediately while the page waits for
   the Flask backend.
   ========================================================= */


function schwarzschildValues(
  mass
) {

  return {

    event_horizon:
      2.0 * mass,

    photon_sphere:
      3.0 * mass,

    isco:
      6.0 * mass,

    ergosphere:
      null

  };

}


/* =========================================================
   KERR ISCO
   ========================================================= */

function kerrISCO(
  mass,
  spinFraction
) {

  const a =
    Math.max(
      -0.998,
      Math.min(
        0.998,
        spinFraction
      )
    );


  const z1 =
    1 +

    Math.cbrt(
      1 - a * a
    ) *

    (
      Math.cbrt(
        1 + a
      )

      +

      Math.cbrt(
        1 - a
      )
    );


  const z2 =
    Math.sqrt(
      3 * a * a +
      z1 * z1
    );


  const radius =
    3 +
    z2 -

    Math.sign(
      a || 1
    ) *

    Math.sqrt(
      Math.max(
        0,

        (3 - z1) *

        (
          3 +
          z1 +
          2 * z2
        )
      )
    );


  return radius * mass;

}


/* =========================================================
   KERR PROGRADE PHOTON ORBIT
   ========================================================= */

function kerrPhotonOrbit(
  mass,
  spinFraction
) {

  const a =
    Math.max(
      -0.998,
      Math.min(
        0.998,
        spinFraction
      )
    );


  return (
    2 *
    mass *
    (
      1 +

      Math.cos(
        (
          2 / 3
        ) *

        Math.acos(
          -a
        )
      )
    )
  );

}


/* =========================================================
   KERR VALUES
   ========================================================= */

function kerrValues(
  mass,
  spinFraction
) {

  const dimensionalSpin =
    spinFraction *
    mass;


  const horizon =
    mass +

    Math.sqrt(
      Math.max(
        0,

        mass * mass -

        dimensionalSpin *
        dimensionalSpin
      )
    );


  return {

    event_horizon:
      horizon,

    photon_sphere:
      kerrPhotonOrbit(
        mass,
        spinFraction
      ),

    isco:
      kerrISCO(
        mass,
        spinFraction
      ),

    /*
      Outer ergosphere radius
      at the equatorial plane.
    */

    ergosphere:
      2.0 * mass

  };

}


/* =========================================================
   FORMAT VALUES
   ========================================================= */

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


/* =========================================================
   GET STRUCTURE VALUE
   ========================================================= */

function getStructureValue(
  structure
) {

  switch (
    structure
  ) {

    case "event-horizon":

      return state.values
        .event_horizon;


    case "photon-sphere":

      return state.values
        .photon_sphere;


    case "isco":

      return state.values
        .isco;


    case "ergosphere":

      return state.values
        .ergosphere;


    case "accretion-disk":

      return state.values
        .isco;


    default:

      return null;

  }

}


/* =========================================================
   UPDATE STRUCTURE LABELS
   ========================================================= */

function updateRadiusLabels() {

  horizonRadiusLabel
    .textContent =
      "r = " +
      formatRadius(
        state.values
          .event_horizon
      );


  photonRadiusLabel
    .textContent =
      state.metric ===
      "schwarzschild"

      ? "r = " +
        formatRadius(
          state.values
            .photon_sphere
        )

      : "prograde ≈ " +
        formatRadius(
          state.values
            .photon_sphere
        );


  iscoRadiusLabel
    .textContent =
      "r = " +
      formatRadius(
        state.values
          .isco
      );


  massReadout
    .textContent =
      "M = " +
      state.mass.toFixed(2);

}


/* =========================================================
   UPDATE SVG SCALE

   The visual diagram remains schematic, but relative
   radii change between Schwarzschild and Kerr.
   ========================================================= */

function updateDiagramGeometry() {

  const scale =
    46;


  const horizonRadius =
    Math.max(
      55,

      state.values
        .event_horizon *
      scale
    );


  const photonRadius =
    Math.max(
      horizonRadius + 22,

      state.values
        .photon_sphere *
      scale
    );


  const iscoRadius =
    Math.max(
      photonRadius + 40,

      Math.min(
        315,

        state.values
          .isco *
        scale
      )
    );


  eventHorizon
    .setAttribute(
      "r",
      horizonRadius
    );


  photonSphere
    .setAttribute(
      "r",
      photonRadius
    );


  iscoRing
    .setAttribute(
      "rx",
      iscoRadius
    );


  iscoRing
    .setAttribute(
      "ry",
      iscoRadius * 0.26
    );

}


/* =========================================================
   UPDATE SELECTED STRUCTURE
   ========================================================= */

function selectStructure(
  structure
) {

  if (
    structure ===
      "ergosphere" &&
    state.metric ===
      "schwarzschild"
  ) {

    return;

  }


  state.selected =
    structure;


  const content =
    theoryContent[
      structure
    ];


  const metricContent =
    content[
      state.metric
    ];


  structureTitle
    .textContent =
      content.title;


  structureTag
    .textContent =
      metricContent.tag;


  structureDescription
    .textContent =
      metricContent
        .description;


  structureEquation
    .textContent =
      metricContent
        .equation;


  structureSimulation
    .textContent =
      metricContent
        .simulation;


  const value =
    getStructureValue(
      structure
    );


  if (
    structure ===
    "shadow"
  ) {

    backendValue
      .textContent =
        state.metric ===
        "schwarzschild"

        ? "bcrit ≈ " +
          (
            3 *
            Math.sqrt(3) *
            state.mass
          ).toFixed(3) +
          " M"

        : "observer-dependent";

  }

  else if (
    structure ===
    "accretion-disk"
  ) {

    backendValue
      .textContent =
        "inner ≈ " +
        formatRadius(
          state.values
            .isco
        );

  }

  else {

    backendValue
      .textContent =
        formatRadius(
          value
        );

  }


  document
    .querySelectorAll(
      "[data-structure]"
    )
    .forEach(
      element => {

        element.classList
          .toggle(
            "selected",

            element.dataset
              .structure ===
            structure
          );

      }
    );


  document
    .querySelectorAll(
      ".structure-nav-button"
    )
    .forEach(
      button => {

        button.classList
          .toggle(
            "active",

            button.dataset
              .select ===
            structure
          );

      }
    );

}


/* =========================================================
   APPLY METRIC
   ========================================================= */

function applyMetric(
  metric
) {

  state.metric =
    metric;


  schwarzschildButton
    .classList
    .toggle(
      "active",

      metric ===
      "schwarzschild"
    );


  kerrButton
    .classList
    .toggle(
      "active",

      metric ===
      "kerr"
    );


  const isKerr =
    metric ===
    "kerr";


  ergosphereGroup
    .classList
    .toggle(
      "hidden",
      !isKerr
    );


  ergosphereLabel
    .classList
    .toggle(
      "hidden",
      !isKerr
    );


  rotationAxis
    .classList
    .toggle(
      "hidden",
      !isKerr
    );


  metricLabel
    .textContent =
      isKerr

      ? "Kerr geometry · a/M = " +
        state.spin.toFixed(2)

      : "Schwarzschild geometry";


  const ergosphereButton =
    document.querySelector(
      '[data-select="ergosphere"]'
    );


  ergosphereButton.disabled =
    !isKerr;


  if (
    isKerr
  ) {

    state.values =
      kerrValues(
        state.mass,
        state.spin
      );

  }

  else {

    state.values =
      schwarzschildValues(
        state.mass
      );

  }


  updateRadiusLabels();

  updateRightTheoryValues();

  updateDiagramGeometry();


  if (
    !isKerr &&
    state.selected ===
      "ergosphere"
  ) {

    state.selected =
      "event-horizon";

  }


  selectStructure(
    state.selected
  );


  loadBackendValues();

}


/* =========================================================
   BACKEND PHYSICS API
   ========================================================= */

async function loadBackendValues() {

  backendStatus
    .textContent =
      "checking backend";


  backendStatus
    .classList
    .remove(
      "connected"
    );


  const query =
    new URLSearchParams({

      mode:
        state.metric,

      mass:
        state.mass,

      spin:
        state.spin

    });


  try {

    const response =
      await fetch(
        "/api/black-hole-properties?" +
        query.toString()
      );


    if (
      !response.ok
    ) {

      throw new Error(
        "Backend unavailable"
      );

    }


    const result =
      await response.json();


    state.values = {

      event_horizon:
        result.event_horizon,

      photon_sphere:
        result.photon_sphere,

      isco:
        result.isco,

      ergosphere:
        result.ergosphere

    };


    backendStatus
      .textContent =
        "Flask backend";


    backendStatus
      .classList
      .add(
        "connected"
      );


    updateRadiusLabels();

    updateDiagramGeometry();

    selectStructure(
      state.selected
    );

  }

  catch (
    error
  ) {

    /*
      The page still works if Flask is not running.
    */

    backendStatus
      .textContent =
        "local formula";

  }

}


/* =========================================================
   CLICKABLE STRUCTURES
   ========================================================= */

document
  .querySelectorAll(
    "[data-structure]"
  )
  .forEach(
    element => {

      element.addEventListener(
        "click",

        () => {

          selectStructure(
            element.dataset
              .structure
          );

        }
      );

    }
  );


document
  .querySelectorAll(
    ".structure-nav-button"
  )
  .forEach(
    button => {

      button.addEventListener(
        "click",

        () => {

          selectStructure(
            button.dataset
              .select
          );

        }
      );

    }
  );


/* =========================================================
   METRIC BUTTONS
   ========================================================= */

schwarzschildButton
  .addEventListener(
    "click",

    () => {

      applyMetric(
        "schwarzschild"
      );

    }
  );


kerrButton
  .addEventListener(
    "click",

    () => {

      applyMetric(
        "kerr"
      );

    }
  );


/* =========================================================
   ZOOM
   ========================================================= */

function applyZoom() {

  const width =
    1000 /
    state.zoom;


  const height =
    720 /
    state.zoom;


  structureSvg
    .setAttribute(
      "viewBox",

      [
        -width / 2,
        -height / 2,
        width,
        height
      ].join(" ")
    );

}


document
  .getElementById(
    "zoomIn"
  )
  .addEventListener(
    "click",

    () => {

      state.zoom =
        Math.min(
          1.75,

          state.zoom +
          0.15
        );


      applyZoom();

    }
  );


document
  .getElementById(
    "zoomOut"
  )
  .addEventListener(
    "click",

    () => {

      state.zoom =
        Math.max(
          0.75,

          state.zoom -
          0.15
        );


      applyZoom();

    }
  );


document
  .getElementById(
    "resetStructure"
  )
  .addEventListener(
    "click",

    () => {

      state.zoom =
        1.0;


      applyZoom();


      selectStructure(
        "event-horizon"
      );

    }
  );


/* =========================================================
   INITIALISE PAGE
   ========================================================= */

applyMetric(
  "schwarzschild"
);


applyZoom();


/* =========================================================
   LANDSCAPE THEORY PAGE — CHAPTER NAVIGATION
   ========================================================= */

document
  .querySelectorAll(
    ".chapter-link"
  )
  .forEach(
    button => {

      button.addEventListener(
        "click",

        () => {

          const target =
            document.getElementById(
              button.dataset.target
            );


          if (!target) {
            return;
          }


          target.scrollIntoView({
            behavior: "smooth",
            block: "start"
          });


          document
            .querySelectorAll(
              ".chapter-link"
            )
            .forEach(
              item => {

                item.classList.remove(
                  "active"
                );

              }
            );


          button.classList.add(
            "active"
          );

        }
      );

    }
  );


/* =========================================================
   SWITCH TO KERR BUTTON
   ========================================================= */

const switchToKerrButton =
  document.getElementById(
    "switchToKerr"
  );


if (switchToKerrButton) {

  switchToKerrButton
    .addEventListener(
      "click",

      () => {

        applyMetric(
          "kerr"
        );


        const kerrSection =
          document.getElementById(
            "kerrSection"
          );


        if (kerrSection) {

          kerrSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
          });

        }

      }
    );

}


/* =========================================================
   MIRROR BACKEND RADII INTO RIGHT PANEL
   ========================================================= */

const rightPhotonValue =
  document.getElementById(
    "rightPhotonValue"
  );


const rightIscoValue =
  document.getElementById(
    "rightIscoValue"
  );


function updateRightTheoryValues() {

  if (
    rightPhotonValue &&
    state.values
  ) {

    rightPhotonValue.textContent =
      formatRadius(
        state.values
          .photon_sphere
      );

  }


  if (
    rightIscoValue &&
    state.values
  ) {

    rightIscoValue.textContent =
      formatRadius(
        state.values
          .isco
      );

  }

}


/*
  Run once after initialisation.
*/

updateRightTheoryValues();