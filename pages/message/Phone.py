import time

from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class PhonePage(BasePage):
    """手机照相-页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'
    __locators = {
        '返回': (MobileBy.ID, 'com.cmic.college:id/action_bar_back'),
        '轻触拍照,长按录像': (MobileBy.ID, 'com.cmic.college:id/action_bar_duration_recording_tv'),
        '照相': (MobileBy.ID, 'com.cmic.college:id/record'),
        '发送': (MobileBy.ID, 'com.cmic.college:id/send'),
        '撤回': (MobileBy.ID, 'com.cmic.college:id/rerecord'),
        '视频播放页面': (MobileBy.ID, 'com.cmic.college:id/playSurfaceView'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('等待选择文件夹页面跳转')
    def wait_for_page_phone(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["轻触拍照,长按录像"]),
                timeout=timeout,
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log('点击照相')
    def click_take_phone(self):
        self.click_element(self.__locators['照相'])

    @TestLogger.log('点击发送')
    def click_take_phone_send(self):
        self.click_element(self.__locators["发送"])
        time.sleep(5)

    @TestLogger.log('点击长按录像')
    def press_long_phone(self):
        self.press(self.get_element(self.__locators["照相"]), wait_time=3)

    @TestLogger.log('等待视频播放页面跳转')
    def wait_for_page_video(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["视频播放页面"]),
                timeout=timeout,
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log('点击发送')
    def click_cancel_send(self):
        self.click_element(self.__locators["撤回"])
