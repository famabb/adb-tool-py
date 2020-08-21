import datetime
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


def getCommodText(cmd):
    text = ''
    try:
        # creationflags  屏蔽adb命令
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
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


if __name__ == '__main__':
    print('util.py')
