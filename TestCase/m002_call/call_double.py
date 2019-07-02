import threading
import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestLogger import TestLogger
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages.guide import GuidePage
from pages.login.LoginPage import OneKeyLoginPage
from pages.call.CallPage import CallPage
from library.core.TestCase import TestCase
from pages.components.Footer import FooterPage

import time
import datetime
import warnings
import traceback

from pages.mine.MinePage import MinePage

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
        call_page.remove_mask_c(2)

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

    @staticmethod
    def close_system_update():
        """确保每个用例开始之前在通话界面界面"""
        call = CallPage()
        if call.is_text_present_c('系统更新'):
            call.click_text('稍后')
            time.sleep(1)
            call.click_text('取消')

    @staticmethod
    def get_remaining_call_time():
        """获取剩余飞信电话时长"""
        call = CallPage()
        call.wait_for_page_load()
        footer = FooterPage()
        footer.open_me_page()
        time.sleep(1)
        mine = MinePage()
        times = 0
        if mine.is_element_already_exist_c('剩余时长_标签'):
            times = int(mine.get_element_text_c('剩余时长_时长'))
        footer.open_call_page()
        return times


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
#         call_page.click_locator_key('多方电话_返回')
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

# noinspection PyBroadException
class CallPageTest(TestCase):
    """Call 模块--全量"""

    @TestLogger.log('执行SetUp')
    def default_setUp(self):
        """确保每个用例开始之前在通话界面界面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('Android-移动')
        Preconditions.close_system_update()
        Preconditions.make_already_in_call_page()

    @TestLogger.log('执行TearDown')
    def default_tearDown(self):
        call = CallPage()
        if call.get_network_status() != 6:
            call.set_network_status(6)
        time.sleep(2)

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
                    time.sleep(1)
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

    @TestLogger.log('切换手机，接听多人视频电话')
    def to_pick_multi_video(self):
        call = CallPage()
        # 切换被叫手机
        Preconditions.select_mobile('Android-移动-N')
        count = 20
        try:
            while count > 0:
                # 如果在视频通话界面，接听视频
                if call.is_text_present('邀请你进行多方视频通话', default_timeout=0.5):
                    print('接听视频-->', datetime.datetime.now().date().strftime('%Y-%m-%d'),
                          datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
                    time.sleep(1)
                    call.click_locator_key_c('多方视频_接听')
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

    @TestLogger.log('切换手机，接听语音电话')
    def to_pick_phone_voice(self):
        call = CallPage()
        # 切换被叫手机
        Preconditions.select_mobile('Android-移动-N')
        count = 20
        try:
            while count > 0:
                # 如果在视频通话界面，接听
                if call.is_text_present_c('短信', default_timeout=0.5) \
                        and call.is_text_present_c('提醒', default_timeout=0.5):
                    print('接听语音电话-->', datetime.datetime.now().date().strftime('%Y-%m-%d'),
                          datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
                    time.sleep(1)
                    call.pick_up_the_call()
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

    # 注：是从0002开始的，没有0001

    @tags('ALL', 'CMCC_double', 'call')
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
        if len(call.get_elements_list('视频通话')) <= 0:
            # 初始化被叫手机
            Preconditions.initialize_class('Android-移动-N')
            # 获取手机号码
            cards = call.get_cards(CardType.CHINA_MOBILE)
            # 切换主叫手机
            Preconditions.select_mobile('Android-移动')
            # 拨打视频电话
            call.pick_up_p2p_video(cards)
            self.to_pick_phone_video()
            time.sleep(3)
            call.tap_screen_three_point()
            call.click_locator_key('视频界面_挂断')
            # 切换主叫手机
            Preconditions.select_mobile('Android-移动')
        time.sleep(1)
        call.click_tag_detail_first_element('视频通话')
        # 判断
        time.sleep(1)
        self.assertEqual(call.on_this_page_call_detail(), True)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 详情_通话  详情_视频 详情_返回
        self.assertEqual(call.is_element_already_exist('详情_通话'), True)
        self.assertEqual(call.is_element_already_exist('详情_视频'), True)
        self.assertEqual(call.is_element_already_exist('详情_返回'), True)
        # 头像  名字  通话时间  通话类型
        self.assertEqual(call.is_element_already_exist('详情_头像'), True)
        self.assertEqual(call.is_element_already_exist('详情_名称'), True)
        self.assertEqual(call.is_element_already_exist('详情_通话时间'), True)
        self.assertEqual(call.is_element_already_exist('详情_返回'), True)
        self.assertEqual(call.is_element_already_exist('详情_通话时长'), True)
        if '通话记录 (视频通话)' != call.get_text(("id", 'com.cmic.college:id/tvCallRecordsType')):
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00019(self):
        """
            1、联网正常已登录
            2、对方离线
            3、当前页通话记录详情
            1、点击视频通话---1、进入拨打视频通话界面，并弹出提示窗，“对方未接听，请稍候再尝试”
        """
        call = CallPage()

        call.wait_for_page_call_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.clear_all_record()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        call.set_network_status(0)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        time.sleep(3)
        call.click_locator_key('视频界面_挂断')
        time.sleep(8)
        call.click_tag_detail_first_element('视频通话')
        time.sleep(1)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 1. 点击视频通话按钮
        call.click_locator_key('详情_视频')
        time.sleep(1)
        if call.on_this_page_flow():
            call.set_not_reminders()
            time.sleep(0.5)
            call.click_locator_key('流量_继续拨打')
        time.sleep(25)
        count = 20
        while count > 0:
            exist = call.is_toast_exist("对方未接听，请稍候再尝试", timeout=0.5)
            if exist:
                break
            time.sleep(0.5)
            count -= 1

    @TestLogger.log('开启网络')
    def tearDown_test_call_00019(self):
        """开启网络"""
        call = CallPage()
        Preconditions.select_mobile('Android-移动-N')
        call.set_network_status(6)

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00020(self):
        """
            1、联网正常已登录
            2、对方离线
            3、当前页通话记录详情
            点击视频通话---点击取消---进入拨打视频通话界面，并弹出提示窗，“通话结束”---返回通话记录详情页
        """
        call = CallPage()
        try:
            call.wait_for_page_load()
            # 判断如果键盘已拉起，则收起键盘
            if call.is_exist_call_key():
                call.click_hide_keyboard()
                time.sleep(1)
            call.clear_all_record()
            # 初始化被叫手机
            Preconditions.initialize_class('Android-移动-N')
            # 获取手机号码
            cards = call.get_cards(CardType.CHINA_MOBILE)
            call.set_network_status(0)
            # 切换主叫手机
            Preconditions.select_mobile('Android-移动')
            # 拨打视频电话
            call.pick_up_p2p_video(cards)
            time.sleep(3)
            call.click_locator_key('视频界面_挂断')
            # # 切换主叫手机
            call.is_text_present_c('视频通话', default_timeout=8)
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
            call.click_locator_key('视频界面_挂断')
            self.assertEqual(call.is_toast_exist("通话结束"), True)
            time.sleep(3)
            self.assertEqual(call.on_this_page_call_detail(), True)
        finally:
            # 切换被叫手机
            Preconditions.select_mobile('Android-移动-N')
            call.set_network_status(0)

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00048(self):
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
        self.assertEqual(self.check_video_call_00048(), True)

    @TestLogger.log()
    def check_video_call_00048(self):
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
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00049(self):
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
        self.assertEqual(self.check_video_call_00049(), True)

    @TestLogger.log()
    def check_video_call_00049(self):
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
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00050(self):
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
        self.assertEqual(self.check_video_call_00050(), True)

    @TestLogger.log()
    def check_video_call_00050(self):
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
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

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
        except Exception:
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
        except Exception:
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
        except Exception:
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
        except Exception:
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
        except Exception:
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
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00057(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话邀请页面"
            4、被叫方接到申请后点击“接听”
            5、点击“小屏”"
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
        self.assertEqual(self.check_video_call_00057(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00057(self):
        """
            1、对方接通后，开始计通话时长。静音、免提、切为语音通话、切换摄像头状态：
            （1）""静音""默认为可选（未选中）状态。
            （2）“免提”默认为选中状态（即免提打开）。
            （3）“切为语音通话”变为可选（未选中）状态。
            （4）“切换摄像头”的状态同呼叫中的状态保持一致。
            2、主叫和被叫的界面互换，即小屏为被叫界面，大屏为主叫界面，。
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
            self.assertEqual(call.is_element_already_exist('视频界面_切换摄像头'), True)
            call.click_locator_key('视频界面_小屏')
            time.sleep(2)
            return True
        except Exception:
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
        except Exception:
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
        except Exception:
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
        except Exception:
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
        except Exception:
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
        except Exception:
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
        except Exception:
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

    @TestLogger.log('验证结果')
    def check_video_call_00065(self):
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_转为语音')
            time.sleep(5)
            call.click_locator_key('语音界面_转为视频')
            # 切回到主叫手机
            Preconditions.select_mobile('Android-移动')
            if call.is_text_present('邀请你进行视频通话', default_timeout=0.5):
                call.click_locator_key('切视频_接受')
                print('切为视频--接受')
            call.tap_screen_three_point('视频界面_时长')
            self.assertEqual(call.is_element_already_exist('视频界面_时长'), True)
            return True
        except Exception:
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
        except Exception:
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
        #
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
                    time.sleep(12)
                    print('视频通话_挂断', datetime.datetime.now().date().strftime('%Y-%m-%d'),
                          datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
                    call.click_locator_key('视频通话_挂断')
                    flag = False
                    return
            except Exception:
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
                # 持续时间太短，不一定能捕捉到
                if call.is_toast_exist('对方拒绝了你的通话邀请', timeout=3):
                    print('已检测到提示文本，执行成功', datetime.datetime.now().date().strftime('%Y-%m-%d'),
                          datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
                    return True
                count -= 1
                print('count ---> ', count, datetime.datetime.now().date().strftime('%Y-%m-%d'),
                      datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
        except Exception:
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
            self.assertEqual(call.is_element_already_exist('视频界面_切换摄像头'), True)
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
        except Exception:
            traceback.print_exc()
            return False
        finally:
            if call.is_element_already_exist('语音界面_挂断'):
                call.click_locator_key('语音界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00071(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话邀请页面
            4、被叫方接到申请后点击“接听”
            5、点击静音按钮
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
        self.assertEqual(self.check_video_call_00071(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00071(self):
        """
        "1、显示视频通话接通界面，小屏为主叫方界面（默认为前摄像头），大屏为被叫方界面（默认前摄像头）。
        界面右上角为“静音”和“免提”功能，静音默认未选中，免提默认选中。
        提供“切到语音通话”和“切换摄像头”的功能。
        2、静音按钮亮起（点击方说话无声）。"
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
            self.assertEqual(call.is_element_already_exist('视频界面_切换摄像头'), True)
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_静音')
            self.assertEqual('true' == call.get_one_element('视频界面_静音').get_attribute('selected'), True)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00072(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话邀请页面
            4、被叫方接到申请后点击“接听”
            5、点击免提按钮
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
        self.assertEqual(self.check_video_call_00072(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00072(self):
        """
        "1、显示视频通话接通界面，小屏为主叫方界面（默认为前摄像头），大屏为被叫方界面（默认前摄像头）。
        界面右上角为“静音”和“免提”功能，静音默认未选中，免提默认选中。
        提供“切到语音通话”和“切换摄像头”的功能。
        2、免提按钮亮起（对方说话声音变大）。"
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
            self.assertEqual(call.is_element_already_exist('视频界面_切换摄像头'), True)
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_免提')
            self.assertEqual('false' == call.get_one_element('视频界面_免提').get_attribute('selected'), True)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00073(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话邀请页面
            4、被叫方接到申请后点击“接听”
            5、点击免提按钮
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
        self.assertEqual(self.check_video_call_00073(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00073(self):
        """
        "1、显示视频通话接通界面，小屏为主叫方界面（默认为前摄像头），大屏为被叫方界面（默认前摄像头）。
        界面右上角为“静音”和“免提”功能，静音默认未选中，免提默认选中。
        提供“切到语音通话”和“切换摄像头”的功能。
        2、免提按钮亮起（对方说话声音变大）。"
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
            self.assertEqual(call.is_element_already_exist('视频界面_切换摄像头'), True)
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_切换摄像头')
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00074(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话邀请页面"
            4、被叫方接到申请后点击“接听”
            5、点击挂断按钮
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
        self.assertEqual(self.check_video_call_00074(), True)
        time.sleep(3)
        # # 初始化被叫手机
        # Preconditions.initialize_class('Android-移动-N')
        # 切换到主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        self.assertEqual(self.to_pick_phone_video(), True)
        call.tap_screen_three_point('视频界面_时长')
        call.click_locator_key('视频界面_挂断')
        # 切换到被叫手机
        Preconditions.select_mobile('Android-移动')
        self.assertEqual(call.is_toast_exist('对方已挂断，通话结束', timeout=3), True)
        print('已捕获‘对方已挂断，通话结束’')

    @TestLogger.log('验证结果')
    def check_video_call_00074(self):
        """
            1、对方接通后，开始计通话时长。静音、免提、切为语音通话、切换摄像头状态：
            （1）""静音""默认为可选（未选中）状态。
            （2）“免提”默认为选中状态（即免提打开）。
            （3）“切为语音通话”变为可选（未选中）状态。
            （4）“切换摄像头”的状态同呼叫中的状态保持一致。
            2、通话挂断时，双方弹出toast提示：
            （1）主动挂断一方提示“通话结束”
            （2）被挂断一方提示“对方已挂断，通话结束”
            （3）toast弹出的位置在底部“挂断”按钮之上。
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
            self.assertEqual(call.is_element_already_exist('视频界面_切换摄像头'), True)
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')
            self.assertEqual(call.is_toast_exist('通话结束', timeout=3), True)
            return True
        except Exception:
            traceback.print_exc()
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00075(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话邀请页面"
            4、被叫方接到申请后点击“接听”
            5、点击“小屏”"
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
        self.assertEqual(self.check_video_call_00075(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00075(self):
        """
            1、对方接通后，开始计通话时长。静音、免提、切为语音通话、切换摄像头状态：
            （1）""静音""默认为可选（未选中）状态。
            （2）“免提”默认为选中状态（即免提打开）。
            （3）“切为语音通话”变为可选（未选中）状态。
            （4）“切换摄像头”的状态同呼叫中的状态保持一致。
            2、主叫和被叫的界面互换，即小屏为被叫界面，大屏为主叫界面，。
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
            self.assertEqual(call.is_element_already_exist('视频界面_切换摄像头'), True)
            call.click_locator_key('视频界面_小屏')
            time.sleep(2)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00077(self):
        """
            1、断网
            2、已登录客户端
            3、当前页面在视频通话邀请页面（被叫方）
            4、查看页面显示
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        call.make_sure_have_p2p_vedio_record()
        call.click_tag_detail_first_element('视频通话')
        time.sleep(1)
        self.assertEqual(call.is_element_already_exist('详情_通话记录'), True)
        # 获取手机号码
        cards = call.get_cards(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00077(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00077(self):
        """
            弹出“通话结束”提示框，回到呼叫前的页面中，在底部“挂断”按钮上面展示
        """
        call = CallPage()
        try:
            time.sleep(3)
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')
            self.assertEqual(call.is_toast_exist('通话结束'), True)
            time.sleep(2)
            self.assertEqual(call.is_element_already_exist('详情_通话记录'), True)
            return True
        except Exception:
            traceback.print_exc()
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00078(self):
        """
            1、网络正常
            2、已登录客户端
            3、当前页面在视频通话邀请页面
            4、被叫方接到申请后长时间未点击“接听”或“挂断”（根据SDK反馈的结果）
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
        self.assertEqual(self.check_video_call_00078(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00078(self):
        """
            1、对方未接听时，弹出toast提示，“对方未接听，请稍候再尝试”
            （1） toast弹出的位置在底部“挂断”按钮之上。
        """
        call = CallPage()
        count = 60
        try:
            while count > 0:
                if call.is_toast_exist('对方未接听，请稍候再尝试', timeout=0.5):
                    return True
                else:
                    count -= 1
                    time.sleep(0.5)
                    print('count:', count, datetime.datetime.now().date().strftime('%Y-%m-%d'),
                          datetime.datetime.now().time().strftime("%H-%M-%S-%f"))
                    continue
            else:
                return False
        except Exception:
            traceback.print_exc()
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00079(self):
        """
            1、网络正常
            2、已登录客户端
            3、当前页面在视频通话邀请页面
            4、被叫方接到申请后点击“挂断”
            5、对方拒绝接听时，弹出toast提示，“对方拒绝了你的通话邀请” toast弹出的位置在底部“挂断”按钮之上。
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
        # 切换到被叫手机
        Preconditions.select_mobile('Android-移动-N')
        call.click_locator_key('视频通话_挂断')
        Preconditions.select_mobile('Android-移动')
        self.assertEqual(call.is_toast_exist('对方拒绝了你的通话邀请'), True)

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00080(self):
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
        self.assertEqual(self.check_video_call_00080(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00080(self):
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_转为语音')
            time.sleep(5)
            call.click_locator_key('语音界面_转为视频')
            # 切回到主叫手机
            Preconditions.select_mobile('Android-移动')
            if call.is_text_present('邀请你进行视频通话', default_timeout=0.5):
                call.click_locator_key('切视频_接受')
                print('切为视频--接受')
            call.tap_screen_three_point('视频界面_时长')
            self.assertEqual(call.is_element_already_exist('视频界面_时长'), True)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00081(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话接通页面
            4、点击“编辑笔”按钮
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
        self.assertEqual(self.check_video_call_00081(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00081(self):
        """
            则在下方依次弹出“线条调色”、“线条粗细”、“橡皮檫粗细”、“清除涂鸦”、“表情贴纸”和“分享”；
        """
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_免提')
            call.click_locator_key('视频界面_涂鸦')
            self.assertEqual(call.is_element_already_exist('涂鸦_颜色'), True)
            self.assertEqual(call.is_element_already_exist('涂鸦_曲线'), True)
            self.assertEqual(call.is_element_already_exist('涂鸦_橡皮'), True)
            self.assertEqual(call.is_element_already_exist('涂鸦_删除'), True)
            self.assertEqual(call.is_element_already_exist('涂鸦_表情'), True)
            self.assertEqual(call.is_element_already_exist('涂鸦_分享'), True)
            call.click_locator_key('涂鸦_返回')
            call.click_locator_key('视频界面_挂断')
            return True
        except Exception:
            traceback.print_exc()
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00082(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话接通页面
            4、已进入涂鸦入口
            4、点击“线条调色”icon
            5、任意点击一种颜色后
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
        self.assertEqual(self.check_video_call_00082(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00082(self):
        """
            1、可以打开可供选择的颜色
            2、可以手动在视频通话窗口进行随意的涂鸦
        """
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_免提')
            call.click_locator_key('视频界面_涂鸦')
            time.sleep(1)
            call.click_locator_key('涂鸦_颜色')
            time.sleep(0.5)
            call.click_locator_key('涂鸦_橙色')
            time.sleep(0.5)
            call.press_move_to_down('涂鸦_画布')
            time.sleep(5)
            call.click_locator_key('涂鸦_返回')
            call.click_locator_key('视频界面_挂断')
            return True
        except Exception:
            traceback.print_exc()
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00083(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话接通页面
            4、已进入涂鸦入口
            5、点击“表情贴纸”icon
            6、任意点击一种贴纸"
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
        self.assertEqual(self.check_video_call_00083(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00083(self):
        """
            1、可以打开可供选择的视频涂鸦贴纸
            2、点击屏幕即可出现表情，并且支持随意拖动
        """
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_免提')
            call.click_locator_key('视频界面_涂鸦')
            time.sleep(1)
            call.click_locator_key('涂鸦_表情')
            time.sleep(0.5)
            call.click_locator_key('涂鸦_表情1')
            time.sleep(2)
            call.tap_coordinate([(500, 200)])
            call.press_move_to_down('涂鸦_表情移动框')
            time.sleep(5)
            call.click_locator_key('涂鸦_返回')
            call.click_locator_key('视频界面_挂断')
            return True
        except Exception:
            traceback.print_exc()
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00084(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话接通页面
            4、已进入涂鸦入口"	"1、点击“线条粗细”icon
            2、选择粗线条（细线条）
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
        self.assertEqual(self.check_video_call_00084(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00084(self):
        """
            1、可以打开可供选择的粗细线条
            2、涂鸦的线条粗（涂鸦的线条细）
        """
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_免提')
            call.click_locator_key('视频界面_涂鸦')
            time.sleep(1)
            call.click_locator_key('涂鸦_曲线')
            time.sleep(0.5)
            call.swipe_direction('涂鸦_滑块', 'right')
            time.sleep(0.5)
            call.click_locator_key('涂鸦_曲线')
            time.sleep(0.5)
            call.press_move_to_down('涂鸦_画布')
            time.sleep(5)
            call.click_locator_key('涂鸦_返回')
            call.click_locator_key('视频界面_挂断')
            return True
        except Exception:
            traceback.print_exc()
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00085(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话接通页面
            4、已进入涂鸦入口"	"1、点击“线条粗细”icon
            2、选择粗线条（细线条）
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
        self.assertEqual(self.check_video_call_00085(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00085(self):
        """
            1、可以打开可供选择的粗细线条
            2、涂鸦的线条粗（涂鸦的线条细）
        """
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_免提')
            call.click_locator_key('视频界面_涂鸦')
            time.sleep(1)
            call.click_locator_key('涂鸦_曲线')
            time.sleep(0.5)
            call.swipe_direction('涂鸦_滑块', 'left')
            time.sleep(0.5)
            call.click_locator_key('涂鸦_曲线')
            time.sleep(0.5)
            call.press_move_to_down('涂鸦_画布')
            time.sleep(5)
            call.click_locator_key('涂鸦_返回')
            call.click_locator_key('视频界面_挂断')
            return True
        except Exception:
            traceback.print_exc()
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00086(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话接通页面
            4、已进入涂鸦入口
            5、点击“清除涂鸦”icon
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
        self.assertEqual(self.check_video_call_00086(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00086(self):
        """
            1、清除显示屏上所有的涂鸦
        """
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_免提')
            call.click_locator_key('视频界面_涂鸦')
            time.sleep(1)
            call.press_move_to_down('涂鸦_画布')
            time.sleep(2)
            call.click_locator_key('涂鸦_橡皮')
            time.sleep(3)
            call.click_locator_key('涂鸦_返回')
            call.click_locator_key('视频界面_挂断')
            return True
        except Exception:
            traceback.print_exc()
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00087(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话接通页面
            4、已进入涂鸦入口
            5、点击“清除涂鸦”icon
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
        self.assertEqual(self.check_video_call_00087(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00087(self):
        """
            1、清除显示屏上所有的涂鸦
        """
        call = CallPage()
        try:
            call.tap_screen_three_point('视频界面_时长')
            call.click_locator_key('视频界面_免提')
            call.click_locator_key('视频界面_涂鸦')
            time.sleep(1)
            call.click_locator_key('涂鸦_分享')
            time.sleep(1)
            call.click_locator_key('涂鸦_分享到微信')
            self.assertEqual(call.is_toast_exist('未安装微信'), True)
            time.sleep(3)
            call.click_locator_key('涂鸦_返回')
            call.click_locator_key('视频界面_挂断')
            return True
        except Exception:
            traceback.print_exc()
            return False

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00096(self):
        """
            1.当前正在视频通话页面
            2.涂鸦功能列表未展开"
            3.本机点击视频涂鸦按钮
            4.本机涂鸦功能列表展开
            5.“静音”、“免提”、“挂断”、“切换摄像头”等按钮隐藏"
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
        self.assertEqual(self.check_video_call_00096(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00096(self):
        """
            1.本机涂鸦功能列表展开
            2.“静音”、“免提”、“挂断”、“切换摄像头”等按钮隐藏
        """
        call = CallPage()
        try:
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_免提')
            # 切换到主叫手机
            Preconditions.select_mobile('Android-移动')
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_免提')
            call.click_locator_key_c('视频界面_涂鸦')
            time.sleep(1)
            self.assertEqual(call.is_element_already_exist_c('视频界面_静音'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_免提'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_挂断'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_切换摄像头'), False)
            time.sleep(3)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.click_locator_key_c('涂鸦_返回')
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00097(self):
        """
            1.当前正在视频通话页面
            2.涂鸦功能列表未展开"
            3.对方点击视频涂鸦按钮
            4.本机涂鸦功能列表展开
            5.“静音”、“免提”、“挂断”、“切换摄像头”等按钮隐藏"
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00097(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00097(self):
        """
            1.本机涂鸦功能列表展开
            2.“静音”、“免提”、“挂断”、“切换摄像头”等按钮隐藏
        """
        call = CallPage()
        try:
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_免提')
            call.click_locator_key_c('视频界面_涂鸦')
            # 切换到主叫手机
            Preconditions.select_mobile('Android-移动')
            time.sleep(1)
            self.assertEqual(call.is_element_already_exist_c('视频界面_静音'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_免提'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_挂断'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_切换摄像头'), False)
            time.sleep(3)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.click_locator_key_c('涂鸦_返回')
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00098(self):
        """
            1.当前正在视频通话页面
            2.涂鸦功能列表未展开"
            3.本机点击视频涂鸦返回按钮
            4.本机涂鸦功能列表隐藏
            5.展示“静音”、“免提”、“挂断”、“切换摄像头”等按钮
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00098(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00098(self):
        """
            1.本机涂鸦功能列表隐藏
            2.展示“静音”、“免提”、“挂断”、“切换摄像头”等按钮
        """
        call = CallPage()
        try:
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_免提')
            # 切换到主叫手机
            Preconditions.select_mobile('Android-移动')
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_免提')
            call.click_locator_key_c('视频界面_涂鸦')
            time.sleep(1)
            call.click_locator_key_c('涂鸦_返回')
            time.sleep(1)
            call.tap_screen_three_point_element_c('视频界面_时长')
            self.assertEqual(call.is_element_already_exist_c('视频界面_静音'), True)
            call.tap_screen_three_point_element_c('视频界面_时长')
            self.assertEqual(call.is_element_already_exist_c('视频界面_免提'), True)
            call.tap_screen_three_point_element_c('视频界面_时长')
            self.assertEqual(call.is_element_already_exist_c('视频界面_挂断'), True)
            call.tap_screen_three_point_element_c('视频界面_时长')
            self.assertEqual(call.is_element_already_exist_c('视频界面_切换摄像头'), True)
            time.sleep(3)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_00099(self):
        """
            1.当前正在视频通话页面
            2.涂鸦功能列表未展开"
            3.对方点击视频涂鸦返回按钮
            4.本机涂鸦功能列表隐藏
            5.展示“静音”、“免提”、“挂断”、“切换摄像头”等按钮
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_00099(), True)

    @TestLogger.log('验证结果')
    def check_video_call_00099(self):
        """
            1.本机涂鸦功能列表隐藏
            2.展示“静音”、“免提”、“挂断”、“切换摄像头”等按钮
        """
        call = CallPage()
        try:
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_免提')
            # 切换到主叫手机
            Preconditions.select_mobile('Android-移动')
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_涂鸦')
            time.sleep(2)
            # 切换到被叫手机
            Preconditions.select_mobile('Android-移动-N')
            call.click_locator_key_c('涂鸦_返回')
            time.sleep(2)
            Preconditions.select_mobile('Android-移动')
            call.tap_screen_three_point_element_c('视频界面_时长')
            self.assertEqual(call.is_element_already_exist_c('视频界面_静音'), True)
            call.tap_screen_three_point_element_c('视频界面_时长')
            self.assertEqual(call.is_element_already_exist_c('视频界面_免提'), True)
            call.tap_screen_three_point_element_c('视频界面_时长')
            self.assertEqual(call.is_element_already_exist_c('视频界面_挂断'), True)
            call.tap_screen_three_point_element_c('视频界面_时长')
            self.assertEqual(call.is_element_already_exist_c('视频界面_切换摄像头'), True)
            time.sleep(3)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000103(self):
        """
            1.当前正在视频通话页面
            2.涂鸦功能列表未展开"
            3.对方点击视频涂鸦返回按钮
            4.本机涂鸦功能列表隐藏
            5.展示“静音”、“免提”、“挂断”、“切换摄像头”等按钮
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_000103(), True)

    @TestLogger.log('验证结果')
    def check_video_call_000103(self):
        """
            1.本机涂鸦功能列表隐藏
            2.展示“静音”、“免提”、“挂断”、“切换摄像头”等按钮
        """
        call = CallPage()
        try:
            call.tap_screen_three_point_element_c('视频界面_时长')
            self.assertEqual('true' == call.get_select_value_c('视频界面_免提'), True)
            time.sleep(3)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000104(self):
        """
            1、4G网络
            2、已登录客户端
            3、当前页面在视频通话接听页面
            4、点击非icon区域
            5、再点击非icon区域
            6、隐藏界面其它，只显示两个视频窗口
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_000104(), True)

    @TestLogger.log('验证结果')
    def check_video_call_000104(self):
        """
            1、点击非icon区域
            2、再点击非icon区域
            3、隐藏界面其它，只显示两个视频窗口
        """
        call = CallPage()
        try:
            if call.is_element_already_exist_c('视频界面_时长'):
                call.tap_screen_center_c('视频界面_主元素')
                time.sleep(1)
                self.assertEqual(call.is_element_already_exist_c('视频界面_免提'), False)
                self.assertEqual(call.is_element_already_exist_c('视频界面_静音'), False)
                self.assertEqual(call.is_element_already_exist_c('视频界面_转为语音 '), False)
                self.assertEqual(call.is_element_already_exist_c('视频界面_涂鸦'), False)
                self.assertEqual(call.is_element_already_exist_c('视频界面_切换摄像头'), False)
                self.assertEqual(call.is_element_already_exist_c('视频界面_挂断'), False)
                self.assertEqual(call.is_element_already_exist_c('视频界面_小屏'), True)
            else:
                call.tap_screen_center_c('视频界面_主元素')
                self.assertEqual(call.is_element_already_exist_c('视频界面_免提'), True)
                self.assertEqual(call.is_element_already_exist_c('视频界面_静音'), True)
                self.assertEqual(call.is_element_already_exist_c('视频界面_转为语音 '), True)
                self.assertEqual(call.is_element_already_exist_c('视频界面_涂鸦'), True)
                self.assertEqual(call.is_element_already_exist_c('视频界面_切换摄像头'), True)
                self.assertEqual(call.is_element_already_exist_c('视频界面_挂断'), True)
                self.assertEqual(call.is_element_already_exist_c('视频界面_小屏'), True)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_挂断')

    # @tags('ALL', 'CMCC_double', 'call')
    # def test_call_000105(self):
    #     """
    #         1、4G网络
    #         2、已登录客户端
    #         3、当前页面在视频通话接听页面
    #         4、点击非icon区域
    #         5、再点击非icon区域
    #         6、隐藏界面其它，只显示两个视频窗口
    #     """
    #     call = CallPage()
    #     call.wait_for_page_load()
    #     # 初始化被叫手机
    #     Preconditions.initialize_class('Android-移动-N')
    #     # 获取手机号码
    #     cards = call.get_cards_c(CardType.CHINA_MOBILE)
    #     # 切换主叫手机
    #     Preconditions.select_mobile('Android-移动')
    #     # 拨打视频电话
    #     call.pick_up_p2p_video(cards)
    #     # 等待返回结果
    #     self.assertEqual(self.to_pick_phone_video(), True)
    #     self.assertEqual(self.check_video_call_000105(), True)
    #
    # @TestLogger.log('验证结果')
    # def check_video_call_000105(self):
    #     """
    #         1、点击非icon区域
    #         2、再点击非icon区域
    #         3、隐藏界面其它，只显示两个视频窗口
    #     """
    #     call = CallPage()
    #     try:
    #         if call.is_element_already_exist_c('视频界面_时长'):
    #             call.tap_screen_center_c('视频界面_小屏')
    #             time.sleep(1)
    #             self.assertEqual(call.is_element_already_exist_c('视频界面_免提'), False)
    #             self.assertEqual(call.is_element_already_exist_c('视频界面_静音'), False)
    #             self.assertEqual(call.is_element_already_exist_c('视频界面_转为语音 '), False)
    #             self.assertEqual(call.is_element_already_exist_c('视频界面_涂鸦'), False)
    #             self.assertEqual(call.is_element_already_exist_c('视频界面_切换摄像头'), False)
    #             self.assertEqual(call.is_element_already_exist_c('视频界面_挂断'), False)
    #             self.assertEqual(call.is_element_already_exist_c('视频界面_小屏'), True)
    #         else:
    #             call.tap_screen_center_c('视频界面_小屏')
    #             time.sleep(0.5)
    #             self.assertEqual(call.is_element_already_exist_c('视频界面_免提'), True)
    #             self.assertEqual(call.is_element_already_exist_c('视频界面_静音'), True)
    #             self.assertEqual(call.is_element_already_exist_c('视频界面_转为语音 '), True)
    #             self.assertEqual(call.is_element_already_exist_c('视频界面_涂鸦'), True)
    #             self.assertEqual(call.is_element_already_exist_c('视频界面_切换摄像头'), True)
    #             self.assertEqual(call.is_element_already_exist_c('视频界面_挂断'), True)
    #             self.assertEqual(call.is_element_already_exist_c('视频界面_小屏'), True)
    #         return True
    #     except Exception:
    #         traceback.print_exc()
    #         return False
    #     finally:
    #         call.tap_screen_three_point_element_c('视频界面_时长')
    #         call.click_locator_key_c('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000106(self):
        """
            1.当前正在视频通话页面
            2.涂鸦功能列表未展开"
            3.对方点击视频涂鸦返回按钮
            4.视频接通后等待5S后，查看页面显示
            5.隐藏界面其它，只显示两个视频窗口
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_000106(), True)

    @TestLogger.log('验证结果')
    def check_video_call_000106(self):
        """
            1.视频接通后等待5S后，查看页面显示
            2.隐藏界面其它，只显示两个视频窗口
        """
        call = CallPage()
        try:
            call.click_locator_key_c('视频界面_免提')
            time.sleep(5)
            self.assertEqual(call.is_element_already_exist_c('视频界面_免提'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_静音'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_转为语音 '), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_涂鸦'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_切换摄像头'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_挂断'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_小屏'), True)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000107(self):
        """
            1.当前正在视频通话页面
            2.涂鸦功能列表未展开"
            3.对方点击视频涂鸦返回按钮
            4.视频接通后等待5S后，查看页面显示
            5.隐藏界面其它，只显示两个视频窗口
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_video_call_000107(), True)

    @TestLogger.log('验证结果')
    def check_video_call_000107(self):
        """
            1.视频接通后等待5S后，查看页面显示
            2.隐藏界面其它，只显示两个视频窗口
        """
        call = CallPage()
        try:
            call.click_locator_key_c('视频界面_免提')
            time.sleep(6)
            call.tap_screen_center_c('视频界面_主元素')
            time.sleep(10)
            self.assertEqual(call.is_element_already_exist_c('视频界面_免提'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_静音'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_转为语音 '), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_涂鸦'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_切换摄像头'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_挂断'), False)
            self.assertEqual(call.is_element_already_exist_c('视频界面_小屏'), True)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000114(self):
        """
            1、正常登录密友圈
            2、呼出一个点对点视频通话
            3、呼出一个多方视频通话
            4、接听一个视频通话
            5、拒接一个多方视频通话
            6、为主叫方呼出一个电话
            7、查看生成的通话记录显示
            8、生成一个呼出的通话记录，记录中显示通话类型为：视频通话
            9、生成一个呼出的通话记录，记录中显示通话类型为：多方视频
            10、生成一个呼入的通话记录，记录中显示通话类型为：视频通话
            11、生成一个呼入的通话记录，记录中显示通话类型为：多方视频
            12、生成一个呼出的通话记录，记录中显示通话类型为：多方电话
        """
        call = CallPage()
        call.wait_for_page_load()
        call.clear_all_record()
        time.sleep(0.5)
        # 呼出一个点对点视频通话
        call.make_sure_p2p_video_no_college()
        if call.is_element_already_exist_c('无密友圈_提示文本'):
            call.click_locator_key_c('无密友圈_取消')
            time.sleep(1)
        call.wait_for_page_call_load()
        time.sleep(1)
        if call.is_element_already_exist_c('视频通话'):
            time.sleep(0.5)
            call.click_tag_detail_first_element('视频通话')
            time.sleep(0.5)
            self.assertEqual('呼出' == call.get_elements_list('详情_通话类型')[0].text, True)
            call.click_detail_back()
            time.sleep(1)
        call.clear_all_record()
        time.sleep(0.5)
        # 呼出一个多方视频通话
        call.multiplayer_vedio_call()
        call.wait_for_page_call_load()
        time.sleep(1)
        if call.is_element_already_exist_c('多方视频'):
            call.click_tag_detail_first_element('多方视频')
            time.sleep(0.5)
            self.assertEqual('呼出' == call.get_elements_list('详情_通话类型')[0].text, True)
            call.click_detail_back()
            time.sleep(1)
        call.clear_all_record()
        time.sleep(0.5)
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        call.clear_all_record()
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        call.click_locator_key_c('视频界面_免提')
        time.sleep(2)
        call.tap_screen_three_point_element_c('视频界面_时长')
        time.sleep(0.5)
        call.click_locator_key_c('视频界面_挂断')
        time.sleep(3)
        if call.is_element_already_exist_c('视频通话'):
            call.click_tag_detail_first_element('视频通话')
            time.sleep(0.5)
            self.assertEqual('呼入' == call.get_elements_list('详情_通话类型')[0].text, True)
            call.click_detail_back()
            time.sleep(1)
        call.clear_all_record()
        # 切换到被叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 切换到被叫手机
        Preconditions.select_mobile('Android-移动-N')
        call.click_locator_key_c('视频通话_挂断')
        time.sleep(3)
        if call.is_element_already_exist_c('视频通话'):
            call.click_tag_detail_first_element('视频通话')
            time.sleep(0.5)
            self.assertEqual('未接' == call.get_elements_list('详情_通话类型')[0].text, True)
            call.click_detail_back()
            time.sleep(1)
        call.clear_all_record()
        call.make_sure_have_multi_voice_record()
        time.sleep(1)
        if call.is_element_already_exist_c('多方电话'):
            call.click_tag_detail_first_element('多方电话')
            time.sleep(0.5)
            self.assertEqual('呼出' == call.get_elements_list('详情_通话类型')[0].text, True)
            call.click_locator_key_c('多方电话_返回')
            time.sleep(1)

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000134(self):
        """
            1.验证双方都为移动用户的多方电话流程
            2.网络正常
            3.主/被号都为移动号码
            4.剩余时长足够
            5.点击拨打电话
            6.呼叫回呼电话
        """
        call = CallPage()
        try:
            call.wait_for_page_load()
            # 初始化被叫手机
            Preconditions.initialize_class('Android-移动-N')
            # 获取手机号码
            cards = call.get_cards_c(CardType.CHINA_MOBILE)
            # 切换主叫手机
            Preconditions.select_mobile('Android-移动')
            # 拨打电话
            call.click_show_keyboard()
            time.sleep(0.5)
            call.input_text_c('键盘输入框', cards)
            call.click_locator_key('拨号界面_呼叫')
            if call.is_element_already_exist_c('回呼_提示文本'):
                call.set_checkbox_checked_c('回呼_不再提醒')
                call.click_locator_key_c('回呼_我知道了')
            time.sleep(10)
            self.assertEqual(call.is_text_present_c('飞信电话') and call.is_text_present_c('12560'), True)
            call.hang_up_the_call()
        except Exception:
            traceback.print_exc()
            time.sleep(70)

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000139(self):
        """
            1. 验证剩余时长更新 网络正常
            2.已使用多方电话通话并减少剩余时长"	"1.点击免费电话icon
            2.查看剩余时长100分钟
            3.拨打多方电话10分钟后返回列表页面
            4.查看剩余时长"	"1.进入多方电话列表页面
            2.剩余时长显示100分钟
            3.多方电话成功通话并成功返回
            4.剩余时长显示为90分钟"

        """
        call = CallPage()
        call.wait_for_page_load()
        time1 = Preconditions.get_remaining_call_time()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打多方电话
        call.pick_up_multi_voice(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_voice(), True)
        Preconditions.select_mobile('Android-移动')
        n = 1
        time.sleep(n * 60)
        call.hang_up_the_call()
        time2 = Preconditions.get_remaining_call_time()
        self.assertEqual((time1 - time2 >= n), True)

    # @tags('ALL', 'CMCC_double', 'call')
    # def test_call_000148(self):
    #     """
    #         1. 验证剩余时长更新 网络正常
    #         2.已使用多方电话通话并减少剩余时长"	"1.点击免费电话icon
    #         2.查看剩余时长100分钟
    #         3.拨打多方电话10分钟后返回列表页面
    #         4.查看剩余时长"	"1.进入多方电话列表页面
    #         2.剩余时长显示100分钟
    #         3.多方电话成功通话并成功返回
    #         4.剩余时长显示为90分钟"
    #
    #     """
    #     call = CallPage()
    #     call.wait_for_page_load()
    #     # 初始化被叫手机
    #     Preconditions.initialize_class('Android-移动-N')
    #     # 获取手机号码
    #     cards = call.get_cards_c(CardType.CHINA_MOBILE)
    #     # 切换主叫手机
    #     Preconditions.select_mobile('Android-移动')
    #     # 拨打多方电话
    #     call.pick_up_multi_voice(cards)
    #     time.sleep(8)
    #     current_mobile().press_home_key()
    #     time.sleep(3)
    #     current_mobile().launch_app()
    #     time.sleep(1)
    #     self.assertEqual(call.is_text_present_c('飞信电话') \
    #                      and call.is_text_present_c('12560'), True)

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000174(self):
        """
            1、正常网络状态下，登录密友圈；
            2、当前页面在通话页面
            3、拨号盘已打开
            4、输入框显示123456
            5、点击清除键一下
            6、输入框显示12345
            7、长按清除键
            8、清除全部输入内容，输入框显示默认字体“直接拨号或拼音搜索”"
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        # 按首字母搜索
        call.input_text_c('键盘输入框', cards)
        self.assertEqual(call.get_elements_count_c('拨号界面_不限时长') > 0, True)

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000183(self):
        """
            拨号盘搜素源新增不限时长成员	"1、正常网络状态下，登录密友圈；
            2、当前页面在拨号盘打开状态"	输入框输入不限时长成员号码或数字匹配
            （去重家庭网、联系人、本地通讯录，补充不限时长成员）优先显示不限时长成员，
            右边有详情页图标,详情页面没有删除按钮
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        # 按首字母搜索
        call.input_text_c('键盘输入框', cards)
        time.sleep(1)
        self.assertEqual(call.is_element_already_exist_c('拨号界面_详情'), True)
        call.get_some_elements_c('拨号界面_详情')[0].clicl()
        time.sleep(1)
        self.assertEqual(call.is_text_present_c('删除'), False)

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000185(self):
        """
            选择1人发起视频通话
            1、网络正常，已登录密友圈；
            2、当前在多方视频-联系人选择器页面；"	选择1名成员，点击“呼叫”按钮	发起单对单视频通话，逻辑与现网保持一致一致
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_p2p_video(cards)
        # 等待结果
        self.assertEqual(call.is_text_present_c('正在等待对方接听', default_timeout=30), True)
        call.click_locator_key_c('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000187(self):
        """
            1、网络正常，已登录密友圈，权限已开启；
            2、当前在多方视频-联系人选择器页面；
            1、选择2名以上联系人，点击“呼叫”按钮；
            进入视频通话窗口，所有成员以小格子画面显示，
            被叫方显示对方设置头像/默认头像，
            头像上浮层显示呼叫中标识“转圈”，
            窗口下方有“免提、静音、关闭摄像头、转换摄像头、挂断”按钮；
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 拨打多人视频 指定一个号码
        call.pick_up_multi_video(cards)
        count = 60
        while count > 0:
            ret = self.check_result_000187(call)
            if ret:
                break
            time.sleep(0.5)
            count -= 1
            print("ret : %s ---> count : %s" % (ret, count))
        else:
            raise RuntimeError('---->False')
        time.sleep(1)
        if call.is_element_already_exist_c('挂断_多方通话'):
            call.is_element_already_exist_c('挂断_多方通话')
            if call.is_element_already_exist_c('挂断_多方通话_确定'):
                call.is_element_already_exist_c('挂断_多方通话_确定')

    @TestLogger.log('校验结果')
    def check_result_000187(self, call):
        """校验结果"""
        return call.is_element_already_exist_c('多方视频_头像', default_timeout=0.5) \
               and call.is_element_already_exist_c('多方视频_呼叫中', default_timeout=0.5) \
               and call.is_element_already_exist_c('多方视频_转换摄像头', default_timeout=0.5) \
               and call.is_element_already_exist_c('多方视频_关闭摄像头', default_timeout=0.5) \
               and call.is_element_already_exist_c('多方视频_免提', default_timeout=0.5) \
               and call.is_element_already_exist_c('多方视频_静音', default_timeout=0.5) \
               and call.is_element_already_exist_c('多方视频_挂断', default_timeout=0.5)

    # @tags('ALL', 'CMCC_double', 'call')
    @unittest.skip('浮窗抓取不到')
    def test_call_000198(self):
        """
            收起和展开视频通话
            1、网络正常，已登录密友圈，权限已开启；
            2、多方视频已接通；
            1、A点击左上角的【收起】按钮；
            2、查看B的视频窗口；
            3、A单击通话浮层；
            1、视频窗口缩小以浮层的方式悬浮在页面的右上角，可按住移动浮层位置；
            窗口收起后，默认停留在发起视频通话页面，切换到任一页面，浮层位置保持不变；
            2、收起视频通话不影响其他视频成员端的视频窗口展示；
            3、A用户返回视频通话窗口；
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打多人视频 指定一个号码
        call.pick_up_multi_video(cards)
        # 等待结果
        self.assertEqual(self.to_pick_phone_video(), True)
        self.assertEqual(self.check_result_000198(), True)

    @TestLogger.log('验证结果')
    def check_result_000198(self):
        """
            收起和展开视频通话
            1、网络正常，已登录密友圈，权限已开启；
            2、多方视频已接通；
            1、A点击左上角的【收起】按钮；
            2、查看B的视频窗口；
            3、A单击通话浮层；
            1、视频窗口缩小以浮层的方式悬浮在页面的右上角，可按住移动浮层位置；
            窗口收起后，默认停留在发起视频通话页面，切换到任一页面，浮层位置保持不变；
            2、收起视频通话不影响其他视频成员端的视频窗口展示；
            3、A用户返回视频通话窗口；
        """
        call = CallPage()
        try:
            call.click_locator_key_c('多方视频_免提')
            # 切换主叫手机
            Preconditions.select_mobile('Android-移动')
            call.click_locator_key_c('多方视频_免提')
            call.click_locator_key_c('多方视频_收起')
            # 切换被叫手机
            Preconditions.select_mobile('Android-移动-N')
            self.assertEqual(call.is_element_already_exist_c('多方视频_收起'), True)
            # 切换主叫手机
            Preconditions.select_mobile('Android-移动')
            call.press_and_move_to_down_c('')
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            call.tap_screen_three_point_element_c('视频界面_时长')
            call.click_locator_key_c('视频界面_挂断')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000205(self):
        """
            视频通话接通页面（免提功能）	"1、网络正常，已登录客户端
            2、麦克风和相机权限已开启
            3、当前在视频通话页面（默认免提打开）"	"1、点击“免提”按钮，被叫方发出声响；
            2、再次点击“免提”按钮，被叫方发出声响；"	"视频通话接通时默认免提功能开启，免提按钮高亮显示，被叫方的声音通过扩音处播放；
            1、点击已高亮的免提按钮，关闭免提功能，按钮由亮变暗，声音从手机顶部耳机位播放；
            2、再次点击已变暗的免提按钮，打开免提功能，按钮高亮显示，声音通过扩音处播放
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_multi_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_multi_video(), True)
        self.assertEqual(self.check_video_call_000205(), True)

    @TestLogger.log('验证结果')
    def check_video_call_000205(self):
        """
             视频通话接通页面（免提功能）	"1、网络正常，已登录客户端
            2、麦克风和相机权限已开启
            3、当前在视频通话页面（默认免提打开）"	"1、点击“免提”按钮，被叫方发出声响；
            2、再次点击“免提”按钮，被叫方发出声响；"	"视频通话接通时默认免提功能开启，免提按钮高亮显示，被叫方的声音通过扩音处播放；
            1、点击已高亮的免提按钮，关闭免提功能，按钮由亮变暗，声音从手机顶部耳机位播放；
            2、再次点击已变暗的免提按钮，打开免提功能，按钮高亮显示，声音通过扩音处播放
        """
        call = CallPage()
        try:
            self.assertEqual('true' == call.get_select_value_c('多方视频_免提'), True)
            call.click_locator_key_c('多方视频_免提')
            time.sleep(1)
            self.assertEqual('false' == call.get_select_value_c('多方视频_免提'), True)
            call.click_locator_key_c('多方视频_免提')
            time.sleep(0.5)
            self.assertEqual('true' == call.get_select_value_c('多方视频_免提'), True)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            if call.is_element_already_exist_c('多方视频_挂断'):
                call.click_locator_key_c('多方视频_挂断')
                if call.is_text_present_c('是否关闭此次多方视频'):
                    call.click_locator_key_c('确定')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000206(self):
        """
              视频通话接通页面（静音功能）	"1、网络正常，已登录客户端
            2、麦克风和相机权限已开启
            3、当前在视频通话页面（默认静音关闭）"	"1、点击“静音”按钮，我方发出声响；
            2、再次点击“静音”按钮，我方发出声响；"	"视频通话接通时默认静音功能关闭，其他成员可听到我方的声音；
            1、点击已静音按钮，开启静音功能，静音按钮高亮显示，我方声音其他成员无法听到；
            2、再次点击已高亮的静音按钮，关闭静音功能，其他成员可再次听到我方的声音；"
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_multi_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_multi_video(), True)
        self.assertEqual(self.check_video_call_000206(), True)

    @TestLogger.log('验证结果')
    def check_video_call_000206(self):
        """
             视频通话接通页面（静音功能）	"1、网络正常，已登录客户端
            2、麦克风和相机权限已开启
            3、当前在视频通话页面（默认静音关闭）"	"1、点击“静音”按钮，我方发出声响；
            2、再次点击“静音”按钮，我方发出声响；"	"视频通话接通时默认静音功能关闭，其他成员可听到我方的声音；
            1、点击已静音按钮，开启静音功能，静音按钮高亮显示，我方声音其他成员无法听到；
            2、再次点击已高亮的静音按钮，关闭静音功能，其他成员可再次听到我方的声音；"
        """
        call = CallPage()
        try:
            self.assertEqual('false' == call.get_select_value_c('多方视频_静音'), True)
            call.click_locator_key_c('多方视频_静音')
            time.sleep(1)
            self.assertEqual('true' == call.get_select_value_c('多方视频_静音'), True)
            call.click_locator_key_c('多方视频_静音')
            time.sleep(0.5)
            self.assertEqual('false' == call.get_select_value_c('多方视频_静音'), True)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            if call.is_element_already_exist_c('多方视频_挂断'):
                call.click_locator_key_c('多方视频_挂断')
                if call.is_text_present_c('是否关闭此次多方视频'):
                    call.click_locator_key_c('确定')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000207(self):
        """
             视频通话接通页面（摄像头开关功能）	"1、网络正常，已登录客户端
            2、麦克风和相机权限已开启
            3、当前在视频通话页面"	"1、点击“关闭摄像头”按钮；
            2、再次点击“打开摄像头”按钮；"	"相机权限开启后，视频通话接通时摄像头按钮高亮显示，下方文字为“关闭摄像头”，其他成员看到我的画面；
            1、点击“关闭摄像头”，按钮由亮变暗，下方文字变为“打开摄像头”，我方及被叫方均看到我的镜头画面消失，显示为我的头像；
            2、再次点击“打开摄像头”，打开摄像头，所有成员均看到我的镜头画面；"
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_multi_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_multi_video(), True)
        self.assertEqual(self.check_video_call_000207(), True)

    @TestLogger.log('验证结果')
    def check_video_call_000207(self):
        """
            视频通话接通页面（摄像头开关功能）	"1、网络正常，已登录客户端
            2、麦克风和相机权限已开启
            3、当前在视频通话页面"	"1、点击“关闭摄像头”按钮；
            2、再次点击“打开摄像头”按钮；"	"相机权限开启后，视频通话接通时摄像头按钮高亮显示，下方文字为“关闭摄像头”，其他成员看到我的画面；
            1、点击“关闭摄像头”，按钮由亮变暗，下方文字变为“打开摄像头”，我方及被叫方均看到我的镜头画面消失，显示为我的头像；
            2、再次点击“打开摄像头”，打开摄像头，所有成员均看到我的镜头画面；"
        """
        call = CallPage()
        try:
            self.assertEqual('false' == call.get_select_value_c('多方视频_关闭摄像头'), True)
            self.assertEqual('关闭摄像头' == call.get_element_text_c('多方视频_关闭摄像头_文本'), True)
            call.click_locator_key_c('多方视频_关闭摄像头')
            time.sleep(1)
            self.assertEqual('true' == call.get_select_value_c('多方视频_关闭摄像头'), True)
            self.assertEqual('打开摄像头' == call.get_element_text_c('多方视频_关闭摄像头_文本'), True)
            call.click_locator_key_c('多方视频_关闭摄像头')
            time.sleep(0.5)
            self.assertEqual('false' == call.get_select_value_c('多方视频_关闭摄像头'), True)
            self.assertEqual('关闭摄像头' == call.get_element_text_c('多方视频_关闭摄像头_文本'), True)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            if call.is_element_already_exist_c('多方视频_挂断'):
                call.click_locator_key_c('多方视频_挂断')
                if call.is_text_present_c('是否关闭此次多方视频'):
                    call.click_locator_key_c('确定')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000208(self):
        """
            视频通话接通页面（摄像头转换功能）	"1、网络正常，已登录客户端
            2、麦克风和相机权限已开启
            3、当前在视频通话页面（摄像头已开启）"	"1、点击“切换摄像头”按钮；
            2、再次点击“切换摄像头”按钮；"	"视频通话时，摄像头开启中才有“切换摄像头”的功能可用，默认使用前置摄像头画面；
            1、点击“切换摄像头”，操作者画面切换到后置摄像头画面；
            2、再次点击“切换摄像头”，操作者画面再次切换到前置摄像头画面；"
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_multi_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_multi_video(), True)
        self.assertEqual(self.check_video_call_000208(), True)

    @TestLogger.log('验证结果')
    def check_video_call_000208(self):
        """
           视频通话接通页面（摄像头转换功能）	"1、网络正常，已登录客户端
            2、麦克风和相机权限已开启
            3、当前在视频通话页面（摄像头已开启）"	"1、点击“切换摄像头”按钮；
            2、再次点击“切换摄像头”按钮；"	"视频通话时，摄像头开启中才有“切换摄像头”的功能可用，默认使用前置摄像头画面；
            1、点击“切换摄像头”，操作者画面切换到后置摄像头画面；
            2、再次点击“切换摄像头”，操作者画面再次切换到前置摄像头画面；"
        """
        call = CallPage()
        try:
            self.assertEqual('false' == call.get_select_value_c('多方视频_转换摄像头'), True)
            time.sleep(0.5)
            call.click_locator_key_c('多方视频_转换摄像头')
            time.sleep(1)
            self.assertEqual('false' == call.get_select_value_c('多方视频_转换摄像头'), True)
            call.click_locator_key_c('多方视频_关闭摄像头')
            time.sleep(1)
            call.click_locator_key_c('多方视频_转换摄像头')
            self.assertEqual(call.is_toast_exist('请打开摄像头后尝试'), True)
            return True
        except Exception:
            traceback.print_exc()
            return False
        finally:
            if call.is_element_already_exist_c('多方视频_挂断'):
                call.click_locator_key_c('多方视频_挂断')
                if call.is_text_present_c('是否关闭此次多方视频'):
                    call.click_locator_key_c('确定')

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000253(self):
        """
            通话记录显示	1、正常登录密友圈
            1、呼出一个点对点视频通话
            2、呼出一个多方视频通话
            3、接听一个视频通话
            4、拒接一个多方视频通话
            5、为主叫方呼出一个电话
            6、查看生成的通话记录显示"	"1、生成一个呼出的通话记录，记录中显示通话类型为：视频通话
            2、生成一个呼出的通话记录，记录中显示通话类型为：多方视频
            3、生成一个呼入的通话记录，记录中显示通话类型为：视频通话
            4、生成一个呼入的通话记录，记录中显示通话类型为：多方视频
            5、生成一个呼出的通话记录，记录中显示通话类型为：飞信电话"
        """
        # 拒接多方视频后没有生成通话记录
        call = CallPage()
        call.wait_for_page_load()
        call.clear_all_record()
        time.sleep(0.5)
        # 呼出一个点对点视频通话
        call.make_sure_p2p_video_no_college()
        if call.is_element_already_exist_c('无密友圈_提示文本'):
            call.click_locator_key_c('无密友圈_取消')
            time.sleep(1)
        call.wait_for_page_call_load()
        time.sleep(1)
        print('--->检查点1<====================')
        self.assertEqual(call.is_text_present_c('视频通话'), True)
        call.clear_all_record()
        time.sleep(0.5)
        # 呼出一个多方视频通话
        call.multiplayer_vedio_call()
        call.wait_for_page_call_load()
        time.sleep(1)
        print('--->检查点2<====================')
        self.assertEqual(call.is_text_present_c('多方视频'), True)
        # 接听一个视频通话
        time.sleep(0.5)
        call.clear_all_record()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        call.clear_all_record()
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打点对点视频电话
        call.pick_up_p2p_video(cards)
        # 等待返回结果
        self.assertEqual(self.to_pick_phone_video(), True)
        call.click_locator_key_c('视频界面_免提')
        time.sleep(2)
        call.tap_screen_three_point_element_c('视频界面_时长')
        time.sleep(0.5)
        call.click_locator_key_c('视频界面_挂断')
        time.sleep(3)
        print('--->检查点3<====================')
        self.assertEqual(call.is_text_present_c('视频通话'), True)
        # 拒接一个多方视频
        time.sleep(1)
        call.clear_all_record()
        # 切换到主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话
        call.pick_up_multi_video(cards)
        # 切换到被叫手机
        Preconditions.select_mobile('Android-移动-N')
        call.click_locator_key_c('视频通话_挂断')
        time.sleep(3)
        print('--->检查点4<====================')
        self.assertEqual(call.is_text_present_c('多方视频'), False)
        # 切换到主叫手机
        Preconditions.select_mobile('Android-移动')
        if call.is_element_already_exist_c('多方视频_挂断'):
            call.click_locator_key_c('多方视频_挂断')
        if call.is_element_already_exist('多方电话_返回'):
            call.click_locator_key('多方电话_返回')
        # 呼出一个多方电话
        call.clear_all_record()
        call.make_sure_have_multi_voice_record()
        time.sleep(1)
        print('--->检查点5<====================')
        self.assertEqual(call.is_text_present_c('多方电话'), True)

    @tags('ALL', 'CMCC_double', 'call')
    def test_call_000272(self):
        """
           首次拨打回呼电话弹框提示	"1、网络正常
            2、正常登录
            3、首次点击回呼电话
            4、当前在福利电话页面
            5、已弹出拨打电话的选择栏"	"1、点击拨打电话
            2、点击我知道了按钮"	"1、弹出上部是过渡页中部文案“请注意接听“密友圈电话”来电，系统将自动呼叫对方。”我知道了按钮
            2、跳转至回呼过渡页面"
        """
        call = CallPage()
        call.wait_for_page_load()
        # 初始化被叫手机
        Preconditions.initialize_class('Android-移动-N')
        # 获取手机号码
        cards = call.get_cards_c(CardType.CHINA_MOBILE)
        # 切换主叫手机
        Preconditions.select_mobile('Android-移动')
        # 拨打视频电话 # 请先接听来电，随后将自动呼叫对方
        call.click_show_keyboard()
        call.input_text_c('键盘输入框', cards)
        call.click_locator_key_c('拨号界面_呼叫')
        flag = False
        try:
            for i in range(10):
                if call.is_element_already_exist_c('回呼_提示文本', default_timeout=0.1):
                    call.click_locator_key_c('回呼_我知道了')
                flag = call.is_text_present_c('随后将自动呼叫对方', default_timeout=0.1)
                if flag:
                    break
            self.assertEqual(flag, True)
            time.sleep(5)
            self.assertEqual(call.is_text_present_c('飞信电话', default_timeout=0.5)
                             and call.is_text_present_c('12560', default_timeout=0.5), True)
        finally:
            call.hang_up_the_call()
