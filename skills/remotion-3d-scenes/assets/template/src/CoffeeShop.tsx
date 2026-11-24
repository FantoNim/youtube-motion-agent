import React, {useLayoutEffect} from 'react';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {ACESFilmicToneMapping, SRGBColorSpace} from 'three';
import {cameraAt, TARGET} from './camera-path.mjs';

type V3 = [number, number, number];
const Box: React.FC<{p: V3; s: V3; color: string; metal?: number}> = ({p,s,color,metal=0}) =>
  <mesh position={p} castShadow receiveShadow><boxGeometry args={s}/><meshStandardMaterial color={color} roughness={metal ? 0.28 : 0.72} metalness={metal}/></mesh>;
const Cup: React.FC<{p: V3; color?: string}> = ({p,color='#e7c78e'}) => <group position={p}>
  <mesh castShadow receiveShadow><cylinderGeometry args={[0.145,0.11,0.23,32]}/><meshStandardMaterial color={color} roughness={0.26}/></mesh>
  <mesh position={[0,0.118,0]}><cylinderGeometry args={[0.125,0.125,0.006,32]}/><meshStandardMaterial color='#43291d' roughness={0.3}/></mesh>
  <mesh position={[0.15,0.025,0]} rotation={[0,Math.PI/2,0]} castShadow><torusGeometry args={[0.075,0.022,12,24]}/><meshStandardMaterial color={color} roughness={0.26}/></mesh>
  <mesh position={[0,-0.13,0]} receiveShadow><cylinderGeometry args={[0.22,0.22,0.025,32]}/><meshStandardMaterial color='#f3ead8' roughness={0.4}/></mesh>
</group>;
const Table: React.FC<{p: V3}> = ({p}) => <group position={p}>
  <mesh position={[0,1.04,0]} castShadow receiveShadow><cylinderGeometry args={[0.67,0.67,0.12,48]}/><meshStandardMaterial color='#b77d48' roughness={0.57}/></mesh>
  <mesh position={[0,0.5,0]} castShadow><cylinderGeometry args={[0.06,0.085,0.95,16]}/><meshStandardMaterial color='#243d39' metalness={0.65} roughness={0.3}/></mesh>
  <mesh position={[0,0.06,0]} castShadow><cylinderGeometry args={[0.38,0.4,0.08,24]}/><meshStandardMaterial color='#243d39' roughness={0.4}/></mesh>
</group>;
const Chair: React.FC<{p: V3; rotation?: number}> = ({p,rotation=0}) => <group position={p} rotation={[0,rotation,0]}>
  <Box p={[0,0.57,0]} s={[0.46,0.09,0.48]} color='#315b4b'/>
  <Box p={[0,0.96,0.2]} s={[0.46,0.57,0.08]} color='#315b4b'/>
  {[-0.17,0.17].flatMap(x=>[-0.17,0.17].map(z=><Box key={x+','+z} p={[x,0.27,z]} s={[0.045,0.55,0.045]} color='#343934'/>))}
</group>;
const Plant: React.FC<{p: V3}> = ({p}) => <group position={p}>
  <mesh position={[0,0.24,0]} castShadow><cylinderGeometry args={[0.25,0.18,0.48,24]}/><meshStandardMaterial color='#b66642' roughness={0.9}/></mesh>
  <Box p={[0,0.75,0]} s={[0.04,0.9,0.04]} color='#416141'/>
  {[0,1,2,3,4].map(i=><mesh key={i} position={[Math.sin(i*2.3)*0.18,0.8+i*0.13,Math.cos(i*2.3)*0.15]} scale={[0.16,0.33,0.1]} rotation={[0,0,i%2 ? -0.6 : 0.6]} castShadow><sphereGeometry args={[1,16,12]}/><meshStandardMaterial color={i%2 ? '#536d40' : '#69894a'} roughness={0.8}/></mesh>)}
</group>;
const CameraRig: React.FC = () => {
  const frame=useCurrentFrame(); const {camera}=useThree();
  // Layout effect runs before ThreeCanvas's effect-triggered capture/advance.
  useLayoutEffect(()=>{camera.position.set(...cameraAt(frame)); camera.lookAt(...TARGET); camera.updateMatrixWorld();},[camera,frame]);
  return null;
};
export const CoffeeShop: React.FC = () => {
  const {width,height}=useVideoConfig();
  return <AbsoluteFill style={{background:'#d8ceba'}}>
    <ThreeCanvas width={width} height={height} dpr={1} shadows="soft"
      camera={{position:cameraAt(0),fov:38,near:0.1,far:70}}
      gl={{antialias:true,alpha:false,powerPreference:'high-performance'}}
      onCreated={({gl})=>{gl.toneMapping=ACESFilmicToneMapping;gl.toneMappingExposure=1.1;gl.outputColorSpace=SRGBColorSpace;const ctx=gl.getContext();const info=ctx.getExtension('WEBGL_debug_renderer_info');console.log('THREE_BACKEND '+JSON.stringify({version:ctx.getParameter(ctx.VERSION),vendor:info ? ctx.getParameter(info.UNMASKED_VENDOR_WEBGL) : ctx.getParameter(ctx.VENDOR),renderer:info ? ctx.getParameter(info.UNMASKED_RENDERER_WEBGL) : ctx.getParameter(ctx.RENDERER),shadowMap:gl.shadowMap.enabled,shadowType:gl.shadowMap.type}));}}>
      <color attach="background" args={['#d8ceba']}/>
      <CameraRig/>
      <ambientLight intensity={0.45}/>
      <hemisphereLight args={['#fff3d7','#6a6c54',1.35]}/>
      <directionalLight position={[-3,7,5]} intensity={3.6} color='#ffe4bb' castShadow shadow-mapSize-width={1024} shadow-mapSize-height={1024} shadow-camera-left={-6} shadow-camera-right={6} shadow-camera-top={6} shadow-camera-bottom={-6} shadow-camera-near={0.1} shadow-camera-far={25} shadow-bias={-0.0003} shadow-normalBias={0.025}/>
      <pointLight position={[0.4,2.9,-1.0]} intensity={12} color='#ffc27a' distance={8} decay={2}/>
      {/* Open dollhouse shell, procedural floor planks and rear wall. */}
      <Box p={[0,-0.14,0]} s={[7,0.28,6]} color='#77583d'/>
      {Array.from({length:14},(_,i)=><Box key={i} p={[-3.24+i*0.5,0.005,0]} s={[0.48,0.025,5.9]} color={i%3===0 ? '#b18c61' : i%3===1 ? '#c4a275' : '#ba966a'}/>)}
      <Box p={[0,1.55,-2.6]} s={[7,3.1,0.16]} color='#d8c9ab'/>
      <Box p={[-3.46,0.58,-0.7]} s={[0.12,1.16,3.7]} color='#d8c9ab'/>
      <Box p={[0.2,0.58,-1.7]} s={[4.3,1.16,0.95]} color='#345449'/>
      <Box p={[0.2,1.2,-1.7]} s={[4.5,0.14,1.1]} color='#e9d9bc'/>
      {[-1.5,-0.5,0.5,1.5].map(x=><Box key={x} p={[x,0.58,-1.211]} s={[0.025,0.98,0.015]} color='#567164'/>)}
      {/* Espresso machine: steel body, group head, drip tray and controls. */}
      <Box p={[-0.5,1.66,-1.8]} s={[1.15,0.78,0.6]} color='#a9b2ae' metal={0.75}/>
      <Box p={[-0.5,1.62,-1.47]} s={[0.94,0.32,0.08]} color='#1f302c' metal={0.3}/>
      <Box p={[-0.5,1.31,-1.36]} s={[1.15,0.05,0.4]} color='#b1b8b2' metal={0.75}/>
      {[-0.78,-0.3].map(x=><group key={x}><Box p={[x,1.62,-1.35]} s={[0.15,0.1,0.18]} color='#afb6b0' metal={0.7}/><Cup p={[x,1.47,-1.24]} color='#f3e3c6'/></group>)}
      <Box p={[1.0,1.51,-1.8]} s={[0.38,0.46,0.42]} color='#243e38'/>
      <mesh position={[1,1.94,-1.8]} castShadow><cylinderGeometry args={[0.18,0.12,0.4,24]}/><meshStandardMaterial color='#795239' roughness={0.3}/></mesh>
      <Box p={[0.45,2.15,-2.49]} s={[1.5,0.86,0.08]} color='#845b37'/>
      <Box p={[0.45,2.15,-2.43]} s={[1.36,0.72,0.04]} color='#173c35'/>
      {[0,1,2].map(i=><Box key={i} p={[0.45,2.34-i*0.19,-2.402]} s={[0.87-i*0.12,0.028,0.015]} color='#ddd0a9'/>)}
      <Table p={[-1.15,0,1]}/><Cup p={[-1.15,1.24,1]}/>
      <Chair p={[-2.12,0,1]} rotation={Math.PI/2}/><Chair p={[-0.25,0,1.25]} rotation={-Math.PI/2}/>
      <Table p={[1.65,0,0.5]}/><Cup p={[1.7,1.24,0.5]} color='#527a67'/><Chair p={[2.55,0,0.65]} rotation={-Math.PI/2}/>
      <Plant p={[-2.6,0,-1.9]}/><Plant p={[2.85,0,-1.9]}/>
      <mesh position={[0.3,3,-1.1]} castShadow><coneGeometry args={[0.4,0.24,32]}/><meshStandardMaterial color='#c59945' metalness={0.7} roughness={0.35}/></mesh>
      <Box p={[0.3,3.33,-1.1]} s={[0.025,0.5,0.025]} color='#33392d'/>
    </ThreeCanvas>
    <div style={{position:'absolute',top:24,left:28,color:'#244239',fontFamily:'Arial, sans-serif',fontSize:15,fontWeight:700,letterSpacing:2}}>SILENT TECHNICAL TEST · PROCEDURAL 3D</div>
    <div style={{position:'absolute',bottom:20,left:28,color:'#244239',fontFamily:'Arial, sans-serif',fontSize:13}}>5 s · frame-driven camera · not a reference-style or user-approved sample</div>
  </AbsoluteFill>;
};
