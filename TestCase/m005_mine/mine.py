import re
import time
import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages.call.CallPage import CallPage

from pages.guide import GuidePage
from pages.login.LoginPage import OneKeyLoginPage
from pages.mine.MeEditProfile import MeEditProfilePage
from pages.mine.mine import MinePage
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

    # @staticmethod
    # def select_mobile(category):
    #     """选择手机手机"""
    #     client = switch_to_mobile(REQUIRED_MOBILES[category])
    #     client.connect_mobile()
    #     return client

    @staticmethod
    def select_assisted_mobile2():
        """切换到单卡、异网卡Android手机 并启动应用"""
        switch_to_mobile(REQUIRED_MOBILES['辅助机2'])
        current_mobile().connect_mobile()

    # @staticmethod
    # def make_already_in_one_key_login_page():
    #     """
    #     1、已经进入一键登录页
    #     :return:
    #     """
    #     # 如果当前页面已经是一键登录页，不做任何操作
    #     one_key = OneKeyLoginPage()
    #     if one_key.is_on_this_page():
    #         return
    #     # 如果当前页不是引导页第一页，重新启动app
    #     guide_page = GuidePage()
    #     if not guide_page.is_on_the_first_guide_page():
    #         current_mobile().launch_app()
    #         guide_page.wait_for_page_load(20)
    #
    #     # 跳过引导页
    #     guide_page.wait_for_page_load(30)
    #     guide_page.swipe_to_the_second_banner()
    #     guide_page.swipe_to_the_third_banner()
    #     guide_page.click_start_the_experience()
    #     guide_page.click_start_the_one_key()

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
    #         gp.click_the_checkbox()
    #         gp.click_the_no_start_experience()
    #     except:
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
    #     2.当前在消息页面
    #     """
    #     # 如果当前页面是在通话录页，不做任何操作
    #     call_page = CallPage()
    #     if call_page.is_on_this_page():
    #         return
    #     # 如果当前页面已经是一键登录页，进行一键登录页面
    #     one_key = OneKeyLoginPage()
    #     if one_key.is_on_this_page():
    #         Preconditions.login_by_one_key_login()
    #     # 如果当前页不是引导页第一页，重新启动app
    #     else:
    #         try:
    #             current_mobile().terminate_app('com.cmic.college', timeout=2000)
    #         except:
    #             pass
    #         current_mobile().launch_app()
    #         try:
    #             call_page.wait_until(
    #                 condition=lambda d: call_page.is_on_this_page(),
    #                 timeout=3
    #             )
    #             return
    #         except TimeoutException:
    #             pass
    #         Preconditions.reset_and_relaunch_app()
    #         Preconditions.make_already_in_one_key_login_page()
    #         Preconditions.login_by_one_key_login()

    @staticmethod
    def make_already_in_me_page():
        """确保应用在消息页面"""
        # 如果在消息页，不做任何操作
        call_page = CallPage()
        me_page = MinePage()
        if me_page.is_on_this_page():
            return
        if call_page.is_on_this_page():
            call_page.open_me_page()
            me_page.is_on_this_page()
            return
        # 进入一键登录页
        Preconditions.make_already_in_call_page()
        call_page.open_me_page()

    @staticmethod
    def make_already_in_me_profilePage():
        Preconditions.make_already_in_me_page()
        me_page = MinePage()
        me_page.click_personal_photo()


class MineTest(TestCase):
    """Mine 模块"""

    @staticmethod
    def setUp_test_me_0001():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0001(self):
        """资料页面的字段可显示并且可以编辑"""
        me_page = MinePage()
        self.assertEqual(me_page.is_on_this_page(), True)
        me_page.click_personal_photo()
        meEdit_page = MeEditProfilePage()
        time.sleep(2)
        self.assertEqual(meEdit_page.is_text_exist("昵称"), True)
        self.assertEqual(meEdit_page.is_text_exist("性别"), True)
        self.assertEqual(meEdit_page.is_text_exist("年龄"), True)
        self.assertEqual(meEdit_page.is_text_exist("我的标签"), True)
        self.assertEqual(meEdit_page.is_text_exist("职业"), True)
        meEdit_page.click_profile_photo()
        meEdit_page.click_photo_back()
        time.sleep(2)
        self.assertEqual(meEdit_page.element_is_clickable("电话"), False)
        self.assertEqual(meEdit_page.element_is_clickable("昵称"), True)
        self.assertEqual(meEdit_page.element_is_clickable("性别"), True)
        self.assertEqual(meEdit_page.element_is_clickable("年龄"), True)
        self.assertEqual(meEdit_page.element_is_clickable("我的标签"), True)
        self.assertEqual(meEdit_page.element_is_clickable("职业"), True)

    @staticmethod
    def setUp_test_me_0002():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0002(self):
        """编辑资料页面里面点击头像"""
        me_page = MinePage()
        self.assertEqual(me_page.is_on_this_page(), True)
        me_page.click_personal_photo()
        meEdit_page = MeEditProfilePage()
        meEdit_page.click_profile_photo()
        meEdit_page.click_photo_more()
        time.sleep(2)
        meEdit_page.element_is_clickable('从手机相册选择')
        meEdit_page.element_is_clickable('保存到手机')

    @staticmethod
    def setUp_test_me_0003():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0003(self):
        """编辑资料页面昵称里面输入sql语句"""
        me_page = MinePage()
        self.assertEqual(me_page.is_on_this_page(), True)
        me_page.click_personal_photo()
        meEdit_page = MeEditProfilePage()
        meEdit_page.input_profile_name('昵称', 'select * from')
        meEdit_page.click_save()
        self.assertTrue(meEdit_page.check_text_exist('保存成功'))

    @staticmethod
    def setUp_test_me_0004():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0004(self):
        """编辑资料页面昵称里面输入字符串"""
        me_page = MinePage()
        self.assertEqual(me_page.is_on_this_page(), True)
        me_page.click_personal_photo()
        meEdit_page = MeEditProfilePage()
        meEdit_page.input_profile_name('昵称', r"<>'\"&\n\r")
        meEdit_page.click_save()
        self.assertTrue(meEdit_page.check_text_exist('保存成功'))

    @staticmethod
    def setUp_test_me_0005():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0005(self):
        """编辑资料页面昵称里面输入数字"""
        me_page = MinePage()
        self.assertEqual(me_page.is_on_this_page(), True)
        me_page.click_personal_photo()
        meEdit_page = MeEditProfilePage()
        meEdit_page.input_profile_name('昵称', '4135435')
        meEdit_page.click_save()
        self.assertTrue(meEdit_page.check_text_exist('保存成功'))

    @staticmethod
    def setUp_test_me_0006():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_profilePage()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0006(self):
        """点击性别选项选择性别"""
        me_edit_page = MeEditProfilePage()
        me_edit_page.input_random_name()
        me_edit_page.click_locator_key('性别')
        me_edit_page.click_locator_key('性别_男')
        me_edit_page.click_locator_key('保存')
        self.assertTrue(me_edit_page.check_text_exist('保存成功'))

    @tags('ALL', 'SMOKE', 'CMCC')
    def setUp_test_me_0007(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_profilePage()

    def test_me_0007(self):
        """编辑年龄选项选择年龄"""
        me_edit_page = MeEditProfilePage()
        me_edit_page.input_random_name()
        me_edit_page.click_locator_key('年龄')
        me_edit_page.click_locator_key('年龄_90后')
        me_edit_page.click_locator_key('保存')
        self.assertTrue(me_edit_page.check_text_exist('保存成功'))

    @tags('ALL', 'SMOKE', 'CMCC')
    def setUp_test_me_0008(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_profilePage()

    def test_me_0008(self):
        """编辑标签选项选择标签"""
        me_edit_page = MeEditProfilePage()
        me_edit_page.click_locator_key('我的标签')
        time.sleep(2)
        me_edit_page.click_locator_key('添加个性标签')
        me_edit_page.click_locator_key('标签取消')
        for i in range(6):
            me_edit_page.click_tag_index('标签', i)
        self.assertTrue(me_edit_page.check_text_exist('最多选择5个标签来形容自己'))

    @tags('ALL', 'SMOKE', 'CMCC')
    def setUp_test_me_0009(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_profilePage()

    def test_me_0009(self):
        """编辑职业选项选择职业"""
        me_edit_page = MeEditProfilePage()
        me_edit_page.input_random_name()
        me_edit_page.click_locator_key('职业')
        me_edit_page.click_locator_key('职业_计算机')
        me_edit_page.click_locator_key('保存')
        self.assertTrue(me_edit_page.check_text_exist('保存成功'))

    @tags('ALL', 'SMOKE', 'CMCC')
    def setUp_test_me_0010(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    def test_me_0010(self):
        """查看我的二维码页面显示"""
        me_page = MinePage()
        me_page.click_locator_key('我的二维码')
        self.assertTrue(me_page.element_is_clickable('二维码_转到上一层级'))
        self.assertTrue(me_page.element_is_clickable('二维码_更多'))
        self.assertTrue(me_page.is_text_exist('我的二维码'))
        self.assertTrue(me_page.is_text_exist('密友圈扫描二维码，添加我为密友'))
        self.assertTrue(me_page.check_qr_code_exist())
        self.assertTrue(me_page.check_element_name_photo_exist())

    @tags('ALL', 'SMOKE', 'CMCC')
    def setUp_test_me_0011(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    def test_me_0011(self):
        """个人二维码点击更多"""
        me_page = MinePage()
        me_page.click_locator_key('我的二维码')
        me_page.click_locator_key('二维码_更多')
        time.sleep(2)
        self.assertEqual(me_page.get_element_text('分享二维码'), '分享我的二维码')
        self.assertTrue(me_page.element_is_enable('分享二维码'))
        self.assertEqual(me_page.get_element_text('保存二维码'), '保存二维码图片')
        self.assertTrue(me_page.element_is_enable('保存二维码'))

    @tags('ALL', 'SMOKE', 'CMCC')
    def setUp_test_me_0012(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    def test_me_0012(self):
        """个人二维码点击更多"""
        me_page = MinePage()
        me_page.click_locator_key('我的二维码')
        me_page.click_locator_key('二维码_更多')
        me_page.click_locator_key('分享二维码')
        self.assertEqual(me_page.get_element_text('分享_密友圈'), '密友圈')
        self.assertEqual(me_page.get_element_text('分享_朋友圈'), '朋友圈')
        self.assertEqual(me_page.get_element_text('分享_微信'), '微信')
        self.assertEqual(me_page.get_element_text('分享_QQ'), 'QQ')
        self.assertEqual(me_page.get_element_text('分享_QQ空间'), 'QQ空间')

    @tags('ALL', 'SMOKE', 'CMCC')
    def setUp_test_me_0013(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    def test_me_0013(self):
        """验证活动中心页面正常打开"""
        me_page = MinePage()
        me_page.click_locator_key('活动中心')
        self.assertTrue(me_page.check_wait_text_exits('活动中心'))
        me_page.click_locator_key('我_二级页面_相同返回')

    @tags('ALL', 'SMOKE', 'CMCC')
    def setUp_test_me_0014(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    def test_me_0014(self):
        """验证卡券页面正常打开"""
        me_page = MinePage()
        me_page.click_locator_key('卡券')
        self.assertTrue(me_page.check_wait_text_exits('我的卡券'))
        me_page.click_locator_key('我_二级页面_相同返回')

    @tags('ALL', 'SMOKE', 'CMCC')
    def setUp_test_me_0015(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    def test_me_0015(self):
        """验证网上营业厅正常打开"""
        me_page = MinePage()
        me_page.click_locator_key('网上营业厅')
        self.assertTrue(me_page.check_wait_text_exits('网上营业厅'))
        me_page.click_locator_key('我_二级页面_相同返回')

    @tags('ALL', 'SMOKE', 'CMCC')
    def setUp_test_me_0016(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    def test_me_0016(self):
        """验证邀请有礼正常打开"""
        me_page = MinePage()
        me_page.click_locator_key('邀请有礼')
        self.assertTrue(me_page.check_wait_text_exits('邀请有奖'))
        me_page.click_locator_key('我_二级页面_相同返回')

    @tags('ALL', 'SMOKE', 'CMCC')
    def setUp_test_me_0017(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    def test_me_0017(self):
        """验证帮助与反馈正常打开"""
        me_page = MinePage()
        me_page.click_locator_key('帮助与反馈')
        self.assertTrue(me_page.check_wait_text_exits('帮助与反馈'))
        me_page.click_locator_key('我_二级页面_相同返回')

    @tags('ALL', 'SMOKE', 'CMCC')
    def setUp_test_me_0018(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    def test_me_0018(self):
        """验证邀请有礼正常打开"""
        me_page = MinePage()
        me_page.click_locator_key('设置')
        me_page.click_locator_key('退出当前账号')
        self.assertTrue(me_page.check_wait_text_exits('本机号码一键登录'))
