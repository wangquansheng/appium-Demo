from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GuidePage(BasePage):
    """fg"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.SplashActivity'

    __locators = {
        'com.cmic.college:id/action_bar_root': (MobileBy.ID, 'com.cmic.college:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.cmic.college:id/splash_view_pager': (MobileBy.ID, 'com.cmic.college:id/splash_view_pager'),
        'com.cmic.college:id/splash_root': (MobileBy.ID, 'com.cmic.college:id/splash_root'),
        'com.cmic.college:id/iv': (MobileBy.ID, 'com.cmic.college:id/iv'),
        'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground')
    }
