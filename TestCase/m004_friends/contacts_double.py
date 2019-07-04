import traceback
import unittest
import uuid
import time
import warnings

from library.core.common.simcardtype import CardType
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.guide import GuidePage
from pages.login.LoginPage import OneKeyLoginPage
from preconditions.BasePreconditions import LoginPreconditions
from pages.call.CallPage import CallPage
from pages.components.Footer import FooterPage
from pages.contacts.contactlocal import ContactsPage

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'Android-移动-N': 'M960BDQN229CH_NOVA',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


# noinspection PyBroadException
class Preconditions(object):
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
    def select_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def select_assisted_mobile2():
        """切换到单卡、异网卡Android手机 并启动应用"""
        switch_to_mobile(REQUIRED_MOBILES['辅助机2'])
        current_mobile().connect_mobile()

    @staticmethod
    def make_already_in_one_key_login_page():
        """
        1、已经进入一键登录页
        :return:
        """
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return
        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        time.sleep(2)
        guide_page.click_always_allow()
        one_key.wait_for_page_load(30)

    @staticmethod
    def login_by_one_key_login():
        """
        从一键登录页面登录
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_page_load()
        # one_key.wait_for_tell_number_load(60)
        one_key.click_one_key_login()
        time.sleep(2)
        if one_key.is_text_present('用户协议和隐私保护'):
            one_key.click_agree_user_aggrement()
            time.sleep(1)
            # one_key.click_agree_login_by_number()
        call_page = CallPage()
        call_page.is_element_already_exist('通话')
        time.sleep(2)
        call_page.remove_mask_c(2)

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

    @staticmethod
    def make_already_in_call_page():
        """
        前置条件：
        1.已登录客户端
        2.当前在消息页面
        """
        # 如果当前页面是在通话录页，不做任何操作
        call_page = CallPage()
        if call_page.is_on_this_page():
            return
        # 如果当前页面已经是一键登录页，进行一键登录页面
        one_key = OneKeyLoginPage()
        try:
            one_key.wait_until(
                condition=lambda d: one_key.is_text_present('一键登录'),
                timeout=15
            )
        except:
            pass
        if one_key.is_text_present('一键登录'):
            Preconditions.login_by_one_key_login()
        # 如果当前页不是引导页第一页，重新启动app
        else:
            try:
                current_mobile().terminate_app('com.cmic.college', timeout=2000)
            except Exception:
                traceback.print_exc()
                pass
            current_mobile().launch_app()
            try:
                call_page.wait_until(
                    condition=lambda d: call_page.is_on_this_page(),
                    timeout=3
                )
                return
            except TimeoutException:
                pass
            Preconditions.reset_and_relaunch_app()
            Preconditions.make_already_in_one_key_login_page()
            Preconditions.login_by_one_key_login()

    @staticmethod
    def make_sure_in_after_login_callpage():
        Preconditions.make_already_in_call_page()
        current_mobile().wait_until_not(condition=lambda d: current_mobile().is_text_present('正在登录...'), timeout=20)

    @staticmethod
    def get_current_activity_name():
        import os, sys
        global findExec
        findExec = 'findstr' if sys.platform == 'win32' else 'grep'
        device_name = current_driver().capabilities['deviceName']
        cmd = 'adb -s %s shell dumpsys window | %s mCurrentFocus' % (device_name, findExec)
        res = os.popen(cmd)
        time.sleep(2)
        # 截取出activity名称 == ''为第三方软件
        current_activity = res.read().split('u0 ')[-1].split('/')[0]
        res.close()
        return current_activity

    @staticmethod
    def initialize_class(moudel):
        """确保每个用例开始之前在通话界面界面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile(moudel)
        Preconditions.make_already_in_call_page()
        FooterPage().open_contact_page()
        contact = ContactsPage()
        contact.permission_box_processing()
        contact.remove_mask_c(1)

    @staticmethod
    def close_system_update():
        """确保每个用例开始之前在通话界面界面"""
        call = CallPage()
        if call.is_text_present_c('系统更新'):
            call.click_text('稍后')
            time.sleep(1)
            call.click_text('取消')

    #
    # @staticmethod
    # def connect_mobiles(category):
    #     """选择手机手机"""
    #     client = switch_to_mobile(REQUIRED_MOBILES[category])
    #     client.connect_mobile()
    #     return client
    #
    # @staticmethod
    # def reset_and_relaunch_app():
    #     """首次启动APP（使用重置APP代替）"""
    #     app_package = 'com.chinasofti.rcs'
    #     current_driver().activate_app(app_package)
    #     current_mobile().reset_app()
    #
    # @staticmethod
    # def terminate_app():
    #     """
    #     强制关闭app,退出后台
    #     :return:
    #     """
    #     app_id = current_driver().desired_capability['appPackage']
    #     current_mobile().termiate_app(app_id)
    #
    # @staticmethod
    # def background_app():
    #     """后台运行"""
    #     current_mobile().press_home_key()
    #
    # @staticmethod
    # def initialize_class(moudel):
    #     """确保每个用例开始之前在通话界面界面"""
    #     warnings.simplefilter('ignore', ResourceWarning)
    #     Preconditions.connect_mobiles(moudel)
    #     Preconditions.make_already_in_call_page()
    #     FooterPage().open_contact_page()
    #     contact = ContactsPage()
    #     contact.permission_box_processing()
    #     contact.remove_mask_c(1)


class ContactlocalPage(TestCase):
    """本地通讯录界面"""

    @classmethod
    def setUp_class(cls):
        warnings.simplefilter('ignore', ResourceWarning)

    def default_setUp(self):
        """确保每个用例开始之前在通讯录界面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_call_page()
        FooterPage().open_contact_page()
        contact = ContactsPage()
        contact.permission_box_processing()
        contact.remove_mask_c(1)

    @tags('ALL', 'CMCC', 'contact')
    def test_member_014(self):
        """
            1、联网正常
            2、已登陆客户端
            3、在通讯录-联系人详情页面
            查看联系人详情元素	复用家庭网详情页面内容，去掉短号栏
        """
        contact_page = ContactsPage()
        contact_page.is_element_already_exist_c('通讯录_标题')
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = contact_page.get_cards_c(CardType.CHINA_MOBILE)[0]
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 确保在通讯录界面
        self.assertEqual(contact_page.is_element_already_exist_c('通讯录_标题'), True)
        # 展开家庭网
        if contact_page.if_home_net_expand():
            contact_page.click_locator_key_c('家庭网_展开_收起')
            time.sleep(1)
        # 点击家庭网第一个联系人
        n = 0
        flag = False
        while n < 8:
            for contact in contact_page.get_elements_list_c('联系人号码'):
                if cards == contact.text:
                    contact.click()
                    flag = True
                    break
            if flag:
                break
            contact_page.page_up()
            n += 1
        time.sleep(3)
        self.assertEqual(contact_page.is_element_already_exist_c('联系人_头像'), True)
        self.assertEqual(contact_page.is_element_already_exist_c('联系人_备注'), True)
        self.assertEqual(contact_page.is_element_already_exist_c('联系人_电话'), True)
        self.assertEqual(contact_page.is_element_already_exist_c('联系人_视频'), True)
        self.assertEqual(contact_page.is_element_already_exist_c('联系人_添加桌面'), True)
        self.assertEqual(contact_page.is_element_already_exist_c('联系人_备注名'), True)
        self.assertEqual(contact_page.is_element_already_exist_c('联系人_备注修改'), True)
        self.assertEqual(contact_page.is_element_already_exist_c('联系人_归属地'), True)
        self.assertEqual(contact_page.is_element_already_exist_c('联系人_长号'), True)
        self.assertEqual(contact_page.is_element_already_exist_c('联系人_更多'), True)
        self.assertEqual(contact_page.is_element_already_exist_c('联系人_更多编辑'), True)
        self.assertEqual(contact_page.is_element_already_exist_c('联系人_规则'), True)

    @tags('ALL', 'CMCC', 'contact')
    def test_member_030(self):
        """
            1、联网正常
            2、已登陆客户端
            3、在通讯录-联系人详情页面
            查看联系人详情元素	复用家庭网详情页面内容，去掉短号栏
        """
        contact_page = ContactsPage()
        contact_page.is_element_already_exist_c('通讯录_标题')
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = contact_page.get_cards_c(CardType.CHINA_MOBILE)[0]
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 确保在通讯录界面
        self.assertEqual(contact_page.is_element_already_exist_c('通讯录_标题'), True)
        # 展开家庭网
        if not contact_page.if_home_net_expand():
            contact_page.click_locator_key_c('家庭网_展开_收起')
            time.sleep(1)
        # 点击家庭网第一个联系人
        n = 0
        flag = False
        while n < 8:
            for contact in contact_page.get_elements_list_c('联系人号码'):
                if cards == contact.text:
                    contact.click()
                    flag = True
                    break
            if flag:
                break
            contact_page.page_up()
            n += 1
        time.sleep(3)
        # 修改备注
        contact_page.click_locator_key_c('联系人_备注修改')
        self.assertEqual(contact_page.is_text_present_c('修改备注名'), True)
        # 清空输入框内容
        contact_page.edit_clear_c('编辑备注_输入框')
        name = '备注'
        contact_page.input_text_c('编辑备注_输入框', name)
        contact_page.click_locator_key_c('编辑备注_保存')
        time.sleep(2)
        contact_page.click_locator_key_c('联系人_视频')
        contact_page.is_text_present_c('正在等待对方接听', default_timeout=20)
        self.assertEqual(contact_page.is_text_present_c(name), True)
        if contact_page.is_element_already_exist_c('视频页面_挂断'):
            contact_page.click_locator_key_c('视频页面_挂断')
