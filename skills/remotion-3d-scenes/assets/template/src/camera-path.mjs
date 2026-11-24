// Pure frame-indexed camera path; no accumulated time, controls, randomness or physics.
export const TOTAL_FRAMES = 150;
export const FPS = 30;
export const WIDTH = 960;
export const HEIGHT = 540;
export const TARGET = [0, 1.05, -0.3];
export const MARKERS = {frontCup: [-1.15, 1.35, 1.0], backMenu: [0.45, 2.15, -2.34]};
export const cameraAt = (frame) => {
  const t = Math.max(0, Math.min(1, frame / (TOTAL_FRAMES - 1)));
  const eased = t * t * (3 - 2 * t);
  return [6.4 - 2.2 * eased, 4.3 - 0.25 * eased, 7.5 + 1.2 * eased];
};
