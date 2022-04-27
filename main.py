import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

Q_15_COLUMNS = slice(30, 39)
CATEGORIAL_COLUMN_LABLE = '12.takes care of pd patients'
raw_data = pd.read_excel(r'C:\Users\Idan\Shira survey\data_headers_update.xlsx')


def process_4and5_votes(data: pd.DataFrame):
    # slice the required data:
    # relevant_data = data[column_headers]

    #sub_question_labels = []
    rate_of_4_and_5_answers = []

    for column in data:
        #sub_question_labels.append(relevant_data[column].name)
        requested_rates = get_rate_of_4and5s(column, data)
        rate_of_4_and_5_answers.append(requested_rates)

    return rate_of_4_and_5_answers


def get_rate_of_4and5s(column, relevant_data):
    #TODO change method input to a series
    values_count = relevant_data[column].value_counts()
    number_of_all_answers = values_count.sum()
    number_of_4_5_answers = 0
    try:
        number_of_4_5_answers += values_count[4]
    except KeyError:
        print(f"no answers 4 on column {relevant_data[column].name}")
    try:
        number_of_4_5_answers += values_count[5]
    except KeyError:
        print(f"no answers 5 on column {relevant_data[column].name}")
    return number_of_4_5_answers / number_of_all_answers

# Todo: unused plot function
# def plot_results_of_4_5_rates(labels, rates, q_number):
#     xticks = np.arange(1, len(labels)+1)
#     plt.bar(x=xticks, height=rates)
#     plt.ylabel('rates of 4/5 answer')
#     plt.title(f"question {q_number} rates of 4 or 5 answers")
#     plt.xticks(xticks, labels, color='orange', rotation=45, fontweight='bold',
#                fontsize='10', horizontalalignment='right')
#     plt.tight_layout()
#     plt.savefig(r"C:\Users\Idan\Shira survey\q_15_important_factors.pdf")
#     plt.show()


# def aggregate_df_for_4_5s_rates(df: pd.DataFrame):
#     answer = []
#     for column in df:
#         rate_for_col = get_rate_of_4and5s(column, df)
#         answer.append(rate_for_col)
#     return pd.series(answer)

#------------- group by column 12 (has pd patients)---------


def group_interest_data_frame_by_indicator_column(dataframe: pd.DataFrame,
                                                  interest_column: pd.Series,
                                                  columns_to_perform_on: list):
    relevant_question_only_columns = dataframe.columns.tolist()[columns_to_perform_on]
    relevant_question_data = raw_data[relevant_question_only_columns]
    relevant_question_data[interest_column.name] = dataframe[interest_column.name]
    # return the groupby object
    return relevant_question_data.groupby(interest_column.name)
    # grpby_yes = grpby.get_group('כן')
    # grpby_no = grpby.get_group('לא')
    # return list(grpby_yes, grpby_no, interest_column_label)


categorial_column = raw_data[CATEGORIAL_COLUMN_LABLE]
question_data_grouped_by_some_categorial_column = group_interest_data_frame_by_indicator_column(raw_data,
                                                                                        categorial_column,
                                                                                        Q_15_COLUMNS)
# for each item of the groupby object:
# 1.   remove the grouped by column and reset index:
# 2.   apply 4and5 rates counter (what is the output?)
result_dict = {}
for key, item in question_data_grouped_by_some_categorial_column:
    print(f"\nworking on key:{key}")
    temp_df_item = item.drop(labels=[CATEGORIAL_COLUMN_LABLE], axis=1).reset_index().drop(labels='index', axis=1)
    result_dict[key] = process_4and5_votes(temp_df_item)

# for key, val in result_dict.items():
#     print(f"key:{key}:")
#     print(f"rates list:{val}\n")

# grpby_yes_wo_haspd_column = grpby_yes.drop(labels='haspd', axis=1).reset_index() # Drop the unnecessary boolean column + reset index
# grpby_no_wo_haspd_column = grpby_no.drop(labels='haspd', axis=1).reset_index()

# TODO: The second argument is redundant
# (columns, yes_data) = process_4and5_votes(grpby_yes_wo_haspd_column,grpby_yes_wo_haspd_column.columns)
# dict_from_lists = dict(zip(columns, yes_data))                      # Why do I create this dictionary?
# del dict_from_lists['index']
# rates_haspd_df_q15 = pd.DataFrame(dict_from_lists, index=[0])       # Why do I turn this into DataFrame
# rates_haspd_df_q15['has_pd_patients'] = 'Yes'

# TODO: The same for "no data"
# (columns, no_data) = process_4and5_votes(grpby_no_wo_haspd_column, grpby_no_wo_haspd_column.columns)
# dict_from_lists = dict(zip(columns, no_data))
# del dict_from_lists['index']
# rates_not_haspd_df_q15 = pd.DataFrame(dict_from_lists, index=[0])
# rates_not_haspd_df_q15['has_pd_patients'] = 'No'


# rates_concated_to_display = pd.concat([rates_haspd_df_q15, rates_not_haspd_df_q15]) # Concatenation of 2 DataFrames:
# lists = rates_concated_to_display.values.tolist()                                   # Transform to a list
# to_display_yes = lists[0]
# to_display_no = lists[1]
# to_display_yes.remove("Yes")
# to_display_no.remove("No")
#
# Display 2 lists with pyplot.bar - pack it in a display function + separate the data from the ploting requirements
width = 0.3
category_counter = 0
for category, data in result_dict.items():
    plt.bar(np.arange(len(data)) + width * category_counter, data, width=width)
    category_counter += 1

# plt.bar(np.arange(len(to_display_yes)), to_display_yes, width=width)
# plt.bar(np.arange(len(to_display_no)) + width, to_display_no, width=width)
plt.ylabel('rates of 4/5 answer')
plt.title('rates of 4/5 answer for has or doesn\'t have pd patients')
labels = raw_data.columns.tolist()[Q_15_COLUMNS]
xticks = np.arange(len(labels))
# labels = column_labels.tolist()
# labels.remove('has_pd_patients')
plt.xticks(xticks, labels, color='orange', rotation=45, fontweight='bold',
                 fontsize='10', horizontalalignment='right')
plt.tight_layout()

#-------------legend:
colors = {'Yes': 'blue', 'No': 'orange'}
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
plt.legend(handles, labels)

#plt.savefig(r"C:\Users\Idan\Shira survey\q_15_important_factors.pdf")
plt.show()




#print(f"type: {type(gby_yes)}\nthe df:\n{gby_yes}")




#sum_grouped_by = data_grpby_has_pd_patients.apply(lambda x: x.sum())
#print(sum_grouped_by)



#test for q15:
#--------------------------------------------------------------------------------
# q_15_keys = raw_data.columns.tolist()[30:39]
# data_pair = process_and_print_highest_rates(raw_data,q_15_keys)
# plot_results_of_4_5_rates(labels=data_pair[0], rates=data_pair[1], q_number=15)


#test for q13
#q_13_keys = data.columns.tolist()[17:29]
#data_pair = process_and_print_highest_rates(q_13_keys)
#plot_results_of_4_5_rates(labels=data_pair[0], rates=data_pair[1], q_number=13)