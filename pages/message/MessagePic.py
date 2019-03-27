import time

from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MessagePicPage(BasePage):
    """消息页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'
    # "../android.widget.RelativeLayout/android.widget.ImageView[2][not(contains(@resource-id,'com.cmic.college:id/iv_video_icon'))]"
    __locators = {
        '返回': (MobileBy.XPATH, '//*[@content-desc="转到上一层级"]'),
        '选择图片': (MobileBy.XPATH, '//*[@text="选择图片"]'),
        '所用图片': (MobileBy.XPATH,
                 "//*[@resource-id='com.cmic.college:id/iv_select']/../android.widget.ImageView[2][not(contains(@resource-id,'com.cmic.college:id/iv_video_icon'))]"),
        '所用视频': (MobileBy.XPATH,
                 "//*[@resource-id='com.cmic.college:id/iv_video_icon']/../android.widget.ImageView[@resource-id='com.cmic.college:id/iv_select']"),
        '勾选': (MobileBy.ID, 'com.cmic.college:id/iv_select'),
        '预览': (MobileBy.ID, 'com.cmic.college:id/tv_preview'),
        '原图': (MobileBy.ID, 'com.cmic.college:id/cb_original_photo'),
        '发送': (MobileBy.ID, 'com.cmic.college:id/button_send'),

    }

    @TestLogger.log('点击所用视频')
    def click_add(self):
        self.click_element(self.__locators['所用视频'])

    @TestLogger.log('点击所用图片')
    def select_pic(self, n):
        pics = self.get_elements(self.__locators['所用图片'])
        if n > len(pics):
            raise AssertionError("在所有照片首页没有 %s 张图片，请上传图片." % n)
        for i in range(n):
            pics[i].click()

    @TestLogger.log('是否在消息页面')
    def is_on_this_page(self):
        el = self.get_elements(self.__locators['选择图片'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log('等待选择图片页面跳转')
    def wait_for_page_select_pic(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["所用图片"]),
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

    @TestLogger.log('点击所用图片可勾选')
    def is_select_pic(self):
        try:
            pics = self.get_elements(self.__locators['勾选'])
            for i in range(len(pics)):
                pics[i].click()
                time.sleep(0.5)
                pics[i].click()
            return True
        except:
            raise AssertionError("该元素不可点击")

    @TestLogger.log('获取发送的内容')
    def get_pic_send_info(self):
        el = self.get_element(self.__locators["发送"])
        return el.text

    @TestLogger.log('获取按钮是否可点击')
    def is_click(self):
        return self._is_enabled(self.__locators["预览"])

    @TestLogger.log('点击预览')
    def click_pre_view(self):
        self.click_element(self.__locators["预览"])

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators["返回"])

