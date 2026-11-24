import React from 'react';
import {Composition} from 'remotion';
import {MotionGraphic, type MotionProps} from './MotionGraphic';
import {defaultPalette} from './theme';
const defaults: MotionProps = {durationSeconds: 4, fps: 30, width: 1280, height: 720, title: 'Made here. Rendered locally.', subtitle: 'Frame-driven type, shapes and audio.', audioSrc: 'audio-fixture.wav', mediaSrc: '', mediaKind: 'image', captionPages: [], palette: defaultPalette};
export const RemotionRoot: React.FC = () => <Composition id="MotionGraphic" component={MotionGraphic} durationInFrames={120} fps={30} width={1280} height={720} defaultProps={defaults} calculateMetadata={({props}) => {
  if (!Number.isFinite(props.durationSeconds) || props.durationSeconds <= 0) throw new Error('durationSeconds must be measured and positive');
  if (!Number.isFinite(props.fps) || props.fps <= 0) throw new Error('fps must be positive');
  if (![props.width, props.height].every((v) => Number.isInteger(v) && v > 0 && v % 2 === 0)) throw new Error('Use positive even dimensions for yuv420p');
  return {durationInFrames: Math.max(1, Math.ceil(props.durationSeconds * props.fps)), fps: props.fps, width: props.width, height: props.height};
}}/>;
