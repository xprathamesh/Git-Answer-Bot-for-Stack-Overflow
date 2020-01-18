# Milestone: DEPLOYMENT

## Deployment Scripts

[Deployment Script Screencast](https://drive.google.com/file/d/19xmucy2qNHtUL1bSc2hb7OS8nEYzdcZ3/view?usp=sharing) demonstrating the implementation and use of configuration management tools in our project - Ansible.

[Screenshot \#1 of our deployment on Google Cloud's Compute Engine](https://drive.google.com/file/d/13UPgXL0WLZEFLVHxMrFUJNCvy_prtXoj/view?usp=sharing)

[Screenshot \#2 of our deployment on Google Cloud's Compute Engine](https://drive.google.com/file/d/1Skjq_sEaYxGP0gbR779aEUfh8-1rWcGf/view?usp=sharing)

The Bot and the StackOverflow datasets are deployed on the Google Cloud Platform. We have used Ansible for configuration management.
The yml script checks for the latest versions of the modules required for the bot. It also installs or updates the modules if required. Finally, it runs the StackOverflow.py to start the Bot process.

## Acceptance Tests

Since this bot resides on NCState StackOverflow Teams website, it does not require any test or TA credentials. Any user with an NCSU account and with access to the NCState StackOverflow can post GIT related questions on the forum which the bot will pick up and start building a response.  
There are few preconditions for the Bot to successfully post a reply and these conditions have been explained below for each use case:

### UC1

The first of our use cases describes how a single user will typically interact with our bot.
Note that this assumes that the user in question has access to the NCSU StackOverflow team.
In this scenario the user has a git-related question, and thus posts a question on the NCSU StackOverflow forum. 

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

#### Acceptance Criteria

1. An answer must be given by the bot in reply to the posted question.
2. The provided answer must be relevant to the posted query. 

#### Testing Steps

1. Navigate to the [NCSU StackOverflow homepage](https://stackoverflow.com/c/ncsu).
2. Login to this page using your existing StackOverflow account (or one with permissions to access this private team).
3. Upon successful login, click the "Ask Private Question" button.
4. Create a post by providing a title and body for a git-related question.
5. Ensure the "tags" field contains the **git** tag.
6. Post the question using the post button at the bottom.
7. Remain on the posted question's page for at least 3 minutes.
8. Refresh the page and ensure that an answer was posted in reply to the asked question.

### UC2

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

#### Acceptance Criteria

1. An answer must be given by the bot in reply to the posted question.
2. The provided answer must be relevant to the posted query.
3. A relevant example must be given in the provided answer's body.

#### Testing Steps

1. Navigate to the [NCSU StackOverflow homepage](https://stackoverflow.com/c/ncsu).
2. Login to this page using your existing StackOverflow account (or one with permissions to access this private team).
3. Upon successful login, click the "Ask Private Question" button.
4. Create a post by providing a title and body for a git-related question.
5. In the body of the post, include the keyword **example**.
6. Ensure the "tags" field contains the **git** tag.
7. Post the question using the post button at the bottom.
8. Remain on the posted question's page for at least 3 minutes.
9. Refresh the page and ensure that the answer posted by the bot contains an example related to the question asked.

### UC3

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

#### Acceptance Criteria

0. Both posted questions must be answered by the bot.
1. The provided answer for the first question posted must be given before the second posted question is answered.
2. After the first question is answered, a sufficient amount of time must pass before the second question is answered.

#### Testing Steps

1. Navigate to the [NCSU StackOverflow homepage](https://stackoverflow.com/c/ncsu).
2. Login to this page using your existing StackOverflow account (or one with permissions to access this private team).
3. Upon successful login, click the "Ask Private Question" button.
4. Create a post by providing a title and body for a git-related question.
5. Ensure the "tags" field contains the **git** tag.
6. Post the question using the post button at the bottom.
7. Return to the [NCSU StackOverflow homepage](https://stackoverflow.com/c/ncsu).
8. Create a separate post in the same manner as described above; as before, ensure that the **git** tag is present.
9. After submission, return to the first post created and await a reply from the bot.
10. After an answer has successfully been posted, navigate to the second question asked.
11. Await the posting of an answer from the bot.

## Final Code

Final code is present within this repo, with the main running file being [`run.py`](/run.py).
Database integrations are found within the [database module](/database), which comtains classes and methods for interfacing between BigQuery and our bot.
The primary class is [db_interface.py](/database/db_interface.py), which handles query generation and parsing of the return values in a manner consistent with our initial design specification.
All database elements can be found via the Google Cloud Console under the [Git Answer Bot project](https://console.cloud.google.com/home/dashboard?cloudshell=false&organizationId=760982978602&project=elated-nectar-258022).
This also contains our deployment platform as a Compute Engine instance.

Note that, due to free-tier restrictions on the Google Cloud platform, only a single additional member could be added.
Hence, we have added Dr. Parnin; please let us know if another teaching staff member would be preferable and we will gladly make the necessary alterations.

## Continuous Integration

We have created a seperate VM Instance on Google Cloud Platform for the purpose of Continuous Integration. There we have configured Jenkins and through that are running the Jenkins server. We have set up a job on Jenkins using SCM Polling that polls our project from our GIT repository periodically, whenever commits are made in the repo and runs the ['run.py'](/run.py) in the build.  

Here's the [link](https://drive.google.com/open?id=1q20dC-JyIuqYAZGXdtXeRRdtCjaEKbUE) of the Jenkins screencast.
