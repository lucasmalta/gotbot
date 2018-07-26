#!/home/lucas/anaconda2/bin/pytho
"""
Data frame for handling shop data

"""
import pandas as pd

class ShopFrame(object):
    """ Class for handling shop data """

    def __init__(self, csv_file):
        """ Initialization """
        
        self.csv_file = csv_file
        self.df = pd.DataFrame()
        self.load_data()
        self.types = list(self.df)

    def load_data(self):
        """ Load data """
        try:
            self.df = pd.read_csv(self.csv_file)
        except IOError: 
            print "IO Error: Cannot open file", self.csv_file

    def add_data_point(self, user, typex, date, ammount):
        """ Creates a new df with input data and append it to 
            current data frame.  
        """
        temp_data = [user, date] + [0]*len(self.types[2:])
        try:
            index = self.types.index(typex)
        except ValueError:
            print "Unkown class " + typex
        else:
            temp_data[index] = ammount
            temp_df = pd.DataFrame([temp_data], columns=self.types)
            self.df = self.df.append(temp_df)
            # Add to file
            self.df.to_csv(self.csv_file, index=False)
            return 0

    def get_grand_total(self):
        """ Get grand frame total """
        # Total from the columns which have shopping ammounts
        # types[2:] excludes User/Date
        grand_total = self.df.loc[:, self.types[2:]].sum()
        return grand_total
    
    def get_total_by_date(self, min_date, max_date):
        """ Get grand frame total """
        # Creates a filtered data frame for the specified data range
        new_df = self.df.loc[(self.df['date'] >= int(min_date) ) &\
        (self.df['date'] <= int(max_date))]
        # Total from the columns which have shopping ammounts
        # types[2:] excludes User/Date
        grand_total = new_df.loc[:, self.types[2:]].sum()
        return grand_total
