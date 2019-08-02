import time
import warnings
import traceback

from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.TestLogger import TestLogger
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from library.core.TestCase import TestCase

from pages.guide import GuidePage
from pages.login.LoginPage import OneKeyLoginPage
from pages.call.CallPage import CallPage


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
    def disconnect_mobile(category):
        """断开手机连接"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.disconnect_mobile()
        return client


# noinspection PyBroadException
class CallPageTest(TestCase):
    """Call 模块--全量"""

    @TestLogger.log('执行SetUp')
    def default_setUp(self):
        """确保每个用例开始之前在通话界面界面"""
        warnings.simplefilter('ignore')
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_call_page()

    @TestLogger.log('执行TearDown')
    def default_tearDown(self):
        call = CallPage()
        if call.get_network_status() != 6:
            call.set_network_status(6)
        time.sleep(2)
        Preconditions.disconnect_mobile('Android-移动')

    @TestLogger.log('修改并验证备注是否修改成功')
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
        time.sleep(2.5)
        if not call.on_this_page_call_detail():
            return False
        time.sleep(0.5)
        if name != call.get_nickname():
            return False
        return True

    # 注：是从0002开始的，没有0001

    @tags('ALL', 'CMCC', 'call')
    def test_call_0002(self):
        """通话界面显示"""
        time.sleep(2)
        call = CallPage()
        call.page_contain_element('通话文案')
        call.page_contain_element('拨号键盘')
        if call.is_element_already_exist('来电名称'):
            call.page_contain_element('来电名称')
        else:
            call.page_should_contain_text('打电话不花钱')

    @tags('ALL', 'CMCC', 'call')
    def test_call_0003(self):
        """通话界面-拨号键盘显示"""
        time.sleep(2)
        call = CallPage()
        call.page_contain_element('拨号键盘')
        if call.is_element_already_exist('来电名称'):
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
        if call.is_element_already_exist('视频通话') and call.is_element_already_exist('多方电话'):
            time.sleep(1)
            call.click_locator_key('视频通话')
            time.sleep(1)
            call.is_text_present('发起视频通话')

    @tags('ALL', 'CMCC', 'call')
    def test_call_0006(self):
        """展开拨号盘，不可以左右滑动切换tab，上方内容显示通话模块通话记录内容"""
        time.sleep(2)
        call = CallPage()
        call.wait_for_page_load()
        if call.is_on_this_page():
            call.click_show_keyboard()
        time.sleep(1)
        # 向左滑动
        call.page_left()
        # 判断滑动后是否还在此页面
        self.assertEqual(call.is_exist_call_key(), True)
        # 向右滑动
        call.page_right()
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
        call.make_sure_p2p_voice_no_college()
        call.is_text_present_c('飞信电话', default_timeout=15)
        try:
            call.hang_up_the_call()
        except Exception:
            pass
        self.assertEqual(call.is_text_present_c('飞信电话', default_timeout=15), True)
        time.sleep(0.5)
        call.click_tag_detail_first_element('飞信电话')
        time.sleep(2)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 单击左上角返回按钮
        time.sleep(0.5)
        call.click_detail_back()
        call.wait_for_page_load()
        time.sleep(0.5)
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
        call.make_sure_p2p_voice_no_college()
        call.is_text_present_c('飞信电话', default_timeout=15)
        try:
            call.hang_up_the_call()
        except Exception:
            pass
        self.assertEqual(call.is_text_present_c('飞信电话', default_timeout=15), True)
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
        time.sleep(0.5)
        call.make_sure_have_p2p_vedio_record()
        call.click_tag_detail_first_element('视频通话')
        time.sleep(2)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 1. 修改为中文
        name = 'select now()'
        self.assertEqual(self.check_modify_nickname(name), True)
        name = '大佬1'
        self.check_modify_nickname(name)

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
        name = '大佬1'
        self.check_modify_nickname(name)

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
        call.make_sure_p2p_video_no_college()
        call.click_locator_key('无密友圈_取消')
        time.sleep(3)
        call.click_tag_detail_first_element('视频通话')
        time.sleep(2)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 1. 点击视频通话按钮
        time.sleep(0.5)
        call.click_locator_key('详情_视频')
        time.sleep(1)
        if call.on_this_page_flow():
            call.set_not_reminders()
            time.sleep(1)
            call.click_locator_key('流量_继续拨打')
            time.sleep(1)
        if call.on_this_page_common('无密友圈_提示文本'):
            call.click_locator_key('无密友圈_取消')
            time.sleep(0.5)
        time.sleep(3)
        self.assertEqual(call.on_this_page_call_detail(), True)
        time.sleep(0.5)

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
        call.make_sure_p2p_video_no_college()
        call.click_locator_key('无密友圈_取消')
        time.sleep(3)
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
        time.sleep(1)
        if call.on_this_page_common('无密友圈_提示文本'):
            call.click_locator_key('无密友圈_确定')
        time.sleep(3)
        self.assertEqual('com.android.mms' == Preconditions.get_current_activity_name(), True)
        time.sleep(2)
        if call.is_element_already_exist_c('短信发送返回'):
            call.click_locator_key_c('短信发送返回')
            time.sleep(1)

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
        time.sleep(0.5)
        call.make_sure_p2p_video_no_college()
        call.click_locator_key('无密友圈_取消')
        time.sleep(3)
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
        call.click_locator_key('详情_通话')
        time.sleep(1)
        if call.on_this_page_flow():
            # call.set_not_reminders()
            time.sleep(1)
            call.click_locator_key('回呼_我知道了')
        time.sleep(1)
        n = 20
        flag = False
        while n > 0:
            if (call.is_text_present_c('飞信电话', default_timeout=0.1)
                    and call.is_text_present_c('12560', default_timeout=0.1)):
                flag = True
                break
            n -= 1
        try:
            self.assertEqual(flag, True)
        finally:
            try:
                call.hang_up_the_call()
            except Exception:
                pass

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
        call.make_sure_p2p_voice_no_college()
        # call.is_text_present_c('飞信电话', default_timeout=15)
        try:
            call.hang_up_the_call()
        except Exception:
            pass
        self.assertEqual(call.is_text_present_c('飞信电话', default_timeout=15), True)
        call.click_tag_detail_first_element('飞信电话')
        time.sleep(1)
        self.assertEqual(call.on_this_page_call_detail(), True)
        # 1. 修改为中文
        name = '修改后的备注'
        self.assertEqual(self.check_modify_nickname(name), True)
        # call.click_locator_key('详情_视频')
        # time.sleep(1)
        # if call.is_element_already_exist('流量_不再提醒'):
        #     call.set_not_reminders()
        #     call.click_locator_key('流量_继续拨打')
        #     time.sleep(2)
        comment = call.get_element_text('视频_备注')
        self.assertEqual(name == comment, True)
        # name = '大佬1'
        # self.check_modify_nickname(name)

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
        call.make_sure_p2p_voice_no_college()
        call.is_text_present_c('飞信电话', default_timeout=15)
        try:
            call.hang_up_the_call()
        except Exception:
            pass
        self.assertEqual(call.is_text_present_c('飞信电话', default_timeout=15), True)
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
        time.sleep(2)
        if call.is_element_already_exist_c('短信发送返回'):
            call.click_locator_key_c('短信发送返回')
            time.sleep(1)

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
        # call.click_locator_key('多方电话_返回')
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
        call.clear_all_record()
        call.wait_for_page_call_load()
        # 判断是否有通话标签、‘+’、打电话不花钱
        self.assertEqual(call.is_text_present('通话'), True)
        self.assertEqual(call.on_this_page_common('加号'), True)
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
        call.click_locator_key('加号')
        time.sleep(0.5)
        call.click_locator_key('视频通话')
        time.sleep(0.5)
        self.assertEqual(call.is_text_present('发起视频通话'), True)
        self.assertEqual(call.on_this_page_common('多方电话_返回'), True)
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
        call.click_locator_key('加号')
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
        call.click_locator_key('加号')
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
        call.click_locator_key('加号')
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
        call.click_locator_key('加号')
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
        call.click_locator_key('加号')
        time.sleep(0.5)
        call.click_locator_key('视频通话')
        time.sleep(1)
        call.wait_page_load_common('发起视频通话')
        time.sleep(1)
        if not call.select_contact_more(9, '最多只能选择8人'):
            raise RuntimeError('最多只能选择8人')

        self.assertEqual(call.is_toast_exist('最多只能选择8人', timeout=8), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000109(self):
        """
            1、正常登录密友圈
            2、通话界面中有通话记录
            3、查看通话界面中的通话记录
            4、通话记录中记录电话的优惠电话、视频的视频通话与多方视频记录
            5、（无优惠电话，只判断‘飞信电话’‘多方电话’‘多方视频’‘视频通话’）
        """
        call = CallPage()
        call.wait_for_page_load()
        # 确保有视频通话
        if not call.is_text_present_c('视频通话'):
            call.make_sure_p2p_video_no_college()
            time.sleep(1)
            if call.is_element_already_exist_c('流量_不再提醒'):
                call.click_locator_key_c('流量_不再提醒')
                call.click_locator_key_c('流量_继续拨打')
            if call.is_element_already_exist_c('无密友圈_提示文本'):
                call.click_locator_key_c('无密友圈_取消')
        call.wait_for_page_c('通话', max_wait_time=60)
        time.sleep(2)
        self.assertEqual(call.is_text_present_c('[视频通话]'), True)
        # 确保有飞信电话
        if not call.is_text_present_c('飞信电话'):
            call.make_sure_p2p_voice_no_college()
            try:
                call.hang_up_the_call()
            except Exception:
                pass
        call.wait_for_page_c('通话', max_wait_time=60)
        time.sleep(2)
        self.assertEqual(call.is_text_present_c('[飞信电话]'), True)
        # 确保有多方视频通话记录
        if not call.is_text_present_c('多方视频'):
            call.make_sure_have_multiplayer_vedio_record()
        call.wait_for_page_c('通话', max_wait_time=60)
        time.sleep(2)
        self.assertEqual(call.is_text_present_c('[多方视频]'), True)
        # 确保有多方电话
        if not call.is_text_present_c('多方电话'):
            call.make_sure_have_multi_voice_record()
        call.wait_for_page_c('通话', max_wait_time=60)
        time.sleep(2)
        self.assertEqual(call.is_text_present_c('[多方电话]'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000115(self):
        """
            1、正常登录密友圈
            2、使用飞信电话给非联系人/不限时长成员/家庭网成员等关系的陌生号码拨打电话
            3、查看通话记录
            4、生成一条呼出的优惠电话记录，记录中昵称位置显示该陌生电话的全号，
            5、类型显示为：飞信电话，并显示该陌生号码的归属地和运营商
        """
        call = CallPage()
        call.wait_for_page_load()
        # 清空以前的通话记录
        call.clear_all_record()
        time.sleep(1)
        # 保证页面只有一条通话记录
        call.make_sure_p2p_voice_no_college()
        try:
            call.hang_up_the_call()
            time.sleep(1)
        except Exception:
            pass
        # 等待通话页面加载
        call.is_text_present_c('飞信电话', default_timeout=15)
        time.sleep(2)
        if call.is_element_already_exist_c('通话类型标签', default_timeout=8):
            self.assertEqual('[飞信电话]' == call.get_element_text_c('通话类型标签'), True)
            time.sleep(0.5)
        if call.is_element_already_exist_c('搜索_电话显示', default_timeout=8):
            self.assertEqual('北京 移动' == call.get_element_text_c('通话记录_归属地'), True)
            time.sleep(0.5)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000156(self):
        """
            1、正常登录密友圈
            2、使用飞信电话给非联系人/不限时长成员/家庭网成员等关系的陌生号码拨打电话
            3、查看通话记录
            4、生成一条呼出的优惠电话记录，记录中昵称位置显示该陌生电话的全号，
            5、类型显示为：飞信电话，并显示该陌生号码的归属地和运营商
        """
        call = CallPage()
        call.wait_for_page_load()
        call.clear_all_record()
        time.sleep(1)
        # 呼出一个多方视频通话
        call.multiplayer_vedio_call()
        call.wait_for_page_call_load()
        time.sleep(1)
        if call.is_element_already_exist_c('多方视频'):
            call.click_tag_detail_first_element('多方视频')
            time.sleep(0.5)
            call.click_locator_key_c('详情_发起多方视频')
            time.sleep(10)
            if call.is_element_already_exist_c('挂断_多方通话'):
                call.click_locator_key_c('挂断_多方通话')
                time.sleep(0.5)
            if call.is_element_already_exist_c('挂断_多方通话_确定'):
                call.click_locator_key_c('挂断_多方通话_确定')
                time.sleep(0.5)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000158(self):
        """展开拨号盘，不可以左右滑动切换tab，上方内容显示通话模块通话记录内容"""
        time.sleep(2)
        call = CallPage()
        call.wait_for_page_load()
        if call.is_on_this_page():
            call.click_show_keyboard()
            time.sleep(1)
        # 向左滑动
        time.sleep(0.5)
        call.page_left()
        # 判断滑动后是否还在此页面
        self.assertEqual(call.is_exist_call_key(), True)
        # 向右滑动
        time.sleep(0.5)
        call.page_right()
        # 判断滑动后是否还在此页面
        self.assertEqual(call.is_exist_call_key(), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000159(self):
        """
        点击拨号盘上面的默认通话记录
        1、正常网络状态下，登录密友圈；
        2、当前页面在通话页面
        3、拨号盘已打开
        4、通话模块存在通话记录
        5、点击该（除详情记录图标）通话记录任意区域
        6、点击右侧详情记录图标
        7、呼叫该记录的通话
        8、跳转该记录的通话详情页面"
        :return:
        """
        call = CallPage()
        call.wait_for_page_load()
        call.clear_all_record()
        time.sleep(0.5)
        # 呼出一个点对点视频通话
        call.make_sure_p2p_video_no_college()
        if call.is_element_already_exist_c('无密友圈_提示文本'):
            call.click_locator_key_c('无密友圈_取消')
            time.sleep(3)
            if call.is_text_present_c('视频通话'):
                call.click_text('视频通话')
                if call.is_element_already_exist_c('无密友圈_提示文本'):
                    call.click_locator_key_c('无密友圈_取消')
                    time.sleep(3)
        time.sleep(0.5)
        call.click_tag_detail_first_element('视频通话')
        time.sleep(1)
        self.assertEqual(call.is_text_present_c('通话记录 (视频通话)'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000160(self):
        """
        1、（未输入内容）上下滑动拨号盘以外的区域
        2、正常网络状态下，登录密友圈；
        3、当前页面在通话页面
        4、拨号盘已打开
        5、未输入内容
        6、在拨号盘以外的区域，进行上下滑动
        7、拨号盘收起；显示通话页面
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        # 上下滑动键盘区以外的区域
        call.swipe_direction_c('通话记录_记录区', 'down')
        time.sleep(0.5)
        self.assertEqual(call.is_exist_call_key(), False)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000161(self):
        """
        （输入匹配的内容）上下滑动拨号盘以外的区域
        1、正常网络状态下，登录密友圈；
        2、当前页面在通话页面
        3、拨号盘已打开
        4、输入的内容匹配到了号码
        在拨号盘以外的区域，进行上下滑动	保持拨号盘半收起状态；拨号盘搜索逻辑按号码，
        首字母，全拼模糊匹配，搜索的数据源包括：搜索的数据源包括：（本地通讯录+联系人+家庭网+未知电话）
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        # 按号码搜索
        call.input_text_c('键盘输入框', '138')
        time.sleep(1)
        call.swipe_direction_c('通话记录_记录区', 'up')
        time.sleep(0.5)
        self.assertEqual(call.is_element_already_exist_c('拨号界面_呼叫') and
                         call.is_element_already_exist_c('收起键盘'), True)
        self.assertEqual(call.get_elements_count_c('通话记录_号码') > 0, True)
        call.edit_clear_c('键盘输入框')
        # 按姓名搜索
        call.input_text_c('键盘输入框', '32')
        time.sleep(0.5)
        call.swipe_direction_c('通话记录_记录区', 'up')
        time.sleep(0.5)
        self.assertEqual(call.is_element_already_exist_c('拨号界面_呼叫') and
                         call.is_element_already_exist_c('收起键盘'), True)
        self.assertEqual(call.get_elements_count_c('通话记录_号码') > 0, True)
        call.edit_clear_c('键盘输入框')
        # 按首字母搜索
        call.input_text_c('键盘输入框', '4')
        time.sleep(0.5)
        call.swipe_direction_c('通话记录_记录区', 'up')
        time.sleep(0.5)
        self.assertEqual(call.is_element_already_exist_c('拨号界面_呼叫') and
                         call.is_element_already_exist_c('收起键盘'), True)
        self.assertEqual(call.get_elements_count_c('通话记录_号码') > 0, True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000162(self):
        """
        展示拨号盘半收起状态和展开拨号盘
        1、正常网络状态下，登录密友圈；
        2、当前页面在通话页面
        3、拨号盘半收起
        4、输入的内容匹配到了号码"	"1、显示拨号盘半收起
        2、点击拨号盘按钮
        3、清空输入框内容"	"1、输入框存在输入内容，底部从左往右依次为展开拨号盘按钮、呼叫按钮、清除按钮
        2、拨号盘全部展开
        3、拨号盘全盘展开"
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        call.input_text_c('键盘输入框', 138)
        time.sleep(1)
        call.swipe_direction_c('通话记录_记录区', 'up')
        time.sleep(0.5)
        self.assertEqual(call.is_element_already_exist_c('拨号界面_呼叫') and
                         call.is_element_already_exist_c('收起键盘'), True)
        self.assertEqual(call.get_elements_count_c('通话记录_号码') > 0, True)
        self.assertEqual(call.is_element_already_exist_c('收起键盘'), True)
        self.assertEqual(call.is_element_already_exist_c('拨号界面_呼叫'), True)
        self.assertEqual(call.is_element_already_exist_c('拨号界面_删除'), True)
        time.sleep(1)
        call.edit_clear_c('键盘输入框')
        time.sleep(1)
        self.assertEqual(call.is_text_present_c('直接拨号或拼音搜索')
                         and call.is_text_present_c('1'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000163(self):
        """
       （输入的内容无匹配）上下滑动拨号盘以外的区域
       1、正常网络状态下，登录密友圈；
        2、当前页面在通话页面
        3、拨号盘已打开
        4、输入的内容无匹配"
        在拨号盘以外的区域，进行上下滑动	保持拨号盘半收起状态；显示“无该联系人”的空白页面
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        # 键盘输入框
        time.sleep(1)
        call.input_text_c('键盘输入框', '12345666')
        time.sleep(1)
        call.swipe_direction_c('通话记录_记录区', 'up')
        time.sleep(1)
        call.swipe_direction_c('通话记录_记录区', 'down')
        time.sleep(0.5)
        self.assertEqual(call.is_element_already_exist_c('拨号界面_呼叫') and
                         call.is_element_already_exist_c('收起键盘'), True)
        self.assertEqual(call.is_text_present_c('无该联系人'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000164(self):
        """
       （拨号键盘半收起状态时，在拨号盘以外的区域，进行上下滑动
        1、正常网络状态下，登录密友圈；
        2、当前页面在通话页面
        3、拨号盘半收起"
        在拨号盘以外的区域，进行上下滑动	拨号盘任保持半收起状态；
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        call.input_text_c('键盘输入框', '12345666')
        time.sleep(1)
        call.swipe_direction_c('通话记录_记录区', 'up')
        time.sleep(0.5)
        call.swipe_direction_c('通话记录_记录区', 'down')
        self.assertEqual(call.is_element_already_exist_c('拨号界面_呼叫') and
                         call.is_element_already_exist_c('收起键盘'), True)
        self.assertEqual(call.is_text_present_c('无该联系人'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000167(self):
        """
       （点击的数字显示在输入框中
        1、正常网络状态下，登录密友圈；
        2、当前页面在通话页面
        3、拨号盘已打开
        任意点击“0/9号码和#与*”
        输入框显示“0/9号码和#与*”
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        call.click_locator_key_c('拨号界面_1')
        call.click_locator_key_c('拨号界面_3')
        call.click_locator_key_c('拨号界面_井')
        call.click_locator_key_c('拨号界面_星')
        self.assertEqual('13#*' == call.get_element_text_c('键盘输入框'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000168(self):
        """
        1、正常网络状态下，登录密友圈；
        2、当前页面在通话页面
        3、拨号盘已打开
        4、输入框默认显示“直接拨号或开始搜索”
        点击拨打	弹出“请输入正确号码”icon提示
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        call.click_locator_key_c('拨号界面_呼叫')
        call.is_toast_exist('请输入正确号码')

    @tags('ALL', 'CMCC', 'call')
    def test_call_000169(self):
        """
        1、正常网络状态下，登录密友圈；
        2、当前页面在通话页面
        3、拨号盘已打开
        4、输入框默认显示“直接拨号或开始搜索”
        点击拨打	弹出“请输入正确号码”icon提示
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        # 按首字母搜索
        call.input_text_c('键盘输入框', '4')
        time.sleep(0.5)
        call.swipe_direction_c('通话记录_记录区', 'up')
        time.sleep(0.5)
        self.assertEqual(call.get_elements_count_c('通话记录_号码') > 0, True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000170(self):
        """
        长按0数字键
        1、正常网络状态下，登录密友圈；
        2、当前页面在通话页面
        3、拨号盘已打开"
        长按0数字键
        输入框显示“+”符号
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        # 按首字母搜索
        call.press_element_c('拨号界面_0', times=1000)
        self.assertEqual('+' == call.get_element_text_c('键盘输入框'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000172(self):
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
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        # 按首字母搜索
        call.input_text_c('键盘输入框', '123456')
        call.click_locator_key_c('拨号界面_删除')
        self.assertEqual('12345' == call.get_element_text_c('键盘输入框'), True)
        call.press_element_c('拨号界面_删除', times=1000)
        self.assertEqual('直接拨号或拼音搜索' == call.get_element_text_c('键盘输入框'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000178(self):
        """
            输入框的字符限制	"1、正常网络状态下，登录密友圈；
            2、当前页面在通话页面
            3、拨号盘已打开"	输入1234567891234567	输入框只显示123456789123456（15位字符）超过字符不显示
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        # 按首字母搜索
        call.input_text_c('键盘输入框', '1234567891234567')
        time.sleep(1)
        self.assertEqual('123456789123456' == call.get_element_text_c('键盘输入框'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000180(self):
        """
            点击搜索出来的本地通讯录或未知号码或通话记录成员	"1、正常网络状态下，登录密友圈；
            2、当前页面在通话页面
            3、拨号盘已打开"	1、点击结果栏任意区域	直接呼叫
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        # 搜索
        call.input_text_c('键盘输入框', '13800138001')
        time.sleep(1)
        call.get_elements_list_c('通话记录_号码')[0].click()
        time.sleep(1)
        if call.is_element_already_exist_c('回呼_提示文本'):
            call.click_locator_key_c('回呼_我知道了')
        try:
            self.assertEqual(call.is_text_present_c('飞信电话', default_timeout=15), True)
        finally:
            try:
                call.hang_up_the_call()
            except Exception:
                pass

    @tags('ALL', 'CMCC', 'call')
    def test_call_000181(self):
        """
            点击搜索出来的联系人或家庭网号码	"1、正常网络状态下，登录密友圈；
            2、当前页面在通话页面
            3、拨号盘已打开"	"1、点击（除详情记录图标）该号码栏任意区域
            2、点击右侧详情记录图标"	"1、直接呼叫
            2、跳转至联系人或家庭网详情页面"
        """
        call = CallPage()
        call.wait_for_page_load()
        call.clear_all_record()
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        # 搜索
        time.sleep(0.5)
        call.input_text_c('键盘输入框', '13800138001')
        time.sleep(1)
        call.get_elements_list_c('通话记录_号码')[0].click()
        time.sleep(1)
        if call.is_element_already_exist_c('回呼_提示文本'):
            call.click_locator_key_c('回呼_我知道了')
        call.is_text_present_c('飞信电话', default_timeout=15)
        try:
            call.hang_up_the_call()
        except Exception:
            pass
        self.assertEqual(call.is_text_present_c('飞信电话', default_timeout=15), True)
        call.click_tag_detail_first_element('飞信电话')
        count = 30
        while count > 0:
            if call.on_this_page_call_detail():
                break
            count -= 1
        self.assertEqual(call.on_this_page_call_detail(), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000213(self):
        """
            联系人选择页点击“←”或者“取消”
            1、正常网络状态下，登录密友圈；
            2、当前页面在多方电话页面"
            点击‘←’或者“取消”按钮	回到通话主页
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已收起，则展开键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        # 搜索
        call.click_locator_key_c('加号')
        time.sleep(0.5)
        call.click_locator_key_c('多方电话')
        time.sleep(1)
        call.click_locator_key_c('多方电话_返回')
        time.sleep(1)
        self.assertEqual(call.is_element_already_exist_c('通话'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000215(self):
        """
            "1、正常网络状态下，登录密友圈；
            2、当前页面在多方电话页面"
            搜索联系人电话号码	支持模糊搜索
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已收起，则展开键盘
        # 判断如果键盘已收起，则展开键盘
        if not call.is_exist_call_key():
            call.click_show_keyboard()
            time.sleep(1)
        # 按首字母搜索
        call.input_text_c('键盘输入框', '138002')
        time.sleep(1)
        self.assertEqual(call.get_elements_count_c('通话记录_号码') > 0, True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000220(self):
        """
            未勾选联系人时的“呼叫”按钮	"1、正常网络状态下，登录密友圈；
            2、当前页面在多方电话页面"	不勾选联系人点击“呼叫”	未勾选联系人时“呼叫”按钮置灰，不可点
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.click_locator_key('加号')
        time.sleep(0.5)
        call.click_locator_key('多方电话')
        time.sleep(1)
        call.is_text_present_c('多方电话')
        time.sleep(1)
        self.assertEqual('false' == call.get_one_element_c('呼叫').get_attribute('enabled'), True)
        call.select_contact_n(1)
        self.assertEqual('true' == call.get_one_element_c('呼叫').get_attribute('enabled'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000221(self):
        """
            未勾选联系人时的“呼叫”按钮	"1、正常网络状态下，登录密友圈；
            2、当前页面在多方电话页面"	不勾选联系人点击“呼叫”	未勾选联系人时“呼叫”按钮置灰，不可点
        """
        call = CallPage()
        call.wait_for_page_load()
        # 判断如果键盘已拉起，则收起键盘
        if call.is_exist_call_key():
            call.click_hide_keyboard()
            time.sleep(1)
        call.click_locator_key('加号')
        time.sleep(0.5)
        call.click_locator_key('多方电话')
        time.sleep(1)
        call.is_text_present_c('多方电话')
        time.sleep(1)
        self.assertEqual(self.check_result_000221(9), True)

    @TestLogger.log('选择第n个联系人')
    def check_result_000221(self, number):
        """选择第n个联系人"""
        call = CallPage()
        try:
            lists = []
            locator = (MobileBy.ID, 'com.cmic.college:id/contact_number')
            count = 0
            selected = 0
            els = call.get_elements(locator)
            while True:
                if count > len(els) - 1:
                    count = 0
                    call.page_up()
                    time.sleep(1)
                    els = call.get_elements(locator)
                    continue
                el = els[count]
                count += 1
                if el.text in lists:
                    continue
                el.click()
                if call.is_text_present_c('最多邀请8人参与多方电话', default_timeout=0.5):
                    return True
                elif int(selected) <= number - 1:
                    selected = int(call.get_element_text_c('呼叫').split('/')[0].split('(')[-1])
                    lists.append(el.text)
                    continue
                else:
                    return False
        except Exception:
            print(traceback.print_exc())
            return False

    @tags('ALL', 'CMCC', 'call')
    def test_call_000248(self):
        """
            1、正常登录密友圈
            2、通话界面中有通话记录
            3、查看通话界面中的通话记录
            4、通话记录中记录电话的优惠电话、视频的视频通话与多方视频记录
            5、（无优惠电话，只判断‘飞信电话’‘多方电话’‘多方视频’‘视频通话’）
        """
        call = CallPage()
        call.wait_for_page_load()
        # 确保有视频通话
        if not call.is_text_present_c('视频通话'):
            call.make_sure_p2p_video_no_college()
            time.sleep(1)
            if call.is_element_already_exist_c('流量_不再提醒'):
                call.click_locator_key_c('流量_不再提醒')
                call.click_locator_key_c('流量_继续拨打')
            if call.is_element_already_exist_c('无密友圈_提示文本'):
                call.click_locator_key_c('无密友圈_取消')
                time.sleep(0.5)
        call.wait_for_page_c('通话', max_wait_time=60)
        time.sleep(2)
        self.assertEqual(call.is_text_present_c('[视频通话]'), True)
        # 确保有飞信电话
        time.sleep(0.5)
        if not call.is_text_present_c('飞信电话'):
            call.make_sure_p2p_voice_no_college()
            try:
                call.hang_up_the_call()
            except Exception:
                pass
        call.wait_for_page_c('通话', max_wait_time=60)
        time.sleep(2)
        self.assertEqual(call.is_text_present_c('[飞信电话]'), True)
        # 确保有多方视频通话记录
        time.sleep(0.5)
        if not call.is_text_present_c('多方视频'):
            call.make_sure_have_multiplayer_vedio_record()
        call.wait_for_page_c('通话', max_wait_time=60)
        time.sleep(2)
        self.assertEqual(call.is_text_present_c('[多方视频]'), True)
        # 确保有多方电话
        time.sleep(0.5)
        if not call.is_text_present_c('多方电话'):
            call.make_sure_have_multi_voice_record()
        call.wait_for_page_c('通话', max_wait_time=60)
        time.sleep(2)
        self.assertEqual(call.is_text_present_c('[多方电话]'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000254(self):
        """
            1、正常登录密友圈
            2、使用飞信电话给非联系人/不限时长成员/家庭网成员等关系的陌生号码拨打电话
            3、查看通话记录
            4、生成一条呼出的优惠电话记录，记录中昵称位置显示该陌生电话的全号，
            5、类型显示为：飞信电话，并显示该陌生号码的归属地和运营商
        """
        call = CallPage()
        call.wait_for_page_load()
        # 清空以前的通话记录
        call.clear_all_record()
        time.sleep(0.5)
        # 保证页面只有一条通话记录
        call.make_sure_p2p_voice_no_college()
        try:
            call.hang_up_the_call()
        except Exception:
            pass
        # 等待通话页面加载
        call.wait_for_page_call_load()
        time.sleep(2)
        # if call.is_element_already_exist_c('通话类型标签'):
        self.assertEqual('[飞信电话]' == call.get_element_text_c('通话类型标签'), True)
        # if call.is_element_already_exist_c('搜索_电话显示'):
        self.assertEqual('北京 移动' == call.get_element_text_c('通话记录_归属地'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000296(self):
        """
            拨号盘对+86号码优化	"1、正常登录密友圈
            2、网络正常
            3、当前页面在通话页面
            4、展开了拨号盘"	"1、输入+86XX号码
            2、点击拨打按钮"	"1、显示+86XX号码
            2、呼叫页面显示XX号码"
        """
        call = CallPage()
        call.wait_for_page_load()
        # 清空以前的通话记录
        call.clear_all_record()
        time.sleep(0.5)
        # 保证页面只有一条通话记录
        call.pick_up_p2p_voice('+8613800000000')
        # 等待通话页面加载
        time.sleep(2)
        try:
            call.hang_up_the_call()
        except Exception:
            pass
        time.sleep(1)
        call.is_text_present_c('飞信电话', default_timeout=30)
        self.assertEqual('13800000000' == call.get_element_text_c('搜索_电话昵称'), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000300(self):
        """
            不限时长通话记录的标记修改	"1、正常登录密友圈
            2、网络正常
            3、当前页面在通话页面
            4、存在不限时长通话记录"	查看修改内容	将名称下方的以前的“福利电话”修改为“飞信电话”
        """
        call = CallPage()
        call.wait_for_page_load()
        # 清空以前的通话记录
        call.clear_all_record()
        time.sleep(0.5)
        # 保证页面只有一条通话记录
        call.make_sure_p2p_voice_no_college()
        # 等待通话页面加载
        time.sleep(2)
        try:
            call.hang_up_the_call()
        except Exception:
            pass
        time.sleep(1)
        self.assertEqual(call.is_text_present_c('飞信电话', default_timeout=30), True)

    @tags('ALL', 'CMCC', 'call')
    def test_call_000306(self):
        """
            不限时长通话记录的标记修改	"1、正常登录密友圈
            2、网络正常
            3、当前页面在通话页面
            4、存在不限时长通话记录"	查看修改内容	将名称下方的以前的“福利电话”修改为“飞信电话”
        """
        call = CallPage()
        call.wait_for_page_load()
        # 清空以前的通话记录
        call.clear_all_record()
        time.sleep(0.5)
        self.assertEqual(call.is_text_present_c('打电话不花钱'), True)

