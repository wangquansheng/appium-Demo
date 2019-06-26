import time
from pages import *
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
import random
from pages.login.LoginPage import OneKeyLoginPage
from pages.guide import GuidePage
from pages.call.CallPage import CallPage



REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class LoginPreconditions(object):
    """登录前置条件"""

    @staticmethod
    def select_mobile(category, reset=False):
        """选择手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        if reset:
            current_mobile().reset_app()
        return client

    @staticmethod
    def make_already_in_one_key_login_page():
        """已经进入一键登录页"""
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return
        else:
            # 如果当前页不是引导页第一页，重新启动app
            guide_page = GuidePage()
            # current_mobile().launch_app()
            current_mobile().reset_app()
            guide_page.wait_for_page_load(20)
            # 跳过引导页
            guide_page.swipe_to_the_second_banner()
            guide_page.swipe_to_the_third_banner()
            current_mobile().hide_keyboard_if_display()
            guide_page.click_start_the_experience()
            time.sleep(1)
            # 权限页
            guide_page.click_one_button_on()
            time.sleep(2)
            if guide_page.is_text_present("取消"):
                guide_page.click_text("取消")
                time.sleep(2)
                guide_page.click_text("取消")
                current_mobile().launch_app()
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
        call_page.click_always_allow_c()
        time.sleep(2)
        call_page.remove_mask_c(2)


    @staticmethod
    def make_already_in_call_page(reset=False):
        """确保应用在通话页面"""
        LoginPreconditions.select_mobile('Android-移动', reset)
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        call_page = CallPage()
        if call_page.is_on_this_page():
            return
        else:
            try:
                current_mobile().launch_app()
                call_page.wait_for_page_load()
            except:
                # 进入一键登录页
                LoginPreconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                LoginPreconditions.login_by_one_key_login()


    # @staticmethod
    # def enter_private_chat_page(reset=False):
    #     """进入单聊会话页面"""
    #     # 登录进入消息页面
    #     LoginPreconditions.make_already_in_call_page(reset)
    #     mess = MessagePage()
    #     # 点击‘通讯录’
    #     mess.open_contacts_page()
    #     contacts = ContactsPage()
    #     contacts.wait_for_page_load()
    #     names = contacts.get_contacts_name()
    #     chat = SingleChatPage()
    #     cdp = ContactDetailsPage()
    #     # 不存在联系则创建联系人
    #     if not names:
    #         contacts.click_add()
    #         ccp = CreateContactPage()
    #         ccp.wait_for_page_load()
    #         name = "atest" + str(random.randint(100, 999))
    #         number = "147752" + str(time.time())[-5:]
    #         ccp.create_contact(name, number)
    #     contacts.select_people_by_name(names[0])
    #     cdp.wait_for_page_load()
    #     # 点击消息进入单聊会话页面
    #     cdp.click_message_icon()
    #     # 如果弹框用户须知则点击处理
    #     flag = chat.is_exist_dialog()
    #     if flag:
    #         chat.click_i_have_read()
    #     chat.wait_for_page_load()
