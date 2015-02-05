import os
import collections

import psycopg2

base = '/var/www/tomat.svartalf.info/app/media/products'
repl = '/var/www/tomat.svartalf.info/app/media/'

conn = psycopg2.connect(database='tomat', user='postgres')
cursor = conn.cursor()

for d in os.listdir(base):
    p = os.path.join(base, d)
    s = {}
    for f in os.listdir(p):
        if '_q' in f:
            continue

        fp = os.path.join(p, f)
        s[fp] = os.stat(fp).st_size

    c = collections.Counter(s.values())
    for k, v in c.items():
        if v == 1:
            continue

        to_remove = []
        for fp, size in s.items():
            if k == size:
                to_remove.append(fp.replace(repl, ''))

        to_remove = list(set(to_remove))
        for fs in to_remove[1:]:
            cursor.execute('''UPDATE products_photos SET image = '' WHERE image = %s AND is_main = false ''', (fs, ))
            # cursor.execute('DELETE FROM products_photos WHERE image = %s', (fs, ))
            conn.commit()
            # os.remove(os.path.join(repl, fs))

