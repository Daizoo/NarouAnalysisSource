import json
import urllib.request
import urllib.parse
import yaml
import gzip
from datetime import datetime
from collections import OrderedDict as od

URL = 'https://api.syosetu.com/novelapi/api/?'  # APIのURL
baseDate = datetime(2018, 10, 31, 23, 59, 59).strftime('%s')
# 2018年10月31日までの作品を対象
firstTenseiDate = datetime(2007, 9, 20, 0, 0, 0).strftime('%s')
# 異世界転生でキーワード検索のうち一番古い作品が2007/9/20
firstTenniDate = datetime(2006, 1, 9, 0, 0, 0).strftime('%s')
# 異世界転移でキーワード検索のうち一番古い作品が2006/1/9

num = 1
filenum = '%04d' % num

parameter = {
    'gzip': 5,
    'out': 'yaml',
    'of': 'n-gf-g-bg',
    'lim': 10,
    'order': 'ncodedesc',
    'word': '異世界転生',
    'firstup': firstTenseiDate + '-' + baseDate
}
# 手始めの処理
p = urllib.parse.urlencode(parameter)
with urllib.request.urlopen(URL + p) as res:
    gz = gzip.GzipFile(fileobj=res)
    data = gz.read().decode('utf-8')
    data = yaml.load(data)[1:]
    gz.close()
    print(data)

saveDict = od()
for d in data:
    ncode = d['ncode']
    saveDict[ncode] = d
    unixTime = d['general_firstup'].strftime('%s')
    saveDict[ncode]['general_firstup'] = unixTime

with open('test.json', 'w') as fw:
    json.dump(saveDict, fw, indent=4)

lastGetData = data[-1]
nextTenseiDate = lastGetData['general_firstup']
print(nextTenseiDate)
print(len(data))

parameter['firstup'] = firstTenseiDate + '-' + nextTenseiDate
p = urllib.parse.urlencode(parameter)
with urllib.request.urlopen(URL + p) as res:
    gz = gzip.GzipFile(fileobj=res)
    data = gz.read().decode('utf-8')
    data = yaml.load(data)[1:]
    gz.close()
    print(data)
