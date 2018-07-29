#!/home/lucas/anaconda2/bin/python
"""
Reset DF in CSV
"""

import pandas as pd

data = ['user1', 20180707, '', 0,0,0,0,0]
df = pd.DataFrame([data], columns = ['user', 'date', 'tags', 'food', 'home','bar','travel','misc'])
df.to_csv('gotbot.csv', index=False)
