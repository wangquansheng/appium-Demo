import multiprocessing
import threading

from selenium.common.exceptions import TimeoutException

from library.core.TestLogger import TestLogger
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages.guide import GuidePage
from pages.login.LoginPage import OneKeyLoginPage
from pages.call.CallPage import CallPage
from library.core.TestCase import TestCase
import time
import datetime
import warnings
from pages.call.Selectcontact import Selectcontactpage
import traceback

REQUIRED_MOBILES = {
    'Android-移动-N': 'M960BDQN229CH',
    'Android-移动': 'M960BDQN229CH_NOVA',
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
        # if not guide_page.is_on_the_first_guide_page():
        #     current_mobile().launch_app()
        #     guide_page.wait_for_page_load(20)

        # 跳过引导页
        # guide_page.wait_for_page_load(30)
        # guide_page.swipe_to_the_second_banner()
        # guide_page.swipe_to_the_third_banner()
        # guide_page.click_start_the_experience()
        # guide_page.click_start_the_one_key()
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
        call_page.remove_mask()

        # 等待通话页面加载
        # call_page.wait_for_page_call_load()
        # call_page.click_always_allow()
        # count = 30
        # while count > 0:
        #     if call_page.is_element_already_exist('通话'):
        #         break
        #     if call_page.is_element_already_exist('暂不升级'):
        #         call_page.click_locator_key('暂不升级')
        #     count -= 1
        #     print('剩余时间：%ss' % count)

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
        one_key.wait_until(
            condition=lambda d: one_key.is_text_present('一键登录'),
            timeout=8
        )
        if one_key.is_text_present('一键登录'):
            Preconditions.login_by_one_key_login()
        # 如果当前页不是引导页第一页，重新启动app
        else:
            try:
                current_mobile().terminate_app('com.cmic.college', timeout=2000)
            except Exception as e:
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


# class CallTest(TestCase):
#     """Call 模块"""
#
#     @staticmethod
#     def setUp_test_call_0001():
#         Preconditions.select_mobile('Android-移动')
#         current_mobile().hide_keyboard_if_display()
#         Preconditions.make_sure_in_after_login_callpage()
#
#     @tags('ALL', 'SMOKE', 'CMCC')
#     def test_call_0001(self):
#         """通话列表页面的显示（单条记录的删除）"""
#         call_page = CallPage()
#         call_page.make_sure_have_p2p_vedio_record()
#         call_page.make_sure_have_multiplayer_vedio_record()
#         call_page.make_sure_have_p2p_voicecall_record()
#         self.assertTrue(call_page.check_delete_text_first_element('视频通话'))
#         call_page.wait_until(condition=lambda x: call_page.is_on_this_page())
#         self.assertTrue(call_page.check_delete_text_first_element('多方视频'))
#         self.assertTrue(call_page.check_delete_text_first_element('福利电话'))
#
#     @staticmethod
#     def setUp_test_call_0002():
#         Preconditions.select_mobile('Android-移动')
#         current_mobile().hide_keyboard_if_display()
#         Preconditions.make_sure_in_after_login_callpage()
#
#     @tags('ALL', 'SMOKE', 'CMCC')
#     def test_call_0002(self):
#         """通话列表页面的显示（清空全部通话记录）"""
#         call_page = CallPage()
#         call_page.make_sure_have_p2p_vedio_record()
#         call_page.make_sure_have_multiplayer_vedio_record()
#         call_page.make_sure_have_p2p_voicecall_record()
#         call_page.click_tag_text_delete_all_record('视频通话')
#         self.assertTrue(call_page.check_text_exist('点击右下角,不花钱打电话'))
#
#     @staticmethod
#     def setUp_test_call_0003():
#         Preconditions.select_mobile('Android-移动')
#         current_mobile().hide_keyboard_if_display()
#         Preconditions.make_sure_in_after_login_callpage()
#
#     @tags('ALL', 'SMOKE', 'CMCC')
#     def test_call_0003(self):
#         """通话列表页面空白文案"""
#         call_page = CallPage()
#         call_page.check_is_have_friend()
#         bol = call_page.wait_until(condition=lambda x: call_page.is_text_present('点击右下角,不花钱打电话'), timeout=8,
#                                    auto_accept_permission_alert=False)
#         self.assertTrue(bol)
#
#     @staticmethod
#     def setUp_test_call_0005():
#         Preconditions.select_mobile('Android-移动')
#         current_mobile().hide_keyboard_if_display()
#         Preconditions.make_sure_in_after_login_callpage()
#
#     @tags('ALL', 'SMOKE', 'CMCC')
#     def test_call_0005(self):
#         """查看视频通话详情页面"""
#         call_page = CallPage()
#         call_page.make_sure_have_p2p_vedio_record()
#         call_page.click_tag_detail_first_element('视频通话')
#         call_page.wait_until(condition=lambda x: call_page.is_text_present('通话记录 (视频通话)'))
#         self.assertTrue(call_page.check_vedio_call_detail_page())
#         call_page.click_locator_key('详情_返回')
#
#     @staticmethod
#     def setUp_test_call_0046():
#         Preconditions.select_mobile('Android-移动')
#         current_mobile().hide_keyboard_if_display()
#         Preconditions.make_already_in_call_page()
#
#     @tags('ALL', 'SMOKE', 'CMCC')
#     def test_call_0046(self):
#         """免费电话业务规则说明入口"""
#         call_page = CallPage()
#         call_page.click_locator_key('电话图标')
#         call_page.click_locator_key('页面规则')
#         bol = call_page.wait_until(
#             condition=lambda d: call_page.is_text_present('规则说明'), timeout=20
#             , auto_accept_permission_alert=False)
#         self.assertTrue(bol)
#
#     @staticmethod
#     def setUp_test_call_0047():
#         Preconditions.select_mobile('Android-移动')
#         current_mobile().hide_keyboard_if_display()
#         Preconditions.make_already_in_call_page()
#
#     @tags('ALL', 'SMOKE', 'CMCC')
#     def test_call_0047(self):
#         """通过手机号码、用户昵称搜索端内联系人"""
#         call_page = CallPage()
#         call_page.click_locator_key('视频')
#         first_phoneNumber = call_page.get_element_text('电话号码')
#         call_page.click_locator_key('多方通话_返回')
#         call_page.click_locator_key('电话图标')
#         call_page.click_locator_key('电话_搜索栏')
#         call_page.input_locator_text('搜索_电话', 1)
#         self.assertTrue(len(call_page.get_elements_count('搜索_电话显示')) > 0)
#         call_page.input_locator_text('搜索_电话', first_phoneNumber)
#         self.assertNotEqual(call_page.get_element_text('搜索_电话昵称'), '未知号码')
#
#     @staticmethod
#     def setUp_test_call_0048():
#         Preconditions.select_mobile('Android-移动')
#         current_mobile().hide_keyboard_if_display()
#         Preconditions.make_already_in_call_page()
#
#     @tags('ALL', 'SMOKE', 'CMCC')
#     def test_call_0048(self):
#         """通过手机号码、用户昵称搜索端外联系人"""
#         call_page = CallPage()
#         call_page.click_locator_key('电话图标')
#         call_page.click_locator_key('电话_搜索栏')
#         call_page.input_locator_text('搜索_电话', 12345678)
#         self.assertEqual(len(call_page.get_elements_count('搜索_电话显示')), 0)
#         call_page.input_locator_text('搜索_电话', 13658489578)
#         self.assertEqual(call_page.get_element_text('搜索_电话昵称'), '未知号码')
#
#     @staticmethod
#     def setUp_test_call_0049():
#         Preconditions.select_mobile('Android-移动')
#         current_mobile().hide_keyboard_if_display()
#         Preconditions.make_already_in_call_page()
#
#     @tags('ALL', 'SMOKE', 'CMCC')
#     def test_call_0049(self):
#         """多方通话剩余分钟数"""
#         call_page = CallPage()
#         call_page.mobile.turn_off_mobile_data()
#         call_page.mobile.turn_off_wifi()
#         call_page.mobile.launch_app()
#         call_page.click_locator_key('电话图标')
#         self.assertIn('--', call_page.get_element_text('免费时长'))
#         call_page.click_locator_key('拨号_返回')
#         call_page.mobile.turn_on_mobile_data()
#         current_mobile().wait_until_not(condition=lambda d: current_mobile().is_text_present('正在登录...'), timeout=20)
#         call_page.click_locator_key('电话图标')
#         import time
#         time.sleep(1.5)
#         self.assertNotIn('--', call_page.get_element_text('免费时长'))
#         call_page.click_locator_key('拨号_返回')
#         call_page.mobile.turn_off_mobile_data()
#         call_page.mobile.turn_off_wifi()
#         call_page.click_locator_key('电话图标')
#         self.assertNotIn('--', call_page.get_element_text('免费时长'))
#
#     @staticmethod
#     def tearDown_test_call_0049():
#         call_page = CallPage()
#         call_page.mobile.turn_on_wifi()
#         call_page.mobile.turn_on_mobile_data()
#
#     @staticmethod
#     def setUp_test_call_0050():
#         Preconditions.select_mobile('Android-移动')
#         current_mobile().hide_keyboard_if_display()
#         Preconditions.make_already_in_call_page()
#
#     @tags('ALL', 'SMOKE', 'CMCC')
#     def test_call_0050(self):
#         """未加载到多方通话剩余分钟数"""
#         call_page = CallPage()
#         call_page.mobile.turn_off_mobile_data()
#         call_page.mobile.turn_off_wifi()
#         call_page.mobile.launch_app()
#         import time
#         time.sleep(1.5)
#         call_page.click_locator_key('电话图标')
#         self.assertIn('--', call_page.get_element_text('免费时长'))
#         call_page.click_locator_key('拨号_返回')
#
#     @staticmethod
#     def tearDown_test_call_0050():
#         call_page = CallPage()
#         call_page.mobile.turn_on_wifi()
#         call_page.mobile.turn_on_mobile_data()
#

class CallPageTest(TestCase):
    """Call 模块--全量"""

    def default_setUp(self):
        """确保每个用例开始之前在通话界面界面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_call_page()

    def default_tearDown(self):
        call = CallPage()
        if call.get_network_status() != 6:
            call.set_network_status(6)
        time.sleep(2)
        current_mobile().terminate_app('com.cmic.college', timeout=2000)


    # 注：是从0002开始的，没有0001

    @tags('ALL', 'CMCC', 'call')
    def test_call_0002(self):
        """通话界面显示"""
        time.sleep(2)
        call = CallPage()
        call.page_contain_element('通话文案')
        call.page_contain_element('拨号键盘')
        if call.is_element_present('来电名称'):
            call.page_contain_element('来电名称')
        else:
            call.page_should_contain_text('打电话不花钱')

    @tags('ALL', 'CMCC', 'call')
    def test_call_0003(self):
        """通话界面-拨号键盘显示"""
        time.sleep(2)
        call = CallPage()
        call.page_contain_element('拨号键盘')
        if call.is_element_present('来电名称'):
            call.page_contain_element('来电名称')
        else:
            call.page_should_contain_text('打电话不花钱')
        # 点击键盘
        call.click_keyboard()
        time.sleep(2)
        call.is_keyboard_shown()
        call.click_keyboard_input_box()
        text = '123'
        call.input_text_in_input_box(text)
        number = call.get_input_box_text()
        self.assertTrue(number)

    @tags('ALL', 'CMCC', 'call')
    def test_call_0004(self):
        """通话界面-拨号盘收起"""
        time.sleep(2)
        call = CallPage()
        call.page_contain_element('拨号键盘')
        if call.is_element_present('来电名称'):
            call.page_contain_element('来电名称')
        else:
            call.page_should_contain_text('打电话不花钱')
        # 点击键盘
        call.click_keyboard()
        time.sleep(2)
        call.is_keyboard_shown()
        # 再次点击拨号盘
        call.click_hide_keyboard()
        time.sleep(2)
        call.page_contain_element('拨号键盘')

    @tags('ALL', 'CMCC', 'call')
    def test_call_0005(self):
        """通话界面-点击视频通话"""
        call = CallPage()
        call.click_add()
        call.page_should_contain_text('视频通话')
        call.page_should_contain_text('多方电话')
        time.sleep(1)
        call.click_text('视频通话')
        Selectcontactpage().page_should_contain_text('发起视频通话')

    # @tags('ALL', 'CMCC', 'call')
    # def test_call_0006(self):
    #     """通话界面-打开通话键盘,显示通话记录"""
    #     time.sleep(2)
    #     call = CallPage()
    #     # 点击键盘
    #     call.click_keyboard()
    #     time.sleep(2)
    #     call.is_keyboard_shown()
    #     if call.is_element_present('来电名称'):
    #         call.page_contain_element('来电名称')
    #     call.page_left()
    #     call.page_contain_element('收起键盘')

    @tags('ALL', 'CMCC', 'call')
    def test_call_0006(self):
        """展开拨号盘，不可以左右滑动切换tab，上方内容显示通话模块通话记录内容"""
        time.sleep(2)
        call = CallPage()
        # call.close_ad()
        call.wait_for_page_load()
        # call.close_ad()
        # 判断如果键盘是拉起的，则不需要再次拉起
        if call.is_on_this_page():
            call.click_show_keyboard()
        time.sleep(1)
        # 向左滑动
        call.swipe_by_percent_on_screen(20, 50, 90, 50, 1000)
        # 判断滑动后是否还在此页面
        self.assertEqual(call.is_exist_call_key(), True)
        # 向右滑动
        call.swipe_by_percent_on_screen(90, 50, 20, 50, 1000)
        # 判断滑动后是否还在此页面
        self.assertEqual(call.is_exist_call_key(), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_0007(self):
        """跳出下拉框，可选择视频通话与多方电话"""
        time.sleep(2)
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 点击加号
        call.click_add()
        time.sleep(1)
        # 判断是否有视频通话与多方电话
        self.assertEqual(call.is_element_present('视频通话x'), True)
        self.assertEqual(call.is_element_present('多方电话x'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_0008(self):
        """打开视频通话界面-联系人选择器页面（该页面逻辑与现网保持一致）"""
        time.sleep(2)
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 点击加号
        call.click_add()
        time.sleep(1)
        call.click_locator_key('视频通话x')
        time.sleep(1)
        self.assertEqual(call.check_text_exist('发起视频通话'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_0009(self):
        """打开多方电话-联系人选择器页面（该页面逻辑与现网保持一致）"""
        time.sleep(2)
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 点击加号
        call.click_add()
        time.sleep(1)
        call.click_locator_key('多方电话x')
        time.sleep(1)
        self.assertEqual(call.check_text_exist('多方电话'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00010(self):
        """
            跳转至通话详情页面中，页面布局左上方返回按钮，顶部展示联系人头像与名称，
            中部展示通话、视频通话，设置备注名，下方展示手机号码与号码归属地，通话记录（视频通话），
            显示通话类型、通话时 长，通话时间点
        """
        time.sleep(2)
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.make_sure_have_p2p_vedio_record()
        call.click_tag_detail_first_element('视频通话')
        # 判断
        time.sleep(1)
        self.assertEqual(call.on_this_page_call_detail(), True)
        self.assertEqual(call.check_vedio_call_detail_page(), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00011(self):
        """
            跳转至多方视频详情页面中，页面布局左上方返回按钮，右边为多方视频文字，下方为：
            发起多方视频按钮栏，展示联系人头像与名称，通话记录（多方视频），
            显示通话类型、通话时长，通话时间点
        """
        time.sleep(2)
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.make_sure_have_multiplayer_vedio_record()
        time.sleep(2)
        call.click_tag_detail_first_element('多方视频')
        # 判断
        time.sleep(1)
        # 是否在多方视频详情页面
        self.assertEqual(call.on_this_page_multi_video_detail(), True)
        self.assertEqual(call.check_multiplayer_vedio_detail_page(), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00012(self):
        """
            跳转至通话详情页面中，返回到通话记录列表页面
        """
        time.sleep(2)
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.click_tag_detail_first_element('飞信电话')
        time.sleep(1)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 单击左上角返回按钮
        call.click_detail_back()
        call.wait_for_page_load()
        self.assertEqual(call.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00013(self):
        """
            验证通话记录详情页-编辑备注名---正确输入并点击保存（中文、英文、特殊符号）---保存成功
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.make_sure_have_p2p_voicecall_record()
        call.click_tag_detail_first_element('飞信电话')
        time.sleep(1)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 1. 修改为中文
        name = '测试中文备注'
        self.assertEqual(self.check_modify_nickname(name), True)
        # 2. 修改为全英文
        name = 'testEnglishNickname'
        self.assertEqual(self.check_modify_nickname(name), True)
        # 3. 修改为特殊字符
        name = '汉字English%^&*()_!@#'
        self.assertEqual(self.check_modify_nickname(name), True)

    def check_modify_nickname(self, name):
        """修改并验证备注是否修改成功"""
        call = CallPage()
        call.click_modify_nickname()
        call.wait_for_page_modify_nickname()
        time.sleep(0.5)
        # call.input_text_in_nickname('')
        call.edit_clear()
        call.input_text_in_nickname(name)
        call.click_save_nickname()
        time.sleep(2)
        if not call.on_this_page_call_detail():
            return False
        if name != call.get_nickname():
            return False
        return True

    @tags('ALL', 'CMCC', 'call')
    def test_call_00016(self):
        """
            验证通话记录详情页-编辑备注名---输入sql语句并点击保存---保存成功
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.make_sure_have_p2p_vedio_record()
        call.click_tag_detail_first_element('视频通话')
        time.sleep(1)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 1. 修改为中文
        name = 'select now()'
        self.assertEqual(self.check_modify_nickname(name), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00017(self):
        """
            验证通话记录详情页-编辑备注名---输入html标签并点击保存---保存成功
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.make_sure_have_p2p_vedio_record()
        call.click_tag_detail_first_element('视频通话')
        time.sleep(1)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 1. 修改为中文
        name = '<a href="www.baidu.com"/>a<a/>'
        self.assertEqual(self.check_modify_nickname(name), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00019(self):
        """
            1、联网正常已登录
            2、对方离线
            3、当前页通话记录详情
            1、点击视频通话---1、进入拨打视频通话界面，并弹出提示窗，“对方未接听，请稍候再尝试”
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.make_sure_have_p2p_vedio_record()
        call.click_tag_detail_first_element('视频通话')
        time.sleep(1)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 1. 点击视频通话按钮
        call.click_locator_key('详情_视频')
        time.sleep(1)
        if call.on_this_page_flow():
            call.set_not_reminders()
            time.sleep(1)
            call.click_locator_key('流量_继续拨打')
        time.sleep(25)
        count = 20
        while count > 0:
            exist = call.is_toast_exist("对方未接听，请稍候再尝试")
            if exist:
                break
            time.sleep(0.3)
            count -= 1
        else:
            raise RuntimeError('测试出错')

    @tags('ALL', 'CMCC', 'call')
    def test_call_00020(self):
        """
            1、联网正常已登录
            2、对方离线
            3、当前页通话记录详情
            点击视频通话---点击取消---进入拨打视频通话界面，并弹出提示窗，“通话结束”---返回通话记录详情页
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.make_sure_have_p2p_vedio_record()
        call.click_tag_detail_first_element('视频通话')
        time.sleep(1)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 1. 点击视频通话按钮
        call.click_locator_key('详情_视频')
        time.sleep(1)
        if call.on_this_page_flow():
            call.set_not_reminders()
            time.sleep(1)
            call.click_locator_key('流量_继续拨打')
        time.sleep(3)
        call.click_locator_key('视频_结束视频通话')
        self.assertEqual(call.is_toast_exist("通话结束"), True)
        time.sleep(5)
        self.assertEqual(call.on_this_page_call_detail(), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00023(self):
        """
            1、联网正常已登录
            2、对方未注册
            3、当前页通话记录详情
            点击视频通话---点击取消---"1、进入拨打视频电话界面，并弹出提示窗--下方是“取消” 和“确定”按钮--返回通话记录详情页"
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.make_sure_have_p2p_vedio_record()
        call.click_tag_detail_first_element('视频通话')
        time.sleep(2)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 1. 点击视频通话按钮
        call.click_locator_key('详情_视频')
        time.sleep(1)
        if call.on_this_page_flow():
            call.set_not_reminders()
            time.sleep(1)
            call.click_locator_key('流量_继续拨打')
        time.sleep(1)
        if call.on_this_page_common('无密友圈_提示文本'):
            call.click_locator_key('无密友圈_取消')
        time.sleep(3)
        self.assertEqual(call.on_this_page_call_detail(), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00025(self):
        """
            1、联网正常已登录
            2、对方未注册
            3、当前页通话记录详情
            "1、进入拨打视频通话界面，并弹出提示窗，
            下方是“取消” 和“确定”按钮
            2、调起系统短信界面，复制文案到短信编辑器，文案如下：
            我在使用联系人圈，视频通话免流量哦，你也赶紧来使用吧，下载地址：feixin.10086.cn/miyou
            3、发送成功，接收方收到短信"

        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.make_sure_have_p2p_vedio_record()
        call.click_tag_detail_first_element('视频通话')
        time.sleep(2)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 1. 点击视频通话按钮
        call.click_locator_key('详情_视频')
        time.sleep(1)
        if call.on_this_page_flow():
            call.set_not_reminders()
            time.sleep(1)
            call.click_locator_key('流量_继续拨打')
        time.sleep(1)
        if call.on_this_page_common('无密友圈_提示文本'):
            call.click_locator_key('无密友圈_确定')
        time.sleep(1)
        name = Preconditions.get_current_activity_name()
        if 'com.android.mms' != name:
            raise RuntimeError('测试出错')

    @tags('ALL', 'CMCC', 'call')
    def test_call_00026(self):
        """
            1、联网正常已登录
            2、对方未注册
            3、当前页通话记录详情
            点击视频通话---点击取消---"1、进入拨打视频电话界面，并弹出提示窗--下方是“取消” 和“确定”按钮--返回通话记录详情页"
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.make_sure_have_p2p_vedio_record()
        call.click_tag_detail_first_element('视频通话')
        time.sleep(2)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 1. 点击视频通话按钮
        call.click_locator_key('详情_视频')
        time.sleep(1)
        if call.on_this_page_flow():
            call.set_not_reminders()
            time.sleep(1)
            call.click_locator_key('流量_继续拨打')
        time.sleep(1)
        if call.on_this_page_common('无密友圈_提示文本'):
            call.click_locator_key('无密友圈_取消')
        time.sleep(3)
        self.assertEqual(call.on_this_page_call_detail(), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00027(self):
        """
            1、联网正常已登录
            2、对方未注册
            3、当前页通话记录详情
            点击视频通话---点击取消---"1、进入拨打视频电话界面，并弹出提示窗--下方是“取消” 和“确定”按钮--返回通话记录详情页"
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.make_sure_have_p2p_vedio_record()
        call.click_tag_detail_first_element('视频通话')
        time.sleep(2)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 1. 点击视频通话按钮
        call.click_locator_key('详情_视频')
        time.sleep(1)
        if call.on_this_page_flow():
            call.set_not_reminders()
            time.sleep(1)
            call.click_locator_key('回呼_我知道了')
        time.sleep(1)
        # TODO 限时回呼电话

    @tags('ALL', 'CMCC', 'call')
    def test_call_00031(self):
        """
            1、备注名修改成功后，视频通话入口；
            2、查看用户名
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.make_sure_have_p2p_voicecall_record()
        call.click_tag_detail_first_element('飞信电话')
        time.sleep(1)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 1. 修改为中文
        name = '修改后的备注'
        self.assertEqual(self.check_modify_nickname(name), True)
        call.click_locator_key('详情_视频')
        time.sleep(1)
        if call.is_element_already_exist('流量_不再提醒'):
            call.set_not_reminders()
            call.click_locator_key('流量_继续拨打')
        time.sleep(2)
        comment = call.get_element_text('视频_备注')
        self.assertEqual(name == comment, True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00032(self):
        """
            1、联网正常已登录
            2、对方未注册
            3、当前页通话记录详情
            4 点击邀请使用按钮
            5 跳转至系统短信页面，附带发送号码与发送内容
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.make_sure_have_p2p_voicecall_record()
        call.click_tag_detail_first_element('飞信电话')
        time.sleep(1)
        self.assertEqual(call.on_this_page_call_detail(), True)
        call.click_locator_key('详情_邀请使用')
        time.sleep(0.5)
        call.click_locator_key('邀请_短信')
        time.sleep(1)
        activity_name = Preconditions.get_current_activity_name()
        print(activity_name)
        self.assertEqual('com.android.mms' == activity_name, True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00034(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在通话页面
            4、有点对点语音通话和点对点视频通话记录、多方视频通话记录
            5、长按对点语音通话和点对点视频通话记录、多方视频通话记录
            6、弹出删除该通话记录和清除全部通话记录选择框
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.make_sure_have_p2p_voicecall_record()
        call.press_tag_detail_first_element('飞信电话')
        time.sleep(1)
        self.assertEqual(call.check_text_exist('删除该通话记录') and call.check_text_exist('清除全部通话记录'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00035(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在通话页面
            4、有点对点语音通话和点对点视频通话记录、多方视频通话记录
            5、长按对点语音通话和点对点视频通话记录、多方视频通话记录
            6、点击删除该通话记录按钮
            7、弹出删除该通话记录和清除全部通话记录选择框
            8、该条记录删除成功"
        """
        call = CallPage()
        time.sleep(5)
        call.close_ad_if_exist()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 点对点通话
        call.make_sure_have_p2p_voicecall_record()
        call.press_tag_detail_first_element('飞信电话')
        time.sleep(1)
        if call.check_text_exist('删除该通话记录'):
            call.click_locator_key('通话记录_删除一条')
            call.wait_for_page_load()
        else:
            raise RuntimeError('没有弹出菜单')
        self.assertEqual(call.is_on_this_page(), True)
        time.sleep(3)
        # 点对点视频
        call.make_sure_have_p2p_vedio_record()
        call.press_tag_detail_first_element('视频通话')
        time.sleep(1)
        if call.check_text_exist('删除该通话记录'):
            call.click_locator_key('通话记录_删除一条')
            call.wait_for_page_load()
        else:
            raise RuntimeError('没有弹出菜单')
        self.assertEqual(call.is_on_this_page(), True)
        time.sleep(3)
        # 多方视频
        call.make_sure_have_multiplayer_vedio_record()
        call.press_tag_detail_first_element('多方视频')
        time.sleep(1)
        if call.check_text_exist('删除该通话记录'):
            call.click_locator_key('通话记录_删除一条')
            call.wait_for_page_load()
        else:
            raise RuntimeError('没有弹出菜单')
        self.assertEqual(call.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00036(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在通话页面
            4、有点对点语音通话和点对点视频通话记录、多方视频通话记录
            5、长按对点语音通话和点对点视频通话记录、多方视频通话记录
            6、点击清除全部通话记录按钮
            7、弹出删除该通话记录和清除全部通话记录选择框
            8、所有通话记录删除成功
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 点对点通话
        call.make_sure_have_p2p_voicecall_record()
        call.wait_for_page_load()
        call.press_tag_detail_first_element('飞信电话')
        time.sleep(1)
        if call.check_text_exist('清除全部通话记录'):
            call.click_locator_key('通话记录_删除全部')
            time.sleep(0.5)
            call.click_locator_key('通话记录_确定')
            call.wait_for_page_load()
        else:
            raise RuntimeError('没有弹出菜单')
        self.assertEqual(call.is_on_this_page(), True)
        time.sleep(3)
        # 点对点视频
        call.make_sure_have_p2p_vedio_record()
        call.wait_for_page_load()
        call.press_tag_detail_first_element('视频通话')
        time.sleep(1)
        if call.check_text_exist('清除全部通话记录'):
            call.click_locator_key('通话记录_删除全部')
            time.sleep(0.5)
            call.click_locator_key('通话记录_确定')
            call.wait_for_page_load()
        else:
            raise RuntimeError('没有弹出菜单')
        self.assertEqual(call.is_on_this_page(), True)
        time.sleep(3)
        # 多方视频
        call.make_sure_have_multiplayer_vedio_record()
        # call.click_locator_key('多方通话_返回')
        call.wait_for_page_load()
        call.press_tag_detail_first_element('多方视频')
        time.sleep(1)
        if call.check_text_exist('清除全部通话记录'):
            call.click_locator_key('通话记录_删除全部')
            time.sleep(0.5)
            call.click_locator_key('通话记录_确定')
            call.wait_for_page_load()
        else:
            raise RuntimeError('没有弹出菜单')
        self.assertEqual(call.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00037(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在通话页面
            4、有联系人或者家庭网联系人
            5、左上方有通话标题，右上方为"+"图标，下方有指引攻略，页面空白中间区域中有“点击左下角拨号盘icon，打电话不花钱”字样
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 清除全部通话记录
        if call.is_text_present('飞信电话'):
            call.press_tag_detail_first_element('飞信电话')
            time.sleep(1)
            if call.check_text_exist('清除全部通话记录'):
                call.click_locator_key('通话记录_删除全部')
                time.sleep(0.5)
                call.click_locator_key('通话记录_确定')
                call.wait_for_page_load()
            else:
                raise RuntimeError('清除通话记录出错')
        elif call.is_text_present('视频通话'):
            call.press_tag_detail_first_element('视频通话')
            time.sleep(1)
            if call.check_text_exist('清除全部通话记录'):
                call.click_locator_key('通话记录_删除全部')
                time.sleep(0.5)
                call.click_locator_key('通话记录_确定')
                call.wait_for_page_load()
            else:
                raise RuntimeError('清除通话记录出错')
        elif call.is_text_present('多方视频'):
            call.press_tag_detail_first_element('多方视频')
            time.sleep(1)
            if call.check_text_exist('清除全部通话记录'):
                call.click_locator_key('通话记录_删除全部')
                time.sleep(0.5)
                call.click_locator_key('通话记录_确定')
                call.wait_for_page_load()
            else:
                raise RuntimeError('清除通话记录出错')
        elif call.is_text_present('多方电话'):
            call.press_tag_detail_first_element('多方电话')
            time.sleep(1)
            if call.check_text_exist('清除全部通话记录'):
                call.click_locator_key('通话记录_删除全部')
                time.sleep(0.5)
                call.click_locator_key('通话记录_确定')
                call.wait_for_page_load()
            else:
                raise RuntimeError('清除通话记录出错')
        call.wait_for_page_call_load()
        # 判断是否有通话标签、‘+’、打电话不花钱
        self.assertEqual(call.is_text_present('通话'), True)
        self.assertEqual(call.on_this_page_common('+'), True)
        self.assertEqual(call.is_text_present('打电话不花钱'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00040(self):
        """
            点击视频通话图标
            跳转至视频通话选择页面，页面布局左上方返回按钮，多方视频字体，
            右上方呼叫按钮，下面显示不限时长成员，家庭V网与联系人联系人、
            未知号码页面，右边为字母快速定位。
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.click_locator_key('+')
        time.sleep(0.5)
        call.click_locator_key('视频通话')
        time.sleep(0.5)
        self.assertEqual(call.is_text_present('发起视频通话'), True)
        self.assertEqual(call.on_this_page_common('多方通话_返回'), True)
        self.assertEqual(call.on_this_page_common('呼叫'), True)
        self.assertEqual(call.on_this_page_common('联系人列表'), True)
        self.assertEqual(call.on_this_page_common('视频通话_字母'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_00041(self):
        """
            点击视频通话图标
            跳转至视频通话选择页面，页面布局左上方返回按钮，多方视频字体，
            右上方呼叫按钮，下面显示不限时长成员，家庭V网与联系人联系人、
            未知号码页面，右边为字母快速定位。
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.click_locator_key('+')
        time.sleep(0.5)
        call.click_locator_key('视频通话')
        time.sleep(1)
        call.wait_page_load_common('发起视频通话')
        time.sleep(1)
        call.click_locator_key('字母_C')
        time.sleep(0.3)
        text = call.get_element_text('字母_第一个')
        if 'C' != text:
            raise RuntimeError('快速定位出错')

    @tags('ALL', 'CMCC', 'call')
    def test_call_00042(self):
        """
            点击视频通话图标
            点击选择1个家庭网成员，1个家庭网成员的头像变化为勾选的图标，右上方呼叫字体变为蓝色显示“呼叫（1/8）”。
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.click_locator_key('+')
        time.sleep(0.5)
        call.click_locator_key('视频通话')
        time.sleep(1)
        call.wait_page_load_common('发起视频通话')
        time.sleep(1)
        call.select_contact_n(1)
        text = call.get_element_text('呼叫')
        if '呼叫(1/8)' != text:
            raise RuntimeError('测试出错')

    @tags('ALL', 'CMCC', 'call')
    def test_call_00043(self):
        """
            点击视频通话图标
            点击选择2个家庭网成员，2个家庭网成员的头像变化为勾选的图标，右上方呼叫字体变为蓝色显示“呼叫（2/8）”。
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.click_locator_key('+')
        time.sleep(0.5)
        call.click_locator_key('视频通话')
        time.sleep(1)
        call.wait_page_load_common('发起视频通话')
        time.sleep(1)
        call.select_contact_n(2)
        text = call.get_element_text('呼叫')
        if '呼叫(2/8)' != text:
            raise RuntimeError('测试出错')

    @tags('ALL', 'CMCC', 'call')
    def test_call_00044(self):
        """
            点击视频通话图标
            点击选择3个家庭网成员，3个家庭网成员的头像变化为勾选的图标，右上方呼叫字体变为蓝色显示“呼叫（3/8）”。
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.click_locator_key('+')
        time.sleep(0.5)
        call.click_locator_key('视频通话')
        time.sleep(1)
        call.wait_page_load_common('发起视频通话')
        time.sleep(1)
        call.select_contact_n(3)
        text = call.get_element_text('呼叫')
        if '呼叫(3/8)' != text:
            raise RuntimeError('测试出错')

    @tags('ALL', 'CMCC', 'call')
    def test_call_00045(self):
        """
            点击视频通话图标
            点击选择8个家庭网成员，8个家庭网成员的头像变化为勾选的图标，右上方呼叫字体变为蓝色显示“呼叫（8/8）”。
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.click_locator_key('+')
        time.sleep(0.5)
        call.click_locator_key('视频通话')
        time.sleep(1)
        call.wait_page_load_common('发起视频通话')
        time.sleep(1)
        call.select_contact_more(9)
        self.assertEqual(call.is_toast_exist('最多只能选择8人', timeout=8), True)

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00051(self):
        """
            弹出“通话结束”提示框，页面回到呼叫前的页面中
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        # 切换回主叫手机
        Preconditions.select_mobile('Android-移动')
        # 挂断电话
        call.tap_screen_three_point('视频界面_时长')
        call.click_locator_key('视频界面_挂断')
        # 判断是否有‘通话结束’字样
        self.assertEqual(call.is_toast_exist('通话结束'), True)
        time.sleep(5)

    @TestLogger.log('切换手机，接听视频电话')
    def to_pick_phone_video(self):
        call = CallPage()
        # 切换被叫手机
        Preconditions.select_mobile('Android-移动-N')
        count = 20
        try:
            while count > 0:
                # 如果在视频通话界面，接听视频
                if call.is_text_present('邀请你进行视频通话', default_timeout=0.5):
                    print('接听视频-->', datetime.datetime.now().date().strftime('%Y-%m-%d'),
                          datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
                    time.sleep(3)
                    call.pick_up_video_call()
                    return True
                else:
                    count -= 1
                    # 1s检测一次，20s没有接听，则失败
                    print(count, '切换手机，接听电话 --->', datetime.datetime.now().date().strftime('%Y-%m-%d'),
                          datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
                    time.sleep(0.5)
                    continue
            else:
                return False
        except Exception as e:
            traceback.print_exc()
            print(e, datetime.datetime.now().date().strftime('%Y-%m-%d'),
                  datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00052(self):
        """
            1、被叫方接到申请后点击“接听”
            2、点击“切换语音通话”按钮

            3、显示视频通话接通界面，小屏为主叫方界面（默认为前摄像头），大屏为被叫方界面（默认前摄像头）。
            界面右上角为“静音”和“免提”功能，静音默认未选中，免提默认选中。提供“切到语音通话”和“切换摄像头”的功能。
            4、跳转至语音通话页面，页面布局上方中间为被叫方头像，头像下方为被叫人名称、号码、时间显示，下方左边为静音按钮、
            中间为切到视频通话按钮、右边为免提按钮，再下方为挂断按钮，背景为灰黑色。
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00052(), True)

    @TestLogger.log()
    def check_video_call_00052(self):
        """
        1、显示视频通话接通界面，小屏为主叫方界面（默认为前摄像头），
            大屏为被叫方界面（默认前摄像头）。
            界面右上角为“静音”和“免提”功能，静音默认未选中，
            免提默认选中。提供“切到语音通话”和“切换摄像头”的功能。
        2、跳转至语音通话页面，页面布局上方中间为被叫方头像，头像下方为被叫人名称、号码、时间显示，下方左边为静音按钮、
            中间为切到视频通话按钮、右边为免提按钮，再下方为挂断按钮，背景为灰黑色。
        :return: True
        """
        call = CallPage()
        try:
            call.tap_coordinate([(100, 100), (100, 110), (100, 120)])
            time.sleep(1)
            call.tap_screen_three_point('视频界面_时长')
            self.assertEqual(call.is_element_already_exist('视频界面_静音'), True)
            # time.sleep(12)
            call.tap_screen_three_point('视频界面_时长')
            self.assertEqual('false' == call.get_one_element('视频界面_静音').get_attribute('selected'), True)
            # time.sleep(12)
            call.tap_screen_three_point('视频界面_时长')
            self.assertEqual(call.is_element_already_exist('视频界面_免提'), True)
            # time.sleep(12)
            call.tap_screen_three_point('视频界面_时长')
            self.assertEqual('true' == call.get_one_element('视频界面_免提').get_attribute('selected'), True)
            # time.sleep(12)
            call.tap_screen_three_point('视频界面_时长')
            self.assertEqual(call.is_element_already_exist('视频界面_转为语音'), True)
            # time.sleep(12)
            call.tap_screen_three_point('视频界面_时长')
            self.assertEqual(call.is_element_already_exist('视频界面_切换摄像头'), True)
            time.sleep(12)
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_转为语音')
            time.sleep(1)
            self.assertEqual(call.is_element_already_exist('视频界面_头像'), True)
            self.assertEqual(call.is_element_already_exist('视频界面_备注'), True)
            self.assertEqual(call.is_element_already_exist('视频界面_号码'), True)
            self.assertEqual(call.is_element_already_exist('语音界面_时长'), True)
            self.assertEqual(call.is_element_already_exist('语音界面_静音'), True)
            self.assertEqual(call.is_element_already_exist('语音界面_转为视频'), True)
            self.assertEqual(call.is_element_already_exist('语音界面_免提'), True)
            self.assertEqual(call.is_element_already_exist('语音界面_挂断'), True)
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            call.click_locator_key('语音界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00053(self):
        """
            1、被叫方接到申请后点击“接听”
            2、点击“切换语音通话”按钮
            3、被叫方接到申请后点击“接听”
            4、点击静音按钮
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00053(), True)

    @TestLogger.log()
    def check_video_call_00053(self):
        """
        1、显示视频通话接通界面，小屏为主叫方界面（默认为前摄像头），
            大屏为被叫方界面（默认前摄像头）。
            界面右上角为“静音”和“免提”功能，静音默认未选中，
            免提默认选中。提供“切到语音通话”和“切换摄像头”的功能。
        2、跳转至语音通话页面，页面布局上方中间为被叫方头像，头像下方为被叫人名称、号码、时间显示，下方左边为静音按钮、
            中间为切到视频通话按钮、右边为免提按钮，再下方为挂断按钮，背景为灰黑色。
        :return: True
        """
        call = CallPage()
        try:
            call.click_locator_key('视频界面_免提')
            call.tap_coordinate([(100, 100), (100, 110), (100, 120)])
            time.sleep(1)
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_静音')
            self.assertEqual('true' == call.get_one_element('视频界面_静音').get_attribute('selected'), True)
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00054(self):
        """
            1、被叫方接到申请后点击“接听”
            2、点击“切换语音通话”按钮
            3、被叫方接到申请后点击“接听”
            4、点击免提按钮
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00054(), True)

    @TestLogger.log()
    def check_video_call_00054(self):
        """
        1、被叫方接到申请后点击“接听”
        2、点击免提按钮"
        3、显示视频通话接通界面，小屏为主叫方界面（默认为前摄像头），大屏为被叫方界面（默认前摄像头）。界面右上角为“静音”和“免提”功能，静音默认未选中，免提默认选中。
        提供“切到语音通话”和“切换摄像头”的功能。
        4、免提按钮亮起（对方说话声音变大）。"
        """
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_免提')
            self.assertEqual('false' == call.get_one_element('视频界面_免提').get_attribute('selected'), True)

            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00055(self):
        """
            1、被叫方接到申请后点击“接听”
            2、点击“切换语音通话”按钮
            3、被叫方接到申请后点击“接听”
            4、点击免提按钮
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00055(), True)

    @TestLogger.log()
    def check_video_call_00055(self):
        """
        1、被叫方接到申请后点击“接听”
        2、点击免提按钮"
        3、显示视频通话接通界面，小屏为主叫方界面（默认为前摄像头），大屏为被叫方界面（默认前摄像头）。界面右上角为“静音”和“免提”功能，静音默认未选中，免提默认选中。
        提供“切到语音通话”和“切换摄像头”的功能。
        4、主叫点击“切换摄像头”，小屏显示主叫后摄像头的界面。
        """
        call = CallPage()
        try:
            # 主叫
            Preconditions.select_mobile('Android-移动')
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_切换摄像头')
            time.sleep(2)
            # call.tap_screen_three_point('视频界面_时长')
            # call.click_locator_key('视频界面_挂断')
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00056(self):
        """
            1、被叫方接到申请后点击“接听”
            2、点击“切换语音通话”按钮
            3、被叫方接到申请后点击“接听”
            4、点击挂断按钮
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        try:
            # 初始化被叫手机
            Preconditions.initialize_class('Android-移动-N')
            # 获取手机号码
            cards = call.get_cards(CardType.CHINA_MOBILE)
            # 切换主叫手机
            Preconditions.select_mobile('Android-移动')
            # 拨打视频电话
            call.pick_up_p2p_video(cards)
            # 等待返回结果
            self.assertEqual(self.to_pick_phone_video(), True)
            self.assertEqual(self.check_video_call_00056(), True)
            # 切换回主叫手机
            Preconditions.select_mobile('Android-移动')
            time.sleep(12)
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')
            print('视频界面_挂断')
            self.assertEqual(call.is_toast_exist('通话结束'), True)
            time.sleep(3)
            self.assertEqual(call.is_on_this_page(), True)
            time.sleep(2)
        except Exception as e:
            traceback.print_exc()
            print('测试出错')
            if call.is_element_already_exist('视频界面_挂断'):
                call.click_locator_key('视频界面_挂断')
        finally:
            call.tap_screen_three_point('视频界面_时长')
            if call.is_element_already_exist('视频界面_挂断'):
                call.click_locator_key('视频界面_挂断')

    @TestLogger.log()
    def check_video_call_00056(self):
        """
        1、被叫方接到申请后点击“接听”
        2、点击挂断按钮"
        3、显示视频通话接通界面，小屏为主叫方界面（默认为前摄像头），大屏为被叫方界面（默认前摄像头）。界面右上角为“静音”和“免提”功能，静音默认未选中，免提默认选中。
        提供“切到语音通话”和“切换摄像头”的功能。
        4、弹出“通话结束”提示框，回到呼叫前页面中
        """
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_免提')
            self.assertEqual('false' == call.get_one_element('视频界面_免提').get_attribute('selected'), True)
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00058(self):
        """
            1、被叫方接到申请后点击“接听”
            2、点击“切换语音通话”按钮
            3、被叫方接到申请后点击“接听”
            4、点击挂断按钮
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        try:
            # 初始化被叫手机
            Preconditions.initialize_class('Android-移动-N')
            # 获取手机号码
            cards = call.get_cards(CardType.CHINA_MOBILE)
            # 切换主叫手机
            Preconditions.select_mobile('Android-移动')
            # 拨打视频电话
            call.pick_up_p2p_video(cards)
            # 等待返回结果
            self.assertEqual(self.to_pick_phone_00058(), True)
        except Exception as e:
            traceback.print_exc()
            print('测试出错')
            raise

    @TestLogger.log('切换手机，接听电话')
    def to_pick_phone_00058(self):
        call = CallPage()
        # 切换手机
        try:
            Preconditions.select_mobile('Android-移动-N')
            self.assertEqual(call.is_element_already_exist('视频界面_头像'), True)
            self.assertEqual(call.is_element_already_exist('视频界面_备注'), True)
            self.assertEqual(call.is_element_already_exist('视频界面_号码'), True)
            self.assertEqual(call.is_text_present('进行视频通话'), True)
            self.assertEqual(call.is_element_already_exist('视频通话_挂断'), True)
            self.assertEqual(call.is_element_already_exist('视频通话_接听'), True)
            return True
        except Exception as e:
            traceback.print_exc()
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00059(self):
        """
            视频通话页面（被叫方不在线）
            1、被叫方接到申请后长时间未点击“接听”或“挂断”（根据SDK反馈的结果）
            2、显示“用户暂时无法接通”，回到呼叫前的页面中
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        try:
            # 切换主叫手机
            Preconditions.initialize_class('Android-移动-N')
            # 获取手机号码
            cards = call.get_cards(CardType.CHINA_MOBILE)
            call.set_network_status(0)
            # 切换主叫手机
            Preconditions.select_mobile('Android-移动')
            # 拨打视频电话
            call.pick_up_p2p_video(cards)
            time.sleep(20)
            self.assertEqual(call.is_toast_exist('对方未接听', timeout=20), True)
        finally:
            Preconditions.select_mobile('Android-移动-N')
            call.set_network_status(6)
            print('已设置被叫手机网络为开启')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00060(self):
        """
            1、被叫方接到申请后点击“接听”
            2、点击“切换语音通话”按钮
            3、被叫方接到申请后点击“接听”
            4、点击静音按钮
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00060(), True)

    @TestLogger.log()
    def check_video_call_00060(self):
        """
        1、显示视频通话接通界面，小屏为主叫方界面（默认为前摄像头），
            大屏为被叫方界面（默认前摄像头）。
            界面右上角为“静音”和“免提”功能，静音默认未选中，
            免提默认选中。提供“切到语音通话”和“切换摄像头”的功能。
        2、跳转至语音通话页面，页面布局上方中间为被叫方头像，头像下方为被叫人名称、号码、时间显示，下方左边为静音按钮、
            中间为切到视频通话按钮、右边为免提按钮，再下方为挂断按钮，背景为灰黑色。
        :return: True
        """
        call = CallPage()
        try:
            call.click_locator_key('视频界面_免提')
            call.tap_coordinate([(100, 100), (100, 110), (100, 120)])
            time.sleep(1)
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_静音')
            if 'true' != call.get_one_element('视频界面_静音').get_attribute('selected'):
                raise RuntimeError('静音出错')
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00061(self):
        """
            1、被叫方接到申请后点击“接听”
            2、点击“切换语音通话”按钮
            3、被叫方接到申请后点击“接听”
            4、点击免提按钮
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00061(), True)

    @TestLogger.log()
    def check_video_call_00061(self):
        """
        1、被叫方接到申请后点击“接听”
        2、点击免提按钮"
        3、显示视频通话接通界面，小屏为主叫方界面（默认为前摄像头），大屏为被叫方界面（默认前摄像头）。界面右上角为“静音”和“免提”功能，静音默认未选中，免提默认选中。
        提供“切到语音通话”和“切换摄像头”的功能。
        4、免提按钮亮起（对方说话声音变大）。"
        """
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_免提')
            if 'false' != call.get_one_element('视频界面_免提').get_attribute('selected'):
                raise RuntimeError('关闭免提出错')
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00063(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在语音通话接通页面
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00063(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00063(self):
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_转为语音')
            time.sleep(1)
            call.click_locator_key('语音界面_转为视频')
            self.assertEqual(call.is_element_already_exist('切视频_头像'), True)
            self.assertEqual(call.is_element_already_exist('切视频_备注'), True)
            self.assertEqual(call.is_element_already_exist('切视频_号码'), True)
            self.assertEqual(call.is_text_present('正在等待对方接受邀请'), True)
            time.sleep(15)
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            call.click_locator_key('语音界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00064(self):
        """
            1、4G网络
            2、已登录客户端
            3、跳转至等待邀请页面，页面布局为上部为头像、名称、号码、正在等待对方接受邀请...,下方为挂断按钮。
            4、弹出“通话结束”提示框，回到呼叫前的页面中，toast弹出的位置在底部“静音”三个按钮之上"
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00064(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00064(self):
        call = CallPage()
        try:
            # 切回到主叫手机
            Preconditions.select_mobile('Android-移动')
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')
            self.assertEqual(call.is_toast_exist('通话结束'), True)
            return True
        except Exception as e:
            traceback.print_exc()
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00065(self):
        """
            1、对方点击了切换视频通话按钮
            2、点击接受按钮
            3、弹出“xxx邀请你进行视频通话”接受与取消按钮
            4、跳转至视频通话接通页面
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00065(), True)
        time.sleep(5)

    @TestLogger.log('验证结果')
    def check_video_call_00065(self):
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_转为语音')
            time.sleep(1)
            call.click_locator_key('语音界面_转为视频')
            # 切回到主叫手机
            Preconditions.select_mobile('Android-移动')
            if call.is_text_present('邀请你进行视频通话', default_timeout=0.5):
                call.click_locator_key('切视频_接受')
                print('切为视频--接受')
            call.tap_screen_three_point('视频界面_时长')
            self.assertEqual(call.is_element_already_exist('视频界面_时长'), True)
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00066(self):
        """
            1、对方点击了切换视频通话按钮
            2、点击接受按钮
            3、弹出“xxx邀请你进行视频通话”接受与取消按钮
            4、跳转至视频通话接通页面
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00066(), True)
        time.sleep(5)

    @TestLogger.log('验证结果')
    def check_video_call_00066(self):
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_转为语音')
            time.sleep(1)
            call.click_locator_key('语音界面_转为视频')
            # 切回到主叫手机
            Preconditions.select_mobile('Android-移动')
            if call.is_text_present('邀请你进行视频通话', default_timeout=0.5):
                call.click_locator_key('切视频_取消')
                print('切视频_取消')
            self.assertEqual(call.is_element_already_exist('语音界面_转为视频'), True)
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('语音界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00068(self):
        """
            背景中前置摄像头改为后置摄像头，持续到视频通话接通页面中
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        time.sleep(2)
        # 检测页面元素
        self.assertEqual(self.check_video_call_00068(), True)

    @TestLogger.log()
    def check_video_call_00068(self):
        """
        背景中前置摄像头改为后置摄像头，持续到视频通话接通页面中
        """
        call = CallPage()
        try:
            time.sleep(5)
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_切换摄像头')
            time.sleep(2)
            return True
        except Exception as e:
            traceback.print_exc()
            print(e, datetime.datetime.now().date().strftime('%Y-%m-%d'),
                  datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00069(self):
        """
            1、对方点击了切换视频通话按钮
            2、点击接受按钮
            3、弹出“xxx邀请你进行视频通话”接受与取消按钮
            4、跳转至视频通话接通页面
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        global flag
        flag = True
        t = threading.Thread(target=self.reject_phone_video())
        print('start:', t.getName())
        t.start()
        print('check')
        Preconditions.select_mobile('Android-移动')
        print('已切换：', current_mobile())
        self.assertEqual(self.check_video_call_00069(), True)
        print('thread join')
        t.join()
        time.sleep(5)

    @TestLogger.log('拒绝接听视频电话')
    def reject_phone_video(self):
        global flag
        count = 60
        call = CallPage()
        Preconditions.select_mobile('Android-移动-N')
        print('已切换：', current_mobile())
        time.sleep(5)
        while count > 0 or flag:
            if count <= 0:
                flag = False
            try:
                if call.is_text_present('邀请你进行视频通话', default_timeout=0.5):
                    time.sleep(10)
                    print('视频通话_挂断', datetime.datetime.now().date().strftime('%Y-%m-%d'),
                          datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
                    call.click_locator_key('视频通话_挂断')
                    flag = False
                    return
            except Exception as e:
                traceback.print_exc()
                print('视频通话_挂断_出错', datetime.datetime.now().date().strftime('%Y-%m-%d'),
                      datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
                return
            count -= 1
            print('视频通话_挂断--->count:', count, datetime.datetime.now().date().strftime('%Y-%m-%d'),
                  datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
            time.sleep(0.5)

    @TestLogger.log('验证结果')
    def check_video_call_00069(self):
        call = CallPage()
        try:
            count = 5
            while count > 0:
                if call.is_toast_exist('对方拒绝了你的通话邀请', timeout=3):
                    print('已检测到提示文本，执行成功', datetime.datetime.now().date().strftime('%Y-%m-%d'),
                          datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
                    return True
                count -= 1
                print('count ---> ', count, datetime.datetime.now().date().strftime('%Y-%m-%d'),
                      datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
        except Exception as e:
            traceback.print_exc()
            print('已检测到提示文本，执行成功', datetime.datetime.now().date().strftime('%Y-%m-%d'),
                  datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00070(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话邀请页面
            4、被叫方接到申请后点击“接听”
            5、点击“切换语音通话”按钮
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00070(), True)
        time.sleep(5)

    @TestLogger.log('验证结果')
    def check_video_call_00070(self):
        """
        1、对方接通后，开始计通话时长。静音、免提、切为语音通话、切换摄像头状态：
        （1）""静音""默认为可选（未选中）状态。
        （2）“免提”默认为选中状态（即免提打开）。
        （3）“切为语音通话”变为可选（未选中）状态。
        （4）“切换摄像头”的状态同呼叫中的状态保持一致。
        2、视频通话过程中，如果自己切为语音通话，弹出toast提示，“已切为语音通话，请使用听筒接听”。
        如果是对方切为语音通话，则提示，“对方切为语音通话，请使用听筒接听”。
        （1）toast弹出的位置在底部“挂断”按钮之上。
        """
        call = CallPage()
        try:
            time.sleep(3)
            call.tap_screen_three_point('视频界面_时长')
            self.assertEqual('false' == call.get_one_element('视频界面_静音').get_attribute('selected'), True)
            call.tap_screen_three_point('视频界面_时长')
            self.assertEqual('true' == call.get_one_element('视频界面_免提').get_attribute('selected'), True)
            call.tap_screen_three_point('视频界面_时长')
            self.assertEqual('false' == call.get_one_element('视频界面_转为语音').get_attribute('selected'), True)
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_转为语音')
            self.assertEqual(call.is_toast_exist('已切为语音通话，请使用听筒接听'), True)
            # call.click_locator_key('语音界面_转为视频')
            # # 主叫
            # Preconditions.select_mobile('Android-移动')
            # call.click_locator_key('切视频_接受')
            # time.sleep(1)
            # call.tap_screen_three_point('视频界面_时长')
            # call.click_locator_key('视频界面_转为语音')
            # # 被叫
            # Preconditions.select_mobile('Android-移动-N')
            # self.assertEqual(call.is_toast_exist('对方切为语音通话，请使用听筒接听'), True)
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            if call.is_element_already_exist('语音界面_挂断'):
                call.click_locator_key('语音界面_挂断')
