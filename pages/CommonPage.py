from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from library.core.utils.applicationcache import current_mobile
import time
import traceback


# noinspection PyBroadException,PyIncorrectDocstring,PyUnresolvedReferences
class CommonPage(BasePage):
    """通用的方法"""
    ACTIVITY = ''

    def get_locators(self, locator):
        return self.__class__.get_locators(self, locator)

    @TestLogger.log('点击始终允许')
    def click_always_allow_c(self):
        """权限框-点击始终允许"""
        while self.is_text_present('始终允许'):
            self.click_text('始终允许')
            time.sleep(1)

    @TestLogger.log('去除遮罩')
    def remove_mask_c(self, num=2):
        """
        去除遮罩
        :param num:遮罩层数
        :return:
        """
        for i in range(num):
            self.tap_coordinate([(100, 100), (100, 110), (100, 120)])
            time.sleep(1)

    @TestLogger.log("您的手机没有授予悬浮窗权限，请开启后再试")
    def close_suspension_c(self):
        """您的手机没有授予悬浮窗权限，请开启后再试"""
        while self.is_text_present('悬浮窗权限') and self.is_text_present(
                '暂不开启'):
            self.click_text('暂不开启')

    @TestLogger.log('等待页面加载完毕')
    def wait_for_page_c(self, text='', locator=None, max_wait_time=30):
        """
        等待页面打开
        :param text: 等待出现的文本
        :param locator: 等待出现的标签
        :param max_wait_time:
        :return:
        """
        self.wait_until(
            condition=lambda d: (self.is_text_present(text) or self.is_element_already_exist_c(locator)),
            timeout=max_wait_time,
        )

    @TestLogger.log("点击locators对应的元素")
    def click_locator_key_c(self, locator):
        self.click_element(self.__class__.get_locators(self, locator))

    @TestLogger.log("输入文本")
    def input_text_c(self, locator, text):
        """输入文本"""
        return self.input_text(self.__class__.get_locators(self, locator), text)

    @TestLogger.log("点击包含文本的第一个元素")
    def click_tag_text_first_element_c(self, locator, text):
        elements_list = self.get_elements(self.__class__.get_locators(self, locator))
        text_list = [i.text for i in elements_list]
        for index, value in enumerate(text_list):
            if value == '[' + text + ']':
                element_first = elements_list[index]
                element_first.click()
                return
        raise AssertionError("没有找到对应的标签--{}".format(text))

    @TestLogger.log("长按包含文本的第一个元素")
    def press_tag_detail_first_element_c(self, locator, text):
        elements_list = self.get_elements(self.__class__.get_locators(self, locator))
        text_list = [i.text for i in elements_list]
        for index, value in enumerate(text_list):
            if value == '[' + text + ']':
                element_first = elements_list[index]
                self.press(element_first)
                return

    @TestLogger.log("截图")
    def take_screen_out_c(self):
        import os
        import time
        path = os.getcwd() + "/screenshot"
        print(path)
        timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        if not os.path.isdir(os.getcwd() + "/screenshot"):
            os.makedirs(path)
        self.driver.get_screenshot_as_file(path + "/" + timestamp + ".png")

    @TestLogger.log("获得元素的文本")
    def get_element_text_c(self, locator):
        return self.get_text(self.__class__.get_locators(self, locator))

    @TestLogger.log("获得元素对应的数量")
    def get_elements_count_c(self, locator):
        return len(self.get_elements(self.__class__.get_locators(self, locator)))

    @TestLogger.log("获得元素对应的数量")
    def get_elements_list_c(self, locator):
        return self.get_elements(self.__class__.get_locators(self, locator))

    @TestLogger.log("点击键盘输入框")
    def click_keyboard_input_box(self, locator):
        self.click_element(self.__class__.get_locators(self, locator))

    # @TestLogger.log("键盘输入框输入文本")
    # def input_text_in_input_box_c(self, locator, text):
    #     self.input_text(self.__class__.get_locators(self, locator), text)

    @TestLogger.log("获取输入框文本")
    def get_elements_text_c(self, locator):
        return self.get_elements(self.__class__.get_locators(self, locator))[0].text

    @TestLogger.log('清空文本框内容')
    def edit_clear_c(self, locator):
        self.get_element(self.__class__.get_locators(self, locator)).clear()

    def get_check_box_status_c(self, locator):
        return self.get_element(self.__class__.get_locators(self, locator)).get_attribute('checked')

    @TestLogger.log('设置复选框为选中')
    def set_checkbox_checked_c(self, locator):
        """设置复选框为选中"""
        el = self.get_elements(self.__class__.get_locators(self, locator))[0].get_attribute('checked')
        if 'false' == el:
            self.click_element(self.__class__.get_locators(self, locator))
            el = self.get_elements(self.__class__.get_locators(self, locator))[0].get_attribute('checked')
            if 'true' == el:
                return True
        return False

    @TestLogger.log('设置复选框为未选中')
    def set_checkbox_unchecked_c(self, locator):
        """设置复选框为未选中"""
        el = self.get_elements(self.__class__.get_locators(self, locator))[0].get_attribute('checked')
        if 'true' == el:
            self.click_element(self.__class__.get_locators(self, locator))
            el = self.get_elements(self.__class__.get_locators(self, locator))[0].get_attribute('checked')
            if 'false' == el:
                return True
        return False

    @TestLogger.log('获取复选元素的状态')
    def get_checkbox_value_c(self, locator):
        """设置复选框为未选中"""
        return self.get_element(self.__class__.get_locators(self, locator)).get_attribute('checked')

    @TestLogger.log('获取select元素的状态')
    def get_select_value_c(self, locator):
        """设置复选框为未选中"""
        return self.get_element(self.__class__.get_locators(self, locator)).get_attribute('selected')

    @TestLogger.log('获取指定运营商类型的手机卡（不传类型返回全部配置的手机卡）')
    def get_cards_c(self, card_type):
        """返回指定类型卡手机号列表"""
        return current_mobile().get_cards(card_type)

    @TestLogger.log('判断元素是否存在')
    def is_element_already_exist_c(self, locator, default_timeout=5, auto_accept_permission_alert=True):
        """判断元素是否存在"""
        try:
            self.wait_until(
                condition=lambda d: len(self.get_elements(self.__class__.get_locators(self, locator))) > 0,
                timeout=default_timeout,
                auto_accept_permission_alert=auto_accept_permission_alert
            )
            return True
        except Exception:
            return False

    @TestLogger.log('判断元素是否存在')
    def is_text_present_c(self, text, default_timeout=5, auto_accept_permission_alert=True):
        """判断元素是否存在"""
        try:
            self.wait_until(
                condition=lambda d: self.mobile.is_text_present(text),
                timeout=default_timeout,
                auto_accept_permission_alert=auto_accept_permission_alert
            )
            return True
        except Exception:
            return False

    @TestLogger.log('获取元素')
    def get_one_element_c(self, locator):
        return self.mobile.get_element(self.__class__.get_locators(self, locator))

    @TestLogger.log('获取所有元素')
    def get_some_elements_c(self, locator):
        return self.mobile.get_elements(self.__class__.get_locators(self, locator))

    @TestLogger.log('模拟三指点击屏幕')
    def tap_screen_three_point_c(self):
        """模拟三指点击屏幕"""
        self.tap_coordinate([(100, 100), (100, 110), (100, 120)])
        time.sleep(1)

    @TestLogger.log('模拟三指点击屏幕')
    def tap_screen_center_c(self, locator):
        """模拟点击元素中心"""
        element = self.get_element(self.__class__.get_locators(self, locator))
        rect = element.rect
        point_x = int(rect["x"]) + int(rect["width"]) / 2
        point_y = int(rect["y"]) + int(rect["height"]) / 2
        self.tap_coordinate([(point_x, point_y)])

    @TestLogger.log('模拟三指点击屏幕')
    def tap_screen_three_point_element_c(self, locator):
        """根据元素模拟三指点击屏幕"""
        if not self.is_element_already_exist_c(locator, default_timeout=1):
            self.tap_coordinate([(100, 100), (100, 110), (100, 120)])
            time.sleep(1)

    @TestLogger.log("按住并向下滑动")
    def press_move_to_down_c(self, locator):
        self.press_and_move_to_down(self.__class__.get_locators(self, locator))

    @TestLogger.log("在元素内滑动")
    def swipe_direction_c(self, locator, direction):
        """
        在元素内滑动
        :param locator: 定位器
        :param direction: 方向（left,right,up,down）
        :param duration: 持续时间ms
        :return:
        """
        self.swipe_by_direction(self.__class__.get_locators(self, locator), direction)

    @TestLogger.log('长按元素')
    def press_element_c(self, locator, times=3000, wait_time=1):
        """长按元素"""
        el = self.get_element(self.__class__.get_locators(self, locator))
        self.press(el, times, wait_time)

    @TestLogger.log('按住并向上滑动')
    def press_and_move_to_up_c(self, locator):
        """按住并向上滑动"""
        self.press_and_move_to_down(self.__class__.get_locators(self, locator))

    @TestLogger.log('按住并向下滑动')
    def press_and_move_to_down_c(self, locator):
        """按住并向下滑动"""
        self.press_and_move_to_down(self.__class__.get_locators(self, locator))
