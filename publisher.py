import matplotlib.pyplot as plt
import numpy as np
#plt.style.use('grayscale')

import pandas as pd


class Publisher:

    PATH = "C:\\Users\\Idan\\Shira_survey"
    XLABEL = "Percentage of significant answers"





    def __init__(self, data: pd.DataFrame,plot_name: str, csv_name: str):
        self.data = data
        self.plot_full_path = self.PATH + "\\" + plot_name
        self.csv_full_path = self.PATH + "\\" + csv_name
        self.plot_name = plot_name


    def publish(self):
        # change header of the data and save a csv:
        #self.data["% of significant(4\\5s)answers"] = self.data.pop(0)
        self.data.to_csv(self.csv_full_path)

        #self.data.plot.barh(title=self.plot_name.split(".")[0], ylabel=self.XLABEL)
        self.data.plot.barh(ylabel=self.XLABEL, legend=False)
        plt.xticks(ticks=[25, 50, 75, 100], labels=["25%", "50%", "75%", "100%"])
        plt.tight_layout()
        plt.show() # adjust the plot visualization and save!


    def publish_black_n_white(self, color, add_bar_labels):

        # Plot configs:
        plt.figure(figsize=(12, 5))
        plt.rc('ytick', labelsize=11)
        csfont = {'size': 12, 'weight': "bold"}
        plt.xlabel('ylabel', **csfont)

        index = self.data.index.tolist()
        if self.data.shape[1] > 1:
            # Plot data
            first_column_as_list = self.data.iloc[:, 0].tolist()
            second_column_as_list = self.data.iloc[:, 1].tolist()
            y_tic_locations = np.arange(len(first_column_as_list))
            bars1 = plt.barh(y_tic_locations + 0.2, first_column_as_list, height=0.4, color=color[0], edgecolor='black')
            bars2 = plt.barh(y_tic_locations - 0.2, second_column_as_list, height=0.4, color=color[1], edgecolor='black')
            plt.legend([bars1, bars2], [self.data.columns.values.tolist()[0], self.data.columns.values.tolist()[1]])
            plt.yticks(ticks=y_tic_locations, labels=index)

            if add_bar_labels:
                for i, v in enumerate(first_column_as_list):
                    plt.text(v + 0.5, i + 0.1, str(int(v)) + "%", color='black', fontsize='x-small' )
                for i, v in enumerate(second_column_as_list):
                    plt.text(v + 0.5, i - 0.3, str(int(v)) + "%", color='black', fontsize='x-small' )


        else:
            plt.barh(index, self.data[0], color=color)
            for i, v in enumerate(self.data[0]):
                plt.text(v + 0.25, i - 0.15, str(int(v)) + "%", color='black')

        plt.xlabel(self.XLABEL)
        plt.xticks(ticks=[25, 50, 75, 100], labels=["25%", "50%", "75%", "100%"])

        plt.tight_layout()
        plt.show()  # adjust the plot visualization and save!

