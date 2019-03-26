from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage


class CallPage(FooterPage):
    """通话页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        'tip1': (MobileBy.ID, 'com.cmic.college:id/ivFreeCall'),
        'tip2': (MobileBy.ID, 'com.cmic.college:id/ivKeyboard'),
        'tip3': (MobileBy.ID, 'com.cmic.college:id/tvContact'),
        '视频': (MobileBy.ID, 'com.cmic.college:id/ivMultipartyCall'),

    }

    @TestLogger.log('点击通话引导页')
    def click_contact_tip(self):
        self.click_element(self.__locators['tip1'])
        self.click_element(self.__locators['tip2'])
        self.click_element(self.__locators['tip3'])

    @TestLogger.log('等待页面自动跳转')
    def wait_for_page_call(self, max_wait_time=8):
        self.wait_until(
            condition=lambda d: self.is_text_present("不花钱打电话"),
            timeout=max_wait_time,
        )

    @TestLogger.log('是否在通话页面')
    def is_on_this_page(self):
        el = self.get_elements(self.__locators['视频'])
        if len(el) > 0:
            return True
        return False

