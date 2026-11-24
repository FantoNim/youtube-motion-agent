import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {bundle} from '@remotion/bundler';
import {RenderInternals,selectComposition,renderStill,renderMedia} from '@remotion/renderer';
const require=createRequire(import.meta.url);
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
process.chdir(root);
if(require('@remotion/renderer/package.json').version!=='4.0.538') throw new Error('Re-review loopback guard for new renderer version');
RenderInternals.getPortConfig=()=>({host:'127.0.0.1',hostsToTry:['127.0.0.1']});
const gl=process.env.REMOTION_GL || 'angle';
if(!['angle','swangle'].includes(gl)) throw new Error('Reviewed backends are angle or swangle');
const executable=process.env.REMOTION_BROWSER_EXECUTABLE || path.resolve(root,'../remotion-local/node_modules/.remotion/chrome-headless-shell/win64/chrome-headless-shell-win64/chrome-headless-shell.exe');
if(!fs.existsSync(executable)) throw new Error('Set REMOTION_BROWSER_EXECUTABLE to a verified local compatible Chromium; no automatic download');
for(const d of ['proof','exports','notes','work']) fs.mkdirSync(d,{recursive:true});
const preview=process.argv.includes('--stills');
const suffix=preview?'stills':'encode';
const logs=[];
const onBrowserLog=(log)=>{logs.push({type:log.type,text:log.text});if(log.text.includes('THREE_BACKEND')) console.log(log.text);};
const serveUrl=await bundle({entryPoint:path.join(root,'src/index.tsx'),outDir:path.join(root,'work','bundle-'+suffix),enableCaching:true,publicDir:null});
const common={serveUrl,browserExecutable:executable,chromiumOptions:{gl},onBrowserLog,logLevel:'warn',timeoutInMilliseconds:120000};
try {
 const composition=await selectComposition({...common,id:'CoffeeShopTechnicalTest'});
 if(preview){
  for(const [frame,name] of [[0,'source-first'],[75,'source-middle'],[149,'source-last'],[75,'source-middle-repeat']]){
   const output=path.join(root,'proof',name+'.png');
   if(fs.existsSync(output)) throw new Error('Refusing overwrite: '+output);
   await renderStill({...common,composition,frame,imageFormat:'png',output,overwrite:false});
   console.log('STILL '+name);
  }
 }else{
  const outputLocation=path.join(root,'exports','coffee-shop-3d-silent-technical-test-v001.mp4');
  if(fs.existsSync(outputLocation)) throw new Error('Refusing overwrite: '+outputLocation);
  let last=-1;
  await renderMedia({...common,composition,outputLocation,codec:'h264',crf:18,pixelFormat:'yuv420p',colorSpace:'bt709',imageFormat:'png',concurrency:1,muted:true,enforceAudioTrack:false,overwrite:false,onProgress:({renderedFrames})=>{const n=Math.floor(renderedFrames/30);if(n!==last){last=n;console.log('RENDERED '+renderedFrames+'/150');}}});
  console.log('ENCODED '+outputLocation);
 }
} finally {
 fs.writeFileSync(path.join(root,'notes','browser-'+suffix+'.json'),JSON.stringify({backendRequested:gl,executable,loopbackGuard:RenderInternals.getPortConfig(false),logs},null,2));
}
