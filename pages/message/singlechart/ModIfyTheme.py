import time
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChartModifyThemePage(BasePage):
    """单聊-设置-改变主题页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'
    __locators = {
        '返回': (MobileBy.XPATH, '//*[@content-desc="转到上一层级"]'),
        '更改此主题背景': (MobileBy.XPATH, '//*[@text="更改此主题背景"]'),
        '当前主题背景，尝鲜试试其他风格': (MobileBy.ID, 'com.cmic.college:id/tv_hint'),
        '背景图': (MobileBy.ID, 'com.cmic.college:id/ivBackground'),
        '更改框1': (MobileBy.ID, 'com.cmic.college:id/cvOne'),
        '更改框2': (MobileBy.ID, 'com.cmic.college:id/cvTwo'),
        '展示框': (MobileBy.ID, 'com.cmic.college:id/imageViewIcon'),
        '取消': (MobileBy.ID, 'com.cmic.college:id/set_theme_cancel'),
        '应用': (MobileBy.ID, 'com.cmic.college:id/set_theme_confirm'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('等待群设置页面跳转')
    def wait_for_page_single_chart_theme(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["当前主题背景，尝鲜试试其他风格"]),
                timeout=timeout,
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log("检查该页面包含元素")
    def page_contain_ele(self, menu):
        for text in menu:
            self._is_element_present(self.__locators[text])
        return True

    @TestLogger.log("检查该页面包含文本")
    def page_contain_text(self, menu):
        for text in menu:
            self.is_text_present(text)
        return True

    @TestLogger.log("左一页")
    def page_left(self):
        """向左滑动"""
        self.swipe_by_percent_on_screen(20, 50, 90, 50, 1000)

    @TestLogger.log("右一页")
    def page_right(self):
        """向右滑动"""
        self.swipe_by_percent_on_screen(90, 50, 20, 50, 1000)

    @TestLogger.log('点击取消')
    def click_cancel(self):
        self.click_element(self.__locators['取消'])

    @TestLogger.log('点击确认')
    def click_sure(self):
        self.click_element(self.__locators['应用'])
