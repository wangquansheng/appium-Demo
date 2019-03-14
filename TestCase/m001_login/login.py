import re
import time
import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags

from pages.guide import GuidePage

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class LoginTest(TestCase):
    """Login 模块"""

    def setUp_test_login_0001(self):
        """"""
        mb = switch_to_mobile('M960BDQN229CH')
        mb.connect_mobile()
        self.gd = GuidePage()
        self.gd.mobile.reset_app()
        self.gd.wait_for_page_load()
        self.gd.swipe_by_percent_on_screen(90, 50, 10, 50, 600)
        self.gd.swipe_by_percent_on_screen(90, 50, 10, 50, 600)
        mb.click_text('立即体验')

    @tags('DEMO')
    def test_login_0001(self):
        """ 本网非首次登录已设置头像-一键登录页面元素检查"""
        import time
        time.sleep(4)
        self.gd.mobile.assert_screen_contain_text('本机号码')
