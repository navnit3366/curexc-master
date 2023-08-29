import exrates
import datetime
import sys

def inputdate(date_text):
    '''function that inputs a date, in a vaild format,
        using python datatime module
    '''
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def print_table(table):
    '''get a list as input, and prints it in a form of table,
        and print it as requested - aligned to the right and in a 5 digit form
    '''

    #setting the maximun width for nicer visualisation of the tabular form
    column_width = 60
    
    print("\nthe folowing is a list of currencies, based on the date the user entered, in the requested format:\n" )

    for row in table:

        #setting the table width
        width = column_width - len(row[0])
        
        #beacause of the sorting, this value has entered, so passing it.....
        if row[0] == 'Name (Code)':

            pass

        else:

            #printing the values as requested in 5 digit precision, aligned to the right
            print(row[0], '{0:>{width}.5f}'.format(float(row[1]),width=width))
    
        


    

def main():
    '''main to test the program: inputs a date,
        and prints the exchange rates for that date in a tabular form
    '''
    
    #getting currencies names
    currencies = exrates.get_currencies()

    #loop to print the values
    while True:
        try:

            datetext = input("Greetings User! please enter a date:" + '\n')        

            #value vaildation using the function above, loop untill correct format, with mentioning problem
            while inputdate(datetext)== False:

                #printing error!
                sys.stderr.write("\Value Error! invalid input - use the correct format! \n")
 
                datetext = input(" ValueError! Let's give it another try! " + "\n" +" please enter a date:" + '\n'
                                 + " i.e. 'YYYY-MM-DD' stracture, an exsample for a vaild format is 2017-03-11" + '\n')        
                inputdate(datetext) 


            #the requested format for values
            format_ert = '{name} ({code})'

            #the requested format for values
            missing_val = '<unknonwn>'
            

            #with the date provided, creating a list, containing the format requested, sorted, and it's matching exchange value             
            sor_table = sorted([[format_ert.format(name=currencies.get(code, missing_val),code=code), value] for code, value in exrates.get_exrates(datetext).items()], key=lambda t: t[0])
            
            
            #printing as requested, see function detail for more details
            print_table(sor_table) 

            
            

        except ValueError:
            print('there has been a Value Error...... too bad')
        break
       

main()
