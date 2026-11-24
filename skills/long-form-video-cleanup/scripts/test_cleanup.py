#!/usr/bin/env python3
"""Synthetic only. Persistent evidence, no downloads, models, user recordings or listening."""
import argparse
import copy
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
import cleanup_local as m

ROOT=None
FFMPEG=None
FFPROBE=None


def row(start,end):
    return dict(start=start,end=end,reason='Synthetic fixture execution test, not semantic editing.',
                transcript_evidence='test_cleanup.py generator: no speech. Unique chirp defines source clock.',
                boundary_review='Synthetic mathematical boundaries; no human listening claimed.')


def request(source,duration=8,fps=10,audio=True,ranges=((.13,1.94),(2.53,4.14),(5.13,7.04))):
    keeps=[row(s,e) for s,e in ranges]
    gaps=[];prev=0.
    for s,e in ranges:
        qs=int(s*fps+.5)/fps;qe=int(e*fps+.5)/fps
        if qs>prev+1e-7:gaps.append(row(prev,qs))
        prev=qe
    if prev<duration-1e-7:gaps.append(row(prev,duration))
    return dict(schema_version=1,source_sha256=m.c.digest(source),video_stream=0,
                audio_stream=1 if audio else None,mapping_reason='Retain all original synthetic A/V streams.',
                selection_basis='Synthetic integration ranges, NOT autonomous repeated-take decisions.',
                limitations='No ASR, speech, real user recording, privacy review or human listening tested.',
                quantization='nearest_frame_reviewed',coverage=dict(duration=duration,
                basis='Full synthetic fixture generator defines timeline.',windows=[dict(start=0,end=duration,
                status='synthetic_fixture',evidence='test_cleanup.py fixture generator',timing_uncertainty_seconds=0)]),
                keep=keeps,deletions=gaps)


def fixture(path,duration=8,fps='10',audio=True,stereo=False,multi=False,silent=False,vfr=False,offset=False):
    cmd=[FFMPEG,'-nostdin','-v','error','-n','-f','lavfi','-i',
         'testsrc2=size=160x90:rate='+fps+':duration='+str(duration)]
    if audio:
        expr='0' if silent else '0.15*sin(2*PI*(190*t+17*t*t))'
        if stereo:expr+='|0.12*sin(2*PI*(410*t+11*t*t))'
        cmd+=['-f','lavfi','-i','aevalsrc='+expr+':s=48000:d='+str(duration)]
    if multi:cmd+=['-f','lavfi','-i','sine=frequency=1000:sample_rate=48000:duration='+str(duration)]
    cmd+=['-map','0:v:0']
    if audio:cmd+=['-map','1:a:0']
    if multi:cmd+=['-map','2:a:0']
    if vfr:cmd+=['-vf',"select='not(eq(mod(n,3),1))'",'-fps_mode','vfr']
    cmd+=['-c:v','libx264','-threads','1','-pix_fmt','yuv420p','-g','100','-sc_threshold','0']
    if audio:cmd+=['-c:a','aac','-b:a','192k']
    if offset:cmd+=['-output_ts_offset','2']
    m.c.run(cmd+[path])


def cli(source,obj,name,action='render',ok=True):
    tag='-retry' if (ROOT/(name+'-request.json')).exists() else ''
    manifest=ROOT/(name+tag+'-request.json');m.c.save(manifest,obj)
    cmd=[sys.executable,'-B',str(Path(m.__file__)),action,'--input',str(source),
         '--keep-list',str(manifest),'--output',str(ROOT/name)]
    p=subprocess.run(cmd,shell=False,capture_output=True,text=True)
    (ROOT/(name+tag+'-command.txt')).write_text(json.dumps(cmd)+'\n'+p.stdout+'\n'+p.stderr,encoding='utf-8')
    if ok:
        if p.returncode:raise AssertionError(p.stderr)
        return json.loads((ROOT/name/('report.json' if action=='render' else 'plan.json')).read_text())
    if p.returncode==0 or (ROOT/name/'report.json').exists():raise AssertionError('Invalid accepted.')
    return p.stderr


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (ROOT/'sources').mkdir()
        cls.source=ROOT/'sources'/'test spaces & ; camera.mp4'
        fixture(cls.source,stereo=True)
        cls.hash=m.c.digest(cls.source)

    def test_01_three_spans_two_joins_stereo(self):
        report=cli(self.source,request(self.source),'joined-smoke')
        self.assertEqual(report['status'],'complete')
        self.assertEqual(report['verification']['video_frames'],53)
        self.assertEqual(report['verification']['full_decode'],'passed')
        self.assertEqual(report['source_hash_after'],self.hash)
        self.assertEqual(len(report['verification']['frame_comparisons']),9)
        self.assertEqual(len(report['verification']['audio_comparisons']),9)
        self.assertEqual(len(report['verification']['join_audio_comparisons']),4)
        self.assertGreater(min(x['pcm_correlation'] for x in report['verification']['join_audio_comparisons']),.9)
        self.assertEqual(report['verification']['expected_audio_samples'],254400)
        self.assertGreater(min(x['pcm_correlation'] for x in report['verification']['audio_comparisons']),.95)
        self.assertEqual(report['verification']['metadata']['streams'][1]['channels'],2)
        self.assertAlmostEqual(report['edit_map']['keep'][0]['start_delta_seconds'],-.03)
        self.assertTrue((ROOT/'joined-smoke'/'edit-map.json').is_file())
        # Deliberately WRONG source clock must not match the unique chirp.
        output=Path(report['output']['path'])
        before=m.pcm(self.source,1,FFMPEG,.7,.1);actual=m.pcm(output,1,FFMPEG,.6,.1)
        wrong=m.pcm(self.source,1,FFMPEG,1.7,.1)
        corr=lambda x,y:sum(a*b for a,b in zip(x,y))/(sum(a*a for a in x)*sum(b*b for b in y))**.5
        good=corr(before,actual);bad=corr(wrong,actual)
        self.assertGreater(good,.95);self.assertLess(abs(bad),.2)
        m.c.save(ROOT/'independent-timeline-check.json',dict(correct_correlation=good,wrong_plus_one_second=bad))

    def test_02_plan_probe_and_no_overwrite(self):
        obj=request(self.source)
        r=cli(self.source,obj,'plan-only',action='plan')
        self.assertEqual(r['status'],'planned_not_rendered')
        self.assertFalse((ROOT/'plan-only'/'cleaned.mp4').exists())
        self.assertIn('NEW',cli(self.source,obj,'plan-only',ok=False))
        p=subprocess.run([sys.executable,'-B',str(Path(m.__file__)),'probe','--input',str(self.source),
                          '--output',str(ROOT/'probe-only')],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(json.loads((ROOT/'probe-only'/'probe.json').read_text())['source_sha256'],self.hash)

    def test_03_invalid_keep_and_deletion_cases(self):
        base=request(self.source)
        mutations={
            'empty':lambda o:o.update(keep=[]),
            'tiny':lambda o:o['keep'][0].update(end=.14),
            'negative':lambda o:o['keep'][0].update(start=-1),
            'out_of_range':lambda o:o['keep'][-1].update(end=9),
            'overlap':lambda o:o['keep'][1].update(start=1),
            'unordered':lambda o:o['keep'].reverse(),
            'duplicate':lambda o:o['keep'].insert(1,copy.deepcopy(o['keep'][0])),
            'bool':lambda o:o['keep'][0].update(start=True),
            'nan':lambda o:o['keep'][0].update(start=float('nan')),
            'missing_evidence':lambda o:o['keep'][0].update(transcript_evidence=''),
            'wrong_hash':lambda o:o.update(source_sha256='0'*64),
            'unknown_field':lambda o:o.update(ffmpeg_args=['-y']),
            'missing_deletion':lambda o:o['deletions'].pop(),
            'wrong_deletion':lambda o:o['deletions'][0].update(end=.2),
            'unreviewed_quantization':lambda o:o.update(quantization='auto')}
        outcomes=[]
        for name,mutate in mutations.items():
            bad=copy.deepcopy(base);mutate(bad)
            with self.subTest(case=name):
                with self.assertRaises(m.Error):m.build_plan(bad,8,10,self.hash,48000)
            outcomes.append(name)
        m.c.save(ROOT/'rejected-plan-cases.json',outcomes)

    def test_04_coverage_failures(self):
        base=request(self.source)
        for name in ('failed','gap','incomplete','uncertain','empty'):
            bad=copy.deepcopy(base);w=bad['coverage']['windows'][0]
            if name=='failed':w['status']='asr_failed'
            elif name=='gap':w['start']=1
            elif name=='incomplete':w['end']=7
            elif name=='uncertain':w['timing_uncertainty_seconds']=-1
            else:bad['coverage']['windows']=[]
            with self.subTest(name=name):
                with self.assertRaises(m.Error):m.build_plan(bad,8,10,self.hash,48000)
        base['coverage']['windows']=[dict(base['coverage']['windows'][0],end=4.1),
                                     dict(base['coverage']['windows'][0],start=3.9)]
        self.assertEqual(m.build_plan(base,8,10,self.hash,48000)['output_frames'],53)

    def test_05_path_confinement(self):
        for path in (self.source.parent/'bad',ROOT/'x'/'..'/'bad',m.SKILL/'bad',ROOT/'models'/'bad'):
            with self.subTest(path=str(path)):
                with self.assertRaises(m.Error):m.c.new_output(path,self.source)
        model=ROOT/'nonstandard-cache';model.mkdir()
        with self.assertRaises(m.Error):m.c.new_output(model/'bad',self.source,[model])
        try:(ROOT/'redirect').symlink_to(self.source.parent,target_is_directory=True)
        except OSError as e:
            (ROOT/'symlink-status.txt').write_text('SKIPPED OS disallows symlink creation: '+str(e))
        else:
            with self.assertRaises(m.Error):m.c.new_output(ROOT/'redirect'/'bad',self.source)
            (ROOT/'symlink-status.txt').write_text('PASS actual symlink-parent confinement')
        with self.assertRaises(m.Error):m.c.source_file('https://example.test/private.mp4')

    def test_06_multiple_streams_rejected(self):
        source=ROOT/'sources'/'multi.mp4';fixture(source,multi=True)
        self.assertIn('Multiple',cli(source,request(source),'multi-rejected',ok=False))
        data=m.c.probe(self.source,FFPROBE)
        for stream in ({'index':3,'codec_type':'subtitle'},dict(data['streams'][0],index=3)):
            bad=copy.deepcopy(data);bad['streams'].append(stream)
            with self.assertRaises(m.Error):m.mapping(bad,request(self.source))

    def test_07_no_audio_stays_no_audio(self):
        source=ROOT/'sources'/'no-audio.mp4';fixture(source,audio=False)
        r=cli(source,request(source,audio=False),'no-audio-render')
        self.assertEqual(len(r['verification']['metadata']['streams']),1)
        self.assertNotIn('audio_comparisons',r['verification'])

    def test_08_silence_only_rejected(self):
        source=ROOT/'sources'/'silence.mp4';fixture(source,silent=True)
        self.assertIn('Silence-only',cli(source,request(source),'silence-rejected',ok=False))
        with self.assertRaises(m.Error):m.check_energy([0.]*10)
        self.assertGreater(m.check_energy([.1]*10),.09)

    def test_09_actual_vfr_offset_blocked(self):
        for name,kw,text in (('vfr',dict(vfr=True,audio=False),'VFR'),('offset',dict(offset=True),'offset')):
            source=ROOT/'sources'/(name+'.mp4');fixture(source,**kw)
            err=cli(source,request(source,audio=kw.get('audio',True)),name+'-rejected',ok=False)
            self.assertIn(text,err)

    def test_10_fractional_cadence_multiple_joins(self):
        source=ROOT/'sources'/'fractional.mp4'
        # 240 frames at 30000/1001 = 8.008s; use 5-frame lattice for exact 48k audio samples.
        fixture(source,duration=8.008,fps='30000/1001')
        fps=30000/1001
        ranges=[(s/fps+.001,e/fps-.001) for s,e in ((5,50),(70,120),(150,225))]
        obj=request(source,duration=8.008,fps=fps,ranges=ranges)
        r=cli(source,obj,'fractional-joined')
        self.assertEqual(r['verification']['video_frames'],170)
        self.assertEqual(r['verification']['metadata']['streams'][0]['avg_frame_rate'],'30000/1001')
        self.assertGreater(min(x['pcm_correlation'] for x in r['verification']['audio_comparisons']),.95)
        bad=request(source,duration=8.008,fps=fps,ranges=((1/fps,50/fps),))
        with self.assertRaisesRegex(m.Error,'lattice'):m.build_plan(bad,8.008,fps,m.c.digest(source),48000)

    def test_11_metadata_blockers(self):
        data=m.c.probe(self.source,FFPROBE);v=data['streams'][0];a=data['streams'][1]
        for fields in ({'field_order':'unknown'},{'field_order':'tt'},{'color_transfer':'smpte2084'},
                       {'color_range':'pc'},{'side_data_list':[{'rotation':90}]},{'pix_fmt':'yuv420p10le'},
                       {'start_time':'2'}):
            bad=dict(v,**fields)
            with self.subTest(fields=fields):
                with self.assertRaises(m.Error):m.c.compatible(data,bad,a)

    def test_13_audio_visual_only_coverage_gate(self):
        bad=request(self.source)
        bad['coverage']['windows'][0]['status']='reviewed_visual_only'
        with self.assertRaisesRegex(m.Error,'Audio present: reviewed_visual_only'):
            m.build_plan(bad,8,10,self.hash,48000)
        outcomes={}
        for action in ('plan','render'):
            name='av-visual-only-'+action+'-rejected'
            outcomes[action]=cli(self.source,bad,name,action=action,ok=False)
            self.assertIn('Audio present: reviewed_visual_only',outcomes[action])
            self.assertFalse((ROOT/name).exists())
        self.assertEqual(m.c.digest(self.source),self.hash)
        source=ROOT/'sources'/'visual-only-no-audio.mp4'
        fixture(source,audio=False)
        visual=request(source,audio=False)
        visual['coverage']['windows'][0].update(status='reviewed_visual_only',
            evidence='Synthetic generated no-audio fixture; visual-only branch test, not real footage review.')
        plan=cli(source,visual,'no-audio-visual-only-plan',action='plan')
        self.assertEqual(plan['status'],'planned_not_rendered')
        self.assertIsNone(plan['selected_streams']['audio'])
        self.assertEqual(m.c.digest(source),visual['source_sha256'])
        m.c.save(ROOT/'visual-only-coverage-regression.json',dict(
            audio_plan_rejected_before_output=True,audio_render_rejected_before_output=True,
            no_audio_visual_plan_accepted=True,audio_source_hash_unchanged=True,
            no_audio_source_hash_unchanged=True,diagnostics=outcomes,
            note='Synthetic fixtures only; no listening/semantic/real-media claim.'))

    def test_12_json_parser_and_resources(self):
        for name,content in (('duplicate','{"keep":[],"keep":[]}'),('nan','{"keep":NaN}'),('array','[]')):
            path=ROOT/(name+'.json');path.write_text(content)
            with self.assertRaises((m.Error,ValueError)):m.load(path)
        good=ROOT/'parse-good.json';m.c.save(good,request(self.source));self.assertEqual(m.load(good)['schema_version'],1)
        links=0
        for path in m.SKILL.rglob('*.md'):
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
                if '://' in target or target.startswith('#'):continue
                self.assertTrue((path.parent/target.split('#')[0]).resolve().is_file(),(path,target));links+=1
        example=json.loads((m.SKILL/'assets'/'keep-list.example.json').read_text())
        self.assertEqual(example['schema_version'],1)
        m.c.save(ROOT/'resource-check.json',dict(local_markdown_links=links,example_json='parsed'))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True)
    p.add_argument('--test',choices=sorted(x for x in dir(Tests) if x.startswith('test_')),
                   help='Run one focused method in a NEW evidence directory; default runs full suite.')
    args=p.parse_args()
    ROOT=Path(args.output).resolve();allowed=m.SKILL.parents[1]/'Videos'/'_tests'/'long-form-video-cleanup'
    if '..' in Path(args.output).parts or not m.c.within(ROOT,allowed) or ROOT==allowed or ROOT.exists():
        p.error('Choose NEW child of Videos/_tests/long-form-video-cleanup.')
    ROOT.mkdir(parents=True)
    FFMPEG=m.c.executable('ffmpeg');FFPROBE=m.c.executable('ffprobe')
    log=io.StringIO();runner=unittest.TextTestRunner(stream=log,verbosity=2)
    suite=(unittest.defaultTestLoader.loadTestsFromName(args.test,Tests) if args.test else
           unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
    result=runner.run(suite)
    (ROOT/'test-log.txt').write_text(log.getvalue(),encoding='utf-8');print(log.getvalue())
    m.c.save(ROOT/'test-summary.json',dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),
             skipped=len(result.skipped),success=result.wasSuccessful(),python=sys.version,
             ffmpeg=m.c.run([FFMPEG,'-version']).splitlines()[0],
             limits='Synthetic only; no ASR, user footage, semantic selection or human listening tested.'))
    sys.exit(0 if result.wasSuccessful() else 1)
