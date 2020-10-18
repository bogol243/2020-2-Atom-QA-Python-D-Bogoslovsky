from selenium.webdriver.common.by import By
from tests_ui.ui.settings import segment_create_name, segment_delete_name


class SegmentsPageLocators():
    ADDING_SOURCE_CHECKBOX = (
        By.XPATH, "//input[contains(@class,'adding-segments-source__checkbox')]")
    ADD_SEGMENT_MODAL_BUTTON = (
        By.XPATH, "//div[contains(@class,'adding-segments-modal__btn')]")
    SEGMENT_NAME_INPUT = (
        By.XPATH, "//div[contains(@class,'input_create-segment-form')]//input")
    CREATE_SEGMENT_BUTTON = (
        By.XPATH, "//div[contains(@class,'button__text') and text()='Создать сегмент']")
    CREATED_SEGMENT_NAME_CREATE = (
        By.XPATH, "//a[text()='"+segment_create_name+"']")
    CREATED_SEGMENT_NAME_DELETE = (
        By.XPATH, "//a[text()='"+segment_delete_name+"']")

    CREATED_CAMPAIGN_CHECKBOX_CREATE = (
        By.XPATH, "//a[@title='"+segment_create_name+"']/../../..//input[@type='checkbox']")
    CREATED_CAMPAIGN_CHECKBOX_DELETE = (
        By.XPATH, "//a[@title='"+segment_delete_name+"']/../../..//input[@type='checkbox']")
    TABLE_ACTIONS_DROPDOWN = (
        By.XPATH, "//div[contains(@class,'segmentsTable-module-massActionsSelect')]")
    TABLE_ACTION_DELETE_BUTTON = (
        By.XPATH, "//li[contains(@class,'optionsList-module-option') and @title='Удалить']")


class NewCampaignPageLocators():
    TARGET_TRAFFIC_BUTTON = (
        By.XPATH, "//div[@data-class-name='ColumnListView']//div[contains(@class,'_traffic')]")
    AD_URL_TEXT_INPUT = (By.XPATH, "//input[@data-gtm-id='ad_url_text']")
    BANNER_FORMAT_BUTTON = (
        By.XPATH, "//div[@class='banner-format-item']//span[text()='Баннер']/..")
    IMAGE_LOADING_INPUT = (By.XPATH, "//input[@data-test='image_240x400']")
    CAMPAIGN_NAME_INPUT = (
        By.XPATH, "//div[contains(@class,'input_campaign-name')]//input[@type='text']")
    SAVE_CAMPAIGN_BUTTON = (
        By.XPATH, "//div[contains(@class,'js-save-button-wrap')]")
    IMAGE_PREVIEW = (By.XPATH, "//img[contains(@class, 'imagePreview-module')]")

class DashboardPageLocators:

    def get_created_campaign_name(campaign_name):
        return (By.XPATH, "//a[@title='"+campaign_name+"']")
    def get_created_campaign_checkbox(campaign_name):
        return (By.XPATH, f"//a[@title='{campaign_name}']/../input[@type='checkbox']")

    CREATE_BUTTON = (
        By.XPATH, "//div[starts-with(@class, 'dashboard-module-createButtonWrap')]//div[starts-with(@class, 'button-module')]")
    
    TABLE_ACTIONS_DROPDOWN = (
        By.XPATH, "//div[contains(@class,'tableControls-module-selectItem')]")
    TABLE_ACTION_DELETE_BUTTON = (
        By.XPATH, "//li[contains(@class,'optionsList-module-option') and @title='Удалить']")


class LoginPageLocators():
    LOGIN_BUTTON = (
        By.XPATH, "//div[starts-with(@class, 'responseHead-module-button-')]")
    NAVBAR_EXPAND_BUTTON = (
        By.XPATH, "//div[starts-with(@class, 'responseHead-module-burger-')]")

    EMAIL_INPUT = (
        By.XPATH, "//div[starts-with(@class, 'authForm-module-input')]//input[@name='email']")
    PASSWORD_INPUT = (
        By.XPATH, "//div[starts-with(@class, 'authForm-module-input')]//input[@name='password']")
    SUBMIT_LOGIN_BUTTON = (
        By.XPATH, "//div[starts-with(@class, 'authForm-module-button')]")
