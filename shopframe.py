"""
Data frame for handling shop data

"""
import datetime
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
            self.df = pd.read_csv(self.csv_file, na_filter=False)
        except IOError: 
            print "IO Error: Cannot open file", self.csv_file

    def add_data_point(self, user, comm, typex, date, ammount):
        """ Creates a new df with input data and append it to 
            current data frame.  
        """
        # types[4:] excludes User/Comm/Date/Tags
        temp_data = [user, comm, int(date), ''] + [0]*len(self.types[4:])
        try:
            ind = self.types.index(typex)
        except ValueError:
            print "Unkown class " + typex
        else:
            temp_data[ind] = ammount
            temp_df = pd.DataFrame([temp_data], columns=self.types)
            self.df = self.df.append(temp_df, ignore_index=True)
            # Add to file
            self.df.to_csv(self.csv_file, index=False)
            return 0

    def get_grand_total(self, **kwargs):
        """ Get grand frame total """
        if 'user' in kwargs:
            mask = (self.df['user'] == kwargs['user'])
            # types[4:] excludes User/Comm/Date/Tags
            grand_total = self.df.loc[mask, self.types[4:]].sum()
        else:    
            # Total from the columns which have shopping ammounts
            # types[4:] excludes User/Comm/Date/Tags
            grand_total = self.df.loc[:, self.types[4:]].sum()
        return grand_total
    
    def get_total_by_date(self, **kwargs):
        """ Get frame total in a date range """
        if ('min_date' in kwargs) and ('max_date' in kwargs):
            if 'user' in kwargs:
                # Creates a filtered data frame for the specified data range and user
                mask = (self.df['date'] >= int(kwargs['min_date'])) &\
                       (self.df['date'] <= int(kwargs['max_date'])) &\
                       (self.df['user'] == kwargs['user']) 
            else: 
                # Creates a filtered data frame for the specified data range
                mask = (self.df['date'] >= int(kwargs['min_date'])) &\
                       (self.df['date'] <= int(kwargs['max_date']))
        else:
            return "ERROR in slicing DF. Need to specify min_date and max_date"
        new_df = self.df.loc[mask]
        # Total from the columns which have shopping ammounts
        # types[4:] excludes User/Comm/Date/Tags
        grand_total = new_df.loc[:, self.types[4:]].sum()
        return grand_total
    
    def set_tag(self, tag):
        """ Set a new tag in the tags column """
        self.df['tags'] = [x + tag for x in self.df['tags']]
        # Add to file
        self.df.to_csv(self.csv_file, index=False)
    
    def del_tag(self, tag):
        """ Remove a given tag in the tags column """
        self.df['tags'] = [x.replace(tag, '') for x in self.df['tags']]
        # Add to file
        self.df.to_csv(self.csv_file, index=False)
    
    def get_tag(self, tag):
        """ Get a tag from the tags column - return date"""
        full_dates = self.df['date'].loc[self.df['tags'].str.contains(tag)]
        #month_year = ', '.join(set([str(x)[0:6] for x in full_dates]))
        if len(full_dates) > 0:
            return str(max(full_dates))
        else:
            return ''
    
    def get_comm(self):
        """ Get a list of commands for current month """
        timenow = datetime.date.today()
        min_date = str(timenow.year) + '{:02d}'.format(timenow.month) + '01'
        max_date = str(timenow.year) + '{:02d}'.format(timenow.month) + '31'
        mask = (self.df['date'] >= int(min_date)) &\
               (self.df['date'] <= int(max_date))
        #comm = self.df['comm'].loc[mask]
        comm = self.df[['date','comm']].loc[mask]
        # Remove empty entries
        filt = comm['comm'] != ""
        comm = comm[filt]
        return comm
