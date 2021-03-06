from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger
from pages.CommonPage import CommonPage


class FooterPage(CommonPage):
    """主页页脚标签栏"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        '我': (MobileBy.ID, 'com.cmic.college:id/tvMe'),
        '消息': (MobileBy.ID, 'com.cmic.college:id/tvMessage'),
        '通讯录': (MobileBy.ID, 'com.cmic.college:id/tvContact'),
        '密友': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
        '通话': (MobileBy.ID, 'com.cmic.college:id/tvCall'),
    }

    @TestLogger.log()
    def open_me_page(self):
        """切换到标签页：我"""
        self.click_element(self.__locators['我'])

    @TestLogger.log()
    def open_message_page(self):
        """切换到标签页：消息"""
        self.click_element(self.__locators['消息'])

    @TestLogger.log()
    def open_call_page(self):
        """切换到标签页：通话"""
        self.click_element(self.__locators['通话'])

    @TestLogger.log()
    def open_contact_page(self):
        """切换到标签页：通讯录"""
        self.click_element(self.__locators['通讯录'])

    @TestLogger.log()
    def open_friend_page(self):
        """切换到标签页：密友"""
        self.click_element(self.__locators['密友'])
