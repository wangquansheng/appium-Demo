import time
from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupCodePage(BasePage):
    """群聊-二维码"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'
    __locators = {
        '返回': (MobileBy.XPATH, '//*[@content-desc="转到上一层级"]'),
        '群二维码': (MobileBy.XPATH, '//*[@text="群二维码"]'),
        '群头像': (MobileBy.ID, 'com.cmic.college:id/photo'),
        '群名称': (MobileBy.ID, 'com.cmic.college:id/group_qr_name'),
        '群二维码内容': (MobileBy.ID, 'com.cmic.college:id/group_qr_icon'),
        '群聊说明': (MobileBy.ID, 'com.cmic.college:id/group_qr_date'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('等待群二维码页面跳转')
    def wait_for_page_group_code(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["群二维码内容"]),
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
