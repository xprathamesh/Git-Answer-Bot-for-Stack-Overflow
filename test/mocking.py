import asyncio
import time

import httpretty
import json
import re

from bs4 import BeautifulSoup, Tag
import os
from pyppeteer import launch, browser
from pyppeteer.page import Page
from unittest import mock

import poster, extractor
import Credentials as c
# from test import test_methods

# loads mock post data from provided json file.
with open('mock_data2.json', 'r') as f:
    data = json.load(f)
re_question = re.compile('https://api.stackexchange.com/2.2/questions/.*')


async def test_question_extractor():
    """Mock data method for question_Extractor().

    :param m: Mock adapter for intercepting calls from requests module
    :return: a list of posts
    """
    # intercepts all GET calls to addresses matching regex and sends a
    # response with our mock data
    # m.get(re_question, text=json.dumps({'hello' : 'world'}))
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, re_question, body=json.dumps(data))
    result = await extractor.question_Extractor()
    httpretty.disable()
    return result


async def localize_page(page: Page, answered_link: str) -> str:
    """Generates a mock local copy of a page for testing.

    answered_link gives the page to navigate to upon form submission. This is
    necessary to enumate the functionality of our bot without directly
    impacting the StackOverflow webpage itself.

    :param page: the page to localize
    :param answered_link: link to the answered version of the question
    :return: absolute path to localized webpage html file
    """
    html = await page.content()
    soup = BeautifulSoup(html)
    answers = soup.find('div', {'id' : 'answers'})
    form = answers.find('form', {'id' : 'post-form'})
    form['action'] = "file://{}".format(answered_link)

    with open('test/mock_post_unanswered.html', 'w') as f:
        f.write(str(soup))

    return os.path.abspath('test/mock_post_unanswered.html')


async def _mock_post(page: Page, bot_post: str) -> str:
    """Creates a mock SO page with a dummy answer.

        :param page: the pyppeteer.page.Page object to post an answer on
        :param content: dict containing question information for answer formatting
        :return:
        """

    # Gets page's html in string format and parses it with BeautifulSoup
    html = await page.content()
    soup = BeautifulSoup(html)

    # Locates answer section on question page (div tag with id set to answers)
    answers = soup.find("div", {"id": "answers"})
    # Since we only target unanswered posts, remove attr set to 'no-answers'
    del answers['class']
    # Answer posts begin after 'answer-header', so we insert nodes after it
    ans_head = answers.find('div', {'id': 'answers-header'})
    # New tag declaring answer id is created and inserted after answer-head
    id_tag = Tag(builder=soup.builder,
                 name='a',
                 attrs={'name': '000'})
    ans_head.insert_after(id_tag)

    # parse html template for a posted suggested answer to a question
    with open('test/mock_post_template.html', 'r') as fp:
        test_tree = BeautifulSoup(fp, 'html.parser')

    # modify template to match our mock answer post
    test_root = test_tree.find('div', {'class': 'answer'})
    # set answer ids and find post body
    test_root['id'] = 'answer-000'
    test_root['data-answerid'] = 000
    post = test_tree.find('div', {'class': "post-text", 'itemprop': 'text'})
    # Insert dummy_answer into post body, then put after matching answer id tag
    post.string = bot_post
    id_tag.insert_after(test_tree)

    # write mock post to file for examination
    with open('test/mock_post_answered.html', 'w') as f:
        f.write(str(soup))

    return os.path.abspath('test/mock_post_answered.html')


async def mock_post(page: Page, content: dict) -> Page:
    """Creates a mock SO page with a dummy answer.

    :param page: the pyppeteer.page.Page object to post an answer on
    :param content: dict containing question information for answer formatting
    :return:
    """
    posting_answer = ''
    example_flag = await poster.containsExample(content)
    if example_flag:
        posting_answer = await poster.getExample(content)
    else:
        posting_answer = await poster.getQuery(content)

    posting_answer = "Hello " + str(content['qposter']).split(' ')[
        0] + ',\n\n' + posting_answer

    # TODO set form redirect to answered_page on submission
    answered_page = await _mock_post(page, posting_answer)
    local_mock = await localize_page(page, answered_page)
    await page.goto("file://{}".format(local_mock))

    await page.type('textarea[id=wmd-input]', posting_answer, {'delay': 15})
    print(posting_answer)
    await page.click('button[id=submit-button]')
    await page.goto("file://{}".format(answered_page))

    return page


@mock.patch('poster.answer', new=lambda x,y: mock_post(x,y))
def test_run(q):
    """Calls _run() with post_answer() method mocked with mock_post()

    @mock.patch() patches calls to post_answer() in test.test_methods with a
    call to mock_post() when run through the current mocking.py file.

    :param q: question steam from question_Extractor
    :return:
    """
    asyncio.get_event_loop().run_until_complete(poster.run(q))


async def test_browser(url):
    """Method to test mock_post() via a simulated browser.

    :param url: the question url to post an answer on
    :return: html string
    """
    browser = await launch(
        {"headless": False, "args": ["--no-sandbox", "--disable-web-security"]})
    page = await browser.newPage()
    await page.goto(url)
    html = await mock_post(page, {'ques' : 'SilverStripe PHP'}).content()
    await browser.close()
    return html


# def mock_data():
#     url = 'https://api.stackexchange.com/2.2/questions/no-answers?order=asc&sort=creation&tagged=git&filter=!9Z(-wwYGT&&site=stackoverflow&team=stackoverflow.com/c/ncsu&key=' + \
#           c.secret['key']
#     headers = {
#         'X-API-Access-Token': c.secret['AccessToken'],
#         'Accept-Charset': 'UTF-8'
#     }
#
#     res = requests.get(url, headers=headers)
#     data = res.json()
#     with open('mock_data2.json', 'w') as f:
#         f.write(json.dumps(data))


if __name__ == '__main__':
    os.chdir('..')
    resp = asyncio.get_event_loop().run_until_complete(
        test_question_extractor())
    print(resp)
    for q in resp:
        test_run(q)
        time.sleep(10)
    # html = asyncio.get_event_loop().run_until_complete(test_browser(
    #     'https://stackoverflow.com/c/ncsu/questions/852'
    # ))
