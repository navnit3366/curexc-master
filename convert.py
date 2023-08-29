import exrates
import datetime
import sys





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
    '''function that inputs a date, in a vaild format,
        using python datatime module'''
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def convert_time_period(amount, first_cur, sec_cur, start_date, end_date):
    '''
       function that returns the orgenized  format of data.
       the data is the exchange rates of time period provided to the function 
    '''
    
    #format for display
    date_format = "%Y-%m-%d"
    
    #sorting the dates using function above
    start_F, end_F = chron_time(datetime.datetime.strptime(start_date, date_format), datetime.datetime.strptime(end_date, date_format))
    
    delta = end_F - start_F
    
    #def dictionery 
    data = {}
    
    #loop to fill the logical values 
    for day in range(delta.days + 1):

        #for ech day in range, calculates the exchange rate 
        date_of_currency = start_F + datetime.timedelta(days=day)

        
        
        rate1 = exrates.convert(amount, first_cur, sec_cur, date_of_currency.strftime(date_format))
        rate2 = exrates.convert(amount, sec_cur, first_cur, date_of_currency.strftime(date_format))

        data[date_of_currency.strftime(date_format)] = [rate1, rate2]

    return data

def main():
    '''
        main program that inputs two dates, an amount, and codes of two currencies.
        it then prints a table, with the amount converted between those currencies, in both directions

    '''
    while True:
        try:
            
            #input values, the time preiod to convert, the amount and the currencies
            
            basic_date= input("Please enter first date: ")
            #value vaildation using the function above, loop untill correct format, with mentioning problem
            while inputdate(basic_date)== False:
                
                basic_date = input(" ValueError! Let's give it another try! " + "\n" +" please enter a date:" + '\n'
                                     + " i.e. 'YYYY-MM-DD' stracture, an exsample for a vaild format is 2017-03-11" + '\n')        
                inputdate(basic_date)

            end_date = input("Please enter second date: ")
            #value vaildation using the function above, loop untill correct format, with mentioning problem
            while inputdate(end_date)== False:
                
                end_date = input(" ValueError! Let's give it another try! " + "\n" +" please enter a date:" + '\n'
                                 + " i.e. 'YYYY-MM-DD' stracture, an exsample for a vaild format is 2017-03-11" + '\n')        
                inputdate(end_date)

             
            while True:
                amount = input("Enter the amount you wish to convert: ")
                try:
                    val = float(amount)
                    if val < 0:  # if not a positive int print message and ask for input again
                        print("Sorry, input must be a positive amount, try again")
                        continue
                    break
                except ValueError:
                    print("come on! I asked for an amount.. not string")

            
            #vaild the currencies
            currencies=exrates.get_currencies()
            
            
            currency_lst=str(input("enter two currency codes: separate them with comma (,)\n"))
            currency_fix_lst=currency_lst.upper().split(",")

            #remove spaces
            currency_fix_lst = [cur.strip(' ') for cur in currency_fix_lst]

                                   
            #only 3 values key for currency, and making sure the currency exists
            while all(currency.strip() not in currencies for currency in currency_fix_lst)==True or len(currency_fix_lst) !=2 :
                
                #as requested to use
                sys.stderr.write("\nsomthing went wrong! are you sure its two vaild currencies? - try again\n")

                #input the currencies requested again, if cur dosent exists
                currency_lst=str(input('try entering two currencies with a comma-separated\n i.e. "ILS, USD" is the correct format\n'))
                currency_fix_lst=currency_lst.upper().split(",")

                    
            #creating currencies in the correct format
            first_cur = str(currency_fix_lst)[2:5]
            sec_cur = str(currency_fix_lst[::-1])[2:5]
            
            
            
            #using the function above to return values in table
            data = convert_time_period(float(amount), first_cur, sec_cur, basic_date, end_date)

            print("\n Here is a list of convertion between two currencies, amount converted: " + amount + " \n")
            
            print("Date", '{0:>30}'.format(first_cur + '#To#' + sec_cur), '{0:>30}'.format(sec_cur + '#To#' + first_cur))
            
            for key, line in data.items():
                
                print(key, '{0:>30}'.format(line[0]), '{0:>30}'.format(line[1]))
            break
 
        except ValueError:
            print('ohhhhh.......there has been a Value Error.... try again!')
        
            break


main()
