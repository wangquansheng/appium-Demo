from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage


class NewMessagePage(FooterPage):
    """新建消息页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {
        '返回': (MobileBy.XPATH, '//*[@content-desc="转到上一层级"]'),
        '搜索联系人或手机号': (MobileBy.ID, '	com.cmic.college:id/editText_keyword'),
        '#': (MobileBy.ID, 'com.cmic.college:id/alphabetIndexText'),
        '联系人图标': (MobileBy.ID, 'com.cmic.college:id/contact_icon'),
        '联系人电话': (MobileBy.ID, 'com.cmic.college:id/contact_number'),
        '联系人姓名': (MobileBy.ID, 'com.cmic.college:id/contact_name'),
        # 删除方式弹框提示
        '批量删除': (MobileBy.XPATH, '//*[@text="批量删除"]'),
        '单个删除': (MobileBy.XPATH, '//*[@text="删除群成员"]'),
        # 删除群成员列表页面
        '删除群成员': (MobileBy.XPATH, '//*[@text="删除群成员"]'),
        '删除': (MobileBy.ID, 'com.cmic.college:id/tv_sure'),
        '搜索': (MobileBy.ID, 'com.cmic.college:id/editText_keyword'),
        '已选中': (MobileBy.ID, 'com.cmic.college:id/select_icon'),
        '群定删除群成员': (MobileBy.XPATH, '//*[contains(@text,"群定删除群成员"]'),
        # 弹框确定与取消
        '确定': (MobileBy.XPATH, '//*[@text="确定"]'),
        '取消': (MobileBy.XPATH, '//*[@text="取消"]'),

    }

    @TestLogger.log('点击通话引导页')
    def click_contact_one(self, n=1):
        els = self.get_elements(self.__locators["联系人姓名"])
        if n > len(els):
            raise AssertionError("暂无联系人，请添加")
        for i in range(n):
            els[i].click()

    @TestLogger.log('等待页面自动跳转')
    def wait_for_page_new_message(self, max_wait_time=8):
        self.wait_until(
            condition=lambda d: self.is_text_present("搜索联系人或手机号"),
            timeout=max_wait_time,
        )

    @TestLogger.log('是否在通话页面')
    def is_on_this_page(self):
        el = self.get_elements(self.__locators['搜索联系人或手机号'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log('长按列表姓名')
    def press_long(self):
        els = self.get_elements(self.__locators["联系人姓名"])
        el = els[0]
        self.press(el)

    @TestLogger.log('长按列表姓名')
    def click_delete_member(self):
        self.click_element(self.__locators["批量删除"])

    @TestLogger.log('获取删除按钮状态')
    def get_delete_button(self):
        return self._is_enabled(self.__locators["删除"])

    @TestLogger.log('等待页面自动跳转')
    def wait_for_page_delete_member(self, max_wait_time=8):
        self.wait_until(
            condition=lambda d: self.is_text_present("删除群成员"),
            timeout=max_wait_time,
        )

    @TestLogger.log('获取删除按钮状态')
    def page_contain_ele(self):
        return self._is_element_present(self.__locators["已选中"])

    @TestLogger.log('等待二次确定删除自动跳转')
    def wait_for_page_delete_member_again(self, max_wait_time=8):
        try:
            self.wait_until(
                condition=lambda d: self.is_text_present("确定删除群成员"),
                timeout=max_wait_time,
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(max_wait_time))
            raise AssertionError(message)

    @TestLogger.log('点击删除')
    def click_delete_button(self):
        self.click_element(self.__locators["删除"])

    @TestLogger.log('点击确定')
    def click_delete_member_sure(self):
        self.click_element(self.__locators["确定"])

    @TestLogger.log('点击取消')
    def click_delete_member_cancel(self):
        self.click_element(self.__locators["取消"])

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators["返回"])

    @TestLogger.log('点击通话引导页')
    def get_contact_one(self):
        els = self.get_elements(self.__locators["联系人姓名"])
        el = els[0]
        return el.text
