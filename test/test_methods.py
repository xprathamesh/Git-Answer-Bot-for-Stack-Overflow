import asyncio
import Credentials as c
import pandas as pd
import requests
import time

from pyppeteer import launch, browser


url = 'https://api.stackexchange.com/2.2/questions/no-answers?filter=withbody&pagesize=100&order=asc&sort=activity&site=stackoverflow&team=stackoverflow.com/c/ncsu&key=fbBOzCZVcE8PkNGwgXlNnQ(('
headers = {'X-API-Access-Token': 'DSf(yHMu58zW3HCQCdF4Uw))', 'Accept-Charset': 'UTF-8'}

NCSU_SO_URL = "https://stackoverflow.com/users/login?ssrc=channels&returnurl=%2fc%2fncsu%2f"
loginEmail = c.login['user']
loginPassword = c.login['pwd']
contentBuilder = {}
_q = None


async def question_Extractor():
    while (True):
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            break

        data = res.json()
        cur_time = time.time()
        df = pd.DataFrame.from_dict(data['items'], orient='columns')
        df.index.name = 'id'
        # df['tags_string'] = [','.join(map(str, l)) for l in df['tags']]
        # df_filtered = df[df['tags_string'].str.contains('git')]
        # print(df_filtered)
        df_filtered = df[cur_time - df['creation_date'] < 129600]
        print(df_filtered)

        q_stream_builder = []
        q_stream = []
        for idx in df_filtered.index:
            q_stream_builder.append(df_filtered['question_id'][idx])
            q_stream_builder.append(df_filtered['title'][idx])
            q_stream_builder.append(df_filtered['body'][idx])
            q_stream.append(q_stream_builder.copy())
            q_stream_builder.clear()
        # for q in q_stream:
        #     await poster.run(q)
        yield q_stream
        time.sleep(100)
    print('Error: Did not receive a response')


async def post_answer(page, content):
    dummy_answer = 'Hi! This question about \"' + \
                   content['ques'] + \
                   '\" has probably been answered earlier.\n\nHere is a link that might be helpful:\n\nhttps://stackoverflow.com/questions/tagged/git'
    await page.type('textarea[id=wmd-input]', dummy_answer, {'delay': 20})
    await page.click('button[id=submit-button]')
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


async def _run(q=_q):
    _q = q
    browser = await launch(
        {"headless": False, "args": ["--no-sandbox", "--disable-web-security"]})
    page = await initiate_login(browser, NCSU_SO_URL)
    page = await login(page)
    contentBuilder['id'] = _q[0]  # await getID()
    contentBuilder['ques'] = _q[1]  # await getIDBody()
    contentBuilder['qdetails'] = _q[2]
    await page.goto(page.url + '/' + str(contentBuilder['id']),
                    {'waitUntil': 'networkidle0'})
    page = await post_answer(page, contentBuilder)
    time.sleep(0.5)
    # await page.close()
    # await page.waitForNavigation()


async def run():
    asyncio.get_event_loop().run_until_complete(_run(_q))


if __name__ == '__main__':
    run()