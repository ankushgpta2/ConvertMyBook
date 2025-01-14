import os
import re
import pandas as pd
import numpy as np
import csv
import json



class DataExploration():
    def __init__(self):
        # initial exploration / stats 
        self.number_of_recs = 0
        self.fields_to_get_count = ["merchantName", "merchantCountryCode", "posEntryMode", "posConditionCode", "merchantCategoryCode", "acqCountry", "cardPresent",
                                    "cardCVV", "enteredCVV", "transactionType", "expirationDateKeyInMatch", "isFraud"]
        self.nan_counts = {}
        self.field_min_max = {"creditLimit": (0,0), "availableMoney": (0,0), "currentBalance": (0,0), "transactionAmount": (0,0), "transactionDateTime": (0,0), "currentExpDate": (0,0), 
                              "accountOpenDate": (0,0), "dateOfLastAddressChange": (0,0)}
        # create log file for exploring data 
        self.base_path_for_logs = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'analysis')
        for filename in ['null_count_min_max_log.csv', 'unique_value_counts.json']:
            self.create_log_file(os.path.join(self.base_path_for_logs, filename))
            # write the header for csv 
            if filename == 'null_count_min_max_log.csv':
                with open(os.path.join(self.base_path_for_logs, 'null_count_min_max_log.csv'), 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Field Name', 'Number of Nulls', 'Min', 'Max'])
    


    # get summary statistics on data
    def initial_exploration(self, cleaned_data, unique_number_of_fields):
        """
        """
        # set class attributes to passed in data 
        self.unique_number_of_fields = unique_number_of_fields

        # get the number of records 
        self.number_of_recs = len(cleaned_data)
        print(f"\n\nTotal # of Non-Empty Records in Transactions.txt Dataset Is: {self.number_of_recs}\n")

        # display number of fields 
        if len(self.unique_number_of_fields) == 1:
            print(f"All Records Have Same # of Fields: {self.unique_number_of_fields[0]}")
        else:
            print(f"Records vary in the # of fields with the following values: {self.unique_number_of_fields}")

        # get the counts for certain fields5
        self.field_counts = {field: cleaned_data[field].value_counts() for field in self.fields_to_get_count}

        # update log data 
        log_data = {
            'General': {
                'Number of Records': self.number_of_recs,
                'Unique Number of Fields Per Record': self.unique_number_of_fields,
                'Number of Unique Values Per Field': {
                }
            }
        }
        for field in self.field_counts:
            # convert to dictionary 
            converted_field_count = self.field_counts[field].to_dict()
            # store necessary information for JSON
            log_data[field] = converted_field_count
            log_data['General']['Number of Unique Values Per Field'][field] = len(converted_field_count)

        # write to json file
        with open(os.path.join(self.base_path_for_logs, 'unique_value_counts.json'), 'a') as file:
            json.dump(log_data, file, indent=4)
        
        # cycle through all fields and count # of nans + store in field counts AND get min/max potentially
        for field in cleaned_data.columns.tolist():

            # count number of NaNs and store it
            self.nan_counts[field] = cleaned_data[field].isna().sum()

            # check if you need to get min/max 
            if field in self.field_min_max.keys():

                # change to correct format / data type prior to finding minimum and maximum
                if field == 'currentExpDate':
                    cleaned_data[field] = pd.to_datetime(cleaned_data[field], format='%m/%Y')
                elif field in ['accountOpenDate', 'dateOfLastAddressChange', 'transactionDateTime']:
                    cleaned_data[field] = pd.to_datetime(cleaned_data[field])
                else:
                    # make sure that field is in numeric 
                    cleaned_data[field] = pd.to_numeric(cleaned_data[field], errors='coerce')

                # get minimum/maximum
                self.field_min_max[field] = (cleaned_data[field].min(), cleaned_data[field].max())
        
                # update the csv file
                csv_entry = [field, self.nan_counts[field], self.field_min_max[field][0], self.field_min_max[field][1]]
            else:
                # update the csv file
                csv_entry = [field, self.nan_counts[field], 'N/A', 'N/A']

            # update the csv file
            with open(os.path.join(self.base_path_for_logs, 'null_count_min_max_log.csv'), 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(csv_entry)
    


    def create_log_file(self, path_to_file):
        """
        """
        # check if file already exists, if so, then delete it 
        if os.path.isfile(path_to_file):
            os.remove(path_to_file)
        # create the new file
        with open(path_to_file, mode='w') as file:
            file.close()



class DuplicateTransactions():
    def __init__(self):
        # time threshold for timeframe transactions need to be within to be considered multi-swipe
        self.time_threshold_for_dup = 5     # in minutes 
        # dataset attribute initialization for post duplicate identification
        self.cleaned_data_dup_ids = pd.DataFrame()

    def find_dup_transactions(self, cleaned_data):
        """
        """
        # identify duplicates from multi-swipe 
        self.cleaned_data_dup_ids = self.identify_reversal_dup_transactions(self.identify_multi_dup_transactions(cleaned_data))

    def identify_multi_dup_transactions(self, cleaned_data):
        """
        """
        # first convert to datetime from string 
        cleaned_data['transactionDateTime'] = pd.to_datetime(cleaned_data['transactionDateTime'])
        
        # second sort entire dataframe by accountNumber and timestamp
        cleaned_data = cleaned_data.sort_values(by=['accountNumber', 'transactionDateTime'])
        
        # calculate difference between all timestamps
        cleaned_data['timeDiff'] = cleaned_data['transactionDateTime'].diff()
        
        # separate all records that have less than 5 minute difference 
        cleaned_data['group'] = (cleaned_data['timeDiff'] > pd.Timedelta(minutes=self.time_threshold_for_dup)).cumsum()
       
        # put group ids in place
        cleaned_data['is_first_in_group'] = cleaned_data.groupby(['accountNumber', 'merchantName', 'group']).cumcount() == 0
        
        # filter out all records in group except for first one 
        duplicates_from_multi = cleaned_data[~cleaned_data['is_first_in_group']]

        # convert transactionAmount for total amount in duplicates
        duplicates_from_multi.loc[:, 'transactionAmount'] = pd.to_numeric(duplicates_from_multi['transactionAmount'])

        # print out results 
        print(f"\nNumber of Multi-Swipe Transactions (Based On {self.time_threshold_for_dup} Minutes): {len(duplicates_from_multi)}")
        print(f"Total Cost of Such Transactions: {np.round(duplicates_from_multi['transactionAmount'].sum(), 2)} Dollars\n")

        # drop columns 
        cleaned_data.drop(columns=['timeDiff', 'group'], inplace=True)

        return cleaned_data

    def identify_reversal_dup_transactions(self, cleaned_data):
        """
        """
        # sort the dataframe
        cleaned_data = cleaned_data.sort_values(by=['accountNumber', 'merchantName', 'transactionDateTime'])

        # identify reversals by creating shifted version of dataframe (to compare each row with the next)
        cleaned_data['nextTransactionType'] = cleaned_data['transactionType'].shift(-1)
        cleaned_data['nextTransactionAmount'] = cleaned_data['transactionAmount'].shift(-1)
        cleaned_data['nextAccountNumber'] = cleaned_data['accountNumber'].shift(-1)
        cleaned_data['nextMerchantName'] = cleaned_data['merchantName'].shift(-1)

        # now compare shifted version across fields 
        cleaned_data['isReversal'] = (
            (cleaned_data['transactionType'] == 'PURCHASE') &
            (cleaned_data['nextTransactionType'] == 'REVERSAL') &
            (cleaned_data['transactionAmount'] == cleaned_data['nextTransactionAmount']) &
            (cleaned_data['accountNumber'] == cleaned_data['nextAccountNumber']) &
            (cleaned_data['merchantName'] == cleaned_data['nextMerchantName'])
        )

        # get all records that are reversals 
        reversal_transactions = cleaned_data[cleaned_data['isReversal']]

        # convert transactionAmount for total amount in duplicates
        reversal_transactions.loc[:, 'transactionAmount'] = pd.to_numeric(reversal_transactions['transactionAmount'])

        # print out results
        print(f"Number of Reversal Transactions: {len(reversal_transactions)}")
        print(f"Total Cost of Such Transactions: {np.round(reversal_transactions['transactionAmount'].sum(), 2)} Dollars\n\n")

        # drop columns 
        cleaned_data.drop(columns=['nextTransactionType', 'nextTransactionAmount', 'nextAccountNumber', 'nextMerchantName'], inplace=True)

        return cleaned_data

