from pprint import pprint as p
from time import sleep
from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select


class EmailCreator:

    def __init__(self, login, password, domain):

        self.display = Display(visible=0, size=(800, 600))
        self.display.start()

        self.mail_domain = domain
        self.login = login
        self.password = password
        options = Options()
        options.headless = True
        '''Вот тут нужно добавить относительный путь до chrome driver'''
        self.driver = webdriver.Chrome(options=options,
                                       service_log_path=r"C:\Users\Andrew\AppData\Local\Temp\chromedriver.log",
                                       executable_path=r"C:\Users\Andrew\AppData\Local\Programs\Python\Python37-32\chromedriver.exe",
                                       #  seleniumwire_options=dict(verify_ssl=False,
                                       #                            ignore_http_methods=['GET', 'POST', 'OPTIONS'])
                                       )

        self.driver.execute_cdp_cmd("Page.setBypassCSP", {"enabled": True})
        self.driver.get("https://hosting.timeweb.ru/login")
        self.driver.get_screenshot_as_file('1.png')

        # self.driver.set_script_timeout(50)
        # self.driver.set_page_load_timeout(50)
        #        self.driver = webdriver.Firefox(options=options,
        #                                        service_log_path=r"D:\geckodriver.log",
        #                                        executable_path=r"C:\Users\Andrew\AppData\Local\Programs\Python\Python37-32\geckodriver.exe")

        # Вход
        #    WebDriverWait(self.driver, 2).until(
        #    lambda driver: driver.execute_script('return document.readyState') == 'complete')

        # self.driver.get("https://hosting.timeweb.ru/login")
        #        while self.driver.current_url != 'https://hosting.timeweb.ru/login':
        #            pass

        p(1)
        self.driver.find_element_by_id("loginform-username").send_keys(login)
        self.driver.find_element_by_id("loginform-password").send_keys(password)
        self.driver.find_element_by_name("login-button").submit()
        p(2)
        while self.driver.current_url == 'https://hosting.timeweb.ru/login':
            pass
        p(3)
        service = self.driver.current_url.split('//')[1].split('.')[0]

        # dropdown_elements=driver.find_elements_by_class_name("k-dropdown")
        # idx = next(y for y, x in enumerate(dropdown_elements) if x.get_attribute('aria-owns') == "js-domain-select_listbox")
        # dropdown_elements[idx]
        # sl=driver.find_elements_by_tag_name('select')
        # Select(sl[0]).options
        # [x.get_attribute('value') for x in Select(sl[0]).options]
        # sl = driver.find_element_by_id('js-domain-select')
        # S = Select(sl)
        # [x.get_attribute('value') for x in S.options].index(self.mail_domain)

        self.driver.get(f"https://{service}.timeweb.ru/mailman?domain={self.mail_domain}")
        #        while self.driver.current_url != f"https://{service}.timeweb.ru/mailman?domain={self.mail_domain}":
        #            pass
        # Мы загрузили страницу по адресу f"https://{service}.timeweb.ru/mailman?domain={self.mail_domain}"  теперь давайте убедимся что нет ошибок
        #        WebDriverWait(self.driver, 2).until(
        #            lambda driver: driver.execute_script('return document.readyState') == 'complete')
        p(4)
        try:
            if self.driver.find_element_by_class_name('page-error').text.split()[0] == 'Ошибка' \
                    or self.driver.find_element_by_class_name('page-error').text.split()[0] == '404':

                self.driver.get(f"https://{service}.timeweb.ru/domains/move")

                while self.driver.current_url != f"https://{service}.timeweb.ru/domains/move":
                    pass

                #                WebDriverWait(self.driver, 2).until(
                #                    lambda driver: driver.execute_script('return document.readyState') == 'complete')

                try:
                    res = self.driver.find_element_by_class_name('page-error').text.split()[0]
                    if res == 'Ошибка':
                        print(f'''Что-то не так с ПУ timeweb или этим скриптом, домен {self.mail_domain}
                    не существует в этом аккаунте, а страница {self.driver.current_url} недоступна''')
                    exit(1)
                except NoSuchElementException:
                    pass
                self.driver.find_element_by_class_name("input__field").send_keys(self.mail_domain)
                #                WebDriverWait(self.driver, 10).until(
                #                    expected_conditions.element_to_be_clickable((By.CLASS_NAME, "tw-button-primary"))).click()
                # elem = \
                self.driver.find_element_by_class_name("tw-button-primary").send_keys(Keys.ENTER)
                # self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                # elem.click()

        except NoSuchElementException:
            p(f"Ошибок нет сейас мы на странцие {self.driver.current_url}")

    def create(self, name, password):

        # add_email_btn\
        WebDriverWait(self.driver, 2).until(
            expected_conditions.element_to_be_clickable((By.ID, "add-mailbox-button")))

        self.driver.find_element_by_id("add-mailbox-button").click()

        try:
            email_name = WebDriverWait(self.driver, 20).until(
                expected_conditions.presence_of_element_located(
                    (By.NAME, 'Mailbox[name]')
                )
            )
            self.driver.find_element(By.NAME, 'Mailbox[name]').send_keys(name)
            #    = self.driver.find_element(By.NAME, 'Mailbox[name]')

        except:
            p("Loading took too much time!")

            #        except NoSuchElementException:
            p(self.driver.current_url)
            p(self.driver.page_source)
        #            sleep(5)
        #            email_name = self.driver.find_element(By.NAME, 'Mailbox[name]')
        try:
            #            WebDriverWait(self.driver, 5).until(
            #                expected_conditions.element_to_be_clickable((By.NAME, 'Mailbox[password]')))
            email_pass = WebDriverWait(self.driver, 20).until(
                expected_conditions.presence_of_element_located(
                    (By.NAME, 'Mailbox[password]')
                )
            )
            self.driver.find_element(By.NAME, 'Mailbox[password]').send_keys(password + Keys.ENTER)
        except NoSuchElementException:
            p(self.driver.current_url)
            sleep(5)
            email_pass = self.driver.find_element(By.NAME, 'Mailbox[password]')
            email_pass.send_keys(password + Keys.ENTER)
        #        email_name.send_keys(name)
        #        email_pass.send_keys(password + Keys.ENTER)

        p('Все }{0(R)0III0')

        sleep(3)

    def exit(self):
        self.driver.close()
        self.display.stop()


ec = EmailCreator(
    login='cf02830',
    password='z4JU2FJ4',
    domain='vianda1n.ru')

ec.create("tes111t", "eAAA222111s")
ec.exit()
