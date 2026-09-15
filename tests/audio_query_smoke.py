"""Query the temporary corpus produced by MMG's real audio pipeline test.

Run with a backend Python, passing that temporary corpus directory. This
uses Flask's HTTP test client and the real CQP executable, without a database.
"""
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import shutil

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
if os.environ.get('MMG_TEST_PYMYSQL') == '1':
    # Optional test environment without native MySQL client headers. /query
    # itself never uses SQL; this only satisfies Flask-MySQLdb's import.
    import pymysql
    pymysql.install_as_MySQLdb()

from korp import create_app

corpus = Path(sys.argv[1])
registry = corpus / 'export/cwb.encoded/registry'
config_dir = corpus / 'backend-config'
(config_dir / 'corpora').mkdir(parents=True)
shutil.copy(corpus / 'export/korp.config/tingfundir.yaml', config_dir / 'corpora/tingfundir.yaml')
shared_config = Path(__file__).resolve().parents[2] / 'gorps-stillingar-aftan'
for folder in ('attributes', 'modes'):
    (config_dir / folder).symlink_to(shared_config / folder, target_is_directory=True)
attrs = ['s_audio_start', 's_audio_end', 's_audio_char_start', 's_audio_char_end',
         'text_ljod', 'text_source_id', 'text_audio_id', 'text_meeting_id', 'text_second']
with contextlib.redirect_stdout(io.StringIO()):
    app = create_app(dict(CQP_EXECUTABLE=shutil.which('cqp'), CWB_SCAN_EXECUTABLE=shutil.which('cwb-scan-corpus'),
                          CWB_REGISTRY=str(registry), LC_COLLATE='C.UTF-8', MEMCACHED_SERVER=None,
                          CORPUS_CONFIG_DIR=str(config_dir), PLUGINS=[], TESTING=True))
    frontend_config = app.test_client().get('/corpus_config', query_string={
        'corpus': 'tingfundir', 'mode': 'MMG2026', 'cache': 'false'}).get_json()
    params = dict(
        corpus='TINGFUNDIR', cqp='[word="næsti"]', default_context='1 text', default_within='s',
        show=','.join(['word', 's'] + attrs), show_struct=','.join(attrs), cache='false', end=10)
    response = app.test_client().get('/query', query_string=params)
    samples = {}
    for context in ('1 s', '2 words', '30 words'):
        r = app.test_client().get('/query', query_string={**params, 'default_context': context})
        samples[context] = r.get_json()
payload = response.get_json()
assert response.status_code == 200 and 'ERROR' not in payload, (response.status_code, payload)
assert payload.get('hits') == 3, payload
payload['context_samples'] = samples
payload['frontend_config'] = frontend_config
print(json.dumps(payload, ensure_ascii=False))
