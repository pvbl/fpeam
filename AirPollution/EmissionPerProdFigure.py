from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pylab import *  # @TODO: remove global scope import
import matplotlib.pyplot as plt
from scipy.stats import scoreatpercentile
import os


# @TODO: refactor to match PEP8 standards
# @TODO: refactor to use string formatting
# @TODO: fill out docstrings

class EmissionPerProdFigure(object):
    """

    """

    def __init__(self, cont):
        """
        Create emmision graphs per a acre..

        :param cont:
        :return:
        """

        self.path = cont.get('path')
        self.db = cont.get('db')
        self.document_file = "EmissionsPerProdFigure"

        # define inputs/constants:
        pollutant_labels = ['$PM_{10}$', '$PM_{2.5}$']
        # the order of the 2 list has to be the same.
        feedstock_list = ['Corn Grain', 'Switchgrass', 'Corn Stover', 'Wheat Straw',]# 'Forest Residue']  # @TODO: remove hardcoded values
        f_list = ['CG', 'SG', 'CS', 'WS']#, 'FR']  # @TODO: remove hardcoded values
        pollutant_list = ['pm10', 'pm25']  # @TODO: remove hardcoded values
        
        for p_num, pollutant in enumerate(pollutant_list):
            # -----------------EXTRACT DATA FROM THE DATABASE-----------------
            data_array = self.__collect_data__(feedstock_list, pollutant, f_list)
            # -----------------PART 2, PLOT DATA----------------------------------
            # pretty plotting things
            fig = plt.figure(figsize=(8, 6))
            canvas = FigureCanvas(fig)        
            self.ax1 = fig.add_subplot(111)
            # adjust this value to change the plot size
            # ----------------------------------------------------------------
            plt.subplots_adjust(left=0.15, right=0.99, top=0.95, bottom=0.1)
            # ----------------------------------------------------------------

            # -------create boxplot
            bp = plt.boxplot(data_array, notch=0, sym='', vert=1, whis=1000)

            plt.setp(bp['boxes'], color='black')
            plt.setp(bp['whiskers'], color='black', linestyle='-')
            # remove to get rid of log scale.
            # plt.yscale('log')
    
            plot_title = pollutant_labels[p_num]
            axis_title = '%s Emissions (mt fugitive dust / (dt for cellulosic, bushel for corn grain) feedstock)' % (pollutant_labels[p_num], )
            
            self.__set_axis__(plot_title, axis_title, data_array, f_list)    
            # plot 95% intervals 
            self.__plot_interval__(data_array)
    
            fig.savefig(os.path.join(self.path, 'Figures', 'EmissionsPerProd_' + pollutant + '.png'), format='png')
    
            print pollutant  # @TODO: convert to logger

    def __collect_data__(self, feedstock_list, pollutant, f_list):
        """

        :param feedstock_list:
        :param pollutant:
        :param f_list:
        :return:
        """
        data = []
        for fNum, feedstock in enumerate(feedstock_list):

            # emissions per production = (pollutant dt) / (total feedstock harvested dt)
            # emissions = pollutant / prod
            # @TODO: Should harv_ac > 0.0 be here? Should this be in the Options class to eliminate the problem in the first place.

            feed_abr = f_list[fNum]
            query = """
                SELECT (fug.""" + pollutant + """ / s.prod)
                FROM """ + self.db.schema + """.summedemissions AS s
                LEFT JOIN (
                    SELECT
                      """ + feed_abr + """_raw.fips,
                      SUM(""" + feed_abr + """_raw.""" + pollutant + """) AS """ + pollutant + """, description
                    FROM
                      """ + self.db.schema + """.""" + feed_abr + """_raw
                    WHERE description LIKE '%Fugitive dust%'
                    GROUP BY """ + feed_abr + """_raw.fips
                    ) fug ON fug.fips = s.fips
                WHERE s.feedstock LIKE '%""" + feedstock + """%' AND s.prod > 0.0 AND fug.description IS NOT NULL
                    """
            emissions = self.db.output(query, )
            data.append(emissions)

        return data

    def __plot_interval__(self, data_array):
        """

        :param data_array:
        :return:
        """

        num_feed = 4
        num_array = array([x for x in range(num_feed)]) + 1  # index starts at 1, not zero
            
        # plot 95% interval
        perc95 = array([scoreatpercentile(data_array[0], 95), scoreatpercentile(data_array[1], 95),
                        scoreatpercentile(data_array[2], 95), scoreatpercentile(data_array[3], 95)])
                          
        # plot 5% interval
        perc5 = array([scoreatpercentile(data_array[0], 5), scoreatpercentile(data_array[1], 5),
                       scoreatpercentile(data_array[2], 5), scoreatpercentile(data_array[3], 5)])
         
        plt.plot(num_array, perc95, '_', markersize=15, color='k')
        plt.plot(num_array, perc5, '_', markersize=15, color='k')
        
        # calculate mean and plot it.
        means = [mean(data_array[0]), mean(data_array[1]), mean(data_array[2]), mean(data_array[3])]
        plt.plot(num_array, means, '_', markersize=75, color='b')

    def __set_axis__(self, plot_title, axis_title, data_array, data_labels):
        """
        function to set axis titles and plot titles

        :param plot_title:
        :param axis_title:
        :param data_array:
        :param data_labels:
        :return:
        """
        # Add a horizontal grid to the plot
        self.ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.7)
                      
        # determine limits of axis
        # @TODO: refactor so users don't have to uncomment code to change plot
        # to view all, let it be logarithim scale: self.ax1.set_ylim(bottom=1e-07, top=1e-01)
        # to view sg, cs, and ws spread: self.ax1.set_ylim(bottom=1e-07, top=0.0002
        # to view cg spread: self.ax1.set_ylim(bottom=0.0002, top=.003)     
        # to view pm spread: self.ax1.set_ylim(bottom=1e-04, top=0.002)                  
        self.ax1.set_ylim(bottom=0.000005, top=0.0009)

        # Hide these grid behind plot objects
        self.ax1.set_axisbelow(True)

        self.ax1.set_ylabel(axis_title, size=10, style='normal')    

        self.ax1.set_xticklabels(data_labels, size=25, style='normal')

if __name__ == "__main__": 
    # from model.Database import Database
    # import Container
    #
    # title = 'sgNew'
    # cont = Container.Container()
    # cont.set('path', 'C:/Nonroad/%s/' % (title,))
    # cont.set('db', Database(title))
    #
    # # Emissions per a production lb figure.
    # print 'Creating emissions per lb figure.'
    # EmissionPerProdFigure(cont)
    raise NotImplementedError
