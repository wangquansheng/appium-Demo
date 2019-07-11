from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage
from pages.CommonPage import CommonPage


class MinePage(CommonPage):
    """通话页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        '电话号码': (MobileBy.ID, 'com.cmic.college:id/card_photo_num'),
        '请完善你的资料': (MobileBy.ID, 'com.cmic.college:id/card_name_hint'),
        '头像': (MobileBy.ID, 'com.cmic.college:id/card_head_photo'),
        '我的二维码': (MobileBy.ID, 'com.cmic.college:id/action_qr'),
        '积分': (MobileBy.ID, 'com.cmic.college:id/rl_integral'),
        '每日资讯': (MobileBy.ID, 'com.cmic.college:id/rlNews'),
        '看点': (MobileBy.ID, 'com.cmic.college:id/rlNews'),
        '活动中心': (MobileBy.ID, 'com.cmic.college:id/activity_center'),
        '卡券': (MobileBy.ID, 'com.cmic.college:id/web_hall_coupons'),
        '网上营业厅': (MobileBy.ID, 'com.cmic.college:id/web_hall_page'),
        '邀请有礼': (MobileBy.ID, 'com.cmic.college:id/share_app'),
        '帮助与反馈': (MobileBy.ID, 'com.cmic.college:id/feedback'),
        '设置': (MobileBy.ID, 'com.cmic.college:id/setting'),

        '退出当前账号': (MobileBy.ID, 'com.cmic.college:id/logout'),
        '二维码_转到上一层级': (MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="转到上一层级"]'),
        '二维码_更多': (MobileBy.ID, 'com.cmic.college:id/action_more'),
        '二维码图片': (MobileBy.ID, 'com.cmic.college:id/my_twodimensionCode'),
        '分享二维码': (MobileBy.XPATH,
                  '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ListView/android.widget.LinearLayout[1]/android.widget.TextView'),
        '保存二维码': (MobileBy.XPATH,
                  '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ListView/android.widget.LinearLayout[2]/android.widget.TextView'),
        '我二级页面顶部元素': (MobileBy.ID, 'com.cmic.college:id/tv_title_actionbar'),
        '我_二级页面_相同返回': (MobileBy.ID, 'com.cmic.college:id/ibt_back_actionbar'),  # 看点，活动中心，卡券，网上营业厅，邀请有礼，帮助与反馈，
        '分享_密友圈': (MobileBy.ID, 'com.cmic.college:id/tv_miyou'),
        '分享_朋友圈': (MobileBy.ID, 'com.cmic.college:id/tv_circle'),
        '分享_微信': (MobileBy.ID, 'com.cmic.college:id/tv_wechat'),
        '分享_QQ': (MobileBy.ID, 'com.cmic.college:id/tv_qq'),
        '分享_QQ空间': (MobileBy.ID, 'com.cmic.college:id/tv_qzone'),
        '剩余时长_标签': (MobileBy.ID, 'com.cmic.college:id/tv_totalDuraton'),
        '剩余时长_时长': (MobileBy.ID, 'com.cmic.college:id/tv_leftDuration'),
        '剩余时长_单位': (MobileBy.ID, 'com.cmic.college:id/tv_minute'),
    }

    @TestLogger.log("当前页面是否在我的页面")
    def get_locators(self, locator):
        return self.__locators[locator]

    @TestLogger.log("当前页面是否在我的页面")
    def is_on_this_page(self):
        """当前页面是否在我的页面"""
        el = self.get_elements(self.__locators['电话号码'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log("点击照片按钮并编辑资料")
    def click_personal_photo(self):
        """点击查看并编辑资料按钮"""
        self.click_element(self.__locators['头像'])

    # @TestLogger.log("点击locators对应的元素")
    # def click_locator_key(self, locator):
    #     self.click_element(self.__locators[locator])

    @TestLogger.log("当前页面是否包含此文本")
    def is_text_exist(self, text):
        """当前页面是否包含此文本"""
        return self.is_text_present(text)

    @TestLogger.log('判断该元素是否能点击')
    def element_is_clickable(self, text):
        return self._is_clickable(self.__locators[text])

    @TestLogger.log('检测二维码是否存在')
    def check_qr_code_exist(self):
        from pyzbar import pyzbar
        import io
        from PIL import Image
        screen_shot = self.mobile.get_element(self.__locators['二维码图片']).screenshot_as_png
        fp = io.BytesIO(screen_shot)
        qr = pyzbar.decode(Image.open(fp))
        if qr:
            return True
        raise AssertionError('不是有效的二维码')

    @TestLogger.log('判断该元素是否可编辑')
    def element_is_enable(self, text):
        return self._is_enabled(self.__locators[text])

    @TestLogger.log('获得元素的文本')
    def get_element_text(self, text):
        return self.get_text(self.__locators[text])

    @TestLogger.log("当前页面是否包含此文本")
    def is_text_exist(self, text):
        """当前页面是否包含此文本"""
        return self.is_text_present(text)

    @TestLogger.log('我二级页面顶部元素是否为text文本')
    def check_wait_text_exits(self, text, timeout=20):
        bol = self.wait_until(
            condition=lambda d: self.is_text_present(text), timeout=timeout
            , auto_accept_permission_alert=False)
        return bol

    @TestLogger.log("判断元素是否存在")
    def check_element_name_photo_exist(self):
        """当前页面元素是否存在"""
        el1 = self.get_elements((MobileBy.ID, 'com.cmic.college:id/twodimensioncode_myprofile_icon'))
        el2 = self.get_elements((MobileBy.ID, 'com.cmic.college:id/twodimension_name_text'))
        if len(el1) > 0 and len(el2) > 0:
            return True
        return False
