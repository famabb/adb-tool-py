
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import apk_info
import util
import adb_util



if __name__ == '__main__':
    try:
        if (len(sys.argv) > 1):
            filePath = sys.argv[1]

            if (filePath.endswith('.apk') or filePath.endswith('.APK')):
               apk = apk_info.ApkInfo(filePath)
               adb_util.uninstall(apk.package)
               util.delatyClose()
    except Exception as e:
        print(e)
        os.system('pause')



  