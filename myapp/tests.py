#from django.test import TestCase
# Create your tests here.
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    fixtures = ['testdb.json',]
 
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
 
    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        #cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )
        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()
        # testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )

    def test_grup(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
        self.selenium.find_element(By.NAME, "username").send_keys("isard")
        self.selenium.find_element(By.NAME, "password").send_keys("pirineus")
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        self.selenium.find_element(By.LINK_TEXT, "Groups").click() # Anem a la secció de grups
        page_source = self.selenium.page_source # Comprovem si el grup apareix
        self.assertIn("Group_1", self.selenium.page_source) 

        self.selenium.find_element(By.LINK_TEXT, "Home").click() # Tornem a l'inici
        self.selenium.find_element(By.LINK_TEXT, "Users").click() # Anem a la secció usuaris
        self.selenium.find_element(By.LINK_TEXT, "ADD USER").click() # Anem a la secció d'afegir usuaris

        self.selenium.find_element(By.NAME, "username").send_keys("user_test") # Omplir nom
        self.selenium.find_element(By.NAME, "password1").send_keys("User_IOC") # Omplir pw
        self.selenium.find_element(By.NAME, "password2").send_keys("User_IOC")
        self.selenium.find_element(By.NAME, "_continue").click()

        wait = WebDriverWait(self.selenium, 10)
        grups_seleccio = wait.until(EC.precense_of_element_located((By.NAME, "groups"))) # Busquem la selecció de grups per l'usuari
        opcions = grups_seleccio.text # Recollida d'opcions de selecció de grup
        self.assertIn("Grup_1", opcions) # Comprova que Grup_1 existeix