"""Run with: retrieval/.venv/Scripts/python.exe -m unittest discover -s scripts -p test_database_retrieval.py -v"""
from contextlib import closing
from pathlib import Path
import tempfile
import unittest
import database_retrieval as r


class RetrievalTests(unittest.TestCase):
    def test_chunk_coverage(self):
        lines = ['line ' + str(n) + ' x' * 60 for n in range(130)]
        coverage = set()
        for first, last, text in r.chunks(lines):
            self.assertEqual(text, '\n'.join(lines[first-1:last]))
            coverage.update(range(first, last+1))
        self.assertEqual(coverage, set(range(1,131)))
        self.assertEqual(list(r.chunks([])), [])
        self.assertEqual(len(list(r.chunks(['x'*10000, 'y']))), 2)

    def test_update_failure_exclusion_and_freshness(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root/'Database'
            source.mkdir()
            (source/'a.md').write_text('# Storytelling\nStakes and re-hook matter.\n',encoding='utf-8')
            (source/'broken.pdf').write_bytes(b'not a pdf')
            (source/'archive.zip').write_bytes(b'archive')
            (source/'.git').mkdir()
            (source/'.git'/'hidden.md').write_text('should never index')
            target, catalog = root/'retrieval',root/'memory/database-catalog.md'
            r.build(root,source,target,catalog)
            with closing(r.connect(target/'sources.sqlite3')) as db:
                self.assertEqual(r.verify(db,root), [])
                self.assertTrue(r.query(db,'stakes'))
                self.assertEqual(r.query(db,'" OR * ; DROP TABLE documents'), [])
                self.assertEqual(db.execute("SELECT status FROM documents WHERE path LIKE '%broken.pdf'").fetchone()[0], 'failed')
                self.assertEqual(db.execute("SELECT count(*) FROM documents WHERE path LIKE '%hidden.md'").fetchone()[0],0)
                self.assertEqual(db.execute("SELECT status FROM documents WHERE path LIKE '%archive.zip'").fetchone()[0],'excluded')
                (source/'a.md').write_text('# Changed\nnew topic',encoding='utf-8')
                (source/'new.md').write_text('new source',encoding='utf-8')
                self.assertEqual({x['issue'] for x in r.verify(db,root)}, {'new or previously unreadable','changed'})
            r.build(root,source,target,catalog)
            with closing(r.connect(target/'sources.sqlite3')) as db:
                self.assertEqual(r.verify(db,root), [])
                self.assertEqual(r.query(db,'stakes'), [])
                self.assertTrue(r.query(db,'changed'))
            (source/'new.md').unlink()
            with closing(r.connect(target/'sources.sqlite3')) as db:
                self.assertEqual(r.verify(db,root)[0]['issue'],'deleted')
            for line in catalog.read_text(encoding='utf-8').splitlines():
                if line.strip():
                    self.assertIn(r.PROJECT,line)

    def test_actual_inventory_and_all_citations(self):
        with closing(r.connect(r.ROOT/'retrieval/sources.sqlite3')) as db:
            self.assertEqual(r.verify(db,r.ROOT), [])
            expected = {p.relative_to(r.ROOT).as_posix() for p,reason in r.inventory(r.ROOT/'Database') if reason is None and p.suffix.lower() in {'.md','.pdf'}}
            indexed = {x[0] for x in db.execute("SELECT path FROM documents WHERE status IN ('indexed','partial')")}
            self.assertEqual(expected,indexed)
            cache = {}
            n = 0
            for row in db.execute('SELECT c.*,d.path,d.sha256 AS source_hash FROM chunks c JOIN documents d ON d.id=c.document_id'):
                if row['path'] not in cache:
                    p = r.ROOT/row['path']
                    pages, _, _ = r.extract(p)
                    cache[row['path']] = dict(pages)
                    self.assertEqual(r.sha(p.read_bytes()),row['source_hash'])
                lines = cache[row['path']][row['page']]
                text = '\n'.join(lines[row['line_start']-1:row['line_end']])
                self.assertEqual(text,row['text'])
                self.assertEqual(r.sha(text.encode()),row['sha256'])
                n += 1
            self.assertGreater(n,100)
            print(f'Validated {n} chunk citations across {len(cache)} sources')

    def test_actual_topics(self):
        checks = [('storytelling stakes','Story Telling'),('controlnet adapter','ComfyUI'),
                  ('rag knowledge','n8n'),('git commit','Git/'),('first sale','Business'),
                  ('ollama gguf','Ollama')]
        with closing(r.connect(r.ROOT/'retrieval/sources.sqlite3')) as db:
            for question, expected in checks:
                hits = r.query(db,question,limit=8)
                self.assertTrue(hits,question)
                self.assertTrue(any(expected.lower() in h['path'].lower() for h in hits),(question,[h['path'] for h in hits]))
                print(question, '=>', hits[0]['citation'])
            pdf = r.query(db,'storytelling stakes',path_filter='.pdf')
            self.assertTrue(pdf)
            self.assertIsNotNone(pdf[0]['page'])
            print('PDF =>',pdf[0]['citation'])


if __name__ == '__main__':
    unittest.main()
