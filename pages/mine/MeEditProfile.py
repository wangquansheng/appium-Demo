from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import uuid


class MeEditProfilePage(BasePage):
    """我-》查看个人资料"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.UserProfileShowActivity'

    __locators = {'': (MobileBy.ID, ''),
                  '个人头像': (MobileBy.ID, 'com.cmic.college:id/profile_photo'),
                  '电话': (MobileBy.ID, 'com.cmic.college:id/phone'),
                  '昵称': (MobileBy.ID, 'com.cmic.college:id/name'),
                  '性别': (MobileBy.ID, 'com.cmic.college:id/rltGender'),
                  '年龄': (MobileBy.ID, 'com.cmic.college:id/rltAgeGroup'),
                  '我的标签': (MobileBy.ID, 'com.cmic.college:id/rltTag'),
                  '职业': (MobileBy.ID, 'com.cmic.college:id/rltProfession'),
                  '返回': (MobileBy.ID, 'com.cmic.college:id/left_back'),
                  '保存': (MobileBy.ID, "com.cmic.college:id/proflie_save"),

                  '弹框取消': (MobileBy.ID, "com.cmic.college:id/btnCancel"),
                  '弹框保存': (MobileBy.ID, "com.cmic.college:id/btnConfirm"),

                  '头像更多': (MobileBy.ID, 'com.cmic.college:id/action_more'),
                  '头像页面返回': (MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="转到上一层级"]'),
                  '从手机相册选择': (MobileBy.XPATH,
                              '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ListView/android.widget.LinearLayout[1]'),
                  '保存到手机': (MobileBy.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ListView/android.widget.LinearLayout[2]'),

                  '性别_男': (MobileBy.XPATH,
                           '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]'),
                  '年龄_90后': (MobileBy.XPATH,
                             '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[3]/android.widget.TextView'),
                  '职业_计算机': (MobileBy.XPATH,
                             '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]'),
                  '标签': [(MobileBy.XPATH,
                          '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.view.ViewGroup[{}]'.format(
                              i)) for _ in range(5) for i in range(2, 8)],
                  '添加个性标签': (MobileBy.XPATH,
                             '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]'),
                  '标签取消': (MobileBy.ID, 'com.cmic.college:id/btnCancel'),
                  }

    @TestLogger.log('判断该元素是否能点击')
    def element_is_clickable(self, text):
        return self._is_clickable(self.__locators[text])

    @TestLogger.log("当前页面是否包含此文本")
    def is_text_exist(self, text):
        """当前页面是否包含此文本"""
        return self.is_text_present(text)

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators["返回"])

    @TestLogger.log('点击取消修改资料')
    def click_cancel_profile(self):
        self.click_element(self.__locators["弹框取消"])

    @TestLogger.log('输入昵称文本内容')
    def input_profile_name(self, locator, text):
        self.input_text(self.__locators[locator], text)

    @TestLogger.log('点击保存')
    def click_save(self):
        self.click_element(self.__locators["保存"])

    @TestLogger.log("点击资料页面头像按钮")
    def click_profile_photo(self):
        self.click_element(self.__locators['个人头像'])

    @TestLogger.log("点击头像更多按钮")
    def click_photo_more(self):
        self.click_element(self.__locators['头像更多'])

    @TestLogger.log("点击头像返回按钮")
    def click_photo_back(self):
        self.click_element(self.__locators['头像页面返回'])

    @TestLogger.log("点击locators对应的元素")
    def click_locator_key(self, locator):
        self.click_element(self.__locators[locator])

    @TestLogger.log("点击资料页面标签按钮选择标签")
    def click_tag_index(self, locator, index):
        self.click_element(self.__locators[locator][int(index)])

    @TestLogger.log("校验text提示内容")
    def check_text_exist(self, text):
        return self.is_toast_exist(text)

    @TestLogger.log("输入随机昵称")
    def input_random_name(self):
        """当前页面元素是否存在"""
        uid = str(uuid.uuid4())
        suid = ''.join(uid.split('-'))
        name = suid[:15]
        self.input_profile_name('昵称', name)
