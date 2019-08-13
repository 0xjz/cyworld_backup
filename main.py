# -*- coding: utf-8 -*-
import datetime
import http.client
import json
import ssl
import time
import sys

from util import getimagefolderpath, userNoList, loadheader, downloadfile, headers

# step 1. load config
imageFolder = getimagefolderpath()
imageUrlPrefix = "http://nthumb.cyworld.com/thumb?width=10000&url="
loadheader()
userNo = userNoList[0]

# step 2. set initial request uri
baseRequestUrl = "/home/{}/posts?listsize=20&homeId={}&searchType=F&search=&folderid={}00000032000000000".format(userNo, userNo, userNo)
reqCnt = int(round(time.time() * 1000))
cnt = 0
params = "&_={}".format(reqCnt)

conn = http.client.HTTPSConnection("cy.cyworld.com", context=ssl._create_unverified_context())

# step 3. get images
while True:
    cnt += 1
    print("try : ", cnt, params, baseRequestUrl + params)

    conn.request("GET", baseRequestUrl + params, headers=headers)
    r1 = conn.getresponse()
    root = json.loads(r1.read())

    for post in root['postList']:
        fileDate = datetime.datetime.fromtimestamp(int(post['publishedDate'])/1000.0).strftime("%Y%m%d")

        fileName = fileDate + "_" + post['identity']
        targetImageUrl = post['summaryModel']['image']
        imageExt = targetImageUrl.split('.')[-1]
        downloadfile(imageUrlPrefix + targetImageUrl, imageFolder + "/" + fileName + "." + imageExt)

    if len(root['postList']) < 20:
        print("--- DOWNLOAD COMPLETE ---")
        break
    else:
        reqCnt += 1
        params = "&_={}&lastid={}&lastdate={}".format(reqCnt, post['identity'], post['publishedDate'])
    time.sleep(0.3)