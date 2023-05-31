'''data.py
Reads CSV files, stores data, access/filter data by variable name
Garam Choi
CS 251 Data Analysis and Visualization
Spring 2022
'''

import numpy as np
import csv


class Data:
    def __init__(self, filepath=None, headers=None, data=None, header2col=None, stringAllowed = False, enumAllowed = False, dateAllowed = False, numericAllowed = True):
        '''Data object constructor

        Parameters:
        -----------
        filepath: str or None. Path to data .csv file
        headers: Python list of strings or None. List of strings that explain the name of each
            column of data.
        data: ndarray or None. shape=(N, M).
            N is the number of data samples (rows) in the dataset and M is the number of variables
            (cols) in the dataset.
            2D numpy array of the dataset’s values, all formatted as floats.
            NOTE: In Week 1, don't worry working with ndarrays yet. Assume it will be passed in
                  as None for now.
        header2col: Python dictionary or None.
                Maps header (var str name) to column index (int).
                Example: "sepal_length" -> 0

        TODO:
        - Declare/initialize the following instance variables:
            - filepath
            - headers
            - data
            - header2col
            - Any others you find helpful in your implementation
        - If `filepath` isn't None, call the `read` method.
        '''
        if stringAllowed == False and enumAllowed == False and dateAllowed == False and numericAllowed == True:
            if(filepath == None):
                self.filepath = filepath
                self.headers = headers
                self.data = data
                self.header2col = header2col
            else:
                self.read(filepath)
        else:
            if(filepath == None):
                self.filepath = filepath
                self.headers = headers
                self.data = data
                self.header2col = header2col
            else:
                Allowed = []
                if stringAllowed == True:
                    Allowed.append(1)
                else: 
                    Allowed.append(0)
                if enumAllowed == True:
                    Allowed.append(1)
                else:
                    Allowed.append(0)
                if dateAllowed == True:
                    Allowed.append(1)
                else:
                    Allowed.append(0)
                if numericAllowed == True:
                    Allowed.append(1)
                else:
                    Allowed.append(0)
                self.readWithOthers(filepath,Allowed)
        pass

    def read(self, filepath):
        '''Read in the .csv file `filepath` in 2D tabular format. Convert to numpy ndarray called
        `self.data` at the end (think of this as 2D array or table).

        Format of `self.data`:
            Rows should correspond to i-th data sample.
            Cols should correspond to j-th variable / feature.

        Parameters:
        -----------
        filepath: str or None. Path to data .csv file

        Returns:
        -----------
        None. (No return value).
            NOTE: In the future, the Returns section will be omitted from docstrings if
            there should be nothing returned

        TODO:
        - Read in the .csv file `filepath` to set `self.data`. Parse the file to only store
        numeric columns of data in a 2D tabular format (ignore non-numeric ones). Make sure
        everything that you add is a float.
        - Represent `self.data` (after parsing your CSV file) as an numpy ndarray. To do this:
            - At the top of this file write: import numpy as np
            - Add this code before this method ends: self.data = np.array(self.data)
        - Be sure to fill in the fields: `self.headers`, `self.data`, `self.header2col`.

        NOTE: You may wish to leverage Python's built-in csv module. Check out the documentation here:
        https://docs.python.org/3/library/csv.html

        NOTE: In any CS251 project, you are welcome to create as many helper methods as you'd like.
        The crucial thing is to make sure that the provided method signatures work as advertised.

        NOTE: You should only use the basic Python library to do your parsing.
        (i.e. no Numpy or imports other than csv).
        Points will be taken off otherwise.

        TIPS:
        - If you're unsure of the data format, open up one of the provided CSV files in a text editor
        or check the project website for some guidelines.
        - Check out the test scripts for the desired outputs.
        '''
        self.data = []
        self.headers = []
        with open(filepath, newline = '') as csvfile:
            csvreader = csv.reader(csvfile,delimiter = ',')
            row_count = 0
            for row in csvreader:
                row_list = []
                if row_count == 0:
                    for header in row:
                        header = ''.join(header.split())
                        self.headers.append(header)
                elif row_count == 1 and 'numeric' in row:
                    new_headers = []
                    counter = 0
                    while(counter < len(row)):
                        datatype = ''.join(row[counter].split())
                        if(datatype == 'numeric'):
                            new_headers.append(self.headers[counter])
                        counter += 1
                    self.headers = new_headers
                elif row_count == 1 and 'numeric' not in row:
                    new_headers = []
                    counter = 0
                    while(counter <len(row)):
                        if self.is_float(row[counter]) != None:
                            row_list.append(self.is_float(row[counter]))
                            new_headers.append(self.headers[counter])
                        counter += 1
                    self.headers = new_headers       
                    self.data.append(row_list)
                else:
                    for i in row:
                        if(self.is_float(i) != None):
                            row_list.append(self.is_float(i))
                    self.data.append(row_list)
                row_count += 1
        self.headers = self.get_headers()
        self.header2col = self.get_mappings()
        self.filepath = filepath
        self.data = np.array(self.data)
        pass

    '''helper function to see if value can be parsed and if it can return said value'''
    def is_float(self, string_number):
        try:
            return float(string_number)
        except ValueError:
            pass 

    def __str__(self):
        '''toString method

        (For those who don't know, __str__ works like toString in Java...In this case, it's what's
        called to determine what gets shown when a `Data` object is printed.)

        Returns:
        -----------
        str. A nicely formatted string representation of the data in this Data object.
            Only show, at most, the 1st 5 rows of data
            See the test code for an example output.
        '''
        string = ""
        for header in self.headers:
            string += str(header) + " "
        string += "\n"
        if(self.data.shape[0] < 5):
            for row in self.data:
                for column in row:
                    string += str(column) + " "
                string += "\n"
        else:
            for x in range(5):
                for column in self.data[x]:
                    string += str(column) + " "
                string += "\n"
        return string
        

    def get_headers(self):
        '''Get method for headers

        Returns:
        -----------
        Python list of str.
        '''
        return self.headers
        pass

    def get_mappings(self):
        '''Get method for mapping between variable name and column index

        Returns:
        -----------
        Python dictionary. str -> int
        '''
        column_mapping = {}
        for i in self.headers:
            column_mapping[i] = self.headers.index(i)
        return column_mapping

    def get_num_dims(self):
        '''Get method for number of dimensions in each data sample

        Returns:
        -----------
        int. Number of dimensions in each data sample. Same thing as number of variables.
        '''
        return len(self.headers)
        

    def get_num_samples(self):
        '''Get method for number of data points (samples) in the dataset

        Returns:
        -----------
        int. Number of data samples in dataset.
        '''
        return len(self.data)

    def get_sample(self, rowInd):
        '''Gets the data sample at index `rowInd` (the `rowInd`-th sample)

        Returns:
        -----------
        ndarray. shape=(num_vars,) The data sample at index `rowInd`
        '''
        return self.data[rowInd,:]


    def get_header_indices(self, headers):
        '''Gets the variable (column) indices of the str variable names in `headers`.

        Parameters:
        -----------
        headers: Python list of str. Header names to take from self.data

        Returns:
        -----------
        Python list of nonnegative ints. shape=len(headers). The indices of the headers in `headers`
            list.
        '''
        header_indices = []
        for header in headers:
            header_indices.append(self.headers.index(header))
        return header_indices
        

    def get_all_data(self):
        '''Gets a copy of the entire dataset

        (Week 2)

        Returns:
        -----------
        ndarray. shape=(num_data_samps, num_vars). A copy of the entire dataset.
            NOTE: This should be a COPY, not the data stored here itself.
            This can be accomplished with numpy's copy function.
        '''
        return self.data.copy()

    def head(self):
        '''Return the 1st five data samples (all variables)

        (Week 2)

        Returns:
        -----------
        ndarray. shape=(5, num_vars). 1st five data samples.
        '''
        if(self.data.shape[0] < 5):
            return self.data
        else:
            return self.data[0:5,:]

    def tail(self):
        '''Return the last five data samples (all variables)

        (Week 2)

        Returns:
        -----------
        ndarray. shape=(5, num_vars). Last five data samples.
        '''
        if(self.data.shape[0] < 5):
            return self.data
        else:
            return self.data[-5:,:]

    def limit_samples(self, start_row, end_row):
        '''Update the data so that this `Data` object only stores samples in the contiguous range:
            `start_row` (inclusive), end_row (exclusive)
        Samples outside the specified range are no longer stored.

        (Week 2)

        '''
        self.data = self.data[start_row:end_row,:]
        pass

    def select_data(self, headers, rows=[]):
        '''Return data samples corresponding to the variable names in `headers`.
        If `rows` is empty, return all samples, otherwise return samples at the indices specified
        by the `rows` list.

        (Week 2)

        For example, if self.headers = ['a', 'b', 'c'] and we pass in header = 'b', we return
        column #2 of self.data. If rows is not [] (say =[0, 2, 5]), then we do the same thing,
        but only return rows 0, 2, and 5 of column #2.

        Parameters:
        -----------
            headers: Python list of str. Header names to take from self.data
            rows: Python list of int. Indices of subset of data samples to select.
                Empty list [] means take all rows

        Returns:
        -----------
        ndarray. shape=(num_data_samps, len(headers)) if rows=[]
                 shape=(len(rows), len(headers)) otherwise
            Subset of data from the variables `headers` that have row indices `rows`.

        Hint: For selecting a subset of rows from the data ndarray, check out np.ix_
        '''
        if rows == []:
            return self.data[:,self.get_header_indices(headers)]
        else:
            return self.data[np.ix_(rows,self.get_header_indices(headers))]

    '''Extension'''
    '''
    Used to parse 4 kinds of data: numeric,enum,date, and string. Used throug contrsuctor by saying if or if not allowed for each 
    datatype. Set in constructor as else statement if not allowed are given. 
    '''
    def readWithOthers(self, filepath, Allowed):
        self.data = []
        self.headers = []
        with open(filepath, newline = '') as csvfile:
            csvreader = csv.reader(csvfile,delimiter = ',')
            row_count = 0
            datatype_indices = []
            for row in csvreader:
                row_list = []
                if row_count == 0:
                    for header in row:
                        header = ''.join(header.split())
                        self.headers.append(header)
                elif row_count == 1 and len(Allowed) == 4:
                    new_headers = []
                    if(Allowed[0] == 1):
                        counter = 0
                        while(counter < len(row)):
                            datatype = ''.join(row[counter].split())
                            if(datatype == 'string'):
                                new_headers.append(self.headers[counter])
                                datatype_indices.append(counter)
                            counter += 1
                    if(Allowed[1] == 1):
                        counter = 0
                        while(counter < len(row)):
                            datatype = ''.join(row[counter].split())
                            if(datatype == 'enum'):
                                new_headers.append(self.headers[counter])
                                datatype_indices.append(counter)
                            counter += 1
                    if(Allowed[2] == 1):
                        counter = 0
                        while(counter < len(row)):
                            datatype = ''.join(row[counter].split())
                            if(datatype == 'date'):
                                new_headers.append(self.headers[counter])
                                datatype_indices.append(counter)
                            counter += 1
                    if(Allowed[3] == 1):
                        counter = 0
                        while(counter < len(row)):
                            datatype = ''.join(row[counter].split())
                            if(datatype == 'numeric'):
                                new_headers.append(self.headers[counter])
                                datatype_indices.append(counter)
                            counter += 1
                    self.headers = new_headers
                elif row_count == 1 and ('numeric' not in row or 'string' not in row or 'enum' not in row or 'date' not in row):
                    print("CSV File does not contain any datatype row. Please add datatype row to csv and try again.")
                else:
                    for number in datatype_indices:
                        row_list.append(row[number])
                    self.data.append(row_list)
                row_count += 1
        self.headers = self.get_headers()
        self.header2col = self.get_mappings()
        self.filepath = filepath
        self.data = np.array(self.data)
        pass 