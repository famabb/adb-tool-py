import datetime
import os
import subprocess
import time
import traceback

import constant


def tranlatePath(path):
    return '\"' + path + '\"'


def delatyClose():
    end = constant.delay
    for x in range(end):
        print(end - x)
        time.sleep(1)


def get_popen(cmd):
    # creationflags  屏蔽adb命令
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=0x08000000)


def getCommodText(cmd):
    text = ''
    try:
        # creationflags  屏蔽adb命令
        popen = get_popen(cmd)
        out, err = popen.communicate()

        for line in out.splitlines():
            text = text + line.decode('utf-8') + '\n'

        if text == '' and err:
            for line in err.splitlines():
                text = text + line.decode('utf-8') + '\n'

    except Exception as e:
        text = traceback.format_exc()
    return text


def getCurFormatTime():
    now_time = datetime.datetime.now()
    return datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')


def delete_file(path):
    if os.path.exists(path):
        try:
            os.remove(path)
            return True
        except Exception as e:
            f = open(path, encoding="utf-8")
            f.close()
            os.remove(path)
    return False


if __name__ == '__main__':
    print('util.py')
