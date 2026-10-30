import sys, json
for line in sys.stdin:
    if line.startswith('HEADLESS_RESULT'):
        d = json.loads(line[len('HEADLESS_RESULT '):])
        print('audit', json.dumps(d['audit']))
        print('clips', d['clips'], 'events', d['events'])
        print('ground', d['ground_min_z'], 'tris', d.get('tris_body'))
        print('free', d['collision_free'])
        for c, v in d['collisions'].items():
            print(' ', c, v)
        if 'export' in d:
            print('export', d['export'])
    elif 'Error' in line or 'Traceback' in line or 'line ' in line:
        print(line.strip())
