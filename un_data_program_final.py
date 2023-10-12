# country_tech.py
# Final Project
# Students RA, ST


'''A terminal-based app for computing & printing UN stats on cell phones and internet usage...

This application loads 3 dataframes from the excel (.xlsx) provided: 
    1. total_cell_phones_by_country.xlsx
    2. percentage_population_internet_users.xlsx
    3. UN Codes.xlsx

The program loads and prepares the 3 datasets and then merges them into a single master dataframe
with a multi-index. The user is then prompted for inputs including the "UN Sub Region", the type of data 
(cell phones or internet usage) and then specific years of interest. The user is also given the opportunity to quit
the program at certain input prompts. User inputs are checked/validated at each stage of input. Once valid inputs
are obtained, data/stats/plots are generated.
 
Further details/specs are provided via our Project Report as well as the project git repository.
Program written/tested in Python version: 3.9.12
Run via terminal/command line: python un_country_tech_final.py
'''

# imports
from logging import exception
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def user_input(un_codes, years):
    '''user_input() function - prompts and checks/validates user inputs.
 
    Args:
        un_codes: dataframe (used in checking for valid un sub-region)
        years: list (years of relatively non-sparse data to be used from original datasets)

    Returns: ui (str), sub_reg (str), data_typ (string), year0 (int), year1 (int) 
    
    (ui: if contains "quit" program terminates // sub_reg: UN Sub-Region name // data_typ: name of data to be assessed // 
    year0: 1st specific year of interest of data // year1: 2nd specific year of interest of data)
    '''
    
    # overview of data and options user can make...
    print('\nThis program provides access to the following UN country tech data/stats organized by UN Sub-Region, Country, and year:\n\
        1. Total Cells Phones by Country\n\
        2. Percentage Population Internet Users\n')

    print('NOTES:\n1) User can quit at several prompts by entering "quit".\n2) Inputs are case in-sensitive.')
    print('3) Sub-regions can be selected by entering the correct labe/name or by numeric index provided.')
    print('4) Years entered identify specific years of data to be averaged for the data type selected.')

    # 1st user input prompt - asking if they want to continue or quit
    ui = input('Enter "quit" to exit the program, or any key to continue: \n').lower()
    
    #### create un_codes sub-dataframe for masking/validing input
    if ui != 'quit':
        # create/assign un_code df to a new df
        valid_subregion = un_codes
        # drop unnecessary country column
        valid_subregion.drop(columns='country', inplace=True)
        # drop duplicate sub-region names/rows
        valid_subregion.drop_duplicates(inplace=True)
        # sort new df and add new index
        valid_subregion.sort_values('un sub-region', axis=0, ascending=True, inplace=True, ignore_index=True)
        valid_subregion['un sub-region'] = valid_subregion['un sub-region'].str.lower()
        print('\nFor Reference: Valid UN sub-region names and index values:\n', valid_subregion, '\n')
    
    ### SUB-REGION ###
    # while loop with try/except block to handle/validate user input: UN sub-region
    # user can wuit, or enter valid sub-region via index number or label/name.
    sub_reg = ''
    eval = True
    while ui != 'quit' and eval == True:
        try:
            # input prompt
            sub_reg = input('Please enter a UN Sub-Region name or numeric index value: ').lower() 
            
            # create mask
            ui_mask = valid_subregion == sub_reg
            
            while eval == True:
                if ui_mask.any().any():
                    sub_reg = valid_subregion[valid_subregion[ui_mask]['un sub-region'].notna()].iloc[0,0]
                    print(sub_reg)
                    eval = False
                    
                elif int(sub_reg) in valid_subregion.index: # int cast doesn't hold within if conditional
                    sub_reg = valid_subregion.loc[int(sub_reg), 'un sub-region']
                    print(sub_reg)
                    eval = False
                else:
                    raise exception
        except:
            print("Invalid UN Sub-Region.\n")
            help = input('Enter "help" to see the UN Sub-Region table, or any other key to continue: ').lower()
            if help == "help":
                print('\nFor Reference: Valid UN sub-region names and index values:\n', valid_subregion, '\n')

    ### Data type ###
    # user can quit or enter '1' or '2' for the different data types
    data_typ = ''
    data_typ_eval = True
    while ui != 'quit' and data_typ_eval == True:
        try:
            data_typ = input('\nFor Cell Phone data enter "1", for Internet Usage (%) enter "2", or "quit" to exit: ').lower()
        
            while data_typ_eval == True:
                if data_typ == '1':
                    data_typ = 'number_cells'
                    print('Selection: number of cell phones data')
                    data_typ_eval = False
                elif data_typ == '2':
                    data_typ = 'internet_users'
                    print('Selection: internet users % data')
                    data_typ_eval = False
                elif data_typ == 'quit':
                    ui = 'quit'
                    break
                else:
                    raise exception
        except:
            print("Invalid data type. Please try again...")

    ### 1ST YEAR ###
    # user can quit or enter 1st year of specific data interest
    year0 = ''
    year_eval = True
    while ui != 'quit' and year_eval == True:
        try:
            year0 = input('\nEnter the 1st specific year of data for avarage calc: ').lower()

            while year_eval == True:
                if year0 == 'quit':
                    ui = 'quit'
                    break
                elif int(year0) in years:
                    year0 = int(year0)
                    print(year0, '\n')
                    year_eval = False
                else:
                    raise exception
        except:
            print('Invalid year entered. Please try again, or enter "quit" to exit...')

    ### 2ND YEAR ###
    # user can quit or enter 2nd year of specific data interest
    year1 = ''
    year1_eval = True
    while ui != 'quit' and year1_eval == True:
        try:
            year1 = input('Enter 2nd specific year of data for avarage calc: ').lower()

            while year1_eval == True:
                if year1 == 'quit':
                    ui = 'quit'
                    break
                elif int(year1) in years:
                    year1 = int(year1)
                    print(year1, '\n')
                    year1_eval = False
                else:
                    raise exception
        except:
            print('Invalid 2nd year entered. Please try again, or enter "quit" to exit...')


    #user inputs printed summary to be returned
    print('User inputs summary:')
    print("Quit? (or any key to continue): {}, UN Sub-Region: {}, Data: {}, Year 1: {}, Year 2: {}".format(ui, sub_reg, data_typ, year0, year1))
    
    # returns
    return ui, sub_reg, data_typ, year0, year1
    

def find_null(null_index,null_input,null_input2):
    """Masks the index'd array and then if there is a null variable will print out a statement, if no missing data is found a different statement will print
    Variables: null_index // null_input // null_input2"""
    mask_index=null_index.isnull().loc[pd.IndexSlice[null_input,:], pd.IndexSlice[null_input2,:]]
    km_index=null_index.loc[pd.IndexSlice[null_input,:], pd.IndexSlice[null_input2,:]]
    if (km_index.isnull().values.any()) == True:
        print("\nThere are values missing within the data, calculations were performed on the data assuming a zero value was present\n")
    else:
        print("No missing information found\n")

def main():
    '''main() function - point of entry for program execution.
    
    Function loads dataframes from excel files, then calls for user inputs. User inputs are fed back to main(), then find_null() function is called to check 
    for nulls in data, and then the data/stats are prepared/calculated and printed out.
    
    Args:    None

    Returns: None
    '''
    # pandas settings 
    # https://stackoverflow.com/questions/27117006/pandas-dataframe-display-without-dimensions   [Reference for pandas dataframe display without dimensions]
    pd.options.display.show_dimensions = False
    #pd.set_option('display.max_columns', 15)

    print("\n***************************** Final Project (Country Tech Data/Stats) *****************************\n")

    ####### Stage 1: Import, merge, and create dataframes #######
   
    print("Importing Country Tech data files and UN Codes and preparing dataframe...")

    #### cell phone dataframe
    # load data
    cells = pd.read_excel('total_cell_phones_by_country.xlsx')
    # drop duplicate rows if any
    cells.drop_duplicates(keep='first', inplace=True, ignore_index=True)
    # drop sparse data columns
    cells_col_drop = list(range(1975,1995)) + [2018, 2019]
    cells.drop(columns=cells_col_drop, inplace=True)
    # converted dataframe data to integers
    cells_int = cells.convert_dtypes(infer_objects=False, convert_string=False, convert_integer=True, convert_boolean=False, convert_floating=False)
    cells_int['country'] = cells_int['country'].str.lower()
    # show summary info for dataframe
    # print('Snapshot of cell phones by country data...\n', cells_int.head(), '\ndata rows, columns: ', cells_int.shape)

    #### internet user (%) dataframe
    # load data
    net_users = pd.read_excel('percentage_population_internet_users.xlsx')
    # drop duplicate rows if any
    net_users.drop_duplicates(keep='first', inplace=True, ignore_index=True)
    # drop sparse data columns
    net_users_col_drop = list(range(1975,1995)) + [2018, 2019]
    net_users.drop(columns=net_users_col_drop, inplace=True)
    net_users['country'] = net_users['country'].str.lower()
    # show summary info for dataframe
    # print('\nSnapshot of internet usage (%) by country data...\n', net_users.head(), '\ndata rows, columns: ', net_users.shape)
    
    #### UN Codes dataframe
    # load data
    un_codes = pd.read_excel('UN Codes.xlsx')
    # drop duplicate rows if any
    un_codes.drop_duplicates(keep='first', inplace=True, ignore_index=True)
    # make column labels lowercase and drop UN Region column
    un_codes.columns = un_codes.columns.str.lower()
    un_codes.drop(columns='un region', inplace=True)
    un_codes['un sub-region'] = un_codes['un sub-region'].str.lower()
    un_codes['country'] = un_codes['country'].str.lower()
    # show summary info for dataframe
    # print('Snapshot of UN Sub-Region codes and countries...\n', un_codes.head(), '\ndata rows, columns: ', un_codes.shape)
    
    #### Dataframe Merges 
    # 1st merge (cell phone and internet usage data)
    cells_net = pd.merge(cells_int, net_users, how="outer", on='country', left_on=None, right_on=None, left_index=False, right_index=False, sort=True, 
               suffixes=("_tot_cells", "_%_net_users"), copy=True)
    # drop duplicate rows if any
    cells_net.drop_duplicates(keep='first', inplace=True, ignore_index=True)
    # drop duplicate columns if any
    cells_net_temp = cells_net.T
    cells_net_temp.drop_duplicates(keep='first', inplace=True, ignore_index=False)
    cells_net_fin = cells_net_temp.T

    # 2nd merge (cell phone/internet usage data + UN codes)
    codes_cells_net = pd.merge(un_codes, cells_net_fin, how="outer", on='country', left_on=None, right_on=None, left_index=False, right_index=False, sort=True, copy=True)
    # drop duplicate rows if any
    codes_cells_net.drop_duplicates(keep='first', inplace=True, ignore_index=True)
    # drop duplicate columns if any
    codes_cells_net_temp = codes_cells_net.T
    codes_cells_net_temp.drop_duplicates(keep='first', inplace=True, ignore_index=False)
    codes_cells_net_fin = codes_cells_net_temp.T

    """Pivot table creation from 2 arrays, will merge them together and then drop duplicate columns. The merged dataframe will set index's and sort and then create a pivot table from the 'country' column
    Variables: Array1 // Array2"""
    pivot_df = pd.merge(un_codes, cells_int, how="outer", on='country', left_on=None, right_on=None, left_index=False, right_index=False, sort=True, copy=True)
    pivot_df.drop_duplicates(keep='first', inplace=True, ignore_index=True)
    pivot_temp = pivot_df.T
    pivot_temp.drop_duplicates(keep='first', inplace=True, ignore_index=False)
    pivot_temp = pivot_temp.T
    pivot_temp
    pivot_temp.set_index(['un sub-region', 'country'], inplace=True, verify_integrity=True)
    pivot_temp.sort_index()
    pivot_dft=(pivot_temp)
    pivot = (pd.pivot_table(pivot_dft,index=['country', 2017],columns=['un sub-region'],aggfunc=np.sum))
    pivot2=pivot.fillna(value=0)

    # create multi-index from UN subregion/country codes
    codes_cells_net_fin.set_index(['un sub-region', 'country'], inplace=True, verify_integrity=True)
    codes_cells_net_fin.sort_index()
    # create column multi-index
    years = list(range(1995, 2018))
    data = ['number_cells', 'internet_users']
    multi_col = pd.MultiIndex.from_product([data, years], names=['data', 'years'])
    # transpose dataframe to set column multi-index
    temp_df = codes_cells_net_fin.T
    temp_df.set_index(multi_col, inplace=True, verify_integrity=True, append=False)
    tech_df = temp_df.T
    # sort dataframe index
    tech_df.sort_index(inplace=True)
    # show summary info for ready-to use dataframe
    print('\nSnapshot of final merged dataframe with row and column multi-indexing:') 
    print('(Note: for better viewing, zooming out may be necessary to avoid row wrapping...)\n')
    print(tech_df.head(5), '\ndata rows, columns: ', tech_df.shape)


    ####### Stage 2: Request user input #######
    
    #Call user input function
    ui, sub_reg, data_typ, year0, year1 = user_input(un_codes, years)
    
    ###### Stage 3: operations / stats #######
    # https://stackoverflow.com/questions/16088741/pandas-add-a-column-to-a-multiindex-column-dataframe   [Reference for adding columns]
    
    if ui != 'quit':
        ### sub-region and datatype slice (years 1995-2017) ###
        # find_null(tech_df,user_input1,user_input2)
        find_null(tech_df,sub_reg,data_typ)
        add_df=tech_df.loc[pd.IndexSlice[sub_reg,:], pd.IndexSlice[data_typ,:]]
        print("***********************************************************Sub-Region & Data Type You Choose************************************************************\n")
        print(add_df, '\n')
        
        #Mean of the total years from 95 to 2017
        mean_df=tech_df.loc[pd.IndexSlice[sub_reg,:], pd.IndexSlice[data_typ,:]]
        print("**********************************************Mean of All Data From 1995 to 2017 for " + str(data_typ) +"*************************************************")
        print("\nMean of all the data from 1995 to 2017 for" + str(data_typ))
        print(mean_df.mean(axis=1))

        #Difference column for total increase in cell phones from 1995 to 2017
        #Reference for how to add columns to a multi-index: #https://stackoverflow.com/questions/16088741/pandas-add-a-column-to-a-multiindex-column-dataframe
        cell_diff=tech_df['number_cells',2017] - tech_df['number_cells',1995]
        tech_df['number_cells', "Cell Phone Difference"] = cell_diff
        int_diff=tech_df['internet_users',2017] - tech_df['internet_users',1995]
        tech_df['internet_users', "Internet Difference"] = int_diff
        print("*********************************************Adding Columns To The Dataframe for Differences From 1995 to 2017********************************************")
        print("\n")
        print(tech_df.head())
        print("\nChange Since 2017 and 1995")
        if data_typ == 'number_cells':
            print(tech_df.loc[pd.IndexSlice[sub_reg,:], pd.IndexSlice['number_cells',"Cell Phone Difference"]])
        else:
            print(tech_df.loc[pd.IndexSlice[sub_reg,:], pd.IndexSlice['internet_users',"Internet Difference"]])

        #Global Data From Merged Data Set
        #Mean of number of cell phones across all UN-Sub Regions in 2017
        number_df=tech_df.groupby(level=0).mean()
        print("\n***********************************************Mean of Number of Cell Phones across all UN Sub-Regions in 2017******************************************")
        print(number_df['number_cells',2017])
        #Total number of cell phones across all UN-Sub Regions in 2017
        number_df2=tech_df.groupby(level=0).sum()
        print("\n************************************************Total number of cell phones across all UN Sub Regions in 2017*******************************************")
        print(number_df2['number_cells', 2017])
        #Total number of Cell phones in the world under UN-Sub Regions in 2017
        print("\n*****************************************Total number of Cell phones in the world under UN-Sub Regions in 2017******************************************")
        print(number_df2['number_cells', 2017].sum())
        #Describe'd Data from Number_Cell Phones
        print("\n*********************************************************Describe'd Data from Number_Cell Phones********************************************************")
        print(number_df['number_cells'].describe())
        #Average From Two Columns The User Choose.
        print("\n**********************************************Average of your two choosen sub-region, data type and years***********************************************")
        print("Average of " + str(data_typ) + " in " + str(year0) + " and " + str(data_typ) + " in " + str(year1) + "\n")
        average_diff=(tech_df.loc[pd.IndexSlice[sub_reg,:], pd.IndexSlice[data_typ,year0]] + tech_df.loc[pd.IndexSlice[sub_reg,:], pd.IndexSlice[data_typ,year1]]) / 2
        print(average_diff)
        print("\n")
 

        #Pivot Table (Table was created above with the other dataframes)
        print("\n***********************************************************************Pivot Table**********************************************************************")
        print(pivot2.T)


        #Bar Plot 1
        graph_df=tech_df.loc[pd.IndexSlice[sub_reg], pd.IndexSlice['internet_users',2017]]
        print("\n************************************************************************Plot 1 Data*********************************************************************")
        print(graph_df)
        graph_df.plot(kind='bar',x=0,y=1,color='red',xlabel='Countries',ylabel='% of Users', title="Internet Users Per UN Sub-Region (%)",grid=True,legend=True,figsize=(12,8))


        #Showing and saving bar graph
        plt.savefig("Percent of Internet Users By Country.png")
        plt.show()
        

        #Pie Plot 2 Creation
        graph2_df=tech_df.loc[pd.IndexSlice[sub_reg], pd.IndexSlice['number_cells',2017]]
        print("\n************************************************************************Plot 2 Data**********************************************************************")
        print(graph2_df)
        graph2_df.plot(kind='pie',x=0,y=1,title="Number of Cell Phones Per UN Sub-Region",legend=True,figsize=(12,8))


        #Showing and saving pie plot
        plt.savefig("Number of Cell Phones By Country.png")
        plt.show()
        

        #Writing combined dataframe to excel
        tech_df.to_excel('Combined_Data_Frame.xlsx')
    
    print("\n****************** Final Project (Country Tech Data/Stats) - Program Terminated ******************\n")
    
if __name__ == '__main__':
    main()

    