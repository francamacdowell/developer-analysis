#!/usr/bin/env python
# coding: utf-8

# # Developers' Software Metrics Analysis

# Projects used in this analysis:
#  * [__Elasticsearch__](https://github.com/elastic/elasticsearch)
#  * [__okhttp__](https://github.com/square/okhttp)
#  * [__signal-android__](https://github.com/signalapp/Signal-Android)
#  * [__bazel__]()
#  * [__guava__]()
#  * [__netty__]()
#  * [__presto__]()
#  * [__rxjava__]()
#  * [__spring-boot__]()
#  
#  <font color='red'>__Note__: For each project, doesn't have all commits. Have commits with __SM__ missing due to configurations commits.</font>

# ## Getting started
# 
# Importing needed libs:

# In[2]:


import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json
from tqdm import tqdm


# In[ ]:


#projects_list = os.listdir('/home/macdowell/pesquisa/developer_analysis/developers_data/bug_reports_validated/')
#for project in projects_list:
project = 'netty'
datapath = '/home/macdowell/pesquisa/developer_analysis/developers_data/bug_reports_validated/' + project + '/metrics_' + project + '.csv'

# Reading developer metrics:
df = pd.read_csv(datapath)

# Dropping all columns less HASH, BUGGY and NATURE:
df.drop(df.columns.difference(['hash','buggy','nature']), 1, inplace=True)

# Getting list of nature:
natures = df.nature.unique()

# Filtering by commit nature:
for nature in tqdm(natures):
    print(nature + " Analysis: ")
    method_result = None
    class_result = None
    first = True

    sm_by_nature = df[df['nature'].str.contains(nature)]
    
    # Getting total lenght of the commits:
    hash_len = len(sm_by_nature['hash'])

    # Iterating over each nature commits':
    for h in sm_by_nature['hash']:
        # Checking if commits exists:
        if os.path.isfile('/home/macdowell/pesquisa/SM_data/' + project + '/' + h + '.csv'):

            sm_data = pd.read_csv('/home/macdowell/pesquisa/SM_data/' + project + '/' + h + '.csv')

            # Filtering by methods and classes SM:
            method_sm_data = sm_data[sm_data['Kind'].str.contains('ethod')]
            class_sm_data = sm_data[sm_data['Kind'].str.contains('lass')]

            # Dropping string columns:
            method_sm_data = method_sm_data.drop(['Kind', 'Name', 'File'], axis=1)
            class_sm_data = class_sm_data.drop(['Kind', 'Name', 'File'], axis=1)
            
            # Get the avarage in the commit:
            class_avg = class_sm_data.sum()/len(class_sm_data)
            method_avg = method_sm_data.sum()/len(method_sm_data)

            if first:
                class_result = class_avg
                method_result = method_avg
                first = False
            else:
                class_result += class_avg
                method_result += method_avg
    
    # Get the avarage of all commits:
    class_result = class_result / hash_len
    method_result = method_result / hash_len
    
    #Output result file:
    class_result.to_csv('/home/macdowell/pesquisa/developer_analysis/results/' + project + '_' + nature + '_classes.csv')
    method_result.to_csv('/home/macdowell/pesquisa/developer_analysis/results/' + project + '_' + nature + '_methods.csv')

