import re
import time
from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages.call.CallPage import CallPage

from pages.guide import GuidePage
from pages.login.LoginPage import OneKeyLoginPage
from pages.message.LocalFiles import LocalFilesPage
from pages.message.MessagePic import MessagePicPage
from pages.message.MessagePicPreview import MessagePicPreviewPage
from pages.message.NewMessage import NewMessagePage
from pages.message.Phone import PhonePage
from pages.message.groupchart.GroupChart import GroupChartPage
from pages.message.groupchart.GroupChartSetting import GroupChartSettingPage
from pages.message.message import MessagePage
from pages.message.singlechart.ModIfyTheme import ChartModifyThemePage
from pages.message.singlechart.SingleChartSetting import SingChartSettingPage
from pages.mine.GroupCode import GroupCodePage

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

    @staticmethod
    def login_by_one_key_login():
        """
        从一键登录页面登录
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_tell_number_load(60)
        login_number = one_key.get_login_number()
        one_key.click_one_key_login()
        one_key.click_sure_login()
        # 等待消息页
        gp = GuidePage()
        try:
            gp.click_cancel_update()
        except:
            pass
        cp = CallPage()
        cp.click_contact_tip()
        return login_number

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
        2.当前在通话页面
        """
        # 如果当前页面是在通话录页，不做任何操作
        call_page = CallPage()
        if call_page.is_on_this_page():
            return
        # 如果当前页面已经是一键登录页，进行一键登录页面
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            Preconditions.login_by_one_key_login()
            return
        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            current_mobile().launch_app()
            guide_page.wait_for_page_load(20)
            # 跳过引导页
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()

    @staticmethod
    def make_already_in_message_page():
        """
        前置条件：
        1.已登录客户端
        2.当前在消息页面
        """
        """确保应用在消息页面"""
        # 如果在消息页，不做任何操作
        call_page = CallPage()
        mep = MessagePage()
        if mep.is_on_this_page():
            return
        if not call_page.is_on_this_page():
            current_mobile().launch_app()
        call_page.open_message_page()

    @staticmethod
    def make_already_in_message_chart_page():
        """
        前置条件：
        1.已登录客户端
        2.当前在消息会话页面
        """
        """确保应用在消息会话页面"""
        # 如果在消息页，不做任何操作
        call_page = CallPage()
        mep = MessagePage()
        if mep.is_on_this_chart_page():
            return
        if mep.is_on_this_page():
            mep.click_add()
            mep.click_add_message()
            nmp = NewMessagePage()
            nmp.wait_for_page_new_message()
            nmp.click_contact_one()
            return
        if call_page.is_on_this_page():
            call_page.open_message_page()
        if not call_page.is_on_this_page():
            current_mobile().launch_app()
            call_page.open_message_page()
        mep.click_add()
        mep.click_add_message()
        nmp = NewMessagePage()
        nmp.wait_for_page_new_message()
        nmp.click_contact_one()

        # Preconditions.make_already_in_call_page()
        # call = CallPage()
        # call.open_message_page()
        # mep = MessagePage()
        # mep.wait_for_page_message()
        # mep.click_add()
        # mep.click_add_message()
        # nmp = NewMessagePage()
        # nmp.wait_for_page_new_message()
        # nmp.click_contact_one()

    @staticmethod
    def make_already_have_group_chart():
        """
        前置条件：
        1.已登录客户端
        2.当前在消息会话页面
        """
        """确保应用在消息页面"""
        # 如果在消息页，不做任何操作
        Preconditions.make_already_in_message_page()
        mep = MessagePage()
        mep.click_add()
        mep.click_group_chart()
        nmp = NewMessagePage()
        nmp.wait_for_page_new_message()
        nmp.click_contact_one(2)
        nmp.click_text("确定")
        time.sleep(1)
        nmp.click_text("确定")
        gcp = GroupChartPage()
        gcp.wait_for_page_group_chart()


class MessageTest(TestCase):
    """Message 模块"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        try:
            Preconditions.make_already_in_call_page()
        except:
            current_mobile().launch_app()
            try:
                current_mobile().reset_app()
                Preconditions.make_already_in_one_key_login_page()
                Preconditions.login_by_one_key_login()
            except:
                pass

    # @staticmethod
    # def setUp_test_message_0001():
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     Preconditions.make_already_in_message_chart_page()
    #
    # @tags('ALL', 'SMOKE', 'CMCC')
    # def test_message_0001(self):
    #     """ 本网正常网络首次登录4G-登录响应"""
    #     mep = MessagePage()
    #     mep.wait_for_page_chart_message()
    #     # 1.长按“录制语音”icon,是否有取消按钮
    #     mep.click_record_audio()
    #     mep.long_click_record_audio()
    #     mep.is_exist_cancel_audio()
    #
    # @staticmethod
    # def setUp_test_message_0002():
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     Preconditions.make_already_in_message_chart_page()
    #
    # @tags('ALL', 'SMOKE', 'CMCC')
    # def test_message_0002(self):
    #     """ 取消录制语音消息"""
    #     mep = MessagePage()
    #     mep.wait_for_page_chart_message()
    #     # 1.长按“录制语音”icon,是否有取消按钮
    #     mep.click_record_audio()
    #     mep.press_and_move_to_el("开始录音", "取消录音")

    @staticmethod
    def setUp_test_message_0003():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0003(self):
        """ 发送语音消息"""
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        # 1.长按“录制语音”icon
        mep.click_record_audio()
        mep.click_start_record_audio()
        time.sleep(2)
        if mep.is_text_present("始终允许"):
            mep.click_text("始终允许")
        time.sleep(1.2)
        mep.long_click_record_audio()

    @staticmethod
    def setUp_test_message_0004():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0004(self):
        """ 会话界面使用录音功能发送0秒语音"""
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        # 1.点击“录制语音”icon，检验有时间太短提示
        mep.click_record_audio()
        # mep.long_click_record_audio(time=100, wait_time=0.5)
        mep.click_start_record_audio()
        if not mep.is_toast_exist("时间太短"):
            raise AssertionError("没有此时间太短提示框")

    @staticmethod
    def setUp_test_message_0005():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0005(self):
        """ 消息会话-发送相册照片页面显示"""
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        # 1.点击点击图片按钮
        mep.click_pic()
        mpp = MessagePicPage()
        mpp.wait_for_page_select_pic()
        # 2.校验a返回按钮，b照片，视频可勾选状态，c 发送按钮匹配
        menu = {"返回", "预览", "原图", "发送"}
        mpp.page_contain_ele(menu)
        mpp.is_select_pic()
        flag = mpp.get_pic_send_info()
        self.assertIsNotNone(re.match(r'发送\(\d+/9\)', flag))

    @staticmethod
    def setUp_test_message_0006():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0006(self):
        """ 消息会话-发送相册照片页面显示"""
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        # 1.点击点击图片按钮
        mep.click_pic()
        mpp = MessagePicPage()
        mpp.wait_for_page_select_pic()
        # 2.a 未勾选时，预览显示置灰；
        self.assertEquals(mpp.is_click(), False)
        # b勾选图片，张数显示;
        mpp.select_pic(2)
        flag = mpp.get_pic_send_info()
        self.assertIsNotNone(re.match(r'发送\(2/9\)', flag))
        mpp.select_pic(2)
        mpp.select_pic(14)
        self.assertEquals(mpp.is_toast_exist("最多只能选择9张照片"), True)
        # c 最多可勾选9张图片

    @staticmethod
    def setUp_test_message_0007():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0007(self):
        """ 消息会话-发送相册照片-预览照片页面"""
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        # 1.点击点击图片按钮
        mep.click_pic()
        mpp = MessagePicPage()
        mpp.wait_for_page_select_pic()
        # 2.a 未勾选时，预览显示置灰；
        self.assertEquals(mpp.is_click(), False)
        # b勾选图片，张数显示;
        mpp.select_pic(2)
        flag = mpp.get_pic_send_info()
        self.assertIsNotNone(re.match(r'发送\(2/9\)', flag))
        mpp.select_pic(2)
        # c 最多可勾选9张图片
        mpp.select_pic(14)
        self.assertEquals(mpp.is_toast_exist("最多只能选择9张照片"), True)
        # 3.点击预览照片
        mpp.click_pre_view()
        mpv = MessagePicPreviewPage()
        mpv.wait_for_page_preview_pic()
        time.sleep(5)
        self.assertEquals(mpv.is_click_send(), True)
        for i in range(9):
            mpv.click_select_box()
            mpv.page_right()
        self.assertEquals(mpv.is_click_send(), False)
        # 4.照片左滑
        mpv.page_right()
        mpv.wait_for_page_preview_pic()
        # 5.照片右滑
        mpv.page_left()
        mpv.wait_for_page_preview_pic()

    @staticmethod
    def setUp_test_message_0008():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0008(self):
        """ 文件消息-发送文件入口"""
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        # 1.点击点击图片按钮
        mep.click_file()
        lfp = LocalFilesPage()
        lfp.wait_for_page_select_files()
        menu = {"照片", "音乐", "视频", "本地文件"}
        lfp.page_contain_ele(menu)
        lfp.click_select_pic()
        lfp.wait_for_page_select_send_files()
        lfp.click_select_pic_file()
        lfp.click_select_send()
        time.sleep(2.8)
        self.assertEquals(mep.is_on_this_chart_page(), True)

    @staticmethod
    def setUp_test_message_0011():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_have_group_chart()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0011(self):
        """ 群聊设置页新增邀请微信或者QQ 好友进群入口"""
        # 0.在群聊天设置页面，进入群管理员页面页面
        gcp = GroupChartPage()
        gcp.wait_for_page_group_chart()
        gcp.click_setting()
        gcs = GroupChartSettingPage()
        gcs.wait_for_page_group_chart_setting()
        gcs.click_group_member()
        nmp = NewMessagePage()
        # 1.在群聊管理员页面长按，点击批量删除,该群成员处于选中状态，顶端右侧显示“删除”按钮
        time.sleep(1.8)
        nmp.press_long()
        nmp.click_delete_member()
        nmp.wait_for_page_delete_member()
        self.assertEquals(nmp.get_delete_button(), True)
        self.assertEquals(nmp.page_contain_ele(), True)
        name = nmp.get_contact_one()
        nmp.click_contact_one(1)
        time.sleep(1.5)
        self.assertEquals(nmp.page_contain_ele(), False)
        self.assertEquals(nmp.get_delete_button(), False)
        nmp.click_contact_one(1)
        # 2.点击删除,等待确定弹框提示
        nmp.click_delete_button()
        nmp.wait_for_page_delete_member_again()
        # 3.点击取消
        nmp.click_delete_member_cancel()
        nmp.wait_for_page_delete_member()
        # 4.重复1-2步骤，选择删除
        nmp.click_delete_button()
        nmp.click_delete_member_sure()
        time.sleep(2)
        nmp.page_should_not_contain_text(name)
        nmp.click_back()
        nmp.click_back()
        gcp.wait_for_page_group_chart()
        gcp.page_should_contain_text(name + "被移除群")

    def tearDown_test_message_0011(self):
        gcp = GroupChartPage()
        gcp.wait_for_page_group_chart()
        # 进入群聊设置页面点击删除
        gcp.click_setting()
        gcp.page_up()
        gcs = GroupChartSettingPage()
        gcs.wait_for_page_group_chart_setting()
        gcs.click_delete_group()
        # 点击确定，选择一个新群主，再确定
        gcs.click_delete_group_sure()
        nmp = NewMessagePage()
        nmp.wait_for_page_new_message()
        nmp.click_contact_one(1)
        gcs.click_delete_group_sure()
        self.assertEquals(gcs.is_toast_exist("已退出群聊"), True)

    @staticmethod
    def setUp_test_message_0014():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_have_group_chart()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0014(self):
        """ 群聊设置页新增邀请微信或者QQ 好友进群入口"""
        # 1.在群聊天设置页面,检查新增邀请微信或者QQ好友进群
        gcp = GroupChartPage()
        gcp.wait_for_page_group_chart()
        gcp.click_setting()
        gcs = GroupChartSettingPage()
        gcs.wait_for_page_group_chart_setting()
        gcs.page_should_contain_text("邀请微信或者QQ好友进群")
        gcs.click_back()

    def tearDown_test_message_0014(self):
        gcp = GroupChartPage()
        gcp.wait_for_page_group_chart()
        # 进入群聊设置页面点击删除
        gcp.click_setting()
        gcp.page_up()
        gcs = GroupChartSettingPage()
        gcs.wait_for_page_group_chart_setting()
        gcs.click_delete_group()
        # 点击确定，选择一个新群主，再确定
        gcs.click_delete_group_sure()
        nmp = NewMessagePage()
        nmp.wait_for_page_new_message()
        nmp.click_contact_one(1)
        gcs.click_delete_group_sure()
        self.assertEquals(gcs.is_toast_exist("已退出群聊"), True)

    @staticmethod
    def setUp_test_message_0015():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_have_group_chart()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0015(self):
        """ 点击后弹出群口令的生成弹窗"""
        # 1.在群聊天设置页面,检查新增邀请微信或者QQ好友进群
        gcp = GroupChartPage()
        gcp.wait_for_page_group_chart()
        gcp.click_setting()
        gcs = GroupChartSettingPage()
        gcs.wait_for_page_group_chart_setting()
        gcs.page_should_contain_text("邀请微信或者QQ好友进群")
        gcs.click_invite()
        gcs.wait_for_page_group_chart_setting_share()
        gcs.page_should_contain_text("分享口令邀请好友进群")
        gcs.page_should_contain_text("分享口令")
        gcs.click_not_share()
        gcs.click_back()

    def tearDown_test_message_0015(self):
        gcp = GroupChartPage()
        gcp.wait_for_page_group_chart()
        # 进入群聊设置页面点击删除
        gcp.click_setting()
        gcp.page_up()
        gcs = GroupChartSettingPage()
        gcs.wait_for_page_group_chart_setting()
        gcs.click_delete_group()
        # 点击确定，选择一个新群主，再确定
        gcs.click_delete_group_sure()
        nmp = NewMessagePage()
        nmp.wait_for_page_new_message()
        nmp.click_contact_one(1)
        gcs.click_delete_group_sure()
        self.assertEquals(gcs.is_toast_exist("已退出群聊"), True)

    @staticmethod
    def setUp_test_message_0016():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_have_group_chart()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0016(self):
        """ 群管理入口-群主"""
        # 1.在群聊天设置页面,检查群管理入口
        gcp = GroupChartPage()
        gcp.wait_for_page_group_chart()
        gcp.click_setting()
        gcs = GroupChartSettingPage()
        gcs.wait_for_page_group_chart_setting()
        # 2 点击群管理,转让
        gcs.click_manager_group()
        gcs.click_transfer_group()
        # 3选择成员
        nmp = NewMessagePage()
        nmp.wait_for_page_new_message()
        nmp.click_contact_one(1)
        gcs.click_delete_group_sure()
        self.assertEquals(nmp.is_toast_exist("已转让"), True)
        gcs.click_back()

    @staticmethod
    def setUp_test_message_0017():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_have_group_chart()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0017(self):
        """ 查看“群二维码”页面显示"""
        # 1.在群聊天设置页面,检查群管理入口
        gcp = GroupChartPage()
        gcp.wait_for_page_group_chart()
        gcp.click_setting()
        gcs = GroupChartSettingPage()
        gcs.wait_for_page_group_chart_setting()
        # 2 点击群管理,转让
        gcs.click_group_code()
        gcp = GroupCodePage()
        gcp.wait_for_page_group_code()
        menu = {"返回", "群二维码", "群头像", "群名称", "群二维码内容"}
        gcp.page_contain_ele(menu)
        gcp.page_should_contain_text("密友圈扫描二维码，加入群聊")
        gcp.click_back()
        gcp.click_back()

    def tearDown_test_message_0017(self):
        gcp = GroupChartPage()
        gcp.wait_for_page_group_chart()
        # 进入群聊设置页面点击群管理
        gcp.click_setting()
        gcs = GroupChartSettingPage()
        gcs.wait_for_page_group_chart_setting()
        gcs.click_text("群管理")
        time.sleep(0.8)
        gcs.click_text("解散群")
        time.sleep(0.8)
        gcs.click_text("确定")
        self.assertEquals(gcs.is_toast_exist("已解散群"), True)

    @staticmethod
    def setUp_test_message_0018():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0018(self):
        """消息会话拍摄1张照片并发送"""
        # 1.在群聊天设置页面,检查群管理入口
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        mep.click_take_photo()
        php = PhonePage()
        php.wait_for_page_phone()
        php.click_take_phone()
        time.sleep(1.8)
        php.click_take_phone_send()

    def tearDown_test_message_0018(self):
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        mep.press_and_do("删除")
        # 进入群聊设置页面点击群管理
        mep.page_should_contain_text("免流量")

    @staticmethod
    def setUp_test_message_0019():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0019(self):
        """消息会话录制1段视频并发送"""
        # 1.在群聊天设置页面,检查群管理入口
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        mep.click_take_photo()
        php = PhonePage()
        php.wait_for_page_phone()
        php.press_long_phone()
        time.sleep(1.8)
        php.click_take_phone_send()

    def tearDown_test_message_0019(self):
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        mep.press_and_do_video("删除")
        # 进入群聊设置页面点击群管理
        mep.page_should_contain_text("免流量")

    @staticmethod
    def setUp_test_message_0020():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0020(self):
        """消息会话录制1段视频并预览"""
        # 1.在群聊天设置页面,检查群管理入口
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        mep.click_take_photo()
        php = PhonePage()
        php.wait_for_page_phone()
        php.press_long_phone()
        time.sleep(1.8)
        php.wait_for_page_video()
        php.click_cancel_send()
        php.click_back()

    def tearDown_test_message_0020(self):
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        # 进入群聊设置页面点击群管理
        mep.page_should_contain_text("免流量")

    @staticmethod
    def setUp_test_message_0021():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0021(self):
        """聊天设置-聊天背景设置入口"""
        # 1.在群聊天设置页面,检查更改聊天主题背景入口
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        mep.click_chart_setting()
        scp = SingChartSettingPage()
        scp.wait_for_page_single_chart_setting()
        scp.page_should_contain_text("更改聊天主题背景")
        # 2.点击“更改聊天主题背景”
        scp.click_modify_theme()
        mtp = ChartModifyThemePage()
        mtp.wait_for_page_single_chart_theme()

    def tearDown_test_message_0021(self):
        mtp = ChartModifyThemePage()
        mtp.click_back()
        mtp.click_back()

    @staticmethod
    def setUp_test_message_0022():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0022(self):
        """聊天设置-聊天背景设置入口"""
        # 1.在群聊天设置页面,检查更改聊天主题背景入口
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        mep.click_chart_setting()
        scp = SingChartSettingPage()
        scp.wait_for_page_single_chart_setting()
        scp.page_should_contain_text("更改聊天主题背景")
        # 2.点击“更改聊天主题背景”
        scp.click_modify_theme()
        mtp = ChartModifyThemePage()
        mtp.wait_for_page_single_chart_theme()
        # 3.校验聊天背景设置页面显示
        menu1 = {"更改此主题背景", "当前主题背景，尝鲜试试其他风格", "取消", "应用"}
        mtp.page_contain_text(menu1)
        menu2 = {"背景图", "更改框1", "更改框2", "展示框", "取消", "应用"}
        mtp.page_contain_ele(menu2)

    def tearDown_test_message_0022(self):
        mtp = ChartModifyThemePage()
        mtp.click_back()
        mtp.click_back()

    @staticmethod
    def setUp_test_message_0023():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL1', 'SMOKE', 'CMCC')
    def test_message_0023(self):
        """聊天设置-聊天背景更改取消"""
        # 1.在群聊天设置页面,检查更改聊天主题背景入口
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        mep.click_chart_setting()
        scp = SingChartSettingPage()
        scp.wait_for_page_single_chart_setting()
        scp.page_should_contain_text("更改聊天主题背景")
        # 2.点击“更改聊天主题背景”
        scp.click_modify_theme()
        mtp = ChartModifyThemePage()
        mtp.wait_for_page_single_chart_theme()
        # 3.校验聊天背景设置页面显示
        menu1 = {"更改此主题背景", "当前主题背景，尝鲜试试其他风格", "取消", "应用"}
        mtp.page_contain_text(menu1)
        menu2 = {"背景图", "更改框1", "更改框2", "展示框", "取消", "应用"}
        mtp.page_contain_ele(menu2)
        for i in range(1):
            mtp.page_right()
        mtp.click_cancel()

