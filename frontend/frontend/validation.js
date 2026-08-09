"use strict";


/* =========================================================
   PHOTON FORGE — VALIDATION DASHBOARD
   ========================================================= */


const statusCard =
  document.querySelector(
    ".validation-status-card"
  );


const statusText =
  document.getElementById(
    "validationStatus"
  );


/* =========================================================
   FORMATTERS
   ========================================================= */

function fixed(
  value,
  digits = 6
) {

  const n =
    Number(value);


  if (
    !Number.isFinite(n)
  ) {

    return "—";

  }


  return n.toFixed(
    digits
  );

}


function scientific(
  value
) {

  const n =
    Number(value);


  if (
    !Number.isFinite(n)
  ) {

    return "—";

  }


  if (
    Math.abs(n) <
    1e-12
  ) {

    return "0";

  }


  return n.toExponential(
    3
  );

}


/* =========================================================
   SVG HELPERS
   ========================================================= */

function svgElement(
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


function chartGrid(
  svg
) {

  for (
    let i = 0;
    i <= 5;
    i++
  ) {

    const x =
      50 +
      i *
      118;


    svg.appendChild(

      svgElement(
        "line",
        {

          x1: x,
          y1: 20,

          x2: x,
          y2: 220,

          class:
            "chart-grid-line"

        }
      )

    );

  }


  for (
    let i = 0;
    i <= 4;
    i++
  ) {

    const y =
      20 +
      i *
      50;


    svg.appendChild(

      svgElement(
        "line",
        {

          x1: 50,
          y1: y,

          x2: 640,
          y2: y,

          class:
            "chart-grid-line"

        }
      )

    );

  }


  svg.appendChild(

    svgElement(
      "line",
      {

        x1: 50,
        y1: 220,

        x2: 640,
        y2: 220,

        class:
          "chart-axis"

      }
    )

  );


  svg.appendChild(

    svgElement(
      "line",
      {

        x1: 50,
        y1: 20,

        x2: 50,
        y2: 220,

        class:
          "chart-axis"

      }
    )

  );

}


/* =========================================================
   TABLE
   ========================================================= */

function buildValidationTable(
  tests
) {

  const tbody =
    document.getElementById(
      "validationTableBody"
    );


  tbody.innerHTML =
    "";


  tests.forEach(
    test => {

      const row =
        document.createElement(
          "tr"
        );


      row.innerHTML =
        `

          <td>
            ${test.name}
          </td>

          <td>
            ${fixed(test.expected)}
            ${test.unit}
          </td>

          <td>
            ${fixed(test.measured)}
            ${test.unit}
          </td>

          <td>
            ${scientific(test.error)}
          </td>

          <td>

            <span
              class="${
                test.passed
                  ? "pass-badge"
                  : "fail-badge"
              }"
            >

              ${
                test.passed
                  ? "✓ PASS"
                  : "✕ FAIL"
              }

            </span>

          </td>

        `;


      tbody.appendChild(
        row
      );

    }
  );

}


/* =========================================================
   CAPTURE CHART
   ========================================================= */

function drawCaptureChart(
  curve,
  criticalB
) {

  const svg =
    document.getElementById(
      "captureChart"
    );


  svg.innerHTML =
    "";


  chartGrid(
    svg
  );


  const minB =
    4.0;


  const maxB =
    7.2;


  const xFromB =
    b =>

      50 +

      (
        (
          b -
          minB
        )

        /

        (
          maxB -
          minB
        )
      )

      *
      590;


  const capturedPoints =
    curve.map(
      point => {

        const x =
          xFromB(
            point.b
          );


        const y =
          point.captured
            ? 55
            : 205;


        return (
          x +
          "," +
          y
        );

      }
    )
    .join(
      " "
    );


  const escapedPoints =
    curve.map(
      point => {

        const x =
          xFromB(
            point.b
          );


        const y =
          point.escaped
            ? 55
            : 205;


        return (
          x +
          "," +
          y
        );

      }
    )
    .join(
      " "
    );


  svg.appendChild(

    svgElement(
      "polyline",
      {

        points:
          capturedPoints,

        class:
          "capture-line"

      }
    )

  );


  svg.appendChild(

    svgElement(
      "polyline",
      {

        points:
          escapedPoints,

        class:
          "escape-line"

      }
    )

  );


  const criticalX =
    xFromB(
      criticalB
    );


  svg.appendChild(

    svgElement(
      "line",
      {

        x1:
          criticalX,

        y1:
          20,

        x2:
          criticalX,

        y2:
          220,

        class:
          "critical-line"

      }
    )

  );


  const label =
    svgElement(
      "text",
      {

        x:
          criticalX + 6,

        y:
          34,

        class:
          "chart-label"

      }
    );


  label.textContent =
    "bc = 5.196M";


  svg.appendChild(
    label
  );


  const axisLabel =
    svgElement(
      "text",
      {

        x:
          530,

        y:
          252,

        class:
          "chart-label"

      }
    );


  axisLabel.textContent =
    "impact parameter b/M";


  svg.appendChild(
    axisLabel
  );

}


/* =========================================================
   DEFLECTION CHART
   ========================================================= */

function drawDeflectionChart(
  curve
) {

  const svg =
    document.getElementById(
      "deflectionChart"
    );


  svg.innerHTML =
    "";


  chartGrid(
    svg
  );


  const minB =
    Math.min(
      ...curve.map(
        p =>
          p.impact_parameter
      )
    );


  const maxB =
    Math.max(
      ...curve.map(
        p =>
          p.impact_parameter
      )
    );


  const maxAlpha =
    Math.max(
      ...curve.map(
        p =>
          p.alpha_rad
      )
    );


  const points =
    curve.map(
      point => {

        const x =

          50 +

          (
            (
              point.impact_parameter -
              minB
            )

            /

            (
              maxB -
              minB
            )
          )

          *
          590;


        const y =

          220 -

          (
            point.alpha_rad /
            maxAlpha
          )

          *
          180;


        return (
          x +
          "," +
          y
        );

      }
    )
    .join(
      " "
    );


  svg.appendChild(

    svgElement(
      "polyline",
      {

        points:
          points,

        class:
          "deflection-line"

      }
    )

  );


  const yLabel =
    svgElement(
      "text",
      {

        x: 8,
        y: 25,

        class:
          "chart-label"

      }
    );


  yLabel.textContent =
    "α (rad)";


  svg.appendChild(
    yLabel
  );


  const xLabel =
    svgElement(
      "text",
      {

        x: 535,
        y: 252,

        class:
          "chart-label"

      }
    );


  xLabel.textContent =
    "impact parameter b/M";


  svg.appendChild(
    xLabel
  );

}


/* =========================================================
   RK4 CONVERGENCE CHART
   ========================================================= */

function drawConvergenceChart(
  curve
) {

  const svg =
    document.getElementById(
      "convergenceChart"
    );


  svg.innerHTML =
    "";


  chartGrid(
    svg
  );


  const maxH =
    Math.max(
      ...curve.map(
        p =>
          p.step_size
      )
    );


  const maxError =
    Math.max(
      ...curve.map(
        p =>
          p.normalized_error
      )
    );


  const points =
    curve.map(
      point => {

        const x =

          50 +

          (
            1 -

            (
              point.step_size /
              maxH
            )
          )

          *
          590;


        const y =

          220 -

          (
            point.normalized_error /
            maxError
          )

          *
          180;


        return (
          x +
          "," +
          y
        );

      }
    )
    .join(
      " "
    );


  svg.appendChild(

    svgElement(
      "polyline",
      {

        points:
          points,

        class:
          "convergence-line"

      }
    )

  );


  curve.forEach(
    point => {

      const x =

        50 +

        (
          1 -

          (
            point.step_size /
            maxH
          )
        )

        *
        590;


      const y =

        220 -

        (
          point.normalized_error /
          maxError
        )

        *
        180;


      svg.appendChild(

        svgElement(
          "circle",
          {

            cx:
              x,

            cy:
              y,

            r:
              4,

            fill:
              "#8a70ff"

          }
        )

      );

    }
  );


  const yLabel =
    svgElement(
      "text",
      {

        x: 8,
        y: 25,

        class:
          "chart-label"

      }
    );


  yLabel.textContent =
    "relative error";


  svg.appendChild(
    yLabel
  );


  const xLabel =
    svgElement(
      "text",
      {

        x: 515,
        y: 252,

        class:
          "chart-label"

      }
    );


  xLabel.textContent =
    "decreasing step size →";


  svg.appendChild(
    xLabel
  );

}


/* =========================================================
   FETCH BACKEND
   ========================================================= */

async function loadValidation() {

  statusText.textContent =
    "Running benchmarks";


  statusCard.classList.remove(
    "connected"
  );


  try {

    const response =
      await fetch(
        "/api/validation-results"
      );


    if (
      !response.ok
    ) {

      throw new Error(
        "HTTP "
        +
        response.status
      );

    }


    const data =
      await response.json();


    if (
      data.status !==
      "ok"
    ) {

      throw new Error(
        data.message ||
        "Validation failed."
      );

    }


    /* -----------------------------------------------------
       SUMMARY
       ----------------------------------------------------- */

    document.getElementById(
      "totalTests"
    ).textContent =
      data.summary.tests;


    document.getElementById(
      "passedTests"
    ).textContent =
      data.summary.passed;


    document.getElementById(
      "failedTests"
    ).textContent =
      data.summary.failed;


    document.getElementById(
      "passRate"
    ).textContent =

      (
        data.summary
          .pass_fraction *
        100
      ).toFixed(0)

      +
      "%";


    /* -----------------------------------------------------
       RADII
       ----------------------------------------------------- */

    document.getElementById(
      "horizonValue"
    ).textContent =

      fixed(
        data.schwarzschild
          .event_horizon,
        3
      )

      +
      " M";


    document.getElementById(
      "photonValue"
    ).textContent =

      fixed(
        data.schwarzschild
          .photon_sphere,
        3
      )

      +
      " M";


    document.getElementById(
      "iscoValue"
    ).textContent =

      fixed(
        data.schwarzschild
          .isco,
        3
      )

      +
      " M";


    document.getElementById(
      "impactValue"
    ).textContent =

      fixed(
        data.schwarzschild
          .critical_impact_parameter,
        3
      )

      +
      " M";


    /* -----------------------------------------------------
       TABLE
       ----------------------------------------------------- */

    buildValidationTable(
      data.tests
    );


    /* -----------------------------------------------------
       KERR LIMIT
       ----------------------------------------------------- */

    document.getElementById(
      "kerrHorizon"
    ).textContent =

      fixed(
        data.kerr_limit
          .event_horizon,
        4
      )

      +
      " M";


    document.getElementById(
      "kerrPhoton"
    ).textContent =

      fixed(
        data.kerr_limit
          .photon_orbit,
        4
      )

      +
      " M";


    document.getElementById(
      "kerrIsco"
    ).textContent =

      fixed(
        data.kerr_limit
          .isco,
        4
      )

      +
      " M";


    const kerrPassed =

      Math.abs(
        data.kerr_limit
          .event_horizon -
        2
      ) < 1e-10

      &&

      Math.abs(
        data.kerr_limit
          .photon_orbit -
        3
      ) < 1e-10

      &&

      Math.abs(
        data.kerr_limit
          .isco -
        6
      ) < 1e-10;


    document.getElementById(
      "kerrLimitResult"
    ).textContent =

      kerrPassed

        ? "✓ Schwarzschild limit recovered"

        : "✕ Limit mismatch";


    /* -----------------------------------------------------
       CHARTS
       ----------------------------------------------------- */

    drawCaptureChart(

      data.capture_curve,

      data.schwarzschild
        .critical_impact_parameter

    );


    drawDeflectionChart(
      data.deflection_curve
    );


    drawConvergenceChart(
      data.convergence_curve
    );


    /* -----------------------------------------------------
       STATUS
       ----------------------------------------------------- */

    statusCard.classList.add(
      "connected"
    );


    statusText.textContent =

      data.summary.failed === 0

        ? "Benchmarks passed"

        : "Review required";


  }

  catch (
    error
  ) {

    console.error(
      "Validation dashboard error:",
      error
    );


    statusText.textContent =
      "Backend unavailable";


    statusCard.classList.remove(
      "connected"
    );

  }

}


/* =========================================================
   START
   ========================================================= */

loadValidation();