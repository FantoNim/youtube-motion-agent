import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {CoffeeShop} from './CoffeeShop';
import {TOTAL_FRAMES,FPS,WIDTH,HEIGHT} from './camera-path.mjs';
const Root: React.FC = () => <Composition id="CoffeeShopTechnicalTest" component={CoffeeShop} durationInFrames={TOTAL_FRAMES} fps={FPS} width={WIDTH} height={HEIGHT}/>;
registerRoot(Root);
