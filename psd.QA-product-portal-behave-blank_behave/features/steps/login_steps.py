from behave import *
from selenium.webdriver.support import expected_conditions as EC
from datasource.users import DATA_ACCESS
from pages.base_page import BasePage
from context.config import settings
from pages.locators import LoginPageLocators, HomePageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time


#----------------------------------------------------------------------------------------------------------------------#
# USER_LOGGED_IN is a method designed to complete the login of a user                                                  #
#----------------------------------------------------------------------------------------------------------------------#
@given('User logged in with valid credential')
def user_logged_in(context):
    """
    BACKGROUND steps are called at begin of each scenario before other steps.
    """
    current_page_is_login_page(context)
    fill_the_email_field(context, 'valid credential', 'username')
    click_on_next_button(context)
    fill_the_password_field(context, 'valid credential', 'password')
    click_on_access_button(context)


#----------------------------------------------------------------------------------------------------------------------#
# CURRENT_PAGE_IS_LOGIN_PAGE is a method designed to verify if the current page is login page                          #
#----------------------------------------------------------------------------------------------------------------------#
@given('I am at a Login page')
def current_page_is_login_page(context):
    locator = getattr(LoginPageLocators, "login_page")
    BasePage.element_exists(BasePage, context, locator, 60)


#----------------------------------------------------------------------------------------------------------------------#
# FILL_THE_EMAIL_FIELD is a method designed to fill the email field                                                    #
#----------------------------------------------------------------------------------------------------------------------#
@when('I fill in the Email with {credential}')
def fill_the_email_field(context, credential, user='username'):
    base_page = BasePage
    user = base_page.datapool_read(base_page, DATA_ACCESS, credential, user)
    username_field = BasePage.get_element(base_page, context, LoginPageLocators.email_field)
    username_field.clear()
    username_field.send_keys(user)


#----------------------------------------------------------------------------------------------------------------------#
# FILL_THE_PASSWORD_FIELD is a method designed to fill the password field                                              #
#----------------------------------------------------------------------------------------------------------------------#
@when('I fill in the field password with {credential}')
def fill_the_password_field(context, credential, password='password'):
    base_page = BasePage
    pwd = base_page.datapool_read(base_page, DATA_ACCESS,credential, password)
    password_field = BasePage.get_element(base_page, context, LoginPageLocators.password_field)
    password_field.clear()
    password_field.send_keys(pwd)


#----------------------------------------------------------------------------------------------------------------------#
# CLICK_ON_NEXT_BUTTON is a method designed to click next button                                                       #
#----------------------------------------------------------------------------------------------------------------------#
@when('I click on Next button')
def click_on_next_button(context):
    base_page = BasePage
    next_button = BasePage.get_element(base_page, context, LoginPageLocators.next_button)
    next_button.click()


#----------------------------------------------------------------------------------------------------------------------#
# CLICK_ON_ACESS_BUTTON is a method designed to click access button                                                    #
#----------------------------------------------------------------------------------------------------------------------#
@when('I click on Sign In button')
def click_on_access_button(context):
    base_page = BasePage
    sign_in = BasePage.get_element(base_page, context, LoginPageLocators.access_button)
    sign_in.click()


#----------------------------------------------------------------------------------------------------------------------#
# CURRENT_PAGE_IS_HOME_PAGE is a method designed to verify if the current page is home page                            #
#----------------------------------------------------------------------------------------------------------------------#
@given('The current page is Home page')
@then('The current page is Home page')
def current_page_is_home_page(context):
    locator = getattr(HomePageLocators, "navigation_drawer")
    BasePage.element_exists(BasePage, context, locator, 120)
    #close_success_alert = getattr(HomePageLocators, "login_success_alert_close_btn")
    #close_success_btn = BasePage.get_element(BasePage, context, close_success_alert)
    #close_success_btn.click()
    
@when("I try to Login")
def i_try_to_login(context):
    pass


@then("An error message appears")
def an_error_message_appears(context):
    pass

