from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage


class NewMessagePage(FooterPage):
    """新建消息页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {
        '搜索联系人或手机号': (MobileBy.ID, '	com.cmic.college:id/editText_keyword'),
        '#': (MobileBy.ID, 'com.cmic.college:id/alphabetIndexText'),
        '联系人图标': (MobileBy.ID, 'com.cmic.college:id/contact_icon'),
        '联系人电话': (MobileBy.ID, 'com.cmic.college:id/contact_number'),
        '联系人姓名': (MobileBy.ID, 'com.cmic.college:id/contact_name'),
    }

    @TestLogger.log('点击通话引导页')
    def click_contact_one(self, n=1):
        els = self.get_elements(self.__locators["联系人电话"])
        if n > len(els):
            raise AssertionError("暂无联系人，请添加")
        for i in range(n):
            els[i].click()

    @TestLogger.log('等待页面自动跳转')
    def wait_for_page_new_message(self, max_wait_time=8):
        self.wait_until(
            condition=lambda d: self.is_text_present("搜索联系人或手机号"),
            timeout=max_wait_time,
        )

    @TestLogger.log('是否在通话页面')
    def is_on_this_page(self):
        el = self.get_elements(self.__locators['搜索联系人或手机号'])
        if len(el) > 0:
            return True
        return False
