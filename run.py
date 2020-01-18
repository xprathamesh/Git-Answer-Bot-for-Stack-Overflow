#!/usr/bin/env python3
from os import system
system('ansible-playbook main.yml -i inventory')
system('python3 StackOverflowBot.py')
