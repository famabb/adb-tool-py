# -*- coding: utf-8 -*-
import os
import sys
import util
import adb_util

if __name__ == '__main__':
    try:
        if (len(sys.argv) > 1):
            filePath = sys.argv[1]

            if (filePath.endswith('.apk') or filePath.endswith('.APK')):
               adb_util.installApk(filePath)
               adb_util.startApp(filePath)
               util.delatyClose()
    except Exception as e:
        print(e)
        os.system('pause')


	


