from selenium.common.exceptions import TimeoutException

from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages.guide import GuidePage
from pages.login.LoginPage import OneKeyLoginPage
from pages.call.CallPage import CallPage
from library.core.TestCase import TestCase
import time
from pages.call.Selectcontact import Selectcontactpage

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
        if not guide_page.is_on_the_first_guide_page():
            current_mobile().launch_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        guide_page.click_start_the_experience()
        guide_page.click_start_the_one_key()
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
            one_key.click_agree_login_by_number()

        # 等待通话页面加载
        call_page = CallPage()
        call_page.wait_for_page_call_load()
        call_page.click_always_allow()
        time.sleep(2)
        call_page.remove_mask()

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
        if one_key.is_on_this_page():
            Preconditions.login_by_one_key_login()
        # 如果当前页不是引导页第一页，重新启动app
        else:
            try:
                current_mobile().terminate_app('com.cmic.college', timeout=2000)
            except:
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
        current_mobile().wait_until_not(condition=lambda d: current_mobile().is_text_present('正在登录...'),timeout=20)

class CallTest(TestCase):
    """Call 模块"""

    @staticmethod
    def setUp_test_call_0001():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_sure_in_after_login_callpage()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0034(self):
        """通话列表页面的显示（单条记录的删除）"""
        call_page = CallPage()
        call_page.make_sure_have_p2p_vedio_record()
        call_page.make_sure_have_multiplayer_vedio_record()
        call_page.make_sure_have_p2p_voicecall_record()
        self.assertTrue(call_page.check_delete_text_first_element('视频通话'))
        call_page.wait_until(condition=lambda x:call_page.is_on_this_page())
        self.assertTrue(call_page.check_delete_text_first_element('多方视频'))
        self.assertTrue(call_page.check_delete_text_first_element('福利电话'))

    @staticmethod
    def setUp_test_call_0002():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_sure_in_after_login_callpage()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0035(self):
        """通话列表页面的显示（清空全部通话记录）"""
        call_page = CallPage()
        call_page.make_sure_have_p2p_vedio_record()
        call_page.make_sure_have_multiplayer_vedio_record()
        call_page.make_sure_have_p2p_voicecall_record()
        call_page.click_tag_text_delete_all_record('视频通话')
        self.assertTrue(call_page.check_text_exist('点击右下角,不花钱打电话'))

    @staticmethod
    def setUp_test_call_0003():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_sure_in_after_login_callpage()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0003(self):
        """通话列表页面空白文案"""
        call_page = CallPage()
        call_page.check_is_have_friend()
        bol = call_page.wait_until(condition=lambda x:call_page.is_text_present('点击右下角,不花钱打电话'), timeout=8, auto_accept_permission_alert=False)
        self.assertTrue(bol)

    @staticmethod
    def setUp_test_call_0005():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_sure_in_after_login_callpage()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0005(self):
        """查看视频通话详情页面"""
        call_page = CallPage()
        call_page.make_sure_have_p2p_vedio_record()
        call_page.click_tag_detail_first_element('视频通话')
        call_page.wait_until(condition=lambda x: call_page.is_text_present('通话记录 (视频通话)'))
        self.assertTrue(call_page.check_vedio_call_detail_page())
        call_page.click_locator_key('详情_返回')

    @staticmethod
    def setUp_test_call_0006():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_sure_in_after_login_callpage()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0006(self):  # 已完成
        """进入通话记录详情页面（发起视频通话）"""
        call_page = CallPage()
        call_page.make_sure_have_p2p_vedio_record()
        call_page.click_tag_detail_first_element('视频通话')
        call_page.click_locator_key('详情_视频按钮')
        bol = call_page.wait_until(condition=lambda x:call_page.check_p2p_vedio_call_page(), timeout=8,
                                   auto_accept_permission_alert=False)
        self.assertTrue(bol)
        call_page.click_locator_key('挂断')
        call_page.click_locator_key('详情_返回')

    @staticmethod
    def setUp_test_call_0007():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_sure_in_after_login_callpage()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0007(self):
        """进入通话记录详情页面（发起消息对话）"""
        call_page = CallPage()
        call_page.make_sure_have_p2p_vedio_record()
        call_page.click_tag_detail_first_element('视频通话')
        call_page.click_locator_key('详情_信息按钮')
        call_page.input_locator_text('信息_聊天框', '什么鬼')
        call_page.click_locator_key('信息_发送')
        if call_page.is_text_present('发送添加密友请求'):
            self.assertTrue(call_page._is_enabled(("id", 'com.cmic.college:id/tv_sys_msg')))
        else:
            bol = call_page.wait_until(condition=lambda x: call_page.check_message_page(), timeout=10,
                                       auto_accept_permission_alert=False)
            self.assertTrue(bol)
        call_page.click_locator_key('群聊_返回上一层')
        call_page.click_locator_key('详情_返回')

    @staticmethod
    def setUp_test_call_0008():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_sure_in_after_login_callpage()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0008(self):
        """进入通话记录详情页面"""
        call_page = CallPage()
        call_page.make_sure_have_multiplayer_vedio_record()
        call_page.click_tag_detail_first_element('多方视频')
        call_page.wait_until(condition=lambda x: call_page.is_text_present('通话记录 (多方视频)'))
        self.assertTrue(call_page.check_multiplayer_vedio_detail_page())
        call_page.click_locator_key('多方通话_返回')

    @staticmethod
    def setUp_test_call_0009():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_sure_in_after_login_callpage()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0009(self):
        """进入通话记录详情页面（发起多方视频通话）"""
        call_page = CallPage()
        call_page.make_sure_have_multiplayer_vedio_record()
        call_page.click_tag_detail_first_element('多方视频')
        call_page.click_locator_key('详情_多人视频')
        bol = call_page.wait_until(condition=lambda x:call_page.check_multiplayer_call_page(), timeout=8,
                                   auto_accept_permission_alert=False)
        self.assertTrue(bol)
        call_page.click_locator_key('挂断_多方通话')
        call_page.click_locator_key('挂断_多方通话_确定')
        call_page.click_locator_key('多方通话_返回')

    @staticmethod
    def setUp_test_call_0010():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_sure_in_after_login_callpage()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0010(self):
        """进入通话记录详情页面（创建群聊）"""
        call_page = CallPage()
        call_page.make_sure_have_multiplayer_vedio_record()
        call_page.click_tag_detail_first_element('多方视频')
        call_page.click_locator_key('详情_群聊')
        call_page.click_locator_key('群聊_确定')
        bol = call_page.wait_until(condition=lambda x:call_page.check_message_page(), timeout=10, auto_accept_permission_alert=False)
        self.assertTrue(bol)
        call_page.click_locator_key('群聊_返回上一层')
        call_page.click_locator_key('多方通话_返回')

    @staticmethod
    def setUp_test_call_0011():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_call_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0011(self):
        """进入视频通话入口"""
        call_page = CallPage()
        call_page.click_locator_key('视频')
        call_page.click_locator_key('视频通话_第一个联系人')
        self.assertTrue(call_page.check_vedio_page())
        call_page.click_locator_key('多方通话_返回')

    @staticmethod
    def setUp_test_call_0037():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_call_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0037(self):
        """进入免费通话页，点击返回功能键"""
        call_page = CallPage()
        call_page.click_locator_key('电话图标')
        bol = call_page.wait_until(condition= lambda x:call_page.is_text_present('福利电话'), timeout=8, auto_accept_permission_alert=False)
        self.assertTrue(bol)
        call_page.click_locator_key('拨号_返回')

    @staticmethod
    def setUp_test_call_0046():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_call_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0046(self):
        """免费电话业务规则说明入口"""
        call_page = CallPage()
        call_page.click_locator_key('电话图标')
        call_page.click_locator_key('页面规则')
        bol = call_page.wait_until(
            condition=lambda d: call_page.is_text_present('规则说明'), timeout=20
            , auto_accept_permission_alert=False)
        self.assertTrue(bol)

    @staticmethod
    def setUp_test_call_0047():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_call_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0047(self):
        """通过手机号码、用户昵称搜索端内联系人"""
        call_page = CallPage()
        call_page.click_locator_key('视频')
        first_phoneNumber = call_page.get_element_text('电话号码')
        call_page.click_locator_key('多方通话_返回')
        call_page.click_locator_key('电话图标')
        call_page.click_locator_key('电话_搜索栏')
        call_page.input_locator_text('搜索_电话', 1)
        self.assertTrue(len(call_page.get_elements_count('搜索_电话显示'))>0)
        call_page.input_locator_text('搜索_电话', first_phoneNumber)
        self.assertNotEqual(call_page.get_element_text('搜索_电话昵称'), '未知号码')

    @staticmethod
    def setUp_test_call_0048():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_call_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0048(self):
        """通过手机号码、用户昵称搜索端外联系人"""
        call_page = CallPage()
        call_page.click_locator_key('电话图标')
        call_page.click_locator_key('电话_搜索栏')
        call_page.input_locator_text('搜索_电话', 12345678)
        self.assertEqual(len(call_page.get_elements_count('搜索_电话显示')), 0)
        call_page.input_locator_text('搜索_电话', 13658489578)
        self.assertEqual(call_page.get_element_text('搜索_电话昵称'), '未知号码')

    @staticmethod
    def setUp_test_call_0049():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_call_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0049(self):
        """多方通话剩余分钟数"""
        call_page = CallPage()
        call_page.mobile.turn_off_mobile_data()
        call_page.mobile.turn_off_wifi()
        call_page.mobile.launch_app()
        call_page.click_locator_key('电话图标')
        self.assertIn('--', call_page.get_element_text('免费时长'))
        call_page.click_locator_key('拨号_返回')
        call_page.mobile.turn_on_mobile_data()
        current_mobile().wait_until_not(condition=lambda d: current_mobile().is_text_present('正在登录...'), timeout=20)
        call_page.click_locator_key('电话图标')
        import time
        time.sleep(1.5)
        self.assertNotIn('--', call_page.get_element_text('免费时长'))
        call_page.click_locator_key('拨号_返回')
        call_page.mobile.turn_off_mobile_data()
        call_page.mobile.turn_off_wifi()
        call_page.click_locator_key('电话图标')
        self.assertNotIn('--', call_page.get_element_text('免费时长'))

    @staticmethod
    def tearDown_test_call_0049():
        call_page = CallPage()
        call_page.mobile.turn_on_wifi()
        call_page.mobile.turn_on_mobile_data()

    @staticmethod
    def setUp_test_call_0050():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_call_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_call_0050(self):
        """未加载到多方通话剩余分钟数"""
        call_page = CallPage()
        call_page.mobile.turn_off_mobile_data()
        call_page.mobile.turn_off_wifi()
        call_page.mobile.launch_app()
        import time
        time.sleep(1.5)
        call_page.click_locator_key('电话图标')
        self.assertIn('--', call_page.get_element_text('免费时长'))
        call_page.click_locator_key('拨号_返回')

    @staticmethod
    def tearDown_test_call_0050():
        call_page = CallPage()
        call_page.mobile.turn_on_wifi()
        call_page.mobile.turn_on_mobile_data()


class Callpage(TestCase):
    """Call 模块--全量"""

    def default_setUp(self):
        """确保每个用例开始之前在通话界面界面"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_call_page()


    @tags('ALL', 'CMCC','call')
    def test_call_0001(self):
        """通话界面显示"""
        time.sleep(2)
        call=CallPage()
        call.page_contain_element('通话文案')
        call.page_contain_element('拨号键盘')
        if call.is_element_present('来电名称'):
            call.page_contain_element('来电名称')
        else:
            call.page_should_contain_text('打电话不花钱')

    @tags('ALL', 'CMCC','call')
    def test_call_0002(self):
        """通话界面-拨号键盘显示"""
        time.sleep(2)
        call=CallPage()
        call.page_contain_element('拨号键盘')
        if call.is_element_present('来电名称'):
            call.page_contain_element('来电名称')
        else:
            call.page_should_contain_text('打电话不花钱')
        #点击键盘
        call.click_keyboard()
        time.sleep(2)
        call.is_keyboard_shown()
        call.click_keyboard_input_box()
        text='123'
        call.input_text_in_input_box(text)
        number=call.get_input_box_text()
        self.assertTrue(number)

    @tags('ALL', 'CMCC','call')
    def test_call_0003(self):
        """通话界面-拨号盘收起"""
        time.sleep(2)
        call=CallPage()
        call.page_contain_element('拨号键盘')
        if call.is_element_present('来电名称'):
            call.page_contain_element('来电名称')
        else:
            call.page_should_contain_text('打电话不花钱')
        #点击键盘
        call.click_keyboard()
        time.sleep(2)
        call.is_keyboard_shown()
        #再次点击拨号盘
        call.click_hide_keyboard()
        time.sleep(2)
        call.page_contain_element('拨号键盘')


    @tags('ALL', 'CMCC','call')
    def test_call_0004(self):
        """通话界面-点击视频通话"""
        call = CallPage()
        call.click_add()
        call.page_should_contain_text('视频通话')
        call.page_should_contain_text('多方电话')
        time.sleep(1)
        call.click_text('视频通话')
        Selectcontactpage().page_should_contain_text('发起视频通话')


    @tags('ALL', 'CMCC','call')
    def test_call_0005(self):
        """通话界面-打开通话键盘,显示通话记录"""
        time.sleep(2)
        call=CallPage()
        #点击键盘
        call.click_keyboard()
        time.sleep(2)
        call.is_keyboard_shown()
        if call.is_element_present('来电名称'):
            call.page_contain_element('来电名称')
        call.page_left()
        call.page_contain_element('收起键盘')























