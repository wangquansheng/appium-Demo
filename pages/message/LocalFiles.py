import time

from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class LocalFilesPage(BasePage):
    """消息—文件页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'
    __locators = {
        '返回': (MobileBy.XPATH, '//*[@content-desc="转到上一层级"]'),
        '本地文件夹': (MobileBy.XPATH, '//*[@text="本地文件夹"]'),
        '照片': (MobileBy.ID, 'com.cmic.college:id/tv_pic'),
        '音乐': (MobileBy.ID, 'com.cmic.college:id/tv_music'),
        '视频': (MobileBy.ID, 'com.cmic.college:id/tv_vedio'),
        '本地文件': (MobileBy.ID, 'com.cmic.college:id/tv_mobile_memory'),
        # 打开照片后
        '照片文件': (MobileBy.ID, 'com.cmic.college:id/rl_sd_file'),
        '发送': (MobileBy.ID, 'com.cmic.college:id/tv_send'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('等待选择文件夹页面跳转')
    def wait_for_page_select_files(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["本地文件夹"]),
                timeout=timeout,
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log('等待选择文件夹发送页面跳转')
    def wait_for_page_select_send_files(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["发送"]),
                timeout=timeout,
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log('点击选择照片')
    def click_select_pic(self):
        self.click_element(self.__locators['照片'])

    @TestLogger.log('点击选择照片文件')
    def click_select_pic_file(self):
        self.click_element(self.__locators['照片文件'])

    @TestLogger.log('点击发送')
    def click_select_send(self):
        self.click_element(self.__locators['发送'])

    @TestLogger.log("检查该页面包含元素")
    def page_contain_ele(self, menu):
        for text in menu:
            self._is_element_present(self.__locators[text])
        return True
