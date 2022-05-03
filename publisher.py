import matplotlib.pyplot as plt
import pandas as pd


class Publisher:

    PATH = "C:\\Users\\Idan\\Shira_survey"
    XLABEL = "% of significant answers (4\\5)"

    def __init__(self, data: pd.DataFrame,plot_name: str, csv_name: str):
        self.data = data
        self.plot_full_path = self.PATH + "\\" + plot_name
        self.csv_full_path = self.PATH + "\\" + csv_name
        self.plot_name = plot_name

    def publish(self):
        # change header of the data and save a csv:
        #self.data["% of significant(4\\5s)answers"] = self.data.pop(0)
        self.data.to_csv(self.csv_full_path)

        self.data.plot.barh(title=self.plot_name.split(".")[0], ylabel=self.XLABEL)
        plt.tight_layout()
        plt.show() # adjust the plot visualization and save!



