import matplotlib.pyplot as plt
import pandas as pd


class Publisher:

    PATH = "C:\\Users\\Idan\\Shira_survey"

    def __init__(self, data, is_horizontal_display, plot_name: str, csv_name: str, *args):
        self.data = data
        self.is_horizontal_display = is_horizontal_display
        self.plot_full_path = self.PATH + "\\" + plot_name
        self.csv_full_path = self.PATH + "\\" + csv_name
        if args:
            self.column_names = args[0]
            self.categorial_column_name = args[1]
        else:
            self.column_names = None
            self.categorial_column_name = None


    def publish(self):
        if type(self.data) is pd.DataFrame:
            self.publish_wo_rt()
        elif type(self.data) is dict:
            self.publish_wrt_categorial()


    def publish_wo_rt(self):
        """
        This method publishes plot and table to desired paths.
        It is assumed that the data recieved to publish is a DataFrame
        In that case the indices are assumed to be the question headers (or the original DF column names)
        :return: NA
        """
        # TODO: Ask for user titles
        # p_title = plt.title(input("Pls specify the whole plot title"))
        # p_xlabel = plt.xlabel(input("Pls specify the required header for the x axis:"))
        p_title = "q15"
        p_xlabel = "% of significant answers (4\\5)"
        ax = self.data.plot.barh(legend=False, title=p_title, xlabel=p_xlabel)
        # show labels on the end of the bars
        # TODO make the values text size smaller and design the plot
        #ax.bar_label(ax.containers[0])
        plt.tight_layout()
        # plt.show()
        plt.savefig(self.plot_full_path)

        # change header of the data and save:
        self.data["% of significant(4\\5s)answers"] = self.data.pop(0)
        self.data.to_csv(self.csv_full_path)


    def publish_wrt_categorial(self):
        """
        This methods plots a categorial bar plot - usually for 2 categories,
        but it can manage with any number.
        the data is given by a dict, the keys are the categories,
        the values are a lists of rates for each original column
        :return:
        """
        # TODO: Refactor. this is pretty much the same as with no respect to (only there is 1 more column)
        df_to_plot = pd.DataFrame(self.data)
        df_to_plot["columns"] = self.column_names
        df_to_plot.set_index("columns", inplace=True)
        ax = df_to_plot.plot.barh(title="wrt_vintage", xlabel="% of significant answers (4\\5)")
        # show labels on the end of the bars
        # TODO make the values text size smaller and design the plot
        #ax.bar_label(ax.containers[0])
        plt.tight_layout()

        # Make minor adjustments and save
        plt.show()

        # TODO Save csv



