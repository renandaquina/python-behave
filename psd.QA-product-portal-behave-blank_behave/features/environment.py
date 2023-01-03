from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from context.config import settings

def browser_config(context, browser_name):
    if browser_name == "firefox":
        option = webdriver.FirefoxOptions()
        option.add_argument("--start-maximized")
        option.add_argument("--ignore-certificate-errors")
        driver = webdriver.Firefox(firefox_options=option)
        return driver

    if browser_name == "headless-firefox":
        option = webdriver.FirefoxOptions()
        option.headless = True
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-gpu")
        option.add_argument("--start-maximized")
        option.add_argument("--disable-extensions")
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--disable-application-cache")
        option.add_argument("--ignore-certificate-errors")
        driver = webdriver.Firefox(firefox_options=option)
        return driver

    if browser_name == "headless-chrome":
        option = webdriver.ChromeOptions()
        option.headless = True
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-extensions")
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--disable-application-cache")
        option.add_argument("--ignore-certificate-errors")
        option.add_argument('--allow-insecure-localhost')
        option.add_argument('--headless')
        option.add_argument('--window-size=1920x1080')
        option.add_argument("--start-maximized") 

        driver = webdriver.Chrome(chrome_options=option)

        return driver

    if browser_name == "chrome":
        option = webdriver.ChromeOptions()
        option.add_argument("--start-maximized") #open Browser in maximized mode
        option.add_argument("--no-sandbox") #bypass OS security model
        option.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option('useAutomationExtension', False)
        option.add_argument("--ignore-certificate-errors")
        option.add_argument('--disable-gpu')

        prefs = {"credentials_enable_service": False,
         "profile.password_manager_enabled": False}
        
        option.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(chrome_options=option)

        return driver

    if browser_name == "phantonjs":
        driver = webdriver.PhantomJS()
        return driver

    if browser_name == "edge":
        driver = webdriver.Edge()
        return driver

def before_scenario(context, scenario):
    browser_name = settings.browser
    context.browser = browser_config(context, browser_name)
    context.browser.implicitly_wait(5)
    context.browser.set_page_load_timeout(60)
    context.location = settings.portal_url
    #context.location = context.config.userdata.get('url')
    context.browser.get(context.location)

def after_scenario(context, scenario):
    try:
        if scenario.status == 'failed':
            context.browser.close()

        else:
            context.browser.close()
    except AttributeError or WebDriverException:
        message = "'Context' object has no attribute 'browser'\nChrome failed to start: exited abnormally"
        raise Exception(message)
