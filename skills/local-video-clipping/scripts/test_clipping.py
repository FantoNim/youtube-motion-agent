#!/usr/bin/env python3
"""Small real FFmpeg regression suite. Synthetic media only; persistent NEW evidence run."""
import argparse
from array import array
import copy
import json
import math
from pathlib import Path
import sys
import unittest
import clip_local as c

ROOT = None
FFMPEG = None
FFPROBE = None


def manifest(source, starts=(1.3, 36.7), **kw):
    obj = {'schema_version':1,'source_sha256':c.digest(source),'requested_count':len(starts),
           'selection_basis':'Synthetic test windows, NOT AI highlights.',
           'coverage':'Synthetic test generator defines full 0..70s timeline; no speech present.',
           'clips':[{'start':t,'title':'Synthetic interval '+str(i),'reason':'Exercise non-keyframe exact seek',
                     'evidence':'Generated moving test pattern and unique chirp, fixture definition in test_clipping.py'}
                    for i,t in enumerate(starts)]}
    obj.update(kw)
    return obj


def cli(source, obj, out, action='render', ok=True):
    mp = ROOT/(out+'-request.json')
    c.save(mp,obj)
    cmd=[sys.executable,'-B',str(Path(c.__file__)),action,'--input',str(source),
         '--manifest',str(mp),'--output',str(ROOT/out)]
    import subprocess
    p=subprocess.run(cmd,capture_output=True,text=True,shell=False)
    (ROOT/(out+'-command.txt')).write_text(json.dumps(cmd)+'\n'+p.stdout+'\n'+p.stderr,encoding='utf-8')
    if ok:
        if p.returncode:
            raise AssertionError(p.stderr)
        return json.loads((ROOT/out/('report.json' if action=='render' else 'plan.json')).read_text(encoding='utf-8'))
    if p.returncode == 0 or (ROOT/out/'report.json').exists():
        raise AssertionError('Invalid request was accepted.')
    return p.stderr


def fixture(path, duration=70, audio=True, multi=False, vf=None, offset=None, fps='10'):
    cmd=[FFMPEG,'-nostdin','-v','error','-n','-threads','1','-f','lavfi','-i',
         'testsrc2=size=160x90:rate='+fps+':duration='+str(duration)]
    if audio:
        # Non-periodic frequency sweep: source position is objectively distinguishable.
        cmd += ['-f','lavfi','-i','aevalsrc=0.15*sin(2*PI*(220*t+3*t*t)):s=48000:d='+str(duration)]
    if multi:
        cmd += ['-f','lavfi','-i','sine=frequency=1200:sample_rate=48000:duration='+str(duration)]
    cmd += ['-map','0:v:0']
    if audio:
        cmd += ['-map','1:a:0']
    if multi:
        cmd += ['-map','2:a:0']
    if vf:
        cmd += ['-vf',vf,'-fps_mode','vfr']
    cmd += ['-c:v','libx264','-threads','1','-pix_fmt','yuv420p','-g','100','-keyint_min','100','-sc_threshold','0']
    if audio:
        cmd += ['-c:a','aac','-b:a','128k']
    if offset is not None:
        cmd += ['-output_ts_offset',str(offset)]
    cmd += [str(path)]
    c.run(cmd)


def pcm(path, stream, start):
    data=c.run([FFMPEG,'-nostdin','-v','error','-threads','1','-protocol_whitelist','file,pipe',
                '-ss',str(start),'-i',path,'-map','0:'+str(stream),'-t','0.25','-ac','1',
                '-ar','48000','-f','f32le','pipe:1'],binary=True)
    out=array('f')
    out.frombytes(data)
    return out


def correlation(a,b):
    n=min(len(a),len(b))
    return sum(a[i]*b[i] for i in range(n))/math.sqrt(sum(a[i]**2 for i in range(n))*sum(b[i]**2 for i in range(n)))


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (ROOT/'sources').mkdir()
        cls.source=ROOT/'sources'/'video spaces & ; name.mp4'
        fixture(cls.source)
        cls.hash=c.digest(cls.source)

    def test_01_explicit_user_30s_two_clips_and_unique_timeline(self):
        # Historical accuracy fixture: user explicitly requests 30 seconds, never default.
        report=cli(self.source,manifest(self.source,duration_seconds=30),'explicit-30s-two')
        self.assertEqual(report['status'],'complete')
        self.assertEqual(len(report['clips']),2)
        self.assertEqual(report['source_sha256'],c.digest(self.source))
        evidence=[]
        for item,start in zip(report['clips'],(1.3,36.7)):
            self.assertEqual(item['verification']['video_frames'],300)
            clip=Path(item['file'])
            for t in (.2,15.1,29.5):
                good=correlation(pcm(self.source,1,start+t),pcm(clip,1,t))
                wrong=correlation(pcm(self.source,1,start+t+1),pcm(clip,1,t))
                self.assertGreater(good,.96)
                self.assertGreater(good-abs(wrong),.7)
                evidence.append({'clip':clip.name,'output_seconds':t,'source_seconds':start+t,
                                 'pcm_correlation_correct':good,'pcm_correlation_wrong_plus_1s':wrong})
            # Moving testsrc2 also distinguishes the correct frame from a one-second error.
            correct=c.decode_frame(self.source,0,start,FFMPEG)
            wrong=c.decode_frame(self.source,0,start+1,FFMPEG)
            actual=c.decode_frame(clip,0,0,FFMPEG)
            mae=lambda x,y:sum(abs(a-b) for a,b in zip(x,y))/len(x)
            self.assertLess(mae(correct,actual),mae(wrong,actual)/3)
        c.save(ROOT/'timeline-evidence.json',evidence)
        # First seek is not a keyframe (keyframes every 10 seconds).
        self.assertEqual(c.digest(self.source),self.hash)

    def test_02_custom_and_explicit_ranges(self):
        r=cli(self.source,manifest(self.source,(2.1,),duration_seconds=2.4),'custom-duration')
        self.assertEqual(r['clips'][0]['verification']['video_frames'],24)
        obj=manifest(self.source,(5.3,9.1),explicit_ranges=True,range_authorization='Synthetic user requested exact 5.3..6.5 and 9.1..11.2')
        obj['clips'][0]['end']=6.5
        obj['clips'][1]['end']=11.2
        r=cli(self.source,obj,'explicit-ranges')
        self.assertEqual([x['verification']['video_frames'] for x in r['clips']],[12,21])

    def test_03_no_audio(self):
        source=ROOT/'sources'/'silent.mp4'
        fixture(source,4,audio=False)
        r=cli(source,manifest(source,(.3,),duration_seconds=2),'no-audio')
        self.assertEqual(len(r['clips'][0]['verification']['metadata']['streams']),1)

    def test_04_ambiguous_audio(self):
        source=ROOT/'sources'/'two tracks.mp4'
        fixture(source,4,multi=True)
        obj=manifest(source,(.3,),duration_seconds=2)
        self.assertIn('Ambiguous',cli(source,obj,'ambiguous-rejected',ok=False))
        obj.update(audio_stream=2,mapping_reason='Synthetic test explicitly selects second 1200Hz track; first not wanted.')
        r=cli(source,obj,'mapped-second')
        self.assertEqual(r['selected_stream_indexes']['audio'],2)
        self.assertGreater(correlation(pcm(source,2,.7),pcm(Path(r['clips'][0]['file']),1,.4)),.96)

    def test_05_plan_and_rejections(self):
        r=cli(self.source,manifest(self.source,duration_seconds=30),'plan-only',action='plan')
        self.assertEqual(r['status'],'planned_not_rendered')
        self.assertFalse((ROOT/'plan-only'/'report.json').exists())
        variants=[]
        base=manifest(self.source,duration_seconds=30)
        obj=copy.deepcopy(base);obj['requested_count']=3;variants.append(obj)
        obj=manifest(self.source,(1,31,61),duration_seconds=30);variants.append(obj)
        obj=manifest(self.source,(1,20),duration_seconds=30);variants.append(obj)
        obj=manifest(self.source,(1,1),duration_seconds=30,allow_overlap=True,overlap_reason='test authorized');variants.append(obj)
        for start in (-1,float('nan'),float('inf'),69):
            obj=manifest(self.source,(start,),duration_seconds=30);variants.append(obj)
        obj=manifest(self.source,(1.35,),duration_seconds=30);variants.append(obj)
        obj=manifest(self.source,(1,),duration_seconds=0);variants.append(obj)
        for i,obj in enumerate(variants):
            with self.subTest(i=i):
                with self.assertRaises(c.ClipError):c.plan(obj,70,10,self.hash)
        obj=manifest(self.source,(1,20),duration_seconds=30,allow_overlap=True,overlap_reason='Synthetic authorized overlap')
        self.assertEqual(len(c.plan(obj,70,10,self.hash)),2)
        obj=manifest(self.source);obj['ffmpeg_args']=['-y']
        c.save(ROOT/'arbitrary-options.json',obj)
        with self.assertRaises(c.ClipError):c.load_manifest(ROOT/'arbitrary-options.json')
        (ROOT/'nonfinite.json').write_text('{"start":NaN}',encoding='utf-8')
        with self.assertRaises((c.ClipError,ValueError)):c.load_manifest(ROOT/'nonfinite.json')

    def test_06_paths_and_sources(self):
        with self.assertRaises(c.ClipError):c.new_output(ROOT/'explicit-30s-two',self.source)
        with self.assertRaises(c.ClipError):c.new_output(self.source.parent/'bad',self.source)
        with self.assertRaises(c.ClipError):c.new_output(ROOT/'x'/'..'/'sources'/'bad',self.source)
        with self.assertRaises(c.ClipError):c.new_output(c.SKILL/'bad',self.source)
        cache=ROOT/'cached-assets';cache.mkdir()
        with self.assertRaises(c.ClipError):c.new_output(cache/'bad',self.source,[cache])
        for x in ('https://example.test/video.mp4','file:///video.mp4','playlist.m3u8'):
            with self.assertRaises((c.ClipError,OSError)):c.source_file(x)
        try:
            (ROOT/'redirect').symlink_to(self.source.parent,target_is_directory=True)
        except OSError as e:
            (ROOT/'symlink-test.txt').write_text('OS denied symlink creation; skipped actual redirect case. '+str(e),encoding='utf-8')
        else:
            with self.assertRaises(c.ClipError):c.new_output(ROOT/'redirect'/'bad',self.source)
            (ROOT/'symlink-test.txt').write_text('Actual symlink-parent source confinement passed.',encoding='utf-8')
        with self.assertRaises(c.ClipError):c.executable('nonexistent-local-video-executable-12345')

    def test_07_fractional_cadence(self):
        source=ROOT/'sources'/'fractional.mp4'
        fixture(source,32,fps='30000/1001')
        start=3*1001/30000
        r=cli(source,manifest(source,(start,),duration_seconds=30),'fractional-explicit-30s')
        qa=r['clips'][0]['verification']
        self.assertEqual(qa['video_frames'],900)
        self.assertEqual(qa['metadata']['streams'][0]['avg_frame_rate'],'30000/1001')

    def test_08_real_vfr_and_offsets_blocked(self):
        vfr=ROOT/'sources'/'vfr.mp4'
        fixture(vfr,4,audio=False,vf="select='not(eq(mod(n,3),1))'")
        error=cli(vfr,manifest(vfr,(0,),duration_seconds=1),'vfr-rejected',ok=False)
        self.assertIn('VFR',error)
        offset=ROOT/'sources'/'offset.mp4'
        fixture(offset,4,offset=2)
        error=cli(offset,manifest(offset,(0,),duration_seconds=1),'offset-rejected',ok=False)
        self.assertIn('offset',error)

    def test_09_interlaced_and_unknown_field_order_blocked(self):
        source=ROOT/'sources'/'interlaced.mp4'
        c.run([FFMPEG,'-nostdin','-v','error','-n','-f','lavfi','-i',
               'testsrc2=size=160x96:rate=50:duration=4','-vf','tinterlace=interleave_top',
               '-c:v','libx264','-threads','1','-flags','+ilme+ildct','-x264-params','tff=1',source])
        data=c.probe(source,FFPROBE)
        video=c.select(data,'video',None)
        self.assertEqual(video['field_order'],'tt')
        source_hash=c.digest(source)
        error=cli(source,manifest(source,(.4,),duration_seconds=2),'interlaced-rejected',ok=False)
        self.assertIn('field order',error)
        self.assertFalse((ROOT/'interlaced-rejected').exists())
        self.assertEqual(c.digest(source),source_hash)
        c.save(ROOT/'interlacing-evidence.json',{'source_metadata':data,
               'source_hash_unchanged':True,'rejection':error,'output_directory_created':False})
        # Missing/unknown and every nonprogressive field order must fail closed.
        progressive=c.probe(self.source,FFPROBE)
        v=c.select(progressive,'video',None)
        a=c.select(progressive,'audio',None)
        self.assertEqual(v['field_order'],'progressive')
        for field_order in (None,'unknown','tt','bb','tb','bt'):
            bad=copy.deepcopy(v)
            if field_order is None:
                bad.pop('field_order',None)
            else:
                bad['field_order']=field_order
            with self.subTest(field_order=field_order):
                with self.assertRaisesRegex(c.ClipError,'field order'):
                    c.compatible(progressive,bad,a)
        # Actual output metadata must also be progressive, not merely source-compatible.
        from unittest.mock import patch
        output=Path(json.loads((ROOT/'explicit-30s-two'/'report.json').read_text())['clips'][0]['file'])
        metadata=c.probe(output,FFPROBE)
        for field_order in (None,'unknown','tt'):
            bad=copy.deepcopy(metadata)
            ov=c.select(bad,'video',None)
            if field_order is None:
                ov.pop('field_order',None)
            else:
                ov['field_order']=field_order
            with self.subTest(output_field_order=field_order):
                with patch.object(c,'probe',return_value=bad):
                    with self.assertRaisesRegex(c.ClipError,'field order'):
                        c.verify(output,v,a,30,10,FFPROBE,FFMPEG)


    def test_10_thought_led_variable_ranges_render(self):
        # Mock labels/ranges test the contract, NOT semantic idea detection.
        starts=(1.3,18.7,44.1)
        ends=(6.5,29.8,61.4)
        obj=manifest(self.source,starts,length_mode='thought_led')
        for row,end in zip(obj['clips'],ends):
            row['end']=end
            row['reason']='Distinct synthetic interval for per-clip timing QA; not a claimed natural thought.'
        self.assertNotIn('duration_seconds',obj)
        self.assertNotIn('explicit_ranges',obj)
        planned=c.plan(obj,70,10,self.hash)
        inferred=copy.deepcopy(obj);inferred.pop('length_mode')
        self.assertEqual(c.plan(inferred,70,10,self.hash),planned)
        report=cli(self.source,obj,'thought-led-variable-three')
        self.assertEqual(report['status'],'complete')
        self.assertEqual(len(report['clips']),3)
        self.assertEqual(len({x['sha256'] for x in report['clips']}),3)
        self.assertTrue(report['source_hash_unchanged'])
        self.assertEqual(report['source_hash_after'],self.hash)
        previous_end=0
        evidence=[]
        for item,start,end in zip(report['clips'],starts,ends):
            length=end-start
            self.assertEqual(item['selection']['start'],start)
            self.assertEqual(item['selection']['end'],end)
            self.assertGreaterEqual(start,previous_end)
            previous_end=end
            qa=item['verification']
            self.assertEqual(qa['video_frames'],round(length*10))
            self.assertEqual(qa['full_decode'],'passed')
            self.assertEqual(len(qa['sampled_source_frame_comparison']),3)
            self.assertEqual(len(qa['sampled_source_audio_comparison']),3)
            v,a=qa['metadata']['streams']
            self.assertAlmostEqual(float(v['duration']),length,places=4)
            self.assertLessEqual(abs(float(a['duration'])-length),qa['audio_packet_tolerance_seconds'])
            self.assertEqual(v['field_order'],'progressive')
            self.assertEqual(v['avg_frame_rate'],'10/1')
            self.assertEqual((v['width'],v['height']),(160,90))
            self.assertEqual(a['sample_rate'],'48000')
            clip=Path(item['file'])
            self.assertEqual(c.digest(clip),item['sha256'])
            for t in (.2,length/2,length-.5):
                good=correlation(pcm(self.source,1,start+t),pcm(clip,1,t))
                wrong=correlation(pcm(self.source,1,start+t+1),pcm(clip,1,t))
                self.assertGreater(good,.96)
                self.assertGreater(good-abs(wrong),.7)
                evidence.append({'clip':clip.name,'length':length,'output_seconds':t,
                                 'source_seconds':start+t,'correct_correlation':good,'wrong_plus_1s':wrong})
            self.assertEqual(len(item['proofs']),3)
            self.assertTrue(all(Path(p['path']).stat().st_size for p in item['proofs']))
        self.assertEqual(c.digest(self.source),self.hash)
        c.save(ROOT/'variable-timeline-evidence.json',evidence)

    def test_11_incomplete_untimed_plan_and_range_guards(self):
        obj=manifest(self.source,(1.3,))
        with self.assertRaisesRegex(c.ClipError,'Incomplete plan.*No implicit fixed duration'):
            c.plan(obj,70,10,self.hash)
        error=cli(self.source,obj,'untimed-missing-end-rejected',action='plan',ok=False)
        self.assertIn('Incomplete plan',error)
        self.assertFalse((ROOT/'untimed-missing-end-rejected').exists())
        obj['clips'][0]['end']=6.5
        rows=c.plan(obj,70,10,self.hash)
        self.assertAlmostEqual(rows[0]['end']-rows[0]['start'],5.2)
        for mutate in ('count','duplicate','overlap','bounds','missing-end','nonfinite','bool','evidence'):
            bad=copy.deepcopy(obj)
            if mutate=='count':bad['requested_count']=2
            elif mutate=='duplicate':
                bad['clips']*=2;bad.update(requested_count=2,allow_overlap=True,overlap_reason='Synthetic authorization')
            elif mutate=='overlap':
                bad['clips'].append(dict(bad['clips'][0],start=2,end=8));bad['requested_count']=2
            elif mutate=='bounds':bad['clips'][0]['end']=71
            elif mutate=='missing-end':bad['clips'][0].pop('end')
            elif mutate=='nonfinite':bad['clips'][0]['end']=float('nan')
            elif mutate=='bool':bad['clips'][0]['end']=True
            else:bad['clips'][0]['evidence']=''
            with self.subTest(mutate=mutate):
                with self.assertRaises(c.ClipError):c.plan(bad,70,10,self.hash)

    def test_12_explicit_constraint_precedence_and_modes(self):
        obj=manifest(self.source,(1.3,),duration_seconds=2.4)
        self.assertAlmostEqual(c.plan(obj,70,10,self.hash)[0]['end'],3.7)
        obj['clips'][0]['end']=6.5
        with self.assertRaisesRegex(c.ClipError,'fixed duration differs'):
            c.plan(obj,70,10,self.hash)
        obj['length_mode']='thought_led'
        with self.assertRaisesRegex(c.ClipError,'conflicts'):
            c.plan(obj,70,10,self.hash)
        obj['length_mode']='fixed';obj['clips'][0]['end']=3.7
        self.assertEqual(len(c.plan(obj,70,10,self.hash)),1)
        for mode in ('user_ranges','unknown',True,{}):
            bad=copy.deepcopy(obj);bad['length_mode']=mode
            with self.subTest(mode=mode):
                with self.assertRaises(c.ClipError):c.plan(bad,70,10,self.hash)
        # Legacy actual user ranges override duration, as before; never use this for editorial windows.
        obj=manifest(self.source,(1.3,),duration_seconds=2.4,explicit_ranges=True,
                     range_authorization='Synthetic user supplied exact 1.3..6.5 range')
        obj['clips'][0]['end']=6.5
        self.assertEqual(c.plan(obj,70,10,self.hash)[0]['end'],6.5)
        obj['length_mode']='user_ranges'
        self.assertEqual(len(c.plan(obj,70,10,self.hash)),1)
        obj.pop('range_authorization')
        with self.assertRaisesRegex(c.ClipError,'authorization'):
            c.plan(obj,70,10,self.hash)
        for mode in ('fixed','user_ranges'):
            bad=manifest(self.source,(1.3,),length_mode=mode)
            bad['clips'][0]['end']=6.5
            with self.assertRaisesRegex(c.ClipError,'conflicts'):
                c.plan(bad,70,10,self.hash)
        bad=manifest(self.source,(1,40),duration_seconds=41)
        with self.assertRaisesRegex(c.ClipError,'2 clips of 41 seconds'):
            c.plan(bad,70,10,self.hash)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',required=True,help='NEW evidence directory under Videos/_tests/local-video-clipping')
    args=p.parse_args()
    ROOT=Path(args.output).resolve()
    allowed=Path(__file__).resolve().parents[3]/'Videos'/'_tests'/'local-video-clipping'
    if not c.within(ROOT,allowed) or ROOT == allowed or ROOT.exists():
        p.error('Choose a NEW child of Videos/_tests/local-video-clipping')
    ROOT.mkdir(parents=True)
    FFMPEG=c.executable('ffmpeg');FFPROBE=c.executable('ffprobe')
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    c.save(ROOT/'test-summary.json',{'tests':result.testsRun,'failures':len(result.failures),
           'errors':len(result.errors),'skipped':len(result.skipped),'success':result.wasSuccessful(),
           'tool_version':c.run([FFMPEG,'-version']).splitlines()[0],
           'human_playback':'not performed; synthetic objective verification only'})
    sys.exit(0 if result.wasSuccessful() else 1)
