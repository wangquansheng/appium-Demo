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

        '呼叫': (MobileBy.ID, 'com.cmic.college:id/tv_sure'),
        '视频通话_第一个联系人': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.ListView/android.widget.LinearLayout[1]/android.widget.RelativeLayout'),
        '视频通话_第二个联系人': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.ListView/android.widget.LinearLayout[1]/android.widget.RelativeLayout'),

        '删除_一条通话记录': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]'),
        '删除_全部通话记录': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[2]'),

        '联系人_详情图标': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.view.ViewGroup/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.ImageView[2]'),
        '详情_视频按钮':  (MobileBy.ID, 'com.cmic.college:id/tvVideoCall'),
        '详情_信息按钮':  (MobileBy.ID, 'com.cmic.college:id/tvSendMessage'),
        '点击返回': (MobileBy.ID, 'com.cmic.college:id/ivBack'),
        '通话类型标签': (MobileBy.ID, 'com.cmic.college:id/tvCallManner'),
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

    @TestLogger.log("点击locators对应的元素")
    def click_locator_key(self, locator):
        self.click_element(self.__locators[locator])

    @TestLogger.log("当前页面是否包含此文本")
    def check_text_exist(self, text):
        """当前页面是否包含此文本"""
        return self.is_text_present(text)

    @TestLogger.log("点击包含文本的元素")
    def click_by_text(self, text):
        """当前页面是否包含此文本"""
        return self.click_text(text)
