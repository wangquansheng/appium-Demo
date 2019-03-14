import re
import time
import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.login import Agreement

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

    @staticmethod
    def setUp_test_login_0001():
        """"""

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_login_0001(self, login_time=60):
        """ 本网非首次登录已设置头像-一键登录页面元素检查"""

