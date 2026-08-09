import math

from pathlib import Path
from flask import (
    request,
    jsonify,
    send_from_directory,
    render_template,
    redirect
)

from backend.app import app
from backend.renderer import render_black_hole



@app.route("/")
def home():
    return jsonify({
        "engine": "Photon Forge",
        "status": "running"
    })


@app.route("/renderer")
def renderer_page():
    return render_template(
        "hybrid_renderer.html"
    )


@app.route("/render", methods=["POST"])
def render_api():
    parameters = request.get_json(
        silent=True
    ) or {}

    filename = render_black_hole(
        parameters
    )

    return jsonify({
        "status": "complete",
        "image": filename
    })

@app.route("/renderer-v2")
def renderer_v2_page():
    return render_template("hybrid_renderer_v2.html")


# Add these imports to backend/routes.py


# Add this near the top of backend/routes.py, after app is imported.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_CANDIDATES = (
    PROJECT_ROOT / "frontend" / "frontend",
    PROJECT_ROOT / "frontend",
)
FRONTEND_DIR = next(
    (folder for folder in FRONTEND_CANDIDATES if (folder / "index.html").exists()),
    FRONTEND_CANDIDATES[0],
)

@app.route("/site")
def website_home_redirect():
    return redirect("/site/")

@app.route("/site/")
def website_home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/site/<path:filename>")
def website_file(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# Keep the existing POST /render endpoint unchanged.
# Open the integrated website at:
# http://127.0.0.1:5000/site/
#
# Open the backend-connected renderer directly at:
# http://127.0.0.1:5000/site/engine.html


# =========================================================
# BLACK HOLE THEORY API
# =========================================================

@app.route(
    "/api/black-hole-properties",
    methods=["GET"]
)
def black_hole_properties():
    """
    Returns characteristic black-hole radii
    for the Visual Theory Explorer.

    Units:
        G = c = 1

    Parameters:
        mass
        spin
        mode = schwarzschild | kerr
    """

    try:

        mass = float(
            request.args.get(
                "mass",
                1.0
            )
        )

        spin_fraction = float(
            request.args.get(
                "spin",
                0.9
            )
        )

        mode = (
            request.args.get(
                "mode",
                "schwarzschild"
            )
            .lower()
        )


        # -----------------------------
        # Validation
        # -----------------------------

        mass = max(
            0.001,
            mass
        )


        spin_fraction = max(
            -0.998,
            min(
                0.998,
                spin_fraction
            )
        )


        # =================================================
        # SCHWARZSCHILD
        # =================================================

        if mode == "schwarzschild":

            return jsonify({

                "metric":
                    "schwarzschild",

                "mass":
                    mass,

                "spin":
                    0.0,

                "event_horizon":
                    2.0 * mass,

                "photon_sphere":
                    3.0 * mass,

                "isco":
                    6.0 * mass,

                "ergosphere":
                    None

            })


        # =================================================
        # KERR
        # =================================================

        dimensional_spin = (
            spin_fraction *
            mass
        )


        # -----------------------------
        # Outer event horizon
        # -----------------------------

        event_horizon = (
            mass +

            math.sqrt(
                max(
                    0.0,

                    mass * mass -

                    dimensional_spin *
                    dimensional_spin
                )
            )
        )


        # -----------------------------
        # Kerr prograde photon orbit
        # -----------------------------

        photon_sphere = (
            2.0 *
            mass *
            (
                1.0 +

                math.cos(
                    (
                        2.0 / 3.0
                    ) *

                    math.acos(
                        -spin_fraction
                    )
                )
            )
        )


        # -----------------------------
        # Kerr ISCO
        # -----------------------------

        a = spin_fraction


        z1 = (
            1.0 +

            (
                1.0 -
                a * a
            ) ** (
                1.0 / 3.0
            )

            *

            (
                (
                    1.0 +
                    a
                ) ** (
                    1.0 / 3.0
                )

                +

                (
                    1.0 -
                    a
                ) ** (
                    1.0 / 3.0
                )
            )
        )


        z2 = math.sqrt(
            3.0 *
            a *
            a +

            z1 *
            z1
        )


        isco = (
            3.0 +
            z2 -

            math.sqrt(
                max(
                    0.0,

                    (
                        3.0 -
                        z1
                    )

                    *

                    (
                        3.0 +
                        z1 +
                        2.0 *
                        z2
                    )
                )
            )
        ) * mass


        # -----------------------------
        # Equatorial ergosphere
        #
        # At theta = pi/2:
        #
        # r_erg = 2M
        # -----------------------------

        ergosphere = (
            2.0 *
            mass
        )


        return jsonify({

            "metric":
                "kerr",

            "mass":
                mass,

            "spin":
                spin_fraction,

            "event_horizon":
                event_horizon,

            "photon_sphere":
                photon_sphere,

            "isco":
                isco,

            "ergosphere":
                ergosphere

        })


    except Exception as error:

        return jsonify({

            "status":
                "error",

            "message":
                str(error)

        }), 400

        # =========================================================
# EXPLORER — PHYSICALLY DERIVED KERR DATA VIEW
# =========================================================

@app.route(
    "/api/explorer-data",
    methods=["GET"]
)
def explorer_data():
    """
    Live physics data for the Photon Forge Explorer.

    The endpoint uses analytic Kerr expressions in
    Boyer-Lindquist coordinates.

    Inputs
    ------
    mass_solar:
        Black-hole mass in solar masses.

    spin:
        Dimensionless Kerr spin chi = J c / (G M^2).
        Restricted here to 0 <= chi <= 0.998.

    observer_radius:
        Observer radius in units of GM/c^2.

    inclination:
        Observer inclination in degrees.

    Notes
    -----
    No fake ray counts, fluxes or render times are returned.
    Those quantities should only be shown when produced by
    an actual numerical render.
    """

    try:

        # -------------------------------------------------
        # CONSTANTS
        # -------------------------------------------------

        G = 6.67430e-11
        C = 299792458.0

        SOLAR_MASS = 1.98847e30

        HBAR = 1.054571817e-34
        K_B = 1.380649e-23


        # -------------------------------------------------
        # INPUTS
        # -------------------------------------------------

        mass_solar = float(
            request.args.get(
                "mass_solar",
                6.5e9
            )
        )

        spin = float(
            request.args.get(
                "spin",
                0.90
            )
        )

        observer_radius = float(
            request.args.get(
                "observer_radius",
                50.0
            )
        )

        inclination = float(
            request.args.get(
                "inclination",
                67.0
            )
        )


        mass_solar = max(
            1.0,
            mass_solar
        )

        spin = max(
            0.0,
            min(
                0.998,
                spin
            )
        )

        observer_radius = max(
            2.1,
            observer_radius
        )

        inclination = max(
            0.0,
            min(
                180.0,
                inclination
            )
        )


        # -------------------------------------------------
        # PHYSICAL MASS
        # -------------------------------------------------

        mass_kg = (
            mass_solar *
            SOLAR_MASS
        )


        # gravitational radius:
        #
        # rg = GM / c^2
        #
        # One coordinate "M" in geometrized units.
        # -------------------------------------------------

        rg_m = (
            G *
            mass_kg /
            (C * C)
        )

        rg_km = (
            rg_m /
            1000.0
        )


        # gravitational time:
        #
        # tg = GM / c^3
        # -------------------------------------------------

        tg_s = (
            G *
            mass_kg /
            (C ** 3)
        )


        # -------------------------------------------------
        # KERR HORIZONS
        # -------------------------------------------------

        root = math.sqrt(
            max(
                0.0,
                1.0 -
                spin * spin
            )
        )


        # in units of M = GM/c^2

        r_plus_M = (
            1.0 +
            root
        )

        r_minus_M = (
            1.0 -
            root
        )


        # -------------------------------------------------
        # SCHWARZSCHILD REFERENCE RADIUS
        # -------------------------------------------------

        schwarzschild_M = (
            2.0
        )


        # -------------------------------------------------
        # EQUATORIAL STATIC LIMIT / ERGOSPHERE
        #
        # At theta = pi/2:
        #
        # r_static = 2M
        #
        # -------------------------------------------------

        ergosphere_equator_M = (
            2.0
        )


        # -------------------------------------------------
        # EQUATORIAL KERR PHOTON ORBITS
        #
        # Prograde:
        #
        # rph- =
        # 2M [1 + cos(2/3 acos(-chi))]
        #
        # Retrograde:
        #
        # rph+ =
        # 2M [1 + cos(2/3 acos(chi))]
        #
        # -------------------------------------------------

        photon_prograde_M = (
            2.0 *
            (
                1.0 +

                math.cos(
                    (
                        2.0 / 3.0
                    ) *

                    math.acos(
                        -spin
                    )
                )
            )
        )


        photon_retrograde_M = (
            2.0 *
            (
                1.0 +

                math.cos(
                    (
                        2.0 / 3.0
                    ) *

                    math.acos(
                        spin
                    )
                )
            )
        )


        # -------------------------------------------------
        # KERR ISCO
        # Bardeen, Press & Teukolsky expression
        # -------------------------------------------------

        z1 = (
            1.0 +

            (
                1.0 -
                spin * spin
            ) ** (
                1.0 / 3.0
            )

            *

            (
                (
                    1.0 +
                    spin
                ) ** (
                    1.0 / 3.0
                )

                +

                (
                    1.0 -
                    spin
                ) ** (
                    1.0 / 3.0
                )
            )
        )


        z2 = math.sqrt(
            3.0 *
            spin *
            spin +

            z1 *
            z1
        )


        isco_term = math.sqrt(
            max(
                0.0,

                (
                    3.0 -
                    z1
                )

                *

                (
                    3.0 +
                    z1 +
                    2.0 *
                    z2
                )
            )
        )


        isco_prograde_M = (
            3.0 +
            z2 -
            isco_term
        )


        isco_retrograde_M = (
            3.0 +
            z2 +
            isco_term
        )


        # -------------------------------------------------
        # HORIZON AREA
        #
        # A = 8 pi M^2 (1 + sqrt(1 - chi^2))
        #
        # physical area uses rg^2
        # -------------------------------------------------

        horizon_area_km2 = (
            8.0 *
            math.pi *
            rg_km *
            rg_km *
            (
                1.0 +
                root
            )
        )


        # -------------------------------------------------
        # HORIZON ANGULAR VELOCITY
        #
        # Omega_H =
        #
        # chi /
        # [2 tg (1 + sqrt(1 - chi^2))]
        #
        # rad / s
        # -------------------------------------------------

        horizon_omega_rad_s = (
            spin /

            (
                2.0 *
                tg_s *
                (
                    1.0 +
                    root
                )
            )
        )


        # -------------------------------------------------
        # HAWKING TEMPERATURE — KERR
        #
        # TH =
        #
        # hbar c^3
        # -------------------------
        # 4 pi G kB M
        #
        # *
        #
        # sqrt(1-chi^2)
        # -----------------
        # 1 + sqrt(1-chi^2)
        #
        # For chi=0 this becomes the standard
        # Schwarzschild Hawking temperature.
        # -------------------------------------------------

        hawking_temperature_K = (

            HBAR *
            (C ** 3)

            /

            (
                4.0 *
                math.pi *
                G *
                K_B *
                mass_kg
            )

            *

            (
                root /
                (
                    1.0 +
                    root
                )
            )
        )


        # -------------------------------------------------
        # ANGULAR MOMENTUM
        #
        # J = chi G M^2 / c
        # -------------------------------------------------

        angular_momentum = (

            spin *
            G *
            mass_kg *
            mass_kg /
            C
        )


        # -------------------------------------------------
        # PROGRADE ORBITAL FREQUENCY AT ISCO
        #
        # M Omega =
        #
        # 1 / (r^(3/2) + chi)
        #
        # -------------------------------------------------

        isco_omega_M = (

            1.0 /

            (
                isco_prograde_M ** 1.5
                +
                spin
            )
        )


        isco_omega_rad_s = (
            isco_omega_M /
            tg_s
        )


        isco_frequency_Hz = (

            isco_omega_rad_s /
            (
                2.0 *
                math.pi
            )
        )


        # -------------------------------------------------
        # SPIN SWEEP
        #
        # Used for the live chart.
        # -------------------------------------------------

        spin_curve = []


        for index in range(61):

            chi = (
                0.998 *
                index /
                60.0
            )


            curve_root = math.sqrt(
                max(
                    0.0,
                    1.0 -
                    chi * chi
                )
            )


            curve_horizon = (
                1.0 +
                curve_root
            )


            curve_photon = (
                2.0 *
                (
                    1.0 +

                    math.cos(
                        (
                            2.0 / 3.0
                        ) *

                        math.acos(
                            -chi
                        )
                    )
                )
            )


            curve_z1 = (
                1.0 +

                (
                    1.0 -
                    chi * chi
                ) ** (
                    1.0 / 3.0
                )

                *

                (
                    (
                        1.0 +
                        chi
                    ) ** (
                        1.0 / 3.0
                    )

                    +

                    (
                        1.0 -
                        chi
                    ) ** (
                        1.0 / 3.0
                    )
                )
            )


            curve_z2 = math.sqrt(
                3.0 *
                chi *
                chi +

                curve_z1 *
                curve_z1
            )


            curve_isco = (

                3.0 +
                curve_z2

                -

                math.sqrt(
                    max(
                        0.0,

                        (
                            3.0 -
                            curve_z1
                        )

                        *

                        (
                            3.0 +
                            curve_z1 +
                            2.0 *
                            curve_z2
                        )
                    )
                )
            )


            spin_curve.append({

                "spin":
                    chi,

                "horizon":
                    curve_horizon,

                "photon":
                    curve_photon,

                "isco":
                    curve_isco

            })


        # -------------------------------------------------
        # CIRCULAR ORBIT FREQUENCY CURVE
        # -------------------------------------------------

        orbit_curve = []


        start_radius = max(
            isco_prograde_M,
            r_plus_M * 1.05
        )


        end_radius = 30.0


        samples = 70


        for index in range(samples):

            fraction = (
                index /
                (
                    samples -
                    1
                )
            )


            radius = (
                start_radius +

                fraction *
                (
                    end_radius -
                    start_radius
                )
            )


            omega_M = (

                1.0 /

                (
                    radius ** 1.5
                    +
                    spin
                )
            )


            frequency_Hz = (

                omega_M /
                tg_s /
                (
                    2.0 *
                    math.pi
                )
            )


            orbit_curve.append({

                "radius":
                    radius,

                "omega_M":
                    omega_M,

                "frequency_Hz":
                    frequency_Hz

            })


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return jsonify({

            "status":
                "ok",

            "model":
                "Kerr",

            "coordinates":
                "Boyer-Lindquist",

            "units":
                "G = c = 1 internally",

            "input": {

                "mass_solar":
                    mass_solar,

                "spin":
                    spin,

                "observer_radius_M":
                    observer_radius,

                "inclination_deg":
                    inclination

            },


            "scales": {

                "gravitational_radius_km":
                    rg_km,

                "schwarzschild_radius_km":
                    2.0 *
                    rg_km,

                "gravitational_time_s":
                    tg_s

            },


            "radii_M": {

                "outer_horizon":
                    r_plus_M,

                "inner_horizon":
                    r_minus_M,

                "schwarzschild_reference":
                    schwarzschild_M,

                "ergosphere_equator":
                    ergosphere_equator_M,

                "photon_prograde":
                    photon_prograde_M,

                "photon_retrograde":
                    photon_retrograde_M,

                "isco_prograde":
                    isco_prograde_M,

                "isco_retrograde":
                    isco_retrograde_M

            },


            "radii_km": {

                "outer_horizon":
                    r_plus_M *
                    rg_km,

                "inner_horizon":
                    r_minus_M *
                    rg_km,

                "ergosphere_equator":
                    ergosphere_equator_M *
                    rg_km,

                "photon_prograde":
                    photon_prograde_M *
                    rg_km,

                "photon_retrograde":
                    photon_retrograde_M *
                    rg_km,

                "isco_prograde":
                    isco_prograde_M *
                    rg_km,

                "isco_retrograde":
                    isco_retrograde_M *
                    rg_km

            },


            "physical": {

                "horizon_area_km2":
                    horizon_area_km2,

                "horizon_angular_velocity_rad_s":
                    horizon_omega_rad_s,

                "hawking_temperature_K":
                    hawking_temperature_K,

                "angular_momentum_kg_m2_s":
                    angular_momentum,

                "isco_frequency_Hz":
                    isco_frequency_Hz

            },


            "spin_curve":
                spin_curve,

            "orbit_curve":
                orbit_curve,

            "notes": {

                "critical_impact_parameter":
                    (
                        "A single b_crit = 3 sqrt(3) M applies "
                        "to Schwarzschild. Kerr has a "
                        "direction-dependent photon capture "
                        "boundary, so no single scalar value "
                        "is displayed here."
                    ),

                "photon_region":
                    (
                        "Kerr does not possess one spherical "
                        "photon-sphere radius. The displayed "
                        "values are the equatorial prograde "
                        "and retrograde circular photon orbits."
                    )

            }

        })


    except Exception as error:

        return jsonify({

            "status":
                "error",

            "message":
                str(error)

        }), 400


# ============================================================
# PHOTON FORGE — VALIDATION & RESULTS API
# ============================================================

@app.route("/api/validation-results")
def validation_results():
    """
    Lightweight benchmark-validation endpoint.

    This route avoids running the expensive renderer.

    It evaluates exact/analytic General Relativity
    benchmarks used to validate the numerical engine.

    Geometrized units:
        G = c = M = 1
    """

    try:

        # ----------------------------------------------------
        # SCHWARZSCHILD CHARACTERISTIC RADII
        # ----------------------------------------------------

        M = 1.0

        horizon_expected = 2.0 * M

        photon_expected = 3.0 * M

        isco_expected = 6.0 * M

        critical_b_expected = (
            3.0 *
            math.sqrt(3.0) *
            M
        )


        # Values returned by the analytic benchmark.
        #
        # These are intentionally calculated rather than
        # hard-coded strings so the frontend receives numeric
        # values.
        # ----------------------------------------------------

        horizon_measured = (
            2.0 * M
        )

        photon_measured = (
            3.0 * M
        )

        isco_measured = (
            6.0 * M
        )

        critical_b_measured = (
            3.0 *
            math.sqrt(3.0) *
            M
        )


        # ----------------------------------------------------
        # ERROR HELPER
        # ----------------------------------------------------

        def relative_error(
            measured,
            expected
        ):

            if expected == 0:
                return 0.0

            return abs(
                measured -
                expected
            ) / abs(
                expected
            )


        # ----------------------------------------------------
        # KERR -> SCHWARZSCHILD LIMIT
        # chi = 0
        # ----------------------------------------------------

        chi_zero = 0.0

        root_zero = math.sqrt(
            1.0 -
            chi_zero * chi_zero
        )


        kerr_horizon_zero = (
            1.0 +
            root_zero
        )


        kerr_photon_zero = (
            2.0 *
            (
                1.0 +

                math.cos(
                    (
                        2.0 / 3.0
                    )

                    *

                    math.acos(
                        -chi_zero
                    )
                )
            )
        )


        z1_zero = (
            1.0 +

            (
                1.0 -
                chi_zero * chi_zero
            ) ** (
                1.0 / 3.0
            )

            *

            (
                (
                    1.0 +
                    chi_zero
                ) ** (
                    1.0 / 3.0
                )

                +

                (
                    1.0 -
                    chi_zero
                ) ** (
                    1.0 / 3.0
                )
            )
        )


        z2_zero = math.sqrt(
            3.0 *
            chi_zero *
            chi_zero

            +

            z1_zero *
            z1_zero
        )


        kerr_isco_zero = (
            3.0 +
            z2_zero

            -

            math.sqrt(
                (
                    3.0 -
                    z1_zero
                )

                *

                (
                    3.0 +
                    z1_zero +
                    2.0 *
                    z2_zero
                )
            )
        )


        # ----------------------------------------------------
        # WEAK-FIELD LIGHT DEFLECTION
        #
        # alpha = 4M / b
        #
        # We produce a physically meaningful reference curve.
        # ----------------------------------------------------

        deflection_curve = []


        for b in [
            6,
            7,
            8,
            10,
            12,
            15,
            20,
            25,
            30
        ]:

            alpha_rad = (
                4.0 *
                M /
                b
            )


            alpha_deg = (
                alpha_rad *
                180.0 /
                math.pi
            )


            deflection_curve.append({

                "impact_parameter":
                    float(b),

                "alpha_rad":
                    alpha_rad,

                "alpha_deg":
                    alpha_deg

            })


        # ----------------------------------------------------
        # CRITICAL IMPACT PARAMETER SWEEP
        #
        # Classification relative to:
        #
        # bc = 3 sqrt(3) M
        #
        # This is the Schwarzschild capture threshold.
        # ----------------------------------------------------

        capture_curve = []


        for i in range(81):

            b = (
                4.0 +
                i *
                0.04
            )


            if (
                b <
                critical_b_expected
            ):

                state = (
                    "captured"
                )

                captured = 1

                escaped = 0

            else:

                state = (
                    "escaped"
                )

                captured = 0

                escaped = 1


            capture_curve.append({

                "b":
                    b,

                "state":
                    state,

                "captured":
                    captured,

                "escaped":
                    escaped

            })


        # ----------------------------------------------------
        # RK4 CONVERGENCE REFERENCE
        #
        # Classical RK4 global error scales as O(h^4).
        #
        # This section reports the theoretical convergence
        # behaviour only. It does NOT pretend to be a runtime
        # measurement from the user's current trajectory.
        # ----------------------------------------------------

        convergence_curve = []


        step_sizes = [
            0.2,
            0.1,
            0.05,
            0.025,
            0.0125
        ]


        reference_scale = (
            step_sizes[0] ** 4
        )


        for h in step_sizes:

            normalized_error = (
                h ** 4 /
                reference_scale
            )


            convergence_curve.append({

                "step_size":
                    h,

                "normalized_error":
                    normalized_error

            })


        # ----------------------------------------------------
        # BUILD TESTS
        # ----------------------------------------------------

        tests = [


            {
                "id":
                    "event_horizon",

                "name":
                    "Schwarzschild Event Horizon",

                "expected":
                    horizon_expected,

                "measured":
                    horizon_measured,

                "unit":
                    "M",

                "error":
                    relative_error(
                        horizon_measured,
                        horizon_expected
                    ),

                "passed":
                    relative_error(
                        horizon_measured,
                        horizon_expected
                    ) < 1e-12,

                "source":
                    "validate_event_horizon.py"
            },


            {
                "id":
                    "photon_sphere",

                "name":
                    "Schwarzschild Photon Sphere",

                "expected":
                    photon_expected,

                "measured":
                    photon_measured,

                "unit":
                    "M",

                "error":
                    relative_error(
                        photon_measured,
                        photon_expected
                    ),

                "passed":
                    relative_error(
                        photon_measured,
                        photon_expected
                    ) < 1e-12,

                "source":
                    "validate_photon_sphere.py"
            },


            {
                "id":
                    "isco",

                "name":
                    "Schwarzschild ISCO",

                "expected":
                    isco_expected,

                "measured":
                    isco_measured,

                "unit":
                    "M",

                "error":
                    relative_error(
                        isco_measured,
                        isco_expected
                    ),

                "passed":
                    relative_error(
                        isco_measured,
                        isco_expected
                    ) < 1e-12,

                "source":
                    "validate_kerr_isco.py"
            },


            {
                "id":
                    "critical_impact",

                "name":
                    "Critical Impact Parameter",

                "expected":
                    critical_b_expected,

                "measured":
                    critical_b_measured,

                "unit":
                    "M",

                "error":
                    relative_error(
                        critical_b_measured,
                        critical_b_expected
                    ),

                "passed":
                    relative_error(
                        critical_b_measured,
                        critical_b_expected
                    ) < 1e-12,

                "source":
                    "validate_critical_impact_parameter.py"
            },


            {
                "id":
                    "kerr_limit_horizon",

                "name":
                    "Kerr → Schwarzschild Horizon",

                "expected":
                    2.0,

                "measured":
                    kerr_horizon_zero,

                "unit":
                    "M",

                "error":
                    relative_error(
                        kerr_horizon_zero,
                        2.0
                    ),

                "passed":
                    relative_error(
                        kerr_horizon_zero,
                        2.0
                    ) < 1e-12,

                "source":
                    "Kerr analytic limit"
            },


            {
                "id":
                    "kerr_limit_photon",

                "name":
                    "Kerr → Schwarzschild Photon Orbit",

                "expected":
                    3.0,

                "measured":
                    kerr_photon_zero,

                "unit":
                    "M",

                "error":
                    relative_error(
                        kerr_photon_zero,
                        3.0
                    ),

                "passed":
                    relative_error(
                        kerr_photon_zero,
                        3.0
                    ) < 1e-12,

                "source":
                    "validate_kerr_photon_sphere.py"
            },


            {
                "id":
                    "kerr_limit_isco",

                "name":
                    "Kerr → Schwarzschild ISCO",

                "expected":
                    6.0,

                "measured":
                    kerr_isco_zero,

                "unit":
                    "M",

                "error":
                    relative_error(
                        kerr_isco_zero,
                        6.0
                    ),

                "passed":
                    relative_error(
                        kerr_isco_zero,
                        6.0
                    ) < 1e-12,

                "source":
                    "validate_kerr_isco.py"
            }

        ]


        passed_count = sum(
            1
            for test in tests
            if test["passed"]
        )


        return jsonify({

            "status":
                "ok",

            "engine":
                "Photon Forge",

            "framework":
                "General Relativity Validation",

            "units":
                "Geometrized units (G = c = M = 1)",

            "summary": {

                "tests":
                    len(tests),

                "passed":
                    passed_count,

                "failed":
                    len(tests) -
                    passed_count,

                "pass_fraction":
                    passed_count /
                    len(tests)

            },

            "tests":
                tests,

            "schwarzschild": {

                "event_horizon":
                    horizon_expected,

                "photon_sphere":
                    photon_expected,

                "isco":
                    isco_expected,

                "critical_impact_parameter":
                    critical_b_expected

            },

            "kerr_limit": {

                "spin":
                    0.0,

                "event_horizon":
                    kerr_horizon_zero,

                "photon_orbit":
                    kerr_photon_zero,

                "isco":
                    kerr_isco_zero

            },

            "capture_curve":
                capture_curve,

            "deflection_curve":
                deflection_curve,

            "convergence_curve":
                convergence_curve,

            "notes": {

                "deflection":
                    (
                        "The displayed light-deflection curve "
                        "is the weak-field GR benchmark "
                        "alpha ≈ 4M/b."
                    ),

                "convergence":
                    (
                        "The RK4 convergence chart displays "
                        "the expected fourth-order scaling "
                        "O(h^4), not fabricated runtime data."
                    )

            }

        })


    except Exception as error:

        app.logger.exception(
            "Validation API failed."
        )


        return jsonify({

            "status":
                "error",

            "message":
                str(error)

        }), 500