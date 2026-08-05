"use strict";

const canvas = document.getElementById("canvas");
const viewport = document.getElementById("viewport");
const errorBox = document.getElementById("shaderError");

const gl = canvas.getContext("webgl2", {
  antialias: false,
  alpha: false,
  depth: false,
  stencil: false,
  preserveDrawingBuffer: false,
  powerPreference: "high-performance"
});

if (!gl) {
  errorBox.hidden = false;
  errorBox.textContent = "WebGL2 is not available in this browser.";
  throw new Error("WebGL2 unavailable");
}

const vertexShaderSource = `#version 300 es
precision highp float;

in vec2 aPosition;
out vec2 vUv;

void main() {
  vUv = aPosition * 0.5 + 0.5;
  gl_Position = vec4(aPosition, 0.0, 1.0);
}
`;

const fragmentShaderSource = `#version 300 es
precision highp float;
precision highp int;

in vec2 vUv;
out vec4 fragColor;

uniform vec2 uResolution;
uniform float uTime;
uniform float uMass;
uniform float uSpin;
uniform float uDistance;
uniform float uFov;
uniform float uYaw;
uniform float uPitch;
uniform float uDiskDensity;
uniform float uDiskThickness;
uniform float uExposure;
uniform int uMaxSteps;
uniform float uJitter;

#define PI 3.141592653589793
#define MAX_STEPS 420

float saturate(float x) {
  return clamp(x, 0.0, 1.0);
}

float hash31(vec3 p) {
  p = fract(p * 0.1031);
  p += dot(p, p.yzx + 33.33);
  return fract((p.x + p.y) * p.z);
}

float noise3(vec3 p) {
  vec3 i = floor(p);
  vec3 f = fract(p);
  f = f * f * (3.0 - 2.0 * f);

  float n000 = hash31(i + vec3(0,0,0));
  float n100 = hash31(i + vec3(1,0,0));
  float n010 = hash31(i + vec3(0,1,0));
  float n110 = hash31(i + vec3(1,1,0));
  float n001 = hash31(i + vec3(0,0,1));
  float n101 = hash31(i + vec3(1,0,1));
  float n011 = hash31(i + vec3(0,1,1));
  float n111 = hash31(i + vec3(1,1,1));

  float nx00 = mix(n000, n100, f.x);
  float nx10 = mix(n010, n110, f.x);
  float nx01 = mix(n001, n101, f.x);
  float nx11 = mix(n011, n111, f.x);

  return mix(mix(nx00, nx10, f.y), mix(nx01, nx11, f.y), f.z);
}

float fbm(vec3 p) {
  float value = 0.0;
  float amplitude = 0.55;

  for (int i = 0; i < 4; i++) {
    value += amplitude * noise3(p);
    p = p * 2.03 + vec3(17.1, 9.2, 13.7);
    amplitude *= 0.5;
  }

  return value;
}

vec3 temperatureColor(float temperatureK) {
  vec3 deepRed = vec3(0.72, 0.015, 0.003);
  vec3 red     = vec3(1.00, 0.08, 0.015);
  vec3 orange  = vec3(1.00, 0.40, 0.045);
  vec3 white   = vec3(1.00, 0.96, 0.88);
  vec3 cyan    = vec3(0.62, 0.90, 1.00);
  vec3 blue    = vec3(0.22, 0.43, 1.15);

  if (temperatureK < 3000.0) {
    return deepRed;
  }

  if (temperatureK < 4000.0) {
    return mix(
      deepRed,
      red,
      (temperatureK - 3000.0) / 1000.0
    );
  }

  if (temperatureK < 5500.0) {
    return mix(
      red,
      orange,
      (temperatureK - 4000.0) / 1500.0
    );
  }

  if (temperatureK < 7000.0) {
    return mix(
      orange,
      white,
      (temperatureK - 5500.0) / 1500.0
    );
  }

  if (temperatureK < 9500.0) {
    return mix(
      white,
      cyan,
      (temperatureK - 7000.0) / 2500.0
    );
  }

  return mix(
    cyan,
    blue,
    saturate((temperatureK - 9500.0) / 7500.0)
  );
}

vec3 backgroundSky(vec3 direction) {
  direction = normalize(direction);

  float longitude = atan(direction.z, direction.x);
  float latitude = asin(clamp(direction.y, -1.0, 1.0));

  float galacticBand = exp(-pow((latitude + 0.12 * sin(longitude * 1.7)) / 0.16, 2.0));
  float dustLane = 0.55 + 0.45 * fbm(direction * 8.0 + vec3(0.0, 0.0, uTime * 0.002));

  vec3 sky = vec3(0.0015, 0.0035, 0.009);
  sky += galacticBand * dustLane * vec3(0.045, 0.028, 0.075);

  float coarseStars = step(0.9945, hash31(floor(direction * 700.0)));
  float fineStars = step(0.9982, hash31(floor(direction * 1450.0 + 31.0)));

  sky += coarseStars * vec3(0.55, 0.72, 1.00);
  sky += fineStars * vec3(1.25, 1.10, 0.90);

  return sky;
}

float kerrISCO(float mass, float spinFraction) {
  float a = clamp(spinFraction, -0.998, 0.998);
  float z1 =
    1.0 +
    pow(1.0 - a * a, 1.0 / 3.0) *
    (
      pow(1.0 + a, 1.0 / 3.0) +
      pow(1.0 - a, 1.0 / 3.0)
    );

  float z2 = sqrt(3.0 * a * a + z1 * z1);

  float radius =
    3.0 +
    z2 -
    sign(a + 0.000001) *
    sqrt(
      max(
        0.0,
        (3.0 - z1) *
        (3.0 + z1 + 2.0 * z2)
      )
    );

  return radius * mass;
}

float diskDensityField(
  vec3 position,
  float innerRadius,
  float outerRadius,
  float thickness
) {
  float cylindricalRadius = length(position.xz);

  if (
    cylindricalRadius <= innerRadius ||
    cylindricalRadius >= outerRadius
  ) {
    return 0.0;
  }

  float radialCoordinate =
    (cylindricalRadius - innerRadius) /
    (outerRadius - innerRadius);

  float radialEnvelope =
    smoothstep(0.0, 0.08, radialCoordinate) *
    (1.0 - smoothstep(0.72, 1.0, radialCoordinate));

  float flaring =
    thickness *
    mix(0.62, 1.65, pow(radialCoordinate, 1.25));

  float verticalEnvelope =
    exp(
      -pow(
        abs(position.y) / max(flaring, 0.001),
        2.0
      )
    );

  float angle = atan(position.z, position.x);

  float spiralA =
    sin(
      angle * 7.0 -
      cylindricalRadius * 1.65 +
      uTime * 0.75
    );

  float spiralB =
    sin(
      angle * 13.0 +
      cylindricalRadius * 2.4 -
      uTime * 0.41
    );

  float turbulence =
    fbm(
      vec3(
        position.xz * 1.4,
        position.y * 5.0 + uTime * 0.035
      )
    );

  float structure =
    0.70 +
    0.16 * spiralA +
    0.08 * spiralB +
    0.38 * turbulence;

  float innerRim =
    0.45 +
    1.55 * exp(-6.5 * radialCoordinate);

  return max(
    0.0,
    radialEnvelope *
    verticalEnvelope *
    structure *
    innerRim
  );
}

vec3 acesFilm(vec3 x) {
  const float a = 2.51;
  const float b = 0.03;
  const float c = 2.43;
  const float d = 0.59;
  const float e = 0.14;

  return clamp(
    (x * (a * x + b)) /
    (x * (c * x + d) + e),
    0.0,
    1.0
  );
}

void main() {
  vec2 pixelJitter = vec2(
    hash31(vec3(gl_FragCoord.xy, uJitter)),
    hash31(vec3(gl_FragCoord.yx, uJitter + 17.0))
  ) - 0.5;

  vec2 screen =
    (
      gl_FragCoord.xy +
      pixelJitter * 0.55
    ) /
    uResolution;

  vec2 p = screen * 2.0 - 1.0;
  p.x *= uResolution.x / uResolution.y;

  float cosYaw = cos(uYaw);
  float sinYaw = sin(uYaw);
  float cosPitch = cos(uPitch);
  float sinPitch = sin(uPitch);

  vec3 rayOrigin =
    uDistance *
    vec3(
      cosPitch * sinYaw,
      sinPitch,
      cosPitch * cosYaw
    );

  vec3 forward = normalize(-rayOrigin);

  vec3 referenceUp =
    abs(forward.y) > 0.96
      ? vec3(0.0, 0.0, 1.0)
      : vec3(0.0, 1.0, 0.0);

  vec3 right = normalize(cross(forward, referenceUp));
  vec3 up = cross(right, forward);

  vec3 rayDirection =
    normalize(
      forward +
      (
        p.x * right +
        p.y * up
      ) *
      tan(uFov * 0.5)
    );

  float dimensionalSpin = uSpin * uMass;

  float horizonRadius =
    uMass +
    sqrt(
      max(
        0.0001,
        uMass * uMass -
        dimensionalSpin * dimensionalSpin
      )
    );

  float innerRadius =
    max(
      horizonRadius * 1.12,
      kerrISCO(uMass, uSpin)
    );

  float outerRadius = 12.0 * uMass;

  vec3 position = rayOrigin;
  vec3 radiance = vec3(0.0);
  float transmittance = 1.0;
  float minimumRadius = length(position);
  bool captured = false;

  for (int step = 0; step < MAX_STEPS; step++) {
    if (step >= uMaxSteps) {
      break;
    }

    float radius = length(position);
    minimumRadius = min(minimumRadius, radius);

    if (radius < horizonRadius * 1.003) {
      captured = true;
      transmittance = 0.0;
      break;
    }

    if (radius > 80.0 * uMass && step > 12) {
      break;
    }

    float cylindricalRadius = length(position.xz);

    float curvature =
      uMass /
      max(radius * radius * radius, 0.0001);

    float stepSize =
      clamp(
        0.036 * radius /
        (1.0 + 26.0 * curvature),
        0.012,
        0.34
      );

    if (
      cylindricalRadius > innerRadius * 0.85 &&
      cylindricalRadius < outerRadius * 1.08 &&
      abs(position.y) < uDiskThickness * 4.0
    ) {
      stepSize = min(stepSize, 0.075);
    }

    vec3 radialDirection =
      position /
      max(radius, 0.0001);

    vec3 angularMomentum =
      cross(position, rayDirection);

    float angularMomentumSquared =
      dot(angularMomentum, angularMomentum);

    vec3 schwarzschildAcceleration =
      -radialDirection *
      (
        1.22 * uMass /
        max(radius * radius, 0.0001) +
        3.0 *
        uMass *
        angularMomentumSquared /
        max(pow(radius, 4.0), 0.0001)
      );

    vec3 frameDraggingAcceleration =
      cross(
        vec3(0.0, 1.0, 0.0),
        rayDirection
      ) *
      (
        2.35 *
        dimensionalSpin *
        uMass /
        max(radius * radius * radius, 0.0001)
      );

    rayDirection =
      normalize(
        rayDirection +
        (
          schwarzschildAcceleration +
          frameDraggingAcceleration
        ) *
        stepSize
      );

    vec3 midpoint =
      position +
      rayDirection * stepSize * 0.5;

    float density =
      diskDensityField(
        midpoint,
        innerRadius,
        outerRadius,
        uDiskThickness
      ) *
      uDiskDensity;

    if (density > 0.0005 && transmittance > 0.002) {
      float diskRadius = length(midpoint.xz);

      float radialCoordinate =
        saturate(
          (diskRadius - innerRadius) /
          (outerRadius - innerRadius)
        );

      float emittedTemperature =
        mix(
          16500.0,
          2800.0,
          pow(radialCoordinate, 0.72)
        );

      vec3 orbitalDirection =
        normalize(
          vec3(
            -midpoint.z,
            0.0,
            midpoint.x
          )
        );

      float beta =
        clamp(
          sqrt(
            uMass /
            max(diskRadius, 0.0001)
          ),
          0.0,
          0.79
        );

      float gamma =
        inversesqrt(
          max(
            0.05,
            1.0 - beta * beta
          )
        );

      float viewAlignment =
        dot(
          -rayDirection,
          orbitalDirection
        );

      float dopplerFactor =
        1.0 /
        max(
          0.20,
          gamma *
          (
            1.0 -
            beta * viewAlignment
          )
        );

      float gravitationalFactor =
        sqrt(
          max(
            0.025,
            1.0 -
            horizonRadius /
            max(diskRadius, horizonRadius + 0.001)
          )
        );

      float redshiftFactor =
        clamp(
          dopplerFactor *
          gravitationalFactor,
          0.20,
          2.65
        );

      float observedTemperature =
        emittedTemperature *
        redshiftFactor;

      vec3 plasmaColor =
        temperatureColor(observedTemperature);

      float limbBrightening =
        0.68 +
        0.32 *
        pow(
          1.0 -
          abs(
            dot(
              rayDirection,
              vec3(0.0, 1.0, 0.0)
            )
          ),
          0.7
        );

      float emissivity =
        density *
        (
          0.18 +
          2.2 *
          exp(
            -4.8 *
            radialCoordinate
          )
        ) *
        pow(redshiftFactor, 4.0) *
        limbBrightening;

      float absorption =
        density *
        mix(
          1.45,
          0.38,
          radialCoordinate
        );

      float alpha =
        1.0 -
        exp(
          -absorption *
          stepSize
        );

      radiance +=
        transmittance *
        plasmaColor *
        emissivity *
        alpha *
        1.55;

      transmittance *=
        1.0 - alpha;
    }

    position += rayDirection * stepSize;
  }

  if (!captured && transmittance > 0.0) {
    radiance +=
      transmittance *
      backgroundSky(rayDirection);
  }

  float criticalRadius =
    3.0 * uMass;

  float photonGlow =
    exp(
      -pow(
        (
          minimumRadius -
          criticalRadius
        ) /
        max(0.14 * uMass, 0.025),
        2.0
      )
    );

  radiance +=
    vec3(1.0, 0.57, 0.22) *
    photonGlow *
    0.18;

  vec3 mapped =
    acesFilm(
      radiance *
      uExposure
    );

  float vignette =
    1.0 -
    0.22 *
    dot(p * 0.62, p * 0.62);

  mapped *= vignette;
  mapped = pow(mapped, vec3(1.0 / 2.2));

  fragColor = vec4(mapped, 1.0);
}
`;

function compileShader(type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);

  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    const log = gl.getShaderInfoLog(shader) || "Unknown shader error";
    gl.deleteShader(shader);
    throw new Error(log);
  }

  return shader;
}

function createProgram() {
  const program = gl.createProgram();
  const vertexShader = compileShader(gl.VERTEX_SHADER, vertexShaderSource);
  const fragmentShader = compileShader(gl.FRAGMENT_SHADER, fragmentShaderSource);

  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);

  gl.deleteShader(vertexShader);
  gl.deleteShader(fragmentShader);

  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    const log = gl.getProgramInfoLog(program) || "Unknown link error";
    gl.deleteProgram(program);
    throw new Error(log);
  }

  return program;
}

let program;

try {
  program = createProgram();
} catch (error) {
  errorBox.hidden = false;
  errorBox.textContent =
    "GPU shader compilation failed:\n\n" +
    error.message;
  throw error;
}

gl.useProgram(program);

const quad = new Float32Array([
  -1, -1,
   1, -1,
  -1,  1,
  -1,  1,
   1, -1,
   1,  1
]);

const vertexBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
gl.bufferData(gl.ARRAY_BUFFER, quad, gl.STATIC_DRAW);

const positionLocation =
  gl.getAttribLocation(program, "aPosition");

gl.enableVertexAttribArray(positionLocation);
gl.vertexAttribPointer(
  positionLocation,
  2,
  gl.FLOAT,
  false,
  0,
  0
);

const uniformNames = [
  "uResolution",
  "uTime",
  "uMass",
  "uSpin",
  "uDistance",
  "uFov",
  "uYaw",
  "uPitch",
  "uDiskDensity",
  "uDiskThickness",
  "uExposure",
  "uMaxSteps",
  "uJitter"
];

const uniforms = Object.fromEntries(
  uniformNames.map(
    name => [
      name,
      gl.getUniformLocation(program, name)
    ]
  )
);

const elements = {
  fpsBadge: document.getElementById("fpsBadge"),
  pauseButton: document.getElementById("pauseButton"),
  fullscreenButton: document.getElementById("fullscreenButton"),
  mass: document.getElementById("mass"),
  spin: document.getElementById("spin"),
  distance: document.getElementById("distance"),
  fov: document.getElementById("fov"),
  yaw: document.getElementById("yaw"),
  pitch: document.getElementById("pitch"),
  diskDensity: document.getElementById("diskDensity"),
  diskThickness: document.getElementById("diskThickness"),
  exposure: document.getElementById("exposure"),
  quality: document.getElementById("quality"),
  resetCamera: document.getElementById("resetCamera"),
  massOutput: document.getElementById("massOutput"),
  spinOutput: document.getElementById("spinOutput"),
  distanceOutput: document.getElementById("distanceOutput"),
  fovOutput: document.getElementById("fovOutput"),
  yawOutput: document.getElementById("yawOutput"),
  pitchOutput: document.getElementById("pitchOutput"),
  densityOutput: document.getElementById("densityOutput"),
  thicknessOutput: document.getElementById("thicknessOutput"),
  exposureOutput: document.getElementById("exposureOutput"),
  horizonValue: document.getElementById("horizonValue"),
  iscoValue: document.getElementById("iscoValue"),
  scaleValue: document.getElementById("scaleValue"),
  stepsValue: document.getElementById("stepsValue")
};

const qualityPresets = {
  performance: {
    renderScale: 0.48,
    maxSteps: 145
  },
  balanced: {
    renderScale: 0.68,
    maxSteps: 220
  },
  quality: {
    renderScale: 0.88,
    maxSteps: 310
  },
  ultra: {
    renderScale: 1.00,
    maxSteps: 400
  }
};

const state = {
  mass: 1.0,
  spin: 0.90,
  distance: 18.0,
  fov: 50.0,
  yaw: 0.0,
  pitch: 18.0 * Math.PI / 180,
  diskDensity: 1.20,
  diskThickness: 0.22,
  exposure: 1.25,
  preset: "balanced",
  paused: false
};

function degreesToRadians(value) {
  return value * Math.PI / 180;
}

function radiansToDegrees(value) {
  return value * 180 / Math.PI;
}

function wrapDegrees(value) {
  return ((value + 180) % 360 + 360) % 360 - 180;
}

function kerrISCO(spinFraction) {
  const a = Math.max(-0.998, Math.min(0.998, spinFraction));

  const z1 =
    1 +
    Math.cbrt(1 - a * a) *
    (
      Math.cbrt(1 + a) +
      Math.cbrt(1 - a)
    );

  const z2 =
    Math.sqrt(
      3 * a * a +
      z1 * z1
    );

  return (
    3 +
    z2 -
    Math.sign(a || 1) *
    Math.sqrt(
      Math.max(
        0,
        (3 - z1) *
        (3 + z1 + 2 * z2)
      )
    )
  );
}

function syncOutputs() {
  elements.massOutput.value =
    state.mass.toFixed(2) + " M";

  elements.spinOutput.value =
    state.spin.toFixed(2) + " a/M";

  elements.distanceOutput.value =
    state.distance.toFixed(1) + " M";

  elements.fovOutput.value =
    Math.round(state.fov) + "°";

  elements.yawOutput.value =
    Math.round(
      wrapDegrees(
        radiansToDegrees(state.yaw)
      )
    ) + "°";

  elements.pitchOutput.value =
    Math.round(
      radiansToDegrees(state.pitch)
    ) + "°";

  elements.densityOutput.value =
    state.diskDensity.toFixed(2);

  elements.thicknessOutput.value =
    state.diskThickness.toFixed(2) + " M";

  elements.exposureOutput.value =
    state.exposure.toFixed(2);

  const dimensionalSpin =
    state.spin * state.mass;

  const horizon =
    state.mass +
    Math.sqrt(
      Math.max(
        0,
        state.mass * state.mass -
        dimensionalSpin * dimensionalSpin
      )
    );

  elements.horizonValue.textContent =
    horizon.toFixed(3) + " M";

  elements.iscoValue.textContent =
    (
      kerrISCO(state.spin) *
      state.mass
    ).toFixed(3) + " M";

  const preset =
    qualityPresets[state.preset];

  elements.scaleValue.textContent =
    preset.renderScale.toFixed(2) + "×";

  elements.stepsValue.textContent =
    String(preset.maxSteps);
}

function updateHash() {
  const yawDegrees =
    wrapDegrees(
      radiansToDegrees(state.yaw)
    );

  const pitchDegrees =
    radiansToDegrees(state.pitch);

  const params = new URLSearchParams({
    zoom: state.distance.toFixed(3),
    preset: state.preset,
    spin: state.spin.toFixed(3),
    pitch: pitchDegrees.toFixed(2),
    yaw: yawDegrees.toFixed(2)
  });

  history.replaceState(
    null,
    "",
    "#" + params.toString()
  );
}

function readHash() {
  const raw =
    location.hash.startsWith("#")
      ? location.hash.slice(1)
      : "";

  if (!raw) {
    return;
  }

  const params = new URLSearchParams(raw);

  const distance =
    Number(params.get("zoom"));

  const spin =
    Number(params.get("spin"));

  const yaw =
    Number(params.get("yaw"));

  const pitch =
    Number(params.get("pitch"));

  const preset =
    params.get("preset");

  if (Number.isFinite(distance)) {
    state.distance =
      Math.max(
        6,
        Math.min(40, distance)
      );
  }

  if (Number.isFinite(spin)) {
    state.spin =
      Math.max(
        0,
        Math.min(0.99, spin)
      );
  }

  if (Number.isFinite(yaw)) {
    state.yaw =
      degreesToRadians(yaw);
  }

  if (Number.isFinite(pitch)) {
    state.pitch =
      degreesToRadians(
        Math.max(-78, Math.min(78, pitch))
      );
  }

  if (preset && qualityPresets[preset]) {
    state.preset = preset;
  }
}

function syncControlsFromState() {
  elements.mass.value = String(state.mass);
  elements.spin.value = String(state.spin);
  elements.distance.value = String(state.distance);
  elements.fov.value = String(state.fov);
  elements.yaw.value =
    String(
      wrapDegrees(
        radiansToDegrees(state.yaw)
      )
    );
  elements.pitch.value =
    String(
      radiansToDegrees(state.pitch)
    );
  elements.diskDensity.value =
    String(state.diskDensity);
  elements.diskThickness.value =
    String(state.diskThickness);
  elements.exposure.value =
    String(state.exposure);
  elements.quality.value =
    state.preset;
}

function bindSlider(
  element,
  stateKey,
  transform = Number
) {
  element.addEventListener(
    "input",
    () => {
      state[stateKey] =
        transform(element.value);

      syncOutputs();
      updateHash();
    }
  );
}

bindSlider(elements.mass, "mass");
bindSlider(elements.spin, "spin");
bindSlider(elements.distance, "distance");
bindSlider(elements.fov, "fov");

elements.yaw.addEventListener(
  "input",
  () => {
    state.yaw =
      degreesToRadians(
        Number(elements.yaw.value)
      );

    syncOutputs();
    updateHash();
  }
);

elements.pitch.addEventListener(
  "input",
  () => {
    state.pitch =
      degreesToRadians(
        Number(elements.pitch.value)
      );

    syncOutputs();
    updateHash();
  }
);

bindSlider(
  elements.diskDensity,
  "diskDensity"
);

bindSlider(
  elements.diskThickness,
  "diskThickness"
);

bindSlider(
  elements.exposure,
  "exposure"
);

elements.quality.addEventListener(
  "change",
  () => {
    state.preset =
      elements.quality.value;

    syncOutputs();
    updateHash();
  }
);

function resetCamera() {
  state.distance = 18;
  state.yaw = 0;
  state.pitch = degreesToRadians(18);

  syncControlsFromState();
  syncOutputs();
  updateHash();
}

elements.resetCamera.addEventListener(
  "click",
  resetCamera
);

viewport.addEventListener(
  "dblclick",
  resetCamera
);

elements.pauseButton.addEventListener(
  "click",
  () => {
    state.paused = !state.paused;

    elements.pauseButton.textContent =
      state.paused
        ? "Resume"
        : "Pause";
  }
);

elements.fullscreenButton.addEventListener(
  "click",
  async () => {
    if (!document.fullscreenElement) {
      await viewport.requestFullscreen();
    } else {
      await document.exitFullscreen();
    }
  }
);

let dragging = false;
let lastPointerX = 0;
let lastPointerY = 0;

canvas.addEventListener(
  "pointerdown",
  event => {
    dragging = true;
    lastPointerX = event.clientX;
    lastPointerY = event.clientY;
    canvas.setPointerCapture(event.pointerId);
  }
);

canvas.addEventListener(
  "pointerup",
  event => {
    dragging = false;

    if (
      canvas.hasPointerCapture(
        event.pointerId
      )
    ) {
      canvas.releasePointerCapture(
        event.pointerId
      );
    }
  }
);

canvas.addEventListener(
  "pointercancel",
  () => {
    dragging = false;
  }
);

canvas.addEventListener(
  "pointermove",
  event => {
    if (!dragging) {
      return;
    }

    const deltaX =
      event.clientX -
      lastPointerX;

    const deltaY =
      event.clientY -
      lastPointerY;

    lastPointerX =
      event.clientX;

    lastPointerY =
      event.clientY;

    state.yaw +=
      deltaX * 0.006;

    state.pitch =
      Math.max(
        degreesToRadians(-78),
        Math.min(
          degreesToRadians(78),
          state.pitch +
          deltaY * 0.005
        )
      );

    elements.yaw.value =
      String(
        wrapDegrees(
          radiansToDegrees(state.yaw)
        )
      );

    elements.pitch.value =
      String(
        radiansToDegrees(state.pitch)
      );

    syncOutputs();
    updateHash();
  }
);

canvas.addEventListener(
  "wheel",
  event => {
    event.preventDefault();

    const zoomFactor =
      Math.exp(
        event.deltaY * 0.0011
      );

    state.distance =
      Math.max(
        6,
        Math.min(
          40,
          state.distance *
          zoomFactor
        )
      );

    elements.distance.value =
      String(state.distance);

    syncOutputs();
    updateHash();
  },
  {
    passive: false
  }
);

function resizeCanvas() {
  const preset =
    qualityPresets[state.preset];

  const rect =
    canvas.getBoundingClientRect();

  const pixelRatio =
    Math.min(
      window.devicePixelRatio || 1,
      1.65
    );

  const width =
    Math.max(
      2,
      Math.floor(
        rect.width *
        pixelRatio *
        preset.renderScale
      )
    );

  const height =
    Math.max(
      2,
      Math.floor(
        rect.height *
        pixelRatio *
        preset.renderScale
      )
    );

  if (
    canvas.width !== width ||
    canvas.height !== height
  ) {
    canvas.width = width;
    canvas.height = height;
    gl.viewport(
      0,
      0,
      width,
      height
    );
  }
}

new ResizeObserver(
  resizeCanvas
).observe(viewport);

readHash();
syncControlsFromState();
syncOutputs();
updateHash();

let lastFrameTime =
  performance.now();

let frameCounter = 0;
let accumulatedTime = 0;
let fps = 0;
let jitterFrame = 0;

function render(now) {
  requestAnimationFrame(render);

  if (state.paused) {
    return;
  }

  resizeCanvas();

  const delta =
    Math.min(
      100,
      now - lastFrameTime
    );

  lastFrameTime = now;
  frameCounter += 1;
  accumulatedTime += delta;

  if (accumulatedTime >= 500) {
    fps =
      frameCounter *
      1000 /
      accumulatedTime;

    elements.fpsBadge.textContent =
      "GPU · " +
      fps.toFixed(0) +
      " FPS";

    frameCounter = 0;
    accumulatedTime = 0;
  }

  const preset =
    qualityPresets[state.preset];

  gl.uniform2f(
    uniforms.uResolution,
    canvas.width,
    canvas.height
  );

  gl.uniform1f(
    uniforms.uTime,
    now * 0.001
  );

  gl.uniform1f(
    uniforms.uMass,
    state.mass
  );

  gl.uniform1f(
    uniforms.uSpin,
    state.spin
  );

  gl.uniform1f(
    uniforms.uDistance,
    state.distance
  );

  gl.uniform1f(
    uniforms.uFov,
    degreesToRadians(
      state.fov
    )
  );

  gl.uniform1f(
    uniforms.uYaw,
    state.yaw
  );

  gl.uniform1f(
    uniforms.uPitch,
    state.pitch
  );

  gl.uniform1f(
    uniforms.uDiskDensity,
    state.diskDensity
  );

  gl.uniform1f(
    uniforms.uDiskThickness,
    state.diskThickness
  );

  gl.uniform1f(
    uniforms.uExposure,
    state.exposure
  );

  gl.uniform1i(
    uniforms.uMaxSteps,
    preset.maxSteps
  );

  gl.uniform1f(
    uniforms.uJitter,
    jitterFrame % 1024
  );

  jitterFrame += 1;

  gl.drawArrays(
    gl.TRIANGLES,
    0,
    6
  );
}

requestAnimationFrame(render);
