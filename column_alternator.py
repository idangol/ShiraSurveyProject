import pandas as pd

class ColumnAlternator:

    def __init__(self, df: pd.DataFrame, column_to_alternate: str, translate_dict: dict):
        """
        :param df: raw df
        :param column_to_alternate: string
        :param translate_dict: {original_val:new value for each value in the column}
        """
        self.raw_df = df
        self.column_to_alternate = column_to_alternate
        self.translate_dict = translate_dict
        #self.result_df = None

    def alternate_df(self):
        for key, value in self.translate_dict.items():
            self.raw_df.loc[self.raw_df[self.column_to_alternate] == key, self.column_to_alternate] = value




