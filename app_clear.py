
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import adb_util
import apk_info
import util

if __name__ == '__main__':
    try:
        if (len(sys.argv) > 1):
            filePath = sys.argv[1]

            if (filePath.endswith('.apk') or filePath.endswith('.APK')):
               apk = apk_info.ApkInfo(filePath)
               adb_util.clear(apk.package)
               adb_util.startApp(filePath)
               util.delatyClose()
    except Exception as e:
        print(e)
        os.system('pause')
