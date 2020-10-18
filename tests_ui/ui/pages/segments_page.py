from selenium.common.exceptions import TimeoutException

from tests_ui.ui.pages.base_page import BasePage
from tests_ui.ui.locators.basic_locators import SegmentsPageLocators
from tests_ui.ui.settings import segment_create_name,segment_delete_name

class SegmentsPage(BasePage):
    locators = SegmentsPageLocators


    def __init__(self, driver):
        self.driver = driver
        self.driver.get("https://target.my.com/segments/segments_list")

    def create_new_segment(self, segment_name=segment_create_name):
        self.driver.get("https://target.my.com/segments/segments_list/new/")
        self.click(self.locators.ADDING_SOURCE_CHECKBOX)
        self.click(self.locators.ADD_SEGMENT_MODAL_BUTTON)
        segment_name_input = self.find(self.locators.SEGMENT_NAME_INPUT)
        segment_name_input.clear()
        segment_name_input.send_keys(segment_name)
        self.click(self.locators.CREATE_SEGMENT_BUTTON)

    def find_segment_created(self):
        result = None
        try:
            result = self.find(self.locators.CREATED_SEGMENT_NAME_CREATE)
        except TimeoutException:
            # Ничего не нашли
            pass

        return result
    
    def find_segment_to_delete(self):
        result = None
        try:
            result = self.find(self.locators.CREATED_SEGMENT_NAME_DELETE)
        except TimeoutException:
            # Ничего не нашли
            pass

        return result
        
