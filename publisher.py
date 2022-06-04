import matplotlib.pyplot as plt
#plt.style.use('grayscale')

import pandas as pd


class Publisher:

    PATH = "C:\\Users\\Idan\\Shira_survey"
    XLABEL = "% of significant answers (4\\5)"
    YLABEL_FONT = {'family' : 'sans-serif',
        'weight' : 'bold',
        'size'   : 14}




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


    def publish_black_n_white(self, color):

        # Plot configs:
        plt.figure(figsize=(12, 5))
        plt.rc('ytick', labelsize=11)
        csfont = {'size': 12, 'weight': "bold"}
        plt.xlabel('ylabel', **csfont)

        # Plot data
        index = self.data.index.tolist()
        value = self.data[0].tolist()

        plt.barh(index, value, align='center', color=color)
        plt.xlabel(self.XLABEL)
        plt.xticks(ticks=[25, 50, 75, 100], labels=["25%", "50%", "75%", "100%"])

        plt.tight_layout()
        plt.show()  # adjust the plot visualization and save!

