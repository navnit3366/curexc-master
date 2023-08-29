import exrates
import datetime
import sys
 




def inputdate(date_text):
    '''function that inputs a date, and verified if the date is in a vaild format, else return False
    '''
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    
    except ValueError:
        
        return False
        


def main():
    '''main to test the program: inputs a date,
    and prints the list of currencies for which there is a date, in format requested
    '''
    datetext = input("Greetings User! please enter a date:" )        

    #value vaildation using the function above, loop untill correct format, with mentioning problem
    while inputdate(datetext)== False:
        #printing error!
        sys.stderr.write("\Value Error! invalid input-choose an available date\n")

        datetext = input(" Let's give it another try! " + "\n" +" please enter a date:" + '\n'
                         + " i.e. 'YYYY-MM-DD' stracture, an exsample for a vaild format is 2017-03-11" + '\n')        
        inputdate(datetext)
        
    #using the date the user entered, to withdraw the dictionery from exrates file, get_exrate fuction and sorted by code.    
    
    date_Rates = sorted(exrates.get_exrates(datetext))
    

    #marging two dictionery, to get the name and code in one dictionery
    curlist = exrates.get_currencies()

    #the format requested
    format_list = '{name} ({code})'

    #creating the list, using the format above, while check every code in the updated code list
    Final_list = [format_list.format(name=curlist.get(code, "<unknonwn>"),code=code) for code in date_Rates]

    print('\nHere is a list of correncies available to ' + datetext + " : \n")

    #print the values of the list
    print('\n'.join(Final_list))
    
    
    
      
main()
