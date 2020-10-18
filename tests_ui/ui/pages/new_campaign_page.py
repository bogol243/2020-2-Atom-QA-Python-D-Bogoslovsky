from tests_ui.ui.pages.base_page import BasePage
from tests_ui.ui.pages import dashboard_page
from tests_ui.ui.locators.basic_locators import NewCampaignPageLocators

from selenium.webdriver.support import expected_conditions as EC



class NewCampaignPage(BasePage):

    locators = NewCampaignPageLocators

    def __init__(self, driver):
        self.driver = driver

    def save_campaign(self):
        self.click(self.locators.SAVE_CAMPAIGN_BUTTON, timeout=10)
        self.wait(5).until(EC.url_contains("https://target.my.com/dashboard"))
        return dashboard_page.DashboardPage(self.driver)

    def click_traffic_button(self):
        self.click(self.locators.TARGET_TRAFFIC_BUTTON)

    def set_ad_url(self, url):
        text_input = self.find(self.locators.AD_URL_TEXT_INPUT)
        text_input.send_keys(url)

    def set_campaign_name(self, name):
        campaign_name_input = self.find(self.locators.CAMPAIGN_NAME_INPUT)
        campaign_name_input.clear()
        campaign_name_input.send_keys(name)

    def select_ad_format(self, format="banner"):
        if format == "banner":
            self.click(self.locators.BANNER_FORMAT_BUTTON)

    def upload_image(self, path):
        image_input = self.find(self.locators.IMAGE_LOADING_INPUT)
        image_input.send_keys(path)
        self.wait(20).until(EC.presence_of_element_located(self.locators.IMAGE_PREVIEW))
