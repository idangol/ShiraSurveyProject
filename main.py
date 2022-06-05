import pandas as pd

from column_alternator import ColumnAlternator
from publisher import Publisher

# Constants: # TODO: import all constants from a utility file
# ----------
Q_15_COLUMNS = slice(30, 39)
Q_13_COLUMNS = slice(17, 29)

CATEGORIAL_COLUMN_LABEL_TREAT_PD_PATIENTS = '12. Do you routinely treat PD patients '
CATEGORIAL_COLUMN_LABEL_VINTAGE = "3.	Duration of practice"
CATEGORIAL_COLUMN_LABEL_NUMBER_OF_PD_PATIENTS = "7.	PD patients #"
CATEGORIAL_COLUMN_LABEL_MODALITY_OF_CHOICE = "17. Your dialysis modality of choice"
CATEGORIAL_COLUMN_LABEL_WORK_PLACE = "Work place"


ALTERNATION_DICT_VINTAGE = {"מעל 15 שנים": "More then 15 years",
                            "1-5 שנים": "Less then 15 years",
                            "11-15 שנים": "Less then 15 years",
                            "6-10 שנים": "Less then 15 years",
                            }
ALTERNATION_DICT_NUMBER_OF_PD_PATIENTS = {"מעל 20": "More then 20",
                                          "11-20": "Less then 20",
                                          "אין תכנית דיאליזה צפקית במוסד בו אני עובד": "Less then 20",
                                          "1-10": "Less then 20",
                                          }

ALTERNATION_DICT_TREAT_PD_PATIENTS = {"כן": "Has Pd patients",
                                      "לא": "Doesn't have Pd patients",
                                      }

ALTERNATION_DICT_MODALITY_OF_CHOICE = {"דיאליזה צפקית": "Pd ",
                                       "המודיאליזה במוסד": "Hemodialysis",
                                       "המודיאליזה ביתית": "Hemodialysis",
                                       }

ALTERNATION_DICT_MODALITY_OF_CHOICE_FULL = {"דיאליזה צפקית": "Pd ",
                                            "המודיאליזה במוסד": "Hemodialysis",
                                            "המודיאליזה ביתית": "Home hemo",
                                            }

ALTERNATION_DICT_WORK_PLACE = {"בית חולים ציבורי, יחידת דיאליזה בקהילה": "There is a community dialysis unit",
                               "בית חולים ציבורי, יחידת דיאליזה בקהילה, מרפאה בקופת חולים":
                                   "There is a community dialysis unit",
                               "יחידת דיאליזה בקהילה": "There is a community dialysis unit",
                               "יחידת דיאליזה בקהילה, מרפאה בקופת חולים": "There is a community dialysis unit",
                               "בית חולים ציבורי": "Public H without com. unit",
                               "בית חולים ציבורי, מרפאה בקופת חולים": "Public H without com. unit",
                               }
#raw_data = pd.read_excel(r'C:\Users\Idan\Shira_survey\Data_headers_update_28_04_2022.xlsx')
raw_data = pd.read_excel(r'C:\Users\Idan\Shira_survey\Survey_29_05_2022.xlsx')

# The research statistic: how many 4 and 5 answers out of all answers:
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


# Helper function:
def group_interest_data_frame_by_indicator_column(dataframe: pd.DataFrame,
                                                  interest_column: pd.Series,
                                                  columns_to_perform_on: list):

    relevant_question_only_columns = dataframe.columns.tolist()[columns_to_perform_on]
    relevant_question_data = raw_data[relevant_question_only_columns]
    relevant_question_data[interest_column.name] = dataframe[interest_column.name]

    return relevant_question_data.groupby(interest_column.name)


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
    alternator.delete_unnecessary_rows()

    # slice and prepare the requested column
    question_of_interest_columns = list(raw_data.columns[question_columns])
    question_of_interest_columns.append(categorial_column_name)
    question_of_interest_df = raw_data[question_of_interest_columns]

    # groupby the categorial column name (remember to deal with NA s)
    groupby_object = question_of_interest_df.groupby(by=categorial_column_name)
    result_dict = {}
    for key, item in groupby_object:
        temp_df_item = item.drop(labels=[categorial_column_name], axis=1).reset_index().drop(labels='index', axis=1)
        result_dict[key] = [float(format(rate, ".2f"))*100 for rate in process_4and5_votes(temp_df_item)]

    return result_dict


def process_and_publish_question_wrt(data: pd.DataFrame,
                                     question_of_interest_columns: slice,
                                     label_of_categorial_column: str,
                                     alternation_dict_for_categorial_column: dict,
                                     plot_name: str,
                                     csv_name: str):

    result_dict = process_question_with_categorial(data,
                                                   question_of_interest_columns,
                                                   label_of_categorial_column,
                                                   alternation_dict_for_categorial_column)
    result_df = pd.DataFrame(result_dict, index=list(data.columns[question_of_interest_columns]))
    pub = Publisher(result_df, plot_name, csv_name)
    #pub.publish()
    pub.publish_black_n_white(color=["#3D3939", "#807979"])


# Here starts the usage for the data analysis:
# ----------------------------------------------------------------------------------------------------------------------
# Process Q13 and Q15 with categorials
# ----------------------------------------------------------------------------------------------------------------------
# 1st category: vintage (column 4)
#---------------------------------
# process_and_publish_question_wrt(raw_data,
#                                  Q_13_COLUMNS,
#                                  CATEGORIAL_COLUMN_LABEL_VINTAGE,
#                                  ALTERNATION_DICT_VINTAGE,
#                                  "q13_wrt_vintage_plot.pdf",
#                                  "q13_wrt_vintage.csv", )
#
# process_and_publish_question_wrt(raw_data,
#                                  Q_15_COLUMNS,
#                                  CATEGORIAL_COLUMN_LABEL_VINTAGE,
#                                  ALTERNATION_DICT_VINTAGE,
#                                  "q15_wrt_vintage_plot.pdf",
#                                  "q15_wrt_vintage.csv", )

# 2st category: number of PD patients (column 4) - needed
# ---------------------------------
# process_and_publish_question_wrt(raw_data,
#                                  Q_13_COLUMNS,
#                                  CATEGORIAL_COLUMN_LABEL_NUMBER_OF_PD_PATIENTS,
#                                  ALTERNATION_DICT_NUMBER_OF_PD_PATIENTS,
#                                  "q13_wrt_number_of_pd_patients_plot.pdf",
#                                  "q13_wrt_number_of_pd_patients.csv")

# process_and_publish_question_wrt(raw_data,
#                                  Q_15_COLUMNS,
#                                  CATEGORIAL_COLUMN_LABEL_NUMBER_OF_PD_PATIENTS,
#                                  ALTERNATION_DICT_NUMBER_OF_PD_PATIENTS,
#                                  "q15_wrt_number_of_pd_patients_plot.pdf",
#                                  "q15_wrt_number_of_pd_patients.csv")


# 3rd category: Treats PD patients (column 12) - needed
# ---------------------------------
process_and_publish_question_wrt(raw_data,
                                 Q_13_COLUMNS,
                                 CATEGORIAL_COLUMN_LABEL_TREAT_PD_PATIENTS,
                                 ALTERNATION_DICT_TREAT_PD_PATIENTS,
                                 "q13_wrt_treats_pd_patients_plot.pdf",
                                 "q13_wrt_treats_pd_patients.csv")

process_and_publish_question_wrt(raw_data,
                                 Q_15_COLUMNS,
                                 CATEGORIAL_COLUMN_LABEL_TREAT_PD_PATIENTS,
                                 ALTERNATION_DICT_TREAT_PD_PATIENTS,
                                 "q15_wrt_treats_pd_patients_plot.pdf",
                                 "q15_wrt_treats_pd_patients.csv")

# 4th category: Modality of choice (column 40, q17)
# ---------------------------------
# process_and_publish_question_wrt(raw_data,
#                                  Q_13_COLUMNS,
#                                  CATEGORIAL_COLUMN_LABEL_MODALITY_OF_CHOICE,
#                                  ALTERNATION_DICT_MODALITY_OF_CHOICE,
#                                  "q13_wrt_modality_of_choice_plot.pdf",
#                                  "q13_wrt_modality_of_choice.csv")
#
# process_and_publish_question_wrt(raw_data,
#                                  Q_15_COLUMNS,
#                                  CATEGORIAL_COLUMN_LABEL_MODALITY_OF_CHOICE,
#                                  ALTERNATION_DICT_MODALITY_OF_CHOICE,
#                                  "q15_wrt_modality_of_choice_plot.pdf",
#                                  "q15_wrt_modality_of_choice.csv")

# 5th category: Work place (column 5)
# ---------------------------------
# process_and_publish_question_wrt(raw_data,
#                                  Q_13_COLUMNS,
#                                  CATEGORIAL_COLUMN_LABEL_WORK_PLACE,
#                                  ALTERNATION_DICT_WORK_PLACE,
#                                  "q13_wrt_work_place_plot.pdf",
#                                  "q13_wrt_work_place.csv")
#
# process_and_publish_question_wrt(raw_data,
#                                  Q_15_COLUMNS,
#                                  CATEGORIAL_COLUMN_LABEL_WORK_PLACE,
#                                  ALTERNATION_DICT_WORK_PLACE,
#                                  "q15_wrt_work_place_plot.pdf",
#                                  "q15_wrt_work_place.csv")

# Processing Q15 and Q13 only (can be un-comma if wants to go again)
# ----------------------------------------------------------------------------------------------------------------------
# q15_processed = process_question_with_no_categorial(raw_data, Q_15_COLUMNS, False)
# q13_processed = process_question_with_no_categorial(raw_data, Q_13_COLUMNS, False)
#
#pub15 = Publisher(q15_processed,
                  # "plot_q15_no_wrt.pdf",
                  # "csv_q15_no_wrt.csv")
# #pub15.publish()
#pub15.publish_black_n_white(color = "#009999")
#
# pub13 = Publisher(q13_processed,
#                   "plot_q13_no_wrt.pdf",
#                   "csv_q13_no_wrt.csv")
#
# #pub13.publish()
# pub13.publish_black_n_white(color = "#009999")

# Processing Q17 (with modality you recommend) with respect to categories of q12 (do you treat PD)
# ----------------------------------------------------------------------------------------------------------------------
# q17_alternator = ColumnAlternator(raw_data, CATEGORIAL_COLUMN_LABEL_MODALITY_OF_CHOICE,
#                                   ALTERNATION_DICT_MODALITY_OF_CHOICE_FULL )
# q12_alternator = ColumnAlternator(raw_data, CATEGORIAL_COLUMN_LABEL_TREAT_PD_PATIENTS,
#                                   ALTERNATION_DICT_TREAT_PD_PATIENTS)
# q17_alternator.alternate_df()
# q12_alternator.alternate_df()
#
# questions_of_interest = raw_data[[CATEGORIAL_COLUMN_LABEL_TREAT_PD_PATIENTS,
#                                   CATEGORIAL_COLUMN_LABEL_MODALITY_OF_CHOICE]]
# grpby = questions_of_interest.groupby(CATEGORIAL_COLUMN_LABEL_TREAT_PD_PATIENTS)
# res_dict = {}
# for key, item in grpby:
#     temp_df_item = item.drop(labels=[CATEGORIAL_COLUMN_LABEL_TREAT_PD_PATIENTS], axis=1).reset_index().drop(labels='index', axis=1)
#     res_dict[key] = (temp_df_item.value_counts()/len(temp_df_item)*100).astype(int)
#
# res_df = pd.DataFrame(res_dict).reset_index()
# res_df["Index"] = ["Hemodialysis", "Home hemo", "Pd"]
# res_df.set_index("Index", inplace=True)
# res_df.drop(labels=CATEGORIAL_COLUMN_LABEL_MODALITY_OF_CHOICE, axis=1, inplace=True)
# ax = res_df.plot.bar(title="Chosen dialysis modality by has Pd patients", ylabel="%")
# plt.title = "Chosen dialysis modality by has Pd patients"
# plt.tight_layout()
# plt.show()


