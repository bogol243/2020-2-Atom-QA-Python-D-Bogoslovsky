import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions

from tests_ui.ui.pages.dashboard_page import DashboardPage
from tests_ui.ui.pages.login_page import LoginPage
from tests_ui.ui.pages.segments_page import SegmentsPage
from tests_ui.ui.settings import credentials, segment_delete_name

from webdriver_manager.chrome import ChromeDriverManager

import uuid


class UsupportedBrowserException(Exception):
    pass


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    version = request.config.getoption('--browser_ver')
    selenoid = request.config.getoption('--selenoid')
    return {'browser': browser,
            'version': version,
            'url': url,
            'selenoid': selenoid,
            'download_dir': '/tmp'}


@pytest.fixture(scope='function')
def driver(config):
    browser = config['browser']
    version = config['version']
    selenoid = config['selenoid']
    url = config['url']
    download_dir = config['download_dir']

    if browser == 'chrome':
        options = ChromeOptions()
        options.add_argument("--window-size=800,600")

        prefs = {"download.default_directory": download_dir}
        options.add_experimental_option('prefs', prefs)

        driver = None
        if selenoid is not None:
            options.set_capability("browserVersion", version)
            driver = webdriver.Remote(command_executor='http://'+selenoid+'/wd/hub/',
                                      options=options,
                                      desired_capabilities={
                                          'acceptInsecureCerts': True}
                                      )
        else:
            manager = ChromeDriverManager(version=version)
            driver = webdriver.Chrome(executable_path=manager.install(),
                                      options=options,
                                      desired_capabilities={
                                          'acceptInsecureCerts': True}
                                      )

    else:
        raise UsupportedBrowserException(f'Usupported browser: "{browser}"')

    driver.get(url)
    driver.maximize_window()
    yield driver

    driver.quit()


@pytest.fixture
def dashboard_page(driver):
    login_page = LoginPage(driver)
    login_page.click_login()
    login_page.enter_credentials(credentials)
    login_page.submit_credentials()

    dashboard_page_obj = DashboardPage(driver)
    return dashboard_page_obj


@pytest.fixture
def segments_page_with_segment(dashboard_page):
    page = SegmentsPage(dashboard_page.driver)
    page.create_new_segment(segment_delete_name)
    return page


@pytest.fixture
def campaign_name():
    return str(uuid.uuid4())
