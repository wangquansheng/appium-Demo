import time
import unittest
import warnings

from library.core.TestLogger import TestLogger
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages.call.CallPage import CallPage
from pages.mine.MeEditProfile import MeEditProfilePage
from pages.mine.MinePage import MinePage
from preconditions.BasePreconditions import LoginPreconditions
from pages.components.Footer import FooterPage

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
    def select_assisted_mobile2():
        """切换到单卡、异网卡Android手机 并启动应用"""
        switch_to_mobile(REQUIRED_MOBILES['辅助机2'])
        current_mobile().connect_mobile()

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
    def relaunch_app():
        """
        重启app
        :return:
        """
        app_id = current_driver().capabilities['appPackage']
        current_mobile().terminate_app(app_id)
        current_mobile().launch_app(app_id)

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
    def make_already_in_me_page():
        """确保应用在消息页面"""
        # 如果在消息页，不做任何操作
        fp = FooterPage()
        call = CallPage()
        me_page = MinePage()
        # 如果icue在我的页面
        if me_page.is_on_this_page():
            return
        # 如果在通话页面
        if call.is_element_already_exist_c('+'):
            fp.open_me_page()
            time.sleep(1)
            return
        # 如果不在我的页面，也不在通话页面，重启app
        # Preconditions.relaunch_app()
        # 进入一键登录页
        Preconditions.make_already_in_call_page()
        fp.open_me_page()
        time.sleep(1)

    @staticmethod
    def make_already_in_me_profilePage():
        """"""
        Preconditions.make_already_in_me_page()
        me_page = MinePage()
        me_page.click_personal_photo()


# noinspection PyPep8Naming
class MineTest(TestCase):
    """Mine 模块"""

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)

    @TestLogger.log('执行SetUp')
    def default_setUp(self):
        """确保每个用例开始之前在我界面"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0001(self):
        """资料页面的字段可显示并且可以编辑"""
        me_page = MinePage()
        time.sleep(1)
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

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0003(self):
        """编辑资料页面昵称里面输入sql语句"""
        me_page = MinePage()
        time.sleep(2)
        self.assertEqual(me_page.is_on_this_page(), True)
        me_page.click_personal_photo()
        meEdit_page = MeEditProfilePage()
        meEdit_page.input_profile_name('昵称', 'selectfrom')
        time.sleep(1)
        meEdit_page.click_save()
        for i in range(3):
            if meEdit_page.is_toast_exist('保存成功', timeout=0.3) \
                    or meEdit_page.is_toast_exist('您的资料未变化', timeout=0.3):
                break

    # @unittest.skip('用例有问题，输入字符串无法保存成功')
    # def test_me_0004(self):
    #     """编辑资料页面昵称里面输入字符串"""
    #     me_page = MinePage()
    #     self.assertEqual(me_page.is_on_this_page(), True)
    #     me_page.click_personal_photo()
    #     meEdit_page = MeEditProfilePage()
    #     meEdit_page.input_profile_name('昵称', r"<>'\"&\n\r")
    #     meEdit_page.click_save()
    #     self.assertTrue(meEdit_page.check_text_exist('保存成功'))

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

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0006(self):
        """点击性别选项选择性别"""
        me_edit_page = MeEditProfilePage()
        MinePage().click_personal_photo()
        time.sleep(0.5)
        me_edit_page.input_random_name()
        me_edit_page.click_locator_key('性别')
        me_edit_page.click_locator_key('性别_男')
        me_edit_page.click_locator_key('保存')
        self.assertTrue(me_edit_page.is_toast_exist('保存成功'), True)

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0007(self):
        """编辑年龄选项选择年龄"""
        me_edit_page = MeEditProfilePage()
        MinePage().click_personal_photo()
        time.sleep(0.5)
        me_edit_page.input_random_name()
        me_edit_page.click_locator_key('年龄')
        me_edit_page.click_locator_key('年龄_90后')
        me_edit_page.click_locator_key('保存')
        self.assertTrue(me_edit_page.check_text_exist('保存成功'))

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0008(self):
        """编辑标签选项选择标签"""
        me_edit_page = MeEditProfilePage()
        MinePage().click_personal_photo()
        time.sleep(0.5)
        me_edit_page.click_locator_key('我的标签')
        time.sleep(2)
        me_edit_page.click_locator_key('添加个性标签')
        me_edit_page.click_locator_key('标签取消')
        for i in range(6):
            me_edit_page.click_tag_index('标签', i)
        self.assertTrue(me_edit_page.check_text_exist('最多选择5个标签来形容自己'))

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0009(self):
        """编辑职业选项选择职业"""
        me_edit_page = MeEditProfilePage()
        MinePage().click_personal_photo()
        time.sleep(0.5)
        me_edit_page.input_random_name()
        me_edit_page.click_locator_key('职业')
        me_edit_page.click_locator_key('职业_计算机')
        me_edit_page.click_locator_key('保存')
        for i in range(3):
            if me_edit_page.is_toast_exist('保存成功', timeout=0.3) \
                    or me_edit_page.is_toast_exist('您的资料未变化', timeout=0.3):
                break

    # @unittest.skip('app改版没有二维码')
    # def test_me_0010(self):
    #     """查看我的二维码页面显示"""
    #     me_page = MinePage()
    #     me_page.click_locator_key('我的二维码')
    #     self.assertTrue(me_page.element_is_clickable('二维码_转到上一层级'))
    #     self.assertTrue(me_page.element_is_clickable('二维  码_更多'))
    #     self.assertTrue(me_page.is_text_exist('我的二维码'))
    #     self.assertTrue(me_page.is_text_exist('密友圈扫描二维码，添加我为密友'))
    #     self.assertTrue(me_page.check_qr_code_exist())
    #     self.assertTrue(me_page.check_element_name_photo_exist())

    # @unittest.skip('app改版没有二维码')
    # def test_me_0011(self):
    #     """个人二维码点击更多"""
    #     me_page = MinePage()
    #     me_page.click_locator_key('我的二维码')
    #     me_page.click_locator_key('二维码_更多')
    #     time.sleep(2)
    #     self.assertEqual(me_page.get_element_text('分享二维码'), '分享我的二维码')
    #     self.assertTrue(me_page.element_is_enable('分享二维码'))
    #     self.assertEqual(me_page.get_element_text('保存二维码'), '保存二维码图片')
    #     self.assertTrue(me_page.element_is_enable('保存二维码'))

    # @unittest.skip('app改版没有二维码')
    # def test_me_0012(self):
    #     """个人二维码点击更多"""
    #     me_page = MinePage()
    #     me_page.click_locator_key('我的二维码')
    #     me_page.click_locator_key('二维码_更多')
    #     me_page.click_locator_key('分享二维码')
    #     self.assertEqual(me_page.get_element_text('分享_密友圈'), '密友圈')
    #     self.assertEqual(me_page.get_element_text('分享_朋友圈'), '朋友圈')
    #     self.assertEqual(me_page.get_element_text('分享_微信'), '微信')
    #     self.assertEqual(me_page.get_element_text('分享_QQ'), 'QQ')
    #     self.assertEqual(me_page.get_element_text('分享_QQ空间'), 'QQ空间')

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0013(self):
        """验证活动中心页面正常打开"""
        me_page = MinePage()
        me_page.click_locator_key_c('活动中心')
        self.assertTrue(me_page.check_wait_text_exits('活动中心', timeout=3 * 60))
        me_page.click_locator_key_c('我_二级页面_相同返回')

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0014(self):
        """验证卡券页面正常打开"""
        me_page = MinePage()
        me_page.click_locator_key_c('卡券')
        self.assertTrue(me_page.check_wait_text_exits('我的卡券'))
        me_page.click_locator_key_c('我_二级页面_相同返回')

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0015(self):
        """验证积分页面正常打开"""
        me_page = MinePage()
        me_page.click_locator_key_c('积分')
        times = 2 * 60
        while times > 0:
            if me_page.is_text_present_c('已连续签到', default_timeout=0.5):
                me_page.click_text('我知道了')
            if me_page.is_text_present_c('我的积分', default_timeout=0.5):
                break
            times -= 1
        self.assertTrue(me_page.check_wait_text_exits('我的积分'))
        me_page.click_locator_key_c('我_二级页面_相同返回')

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0016(self):
        """验证网上营业厅正常打开"""
        me_page = MinePage()
        me_page.click_locator_key_c('网上营业厅')
        self.assertTrue(me_page.check_wait_text_exits('网上营业厅'))
        me_page.click_locator_key_c('我_二级页面_相同返回')

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0017(self):
        """验证邀请有礼正常打开"""
        me_page = MinePage()
        me_page.click_locator_key_c('邀请有礼')
        self.assertTrue(me_page.check_wait_text_exits('邀请有奖'))
        me_page.click_locator_key_c('我_二级页面_相同返回')

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0018(self):
        """验证帮助与反馈正常打开"""
        me_page = MinePage()
        me_page.click_locator_key_c('帮助与反馈')
        self.assertTrue(me_page.check_wait_text_exits('帮助与反馈'))
        me_page.click_locator_key_c('我_二级页面_相同返回')

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_me_0019(self):
        """验证我-设置-退出当前账号	中	"1、联网正常
        2、已登陆客户端
        3、在我模块-设置页面"	点击退出当前账号	成功退出登录显示，并跳转至登录页
        """
        me_page = MinePage()
        time.sleep(1)
        for i in range(3):
            if me_page.is_element_already_exist_c('设置'):
                me_page.click_locator_key_c('设置')
                break
            else:
                me_page.page_up()
        time.sleep(1)
        me_page.click_locator_key_c('退出当前账号')
        time.sleep(3)
        self.assertTrue(me_page.check_wait_text_exits('一键登录'))
