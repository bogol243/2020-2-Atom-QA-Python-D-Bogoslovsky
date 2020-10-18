from selenium.common.exceptions import TimeoutException

from tests_ui.ui.locators.basic_locators import DashboardPageLocators
from tests_ui.ui.pages.base_page import BasePage
from tests_ui.ui.pages.new_campaign_page import NewCampaignPage


class DashboardPage(BasePage):
    locators: DashboardPageLocators = DashboardPageLocators

    def __init__(self, driver):
        self.driver = driver

    def click_create_company(self):
        self.click(self.locators.CREATE_BUTTON)
        return NewCampaignPage(self.driver)

    def find_campaign(self, campaign_name):
        result = None
        try:
            result = self.find(self.locators.get_created_campaign_name(
                campaign_name), timeout=10)
        except TimeoutException:
            # Ничего не нашли
            pass

        return result

    def delete_campaign(self, id=None, name=None):
        if id is not None:
            pass
            return True
        if name is not None:
            self.click(self.locators.get_created_campaign_checkbox(name))
            self.click(self.locators.TABLE_ACTIONS_DROPDOWN)
            self.click(self.locators.TABLE_ACTION_DELETE_BUTTON)
            return True
