# coding=utf-8

import requests
import re
import json
import execjs
from lxml import etree
with open("mysdk.js", "r", encoding="utf-8") as f:
    js = f.read()
    ctx = execjs.compile(js)
def getHeros(text=None):
    if text:
        content = text
        w80s = ""
    else:
        headers = {
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        response = requests.get('http://epub.sipo.gov.cn/', headers=headers, timeout=30)
        w80s = response.cookies['wIlwQR28aVgb80S']
        content = response.text
    html = etree.HTML(content)
    js = html.xpath("//script[2]/text()")[0]
    if text:
        naruto = html.xpath("//meta/@content")[2]
    else:
        naruto = html.xpath("//meta/@content")[1]
    states = re.findall("\[\[[,0-9]+\],\[[,0-9]+\],\[[,0-9]+\],\[[,0-9]+\],\[[0-9,]+\]\]", js)[0]
    tens = [None] * 101
    sasuke = []
    kakashi = []
    sakura = []
    lno = json.loads(states)[1][90:93]
    udon = sorted(lno)
    tenten = re.findall("_\$.{2}\._\$.{2}=[0-9]+;", js)
    asuma = sorted(tenten)
    if asuma[0][:4] != asuma[1][:4]:
        tyochi = asuma[0]
    else:
        tyochi = asuma[3]
    temp = tenten
    tenten = []
    for p in temp:
        if p != tyochi:
            tenten.append(p)
    for i in range(0, len(udon)):
        tens[udon[i]] = re.findall("=([0-9]+);", tenten[i])[0]
    for i in lno:
        sasuke.append(int(tens[i]))
    lno = json.loads(states)[1][93:107] + json.loads(states)[1][108:117]
    udon = sorted(lno)
    tenten = re.findall("_\$.{2}\._\$.{2}=\"[a-zA-Z\\.0-9_\\$]*\";", js)
    for i in range(0, len(udon)):
        tens[udon[i]] = re.findall("\"(.*)\";", tenten[i])[0]
    for i in lno:
        kakashi.append(tens[i])
    varNames = ""
    maybeParams = [103, 0, 102, 203, 224, 181, 108, 240, 101, 126, 103, 11, 102, 203, 224, 181, 208, 180, 100, 127]
    lno = json.loads(states)[1][14:24]
    udon = sorted(lno)
    tenten = re.findall("_\$.{2}\+=\"[a-zA-Z0-9_\$]+\";", js)
    for i in range(0, len(udon)):
        tens[udon[i]] = re.findall("\"(.*)\";", tenten[i])[0]
    for i in lno:
        varNames += tens[i]
    tempVars = []
    for i in range(290, 330, 2):
        tempVars.append("_$" + varNames[i:i+2])
    allVars = dict(zip(tempVars, maybeParams))
    sakura.append(allVars[kakashi[16]])
    sakura.append(allVars[kakashi[18]])
    sakura.append(allVars[kakashi[20]])
    sakura.append(allVars[kakashi[22]])
    return [w80s, [naruto, sasuke, kakashi, sakura]]

if __name__ == "__main__":
    w80s, tens = getHeros()
    naruto, sasuke, kakashi, sakura = tens
    url = "http://epub.sipo.gov.cn/"
    ywtu, w80t = ctx.call("roger", naruto, sasuke, kakashi, sakura)
    cookies = {
        'wIlwQR28aVgb80S': w80s,
        'wIlwQR28aVgb80T': w80t,
    }
    headers = {
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': 'http://epub.sipo.gov.cn/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = requests.get(url, headers=headers, cookies=cookies, timeout=30, verify=False)
    _, tens = getHeros(response.text)
    naruto, sasuke, kakashi, sakura = tens
    url = "http://epub.sipo.gov.cn/patentoutline.action"
    _, w80t = ctx.call("roger", naruto, sasuke, kakashi, sakura, ywtu, w80t)
    cookies = {
        'wIlwQR28aVgb80S': w80s,
        'wIlwQR28aVgb80T': w80t,
    }
    headers = {
        'Proxy-Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://epub.sipo.gov.cn',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': 'http://epub.sipo.gov.cn/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    data = {
      'showType': '1',
      'strSources': '',
      'strWhere': 'PD=\'2020.03.06\'',
      'numSortMethod': '5',
      'strLicenseCode': '',
      'numIp': '',
      'numIpc': '',
      'numIg': '',
      'numIgc': '',
      'numIgd': '',
      'numUg': '',
      'numUgc': '',
      'numUgd': '',
      'numDg': '0',
      'numDgc': '',
      'pageSize': '10',
      'pageNow': '1'
    }
    response = requests.post(url, headers=headers, cookies=cookies, data=data, timeout=30, verify=False)
    print(response.text)
