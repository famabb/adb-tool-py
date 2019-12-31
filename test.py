
# -*- coding: utf-8 -*-
import winreg
import sys
import os

def adbTest():
	
    a = os.popen('adb')
    #此时打开的a是一个对象，如果直接打印的话是对象内存地址
    text = a.read()
    #要用read（）方法读取后才是文本对象
    print(text)
    a.close()#打印后还需将对象关闭
    #下面执行adb devices同理
    b = os.popen('adb devices')
    text2 = b.read()
    print(text2)
    b.close()



env_dist = os.environ # environ是在os.py中定义的一个dict environ = {}
evn = env_dist.get('PYTHON_EXE')
# print('current path is: {0}'.format(sys.argv[1]))
print("----",sys.path[0],evn)
# adbTest()`

