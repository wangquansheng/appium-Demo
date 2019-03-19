from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage


class MinePage(FooterPage):
    """通话页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        'tip1': (MobileBy.ID, 'com.cmic.college:id/ivFreeCall'),
        'tip2': (MobileBy.ID, 'com.cmic.college:id/ivKeyboard'),
        'tip3': (MobileBy.ID, 'com.cmic.college:id/tvContact'),
        '视频': (MobileBy.ID, 'com.cmic.college:id/ivMultipartyCall'),

    }

