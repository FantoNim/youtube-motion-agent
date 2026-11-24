import {Easing} from 'remotion';
export type Palette = {ink: string; hero: string; accent: string; background: string; highlight: string; card: string};
// Neutral example palette only. Put each user's actual brand in project props/theme.
export const defaultPalette: Palette = {ink: '#111827', hero: '#BFDBFE', accent: '#2563EB', background: '#F8FAFC', highlight: '#DBEAFE', card: '#FFFFFF'};
export const motion = {easeOut: Easing.bezier(0.16, 1, 0.3, 1), easeIn: Easing.bezier(0.7, 0, 0.84, 0), spring: {damping: 22, stiffness: 130, mass: 0.8}};
export const typography = {font: 'Arial, sans-serif'}; // Smoke-test fallback; use a licensed local font for reproducible brand work.
