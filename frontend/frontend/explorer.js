"use strict";


/* =========================================================
   PHOTON FORGE — BLACK HOLE EXPLORER
   =========================================================

   IMPORTANT ARCHITECTURE

   A) TOP VIEW BUTTONS
      Render
      Thermal
      Geodesic Grid
      Data

      These control ONLY the large central display.

   B) LEFT OBJECT BUTTONS
      Sagittarius A*
      M87*
      Cygnus X-1
      NGC 1277
      TON 618

      These control ONLY:
      - object information
      - facts
      - optional object image/GIF/video

   The systems are deliberately independent.
   ========================================================= */


/* =========================================================
   CENTRAL SCIENTIFIC VIEWS
   ========================================================= */

const scientificViews = {

  render: {

    type:
      "RENDER VIEW",

    title:
      "Relativistic Appearance",

    mediaType:
      "video",

    source:
      "assets/explorer/views/render-view.mp4"

  },


  thermal: {

    type:
      "THERMAL VIEW",

    title:
      "Accretion Temperature",

    mediaType:
      "image",

    source:
      "assets/explorer/views/thermal-view.png"

  },


  geodesic: {

    type:
      "GEODESIC GRID",

    title:
      "Spacetime Geometry",

    mediaType:
      "image",

    source:
      "assets/explorer/views/geodesic-grid.gif"

  }

};


/* =========================================================
   CENTRAL VIEW ELEMENTS
   ========================================================= */

const visualView =
  document.getElementById(
    "visualView"
  );


const dataView =
  document.getElementById(
    "dataView"
  );

  const mainViewVideo =
  document.getElementById(
    "mainViewVideo"
  );

const mainViewImage =
  document.getElementById(
    "mainViewImage"
  );


const viewType =
  document.getElementById(
    "viewType"
  );


const viewTitle =
  document.getElementById(
    "viewTitle"
  );


/* =========================================================
   SWITCH CENTRAL VIEW
   ========================================================= */

function setView(viewName) {

  /* -----------------------------------------
     ACTIVE TAB
     ----------------------------------------- */

  document
    .querySelectorAll(".view-tab")
    .forEach(button => {

      button.classList.toggle(
        "active",
        button.dataset.view === viewName
      );

    });


  /* =========================================
     DATA VIEW
     ========================================= */

  if (viewName === "data") {

    visualView.classList.add(
      "hidden"
    );

    dataView.classList.remove(
      "hidden"
    );


    /*
      Stop render video while Data View
      is being inspected.
    */

    mainViewVideo.pause();


    loadPhysicsData();

    return;
  }


  /* =========================================
     VISUAL VIEWS
     ========================================= */

  const selected =
    scientificViews[viewName];


  if (!selected) {
    return;
  }


  dataView.classList.add(
    "hidden"
  );

  visualView.classList.remove(
    "hidden"
  );


  /* =========================================
     VIDEO
     ========================================= */

  if (selected.mediaType === "video") {

    mainViewImage.classList.add(
      "hidden"
    );

    mainViewVideo.classList.remove(
      "hidden"
    );


    /*
      Only change source if necessary.
    */

    if (
      !mainViewVideo.src.endsWith(
        selected.source
      )
    ) {

      mainViewVideo.src =
        selected.source;

      mainViewVideo.load();

    }


    mainViewVideo
      .play()
      .catch(() => {
        /*
          Browser autoplay restrictions are
          harmless because the video is muted.
        */
      });

  }


  /* =========================================
     IMAGE / GIF
     ========================================= */

  else {

    /*
      Stop GPU/video decoding when not needed.
    */

    mainViewVideo.pause();


    mainViewVideo.classList.add(
      "hidden"
    );

    mainViewImage.classList.remove(
      "hidden"
    );


    mainViewImage.src =
      selected.source;

  }


  /* =========================================
     CAPTION
     ========================================= */

  viewType.textContent =
    selected.type;


  viewTitle.textContent =
    selected.title;

}


/* =========================================================
   VIEW BUTTON EVENTS
   ========================================================= */

document
  .querySelectorAll(
    ".view-tab"
  )
  .forEach(
    button => {

      button.addEventListener(
        "click",

        () => {

          setView(
            button.dataset.view
          );

        }
      );

    }
  );


/* =========================================================
   REAL BLACK-HOLE CATALOGUE
   =========================================================

   IMPORTANT:

   media is currently null because you said you only
   have the main scientific-view media right now.

   Later, when we add a Sagittarius image, for example:

   mediaType: "image",
   media: "assets/explorer/objects/sagittarius-a.jpg"

   No other code needs to change.
   ========================================================= */

const blackHoles = {

  sagittarius: {

    name:
      "Sagittarius A*",

    type:
      "Supermassive black hole",

    mass:
      "≈ 4.3 × 10⁶ M☉",

    distance:
      "≈ 26,700 ly",

    host:
      "Milky Way",

    mediaType:
      "image",

    media:
      "assets/explorer/objects/sag_a.jpg",

    facts: [

      "Located at the dynamical centre of the Milky Way.",

      "Its mass is constrained by monitoring stars orbiting the Galactic Centre.",

      "Its surrounding emission was imaged by the Event Horizon Telescope."

    ]

  },


  m87: {

    name:
      "M87*",

    type:
      "Supermassive black hole",

    mass:
      "≈ 6.5 × 10⁹ M☉",

    distance:
      "≈ 53 million ly",

    host:
      "Messier 87",

    mediaType:
      "image",

    media:
      "assets/explorer/objects/m87.jpg",

    facts: [

      "M87* lies at the centre of the giant elliptical galaxy Messier 87.",

      "It became the first black hole whose surrounding emission was imaged by the Event Horizon Telescope.",

      "Its host galaxy contains a prominent relativistic jet."

    ]

  },


  cygnus: {

    name:
      "Cygnus X-1",

    type:
      "Stellar-mass black hole",

    mass:
      "≈ 21 M☉",

    distance:
      "≈ 7,200 ly",

    host:
      "Milky Way",

    mediaType:
      "image",

    media:
      "assets/explorer/objects/cygnus_x1.jpg",

    facts: [

      "Cygnus X-1 is one of the best-known stellar-mass black-hole systems.",

      "It forms an X-ray binary with a massive companion star.",

      "Gas transferred from the companion forms a hot accretion flow and produces strong X-ray emission."

    ]

  },


  ngc1277: {

    name:
      "NGC 1277",

    type:
      "Supermassive black hole",

    mass:
      "≈ several × 10⁹ M☉",

    distance:
      "≈ 220 million ly",

    host:
      "NGC 1277",

    mediaType:
      "image",

    media:
      "assets/explorer/objects/ngc_1277.jpg",

    facts: [

      "NGC 1277 is a compact lenticular galaxy associated with the Perseus region.",

      "Its central black-hole mass has been investigated through stellar-dynamical observations.",

      "The galaxy is notable for hosting an unusually massive central black hole relative to its compact size."

    ]

  },


  ton618: {

    name:
      "TON 618",

    type:
      "Ultramassive black hole",

    mass:
      "≈ 4 × 10¹⁰ M☉",

    distance:
      "Cosmological",

    host:
      "TON 618 quasar",

    mediaType:
      "image",

    media:
      "assets/explorer/objects/ton_618.jpg",

    facts: [

      "TON 618 is an extremely luminous distant quasar.",

      "Its central black hole is among the most massive known black holes by commonly cited estimates.",

      "Its enormous luminosity is produced by matter accreting onto the central black hole."

    ]

  }

};

/* =========================================================
   OBJECT INFORMATION ELEMENTS
   ========================================================= */

const objectName =
  document.getElementById(
    "objectName"
  );


const objectType =
  document.getElementById(
    "objectType"
  );


const objectMass =
  document.getElementById(
    "objectMass"
  );


const objectDistance =
  document.getElementById(
    "objectDistance"
  );


const objectHost =
  document.getElementById(
    "objectHost"
  );


const objectFacts =
  document.getElementById(
    "objectFacts"
  );


const objectMediaHost =
  document.getElementById(
    "objectMediaHost"
  );


/* =========================================================
   SHOW OBJECT MEDIA
   ========================================================= */

function showObjectMedia(
  object
) {

  objectMediaHost.innerHTML =
    "";


  /*
    No media yet.

    This makes the page work immediately without requiring
    five real-black-hole image files.
  */

  if (
    !object.media ||
    !object.mediaType
  ) {

    const placeholder =
      document.createElement(
        "div"
      );


    placeholder.className =
      "object-empty";


    placeholder.innerHTML =
      `
        <div>
          <strong>${object.name}</strong>
          <br><br>
          Object media can be added here later.
        </div>
      `;


    objectMediaHost.appendChild(
      placeholder
    );


    return;

  }


  /* -------------------------------------------------------
     VIDEO
     ------------------------------------------------------- */

  if (
    object.mediaType ===
    "video"
  ) {

    const video =
      document.createElement(
        "video"
      );


    video.src =
      object.media;


    video.autoplay =
      true;


    video.muted =
      true;


    video.loop =
      true;


    video.playsInline =
      true;


    video.preload =
      "metadata";


    objectMediaHost.appendChild(
      video
    );


    return;

  }


  /* -------------------------------------------------------
     IMAGE OR GIF

     GIF uses the same <img> element and animates
     automatically.
     ------------------------------------------------------- */

  const image =
    document.createElement(
      "img"
    );


  image.src =
    object.media;


  image.alt =
    object.name;


  objectMediaHost.appendChild(
    image
  );

}


/* =========================================================
   SELECT REAL BLACK HOLE
   ========================================================= */

function selectObject(objectKey) {

  const object =
    blackHoles[objectKey];

  if (!object) {
    return;
  }


  /* ===============================
     RIGHT-SIDE DATA
     =============================== */

  objectName.textContent =
    object.name;

  objectType.textContent =
    object.type;

  objectMass.textContent =
    object.mass;

  objectDistance.textContent =
    object.distance;

  objectHost.textContent =
    object.host;


  objectFacts.innerHTML = "";

  object.facts.forEach(fact => {

    const li =
      document.createElement("li");

    li.textContent =
      fact;

    objectFacts.appendChild(li);

  });


  /* ===============================
     ACTIVE LEFT BUTTON
     =============================== */

  document
    .querySelectorAll(".object-button")
    .forEach(button => {

      button.classList.toggle(
        "active",
        button.dataset.object === objectKey
      );

    });


  /* ===============================
     SHOW OBJECT IN MAIN MIDDLE BOX
     =============================== */

  dataView.classList.add("hidden");

  visualView.classList.remove("hidden");


  /* stop render video */

  if (mainViewVideo) {

    mainViewVideo.pause();

    mainViewVideo.classList.add("hidden");

  }


  /* show image element */

  mainViewImage.classList.remove("hidden");


  /* THIS is the important part */

  mainViewImage.src =
    object.media;

  mainViewImage.alt =
    object.name;


  viewType.textContent =
    "BLACK HOLE OBJECT";

  viewTitle.textContent =
    object.name;


  /* remove active state from top view tabs */

  document
    .querySelectorAll(".view-tab")
    .forEach(button => {

      button.classList.remove("active");

    });

}


/* =========================================================
   OBJECT BUTTON EVENTS
   ========================================================= */

document
  .querySelectorAll(
    ".object-button"
  )
  .forEach(
    button => {

      button.addEventListener(
        "click",

        () => {

          selectObject(
            button.dataset.object
          );

        }
      );

    }
  );


/* =========================================================
   BACKEND DATA VIEW
   ========================================================= */

const backendStatus =
  document.getElementById(
    "backendStatus"
  );


const backendDot =
  document.getElementById(
    "backendDot"
  );


const backendStatusContainer =
  document.querySelector(
    ".backend-status"
  );


/* =========================================================
   NUMBER FORMATTERS
   ========================================================= */

function formatScientific(
  value,
  decimals = 3
) {

  const number =
    Number(
      value
    );


  if (
    !Number.isFinite(
      number
    )
  ) {

    return "—";

  }


  return number.toExponential(
    decimals
  );

}


function formatM(
  value
) {

  const number =
    Number(
      value
    );


  if (
    !Number.isFinite(
      number
    )
  ) {

    return "—";

  }


  return (
    number.toFixed(4)
    +
    " M"
  );

}


function formatKm(
  value
) {

  return (
    formatScientific(
      value,
      3
    )
    +
    " km"
  );

}


/* =========================================================
   LOAD PHYSICS DATA FROM FLASK
   ========================================================= */

async function loadPhysicsData() {

  const mass =
    document.getElementById(
      "dataMass"
    ).value;


  const spin =
    document.getElementById(
      "dataSpin"
    ).value;


  const observer =
    document.getElementById(
      "dataObserver"
    ).value;


  const inclination =
    document.getElementById(
      "dataInclination"
    ).value;


  backendStatus.textContent =
    "Calculating";


  backendStatusContainer.classList.remove(
    "connected"
  );


  const parameters =
    new URLSearchParams({

      mass_solar:
        mass,

      spin:
        spin,

      observer_radius:
        observer,

      inclination:
        inclination

    });


  try {

    const response =
      await fetch(
        "/api/explorer-data?" +
        parameters.toString()
      );


    if (
      !response.ok
    ) {

      throw new Error(
        "Backend returned HTTP "
        +
        response.status
      );

    }


    const result =
      await response.json();


    if (
      result.status !==
      "ok"
    ) {

      throw new Error(
        result.message ||
        "Physics calculation failed."
      );

    }


    /* =====================================================
       TOP SUMMARY
       ===================================================== */

    document.getElementById(
      "valueRg"
    ).textContent =
      formatKm(
        result.scales
          .gravitational_radius_km
      );


    document.getElementById(
      "valueHorizon"
    ).textContent =
      formatM(
        result.radii_M
          .outer_horizon
      );


    document.getElementById(
      "valuePhoton"
    ).textContent =
      formatM(
        result.radii_M
          .photon_prograde
      );


    document.getElementById(
      "valueIsco"
    ).textContent =
      formatM(
        result.radii_M
          .isco_prograde
      );


    /* =====================================================
       CHARACTERISTIC RADII
       ===================================================== */

    document.getElementById(
      "outerHorizon"
    ).textContent =
      formatM(
        result.radii_M
          .outer_horizon
      );


    document.getElementById(
      "innerHorizon"
    ).textContent =
      formatM(
        result.radii_M
          .inner_horizon
      );


    document.getElementById(
      "ergosphereRadius"
    ).textContent =
      formatM(
        result.radii_M
          .ergosphere_equator
      );


    document.getElementById(
      "photonPrograde"
    ).textContent =
      formatM(
        result.radii_M
          .photon_prograde
      );


    document.getElementById(
      "photonRetrograde"
    ).textContent =
      formatM(
        result.radii_M
          .photon_retrograde
      );


    document.getElementById(
      "iscoPrograde"
    ).textContent =
      formatM(
        result.radii_M
          .isco_prograde
      );


    document.getElementById(
      "iscoRetrograde"
    ).textContent =
      formatM(
        result.radii_M
          .isco_retrograde
      );


    /* =====================================================
       PHYSICAL QUANTITIES
       ===================================================== */

    document.getElementById(
      "gravTime"
    ).textContent =

      formatScientific(
        result.scales
          .gravitational_time_s
      )
      +
      " s";


    document.getElementById(
      "horizonArea"
    ).textContent =

      formatScientific(
        result.physical
          .horizon_area_km2
      )
      +
      " km²";


    document.getElementById(
      "horizonOmega"
    ).textContent =

      formatScientific(
        result.physical
          .horizon_angular_velocity_rad_s
      )
      +
      " rad/s";


    document.getElementById(
      "hawkingTemperature"
    ).textContent =

      formatScientific(
        result.physical
          .hawking_temperature_K
      )
      +
      " K";


    document.getElementById(
      "iscoFrequency"
    ).textContent =

      formatScientific(
        result.physical
          .isco_frequency_Hz
      )
      +
      " Hz";


    /* =====================================================
       CHARTS
       ===================================================== */

    drawSpinChart(
      result.spin_curve
    );


    drawFrequencyChart(
      result.orbit_curve
    );


    backendStatus.textContent =
      "Flask backend · live";


    backendStatusContainer.classList.add(
      "connected"
    );

  }

  catch (
    error
  ) {

    console.error(
      "Explorer backend error:",
      error
    );


    backendStatus.textContent =
      "Backend error";


    backendStatusContainer.classList.remove(
      "connected"
    );

  }

}


/* =========================================================
   SVG HELPERS
   ========================================================= */

function makeSvgElement(
  tag,
  attributes = {}
) {

  const element =
    document.createElementNS(
      "http://www.w3.org/2000/svg",
      tag
    );


  Object.entries(
    attributes
  )
  .forEach(
    ([key, value]) => {

      element.setAttribute(
        key,
        value
      );

    }
  );


  return element;

}


/* =========================================================
   CHART GRID
   ========================================================= */

function drawChartGrid(
  svg
) {

  /*
    Vertical grid lines.
  */

  for (
    let index = 0;
    index <= 5;
    index++
  ) {

    const x =
      45 +
      index *
      100;


    svg.appendChild(

      makeSvgElement(
        "line",

        {

          x1: x,
          y1: 15,

          x2: x,
          y2: 185,

          class:
            "chart-grid"

        }

      )

    );

  }


  /*
    Horizontal grid lines.
  */

  for (
    let index = 0;
    index <= 4;
    index++
  ) {

    const y =
      15 +
      index *
      42.5;


    svg.appendChild(

      makeSvgElement(
        "line",

        {

          x1: 45,
          y1: y,

          x2: 555,
          y2: y,

          class:
            "chart-grid"

        }

      )

    );

  }


  /* x axis */

  svg.appendChild(

    makeSvgElement(
      "line",

      {

        x1: 45,
        y1: 185,

        x2: 555,
        y2: 185,

        class:
          "chart-axis"

      }

    )

  );


  /* y axis */

  svg.appendChild(

    makeSvgElement(
      "line",

      {

        x1: 45,
        y1: 15,

        x2: 45,
        y2: 185,

        class:
          "chart-axis"

      }

    )

  );

}


/* =========================================================
   RADII VS SPIN CHART
   ========================================================= */

function drawSpinChart(
  data
) {

  const svg =
    document.getElementById(
      "spinChart"
    );


  svg.innerHTML =
    "";


  if (
    !Array.isArray(
      data
    ) ||
    data.length === 0
  ) {

    return;

  }


  drawChartGrid(
    svg
  );


  /*
    Schwarzschild ISCO begins at 6M,
    so use slightly above 6 for vertical range.
  */

  const maxRadius =
    6.5;


  function createPoints(
    property
  ) {

    return data
      .map(
        item => {

          const x =

            45 +

            (
              Number(
                item.spin
              )

              /
              0.998
            )

            *
            510;


          const y =

            185 -

            (
              Number(
                item[property]
              )

              /
              maxRadius
            )

            *
            160;


          return (
            x.toFixed(2)
            +
            ","
            +
            y.toFixed(2)
          );

        }
      )

      .join(
        " "
      );

  }


  /* Event horizon */

  svg.appendChild(

    makeSvgElement(
      "polyline",

      {

        points:
          createPoints(
            "horizon"
          ),

        class:
          "chart-horizon"

      }

    )

  );


  /* Prograde photon orbit */

  svg.appendChild(

    makeSvgElement(
      "polyline",

      {

        points:
          createPoints(
            "photon"
          ),

        class:
          "chart-photon"

      }

    )

  );


  /* Prograde ISCO */

  svg.appendChild(

    makeSvgElement(
      "polyline",

      {

        points:
          createPoints(
            "isco"
          ),

        class:
          "chart-isco"

      }

    )

  );


  /* -------------------------------------------------------
     Labels
     ------------------------------------------------------- */

  const labelSpin =
    makeSvgElement(
      "text",

      {

        x: 510,
        y: 210,

        fill:
          "#687384",

        "font-size":
          "10"

      }
    );


  labelSpin.textContent =
    "spin χ";


  svg.appendChild(
    labelSpin
  );


  const labelRadius =
    makeSvgElement(
      "text",

      {

        x: 8,
        y: 18,

        fill:
          "#687384",

        "font-size":
          "10"

      }
    );


  labelRadius.textContent =
    "r / M";


  svg.appendChild(
    labelRadius
  );

}


/* =========================================================
   ORBITAL FREQUENCY VS RADIUS
   ========================================================= */

function drawFrequencyChart(
  data
) {

  const svg =
    document.getElementById(
      "frequencyChart"
    );


  svg.innerHTML =
    "";


  if (
    !Array.isArray(
      data
    ) ||
    data.length === 0
  ) {

    return;

  }


  drawChartGrid(
    svg
  );


  const radiusMinimum =
    Number(
      data[0].radius
    );


  const radiusMaximum =
    Number(
      data[
        data.length - 1
      ].radius
    );


  const omegaMaximum =
    Math.max(
      ...data.map(
        item =>
          Number(
            item.omega_M
          )
      )
    );


  const points =
    data

      .map(
        item => {

          const radius =
            Number(
              item.radius
            );


          const omega =
            Number(
              item.omega_M
            );


          const x =

            45 +

            (
              (
                radius -
                radiusMinimum
              )

              /

              (
                radiusMaximum -
                radiusMinimum
              )
            )

            *
            510;


          const y =

            185 -

            (
              omega /
              omegaMaximum
            )

            *
            160;


          return (
            x.toFixed(2)
            +
            ","
            +
            y.toFixed(2)
          );

        }
      )

      .join(
        " "
      );


  svg.appendChild(

    makeSvgElement(
      "polyline",

      {

        points:
          points,

        class:
          "chart-frequency"

      }

    )

  );


  /* labels */

  const labelRadius =
    makeSvgElement(
      "text",

      {

        x: 492,
        y: 210,

        fill:
          "#687384",

        "font-size":
          "10"

      }
    );


  labelRadius.textContent =
    "radius r / M";


  svg.appendChild(
    labelRadius
  );


  const labelOmega =
    makeSvgElement(
      "text",

      {

        x: 8,
        y: 18,

        fill:
          "#687384",

        "font-size":
          "10"

      }
    );


  labelOmega.textContent =
    "MΩ";


  svg.appendChild(
    labelOmega
  );

}


/* =========================================================
   MANUAL RECALCULATION
   ========================================================= */

const calculateDataButton =
  document.getElementById(
    "calculateData"
  );


calculateDataButton
  .addEventListener(
    "click",

    loadPhysicsData
  );


/* =========================================================
   ALLOW ENTER IN DATA INPUTS
   ========================================================= */

document
  .querySelectorAll(
    ".data-controls input"
  )
  .forEach(
    input => {

      input.addEventListener(
        "keydown",

        event => {

          if (
            event.key ===
            "Enter"
          ) {

            loadPhysicsData();

          }

        }
      );

    }
  );


/* =========================================================
   INITIALISE PAGE
   ========================================================= */

/*
   Default central scientific view.
*/

setView(
  "render"
);


/*
   Default real black hole.

   This does not affect the Render View.
*/

selectObject(
  "sagittarius"
);