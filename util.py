import time
import constant
import subprocess
import locale

def tranlatePath(path):
    return '\"'+path+'\"'


def delatyClose():
    end = constant.delay
    for x in range(end):
        print(end-x)
        time.sleep(1)


def getCommodText(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out,err = popen.communicate()
    text = ''
    for line in out.splitlines():
        text = text+line.decode('utf-8')+'\n'
    return text

if __name__ == '__main__':
	print('util.py')