# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'

#%%
import pandas as pd
import plot
import preprocess
import stats_test
import numpy as np

#%%
# Read csv files
data_op = pd.read_csv('W10_insert_fake.csv')
data_gr = pd.read_csv('W10_bubble_fake.csv')
data_11 = pd.read_csv('W11_prepare_fake.csv')
data_12_pre = pd.read_csv('W12_prepare_fake.csv')
data_12_pfm = pd.read_csv('W12_perform_fake.csv')
data = pd.read_csv('overall_fake.csv')
pd.set_option('display.max_colwidth', 1000)

#%%
# Preprocessing general to all experimental versions
data_list = [data_op, data_gr, data_11, data_12_pre, data_12_pfm]
data_names = ['W10_insert', 'W10_bubble', 'W11_prepare', 'W12_prepare', 'W12_perform']
data_dict = dict(zip(data_names, data_list))

X = ['motivate', 'metacognitive', 'friend', 'big', 'question', 'instructor', 
    'sentence', 'research', 'how']
X_extended = ['motivate', 'metacognitive', 'friend', 'big', 'question', 'instructor', 
    'sentence', 'research', 'how', 'W10_bubble', 'W11_prepare', 'W12_prepare']
old_exp = ['W10_insert', 'W10_bubble', 'W11_prepare']
non_bin = np.array([['motivate', 'research']])

#%% [markdown]
# # Statistical Significance

#%%
# Self-reported helpfulness
plot.explore(data, data_dict, X, 'expl_helpfulness', 
    'Self-reported helpfulness', max_plot_val=7, old_exp=old_exp, non_bin=non_bin)
#%%
stats_test.analyze(data, data_dict, X, 'expl_helpfulness', 'ttest', './', 
    old_exp=old_exp, non_bin=non_bin)

#%%
# Correct rate on a related problem
plot.explore(data, data_dict, X, 'correct_rate', 'Correct rate on related problem')

#%%
stats_test.analyze(data, data_dict, X, 'correct_rate', 'ttest', './', 
    old_exp=old_exp, non_bin=non_bin)

#%% 
# Time spent on answering the survey 
plot.explore(data, data_dict, X, 'Duration', 'Duration', max_plot_val=500, 
    boxplot=True, old_exp=old_exp, non_bin=non_bin)

#%%
# TODO should I exclude outliers?
#threshold = data['Duration'].quantile(0.75) * 2
#filtered = data[data['Duration'] < threshold]
#filtered_dict = preprocess.filter_dict(data_dict, 'Duration', threshold)
#stats_test.analyze(filtered, filtered_dict, X, 'Duration', 'Duration', 'ttest', './')
stats_test.analyze(data, data_dict, X, 'Duration', 'Duration', 'ttest', './', 
    old_exp=old_exp, non_bin=non_bin)

#%% 
# Quality (length) of explanation
threshold = 1
filtered = data[data['explanation_length'] > threshold]
filtered_dict = preprocess.filter_dict(data_dict, 'explanation_length', threshold, smaller=False)
plot.explore(filtered, filtered_dict, X, 'explanation_length', 'Length of explanations', 
    max_plot_val=400, boxplot=True, old_exp=old_exp, non_bin=non_bin)

#%%
# TODO should I exclude outliers?
#threshold = data['explanation_length'].quantile(0.75) * 2
#filtered = data[data['explanation_length'] < threshold]
#filtered_dict = preprocess.filter_dict(data_dict, 'explanation_length', threshold)
stats_test.analyze(filtered, filtered_dict, X, 'explanation_length', 'ttest', './', 
    old_exp=old_exp, non_bin=non_bin)
#stats_test.analyze(data, data_dict, X, 'explanation_length', 'ttest', './', old_exp=old_exp, non_bin=non_bin)

#%% 
# Proportion of people who wrote explanations
plot.explore(data, data_dict, X, 'has_explanation', 'Has explanation', 
    max_plot_val=0.5, old_exp=old_exp, non_bin=non_bin)

#%%
stats_test.analyze(data, data_dict, X, 'has_explanation', 'ztest', './', log=False, 
    old_exp=old_exp, non_bin=non_bin)

#%%
# Proportion of people who completed the survey
plot.explore(data, data_dict, X, 'Finished', 'Completion rate', max_plot_val=0.6, 
    old_exp=old_exp, non_bin=non_bin)

#%%
stats_test.analyze(data, data_dict, X, 'Finished', 'ztest', './', 
    old_exp=old_exp, non_bin=non_bin)

#%%
# Print the number of students assigned to each condition and 
# the number of students who completed the survey
for name, prob in data_dict.items():
    print(name.replace('_', ' ').title())
    relevant_X = preprocess.select_X(X, name)
    for x in relevant_X:
        if x in np.delete(non_bin, 0, axis=1): 
            # dummy variable of another factor
            continue
        elif name not in old_exp and x in non_bin[:,0]:
            # more than two levels
            message = x + ': '
            factor = np.where(non_bin[:,0] == x)[0][0]
            base_data = prob
            for level in non_bin[factor]:
                message += '{0} received "{1}" ({2} completed) vs '.format(len(prob[prob[
                    level] == 1]), level, len(prob[(prob[level] == 1) & (prob['Finished'] == 1)]))
                base_data = base_data[base_data[level] == 0]
            message += '{0} received none ({1} completed)'.format(len(base_data), len(base_data[
                base_data['Finished'] == 1]))
            print(message)
        else:
            print('{0}: {1} assigned ({2} completed) vs {3} not assigned ({4} completed)'.format(
                x, len(prob[prob[x] == 1]), len(prob[(prob[x] == 1) & (
                    prob['Finished'] == 1)]), len(prob[prob[x] == 0]), len(
                        prob[(prob[x] == 0) & (prob['Finished'] == 1)])))