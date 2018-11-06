import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':

    plots = []
    projects = os.walk('../Brute Data')

    for path, trash, files in projects:

        if 'HikariCP.zip' in files:
            continue
        project_len = len(files)
        dev_list= []

        for file in files:
            splitted = file.split('_')
            dev_list.append(splitted[0])

        df = pd.DataFrame(dev_list, columns=['user'])
        df = pd.value_counts(df.user).to_frame().reset_index()
        df.columns = ['user', 'commits_number']
        df['commits_percent'] = round(np.multiply(df['commits_number'], 1 / project_len), 4)
        p_name = path.split('/')
        p_name = p_name[-1]
        print('\nProject: ' + p_name)
        print(path)
        print(df.head())
        print()
        top_five = df.head()
        top_five['commits_percent'].plot(kind='bar', title=p_name + ' Contributions percent')

# Note: For each project, doesn't have all commits, just commits with SM
# due to configurations commits.