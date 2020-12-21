# !/usr/bin/env python
# -*- coding: utf-8 -*-
import apk_info
import util


def stop_app(pkg):
    cmd = 'adb shell am force-stop ' + pkg
    msg = util.getCommodText(cmd)
    print('stop_app : ' + msg)
    return msg


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


def reInstallApk(apkPath):
    cmd = 'adb install -r ' + util.tranlatePath(apkPath)
    msg = util.getCommodText(cmd)
    print('reInstallApk : ' + msg)
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


def start_App(package, launchable):
    cmd = 'adb shell am start -W -n ' + package + "/" + launchable
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
    # print('get_dev_version : ' + msg)
    return msg


def get_dev_api():
    cmd = 'adb shell getprop ro.build.version.sdk'
    msg = util.getCommodText(cmd)
    # print('get_dev_api : ' + msg)
    return msg


def click_tap(x, y):
    cmd = 'adb shell input tap ' + str(x) + '  ' + str(y)
    msg = util.getCommodText(cmd)
    # print('click tap : ' + msg)
    return msg


# 滑动 time 毫秒
def click_swipe(x, y, x2, y2, time):
    cmd = 'adb shell input swipe ' + str(x) + '  ' + str(y) + '  ' + str(x2) + '  ' + str(y2) + '  ' + str(time)
    msg = util.getCommodText(cmd)
    return msg


# https://www.cnblogs.com/sharecenter/p/5621048.html
def click_keyevent(keyCode):
    cmd = 'adb shell input keyevent ' + str(keyCode)
    msg = util.getCommodText(cmd)
    # print('click keyevent : ' + msg)
    return msg


def event_input(text):
    cmd = 'adb shell input text ' + text
    msg = util.getCommodText(cmd)
    return msg


def get_click_event_popen():
    cmd = 'adb shell getevent '
    return util.get_popen(cmd)


def get_focus_app_pkg():
    cmd = 'adb shell \"dumpsys window | grep mCurrentFocus\"'
    msg = util.getCommodText(cmd)
    package = None
    try:
        package = msg.split(" ")[4].split("/")[0]
    except Exception as e:
        print("get_focus_app_pkg Exception:" + e.args[0]+'   '+msg)
    return package


# {package,versionCode,versionName}
def get_pkg_info(pkg):
    info = {"package": pkg}
    try:
        cmd = 'adb shell pm dump ' + pkg + '  |  grep  \"versionName\"'
        version_name = util.getCommodText(cmd)
        info["versionName"] = version_name

        cmd = 'adb shell pm dump ' + pkg + '  |  grep  \"versionCode\"'
        version_code = util.getCommodText(cmd)
        info["versionCode"] = version_code
    except Exception as e:
        print("get_pkg_info Exception  " + e.args[0])
    return info


def safe_index_of(str0, substr):
    try:
        return str0.index(substr)
    except ValueError:
        return -1


def get_app_main(package_name):
    cmd = "adb shell dumpsys package " + package_name
    result = util.getCommodText(cmd)
    if not result:
        return None
    end_index = safe_index_of(result, "android.intent.category.LAUNCHER")
    if end_index >= 0:
        start_index = (end_index - 150) if end_index - 150 >= 0 else 0
        lines = result[start_index:end_index].split(' ')
        for line in lines:
            if package_name in line:
                return line.strip()

    start_index = safe_index_of(result, "android.intent.action.MAIN")
    if start_index >= 0:
        end_index = (start_index + 300) if (start_index + 300 < len(result)) else len(result)
        lines = result[start_index:end_index].split(' ')
        key = "%s/" % (package_name)
        for line in lines:
            if '/com.' in line:
                if "/%s" % (package_name) in line:
                    return line.strip()
            if key in line:
                return line.strip()
    return None


def get_launcher(package_name):
    main_info = get_app_main(package_name)
    if main_info:
        sp = main_info.split("/")
        if len(sp) > 1:
            return sp[1]
    return main_info


if __name__ == '__main__':
    print('adb_util.py')
