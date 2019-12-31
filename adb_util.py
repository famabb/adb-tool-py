import subprocess
import apk_info
import util

def startAdbServer():
    cmd = 'adb start-server'
    msg = util.getCommodText(cmd)
    print(msg)

def installApk(apkPath):
    cmd = 'adb install '+util.tranlatePath(apkPath)
    msg = util.getCommodText(cmd)
    print(msg)


def uninstall(package):
    cmd = 'adb uninstall '+package
    msg = util.getCommodText(cmd)
    print(msg)



def reInstallApk(apkPath):
    cmd = 'adb install -r  '+util.tranlatePath(apkPath)
    msg = util.getCommodText(cmd)
    print(msg)

def clear(package):
    cmd = 'adb shell pm clear '+package
    msg = util.getCommodText(cmd)
    print(msg)

def startApp(apkPath):
    apk = apk_info.ApkInfo(apkPath)
    cmd = 'adb shell am start -W -n '+apk.package+"/"+apk.launchable
    msg = util.getCommodText(cmd)
    print(msg)




if __name__ == '__main__':
	print('adb_util.py')