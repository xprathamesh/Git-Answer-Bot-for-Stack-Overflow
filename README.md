# Git Bot for Stack Overflow
### ExampleBot

### Project Milestone Documents
- [Design Milestone Documentation](./docs/DESIGN.md)
- [Bot Milestone Documentation](./docs/BOT.md)
- [Process Milestone Documentation](./docs/PROCESS.md)
- [Deploy Milestone Documentation](./docs/DEPLOY.md)
- [Report Milestone Documentation](./docs/REPORT.md)

### Team Members:
- Michael Suggs (mjsuggs)  
- Prathamesh Pandit (pppandi2)  
- Rishal Shah (rshah27)  
- Rohit Nair (rnair2)

### Deployment

Our bot has been deployed via Google Compute Engine, which hosts a remote VM instance on the Google Cloud servers.
The image in question was selected as an Ubuntu 18.04 image due to its relative recency and long-term support status, which lends to stability for extended operation.
Code is deployed to this platform directly from a Google Cloud Repository, which is a mirrored copy of our GitHub Enterprise code.

Configuration and deployment are handled via Ansible, which is run via the [main.yml](/main.yml) as follows: 
```
ansible-playbook main.yml -i inventory
``` 
This playbook handles the installation and updating of all necessary pip packages, as well as ensuring system services such as openssl are up to date.
Further, this downloads sets up the Chromium webdriver for use with pyppeteer which must be done before headless chrome can be used.
The bots operationsn is controlled via [`StackOverflowBot.py`](/StackOverflowBot.py), which handles the main question extraction loop used to poll for new git-tagged questions.
From this, [answer generation](answergenerator.py) is called to provide content for the bot to [post](poster.py).

Both of the aforementioned stages can be handled within [`run.py`](run.py); a simple Python 3.x script for running Ansible followed by spinning up our bot.
By making this script executable (via `chmod u+x run.py`), the script can be run by calling `./run.py` from within the root directory. 
