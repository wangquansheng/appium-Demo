from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage


class MessagePage(FooterPage):
    """消息页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        '+': (MobileBy.ID, 'com.cmic.college:id/action_add_sms'),
        '搜索': (MobileBy.ID, 'com.cmic.college:id/action_search'),
        '免流量,无限畅聊': (MobileBy.ID, 'com.cmic.college:id/tv_empty'),
        '视频': (MobileBy.ID, 'com.cmic.college:id/ivMultipartyCall'),
        '聊天标志': (MobileBy.ID, 'com.cmic.college:id/action_setting'),
        '选择照片': (MobileBy.ID, 'com.cmic.college:id/ib_pic'),
        '选择照相': (MobileBy.ID, 'com.cmic.college:id/ib_take_photo'),
        '选择卡卷': (MobileBy.ID, 'com.cmic.college:id/ib_redpaper'),
        '选择文件': (MobileBy.ID, 'com.cmic.college:id/ib_file'),
        # 打开“+”
        '新建消息': (MobileBy.XPATH, '//*[contains(@text,"新建消息")]'),
        '发起群聊': (MobileBy.XPATH, '//*[contains(@text,"发起群聊")]'),
        '添加密友': (MobileBy.XPATH, '//*[contains(@text,"添加密友")]'),
        '扫一扫': (MobileBy.XPATH, '//*[contains(@text,"扫一扫")]'),
        # 聊天设置页面
        '录音': (MobileBy.ID, 'com.cmic.college:id/ib_audio'),
        '开始录音': (MobileBy.ID, 'com.cmic.college:id/record_audio'),
        '取消录音': (MobileBy.ID, 'com.cmic.college:id/image_cancel'),
    }

    @TestLogger.log('点击+')
    def click_add(self):
        self.click_element(self.__locators['+'])

    @TestLogger.log('点击+消息')
    def click_add_message(self):
        self.click_element(self.__locators['新建消息'])

    @TestLogger.log('等待消息页面自动跳转')
    def wait_for_page_message(self, max_wait_time=8):
        self.wait_until(
            condition=lambda d: self._is_element_present(self.__locators["+"]),
            timeout=max_wait_time,
        )

    @TestLogger.log('是否在消息页面')
    def is_on_this_page(self):
        el = self.get_elements(self.__locators['+'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log('等待聊天消息页面自动跳转')
    def wait_for_page_chart_message(self, timeout=20):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["聊天标志"]),
                timeout=timeout,
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log('点击录音按钮')
    def click_record_audio(self):
        self.click_element(self.__locators['录音'])

    @TestLogger.log('长按开始录音')
    def long_click_record_audio(self, time=3000, wait_time=1):
        self.press(self.get_element(self.__locators["开始录音"]), time, wait_time)

    @TestLogger.log('点击开始录音')
    def click_start_record_audio(self):
        self.click_element(self.__locators["开始录音"])

    @TestLogger.log('判断是否又取消录音')
    def is_exist_cancel_audio(self, timeout=8):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators["取消录音"]),
                timeout=timeout,
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log("按住元素滑动到另一个元素")
    def press_and_move_to_el(self, locator1, locator2):
        """按住并滑动"""
        element1 = self.get_element(self.__locators[locator1])
        TouchAction(self.driver).long_press(element1).move_to(self.get_element(self.__locators[locator2])).wait(
            2).release().perform()

    @TestLogger.log('点击选择照片')
    def click_pic(self):
        self.click_element(self.__locators['选择照片'])
