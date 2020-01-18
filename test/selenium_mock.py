import asyncio
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import poster
import Credentials as c
from test import mocking


# Ensure question answer is posted.
class TestAnswerQueryH(unittest.TestCase):
    """Happy scenario for providing an answer to a git-tagged question.

    """
    def setUp(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get("https://stackoverflow.com/users/login?ssrc=channels&returnurl=%2fc%2fncsu%2f")
        self.driver.find_element_by_id('has-public-account-radio').click()
        email = self.driver.find_element_by_name('email')
        passwd = self.driver.find_element_by_name('password')
        email.send_keys(c.login['user'])
        passwd.send_keys(c.login['pwd'])
        self.driver.find_element_by_name('submit-button').click()

    def test_git_answer(self):
        # TODO need to get reference to page object
        iden = asyncio.get_event_loop().run_until_complete(poster.run(poster._q))
        self.driver.get('https://stackoverflow.com/c/ncsu/questions/{}'.format(iden))
        answers = self.driver.find_element_by_id('answers')
        assert answers.get_attribute("class") != "no-answers"
        answer = answers.find_element_by_class_name("user-details")
        name = answer.find_element_by_class_name('d-none').text
        assert name in c.login['user']

    def tearDown(self) -> None:
        self.driver.close()


# Question answer is not posted.
class TestAnswerQueryU(unittest.TestCase):
    """Unhappy scenario for providing an answer to a git-tagged question.

    """
    def setUp(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get(
            "https://stackoverflow.com/users/login?ssrc=channels&returnurl=%2fc%2fncsu%2f")
        self.driver.find_element_by_id('has-public-account-radio').click()
        email = self.driver.find_element_by_name('email')
        passwd = self.driver.find_element_by_name('password')
        email.send_keys(c.login['user'])
        passwd.send_keys(c.login['pwd'])
        self.driver.find_element_by_name('submit-button').click()

    def test_git_answer(self):
        iden = asyncio.get_event_loop().run_until_complete(
            poster.run(poster._q))
        self.driver.get(
            'https://stackoverflow.com/c/ncsu/questions/{}'.format(iden))
        answers = self.driver.find_element_by_id('answers')
        assert answers.get_attribute("class") == 'no-answers'

    def tearDown(self) -> None:
        self.driver.close()


class TestExampleQueryH(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get(
            "https://stackoverflow.com/users/login?ssrc=channels&returnurl=%2fc%2fncsu%2f")
        self.driver.find_element_by_id('has-public-account-radio').click()
        email = self.driver.find_element_by_name('email')
        passwd = self.driver.find_element_by_name('password')
        email.send_keys(c.login['user'])
        passwd.send_keys(c.login['pwd'])
        self.driver.find_element_by_name('submit-button').click()

    def test_example_query(self):
        iden = asyncio.get_event_loop().run_until_complete(
            poster.run(poster._q))
        self.driver.get(
            'https://stackoverflow.com/c/ncsu/questions/{}'.format(iden))
        answers = self.driver.find_element_by_id('answers')
        assert answers.get_attribute("class") != "no-answers"
        user = answers.find_element_by_class_name("user-details")
        name = user.find_element_by_class_name('d-none').text
        assert name in c.login['user']

    def tearDown(self) -> None:
        self.driver.close()


class TestExampleQueryU(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get(
            "https://stackoverflow.com/users/login?ssrc=channels&returnurl=%2fc%2fncsu%2f")
        self.driver.find_element_by_id('has-public-account-radio').click()
        email = self.driver.find_element_by_name('email')
        passwd = self.driver.find_element_by_name('password')
        email.send_keys(c.login['user'])
        passwd.send_keys(c.login['pwd'])
        self.driver.find_element_by_name('submit-button').click()

    def test_example_query(self):
        iden = asyncio.get_event_loop().run_until_complete(
            poster.run(poster._q))
        self.driver.get(
            'https://stackoverflow.com/c/ncsu/questions/{}'.format(iden))
        answers = self.driver.find_element_by_id('answers')
        assert answers.get_attribute("class") == 'no-answers'

    def tearDown(self) -> None:
        self.driver.close()


class TestMultipleQuestionsH(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get(
            "https://stackoverflow.com/users/login?ssrc=channels&returnurl=%2fc%2fncsu%2f")
        self.driver.find_element_by_id('has-public-account-radio').click()
        email = self.driver.find_element_by_name('email')
        passwd = self.driver.find_element_by_name('password')
        email.send_keys(c.login['user'])
        passwd.send_keys(c.login['pwd'])
        self.driver.find_element_by_name('submit-button').click()

    def test_multiple_questions(self):
        iden = asyncio.get_event_loop().run_until_complete(
            poster.run(poster._q))
        self.driver.get(
            'https://stackoverflow.com/c/ncsu/questions/{}'.format(iden))
        answers = self.driver.find_element_by_id('answers')
        assert answers.get_attribute("class") != "no-answers"
        user = answers.find_element_by_class_name("user-details")
        name = user.find_element_by_class_name('d-none').text
        assert name in c.login['user']

    def tearDown(self) -> None:
        self.driver.close()


class TestMultipleQuestionsU(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get(
            "https://stackoverflow.com/users/login?ssrc=channels&returnurl=%2fc%2fncsu%2f")
        self.driver.find_element_by_id('has-public-account-radio').click()
        email = self.driver.find_element_by_name('email')
        passwd = self.driver.find_element_by_name('password')
        email.send_keys(c.login['user'])
        passwd.send_keys(c.login['pwd'])
        self.driver.find_element_by_name('submit-button').click()

    def test_multiple_questions(self):
        iden = asyncio.get_event_loop().run_until_complete(
            poster.run(poster._q))
        self.driver.get(
            'https://stackoverflow.com/c/ncsu/questions/{}'.format(iden))
        answers = self.driver.find_element_by_id('answers')
        assert answers.get_attribute("class") != "no-answers"
        user = answers.find_element_by_class_name("user-details")
        name = user.find_element_by_class_name('d-none').text
        assert name in c.login['user']

    def tearDown(self) -> None:
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
