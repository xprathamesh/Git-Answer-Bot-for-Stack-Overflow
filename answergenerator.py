import json
import re
import string
import nltk
from database.db_interface import *
# from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
stemmer                 = nltk.stem.porter.PorterStemmer()
remove_punctuation_map  = dict((ord(char), None) for char in string.punctuation)

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

async def containsExample(content):
    content_string  = content['ques']+' '+content['qdetails']
    content_string  = re.sub('<[^<]+?>', '', content_string)
    res             = re.sub('['+string.punctuation+']', '', content_string).split()

    ## Synonyms for Example - Needs testing
    # ex_synonyms = []
    # for syn in wordnet.synsets("good"):
    # for l in syn.lemmas():
    #     synonyms.append(l.name())

    example_synonyms = ['example', 'sample',
                        'instance', 'illustration', 'prototype']

    # if any(word in str(res).lower() for word in set(ex_synonyms)):
    if any(word in str(res).lower() for word in example_synonyms):
        return True
    else:
        return False

async def getExample(content):
    posting_answer = ''
    flag=False
    with open('git_examples.json', 'r', encoding='utf-8') as example_file:
        git_examples = json.load(example_file)

    tags_present = content['tags']
    if 'git' in tags_present:
        tags_present.remove('git')

    for data in git_examples:
        for tag in tags_present:
            if tag in data['command']:
                flag=True
                posting_answer = data['title'] + \
                    '\n' + data['description'] + '\n' + data['example_heading'] + '\n\n'
                for eg in data['example']:
                    posting_answer += eg['eg_title'] + '\n\n' + eg['eg_command'] + '\n' + eg['eg_description'] + '\n\n'
                posting_answer += 'For more information, visit: ' + data['link']
                break

        if(flag):
            break

    if (flag==False):
        for data in git_examples:
            if content['qdetails'].lower().find(data['command'])!=-1:
                posting_answer = data['title'] + \
                    '\n' + data['description'] + '\n' + data['example_heading'] + '\n\n'
                for eg in data['example']:
                    posting_answer += eg['eg_title'] + '\n\n' + eg['eg_command'] + '\n' + eg['eg_description'] + '\n\n'
                posting_answer += 'For more information, visit: ' + data['link']
                break

    return posting_answer

async def getDBAnswer(content):

    posting_answer      = ''
    tags_asked          = content['tags']
    answer_contenders   = []
    interface           = DatabaseInterface()
    q1                  = TableCols(uri='elated-nectar-258022.stackoverflow', table='git_tags', cols=['tag_name'])
    res                 = interface.generic_query(q1)
    all_tags            = res.values.tolist() # [[x for x in row] for row in res]
    max_sim             = 0.6  # threshold_value
    answer_contender    = ''

    for tag in tags_asked:
        # tagged = [tag]
        if [tag] in all_tags:
            # print(tag)
            table_tag = tag.replace('-','_')
            q3c = TableCols(uri='elated-nectar-258022.gitbot',
                            table=table_tag,
                            cols=['title','body','id'])
            q3w = [
                Cond('accepted_answer_id', 'IS NOT NULL', ''),
                Cond('score', '> 3', '')
            ]

            tagdat          = interface.generic_query(q3c, q3w)
            tagdat.columns  = ['_title','_body','_id']

            for index, data in tagdat.iterrows():
                qcontent = str(data['_title'])+str(data['_body'])
                question = str(content['ques'])+str(content['qdetails'])
                sim = cosine_sim(qcontent, question)
                # print(sim)
                if sim > max_sim:
                    max_sim = sim
                    answer_contender=str(data['_id'])
                    print(max_sim)
                    print(answer_contender)
                    if max_sim > 0.7:
                        break

    if answer_contender == '':
        return ''
    else:
        # answer = Select * from `elated-nectar-258022.stackoverflow.git_answers where id = answer_contender.accepted_answer_id
        posting_answer = 'This question has probably been answered earlier on the main StackOverflow website. Kindly have a look here:\n\n'+'https://stackoverflow.com/questions/'+answer_contender
        print(posting_answer)
        return posting_answer

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]
