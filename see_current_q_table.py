import json
from running_gridworld import Env, print_q_table
import time
import numpy as np

# Read the q_table
with open('q_table_5.json') as json_file:
    q_table = json.load(json_file)
print('read the q_table finished, begin to painting...')

# Draw the q_table
env = Env()
print_q_table(q_table, env)

# Pause for a while
time.sleep(100)