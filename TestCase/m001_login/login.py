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


class LoginTest(TestCase):
    """Login 模块"""

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)

    @staticmethod
    def setUp_test_login_0001():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'CMCC', 'login')
    def test_login_0001(self):
        """
            取消首次登录时登录按钮的置灰显示	"1、正常网络
            2、当前在一键登录页面
            3、用户首次登录"	"1、查看页面显示
            2、点击本机号码一键登录按钮
            3、点击不同意
            4、同2步骤，点击同意
            5、点击确定按钮"	"1、文案“登录即代表阅读并同意《软件许可服务协议》和《隐私和信息保护政策》”显示在底部，无勾选框，登录按钮高亮显示
            2、弹出“用户协议和隐私保护，
            欢迎使用密友圈，我们非常重视保护您的个人协议并严格遵守相关法律法规。
            我们会根据国家相关法律法规不定时更新我们的软件许可协议和隐私协议，您可通过《软件许可服务协议》和《隐私和信息保护政策》查看详细条款，请您在使用密友圈前务必仔细阅读。
            点击下方“同意”按钮，方可开始使用密友圈，与此同时我们将竭力保护您的隐私安全
            ”同意与不同意按钮
            3、弹窗消失，停留当前页面
            4、弹出“使用号码XXXX登录，登录后，在密友圈app内的视频通话、语音通话和聊天将使用该号码发起”确定按钮
            5、成功进入密友圈"
            :return:
        """
        login = OneKeyLoginPage()
        # 检查一键登录
        cards = login.get_cards_c(CardType.CHINA_MOBILE)
        login.wait_for_page_load()
        login.wait_for_tell_number_load(timeout=10)
        login.click_text('一键登录')
        time.sleep(1)
        if login.is_text_present_c('用户协议和隐私保护'):
            login.click_locator_key_c('不同意')
            time.sleep(0.5)
        self.assertEqual(login.is_text_present_c('使用{}一键登录'.format((cards[0]))), True)
        login.click_text('一键登录')
        time.sleep(1)
        if login.is_text_present_c('用户协议和隐私保护'):
            login.click_locator_key_c('同意')
        call = CallPage()
        call.is_text_present_c('通话', default_timeout=20)
        time.sleep(2)
        call.click_always_allow_c()
        time.sleep(3)
        call.remove_mask_c(2)
        self.assertEqual(call.is_on_this_page(), True)

    @staticmethod
    def setUp_test_login_0003():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        # Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'CMCC', 'me')
    def test_login_0003(self):
        """ 非首次登陆	"1、正常网络
            2、当前在一键登录页面
            3、用户非首次登录"	"1、点击一键登陆
            2、点击确认使用XX号码登录"	成功登陆密友，进入通话页面
        """

        login = OneKeyLoginPage()
        if login.is_text_present_c('一键登录'):
            login.wait_for_tell_number_load(20)
            login.click_text('一键登录')
            if login.is_text_present_c('用户协议和隐私保护'):
                login.click_locator_key_c('同意')
        call = CallPage()
        call.is_text_present_c('通话', default_timeout=20)
        time.sleep(2)
        call.click_always_allow_c()
        time.sleep(3)
        call.remove_mask_c(2)
        self.assertEqual(login.is_text_present_c("通话"), True)
