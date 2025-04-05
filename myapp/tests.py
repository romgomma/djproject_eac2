#from django.test import TestCase
# Create your tests here.
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
 
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
        cls.selenium.quit()
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

    def test_login_error(self):
        # comprovem que amb un usuari i contrasenya inexistent, el test falla
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )
 
        # introduim dades de login
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('user_error')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pw_error')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()
 
        # utilitzem assertNotEqual per testejar que NO hem entrat
        self.assertNotEqual( self.selenium.title , "Site administration | Django site admin" )


# Testejar que un element NO existeix
# Aquesta localització de l'element ens serveix també a mode de ASSERT
# Si no localitza l'element, llençarà una NoSuchElementException
#self.selenium.find_element(By.XPATH,"//button[text()='Log out']")


# Però què passa si volem comprovar que l'element NO existeix?
#from selenium.common.exceptions import NoSuchElementException
#...
#try:
#self.selenium.find_element(By.XPATH,"//a[text()='Log out']")
#assert False, "Trobat element que NO hi ha de ser"
#except NoSuchElementException:
#pass
