import exrates
import datetime
import pandas as pd
import sys
import os

def design_table(table_Cur):
    '''using pandas module to desing the file created, analizes the change (%) in exchange rate during the time perio
    presenting the max and min values, and diff between them
    '''
    #creating the table
    table_Cur=table_Cur.describe()
    table_Cur=table_Cur.T

    #adding diff between max and min values
    table_Cur = table_Cur.assign(diff=pd.Series(table_Cur['max']-table_Cur['min']).values)

    #adding name for more friendly output
    table_Cur.index.name = 'Currencies \ extreme values in precents '

    #sorting as requested, by diff between correncies descending order
    
    table_Cur=table_Cur.sort_values(by='diff',  ascending = False)
    
    
    #deleting unrequested math calculations that pandas does by default
    del table_Cur['count']
    del table_Cur['mean']
    del table_Cur['std']
    del table_Cur['25%']
    del table_Cur['50%']
    del table_Cur['75%']


    print("\n Here is a table, with the extremes value in the given time periot :")
    
    #printing the table
    print(table_Cur[:-1])

    
    print("\n zero in the mininum/maximun value means there are days which the currency hasn't changed!")



def chron_time(start_date, end_date):
    '''chronologicly sort two dates, provided as input'''
    if start_date > end_date:
            end_dateTemp=start_date
            start_dateTemp=end_date
    else:
            end_dateTemp=end_date
            start_dateTemp=start_date
        
    return start_dateTemp, end_dateTemp

def inputdate(date_text):
    '''function that inputs a date, in a vaild format, using python datatime module
    '''
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    
    except ValueError:
        return False


def main():
    '''main to test the program - the program allowing the user to enter 2 dates,
    it then will calculate for each date between them the change in precents,
    and finally will print the extremes value in the given time periot 
    '''
    while True:
            try:
                    #input date parameters
                    start_date = input("enter the start date: ")
                    while inputdate(start_date)== False:
                        start_date = input(" ValueError! Let's give it another try! " + "\n" +" please enter a date:" + '\n'
                                                 + " i.e. 'YYYY-MM-DD' stracture, an exsample for a vaild format is 2017-03-11" + '\n')        
                        inputdate(start_date)
                        
                    end_date = input("enter the end date: ")
                    while inputdate(end_date)== False:
                            end_date = input(" ValueError! Let's give it another try! " + "\n" +" please enter a date:" + '\n'
                                                 + " i.e. 'YYYY-MM-DD' stracture, an exsample for a vaild format is 2017-03-11" + '\n')
                            inputdate(end_date)
                
                    #input the currencies requested
                    currency_lst=str(input("enter a comma-separated list of currency codes: "))
                    currency_fix_lst=currency_lst.upper().split(",")

                    #saving the currencies available using the module exrates
                    currency_file=exrates.get_currencies()

                    #remove spaces
                    currency_fix_lst = [cur.strip(' ') for cur in currency_fix_lst]

                    #vaildation for currencies entered, allowing capiral and lowers letters
                    if all(currency.strip(" ") not in currency_file for currency in currency_fix_lst)==True:
                            #as requested to use
                            sys.stderr.write("\nsomthing went wrong! invalid currency - try again\n")
                            continue
                          
                    with open(os.path.join('data','analyze request.csv'), mode="wt", encoding="utf8") as diff_file:

                            #begin writing in the file, the titles
                            diff_file.write('Date,')

                            for currency in currency_fix_lst:
                                                                    
                                    currency=currency.strip(" ")

                                    if currency in currency_file:
                                            diff_file.write(str(currency))
                                            diff_file.write(",")
                            #new line for the values    
                            diff_file.write("\n")
                            
                            #vaild the order of the input dates, with function
                            start_dateF, end_dateF = chron_time(start_date, end_date)
                            #loop over dates, using oandas module
                            daterange = pd.date_range(start_dateF, end_dateF)
                            #base to calculate all of the changes
                            exrates_base_date = exrates.get_exrates(start_dateF)

                            
		            #loop by date, to fill all the delta between the dates above
                            for date in daterange:
                                    #witdraw the rates for the requested date
                                    date_str = date.strftime("%Y-%m-%d")
                                    exrates_date=exrates.get_exrates(date_str)
                                    
                                    #insert to the file the requested values
                                    diff_file.write(date_str)
                    
                                    #to each of the currency
                                    for coin in currency_fix_lst:
                                            #deleting empty space for a vaild format
                                            coin=coin.strip(" ")
                                            
                                            
                                            if coin in currency_file:

                                                    
                                                    diff_file.write(",")
                                                    if coin in exrates_date and coin in exrates_base_date:

                                                            
                                                            diff = ((float(exrates_date[coin])/float(exrates_base_date[coin]))-1)*100
                                                            diff_file.write(str(diff))
                                                    else:
                                                            #if currency dossent exists it will write - as requested
                                                            diff_file.write("-")
                                    #moving the writing forward - new line for new date
                                    diff_file.write("\n")

                                    #saving last day list to calculate diff between each day and his previous...
                                    exrates_base_date = exrates_date
                    
                    user_date = pd.read_csv(os.path.join('data','analyze request.csv'),sep=',', encoding='utf8')
                    #using a function te create the table as required
                    design_table(user_date)
      
                    
            except ValueError:
                  
                    #bad format Value
                    print("ohh ohhh......Value Error - are you sure the date exists? try again...")

            except PermissionError:
                    print("the file is probbly open, close it beform preforming this program")
            else:
                    break



main()
                  
        
