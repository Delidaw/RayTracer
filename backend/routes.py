import math

from pathlib import Path
from flask import (
    request,
    jsonify,
    send_from_directory,
    render_template
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