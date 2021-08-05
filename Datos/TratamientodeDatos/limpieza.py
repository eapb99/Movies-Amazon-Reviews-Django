import datetime
import re
import psycopg2
import tzlocal

moviefile = open('movies.txt', encoding='latin')
output = open('output.txt', 'w', encoding='latin')
cont = 0
for line in moviefile:
    if line != '\n':
        output.write(line.strip() + "\n")
moviefile.close()
output.close()

REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
conn = psycopg2.connect(database="", user='', password='', host='', port='')
cursor = conn.cursor()
output = open('output.txt', 'r', encoding='latin')
pr = ''
indice = 1
d = {}
for line in output:
    if "product" in line or 'review' in line:
        a, b = line.strip().split("/", 1)[1].split(":", 1)
        pr = b
        d[a] = b.strip()
        if a == 'score':
            d[a] = float(b)
        elif a == 'helpfulness':
            nu, dem = b.split("/")
            nu = int(nu);
            dem = int(dem)
            if nu != 0:
                d[a] = round((nu / dem) * 100, 2)
            else:
                d[a] = 0
        elif a == 'time':
            ts = int(b)
            tztime = tzlocal.get_localzone()
            localtime = datetime.datetime.fromtimestamp(ts, tztime)
            d[a] = localtime
        elif a == 'text' or a == 'summary' or a == 'profileName':
            b = REPLACE_NO_SPACE.sub("", b.strip())
            b = REPLACE_WITH_SPACE.sub(" ", b.strip())
            d[a] = b
    else:
        nueva = pr.strip() + " " + line.strip()
        pr = nueva
        d[a] = REPLACE_NO_SPACE.sub("", pr.strip())
    if len(d) == 8:
        try:
            data = (
                d["productId"].strip(), d["userId"].strip(), d["profileName"].strip(), d["score"], indice, d["summary"],
                d["text"], d['time'], d["helpfulness"])
        except KeyError as k:
            print(data)
            break
        q = '''INSERT INTO public.REVIEWS (productid, userid, profilename, score, id, summary, text,timed,helpfulness ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cursor.execute(q, data)
        conn.commit()
        indice += 1
        d = {}
output.close()
conn.close()
