import requests
import time
import os
import pandas as pd
import poster
import asyncio
import Credentials as c

url     = 'https://api.stackexchange.com/2.2/questions/no-answers?order=asc&sort=creation&tagged=git&filter=!9Z(-wwYGT&&site=stackoverflow&team=stackoverflow.com/c/ncsu&key='+c.secret['key']
headers = {
    'X-API-Access-Token': c.secret['AccessToken'],
    'Accept-Charset'    :'UTF-8'
}

async def question_Extractor():
    while(True):
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            break

        data = res.json()
        # print(data)
        cur_time            = time.time()
        df = pd.DataFrame.from_dict(data['items'], orient='columns')
        df.index.name       = 'id'
        # print(df)
        df_filtered = df[cur_time - df['creation_date'] < 1296000]
        q_stream_builder    = []
        q_stream            = []
        # print(df_filtered)
        for idx in df_filtered.index:
            q_stream_builder.append(df_filtered['question_id'][idx])
            q_stream_builder.append(df_filtered['title'][idx])
            q_stream_builder.append(df_filtered['body'][idx])
            q_stream_builder.append(df_filtered['owner'][idx]['display_name'])
            q_stream_builder.append(df_filtered['tags'][idx])
            #print(q_stream_builder[3])
            q_stream.append(q_stream_builder.copy())
            q_stream_builder.clear()

        # print(q_stream)
        print("Running....")
        if q_stream != []:
            print("Found New Question....")
            await poster.run(q_stream)
        time.sleep(120)
    print('Error: Did not recieve a response')


while(True):
    try:
        # print("Before credentials")
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = c.GOOGLE_APPLICATION_CREDENTIALS
        # print("Beginning loop")
        asyncio.get_event_loop().run_until_complete(question_Extractor())
    except Exception as e:
        print(e)
        continue
