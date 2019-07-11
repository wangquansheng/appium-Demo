import time
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SingChartSettingPage(BasePage):
    """单聊-设置页面_"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'
    __locators = {
        '返回': (MobileBy.XPATH, '//*[@content-desc="转到上一层级"]'),
        '更改聊天主题背景': (MobileBy.ID, 'com.cmic.college:id/rl_message_bg_set'),
        '消息免打扰': (MobileBy.ID, 'com.cmic.college:id/manage_switch_undisturb'),
        '查找聊天记录': (MobileBy.ID, 'com.cmic.college:id/tv_serarch_chat_record'),
        '聊天文件': (MobileBy.ID, 'com.cmic.college:id/tv_chat_file'),
        '投诉': (MobileBy.ID, 'com.cmic.college:id/rl_complain'),
        '取消': (MobileBy.XPATH, '//*[@text="取消"]'),
        '聊天联系人': (MobileBy.ID, 'com.cmic.college:id/iv_setting_avatar'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('等待群设置页面跳转')
    def wait_for_page_single_chart_setting(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["更改聊天主题背景"]),
                timeout=timeout,
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log('点击更改聊天主题背景')
    def click_modify_theme(self):
        self.click_element(self.__locators['更改聊天主题背景'])

    @TestLogger.log('点击聊天联系人')
    def click_chart_profile(self):
        self.click_element(self.__locators['聊天联系人'])
