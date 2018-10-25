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
firstTenseiDate = datetime(2004, 4, 2, 0, 0, 0).strftime('%s')
# なろうの設立日
num = 1
filenum = '%04d' % num
count = 0
p = 1

parameter = {
    'gzip': 5,
    'out': 'yaml',
    'of': 'n-gf-i-g-bg',
    'lim': 500,
    'order': 'ncodedesc',
    'word': '異世界転移',
    'firstup': firstTenseiDate + '-' + baseDate
}
# 手始めの処理
p = urllib.parse.urlencode(parameter)
with urllib.request.urlopen(URL + p) as res:
    gz = gzip.GzipFile(fileobj=res)
    data = gz.read().decode('utf-8')
    data = yaml.load(data)[1:]
    gz.close()

saveDict = od()
for d in data:
    ncode = d['ncode']
    saveDict[ncode] = d
    saveDict[ncode]['general_firstup'] = d['general_firstup'].strftime('%s')

with open('./novelsData/tenni/Tenni_' + filenum + '.json', 'w') as fw:
    json.dump(saveDict, fw, indent=4)

count += len(data)
print(count)
lastGetData = data[-1]
nextTenseiDate = lastGetData['general_firstup']
print(datetime.fromtimestamp(int(nextTenseiDate)))

while True:
    num += 1
    filenum = '%04d' % num
    parameter['firstup'] = firstTenseiDate + '-' + nextTenseiDate
    p = urllib.parse.urlencode(parameter)
    with urllib.request.urlopen(URL + p) as res:
        gz = gzip.GzipFile(fileobj=res)
        data = gz.read().decode('utf-8')
        data = yaml.load(data)[2:]
        gz.close()

    if len(data) < 1:
        break
    saveDict = od()
    for d in data:
        ncode = d['ncode']
        saveDict[ncode] = d
        saveDict[ncode]['general_firstup'] = d['general_firstup'].\
            strftime('%s')

    with open('./novelsData/tenni/Tenni_' + filenum + '.json', 'w') as fw:
        json.dump(saveDict, fw, indent=4)

    count += len(data)
    print(count)
    lastGetData = data[-1]
    nextTenseiDate = lastGetData['general_firstup']
    print(datetime.fromtimestamp(int(nextTenseiDate)))
