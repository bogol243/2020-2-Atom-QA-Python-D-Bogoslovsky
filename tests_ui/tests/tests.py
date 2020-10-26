import os
import time
import pytest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from tests_ui.ui.fixtures import *
from tests_ui.ui.pages.login_page import LoginPage
from tests_ui.ui.pages.segments_page import SegmentsPage
from tests_ui.ui.settings import credentials, credentials_wrong

from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.UI
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.click_login()
    login_page.enter_credentials(credentials)
    login_page.submit_credentials()

    assert driver.current_url == "https://target.my.com/dashboard"

@pytest.mark.UI
def test_login_negative(driver):
    login_page = LoginPage(driver)
    login_page.click_login()
    login_page.enter_credentials(credentials_wrong)
    login_page.submit_credentials()

    assert driver.current_url != "https://target.my.com/dashboard"


@pytest.mark.UI
def test_create_campaign(dashboard_page: DashboardPage, campaign_name):
    #page это NewCampaignPage
    page = dashboard_page.click_create_company()

    page.click_traffic_button()

    page.set_ad_url("https://mail.ru")

    page.select_ad_format("banner")

    page.set_campaign_name(campaign_name)

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(os.path.sep, ROOT_DIR, 'img.jpg')
    page.upload_image(img_path)
    time.sleep(2)

    # создали кампанию, возвращаемся обратно на dashboard
    dashboard_page = page.save_campaign()

    # пробуем найти созданную кампанию на странице
    # если не найдём, получим None
    campaign = dashboard_page.find_campaign(campaign_name)

    assert campaign is not None

    # Кампания найдена
    # тест пройден, теперь удалим то что создали
    dashboard_page.delete_campaign(name=campaign_name)


@pytest.mark.UI
def test_create_segment(dashboard_page: DashboardPage, api_client: ApiClient):
    page = SegmentsPage(dashboard_page.driver)
    page.create_new_segment()
    segment = page.find_segment_created()
    segment_id = segment.get_attribute("href").split('/')[-1]
    assert segment is not None
    
    api_client.delete_segment(segment_id)
    #тест пройден, теперь удалим то что создали
    #page.click(page.locators.CREATED_CAMPAIGN_CHECKBOX_CREATE)
    #page.click(page.locators.TABLE_ACTIONS_DROPDOWN)
    #page.click(page.locators.TABLE_ACTION_DELETE_BUTTON)

@pytest.mark.UI
def test_delete_segment(segments_page_with_segment: SegmentsPage):
    page = segments_page_with_segment
    page.click(page.locators.CREATED_CAMPAIGN_CHECKBOX_DELETE)
    page.click(page.locators.TABLE_ACTIONS_DROPDOWN)
    page.click(page.locators.TABLE_ACTION_DELETE_BUTTON)
    page.wait(2).until_not(EC.presence_of_element_located(
        page.locators.CREATED_CAMPAIGN_CHECKBOX_DELETE))

    segment = page.find_segment_to_delete()

    # если нашли удалённый сегмент, значит он не удалился
    assert segment is None
