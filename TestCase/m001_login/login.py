import re
import time
import unittest
import warnings

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages.call.CallPage import CallPage

from pages.guide import GuidePage
from pages.login.LoginPage import OneKeyLoginPage
from preconditions.BasePreconditions import LoginPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


# class LoginTest(TestCase):
#     """Login 模块"""
#
#     def setUp_test_login_0001(self):
#         """"""
#         mb = switch_to_mobile('M960BDQN229CH1')
#         mb.connect_mobile()
#         self.gd = GuidePage()
#         self.gd.mobile.reset_app()
#         self.gd.wait_for_page_load()
#         self.gd.swipe_by_percent_on_screen(90, 50, 10, 50, 600)
#         self.gd.swipe_by_percent_on_screen(90, 50, 10, 50, 600)
#         mb.click_text('立即体验')
#         mb.click_text('一键开启')
#         mb.click_text('本机号码一键登录')
#         mb.click_text('确定')
#
#     @tags('DEMO')
#     def test_login_0001(self):
#         """ 本网非首次登录已设置头像-一键登录页面元素检查"""
#         import time
#         time.sleep(4)
#         self.gd.mobile.assert_screen_contain_text('本机号码')

class Preconditions(LoginPreconditions):
    """
    分解前置条件
    """

    @staticmethod
    def select_single_cmcc_android_4g_client():
        """
        启动
        1、4G，安卓客户端
        2、移动卡
        :return:
        """
        client = switch_to_mobile(REQUIRED_MOBILES['测试机'])
        client.connect_mobile()

    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def select_assisted_mobile2():
        """切换到单卡、异网卡Android手机 并启动应用"""
        switch_to_mobile(REQUIRED_MOBILES['辅助机2'])
        current_mobile().connect_mobile()

    # @staticmethod
    # def login_by_one_key_login():
    #     """
    #     从一键登录页面登录
    #     :return:
    #     """
    #     # 等待号码加载完成后，点击一键登录
    #     one_key = OneKeyLoginPage()
    #     one_key.wait_for_tell_number_load(60)
    #     login_number = one_key.get_login_number()
    #     one_key.click_one_key_login()
    #     one_key.click_sure_login()
    #     # 等待消息页
    #     gp = GuidePage()
    #     try:
    #         gp.click_cancel_update()
    #         # gp.click_the_checkbox()
    #         # gp.click_the_no_start_experience()
    #     except:
    #         gp.click_text("暂不升级")
    #         pass
    #     cp = CallPage()
    #     cp.click_contact_tip()
    #     return login_number

    @staticmethod
    def app_start_for_the_first_time():
        """首次启动APP（使用重置APP代替）"""
        current_mobile().reset_app()

    @staticmethod
    def terminate_app():
        """
        强制关闭app,退出后台
        :return:
        """
        app_id = current_driver().capabilities['appPackage']
        current_mobile().terminate_app(app_id)

    @staticmethod
    def background_app(seconds):
        """后台运行"""
        current_mobile().background_app(seconds)

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.cmic.college'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    # @staticmethod
    # def make_already_in_call_page():
    #     """
    #     前置条件：
    #     1.已登录客户端
    #     2.当前在通话页面
    #     """
    #     # 如果当前页面是在通话录页，不做任何操作
    #     call_page = CallPage()
    #     if call_page.is_on_this_page():
    #         return
    #     # 如果当前页面已经是一键登录页，进行一键登录页面
    #     one_key = OneKeyLoginPage()
    #     if one_key.is_on_this_page():
    #         Preconditions.login_by_one_key_login()
    #         return
    #     # 如果当前页不是引导页第一页，重新启动app
    #     guide_page = GuidePage()
    #     if not guide_page.is_on_the_first_guide_page():
    #         current_mobile().launch_app()
    #         guide_page.wait_for_page_load(20)
    #         # 跳过引导页
    #     Preconditions.make_already_in_one_key_login_page()
    #     Preconditions.login_by_one_key_login()


class LoginTest(TestCase):
    """Login 模块"""

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)

    @staticmethod
    def setUp_test_login_0001():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        # Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_login_0001(self):
        """ 本网正常网络首次登录4G-登录响应"""
        oklp = OneKeyLoginPage()
        # 检查一键登录
        oklp.wait_for_page_load()
        oklp.wait_for_tell_number_load(timeout=10)
        # 检查电话号码
        phone_numbers = current_mobile().get_cards(CardType.CHINA_MOBILE)
        oklp.assert_phone_number_equals_to(phone_numbers[0])

    @staticmethod
    def setUp_test_login_0002():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_login_0002(self):
        """ 本网正常网络首次登录4G-登录响应成功"""
        # 1.点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_tell_number_load(60)
        one_key.click_one_key_login()
        one_key.click_agree_user_aggrement()
        one_key.click_agree_login_by_number()
        # 已登录密友圈
        cp = CallPage()
        call_page = CallPage()
        call_page.wait_for_page_call_load()
        call_page.click_always_allow_c()
        time.sleep(2)
        call_page.remove_mask_c(2)
        time.sleep(2)
        self.assertEquals(cp.is_on_this_page(), True)

    @staticmethod
    def setUp_test_login_0003():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_login_0003(self):
        """ 一键登录协议响应"""
        # 1.点击《密友圈软件许可及服务协议》按钮
        one_key = OneKeyLoginPage()
        one_key.wait_for_tell_number_load(60)
        one_key.click_license_agreement()
        time.sleep(15)
        # 2.跳转至服务协议H5页面
        one_key.page_should_contain_text("密友圈")
