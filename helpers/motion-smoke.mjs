// Copied only into a new isolated 2D smoke project. Not a general production renderer.
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
process.chdir(root);
const require=createRequire(import.meta.url);
const {bundle}=require('@remotion/bundler');
const {RenderInternals,selectComposition,renderMedia,ensureBrowser}=require('@remotion/renderer');
assert.equal(require('@remotion/renderer/package.json').version,'4.0.538');
RenderInternals.getPortConfig=()=>({host:'127.0.0.1',hostsToTry:['127.0.0.1']});
let executable=process.env.REMOTION_BROWSER_EXECUTABLE;
if(executable){assert(fs.existsSync(executable),'Browser missing');}
else{
 assert(process.argv.includes('--download-browser'),'Explicit browser download authorization required');
 const status=await ensureBrowser({logLevel:'warn'});
 assert('path' in status,'Matching browser not ready: '+JSON.stringify(status));
 executable=status.path;
}
const command=(tool,args,encoding=null)=>{const result=spawnSync(tool,args,{encoding,maxBuffer:30*1024*1024,windowsHide:true});if(result.error)throw result.error;assert.equal(result.status,0,String(result.stderr));return result.stdout;};
const browserVersion=command(executable,['--version'],'utf8').trim();
fs.writeFileSync('notes/browser.json',JSON.stringify({path:executable,browserVersion,guard:RenderInternals.getPortConfig()},null,2));
const props=JSON.parse(fs.readFileSync('props.example.json','utf8'));
const serveUrl=await bundle({entryPoint:path.join(root,'src/index.ts'),outDir:path.join(root,'work/bundle'),enableCaching:false});
const common={serveUrl,browserExecutable:executable,inputProps:props,logLevel:'warn'};
const composition=await selectComposition({...common,id:'MotionGraphic'});
const output='exports/kit-motion-test.mp4';
assert(!fs.existsSync(output),'Refusing to overwrite export');
await renderMedia({...common,composition,outputLocation:path.join(root,output),codec:'h264',audioCodec:'aac',pixelFormat:'yuv420p',crf:18,concurrency:1,overwrite:false});
const probe=JSON.parse(command('ffprobe',['-v','error','-count_frames','-show_streams','-show_format','-of','json',output],'utf8'));
const video=probe.streams.find(s=>s.codec_type==='video'),audio=probe.streams.find(s=>s.codec_type==='audio');
assert(video&&audio,'Video AND test audio are required');
assert.equal(video.codec_name,'h264');assert.equal(audio.codec_name,'aac');
assert.equal(video.width,1280);assert.equal(video.height,720);assert.equal(video.r_frame_rate,'30/1');
assert.equal(Number(video.nb_read_frames),120);assert(Math.abs(Number(video.duration)-4)<0.04);
assert(Math.abs(Number(audio.duration)-4)<0.08);
command('ffmpeg',['-v','error','-i',output,'-f','null','-']);
const raw=f=>command('ffmpeg',['-v','error','-i',output,'-vf',"select='eq(n,"+f+")'",'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1']);
const stats=[];const hashes=[];
for(const [frame,name] of [[0,'first'],[60,'middle'],[108,'settled'],[119,'last']]){
 const dest='proof/encoded-'+name+'.png';
 command('ffmpeg',['-v','error','-n','-i',output,'-vf',"select='eq(n,"+frame+")'",'-frames:v','1',dest]);
 const pixels=raw(frame);assert.equal(pixels.length,1280*720*3);
 let sum=0,sq=0;for(const x of pixels){sum+=x;sq+=x*x;}const mean=sum/pixels.length,sd=Math.sqrt(sq/pixels.length-mean*mean);
 if(frame===119){assert(mean>240&&sd<4,'Expected deliberate final fade to the pale stage');}
 else{assert(mean>15&&sd>8,'Black/blank content frame: '+JSON.stringify({frame,mean,sd}));}
 stats.push({frame,mean,standardDeviation:sd,intentionalFadeToBackground:frame===119});
 hashes.push(crypto.createHash('sha256').update(pixels).digest('hex'));
}
assert(new Set(hashes).size>1,'Encoded frames must change');
const pcm=input=>command('ffmpeg',['-v','error','-i',input,'-map','0:a:0','-ac','1','-ar','16000','-f','f32le','pipe:1']);
const inputPCM=pcm('public/audio-fixture.wav'),outputPCM=pcm(output);
const count=Math.min(inputPCM.length,outputPCM.length)/4;
assert(count>=63500&&Math.abs(inputPCM.length-outputPCM.length)/4<1600,'Unexpected source/output audio sample count');
let dot=0,aa=0,bb=0,peak=0;
for(let i=0;i<count;i++){const a=inputPCM.readFloatLE(i*4),b=outputPCM.readFloatLE(i*4);dot+=a*b;aa+=a*a;bb+=b*b;peak=Math.max(peak,Math.abs(b));}
const correlation=dot/Math.sqrt(aa*bb),rms=Math.sqrt(bb/count);
assert(correlation>0.95&&rms>0.01&&peak<1,'Fixture audio timing/content/level check failed');
const report={status:'encoded-machine-verified',output,sha256:crypto.createHash('sha256').update(fs.readFileSync(output)).digest('hex'),video:{width:video.width,height:video.height,frames:Number(video.nb_read_frames),fps:30,duration:Number(video.duration)},audio:{codec:audio.codec_name,duration:Number(audio.duration),correlation,rms,peak,syntheticFixture:true,listeningPerformed:false},fullDecodePassed:true,sampledEncodedFrames:stats,visualReview:'pending-agent-review',browserVersion};
fs.writeFileSync('proof/verification-report.json',JSON.stringify(report,null,2));
console.log(JSON.stringify(report,null,2));
