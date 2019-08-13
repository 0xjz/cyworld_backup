# -*- coding: utf-8 -*-
import os
import urllib.request

userNoList = []
headers = {}

# 현재 스크립트 하위 images 폴더 경로 반환
# 폴더가 없을경우 폴더 생성
def getimagefolderpath():
    imageFolderPath = os.path.dirname(os.path.abspath(__file__)) + "/images"
    if not os.path.exists(imageFolderPath):
        os.makedirs(imageFolderPath)
    return imageFolderPath

def downloadfile(URL, filePath):
    try:
        urllib.request.urlretrieve(URL, filePath)
    except:
        print("DOWNLOAD ERROR, URL : ", URL)

def loadheader():
    global userNoList

    headerFilePath = os.path.dirname(os.path.abspath(__file__)) + "/header.txt"

    if not os.path.exists(headerFilePath) or os.stat(headerFilePath).st_size == 0:
        raise Exception("ERROR : header.txt does not exist or file has no text")

    f = open(headerFilePath, "r")

    try:
        while True:
            line = f.readline()
            if not line: break

            if line.startswith("GET"):
                userNoList.append(line.split(" ")[1].split("/")[2])

                if not userNoList[0].isnumeric():
                    raise Exception("ERROR : cannot find userNo")
            else:
                global headers
                kv = line.split(":", 1)
                kv[1] = kv[1].endswith("\n") and kv[1][:-1] or kv[1]
                kv[1] = kv[1].startswith(" ") and kv[1][1:] or kv[1]
                headers[kv[0]] = kv[1]
        if not userNoList:
            raise Exception("ERROR : cannot find userNo")

    except Exception as e:
        print("error occured, please check header.txt, error message : ", e)
        raise(e)
    finally:
        f.close()

