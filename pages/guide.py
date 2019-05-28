from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time

class GuidePage(BasePage):
    """fg"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.SplashActivity'

    __locators = {
        'Banner': (MobileBy.ID, 'com.cmic.college:id/splash_view_pager'),
        'iv': (MobileBy.ID, 'com.cmic.college:id/iv'),
        # 体验页面
        '去体验': (MobileBy.ID, 'com.cmic.college:id/btn_update'),
        '不再提醒': (MobileBy.ID, 'com.cmic.college:id/select_checkbox'),
        '不去体验': (MobileBy.ID, 'com.cmic.college:id/btn_not_update'),
        # 发现新版本页面
        '暂不升级': (MobileBy.XPATH, '//*[@text="暂不升级"]'),
        #权限页
        '一键开启':(MobileBy.ID, 'com.cmic.college:id/btnConfirm'),
        '禁止':(MobileBy.ID, 'com.android.packageinstaller:id/permission_deny_button'),
        '始终允许': (MobileBy.ID, 'com.android.packageinstaller:id/permission_allow_button'),

    }

    @TestLogger.log()
    def click_cancel_update(self):
        """点击不再提醒"""
        self.click_element(self.__locators["暂不升级"], 25)

    @TestLogger.log()
    def click_the_checkbox(self):
        """点击不再提醒"""
        self.click_element(self.__locators["不再提醒"], 15)

    @TestLogger.log()
    def click_the_first_start_experience(self):
        """点击去体验"""
        self.click_element(self.__locators["去体验"])

    @TestLogger.log()
    def click_the_no_start_experience(self):
        """点击不去体验"""
        self.click_element(self.__locators["不去体验"])

    @TestLogger.log()
    def click_one_button_on(self):
        """点击一键开启"""
        if self.page_should_contain_text('一键开启'):
            self.click_element(self.__class__.__locators['一键开启'])
            time.sleep(2)

    @TestLogger.log()
    def click_always_allow(self):
        """权限框-点击始终允许"""
        self.click_text('始终允许')
        time.sleep(2)
        self.click_text('始终允许')
        time.sleep(2)
        self.click_text('始终允许')
        time.sleep(8)

    @TestLogger.log()
    def is_on_the_first_guide_page(self):
        """判断当前页是否在引导页第一页"""
        flag = self._is_element_present(self.__locators["iv"])
        return flag

    @TestLogger.log()
    def swipe_to_the_second_banner(self):
        """从引导页第一屏左滑到第二屏"""
        try:

            self.wait_until(
                timeout=5,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__locators["iv"])
            )
        except:
            raise AssertionError('页面没有包含文本：真实号码来电')
        self.swipe_by_direction(self.__class__.__locators['Banner'], 'left', 200)
        return self

    @TestLogger.log()
    def swipe_to_the_third_banner(self):
        """从引导页第二屏左滑到第三屏"""
        try:
            self.wait_until(
                timeout=6,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__locators["iv"])
            )
        except:
            raise AssertionError('页面没有包含文本：视频涂鸦表情斗图')
        self.swipe_by_direction(self.__class__.__locators['Banner'], 'left', 200)
        return self

    @TestLogger.log()
    def click_start_the_experience(self):
        """点击引导页第三屏的开始体验"""
        try:
            self.wait_until(
                timeout=7,
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present("立即体验")
            )
        except:
            raise AssertionError('页面没有包含文本：立即体验')
        self.click_text("立即体验", True)
        return self

    @TestLogger.log()
    def click_start_the_one_key(self):
        """点击引导页的一键开启"""
        try:
            self.wait_until(
                timeout=5,
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present("一键开启")
            )
        except:
            raise AssertionError('页面没有包含文本：一键开启')
        self.click_text("一键开启", True)
        return self

    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待页面进入引导页第一页（自动允许权限）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators["iv"])
            )
        except:
            message = "引导页首页在限定的时间：{}s内没有加载完毕，或者没有包含文本：时长福利多".format(timeout)
            raise AssertionError(
                message
            )
        return self
