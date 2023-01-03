from selenium.webdriver.common.by import By

"""Locator objects for finding Selenium WebElements"""
class Locator:

    def __init__(self, l_type, selector):
        self.l_type = l_type
        self.selector = selector

    def parameterize(self, *args):
        self.selector = self.selector.format(*args)

"""Login page element locators"""
class LoginPageLocators:
    access = Locator(By.ID, "login-toolbar")
    #login_card = Locator(By.ID, "login-container")
    login_page = Locator(By.ID, "login-toolbar")
    email_field = Locator(By.ID, "login-email")
    next_button = Locator(By.ID, "login-button-next")
    password_field = Locator(By.ID, "login-password")
    access_button = Locator(By.ID, "login-button-access")

class HomePageLocators:
    navigation_drawer = Locator(By.ID, "navigation-drawer-logo-link")