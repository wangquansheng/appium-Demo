from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage
import time


class CallPage(FooterPage):
    """通话页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        # 权限框
        '禁止': (MobileBy.ID, 'com.android.packageinstaller:id/permission_deny_button'),
        '始终允许': (MobileBy.ID, 'com.android.packageinstaller:id/permission_allow_button'),
        '遮罩1': (MobileBy.ID, 'com.cmic.college:id/tvContact'),
        '遮罩2': (MobileBy.ID, 'com.cmic.college:id/header'),

        '通话文案': (MobileBy.ID, 'com.cmic.college:id/header'),
        '来电名称': (MobileBy.ID, 'com.cmic.college:id/tvName'),
        '来电详情': (MobileBy.ID, 'com.cmic.college:id/ivDetail'),
        '+': (MobileBy.ID, 'com.cmic.college:id/ivOperation'),
        '视频通话': (MobileBy.XPATH, '//*[contains(@text,"视频通话")]'),
        '多方电话': (MobileBy.XPATH, '//*[contains(@text,"多方电话")]'),

        '视频通话x': (
            MobileBy.XPATH,
            '//android.widget.TextView[@resource-id="com.cmic.college:id/pop_navi_text" and @text="视频通话"]'),
        '多方电话x': (
            MobileBy.XPATH,
            '//android.widget.TextView[@resource-id="com.cmic.college:id/pop_navi_text" and @text="多方电话"]'),
        '空白文案': (MobileBy.XPATH, '//*[contains(@text,"打电话不花钱")]'),
        '键盘输入框': (MobileBy.ID, 'com.cmic.college:id/etInputNum'),
        '收起键盘': (MobileBy.ID, 'com.cmic.college:id/ivHide'),

        'tip1': (MobileBy.ID, 'com.cmic.college:id/ivFreeCall'),
        'tip2': (MobileBy.ID, 'com.cmic.college:id/ivKeyboard'),
        'tip3': (MobileBy.ID, 'com.cmic.college:id/tvContact'),
        '视频': (MobileBy.ID, 'com.cmic.college:id/ivMultipartyCall'),
        '通话类型标签': (MobileBy.ID, 'com.cmic.college:id/tvCallManner'),
        '联系人_详情图标': (MobileBy.ID, 'com.cmic.college:id/ivDetail'),
        '电话图标': (MobileBy.ID, 'com.cmic.college:id/ivFreeCall'),
        '拨号键盘': (MobileBy.ID, 'com.cmic.college:id/ivKeyboard'),

        '呼叫': (MobileBy.ID, 'com.cmic.college:id/tv_sure'),
        # 发起视频通话页面
        '视频通话_第一个联系人': (MobileBy.XPATH,
                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.'
                        'FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.'
                        'LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.'
                        'LinearLayout/android.widget.RelativeLayout/android.widget.ListView/android.widget.'
                        'LinearLayout[1]/android.widget.RelativeLayout'),
        '视频通话_第二个联系人': (MobileBy.XPATH,
                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.'
                        'FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.'
                        'LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.'
                        'LinearLayout/android.widget.RelativeLayout/android.widget.ListView/android.widget.'
                        'LinearLayout[2]/android.widget.RelativeLayout'),
        '视频通话_第三个联系人': (MobileBy.XPATH,
                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.'
                        'FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.'
                        'LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.'
                        'LinearLayout/android.widget.RelativeLayout/android.widget.ListView/android.widget.'
                        'LinearLayout[3]/android.widget.RelativeLayout'),

        '多方通话_返回': (MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="转到上一层级"]'),
        '电话号码': (MobileBy.ID, 'com.cmic.college:id/contact_number'),
        # 多人视频通话页面
        '挂断_多方通话': (MobileBy.ID, 'com.cmic.college:id/end_video_call_btn'),
        '挂断_多方通话_确定': (MobileBy.ID, 'com.cmic.college:id/btnConfirm'),
        '删除_一条通话记录': (MobileBy.XPATH,
                      '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]'),
        '删除_全部通话记录': (MobileBy.XPATH,
                      '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[2]'),
        '通话记录_删除一条': (
            MobileBy.XPATH,
            '//android.widget.TextView[@resource-id="com.cmic.college:id/tvContent" and @text="删除该通话记录"]'),
        '通话记录_删除全部': (
            MobileBy.XPATH,
            '//android.widget.TextView[@resource-id="com.cmic.college:id/tvContent" and @text="清除全部通话记录"]'),
        '通话记录_确定': (MobileBy.ID, 'com.cmic.college:id/btnConfirm'),
        '通话记录_取消': (MobileBy.ID, 'com.cmic.college:id/btnCancel'),

        # 单人视频详情页
        '详情_视频按钮': (MobileBy.ID, 'com.cmic.college:id/tvVideoCall'),
        '详情_信息按钮': (MobileBy.ID, 'com.cmic.college:id/tvSendMessage'),
        # '详情_返回': (MobileBy.ID, 'com.cmic.college:id/ivBack'),
        '挂断': (MobileBy.ID, 'com.cmic.college:id/video_iv_term'),
        # 多人视频详情页
        '详情_多人视频': (MobileBy.ID, 'com.cmic.college:id/rlStartMultipartyVideo'),
        '详情_群聊': (MobileBy.ID, 'com.cmic.college:id/rlCreateGroup'),
        '群聊_确定': (MobileBy.ID, 'com.cmic.college:id/tv_sure'),
        '群聊_返回上一层': (MobileBy.ID, 'com.cmic.college:id/back_arrow'),
        '多人_挂断': (MobileBy.ID, 'com.cmic.college:id/end_video_call_btn'),
        '信息_聊天框': (MobileBy.ID, 'com.cmic.college:id/et_message'),
        '信息_发送': (MobileBy.ID, 'com.cmic.college:id/ib_send'),
        # 拨号界面
        '拨叫号码': (MobileBy.ID, 'com.cmic.college:id/etInputNum'),
        '拨号界面_呼叫': (MobileBy.ID, 'com.cmic.college:id/ivVoiceCall'),
        '拨号界面_挂断': (MobileBy.ID, 'com.android.incallui:id/endButton'),
        '拨号_返回': (MobileBy.XPATH,
                  '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.ImageButton'),
        # 福利电话
        '页面规则': (MobileBy.ID, 'com.cmic.college:id/action_rule'),
        '电话_搜索栏': (MobileBy.ID, 'com.cmic.college:id/action_search'),
        '搜索_电话': (MobileBy.ID, 'com.cmic.college:id/search_src_text'),
        '搜索_电话显示': (MobileBy.ID, 'com.cmic.college:id/tvPhoneNum'),
        '搜索_电话昵称': (MobileBy.ID, 'com.cmic.college:id/tvName'),
        '免费时长': (MobileBy.ID, 'com.cmic.college:id/tv_leftDuration'),

        # 关闭广告页面
        '广告_关闭': (MobileBy.ID, 'com.cmic.college:id/ivClose'),
        '广告_内容': (MobileBy.ID, 'com.cmic.college:id/ivContent'),
        '广告_立即参与': (MobileBy.ID, 'com.cmic.college:id/ivEnter'),

        # 通话详情页面
        '详情_返回': (MobileBy.ID, 'com.cmic.college:id/ivBack'),
        '详情_更多': (MobileBy.ID, 'com.cmic.college:id/iv_more'),
        '详情_红点': (MobileBy.ID, 'com.cmic.college:id/view_red_dot'),
        '详情_头像': (MobileBy.ID, 'com.cmic.college:id/ivAvatar'),
        '详情_名称': (MobileBy.ID, 'com.cmic.college:id/tvName'),
        '详情_通话': (MobileBy.ID, 'com.cmic.college:id/tvSendMessage'),
        '详情_视频': (MobileBy.ID, 'com.cmic.college:id/tvVideoCall'),
        '详情_备注标签': (MobileBy.ID, 'com.cmic.college:id/tv_nickname'),
        '详情_备注内容': (MobileBy.ID, 'com.cmic.college:id/tv_nickset'),
        '详情_>': (MobileBy.ID, 'com.cmic.college:id/iv_arrow_right'),
        '详情_归属地': (MobileBy.ID, 'com.cmic.college:id/tv_phoneProperty'),
        '详情_电话号码': (MobileBy.ID, 'com.cmic.college:id/tv_phoneValue'),
        '详情_通话记录': (MobileBy.ID, 'com.cmic.college:id/tvCallRecordsType'),
        '详情_通话时间': (MobileBy.ID, 'com.cmic.college:id/tvCallTime'),
        '详情_通话类型': (MobileBy.ID, 'com.cmic.college:id/tvCallType'),
        '详情_通话时长': (MobileBy.ID, 'com.cmic.college:id/tvCallDuration'),
        '详情_邀请使用': (MobileBy.ID, 'com.cmic.college:id/bt_add_meetyou'),
        # 邀请使用
        '邀请_微信好友': (MobileBy.ID, 'com.cmic.college:id/tv_wechat'),
        '邀请_QQ好友': (MobileBy.ID, 'com.cmic.college:id/tv_qq'),
        '邀请_短信': (MobileBy.ID, 'com.cmic.college:id/tv_sms'),

        #  修改备注页面
        '备注_保存': (MobileBy.ID, 'com.cmic.college:id/nick_name_save'),
        '备注_返回': (MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="到上一层级"]'),
        '修改备注名': (MobileBy.XPATH, '//android.widget.TextView[@text="修改备注名"]'),
        '备注': (MobileBy.ID, 'com.cmic.college:id/edit_query'),
        '备注_备注': (MobileBy.XPATH, '//android.widget.EditText[@resource-id="com.cmic.college:id/edit_query"]'),

        # 流量优惠提示框
        '流量_不再提醒': (MobileBy.ID, 'com.cmic.college:id/select_checkbox'),
        '流量_去开通': (MobileBy.ID, 'com.cmic.college:id/bt_open'),
        '流量_继续拨打': (MobileBy.ID, 'com.cmic.college:id/tv_continue'),
        '流量_提示内容': (MobileBy.ID, 'com.cmic.college:id/content'),

        # 视频通话界面
        '视频_转为语音通话': (MobileBy.ID, 'com.cmic.college:id/video_iv_change_to_voice'),
        '视频_结束视频通话': (MobileBy.ID, 'com.cmic.college:id/video_iv_term'),
        '视频_切换摄像头': (MobileBy.ID, 'com.cmic.college:id/video_iv_switch_camera'),
        '视频_备注': (MobileBy.ID, 'com.cmic.college:id/video_tv_name'),

        # 对方还未使用密友圈，喊他一起来免流量视频通话
        '无密友圈_提示文本': (MobileBy.XPATH, '//*[contains(@text,"对方还未使用密友圈")]'),
        '无密友圈_确定': (MobileBy.ID, 'com.cmic.college:id/btnConfirm'),
        '无密友圈_取消': (MobileBy.ID, 'com.cmic.college:id/btnCancel'),
        '回呼_提示文本': (MobileBy.ID, 'com.cmic.college:id/content'),
        '回呼_不再提醒': (MobileBy.ID, 'com.cmic.college:id/select_checkbox'),
        '回呼_我知道了': (MobileBy.ID, 'com.cmic.college:id/bt_open'),

        # 悬浮窗授权提示
        '悬浮窗_内容': (MobileBy.XPATH, '//*[contains(@text,"您的手机没有授予悬浮窗权限，请开启后再试")]'),
        '暂不开启': (MobileBy.ID, 'android:id/button2'),
        '现在去开启': (MobileBy.ID, 'android:id/button1'),

    }

    @TestLogger.log('点击通话引导页')
    def click_contact_tip(self):
        self.click_element(self.__locators['tip1'])
        self.click_element(self.__locators['tip2'])
        self.click_element(self.__locators['tip3'])

    @TestLogger.log()
    def click_always_allow(self):
        """权限框-点击始终允许"""
        while self.is_text_present('始终允许'):
            self.click_text('始终允许')
            time.sleep(2)

    @TestLogger.log()
    def remove_mask(self):
        """去除遮罩"""
        self.click_element(self.__class__.__locators['遮罩1'])
        self.click_element(self.__class__.__locators['遮罩2'])

    @TestLogger.log("页面是否包含广告推送页，并关闭")
    def close_ad_if_exist(self):
        """页面是否包含广告推送页，并关闭"""
        if self.on_this_page_common('广告_关闭') and self.on_this_page_common('广告_立即参与'):
            self.click_locator_key('广告_关闭')

    @TestLogger.log("您的手机没有授予悬浮窗权限，请开启后再试")
    def close_suspension_if_exist(self):
        """您的手机没有授予悬浮窗权限，请开启后再试"""
        while self.is_text_present('您的手机没有授予悬浮窗权限，请开启后再试') and self.is_text_present(
                '暂不开启') and self.is_text_present('现在去开启'):
            self.click_text('暂不开启')
    #
    # @TestLogger.log("您的的好友没有开通密友圈")
    # def close_not_opened_if_exist(self):
    #     """您的的好友没有开通密友圈"""
    #     while self.on_this_page_common('无密友圈_提示文本'):
    #         self.click_locator_key('无密友圈_取消')

    @TestLogger.log('等待页面自动跳转')
    def wait_for_page_call(self, max_wait_time=30):
        self.wait_until(
            condition=lambda d: self.is_text_present("不花钱打电话"),
            timeout=max_wait_time,
        )

    @TestLogger.log('等待页面自动跳转')
    def wait_for_page_call_load(self, max_wait_time=30):
        self.wait_until(
            condition=lambda d: self.is_text_present("通话"),
            timeout=max_wait_time,
        )

    @TestLogger.log('是否在通话页面')
    def is_on_this_page(self):
        el = self.get_elements(self.__locators['拨号键盘'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log("点击locators对应的元素")
    def click_locator_key(self, locator):
        self.click_element(self.__locators[locator])

    @TestLogger.log("当前页面是否包含此文本")
    def check_text_exist(self, text):
        """当前页面是否包含此文本"""
        return self.is_text_present(text)

    @TestLogger.log("点击包含文本的元素")
    def click_by_text(self, text):
        """点击文本"""
        return self.click_text(text)

    @TestLogger.log("点击包含文本的元素")
    def input_locator_text(self, locator, text):
        """输入文本"""
        return self.input_text(self.__locators[locator], text)

    @TestLogger.log("点击包含文本的第一个元素")
    def click_tag_text_first_element(self, text):
        elements_list = self.get_elements(self.__locators['通话类型标签'])
        text_list = [i.text for i in elements_list]
        for index, value in enumerate(text_list):
            if value == '[' + text + ']':
                element_first = elements_list[index]
                element_first.click()
                return
        raise AssertionError("没有找到对应的标签--{}".format(text))

    @TestLogger.log("点击包含文本的第一个详细信息(i)元素")
    def click_tag_detail_first_element(self, text):
        elements_list = self.get_elements(self.__locators['通话类型标签'])
        detail_list = self.get_elements(self.__locators['联系人_详情图标'])
        text_list = [i.text for i in elements_list]
        for index, value in enumerate(text_list):
            if value == '[' + text + ']':
                element_first = detail_list[index]
                element_first.click()
                return
        raise AssertionError("没有找到对应的标签--{}".format(text))

    @TestLogger.log("长按包含文本的第一个通话记录元素")
    def press_tag_detail_first_element(self, text):
        elements_list = self.get_elements(self.__locators['通话类型标签'])
        text_list = [i.text for i in elements_list]
        for index, value in enumerate(text_list):
            if value == '[' + text + ']':
                element_first = elements_list[index]
                self.press(element_first)
                return

    @TestLogger.log('拨打并挂断一个点对点语音通话')
    def point2point_voice_call(self):
        self.click_locator_key('拨号键盘')
        self.input_text(self.__locators['拨叫号码'], '10086')
        self.click_locator_key('拨号界面_呼叫')
        import time
        time.sleep(1)
        print(self.get_elements(("id", 'com.cmic.college:id/bt_open')))
        if len(self.get_elements(("id", 'com.cmic.college:id/bt_open'))) > 0:
            self.click_element(("id", 'com.cmic.college:id/bt_open'))
        self.wait_until(condition=lambda x: self.is_text_present('飞信电话'), timeout=30)
        self.click_locator_key('拨号界面_挂断')

    @TestLogger.log('拨打并挂断一个点对点视频通话')
    def point2point_vedio_call(self):
        self.click_locator_key('+')
        self.click_locator_key('视频通话')
        self.click_locator_key('视频通话_第一个联系人')
        time.sleep(0.5)
        if self.is_toast_exist('不能选择本机号码', timeout=8):
            self.click_locator_key('视频通话_第二个联系人')
        self.click_locator_key('呼叫')
        time.sleep(1)
        if self.on_this_page_common('无密友圈_提示文本'):
            self.click_locator_key('无密友圈_取消')
        time.sleep(1)
        if self.on_this_page_common('挂断'):
            self.click_locator_key('挂断')

    @TestLogger.log('拨打并挂断一个多方视频通话')
    def multiplayer_vedio_call(self):
        self.click_locator_key('+')
        self.click_locator_key('视频通话')
        self.click_locator_key('视频通话_第一个联系人')
        self.click_locator_key('视频通话_第二个联系人')
        self.click_locator_key('视频通话_第三个联系人')
        self.click_locator_key('呼叫')
        time.sleep(1)
        if self.is_text_present('您的手机没有授予悬浮窗权限，请开启后再试') and self.is_text_present(
                '暂不开启') and self.is_text_present('现在去开启'):
            self.click_text('暂不开启')
        time.sleep(2)
        if self.on_this_page_common('挂断_多方通话'):
            self.click_locator_key('挂断_多方通话')
            self.click_locator_key('挂断_多方通话_确定')
        if self.on_this_page_common('多方通话_返回'):
            self.click_locator_key('多方通话_返回')

    @TestLogger.log('确保页面有点对点视频的记录')
    def make_sure_have_p2p_vedio_record(self):
        if self.is_text_present('视频通话'):
            return
        self.point2point_vedio_call()
        self.wait_until(
            condition=lambda d: self.is_text_present("视频通话"),
            timeout=8,
        )

    @TestLogger.log('确保页面有多方视频的记录')
    def make_sure_have_multiplayer_vedio_record(self):
        if self.is_text_present('多方视频'):
            return
        self.multiplayer_vedio_call()
        self.wait_until(
            condition=lambda d: self.is_text_present("多方视频"),
            timeout=8,
        )

    @TestLogger.log('确保页面有点对点通话的记录')
    def make_sure_have_p2p_voicecall_record(self):
        if self.is_text_present('飞信电话'):
            return
        self.point2point_voice_call()
        self.wait_until(
            condition=lambda d: self.is_text_present("飞信电话"),
            timeout=8,
        )

    @TestLogger.log('检查是否在点对点通话页面')
    def check_p2p_vedio_call_page(self):
        el = self.get_elements(self.__locators['挂断'])
        if len(el) > 0 or self.is_toast_exist('对方未接听，请稍候再尝试'):
            return True
        return False

    @TestLogger.log('检查是否在多方通话页面')
    def check_multiplayer_call_page(self):
        el = self.get_elements(self.__locators['多人_挂断'])
        return len(el) > 0

    @TestLogger.log('检查是否在消息页面')
    def check_message_page(self):
        el = self.get_elements(self.__locators['信息_聊天框'])
        return len(el) > 0

    @TestLogger.log("清除全部通话记录")
    def click_tag_text_delete_all_record(self, text):
        elements_list = self.get_elements(self.__locators['通话类型标签'])
        text_list = [i.text for i in elements_list]
        for index, value in enumerate(text_list):
            if value == '[' + text + ']':
                element_first = elements_list[index]
                self.press(element_first)
                self.click_text('清除全部通话记录')
                self.click_element((MobileBy.ID, 'com.cmic.college:id/btnConfirm'))
                return

    @TestLogger.log("删除包含文本的第一个通话记录")
    def check_delete_text_first_element(self, text):
        elements_list = self.get_elements(self.__locators['通话类型标签'])
        text_list = [i.text for i in elements_list]
        for index, value in enumerate(text_list):
            if value == '[' + text + ']':
                element_first = elements_list[index]
                self.press(element_first)
                self.click_text('删除该通话记录')
                elements_check_list = self.get_elements(self.__locators['通话类型标签'])
                return element_first not in elements_check_list
        raise AssertionError("没有找到对应的标签--{}".format(text))

    @TestLogger.log("检查是否有联系人")
    def check_is_have_friend(self):
        self.click_locator_key('视频')
        el = self.wait_until(condition=lambda x: self.get_elements(self.__locators['视频通话_第一个联系人']), timeout=10)
        if len(el) > 0:
            self.click_locator_key('多方通话_返回')
        else:
            raise AssertionError("通讯录没有密友")

    @TestLogger.log("检查点对点视频通话详细页")
    def check_vedio_call_detail_page(self):
        for locator in [self.__locators['详情_信息按钮'], self.__locators['详情_视频按钮'], self.__locators['详情_返回']]:
            if not self._is_enabled(locator):
                return "检查点[%s]未通过" % locator
        # 头像  名字  通话时间  通话类型
        locator_list = [("id", 'com.cmic.college:id/ivAvatar'), ("id", 'com.cmic.college:id/tvName'),
                        ("id", 'com.cmic.college:id/tvCallTime'), ("id", 'com.cmic.college:id/tvCallType')]
        for locator in locator_list:
            if not self._is_visible(locator):
                l = locator[-1]
                if l == 'com.cmic.college:id/ivAvatar':
                    locator = '详情_头像'
                elif l == 'com.cmic.college:id/tvName':
                    locator = '详情_名字'
                elif l == 'com.cmic.college:id/tvCallTime':
                    locator = '详情_通话时间'
                elif l == 'com.cmic.college:id/tvCallType':
                    locator = '详情_通话类型'
                else:
                    locator = '未知错误'
                return "检查点[%s]未通过" % locator
        if '通话记录 (视频通话)' != self.get_text(("id", 'com.cmic.college:id/tvCallRecordsType')):
            return "检查点[通话记录 (视频通话)]未通过"
        if len(self.get_elements(("id", 'com.cmic.college:id/tvCallDuration'))) > 0:
            if not self._is_visible(("id", 'com.cmic.college:id/tvCallDuration')):  # 通话时长
                return "检查点[通话时长]未通过"
        return True

    @TestLogger.log("检查多方视频详细页")
    def check_multiplayer_vedio_detail_page(self):
        if not self._is_enabled(self.__locators['多方通话_返回']):
            return False
        # 头像  名字  通话时间  通话类型
        locator_list = [("id", 'com.cmic.college:id/ivAvatar'), ("id", 'com.cmic.college:id/tvName'),
                        ("id", 'com.cmic.college:id/tvCallTime'), ("id", 'com.cmic.college:id/tvCallType')]
        for locator in locator_list:
            if not self._is_visible(locator):
                return False
        if '通话记录 (多方视频)' != self.get_text(("id", 'com.cmic.college:id/tvCallRecordsType')):
            return False
        if len(self.get_elements(("id", 'com.cmic.college:id/tvCallDuration'))) > 0:
            if not self._is_visible(("id", 'com.cmic.college:id/tvCallDuration')):  # 通话时长
                return False
        return True

    @TestLogger.log("检查视频页面显示")
    def check_vedio_page(self):
        for locator in [self.__locators['多方通话_返回'], self.__locators['呼叫']]:
            if not self._is_enabled(locator):
                return
        # 联系人  快速定位
        locator_list = [("id", 'com.cmic.college:id/contact_selection_list_view'),
                        ("id", 'com.cmic.college:id/contact_index_bar_view')]
        for locator in locator_list:
            if not self._is_visible(locator):
                return
        return True

    @TestLogger.log("截图")
    def take_screen_out(self):
        import os
        import time
        path = os.getcwd() + "/screenshot"
        print(path)
        timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        if not os.path.isdir(os.getcwd() + "/screenshot"):
            os.makedirs(path)
        self.driver.get_screenshot_as_file(path + "/" + timestamp + ".png")

    @TestLogger.log("获得元素的文本")
    def get_element_text(self, locator):
        return self.get_text(self.__locators[locator])

    @TestLogger.log("获得元素对应的数量")
    def get_elements_count(self, locator):
        return self.get_elements(self.__locators[locator])

    @TestLogger.log("页面应该包含元素")
    def page_contain_element(self, locator):
        self.page_should_contain_element(self.__locators[locator])

    @TestLogger.log("判断页面元素是否存在")
    def is_element_present(self, locator):
        return self._is_element_present(self.__locators[locator])

    @TestLogger.log("页面应该包含元素")
    def click_keyboard(self):
        self.click_element(self.__locators['拨号键盘'])

    @TestLogger.log("点击键盘输入框")
    def click_keyboard_input_box(self):
        self.click_element(self.__locators['键盘输入框'])

    @TestLogger.log("键盘输入框输入文本")
    def input_text_in_input_box(self, text):
        self.input_text(self.__locators['键盘输入框'], text)

    @TestLogger.log("获取输入框文本")
    def get_input_box_text(self, ):
        return self.get_element(self.__class__.__locators['键盘输入框']).text

    @TestLogger.log("点击收起键盘")
    def click_hide_keyboard(self):
        self.click_element(self.__class__.__locators['收起键盘'])

    @TestLogger.log("点击打开键盘")
    def click_show_keyboard(self):
        self.click_element(self.__class__.__locators['拨号键盘'])

    @TestLogger.log("点击+")
    def click_add(self):
        self.click_element(self.__class__.__locators['+'])

    @TestLogger.log()
    def close_ad(self):

        if self._is_element_present('关闭广告'):
            self.click_element('关闭广告')
        return

    @TestLogger.log('是否在拨号界面')
    def is_exist_call_key(self):
        el = self.get_elements(self.__locators['拨号界面_呼叫'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log('是否在通话记录详情页面')
    def on_this_page_call_detail(self):
        """是否在通话记录详情页面"""
        el = self.get_elements(self.__locators['详情_通话'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log("点击详情页返回")
    def click_detail_back(self):
        self.click_element(self.__class__.__locators['详情_返回'])

    @TestLogger.log("修改备注")
    def click_modify_nickname(self):
        self.click_element(self.__class__.__locators['详情_>'])

    @TestLogger.log('等待页面自动跳转')
    def wait_for_page_modify_nickname(self, max_wait_time=30):
        self.wait_until(
            condition=lambda d: self.is_text_present("修改备注名"),
            timeout=max_wait_time,
        )

    @TestLogger.log("点击备注输入框")
    def click_nickname_input_box(self):
        self.click_element(self.__locators['备注'])

    @TestLogger.log("备注输入框输入文本")
    def input_text_in_nickname(self, text):
        self.input_text(self.__locators['备注_备注'], text)
        # self.input_text(self.__locators[locator], text)

    @TestLogger.log("保存备注")
    def click_save_nickname(self, ):
        return self.click_element(self.__locators['备注_保存'])

    @TestLogger.log("获取备注")
    def get_nickname(self):
        return self.get_element(self.__class__.__locators['详情_备注内容']).text

    @TestLogger.log('清空文本框内容')
    def edit_clear(self):
        locator = self.get_element(self.__class__.__locators['备注']).text
        self.click_element(self.__locators['备注'])
        #     123代表光标移动到末尾
        self.driver.keyevent(123)
        for i in range(0, len(locator)):
            # 67退格键
            self.driver.keyevent(67)

    @TestLogger.log('是否有流量优惠界面')
    def on_this_page_flow(self):
        """是否在流量优惠界面页面"""
        el = self.get_elements(self.__locators['流量_提示内容'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log('设置不再提醒为选中')
    def set_not_reminders(self):
        """设置不再提醒为选中"""
        el = self.get_elements(self.__locators['流量_不再提醒'])[0].get_attribute('checked')
        if 'false' == el:
            self.click_element(self.__locators['流量_不再提醒'])
            el = self.get_elements(self.__locators['流量_不再提醒'])[0].get_attribute('checked')
            if 'true' == el:
                return True
        return False

    @TestLogger.log('是否在某个页面')
    def on_this_page_common(self, locator):
        """是否在某个页面"""
        try:
            el = self.get_elements(self.__locators[locator])
            if len(el) > 0:
                return True
            return False
        except:
            return False
