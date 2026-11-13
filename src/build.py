import json, collections, sys
L = collections.OrderedDict(); cur = None
for f in ['lines.txt', 'lines2.txt']:
  for line in open(f, encoding='utf-8'):
    line = line.strip()
    if not line or line.startswith('# '): continue
    if line.startswith('## '):
        n, g = [x.strip() for x in line[3:].split('|')]; cur = n
        if n in L: assert L[n]['g'] == g, n
        L.setdefault(n, {'n': n, 'g': g, 'a': []}); continue
    if line not in L[cur]['a']: L[cur]['a'].append(line)
data = list(L.values())
t = open('template.html', encoding='utf-8').read()
t = t.replace('__DATA__', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
t = t.replace('"JERE_PFP"', '"' + open(sys.argv[1]).read().strip() + '"')
open('philosophy-ragebait.html', 'w', encoding='utf-8').write(t)
groups = collections.OrderedDict()
for d in data: groups.setdefault(d['g'], []).append(d)
for g, ds in groups.items(): print(f"{g}: {len(ds)} targets, {sum(len(d['a']) for d in ds)} lines")
allx = [x for d in data for x in d['a']]
print('total', len(data), 'targets,', len(allx), 'lines; dupes across targets:', [k for k, v in collections.Counter(allx).items() if v > 1])
print('shortest sets:', sorted((len(d['a']), d['n']) for d in data)[:5])
