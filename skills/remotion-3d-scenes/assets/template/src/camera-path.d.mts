export const TOTAL_FRAMES: number;
export const FPS: number;
export const WIDTH: number;
export const HEIGHT: number;
export const TARGET: [number, number, number];
export const MARKERS: Record<string, [number, number, number]>;
export function cameraAt(frame: number): [number, number, number];
