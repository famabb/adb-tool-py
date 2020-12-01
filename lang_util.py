import os
import adb_util
import util


class LangBean:
    """
        语言Bean
    """
    name = ''  # 中文（简体）
    locale = ''  # zh_CN）


class Lang:
    """
        修改系统语言工具
    """
    parent_path = ''
    apk_path = ''
    lang_path = ''
    lang_dict = {}

    def __init__(self):
        super().__init__()
        cur_path = os.path.abspath(__file__)
        self.parent_path = os.path.abspath(os.path.dirname(cur_path)).replace('/', '\\')
        self.apk_path = self.parent_path + '\\lang\\ChangeLanguage.apk'
        self.lang_path = self.parent_path + '\\lang\\lang.txt'

    def install_lang_apk(self):
        return adb_util.installApk(self.apk_path)

    def startLangApk(self):
        return adb_util.startApp(self.apk_path)

    # 申请 CHANGE_CONFIGURATION 权限
    def fix_change_configuration(self):
        cmd = 'adb shell pm grant com.ew.escort.languages android.permission.CHANGE_CONFIGURATION'
        msg = util.getCommodText(cmd)
        print('fix_change_configuration : ' + msg)
        return msg

    # 打开 WRITE_SETTINGS 权限设置窗口
    def open_write_settings(self):
        cmd = 'adb shell am broadcast -a com.ew.action.CHANGE_LANGUAGE --es ws "true" --include-stopped-packages ' \
              'com.ew.escort.languages '
        msg = util.getCommodText(cmd)
        return msg

    def change_language(self, lang):
        cmd = 'adb shell am broadcast -a com.ew.action.CHANGE_LANGUAGE --es locale \"' + lang + \
              '\" --include-stopped-packages  com.ew.escort.languages '
        msg = util.getCommodText(cmd)
        return msg

    def get_lang_config(self):
        f = open(self.lang_path, encoding='utf-8')
        content_list = f.readlines()
        lang_beans = list()
        self.lang_dict = {}
        for content in content_list:
            content = content.replace("\n", "")
            if str(content).replace(" ", "", 100000) is "":
                continue
            sp = str(content).split(' ')
            bean = LangBean()
            index = 0
            for n in sp:
                if n is not ' ' and n is not '':
                    if index is 0:
                        bean.locale = n
                        index += 1
                    elif index is 1:
                        bean.name = n
                        index += 1
            self.lang_dict[bean.name] = bean.locale
            lang_beans.append(bean)
        f.close()
        return lang_beans

    def getLangLocale(self, name):
        return self.lang_dict[name]


if __name__ == '__main__':
    lang = Lang()
    # lang.install_lang_apk()
    # lang.startLangApk()
    # lang.fix_change_configuration()
    # lang.open_write_settings()
    # lang.change_language("en_US")
    # lang_beans = lang.get_lang_config()
    # for bean in lang_beans:
    #     print("bean :" + bean.name + "  " + bean.locale)
