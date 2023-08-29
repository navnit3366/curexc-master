import exrates
import datetime
import sys
import pandas as pd
import os


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
    '''function that inputs a date, in a vaild format, using python datatime module'''

    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    
    except ValueError:
        return False

        
def main():
    '''to preform the main: inputs two dates, and codes of two currencies and a file name
        created a file of cscv of the given name.
        saves exchange rates on the given time period
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
                
            #vaild the currencies
            currencies=exrates.get_currencies()
            currency_lst=str(input("enter two currency codes: separate them with comma (,)\n"))
            currency_fix_lst=currency_lst.upper().split(",")

            #remove spaces
            currency_fix_lst = [cur.strip(' ') for cur in currency_fix_lst]

            
            while all(currency.strip(" ") not in currencies for currency in currency_fix_lst)==True:

                #as requested to use
                sys.stderr.write("\nsomthing went wrong! invalid currency - try again\n")
                            
                #input the currencies requested again, if cur dosent exists, one currect currency is enoght
                currency_lst=str(input('wait a Minute! are you sure its a vaild currency?\n try entering a comma-separated code \n i.e. "ILS, USD" is the correct format'))
                currency_fix_lst=currency_lst.upper().split(",")

                           
                

            #input the file requested name    
            file_name =input("choose a file name: ")
      
            
            with open(os.path.join('data','{}.csv'.format(file_name)), mode="wt", encoding="utf8") as file_name:
                file_name.write('Date,')

                
                for currency in currency_fix_lst:
                    
                    #deleting empty space for a vaild format
                    currency=currency.strip(" ")
                             
                    #write only the currencies available
                    if currency in currencies:              
                        file_name.write(str(currency))
                        file_name.write(",")

                #allowing new input for the loop       
                file_name.write("\n")

                #vaild the order of the input dates
                start_dateF, end_dateF = chron_time(start_date, end_date)
                
                
                #loop over dates, using oandas module
                daterange = pd.date_range(start_dateF, end_dateF)

                
                #loop by date, to fill all the delta between the dates above
                for date in daterange:
                    
                    #as long as the date in a vaild logical stracture
                    date_str = date.strftime("%Y-%m-%d")
                    exrates_date=exrates.get_exrates(date_str)


                    #insert to the file the requested values
                    file_name.write(str(date_str))
                    
                    #to each of the currency  
                    for currency1 in currency_fix_lst:
                    
                        #deleting empty space for a vaild format
                        currency1=currency1.strip(" ")
                        
                        if currency1 in currencies:                        
                            file_name.write(",")
                            if currency1 not in exrates_date:
                                file_name.write("-")
                            
                            else:
                                file_name.write(str(exrates_date[currency1]))
                          
                    #moving to the next value in the time periot requested
                    
                    file_name.write("\n")
                    print("successfully created! go to data folder to check")
                    
        except ValueError:
            #bad format Value
            print("ohh ohhh......Value Error - are you sure the date exists? try again...")
            continue
        
        else:
            break



main()

