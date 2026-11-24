#!/usr/bin/env python3
"""Auditable chronological keep-list executor. No semantic cut detection or network calls."""
import argparse
from array import array
import importlib.util
import json
import math
from pathlib import Path
import sys

# Reuse the installed repository's conservative probe/confinement/verification gates.
SIBLING = Path(__file__).resolve().parents[2] / 'local-video-clipping' / 'scripts' / 'clip_local.py'
if not SIBLING.is_file():
    raise SystemExit('Required sibling local-video-clipping/scripts/clip_local.py is missing.')
spec = importlib.util.spec_from_file_location('cleanup_clip_dependency', SIBLING)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
Error = c.ClipError
SKILL = Path(__file__).resolve().parents[1]
RUN_LOG = None
BASE_RUN = c.run

def logged_run(argv, binary=False, timeout=1800):
    if RUN_LOG is not None:
        with RUN_LOG.open('a',encoding='utf-8') as f:
            f.write(json.dumps({'argv':[str(x) for x in argv],'binary_stdout':binary,'timeout_seconds':timeout})+'\n')
    return BASE_RUN(argv,binary=binary,timeout=timeout)

c.run = logged_run


def require_text(obj, key):
    if not isinstance(obj.get(key), str) or not obj[key].strip():
        raise Error('Required nonempty evidence text: ' + key)


def load(value):
    def unique(pairs):
        obj = {}
        for key, val in pairs:
            if key in obj:
                raise Error('Duplicate JSON key: ' + key)
            obj[key] = val
        return obj
    with Path(value).open(encoding='utf-8') as f:
        obj = json.load(f, object_pairs_hook=unique,
                        parse_constant=lambda x: (_ for _ in ()).throw(Error('Nonfinite JSON.')))
    if not isinstance(obj, dict):
        raise Error('Keep-list must be an object.')
    return obj


def mapping(data, obj):
    # Narrow initial scope: retain ALL original A/V, reject ambiguity rather than drop tracks.
    if any(s.get('codec_type') not in {'video', 'audio'} or
           s.get('disposition', {}).get('attached_pic') for s in data['streams']):
        raise Error('Extra/attached/subtitle/data streams unsupported; no silent dropping.')
    vv = [s for s in data['streams'] if s.get('codec_type') == 'video']
    aa = [s for s in data['streams'] if s.get('codec_type') == 'audio']
    if len(vv) != 1 or len(aa) > 1:
        raise Error('Multiple/missing video or multiple audio streams unsupported; preserve all via a separate design.')
    v, a = vv[0], aa[0] if aa else None
    if type(obj.get('video_stream')) is not int or obj['video_stream'] != v['index']:
        raise Error('Explicit absolute video_stream must match source.')
    if (a and (type(obj.get('audio_stream')) is not int or obj['audio_stream'] != a['index'])) or (not a and obj.get('audio_stream', 'missing') is not None):
        raise Error('Explicit absolute audio_stream must match source, or null for no audio.')
    require_text(obj, 'mapping_reason')
    return v, a


def evidence(row):
    for key in ('reason', 'transcript_evidence', 'boundary_review'):
        require_text(row, key)


def build_plan(obj, duration, fps, source_hash, hz=None):
    allowed = {'schema_version','source_sha256','video_stream','audio_stream','mapping_reason',
               'selection_basis','coverage','keep','deletions','limitations','quantization'}
    if set(obj) - allowed or obj.get('schema_version') != 1 or type(obj.get('schema_version')) is not int:
        raise Error('Unknown fields/schema; no arbitrary output names or FFmpeg flags.')
    if obj.get('source_sha256') != source_hash:
        raise Error('Source SHA-256 differs from reviewed keep-list.')
    for key in ('selection_basis','limitations'):
        require_text(obj, key)
    if obj.get('quantization') != 'nearest_frame_reviewed':
        raise Error('Require explicit nearest_frame_reviewed quantization authorization; inspect resulting plan before render.')
    coverage = obj.get('coverage')
    if not isinstance(coverage, dict) or set(coverage) != {'duration','basis','windows'}:
        raise Error('coverage requires duration, basis and full windows.')
    if abs(c.number(coverage['duration'],'coverage duration')-duration) > 1e-5:
        raise Error('Coverage duration differs from shortest original A/V bound.')
    require_text(coverage, 'basis')
    windows = coverage['windows']
    if not isinstance(windows, list) or not windows:
        raise Error('Empty coverage map.')
    covered = 0.
    for w in windows:
        if not isinstance(w, dict) or set(w) != {'start','end','status','evidence','timing_uncertainty_seconds'}:
            raise Error('Coverage window fields invalid.')
        start, end = c.number(w['start'],'coverage start'), c.number(w['end'],'coverage end')
        if not 0 <= start < end <= duration+1e-6 or start > covered+1e-6:
            raise Error('Coverage gap/out-of-range/empty window; complete full-source context first.')
        if w['status'] not in {'reviewed_transcript','reviewed_playback','reviewed_visual_only','synthetic_fixture'}:
            raise Error('Unresolved/failed ASR coverage is blocked; review playback or supply reliable transcript.')
        # hz is supplied only for an actual selected source audio stream.
        if hz is not None and w['status'] == 'reviewed_visual_only':
            raise Error('Audio present: reviewed_visual_only coverage is unsupported for speech cleanup; require reviewed transcript/playback.')
        require_text(w, 'evidence')
        uncertainty = c.number(w['timing_uncertainty_seconds'],'timing uncertainty')
        if uncertainty < 0:
            raise Error('Timing uncertainty cannot be negative.')
        covered = max(covered,end)
    if covered < duration-1e-6:
        raise Error('Incomplete full-source coverage.')
    keeps = obj.get('keep')
    if not isinstance(keeps,list) or not 1 <= len(keeps) <= 2000:
        raise Error('Nonempty keep list required (maximum 2000 spans).')
    result=[]
    previous = 0.
    out_frames = 0
    for row in keeps:
        if not isinstance(row,dict) or set(row) != {'start','end','reason','transcript_evidence','boundary_review'}:
            raise Error('Keep fields invalid.')
        evidence(row)
        start,end=c.number(row['start'],'keep start'),c.number(row['end'],'keep end')
        if not 0 <= start < end <= duration+1e-6 or start < previous-1e-7:
            raise Error('Keep spans must be chronological, nonoverlapping and in bounds.')
        # Half-up frame quantization, recorded explicitly, never forced fps conversion.
        sf,ef=math.floor(start*fps+.5),math.floor(end*fps+.5)
        qs,qe=sf/fps,ef/fps
        if ef-sf < 2 or qe > duration+1e-6:
            raise Error('Empty/tiny/out-of-bound quantized span (minimum two frames).')
        if result and sf < result[-1]['end_frame']:
            raise Error('Quantized overlap forbidden.')
        if hz and any(abs(t*hz-round(t*hz)) > .0001 for t in (qs,qe)):
            raise Error('Frame/sample lattice incompatible; exact shared boundaries need a deliberate implementation, no silent padding/stretch.')
        result.append(dict(row,start_frame=sf,end_frame=ef,source_start=qs,source_end=qe,
                           start_delta_seconds=qs-start,end_delta_seconds=qe-end,
                           output_start_frame=out_frames,output_end_frame=out_frames+ef-sf,
                           output_start=out_frames/fps,output_end=(out_frames+ef-sf)/fps))
        out_frames += ef-sf
        previous=end
    # Every deleted interval must be explicitly justified: no unexplained gaps.
    gaps=[]
    previous=0.
    for row in result:
        if row['source_start'] > previous+1e-7:
            gaps.append((previous,row['source_start']))
        previous=row['source_end']
    if previous < duration-1e-7:
        gaps.append((previous,duration))
    deletions=obj.get('deletions')
    if not isinstance(deletions,list) or len(deletions)!=len(gaps):
        raise Error('Deletions must cover exactly every complement interval of the quantized keep-list.')
    for row,(start,end) in zip(deletions,gaps):
        if not isinstance(row,dict) or set(row) != {'start','end','reason','transcript_evidence','boundary_review'}:
            raise Error('Deletion fields invalid.')
        evidence(row)
        if abs(c.number(row['start'],'deletion start')-start)>1e-6 or abs(c.number(row['end'],'deletion end')-end)>1e-6:
            raise Error('Deletion does not match quantized keep complement; revise evidence explicitly.')
    return {'keep':result,'deletions':deletions,'output_frames':out_frames,
            'output_duration':out_frames/fps,'source_duration':duration,
            'note':'Source/output seconds use original common zero-origin clock; quantization is explicit.'}


def common_input(ffmpeg, source):
    return [ffmpeg,'-nostdin','-v','error','-xerror','-n','-threads','1',
            '-protocol_whitelist','file,pipe','-noautorotate','-i',source]


def pcm(path,index,ffmpeg,start=0,seconds=None):
    cmd=[ffmpeg,'-nostdin','-v','error','-threads','1','-protocol_whitelist','file,pipe',
         '-ss',str(start),'-i',path,'-map','0:'+str(index),'-vn']
    if seconds is not None:
        cmd+=['-t',str(seconds)]
    # Do not downmix/resample: retain all original channels/sample clock.
    raw=c.run(cmd+['-f','f32le','pipe:1'],binary=True)
    vals=array('f');vals.frombytes(raw)
    if not vals or any(not math.isfinite(x) for x in vals):
        raise Error('Missing/nonfinite PCM.')
    return vals


def check_energy(values):
    rms=math.sqrt(sum(x*x for x in values)/len(values))
    if rms <= 1e-5:
        raise Error('Silence-only/near-zero selected audio span; do not infer speech from empty ASR. Review or use a separate visual-only design.')
    return rms


def encode_video_options():
    return ['-map_metadata','-1','-map_chapters','-1','-c:v','libx264','-preset','fast','-crf','18',
            '-threads','1','-fps_mode','passthrough']


def compare_audio(source,a,output,rows,ffmpeg):
    checks=[]
    for row in rows:
        length=row['source_end']-row['source_start']
        seconds=min(.1,length/8)
        for t in (seconds,length/2,length-2*seconds):
            before=pcm(source,a['index'],ffmpeg,row['source_start']+t,seconds)
            after=pcm(output,1,ffmpeg,row['output_start']+t,seconds)
            if len(before)!=len(after):
                raise Error('Audio sampled length changed.')
            p=sum(x*x for x in before);q=sum(x*x for x in after)
            corr=None
            if min(p,q)/len(before)>1e-8:
                corr=sum(x*y for x,y in zip(before,after))/math.sqrt(p*q)
                if corr < .9:
                    raise Error('Sampled source/output PCM mismatch; possible join drift.')
            elif max(p,q)/len(before)>1e-7:
                raise Error('Sampled audio silence/content differs.')
            checks.append({'source_seconds':row['source_start']+t,'output_seconds':row['output_start']+t,
                           'pcm_correlation':corr})
    return checks


def compare_audio_joins(source,a,output,rows,ffmpeg):
    checks=[]
    for left,right in zip(rows,rows[1:]):
        seconds=min(.02,(left['source_end']-left['source_start'])/8,(right['source_end']-right['source_start'])/8)
        for side,st,ot in (('left',left['source_end']-seconds,left['output_end']-seconds),
                           ('right',right['source_start'],right['output_start'])):
            before=pcm(source,a['index'],ffmpeg,st,seconds)
            after=pcm(output,1,ffmpeg,ot,seconds)
            if len(before)!=len(after):raise Error('Join PCM sample length mismatch.')
            p=sum(x*x for x in before);q=sum(x*x for x in after);corr=None
            if min(p,q)/len(before)>1e-8:
                corr=sum(x*y for x,y in zip(before,after))/math.sqrt(p*q)
                if corr<.9:raise Error('Immediate join PCM mismatch/drift.')
            elif max(p,q)/len(before)>1e-7:raise Error('Join silence/content mismatch.')
            checks.append({'side':side,'source_seconds':st,'output_seconds':ot,'seconds':seconds,'pcm_correlation':corr})
    return checks


def proof_and_compare(source,v,output,rows,fps,ffmpeg,root):
    checks=[]
    for i,row in enumerate(rows,1):
        count=row['end_frame']-row['start_frame']
        for label,offset in (('first',0),('middle',count//2),('last',count-1)):
            st=(row['start_frame']+offset)/fps
            ot=(row['output_start_frame']+offset)/fps
            before=c.decode_frame(source,v['index'],st,ffmpeg)
            after=c.decode_frame(output,0,ot,ffmpeg)
            if not before or len(before)!=len(after):
                raise Error('Frame sample missing/dimensions changed.')
            mae=sum(abs(x-y) for x,y in zip(before,after))/len(before)
            if mae>16:
                raise Error('Source/output frame sample mismatch.')
            proof=root/('span-%04d-%s.jpg'%(i,label))
            c.run([ffmpeg,'-nostdin','-v','error','-n','-threads','1','-ss',str(ot),'-i',output,
                   '-map','0:v:0','-frames:v','1','-threads','1','-q:v','2','-update','1',proof])
            if not proof.is_file() or not proof.stat().st_size:
                raise Error('Missing proof image.')
            checks.append({'span':i,'boundary':label,'source_seconds':st,'output_seconds':ot,
                           'rgb_mae':mae,'proof':str(proof)})
    return checks


def execute(args):
    source=c.source_file(args.input)
    ffmpeg,ffprobe=c.executable(args.ffmpeg),c.executable(args.ffprobe)
    before=c.digest(source)
    data=c.probe(source,ffprobe)
    root=c.new_output(args.output,source,args.protect)
    if args.action=='probe':
        root.mkdir();c.save(root/'probe.json',{'status':'inspected','source_path':str(source),
                     'source_sha256':before,'metadata':data})
        if c.digest(source)!=before:raise Error('Source changed during probe.')
        print(root/'probe.json');return
    if not args.keep_list:raise Error('plan/render require --keep-list.')
    obj=load(args.keep_list)
    v,a=mapping(data,obj)
    fps,duration=c.compatible(data,v,a)
    if a and int(a['sample_rate']) not in {32000,44100,48000,88200,96000}:
        raise Error('Unreviewed AAC sample rate.')
    # Block unverified visual presentation metadata instead of silently discarding it.
    for s in data['streams']:
        if s is a and s.get('side_data_list'):
            raise Error('Audio side data requires an explicit retention design.')
    pts=c.frames(source,v['index'],ffprobe);c.check_cfr(pts,fps)
    if abs(len(pts)/fps-float(v['duration']))>1/fps:
        raise Error('Source decoded duration differs.')
    if a:
        c.check_audio_timeline(source,a['index'],ffprobe)
        if abs(float(a['duration'])-float(v['duration'])) > 1/int(a['sample_rate'])+.00001:
            raise Error('Original A/V durations differ; no silent truncation or padding.')
    plan=build_plan(obj,duration,fps,before,int(a['sample_rate']) if a else None)
    if not a and any(w['status']=='reviewed_transcript' for w in obj['coverage']['windows']):
        raise Error('No audio: transcript coverage cannot be claimed.')
    root.mkdir()
    global RUN_LOG
    RUN_LOG=root/'commands.jsonl'
    report={'schema_version':1,'status':'incomplete','source_path':str(source),'source_sha256':before,
            'source_metadata':data,'request':obj,'edit_map':plan,'selected_streams':{'video':v['index'],'audio':a['index'] if a else None},
            'tools':{n:c.run([x,'-version']).splitlines()[0] for n,x in [('ffmpeg',ffmpeg),('ffprobe',ffprobe)]},
            'dependency_sha256':c.digest(SIBLING),'human_listening':'not performed by helper',
            'limitations':'Objective sampled checks are not semantic review, exhaustive privacy clearance or perceptual lip sync.'}
    c.save(root/'manifest.incomplete.json',report)
    c.save(root/'edit-map.planned.json',{'source_sha256':before,**plan})
    # Energy check on full selected PCM in bounded batches; not speech detection.
    energies=[]
    if a:
        for row in plan['keep']:
            energy=0.;samples=0
            t=row['source_start']
            while t<row['source_end']-1e-7:
                length=min(30.,row['source_end']-t)
                vals=pcm(source,a['index'],ffmpeg,t,length)
                energy+=sum(x*x for x in vals);samples+=len(vals);t+=length
            rms=math.sqrt(energy/samples) if samples else 0
            if rms<=1e-5:raise Error('Silence-only/near-zero selected audio span; review explicitly, not empty-ASR inference.')
            energies.append(rms)
    report['selected_span_pcm_rms']=energies
    c.save(root/'selected-span-energy.json',{'pcm_rms':energies,'gate':'All selected audio spans RMS > 1e-5; not speech detection.'})
    if args.action=='plan':
        if c.digest(source)!=before:raise Error('Source changed.')
        report['status']='planned_not_rendered';c.save(root/'plan.json',report)
        print(root/'plan.json');return
    # Video-only reencoded parts with lossless PCM. No AAC per-part priming.
    parts=[]
    for i,row in enumerate(plan['keep'],1):
        path=root/('part-%04d.mov'%i)
        start,end=row['source_start'],row['source_end']
        cmd=common_input(ffmpeg,source)
        vf='trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS'%(row['start_frame'],row['end_frame'])
        cmd+=['-map','0:'+str(v['index']),'-vf',vf]
        if a:
            hz=int(a['sample_rate'])
            af='atrim=start_sample=%d:end_sample=%d,asetpts=PTS-STARTPTS'%(round(start*hz),round(end*hz))
            cmd+=['-map','0:'+str(a['index']),'-af',af]
        cmd+=encode_video_options()
        if a:cmd+=['-c:a','pcm_s24le','-ar',a['sample_rate']]
        cmd += [path]
        c.run(cmd)
        meta=c.probe(path,ffprobe)
        pv=c.select(meta,'video',None);pa=c.select(meta,'audio',None)
        pp=c.frames(path,pv['index'],ffprobe);c.check_cfr(pp,fps)
        if len(pp)!=row['end_frame']-row['start_frame'] or abs(float(pv['duration'])-(end-start))>.00001:
            raise Error('Intermediate exact video frame duration failed.')
        if a:
            c.check_audio_timeline(path,pa['index'],ffprobe)
            scan=json.loads(c.run([ffprobe,'-v','error','-protocol_whitelist','file,pipe',
                            '-select_streams',str(pa['index']),'-show_frames',
                            '-show_entries','frame=nb_samples','-of','json',path]))
            samples=sum(int(x['nb_samples']) for x in scan.get('frames',[]))
            expected=round((end-start)*int(a['sample_rate']))
            if samples!=expected or abs(float(pa['duration'])-(end-start))>1/int(a['sample_rate'])+.000002:
                raise Error('Intermediate PCM sample count/duration failed; no padding.')
            if any(pa.get(k)!=a.get(k) for k in ('sample_rate','channels','channel_layout')):
                raise Error('Intermediate original audio layout changed.')
        parts.append(path)
        c.save(root/('part-%04d-metadata.json'%i),meta)
        c.save(root/('part-%04d-verification.json'%i),{
            'video_frames':len(pp),'expected_video_frames':row['end_frame']-row['start_frame'],
            'audio_samples':samples if a else None,'expected_audio_samples':expected if a else None,
            'duration':end-start,'exact_count_gate':'passed'})
    listing='ffconcat version 1.0\n'+''.join("file '"+p.name+"'\nduration "+format(r['source_end']-r['source_start'],'.12f')+'\n' for p,r in zip(parts,plan['keep']))
    with (root/'parts.ffconcat').open('x',encoding='utf-8') as f:f.write(listing)
    output=root/'cleaned.mp4'
    cmd=[ffmpeg,'-nostdin','-v','error','-xerror','-n','-threads','1','-protocol_whitelist','file,pipe',
         '-f','concat','-safe','1','-i',root/'parts.ffconcat','-map','0:v:0']
    if a:cmd+=['-map','0:a:0']
    # Copy only the already accurately decoded/trimmed/reencoded video, not original keyframes.
    cmd+=['-map_metadata','-1','-map_chapters','-1','-c:v','copy']
    if a:cmd+=['-c:a','aac','-b:a','192k','-ar',a['sample_rate']]
    cmd+=['-movflags','+faststart',output]
    c.run(cmd)
    qa=c.verify(output,v,a,plan['output_duration'],fps,ffprobe,ffmpeg)
    if qa['video_frames']!=plan['output_frames']:
        raise Error('Joined exact frame count failed.')
    # Full decode scan covers all output A/V; sampled proofs cover both sides of EVERY join.
    qa['frame_comparisons']=proof_and_compare(source,v,output,plan['keep'],fps,ffmpeg,root)
    if a:
        qa['audio_comparisons']=compare_audio(source,a,output,plan['keep'],ffmpeg)
        qa['join_audio_comparisons']=compare_audio_joins(source,a,output,plan['keep'],ffmpeg)
        decoded=json.loads(c.run([ffprobe,'-v','error','-protocol_whitelist','file,pipe',
                           '-select_streams','a:0','-show_frames','-show_entries','frame=nb_samples','-of','json',output]))
        sample_count=sum(int(x['nb_samples']) for x in decoded.get('frames',[]))
        wanted=round(plan['output_duration']*int(a['sample_rate']))
        if not wanted <= sample_count < wanted+1024:
            raise Error('Final decoded audio sample count differs beyond one final AAC packet.')
        qa['decoded_audio_samples']=sample_count
        qa['expected_audio_samples']=wanted
    if c.digest(source)!=before:raise Error('Source changed; no complete report.')
    report.update(status='complete',source_hash_after=c.digest(source),source_hash_unchanged=True,
                  output={'path':str(output),'sha256':c.digest(output)},verification=qa)
    c.save(root/'edit-map.json',{'source_sha256':before,'output_sha256':report['output']['sha256'],**plan})
    c.save(root/'report.json',report)
    print('Complete joined cleaned MP4: '+str(output))


def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['probe','plan','render'])
    p.add_argument('--input',required=True)
    p.add_argument('--keep-list')
    p.add_argument('--output',required=True,help='NEW separate directory, existing parent')
    p.add_argument('--protect',action='append',default=[])
    p.add_argument('--ffmpeg',default='ffmpeg');p.add_argument('--ffprobe',default='ffprobe')
    return p

if __name__=='__main__':
    try:execute(parser().parse_args())
    except (Error,OSError,ValueError,KeyError,TypeError) as e:
        print('ERROR (private): '+str(e),file=sys.stderr);sys.exit(2)
