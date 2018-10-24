import json
import urllib.request
import urllib.parse
import gzip
from datetime import datetime

URL = 'https://api.syosetu.com/novelapi/api/?'  # APIのURL
baseDate = datetime(2018, 10, 31, 23, 59, 59).strftime('%s')
# 2018年10月31日までの作品を対象
firstTenseiDate = datetime(2007, 9, 20, 0, 0, 0).strftime('%s')
# 異世界転生でキーワード検索のうち一番古い作品が2008/2/22
firstTenniDate = datetime(2006, 1, 9, 0, 0, 0).strftime('%s')
# 異世界転移でキーワード検索のうち一番古い作品が2006/1/9
parameter = {
    'gzip': 5,
    'out': 'json',
    'of': 'n-gf',
    'lim': 10,
    'order': 'old',
    'word': '異世界転生',
    'firstup': firstTenseiDate + '-' + baseDate
}

p = urllib.parse.urlencode(parameter)
with urllib.request.urlopen(URL + p) as res:
    gz = gzip.GzipFile(fileobj=res)
    data = gz.read().decode('utf-8')
    data = json.loads(data)
    gz.close()
    print(data[1:])
