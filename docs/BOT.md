## Bot Implementation

We have completed the following tasks with respect to the implementation of the bot:

* Fetching of unanswered GIT related questions from the NC State StackOverflow Teams account.
* High level Logic of identifying whether the question is a request for examples or a query related to an error.
* Creating the format for the answer and posting it on the Teams account using Pyppeteer module.

Our Bot resides and interacts with the StackOverflow forum. We have used Python modules like pandas, pyppeteer, asyncio, selenium-webdriver and json.

## Use Case Refinement
Based on our initial implementation and feedback, below are the updated Use Cases for our Bot along with the description of the changes:

```
Use Case: Give a possible answer to User's Query or Error that is related to GIT on NCSU Team StackOverflow.
1 Preconditions -
    User must have the permission to post question on NCState's Team StackOverflow.
2 Main Flow -
    The User posts their query on NCSU's StackOverflow.[S1]
    The bot listens to the questions related to Git posted by all users on StackOverflow Teams.[S2]
    The Bot generates an answer to the corresponding question.[S3]
    The solutions are posted by the bot on the user's question post.[S4]
3 Sub Flows -
    [S1] The User posts a question that contains errors or queries related to specific topics, with appropriate tags.
    [S2] The bot filters out all the questions posted on the StackOverflow Teams that have used the 'Git' tag.
    [S3] The bot creates a solution containing an explanation and a link to previously answered related questions from the StackOverflow Data Dump.
    [S4] The solution will be posted using the Python Pyppeteer module after a short indefinite time-period.
4 Alternative Flows -
    [E1] Unable to find solutions or 'Git' tag not present for the user's question, therefore the Bot does not post an answer.
```
#### Description of Changes

For this use-case, initially we were going to post the answer on the NC State StackOverflow Teams using the StackExchange API. But after trying to implement this, we found out that the API does not support "POST" requests to write an answer on the StackOverflow Teams. We can only fetch data from it. To resolve this issue, we used the Python Pyppeteer module to successfully post our generated answers on NC State StackOverflow Teams account. The module logs into the Teams account and then opens the page containing the question to be answered. It locates the "Your Answer" textbox and types in the answer for the question and then submits the answer.

```
Use Case: User's queries contain requests for examples for a particular Git command.
1 Preconditions -
    User must have the permission to post on NCState's Team StackOverflow.
2 Main Flow -
    User is unsure of a command use, and thus posts a question with relevant tags requesting for examples.[S1]
    The bot listens for questions relating to GIT commands.[S2]
    The bot will then provide examples as a solution to the user based on the provided query in the question [S3].
3 Subflows -
    [S1] User will request for examples using text (like give examples, how to) in the question along with appropriate command tags.
    [S2] Bot filters out the questions that contain GIT and GIT_command tags.
    [S3] Bot builds a solution containing examples and a brief explanation of the requested command.
    [S3] The bot posts the example as the answer using the Python Pyppeteer module.
4 Alternative Flows -
    [E1] Question posted does not contain GIT or GIT command tags.
    [E2] Examples for the command are not available, hence the bot does not answer.
```
#### Description of Changes

The Stack Exchange API does not provide write access for StackOverflow teams as mentioned in the previous description. So, when the user requests for example, the bot will post the example using browser automation with help from pyppeteer, which is an unofficial port for puppeteer. The example will be fetched from a dataset which contains stored examples for different GIT commands. This dataset is created using the Atlassian GIT documentation website.

```
Use Case: New questions are posted when the bot is working on solutions to other questions. This use case shows the capability of the bot to run indefinitely and to handle multiple questions correctly.
1 Preconditions -
    Multiple new questions have been posted and are waiting to be answered.
2 Main Flow -
    A new question has been posted before the bot has answered the previous question(s).[S1]
    If the new question is related to GIT, it would be added to the queue containing the set of unanswered questions.[S2]
    The bot will answer each question as per their queue position.[S3]
3 Subflows -
    [S1] Multiple new questions have been posted during the time the bot is working on an answer for another question.
    [S2] All the relevant GIT questions will be filtered out and added to the queue as per their time of posting.
    [S3] The bot will move through the queue and begin building solutions for the questions which are first in the queue and post them iteratively. Thus the bot reruns itself and answers the new questions in the next iteration.
4 Alternative Flows -
    [E1] No new GIT related question was posted.
```
#### Description of Changes

Updated this usecase to further explain the capability of the bot to handle multiple questions iteratively and to run the bot indefinitely.

## Selenium Testing

The Selenium code is test/selenium.py file. We have used Selenium to verify the post made by the bot using Pyppeteer.  
Pyppeteer is used to post answers on NC State Teams Stack Overflow. 

## Mocking Service Component

The Mocking code is present in test/Mocking.py. Mocking is used to mock services and data. In this component the bot instead of posting on the actual NC State Teams Stack Overflow, it uses a local html file of the actual website.

## Screencast
[Bot Screencast Video Link](https://drive.google.com/file/d/1k3CUEvOwwdfqu2RcsnUwMEk6YGrCUgHl/view?usp=sharing)
