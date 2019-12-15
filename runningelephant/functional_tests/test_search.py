from selenium import webdriver
from runningelephant.models import Player, Score, Thoughts
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
from django.test.utils import override_settings
from django.contrib.auth import get_user_model
import time

User = get_user_model()

@override_settings(DEBUG=True)
class TestSearch(LiveServerTestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            username = 'changhay',
            first_name = 'Changhao',
            last_name = 'Yang'
        )
        self.user1.set_password('changhay')
        self.user1.save()

        self.user2 = User.objects.create(
            username = 'zhaoxinyan',
            first_name = 'Xinyan',
            last_name = 'Zhao'
        )
        self.user2.set_password('zhaoxinyan')
        self.user2.save()

        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.close()
    
    def test_search(self):
        # Login
        self.browser.get(self.live_server_url + reverse('addfriends'))
        self.browser.find_element_by_id('id_username').send_keys('changhay')
        self.browser.find_element_by_id('id_password').send_keys('changhay')
        self.browser.find_element_by_id('login-submit').click()
        
        # Search
        self.browser.find_element_by_id('search-input').send_keys('z')
        self.browser.find_element_by_id('search-button').click()

        name = self.browser.find_elements_by_tag_name('h6')[0].text
        
        self.assertEquals(name, self.user2.username)
