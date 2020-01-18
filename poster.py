import asyncio
import Credentials as c
import time
from pyppeteer import launch, browser
import json
import re
import string
import answergenerator as agen
from database import db_interface as db

loginEmail      = c.login['user']
loginPassword   = c.login['pwd']
NCSU_SO_URL     = "https://stackoverflow.com/users/login?ssrc=channels&returnurl=%2fc%2fncsu%2f"
contentBuilder  = {}
_q              = None

async def getQuery(content):
    with open('git_queries.json', 'r') as query_file:
        git_queries = json.load(query_file)

    for data in git_queries:
        posting_answer = data['body'] + '\n\n' + data['link']
    return posting_answer

async def answer(page, content):
    posting_answer = ''
    print(content)
    posting_answer = await agen.getDBAnswer(content)
    if posting_answer == '':
        example_flag = await agen.containsExample(content)
        if example_flag:
            posting_answer = await agen.getExample(content)

    #print(type(posting_answer))
    if posting_answer != '':
        posting_answer = "Hello "+ str(content['qposter']).split(' ')[0] + ',\n\n' + posting_answer

    await page.type('textarea[id=wmd-input]', posting_answer, {'delay': 20})
    #print(posting_answer)
    #await page.click('button[id=submit-button]')
    return page

async def initiate_login(browser, url):
    page = await get_page(browser, url)
    await asyncio.gather(
        page.click('input[id=has-public-account-radio]'),
    )
    return page

async def get_page(browser, url):
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle0'})
    return page

async def login(page):
    await page.type('input[id=email]', loginEmail)
    await page.type('input[id=password]', loginPassword)
    await page.click('button[id=submit-button]')
    await page.waitForNavigation()
    return page

async def run(q):
    browser = await launch({"headless": False, "args": ["--no-sandbox", "--disable-web-security"]})
    page = await initiate_login(browser, NCSU_SO_URL)
    page = await login(page)
    for _q in q:
        contentBuilder['id'] = _q[0]
        contentBuilder['ques'] = _q[1]
        contentBuilder['qdetails'] = _q[2]
        contentBuilder['qposter'] = _q[3]
        contentBuilder['tags'] = _q[4]
        await page.goto('https://stackoverflow.com/c/ncsu/questions/'+str(contentBuilder['id']), {'waitUntil': 'networkidle0'})
        page = await answer(page, contentBuilder)
        time.sleep(0.5)

    await browser.close()
    # return contentBuilder['id']
    # await page.close()
    # await page.waitForNavigation()

# if __name__ == "StackOverflowBot":
#     asyncio.get_event_loop().run_until_complete(run(_q))
