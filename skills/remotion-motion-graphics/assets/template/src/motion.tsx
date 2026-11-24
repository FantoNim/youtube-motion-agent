import React from 'react';
import {Img, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {motion} from './theme';
export const clamp01 = (n: number) => Math.max(0, Math.min(1, n));
export function easedProgress(frame: number, start: number, end: number): number {
  return interpolate(frame, [start, Math.max(start + 1, end)], [0, 1], {easing: motion.easeOut, extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
}
export const Entrance: React.FC<{at?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({at = 0, children, style}) => {
  const frame = useCurrentFrame(); const {fps} = useVideoConfig();
  const p = clamp01(spring({frame: frame - Math.round(at * fps), fps, config: motion.spring}));
  return <div style={{...style, opacity: p, transform: 'translateY(' + ((1 - p) * 24) + 'px) scale(' + (0.96 + p * 0.04) + ')'}}>{children}</div>;
};
export const WordReveal: React.FC<{text: string; at?: number; color: string}> = ({text, at = 0.12, color}) => <div style={{display: 'flex', flexWrap: 'wrap', gap: '10px 16px', color}}>{text.split(/\s+/).map((word, i) => <Entrance key={i} at={at + i * 0.1}><span>{word}</span></Entrance>)}</div>;
export const BarChart: React.FC<{color: string; ink: string; surface: string}> = ({color, ink, surface}) => {
  const frame = useCurrentFrame(); const {fps} = useVideoConfig();
  return <div style={{display: 'flex', flexDirection: 'column', gap: 22}}>{[{label: 'Type', value: 35}, {label: 'Shape', value: 65}, {label: 'Sound', value: 90}].map((row, i) => {
    const p = easedProgress(frame, (0.8 + i * 0.12) * fps, (1.75 + i * 0.12) * fps);
    return <div key={row.label}><div style={{display: 'flex', justifyContent: 'space-between', fontSize: 19, marginBottom: 8, color: ink}}><span>{row.label}</span><span style={{fontVariantNumeric: 'tabular-nums'}}>{Math.round(row.value * p)}%</span></div><div style={{height: 12, background: surface, borderRadius: 8, overflow: 'hidden'}}><div style={{height: '100%', width: (row.value * p) + '%', background: color, borderRadius: 8}} /></div></div>;
  })}</div>;
};
// All paths are relative to public/. No remote media or uploads.
export const LocalMedia: React.FC<{src: string; kind: 'image' | 'video'}> = ({src, kind}) => {
  const style: React.CSSProperties = {width: '100%', height: '100%', objectFit: 'contain'};
  return kind === 'video' ? <OffthreadVideo src={staticFile(src)} muted style={style}/> : <Img src={staticFile(src)} style={style}/>;
};
export type CaptionPage = {startSeconds: number; endSeconds: number; text: string};
export const CaptionPages: React.FC<{pages: CaptionPage[]; ink: string; background: string}> = ({pages, ink, background}) => {
  const frame = useCurrentFrame(); const {fps} = useVideoConfig();
  const page = pages.find((p) => frame / fps >= p.startSeconds && frame / fps < p.endSeconds);
  if (!page) return null;
  return <div style={{position: 'absolute', left: '12%', right: '12%', bottom: 20, textAlign: 'center', padding: 12, fontSize: 26, lineHeight: 1.25, fontWeight: 700, color: ink, background, borderRadius: 16}}>{page.text}</div>;
};
