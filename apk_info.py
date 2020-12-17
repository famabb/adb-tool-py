# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import util
import zipfile


# package: name='com.poly.art.coloring.color.by.number' versionCode='3' versionName='0.9.3'
class ApkInfo:
    package = ''
    launchable = ''
    versionCode = ''
    versionName = ''
    apk_path = ''

    def __init__(self, apkpath):
        self.apk_path = apkpath
        sv_path = ''
        if apkpath.lower().endswith('.apks'):
            cur_path = os.path.abspath(__file__)
            parent_path = os.path.abspath(os.path.dirname(cur_path)).replace('/', '\\')
            apk = os.path.join(parent_path, 'standalone.apk')
            if os.path.exists(apk):
                os.remove(apk)
            dstf = open(apk, mode='wb')
            z = zipfile.ZipFile(apkpath, "r")
            standalone = z.read('standalones/standalone.apk')
            dstf.write(standalone)
            dstf.flush()
            dstf.close()
            z.close()
            sv_path = apk
        else:
            sv_path = apkpath

        self.text = self.getApkText(sv_path)

        # self.package = self.getPackage()
        self.launchable = self.getLaunchable()

        match = re.compile(
            "package: name='(\\S+)' versionCode='(\\d+)' versionName='(\\S+)'").match(self.text)
        if match:
            self.package = match.group(1)
            self.versionCode = match.group(2)
            self.versionName = match.group(3)

    def getApkText(self, apk_path):
        aapt_exe = self.get_aapt()
        path = util.tranlatePath(apk_path)
        cmd = aapt_exe + "  dump badging " + path
        return util.getCommodText(cmd)

    def get_aapt(self):
        env_dist = os.environ  # environ是在os.py中定义的一个dict environ = {}
        aapt_exe = env_dist.get('AAPT_EXE')
        return aapt_exe

    # def getPackage(self):
    #     packageMatch = re.compile("package: name='(\\S+)'").match(self.text)
    #     return packageMatch.group(0).replace('package: name=', '').replace('\'', '', 2)

    def getLaunchable(self):
        launchableMatch = re.compile("launchable-activity: name='(\\S+)'").search(self.text)
        return launchableMatch.group(0).replace('launchable-activity: name=', '').replace('\'', '', 2)

    # def getVersionCode(self):
    #     versionCodeMatch = re.compile("versionCode='(\\S+)'").match(self.text)
    #     return versionCodeMatch.group(0).replace('versionCode=', '').replace('\'', '', 2)
    #
    # def getVersionName(self):
    #     versionNameMatch = re.compile("versionName='(\\S+)'").match(self.text)
    #     return versionNameMatch.group(0).replace('versionName=', '').replace('\'', '', 2)


if __name__ == '__main__':
    print('apk_info.py')
    # apk_info = ApkInfo(r"C:\\Users\\chenj\\Desktop\\LowPoly-1.0.13-SDK3935-2019.01.25-release.apk")
    # print(apk_info.package)
    # print(apk_info.launchable)
