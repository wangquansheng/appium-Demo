from appium.webdriver.common.mobileby import MobileBy

from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage
import time


class ContactsPage(FooterPage):
    """通讯录页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        #权限框
        '取消': (MobileBy.ID, 'com.cmic.college:id/btnCancel'),
        '去开通': (MobileBy.ID, 'com.cmic.college:id/btnConfirm'),
        '遮罩1': (MobileBy.ID, 'com.cmic.college:id/contact_list'),
        #通讯录首页
        '搜索': (MobileBy.ID, 'com.cmic.college:id/action_search'),
        '消息': (MobileBy.ID, 'com.cmic.college:id/action_message'),
        '不限时长-去开通': (MobileBy.ID, 'com.cmic.college:id/tv_open'),
        '联系人名称': (MobileBy.ID, 'com.cmic.college:id/contact_name'),
        '联系人号码': (MobileBy.ID, 'com.cmic.college:id/contact_phone'),
        '电话图标': (MobileBy.ID, 'com.cmic.college:id/rl_call'),

        }

    @TestLogger.log()
    def permission_box_processing(self):
        """权限框处理"""
        time.sleep(1)
        if self.is_text_present('开通不限时长电话'):
            self.click_element(self.__class__.__locators['取消'])
