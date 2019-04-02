import time
from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChartProfilePage(BasePage):
    """单聊-联系人profile页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'
    __locators = {
        '返回': (MobileBy.ID, 'com.cmic.college:id/left_back_btn'),
        '联系人头像': (MobileBy.ID, 'com.cmic.college:id/profile_photo'),
        '联系人名称': (MobileBy.ID, 'com.cmic.college:id/profile_name'),
        '视频': (MobileBy.ID, 'com.cmic.college:id/iv_netcall'),
        '消息': (MobileBy.ID, 'com.cmic.college:id/iv_message'),
        '手机号码': (MobileBy.ID, 'com.cmic.college:id/tv_phone_number'),
        '给TA打电话': (MobileBy.ID, 'com.cmic.college:id/bt_free_call'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('等待联系人profile页面跳转')
    def wait_for_page_chart_profile(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["给TA打电话"]),
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

    @TestLogger.log("点击消息入口")
    def click_profile_message(self):
        self.click_element(self.__locators["消息"])

    @TestLogger.log("点击视频入口")
    def click_profile_video(self):
        self.click_element(self.__locators["视频"])
