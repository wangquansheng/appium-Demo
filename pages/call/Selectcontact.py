from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage
import time


class Selectcontactpage(FooterPage):
    """选择联系人页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {
        '返回': (MobileBy.ID, ''),
        '标题栏': (MobileBy.ID, ''),
        '搜索框': (MobileBy.ID, 'com.cmic.college:id/editText_keyword'),
        '呼叫': (MobileBy.ID, 'com.cmic.college:id/tv_sure'),
        '联系人姓名': (MobileBy.ID, 'com.cmic.college:id/contact_name'),
        '联系人电话': (MobileBy.ID, 'com.cmic.college:id/contact_number'),
        '联系人头像': (MobileBy.ID, 'com.cmic.college: id / contact_icon'),
        '右侧字母列表': (MobileBy.ID, 'com.cmic.college:id/contact_index_bar_container'),

    }