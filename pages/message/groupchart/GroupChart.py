import time
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChartPage(BasePage):
    """群聊页面_"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'
    __locators = {
        '返回': (MobileBy.XPATH, '//*[@content-desc="转到上一层级"]'),
        '通话': (MobileBy.ID, 'com.cmic.college:id/iv_icon'),
        '聊天设置': (MobileBy.ID, 'com.cmic.college:id/action_setting'),

    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('等待选择预览图片页面跳转')
    def wait_for_page_group_chart(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["通话"]),
                timeout=timeout,
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log('点击设置')
    def click_setting(self):
        self.click_element(self.__locators['聊天设置'])
