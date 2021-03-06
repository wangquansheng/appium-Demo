import time
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChartSettingPage(BasePage):
    """群聊-设置页面_"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'
    __locators = {
        '返回': (MobileBy.XPATH, '//*[@content-desc="转到上一层级"]'),
        '聊天设置': (MobileBy.XPATH, '//*[@text="聊天设置"]'),
        '群管理': (MobileBy.XPATH, '//*[@text="群管理"]'),
        '群二维码': (MobileBy.XPATH, '//*[@text="群二维码"]'),
        '删除并退出': (MobileBy.ID, 'com.cmic.college:id/delete_and_exit'),
        '邀请微信或者QQ好友进群': (MobileBy.ID, 'com.cmic.college:id/rltGroupPassword'),
        '群成员': (MobileBy.ID, 'com.cmic.college:id/member_count'),
        '我在本群的昵称': (MobileBy.ID, 'com.cmic.college:id/group_name'),
        # 打开群管理入口
        '转让群': (MobileBy.XPATH, '//*[@text="转让群"]'),
        '解散群': (MobileBy.XPATH, '//*[@text="解散群"]'),
        # 打开邀请微信或者QQ好友进群
        '分享口令邀请好友进群': (MobileBy.ID, 'com.cmic.college:id/tvTitle'),
        '分享口令': (MobileBy.ID, 'com.cmic.college:id/btnShare'),
        '分享口令1': (MobileBy.XPATH, '//*[@text="分享口令"]'),
        '不分享口令1': (MobileBy.XPATH, '//*[@text="不分享了"]'),
        # 弹框确定与取消
        '解散群后': (MobileBy.XPATH, '//*[contains(@text, "解散群后")]'),
        # 弹框确定与取消
        '确定': (MobileBy.XPATH, '//*[@text="确定"]'),
        '取消': (MobileBy.XPATH, '//*[@text="取消"]'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('等待群设置页面跳转')
    def wait_for_page_group_chart_setting(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["邀请微信或者QQ好友进群"]),
                timeout=timeout,
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log('等待分享口令弹框跳转')
    def wait_for_page_group_chart_setting_share(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["分享口令"]),
                timeout=timeout,
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log('点击邀请微信进群')
    def click_invite(self):
        self.click_element(self.__locators['邀请微信或者QQ好友进群'])

    @TestLogger.log('点击删除并退出')
    def click_delete_group(self):
        self.click_element(self.__locators['删除并退出'])

    @TestLogger.log('点击确定')
    def click_delete_group_sure(self):
        self.click_element(self.__locators['确定'])

    @TestLogger.log('点击取消')
    def click_delete_group_cancel(self):
        self.click_element(self.__locators['取消'])

    @TestLogger.log('点击不分享口令1')
    def click_not_share(self):
        self.click_element(self.__locators['不分享口令1'])

    @TestLogger.log('点击群管理')
    def click_manager_group(self):
        self.click_element(self.__locators['群管理'])

    @TestLogger.log('点击转让群')
    def click_transfer_group(self):
        self.click_element(self.__locators['转让群'])

    @TestLogger.log('点击解散群')
    def click_cancel_group(self):
        self.click_element(self.__locators['解散群'])

    @TestLogger.log('点击群成员')
    def click_group_member(self):
        self.click_element(self.__locators['群成员'])

    def click_group_code(self):
        self.click_element(self.__locators['群二维码'])

    @TestLogger.log('等待解散群弹框跳转')
    def wait_for_page_group_chart_cancel(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["解散群后"]),
                timeout=timeout,
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log('获取群聊名称')
    def get_group_chart_name(self):
        return self.get_element(self.__locators["我在本群的昵称"]).text
