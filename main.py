import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from column_alternator import ColumnAlternator
from publisher import Publisher

Q_15_COLUMNS = slice(30, 39)
Q_13_COLUMNS = slice(17, 29)
CATEGORIAL_COLUMN_LABEL = '12. Do you routinely treat PD patients '
CATEGORIAL_COLUMN_LABEL_VINTAGE = "3.vintage"
ALTERNATION_DICT_VINTAGE = {"מעל 15 שנים": "More then 15 years",
                            "1-5 שנים": "Less then 15 years",
                            "11-15 שנים": "Less then 15 years",
                            "6-10 שנים": "Less then 15 years",
                            }
raw_data = pd.read_excel(r'C:\Users\Idan\Shira_survey\Data_headers_update_28_04_2022.xlsx')


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


#categorial_column = raw_data[CATEGORIAL_COLUMN_LABLE]
#question_data_grouped_by_some_categorial_column = group_interest_data_frame_by_indicator_column(raw_data,
#                                                                                                categorial_column,
#                                                                                                Q_13_COLUMNS)
#result_dict = {}
#for key, item in question_data_grouped_by_some_categorial_column:
#    temp_df_item = item.drop(labels=[CATEGORIAL_COLUMN_LABLE], axis=1).reset_index().drop(labels='index', axis=1)
#    result_dict[key] = process_4and5_votes(temp_df_item)


def process_question_with_no_categorial(raw_data, question_columns: slice, break_long_descriptors_section):
    question_of_interest_columns = list(raw_data.columns[question_columns])
    question_of_interest_df = raw_data[question_of_interest_columns]
    modified_index = question_of_interest_columns

    # Calculate rates:
    rates_for_requested_question = [float(format(rate, ".2f"))*100 for rate in process_4and5_votes(question_of_interest_df)]

    # U can insert all descriptors modifications here:
    if break_long_descriptors_section:
        # For better printing results, add \n for long descriptor:
        modified_index[4] = "15e. Fear that their chance of getting a transplant\n is reduced by being on PD"

    q15_df = pd.DataFrame(rates_for_requested_question, index=modified_index)
    return q15_df


def process_question_with_categorial(raw_data, question_columns: slice, categorial_column_name: str, alternation_dict):
    # Alternate the requested column by shira's pre-given condition (see word doc)
    alternator = ColumnAlternator(raw_data, categorial_column_name, alternation_dict)
    alternator.alternate_df()

    # slice and prepare the requested column
    question_of_interest_columns = list(raw_data.columns[question_columns])
    question_of_interest_columns.append(categorial_column_name)
    question_of_interest_df = raw_data[question_of_interest_columns]

    # groupby the categorial column name (remember to deal with NA s)
    groupby_object = question_of_interest_df.groupby(by="3.vintage")
    result_dict = {}
    for key, item in groupby_object:
        temp_df_item = item.drop(labels=[categorial_column_name], axis=1).reset_index().drop(labels='index',                                                                                           axis=1)
        result_dict[key] = process_4and5_votes(temp_df_item)

    return result_dict



# Process Q13 and Q15 with categorials
# ----------------------------------------------------------------------------------------------------------------------
result_dict = process_question_with_categorial(raw_data, Q_13_COLUMNS, CATEGORIAL_COLUMN_LABEL_VINTAGE, ALTERNATION_DICT_VINTAGE)
pub13_wrt_vintage = Publisher(result_dict,
                              False,
                              "q13_wrt_vintage_plot.pdf",
                              "q13_wrt_vintage.csv",
                              list(raw_data.columns[Q_13_COLUMNS]),
                              CATEGORIAL_COLUMN_LABEL_VINTAGE)

pub13_wrt_vintage.publish_wrt_categorial()


# Processing Q15 and Q13 only (can be un-comma if wants to go again)
# ----------------------------------------------------------------------------------------------------------------------
# q15_processed = process_question_with_no_categorial(raw_data, Q_15_COLUMNS, True)
# q13_processed = process_question_with_no_categorial(raw_data, Q_13_COLUMNS, False)
#
# pub15 = Publisher(q15_processed,
#                 True,
#                 "plot_q15_no_wrt.pdf",
#                 "csv_q15_no_wrt.csv")
# pub15.publish()
#
# pub13 = Publisher(q13_processed,
#                 True,
#                 "plot_q13_no_wrt.pdf",
#                 "csv_q13_no_wrt.csv")
#
# pub13.publish()

# Display:
# ----------------------------------------------------------------------------------------------------------------------
width = 0.3
category_counter = 0
# for category, data in result_dict.items():
#     plt.bar(np.arange(len(data)) + width * category_counter, data, width=width)
#     category_counter += 1
# TODO:  Maybe ask for a user lables and titles?
plt.ylabel('rates of 4/5 answer')
plt.title('rates of 4/5 answer for has or doesn\'t have pd patients')
xlabels = raw_data.columns.tolist()[Q_13_COLUMNS]
xticks = np.arange(len(xlabels))
plt.xticks(xticks, xlabels, color='orange', rotation=45, fontweight='bold',
                 fontsize='10', horizontalalignment='right')
plt.tight_layout()

#-------------legend:
colors = {'Yes': 'blue', 'No': 'orange'}
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
plt.legend(handles, labels)

# Outputs:
#plt.show() # For debug
plt.savefig(r"C:\Users\Idan\Shira_survey\q_13_wrt_have_pd_patients.pdf")

result_dict["Yes"] = result_dict.pop("כן")
result_dict["No"] = result_dict.pop("לא")
result_table = pd.DataFrame(result_dict, index=xlabels)
result_table.plot.barh()
plt.show()

to_output = result_table.transpose(copy=True)
to_output.set_axis(xlabels, axis=1, inplace=True)
to_output.to_csv(r"C:\Users\Idan\Shira survey\q_13_wrt_have_pd_patients.csv")





#
