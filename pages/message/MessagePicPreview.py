import time

from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MessagePicPreviewPage(BasePage):
    """消息页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'
    __locators = {
        '返回': (MobileBy.XPATH, '//*[@content-desc="转到上一层级"]'),
        '预览': (MobileBy.XPATH, '//*[@text="预览"]'),
        '编辑': (MobileBy.ID, 'com.cmic.college:id/tvEditPhoto'),
        '图片': (MobileBy.ID, 'com.cmic.college:id/pv_item'),
        '选择框': (MobileBy.ID, 'com.cmic.college:id/iv_select'),
        '原图': (MobileBy.ID, 'com.cmic.college:id/cb_original_photo'),
        '发送1': (MobileBy.ID, 'com.cmic.college:id/btn_send')
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('等待选择预览图片页面跳转')
    def wait_for_page_preview_pic(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["选择框"]),
                timeout=timeout,
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log('点击选择框')
    def click_select_box(self):
        self.click_element(self.__locators['选择框'])

    @TestLogger.log('获取按钮是否可点击')
    def is_click_send(self):
        return self._is_enabled(self.__locators["发送1"])

    @TestLogger.log("左一页")
    def page_left(self):
        """向左滑动"""
        self.swipe_by_percent_on_screen(20, 50, 90, 50, 1000)

    @TestLogger.log("右一页")
    def page_right(self):
        """向右滑动"""
        self.swipe_by_percent_on_screen(90, 50, 20, 50, 1000)
