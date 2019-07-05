from appium.webdriver.common.mobileby import MobileBy

from library.core.TestLogger import TestLogger
from pages.CommonPage import CommonPage
import time
import traceback

# noinspection PyBroadException
class ContactsPage(CommonPage):
    """通讯录页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        # 权限框
        '取消': (MobileBy.ID, 'com.cmic.college:id/btnCancel'),
        '去开通': (MobileBy.ID, 'com.cmic.college:id/btnConfirm'),
        '遮罩1': (MobileBy.ID, 'com.cmic.college:id/contact_list'),
        # 通讯录首页
        '搜索': (MobileBy.ID, 'com.cmic.college:id/action_search'),
        '搜索_返回': (MobileBy.ID, 'com.cmic.college:id/iv_back'),
        '搜索_搜索框': (MobileBy.ID, 'com.cmic.college:id/edit_query'),
        '搜索_清空': (MobileBy.ID, 'com.cmic.college:id/iv_delect'),
        '搜索_联系人号码': (MobileBy.ID, 'com.cmic.college:id/tv_phone'),
        '消息': (MobileBy.ID, 'com.cmic.college:id/action_message'),
        '不限时长-去开通': (MobileBy.ID, 'com.cmic.college:id/tv_open'),
        '联系人名称': (MobileBy.ID, 'com.cmic.college:id/contact_name'),
        '联系人号码': (MobileBy.ID, 'com.cmic.college:id/contact_phone'),
        '电话图标': (MobileBy.ID, 'com.cmic.college:id/rl_call'),
        # title
        '通讯录_标题': (MobileBy.XPATH, '//android.widget.RelativeLayout[@resource-id="com.'
                                   'cmic.college:id/rl_toolbar"]/android.widget.TextView[1]'),
        # 家庭网
        '家庭网_展开_收起': (MobileBy.ID, 'com.cmic.college:id/iv_arrow'),
        '家庭网_管理': (MobileBy.XPATH, '//android.widget.LinearLayout[@resource-id="com.cmic.'
                                   'college:id/ll_manage"]/android.widget.TextView[1]'),
        '家庭网_感叹号': (MobileBy.ID, 'com.cmic.college:id/action_rule'),
        '家庭网_添加成员': (MobileBy.ID, 'com.cmic.college:id/rl_add'),
        '家庭网_添加成员_确定': (MobileBy.ID, 'com.cmic.college:id/bt_ok'),
        '家庭网_输入手机号': (MobileBy.ID, 'com.cmic.college:id/edit_number'),
        '家庭网_通讯录': (MobileBy.ID, 'com.cmic.college:id/iv_add'),
        '家庭网_通讯录_搜索框': (MobileBy.ID, 'com.cmic.college:id/editText_keyword'),
        '家庭网_通讯录_号码': (MobileBy.ID, 'com.cmic.college:id/contact_number'),
        # 密友圈（不限时长）
        '密友圈_管理': (MobileBy.ID, 'com.cmic.college:id/tv_manage'),
        '密友圈_添加成员': (MobileBy.ID, 'com.cmic.college:id/iv_add'),
        '密友圈_管理_成员': (MobileBy.ID, 'com.cmic.college:id/rl_root'),
        '密友圈_解绑_确定': (MobileBy.ID, 'com.cmic.college:id/btnConfirm'),
        '密友圈_解绑_取消': (MobileBy.ID, 'com.cmic.college:id/btnCancel'),
        # 联系人详情
        '联系人_头像': (MobileBy.ID, 'com.cmic.college:id/profile_photo'),
        '联系人_备注': (MobileBy.ID, 'com.cmic.college:id/profile_name'),
        '联系人_电话': (MobileBy.ID, 'com.cmic.college:id/my_profile_call'),
        '联系人_视频': (MobileBy.ID, 'com.cmic.college:id/my_profile_video'),
        '联系人_添加桌面': (MobileBy.ID, 'com.cmic.college:id/my_profile_desk'),
        '联系人_备注名': (MobileBy.ID, 'com.cmic.college:id/nick_name'),
        '联系人_备注内容': (MobileBy.ID, 'com.cmic.college:id/tv_nickset'),
        '联系人_备注修改': (MobileBy.XPATH, '//android.widget.RelativeLayout[@resource-id="com.'
                                     'cmic.college:id/rl_nick_name"]/android.widget.ImageView[1]'),
        '联系人_归属地': (MobileBy.ID, 'com.cmic.college:id/tv_phone_location'),
        '联系人_长号': (MobileBy.ID, 'com.cmic.college:id/tv_phone_number'),
        '联系人_短号标签': (MobileBy.ID, 'com.cmic.college:id/tv_short_property'),
        '联系人_短号': (MobileBy.ID, 'com.cmic.college:id/tv_short_value'),
        '联系人_更多': (MobileBy.ID, 'com.cmic.college:id/tv_more'),
        '联系人_更多编辑': (MobileBy.ID, 'com.cmic.college:id/tv_more'),
        '联系人_规则': (MobileBy.ID, 'com.cmic.college:id/tv_freecall_rule'),
        '联系人_规则说明': (MobileBy.ID, 'com.cmic.college:id/tv_title_actionbar'),
        '联系人_规则返回': (MobileBy.ID, 'com.cmic.college:id/ibt_back_actionbar'),
        '联系人_联系人': (MobileBy.ID, 'com.cmic.college:id/rl_content'),
        # 更多页面
        '更多_性别_标签': (MobileBy.ID, 'com.cmic.college:id/tv_sex_title'),
        '更多_年龄_标签': (MobileBy.ID, 'com.cmic.college:id/tv_age_title'),
        '更多_职业_标签': (MobileBy.ID, 'com.cmic.college:id/tv_profession_title'),
        '更多_个性_标签': (MobileBy.ID, 'com.cmic.college:id/tv_my_tag_title'),
        # 编辑备注
        '编辑备注_返回': (MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="转到上一层级"]'),
        '编辑备注_输入框': (MobileBy.ID, 'com.cmic.college:id/edit_query'),
        '编辑备注_保存': (MobileBy.ID, 'com.cmic.college:id/nick_name_save'),
        # 拨打电话页面
        '电话页面_状态': (MobileBy.ID, 'com.android.incallui:id/callStateLable'),
        '电话页面_备注': (MobileBy.ID, 'com.android.incallui:id/name'),
        # 拨打视频页面
        '视频页面_状态': (MobileBy.XPATH, '//android.widget.TextView[@text="正在等待对方接听"]'),
        '视频页面_挂断': (MobileBy.ID, 'com.cmic.college:id/video_iv_term'),
        #
        # 流量优惠提示框
        '流量_不再提醒': (MobileBy.ID, 'com.cmic.college:id/select_checkbox'),
        '流量_去开通': (MobileBy.ID, 'com.cmic.college:id/bt_open'),
        '流量_继续拨打': (MobileBy.ID, 'com.cmic.college:id/tv_continue'),
        '流量_提示内容': (MobileBy.ID, 'com.cmic.college:id/content'),
        # 通讯录--密友圈(不限时长)
        '不限时长_联系人组': (MobileBy.XPATH, '//android.support.v7.widget.RecyclerView[@resource-id="com.'
                                      'cmic.college:id/rv_content"]/android.widget.LinearLayout'),
        # 回呼
        '回呼_提示文本': (MobileBy.ID, 'com.cmic.college:id/content'),
        '回呼_不再提醒': (MobileBy.ID, 'com.cmic.college:id/select_checkbox'),
        '回呼_我知道了': (MobileBy.ID, 'com.cmic.college:id/bt_open'),

    }

    @TestLogger.log("getLocators")
    def get_locators(self, locator):
        return self.__locators[locator]

    @TestLogger.log()
    def permission_box_processing(self):
        """权限框处理"""
        time.sleep(1)
        if self.is_text_present('开通不限时长电话'):
            self.click_element(self.__class__.__locators['取消'])

    @TestLogger.log()
    def if_home_net_expand(self) -> bool:
        """判断家庭网是否展开"""
        locator = (
            'xpath', '//android.widget.TextView[@text="联系人"]/../preceding-sibling::android.widget.LinearLayout[1]')
        try:
            return len(self.get_elements(locator)) > 0
        except:
            return False

    @TestLogger.log()
    def if_meet_net_expand(self) -> bool:
        """判断密友圈（不限时长）是否有成员"""
        locator = (
            'xpath', '//android.support.v7.widget.RecyclerView[@resource-id="com.'
                     'cmic.college:id/rv_content"]/android.widget.LinearLayout')
        try:
            return len(self.get_elements(locator)) > 0
        except:
            return False

    @TestLogger.log()
    def click_to_call(self, text):
        """点击指定联系人的电话图标"""
        locator = (
            'xpath', '//*[contains(@text,%s)]/../following-sibling::*[2]' % text)
        try:
            self.get_element(locator).click()
        except Exception:
            traceback.print_exc()
