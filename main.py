import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

Q_15_COLUMNS = slice(30, 39)
CATEGORIAL_COLUMN_LABLE = '12.takes care of pd patients'
raw_data = pd.read_excel(r'C:\Users\Idan\Shira survey\data_headers_update.xlsx')


def process_4and5_votes(data: pd.DataFrame):
    rate_of_4_and_5_answers = []
    for column in data:
        requested_rates = get_rate_of_4and5s(column, data)
        rate_of_4_and_5_answers.append(requested_rates)
    return rate_of_4_and_5_answers


def get_rate_of_4and5s(column, relevant_data):
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


def group_interest_data_frame_by_indicator_column(dataframe: pd.DataFrame,
                                                  interest_column: pd.Series,
                                                  columns_to_perform_on: list):

    relevant_question_only_columns = dataframe.columns.tolist()[columns_to_perform_on]
    relevant_question_data = raw_data[relevant_question_only_columns]
    relevant_question_data[interest_column.name] = dataframe[interest_column.name]

    return relevant_question_data.groupby(interest_column.name)

# Here starts the usage for the data analysis:
# ----------------------------------------------------------------------------------------------------------------------


categorial_column = raw_data[CATEGORIAL_COLUMN_LABLE]
question_data_grouped_by_some_categorial_column = group_interest_data_frame_by_indicator_column(raw_data,
                                                                                                categorial_column,
                                                                                                Q_15_COLUMNS)

result_dict = {}
for key, item in question_data_grouped_by_some_categorial_column:
    temp_df_item = item.drop(labels=[CATEGORIAL_COLUMN_LABLE], axis=1).reset_index().drop(labels='index', axis=1)
    result_dict[key] = process_4and5_votes(temp_df_item)

# Display:
# ----------------------------------------------------------------------------------------------------------------------
width = 0.3
category_counter = 0
for category, data in result_dict.items():
    plt.bar(np.arange(len(data)) + width * category_counter, data, width=width)
    category_counter += 1
# TODO:  Maybe ask for a user lables and titles?
plt.ylabel('rates of 4/5 answer')
plt.title('rates of 4/5 answer for has or doesn\'t have pd patients')
labels = raw_data.columns.tolist()[Q_15_COLUMNS]
xticks = np.arange(len(labels))
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