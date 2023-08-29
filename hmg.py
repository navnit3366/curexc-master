import exrates
import datetime
import sys
import matplotlib.pyplot as plt
import os
import calendar
from pandas import date_range



def inputdate(date_text):
    '''function that inputs a date, in a vaild format,
        using python datatime module'''
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def valid_number(number, high):
    
    '''function that valid number as int, and under max value,  
    '''
    if number and number.isdigit():
        if int(number) <= high:
          return True
        else:
          sys.stderr.write("\nsomthing went wrong! are you sure its a logical year? - try again listing to instractions this time\n")
          return False

def main():
    
    '''
        inputs two integers - year and mouth.later, it inputs currencies code.
        the program is builting a graph,
        of the month and the currencies change in percentage relative to the USD 

    '''
    while True:
        try:
            #getting the current year
          now_year = datetime.datetime.now().year
          #input the year, and vaild it
          year = input("Type in the year with four digits: ")

          #assuming no dates befor 2000 has history
          while valid_number(year, now_year) == False or year.isdigit()==False or int(year)< 2000:
              year = input("somthing wen't wrong....\n Type in the year with four digits: ")
          
          #getting the current month
          now_month = datetime.datetime.now().month
          #input the month, and vaild it
          month =  input("Type in the month with two digits: ")


          while valid_number(month, now_month) == False or month.isdigit()==False:                
        
                
                month = input("somthing wen't wrong....\n Type in the month with two digits: ")

          #the currect month is yet to publish all the exchange rate, therefor a edge case.....
          while int(year)==int(now_year) and int(month)>= int(now_month):
              print("funny! you tried seeing the future?! try again....")   
                
              month = input("somthing wen't wrong....\n Type in the month with two digits: ")
              while valid_number(month, now_month) == False or month.isdigit()==False:                
        
                
                month = input("somthing wen't wrong....\n Type in the month with two digits: ")

          #vaild the currencies
          currencies=exrates.get_currencies()
          currency_lst=str(input("enter currency codes: separate them with comma (,)\n"))
          currency_fix_lst=currency_lst.upper().split(",")

          #remove spaces
          currency_fix_lst = [cur.strip(' ') for cur in currency_fix_lst]

          #only 3 values key for currency, and making sure the currency exists
          while all(currency.strip(" ") not in currencies for currency in currency_fix_lst)==True:
            #as requested to use
            sys.stderr.write("\nsomthing went wrong! are you sure its a vaild currency? - try again\n")

            #input the currencies requested again, if cur dosent exists
            currency_lst=str(input('try entering a comma-separated code and space\n i.e. "ILS, USD" is the correct format\n'))
            currency_fix_lst=currency_lst.upper().split(",")

            #remove spaces
            currency_fix_lst = [cur.strip(' ') for cur in currency_fix_lst]

          #getting the file name for later - creation of file
          file_name=input("in which name you wish to save the graph?: \n")
      
          year=int(year)
          month=int(month)
      
          #start day as the first of each month, end date as the last
          start_dateF =  datetime.date(year, month, int(1))
          end_dateF = datetime.date(year, month, int(calendar.monthrange(year,month)[-1]))
                
                
          #creating pandas database
          daterange = date_range(start_dateF, end_dateF)
      
             
          #for each currency, loop by date, to fill all the delta between the dates above
          for each_currency in currency_fix_lst:

              #deleting empty space for a vaild format
              each_currency=each_currency.strip(" ")
          
              if each_currency in currencies:

                #getting the rates of the day
                exrates_base=exrates.get_exrates(start_dateF.strftime("%Y-%m-%d"))

                #list of x values to the plt - dates
                date_val= []

                #list of y values to the plt - currencies values
                exchange_val= []

                #loop over dates, using oandas module
                for date in daterange:
              
                  #as long as the date in a vaild logical stracture
                  date_str = date.strftime("%Y-%m-%d")

                  #get the exchange rates for the date in the correct format
                  exrates_date=exrates.get_exrates(date_str)

                  #list of dates in month
                  date_val.append(date.strftime("%Y-%m-%d"))
              
                  if each_currency in exrates_base and each_currency in exrates_date:
                    diff_val = (float(exrates_date[each_currency])/float(exrates_base[each_currency]) -1)*100
                    exchange_val.append(diff_val)
                
                  else:
                    exchange_val.append(0)
                
                  #moving to the next values, to save the previous
                  exrates_base = exrates_date
            
                #creating the graph for each currency, with label
                plt.plot(exchange_val, label = each_currency)
            
      
      
      
          #plot creating
          
                       
          #setting x values regarding the date entered earlier
          plt.xlim(0,calendar.monthrange(year,month)[-1])

          #nicer visuallisation for the graph
      
          plt.grid(True)
          plt.title('History of one Month Graph changes')
          plt.legend()
          plt.ylabel('Change in (%)')
          plt.xlabel('Days of : ' + str(year) + '/' + str(month))


          #saving the graph as .png file
          plt.savefig(os.path.join('data','{}.png'.format(file_name)))

          print('{}.png'.format(file_name) + ' was succesfully created!')
      
          break
      
        except ValueError as V:
            print(V)
      



main()


