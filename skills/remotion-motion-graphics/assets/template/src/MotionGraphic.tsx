import React from 'react';
import {AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {BarChart, CaptionPages, Entrance, LocalMedia, WordReveal, type CaptionPage} from './motion';
import {motion, typography, type Palette} from './theme';
export type MotionProps = {durationSeconds: number; fps: number; width: number; height: number; title: string; subtitle: string; audioSrc: string; mediaSrc: string; mediaKind: 'image' | 'video'; captionPages: CaptionPage[]; palette: Palette};
export const MotionGraphic: React.FC<MotionProps> = (props) => {
  const {palette: c} = props; const frame = useCurrentFrame(); const {fps, durationInFrames, width, height} = useVideoConfig();
  const exit = interpolate(frame, [Math.max(0, durationInFrames - Math.round(0.22 * fps)), durationInFrames - 1], [1, 0], {easing: motion.easeIn, extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  // Design on a 1280x720 stage and scale as a unit; redesign for portrait production rather than cropping blindly.
  const stageScale = Math.min(width / 1280, height / 720);
  return <AbsoluteFill style={{background: c.background, color: c.ink, fontFamily: typography.font}}>
    {props.audioSrc ? <Audio src={staticFile(props.audioSrc)}/> : null}
    <div style={{position: 'absolute', width: 1280, height: 720, left: (width - 1280 * stageScale) / 2, top: (height - 720 * stageScale) / 2, transform: 'scale(' + stageScale + ')', transformOrigin: 'top left', opacity: exit}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 86, background: c.hero, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 64px', fontSize: 20, fontWeight: 700, letterSpacing: 1}}><span>LOCAL MOTION / 001</span><span>{props.durationSeconds.toFixed(2)}s / {fps} FPS</span></div>
      <div style={{position: 'absolute', left: 64, top: 138, width: 610}}>
        <Entrance at={0.05}><div style={{display: 'inline-block', border: '2px solid ' + c.ink, borderRadius: 100, padding: '9px 16px', fontSize: 15, fontWeight: 700, letterSpacing: 1}}>EDITABLE. DETERMINISTIC. LOCAL.</div></Entrance>
        <div style={{fontSize: 68, lineHeight: 1.07, letterSpacing: -2, fontWeight: 800, marginTop: 28}}><WordReveal text={props.title} color={c.ink}/></div>
        <Entrance at={0.65}><div style={{fontSize: 25, lineHeight: 1.4, marginTop: 24, maxWidth: 540}}>{props.subtitle}</div></Entrance>
      </div>
      <Entrance at={0.45} style={{position: 'absolute', right: 64, top: 142, width: 424, height: 300, padding: 28, boxSizing: 'border-box', borderRadius: 22, background: c.card}}>
        {props.mediaSrc ? <LocalMedia src={props.mediaSrc} kind={props.mediaKind}/> : <><div style={{fontSize: 15, fontWeight: 700, marginBottom: 24, letterSpacing: 1}}>ILLUSTRATIVE MOTION DATA</div><BarChart color={c.accent} ink={c.ink} surface={c.highlight}/></>}
      </Entrance>
      <div style={{position: 'absolute', left: 64, right: 64, bottom: 94, display: 'flex', gap: 20}}>{['01 / TYPE', '02 / SHAPES', '03 / AUDIO'].map((label, i) => <Entrance key={label} at={0.95 + i * 0.14} style={{flex: 1, borderRadius: 20, background: i === 0 ? c.highlight : c.card, padding: '25px 26px'}}><div style={{width: 28, height: 7, background: c.accent, borderRadius: 6, marginBottom: 18}}/><div style={{fontWeight: 700, fontSize: 20}}>{label}</div><div style={{fontSize: 17, marginTop: 9}}>{['Frame-timed words', 'Purposeful movement', 'Original timing kept'][i]}</div></Entrance>)}</div>
      {props.captionPages.length === 0 ? <div style={{position: 'absolute', bottom: 35, left: 64, right: 64, display: 'flex', justifyContent: 'space-between', fontSize: 16}}><span>Remotion + React / rendered on this machine</span><span>LOCAL TOOL SMOKE TEST</span></div> : null}
      <CaptionPages pages={props.captionPages} ink={c.ink} background={c.card}/>
    </div>
  </AbsoluteFill>;
};
