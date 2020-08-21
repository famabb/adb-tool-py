import apk_info
import util


def startAdbServer():
    cmd = 'adb start-server'
    msg = util.getCommodText(cmd)
    print('startAdbServer : ' + msg)
    return msg


def installApk(apkPath):
    cmd = 'adb install ' + util.tranlatePath(apkPath)
    msg = util.getCommodText(cmd)
    print('installApk : ' + msg)
    return msg


def uninstall(package):
    cmd = 'adb uninstall ' + package
    msg = util.getCommodText(cmd)
    print('uninstall : ' + msg)
    return msg


def reInstallApk(apkPath):
    cmd = 'adb install -r  ' + util.tranlatePath(apkPath)
    msg = util.getCommodText(cmd)
    print('reInstallApk : ' + msg)
    return msg


def clear(package):
    cmd = 'adb shell pm clear ' + package
    msg = util.getCommodText(cmd)
    print('clear : ' + msg)
    return msg


def startApp(apkPath):
    apk = apk_info.ApkInfo(apkPath)
    cmd = 'adb shell am start -W -n ' + apk.package + "/" + apk.launchable
    msg = util.getCommodText(cmd)
    print('startApp : ' + msg)
    return msg


def installApks(bundle_tool_path, apks_path):
    cmd = 'java -jar ' + bundle_tool_path + ' install-apks --apks=' + apks_path
    msg = util.getCommodText(cmd)
    print('installApks : ' + msg)
    return msg


# 修改语言 country CA, language fr 需要root权限
def fixLanguage(country, language):
    cmd = 'adb shell "setprop persist.sys.language ' + language + '; setprop persist.sys.country ' + country + '; setprop ctl.restart zygote"'
    msg = util.getCommodText(cmd)
    print('fixLanguage : ' + msg)
    return msg

def get_dev_version():
    cmd = 'adb shell getprop ro.build.version.release'
    msg = util.getCommodText(cmd)
    print('get_dev_version : ' + msg)
    return msg


def get_dev_api():
    cmd = 'adb shell getprop ro.build.version.sdk'
    msg = util.getCommodText(cmd)
    print('get_dev_api : ' + msg)
    return msg

if __name__ == '__main__':
    print('adb_util.py')
