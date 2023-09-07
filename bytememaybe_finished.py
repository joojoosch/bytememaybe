#ATTENTION: IF YOU WANT TO SELECT "M" AND MAKE A CSV FILE OF ALL THE RESERVATIONS YOU HAVE TO CHANGE THE FILE PATH IN FUNCTION NUMBER 20 (LINE 570-572). THE REST OF THE CODE SHOULD WORK FINE FROM ANY COMPUTER.



# different imports that are necessary for the code
import datetime
import pickle
import csv
import os


# class for admins that defines them so that each has to have a name and a ID and the masterkey, which is used to log in

class admin:
    def __init__(self, name, id_number):
        self._name = name
        self._id_number = id_number
        self._master_key = 1234

    def set_name(self, new_value):
        if new_value.isnumeric() == False: # checks if the given name contains any numbers and if he doesn't it is a valid name because names cannot contain any numbers
            self._name = new_value
        else:
            print("This name contains invalid symbols. (e.x. numbers)")
    
    def set_id_number(self, new_value):
        if isinstance(new_value, (int)): #checks if the given ID is a number, because the ID can only contain numbers
            self._id_number = new_value
        else:
            print("This is not a valid ID.")

    def get_masterkey(self):
        return self._master_key


# below are the two admins of the firm

admin1 = admin("Al", 1)
admin2 = admin("Guido", 2)


# the list below contains all the admins

admin_list = [admin1, admin2]

        
# class for employees that defines them so that each has to have a name and a ID, which is used to log in
class employees:
    def __init__(self, name, id_number):
            self._name = name
            self._id_number = id_number
            
    def set_name(self, new_value):
        if new_value.isnumeric() == False: # checks if the given name contains any numbers and if he doesn't it is a valid name because names cannot contain any numbers
            self._name = new_value
        else:
            print("This name contains invalid symbols. (e.x. numbers)")

    def set_id_number(self, new_value):
        if isinstance(new_value, (int)): #checks if the given ID is a number, because the ID can only contain numbers
            self._id_number = new_value
        else:
            print("This is not a valid ID.")



#creates dict with name of office as keys and the corresponding capacity as value
weekday_list = ["monday", "tuesday", "wednesday", "thursday", "friday"]


# names for the loops that were used in the definitions below:
# (the loops were mostly used so that if the input was invalid the questions was posed again)
# first loop = valid_entry
# second loop = valid_a
# third loop = valid_b
# fourth loop = valid_c



def log_in_admins():

    valid_entry = False 
    admin_name = None

    while valid_entry == False:
        valid_a = False
        while valid_a == False:
            name = input("Please enter your name:\n")
            if name.isnumeric() == False:
                valid_a = True
            else: 
                print("Entry invalid. Try again.")
            
                
        valid_b = False
        while valid_b == False:
            id_number = input("Please enter your ID number:\n")
            if id_number.isnumeric() == True:
                id_number = int(id_number)
                valid_b = True
            else:
                print("Entry invalid. Try again")
        
        valid_c = False
        while valid_c == False:
            masterkey = input("Please enter the Masterkey:\n")
            if masterkey.isnumeric() == True:
                masterkey = int(masterkey)
                valid_c = True
            else:
                print("Entry invalid. Try again")


        for i in admin_list:
            if i._name == name and i._id_number == id_number and i.get_masterkey() == masterkey: #ensures that the admin can only log in, if he enters the correct id, name and masterkey that belong to each other
                admin_name = name  #stores the name and id number of the admin in admin data in order to store it into files later on to make reservations etc.
                print("Your log in has been successfull.")
                valid_entry = True #sets valide_entry to True, in order to exit the while loop
            
        
        if admin_name == None: #the variable admin data remains empty if the name, id and masterkey are not correct
            print("Your name, ID number or Masterkey is wrong. Please try again.")
        
    return admin_name #return name and id of admin 

def log_in_employees(employee_list):
# does the same as lig_in_admin, except that it doesnt ask for the masterkey
    valid_entry = False
    employee_name = None

    while valid_entry == False:
        valid_a = False
        while valid_a == False:
            name = input("Please enter your name:\n")
            if name.isnumeric() == False:
                valid_a = True
            else:
                print("Entry invalid. Try again")
            
        valid_b = False
        while valid_b == False:
            id_number = input("Please enter your ID number:\n")
            if id_number.isnumeric() == True:
                id_number = int(id_number)
                valid_b = True
            else:
                print("Entry invalid. Try again")


        for i in employee_list:
            if i._name == name and i._id_number == id_number:
                employee_name = name
                print("Your log in has been successfull.")
                valid_entry = True
        
        if employee_name == None:
            print("Your name or ID number is wrong. Please try again.")
    
    return employee_name



# below are functions that are necessary to execute the primary functions, that's why we classified them as assisting functions
# assisting functions: (1-7)
        
#1
def get_day(type_of_request):
    valid_entry = False
    while valid_entry == False:
        day = input("Please enter the day for which you want to " + type_of_request + ":\n") 
        day = day.lower() #ensures that the day is always lowercase
        if day in weekday_list: #if the input is in the weekday list, the loop is exited
            valid_entry = True
        else:
            print("This is an invalid entry. Please try again\n")
    return day 

#2
def get_office(type_of_request, office_dict):
    valid_entry = False
    office_exists = False

    while valid_entry == False:
        office = input("Please enter the office for which you would like to " + type_of_request + ":\n")
        office = office.lower() #ensures lowercase offices names
        for key in office_dict.keys(): #iterates trough the office dict, keys which are the name of the offices
            if office == key: #if the input office is a key in the office list, the loop stops 
                valid_entry = True
                office_exists = True

        if office_exists == False:
            print("This is an invalid entry or the office doesn't exist. Please try again\n")    
            
    return office

#3
def check_availability(day, office, a_file, office_dict):
    working_places = office_dict[office]

    with open(a_file, "r") as f: #opens the file and looks how many lines are used. Hence this many people have a reservation at the office at this day
        content = f.readlines()
        try:
            for i in content:
                if i.strip() == "":
                    content.remove(i)
                with open(a_file, "w") as f:
                    f.writelines(content)
        except ValueError:
            pass
    
    used_places = len(content)
    
    available_places = working_places - used_places

    if available_places > 0: #checks wether there are still places available and returs the the available places
        statement = ("On " + day + " there is/are " + str(available_places) + " place/s available at " + office + ".")
    else:
        statement = ("There are no places available on " + day + " at " + office + ". Maybe you should work from home on that day or try a different office.")

    print(statement)

    return available_places

#4
def check_already_there(day, office, file, user_name):
    already_there = False
    with open(file, "r") as f:
        content = f.readlines() 
    
    if user_name + "\n" in content: #checks whether the users name is already in the contents list (e.g. has already made a reservation)
        print("You have already made a reservation on " + day + " at " + office + " so you can't make another one.")
        already_there = True
    return already_there

#5
def make_office_files(office_name):
    #make_files creates a txt file for each day of the week and office (example: monday.hq.txt)
    for day in weekday_list:
        with open(day + "." + office_name + ".txt", "w") as f:
            pass

#6
def delete_office_files(office_name):
    for day in weekday_list:
        os.remove(day + "." + office_name + ".txt")

#7
def clear_yesterday(office_dict): 
    #deletes the content of the of the day that has passed so that new reservations can be made

    office_name = []
    for key in office_dict.keys():
        office_name.append(key)
    current_date = datetime.datetime.now()
    yesterday = current_date - datetime.timedelta(days=1)
    day_name_yesterday = yesterday.strftime("%A")
    day_name_yesterday = day_name_yesterday.lower()
    for office in office_name:
        with open(day_name_yesterday + "." + office + ".txt", "w"):
            pass



#functions to save the employees/offices in an external file so that you can access them anytime and that it saves the changes that were made even if the code is executed again (8-11)

#8
def save_employee_data(employee_list):
    # because of the pickle function we can save the employees in form of a list to an external file
    with open("employee_data", "wb") as f:
        pickle.dump(employee_list, f)

#9
def get_employee_data():
    # gets the list from the file 
    with open("employee_data", "rb") as f:
        employee_list = pickle.load(f)
    return employee_list

#10
def save_office_data(a_dict):
    # saves the offices in form of a dictionary to an external file
    with open("office_data", "wb") as f:
        pickle.dump(a_dict, f)

#11
def get_office_data():
    # gets the dictionary back from the file
    with open("office_data", "rb") as f:
        office_dict = pickle.load(f)
    return office_dict
    



# below are the functions that motivate people to go to the office by using invitations or free snacks, that's why we classified them as motivational functions
# motivational functions: (12-13)

#12
def motivation_if_low_occupation(office_dict):
    #if there are more than and 3 places available at an office, it prints that there are free snacks when you log in so that more people go to the office
    current_date = datetime.datetime.now() 
    day_name = current_date.strftime("%A")
    day_name = day_name.lower()
    for office, working_places in office_dict.items():
        with open(day_name + "." + office + ".txt", "r") as f:
            names = f.readlines()
            used_places = len(names)
        if (working_places - used_places) >= 3: 
            print("Free snacks at " + office + " today, come by! :) " )

#13
def check_if_invited(user_name):
    #checks if you got an invitation from someone and if that is the case it will tell you who invited you to come where
    try:
        with open(user_name + "_invited.txt", "r") as me_invited:
            content = me_invited.readline()
            print(content)
        os.remove(user_name + "_invited.txt")
    except FileNotFoundError:    
        pass


# below are all the functions that a user can select to execute, that's why we classified them as primary functions
# primary functions: (14-25)

#14
def make_reservation(user_name, office_dict):
    #function makes a reservation by storing the name of the user into the file of the chosen day and office
    type_of_request = "make a reservation"
    valid_entry = False
    while valid_entry == False:
    
        day = get_day(type_of_request)
        office = get_office(type_of_request, office_dict)

        file = day + "." + office + ".txt" 
        available_places = check_availability(day, office, file, office_dict) #checks availability at certain day, and office by looking up the corresponding file

        if available_places > 0:
            valid_a = False
            while valid_a == False:
                want_reservation = input("Do you want to make the reservation? (Y/N)\n")
                want_reservation = want_reservation.lower()
                if want_reservation == "y":
                    already_there = check_already_there(day, office, file, user_name) #checks that you didn't already make a reservation for the chosen day and office
                    if already_there == False:
                        with open(file, "a") as f:
                            f.write(user_name + "\n")
                        print("Youre reservation has been successfull. See you on " + day + " at " + office + ".")
                        valid_a = True
                        valid_entry = True
                    elif already_there == True:
                        valid_c = False
                        while valid_c == False:
                            want_another_day = input("Do you want to make a reservation for a different day instead? (Y/N)\n")
                            want_another_day = want_another_day.lower()
                            if want_another_day == "y":
                                valid_c = True
                                valid_a = True
                                
                            elif want_another_day == "n":
                                valid_c = True
                                valid_a = True
                                valid_entry = True

                            else:
                                print("Entry invalid. Please try again.")

                        

                elif want_reservation == "n":
                    valid_a = True
                    valid_entry = True
                else:
                    print("Entry invalid. Please try again.")

        else:
            valid_b = False
            while valid_b == False:
                want_another_day = input("Do you want to make a reservation for a different day or at a different office instead? (Y/N)\n")
                want_another_day = want_another_day.lower()
                if want_another_day == "y":
                    valid_b = True
                    
                elif want_another_day == "n":
                    valid_entry = True
                    valid_b = True

                else:
                    print("Entry invalid. Please try again.")
    return day

#15
def make_cancellation(user_name, office_dict):
    #cancels by rewriting the file without the name of the person that wants to cancel

    type_of_request = "make a cancellation"

    day = get_day(type_of_request)
    office = get_office(type_of_request, office_dict)

    file = day + "." + office + ".txt"

    with open(file, "r") as f: #opens the requested file and reads each lineinto conent list
        content = f.readlines()

    content.remove(user_name + "\n") #removes the reservation from the list but not yet from the file

    with open(file, "w") as f: #opens corresponding file with w, delets all content and adds the modified content from the content list
        f.writelines(content)

    print("Youre reservation on " + day + " at " + office + " has successfully been removed.")

#16
def make_office(office_dict):
    #creates a new office by making all the corresponding files (ex. monday.hq.txt, tuesday.hq.txt etc.) and adding the new office and its working spaces to the dictionary office_dict
    
    valid = False
    while valid == False:
        iterations = input("How many offices do you want to add?\n")
        if iterations.isnumeric() == True:
            iterations = int(iterations)
            valid = True
        else:
            print("Entry invalid. Try again")

    while iterations > 0:

        valid_a = False
        while valid_a == False:
            name_office = input("Please enter the name of the new office:\n")            
            if name_office.isnumeric() == False:
                valid_a = True
            else:
                print("Entry invalid. Try again")
        

        valid_b = False
        while valid_b == False:
            working_spaces_office = input("Please enter the number of working spaces at " + name_office + ":\n")
            if working_spaces_office.isnumeric() == True:
                working_spaces_office = int(working_spaces_office)
                valid_b = True
            else:
                print("Entry invalid. Try again")
        

        office_dict[name_office] = working_spaces_office 

        make_office_files(name_office) #creates all the files needed for the new office (each day)

        print("You have successfully added the office " + name_office + " with " + str(working_spaces_office) + " places.")
        iterations -= 1

#17
def delete_office(office_dict):
    #deletes office by taking it out of the dictionary and deleting all the corresponding files
    
    valid = False
    while valid == False:
        iterations = input("How many offices do you want to delete?\n")
        if iterations.isnumeric():
            iterations = int(iterations)
            valid = True
        else:
            print("Entry invalid. Try again")


    office_exists = False

    while iterations > 0:
        
        valid_a = False
        while valid_a == False:
            office_name = input("What is the name of the office that you want to delete?\n")           
            if office_name.isnumeric() == False:
                valid_a = True
            else:
                print("Entry invalid. Try again")
        
        for k in office_dict.keys():
            if office_name == k:
                delete_office_files(office_name)
                iterations -= 1
                office_exists = True

        if office_exists == True:
            office_dict.pop(office_name)
            print("office has successfully been removed.")


        elif office_exists == False:
            print("The given name does not exist. Please try again.")

#18
def create_employee(employee_list):
    #creates employees by creating them as objects of the class employees and then adding them to the list of employees
    
    
    valid = False
    while valid == False:
        iterations = input("How many employees do you want to add?\n")
        if iterations.isnumeric() == True:
            iterations = int(iterations)
            valid = True
        else:
            print("Entry invalid. Try again")
    
    while iterations > 0:
        
        valid_a = False
        while valid_a == False:
            name = input("Please enter the name of the new employee:\n")            
            if name.isnumeric() == False:
                valid_a = True
            else:
                print("Entry invalid. Try again")

        valid_b = False
        while valid_b == False:
            id_number = input("Please enter the id_number of the new employee:\n")
            if id_number.isnumeric() == True:
                id_number = int(id_number)
                valid_b = True
            else:
                print("Entry invalid. Try again")

        e = employees(name, id_number)
        employee_list.append(e)
        print("You have added " + name)
        iterations -= 1
    print("The adding process has been completed.")

#19
def delete_employee(employee_list):
    #deletes the employees by removing them from the employee list
    

    valid = False
    while valid == False:
        iterations = input("How many employees do you want to delete?\n")
        if iterations.isnumeric() == True:
            iterations = int(iterations)
            valid = True
        else:
            print("Entry invalid. Try again")

    name_exists = False
    
    while iterations > 0:

        valid_a = False
        while valid_a == False:
            name = input("Please enter the name of the employee that you want to delete:\n")
            if name.isnumeric() == False:
                valid_a = True
            else:
                print("Entry invalid. Try again")
        
        for employee in employee_list:
            if name == employee._name:
                employee_list.remove(employee)
                print(name + " has succesfully been removed.")
                name_exists = True
                iterations -= 1
        if name_exists == False:
            print("The given name does not exist. Please try again")
    return employee_list

#20
def see_capacity(office_dict):
    #creates a csv file with an overview of all the reservations that were made for the week and by whom and where

    #directory where the needed .txt files are located
    #ATTENTION: YOU HAVE TO CHANGE THE FILE PATH (LINE 570-572) BELOW IF YOU WANT TO USE THIS FUNCTION ON YOUR OWN COMPUTER

    txt_directory = "C:\\Users\\alle\Desktop"
    
    csv_output_directory =  "C:\\Users\\alle\\Desktop"

    csv_filename = 'booking_overview.csv'

    csv_output_path = os.path.join(csv_output_directory, csv_filename) #creates whole outputpath with desired filename

    #define offices and days of the week as lists day.office


    office_name = []
    for key in office_dict.keys():
        office_name.append(key)

    #create dictionary to store the data. tuples of office and day of week are the keys and values are lists of employee information

    data_dict = {(day, office): [] for day in weekday_list for office in office_name}

    day, office = None, None

    #iterate trough each .txt file in the directory to add the employee information to the data_dict dictionnary

    for filename in os.listdir(txt_directory): #start a loop and iterates trough all files in the given txt_directory
        if filename.endswith('.txt'): # checks if current filename ends with .txt in order to only process .txt files in the directory
            file_path = os.path.join(txt_directory, filename) #in order to read the current files content a filepath is needed.
            #the filepath is composed of the txt_general directory and the filename itself, hence they get joined together
            parts_filename = filename.split('.') #splits filename into three parts seperated by '.' and extracts the day and office name from the filename

            if len(parts_filename) == 3: # checks if there are 3 parts to ensure the correct filename structure
                day, office, _ = parts_filename #removes the .txt of the filename which is not needed
                
            


    # read content of file to get the employee information

            with open(file_path, 'r') as txt_file:
                content = txt_file.read() #reads files content into the variable 'content' as a str
                lines = content.split('\n') #creates a list 'lines' where each element is seperated by '\n' since each employee information was a line in the .txt file
                for line in lines:
                    if line: #to skip empty lines and prevent errors
                        name = line
                        data_dict[(day, office)].append(name) #since files content is only employee name, it appends the name to data dicts as value. 

    with open (csv_output_path, 'w', newline= '') as csv_file:
        csv_writer = csv.writer(csv_file) #creates writer object to use the suitable methods for it

        #header row with weekdays as the column headers
        header_row = ['Office'] + weekday_list
        csv_writer.writerow(header_row)

    #write data in csv for each office and day combination

        for office in office_name: #iterate trough each office in office_spaces list
            row_data = [office] #for each office a new list called row_date is created with the first element being the office name
            for day in weekday_list: #iterate over each day_of_weak list
                cell_data = ', '.join(data_dict[(day, office)]) #for each day, office combination the corresponding information from the data_dict is retrieved. .join joins these names into a string seperated by comma
                row_data.append(cell_data) #the string of names is appended to the row_data list
            csv_writer.writerow(row_data) #the names are written into the cell in the csv file

    print(f'Generated the CSV file: {csv_output_directory}') #prints direcory of csv file

#21
def send_invite(employee_list, office_dict, user_name):
    #sends an invite by creating a file with the name of the recipient and the message that they have been invited so that if the invited person logs in he/she sees that they have been invited, because it opens the file and prints the content 
    type_of_request = "send an invitation"

    found_person = False

    while found_person == False:
        valid_a = False
        while valid_a == False:
            name_of_invited_person = input("Who do you want to invite? \n")            
            if name_of_invited_person.isnumeric() == False:
                valid_a = True
            else:
                print("Entry invalid. Try again")

        
        office = get_office(type_of_request, office_dict)
            

        for employee in employee_list:
            if name_of_invited_person == employee._name:
                found_person = True
                print("Message sent: Invitation to " + name_of_invited_person)
                with open(name_of_invited_person + "_invited.txt", "w") as invited:
                    invited.write("You " + name_of_invited_person + " have been invited by " + user_name + " to join him/her at " + office + ".")
            
        if found_person == False:
            want_to_try_again = input("The person that you wanted to invite has not been found so no invitation was made. If you want to enter the name again type Y, with every other input you will be redirected back to the other options. \n")
            want_to_try_again = want_to_try_again.lower()

            if want_to_try_again == "y":
                pass
            else:
                found_person = True

 
#22
def see_employee_list(employee_list):
    #prints out all the existing employees
    if not employee_list:
        print("There are no existing employees. The admin still has to add them.")
    else:
        for e in employee_list:
            name = e._name
            id_number = e._id_number
            employee_info = name + ": " + str(id_number)
            print(employee_info)

#23
def see_office_dict(office_dict):
    #prints out all the existing offices
    if not office_dict:
        print("There are no existing offices. The admin still has to create them.")
    else:
        for k,v in office_dict.items():
            office_info = k + ": " + str(v)
            print(office_info)
    

#the functions below control that there are employees and offices because if they are none many parts of the code don't work so it needs to make sure that the admin creates them
#control functions (24-25)

#24
def check_employees_exist(employee_list):
    #checks if there are any employees at all
    if employee_list == []:
        print("At the moment no employees exist. If you are an admin please create them.\n")
        employee_exist = False
    else:
        employee_exist = True
    return employee_exist

#25
def check_office_exist(office_dict):
    #checks if there are any offices
    if not office_dict:
        print("No offices have been added by the admin. If you are an admin please create them.\n")
        office_exist = False
    else:
        office_exist = True
    return office_exist
    




#26 and 27 are the main functions

#26
def create_files():
    empty_list = []
    empty_dict = {}


    try:
        employee_list = get_employee_data()
        
    except FileNotFoundError:
        save_employee_data(empty_list)
        

    try:
        office_dict = get_office_data()
    
    except FileNotFoundError:
        save_office_data(empty_dict)
        
#27
def main():
    
    office_dict = get_office_data()
    employee_list = get_employee_data()

    valid_entry = False 
    #loops to make sure that a valid input was made or else the question was posed again
    while valid_entry == False:

        #finds out if the user is an admin or employee and logs them in

        type_of_person = input("Are you an admin or employee? (a/e)\n")

        type_of_person = type_of_person.lower()

        if type_of_person == "a":
            user_name = log_in_admins()
            valid_entry = True

        elif type_of_person == "e":
            employee_exist = check_employees_exist(employee_list)
            if employee_exist == True: #only if employees have already been created you can log in as an employee
                user_name = log_in_employees(employee_list)
                valid_entry = True
        

        else:
            print("Invalid entry. Please try again.")

    check_if_invited(user_name)

    want_something = True


    if type_of_person == "e":


        while want_something == True:
            office_exist = check_office_exist(office_dict)

            if office_exist == False:
                print("You will now be logged out since you can't do anything without an office.\n")
                wants = "l"
            
            elif office_exist == True:
                motivation_if_low_occupation(office_dict)
                wants = input("What do you want to do?\n r = make a reservation\n c = make a cancellation\n m = get overview of made reservations\n s = send invite to your coworkers\n l = log out\n")
            wants= wants.lower()

            valid_input = False

            if wants == "r":
                make_reservation(user_name, office_dict)

            elif wants == "c":
                make_cancellation(user_name, office_dict)

            elif wants == "m":
                see_capacity(office_dict)
            
            elif wants == "s":
                send_invite(employee_list, office_dict, user_name)
                
            elif wants == "l":
                print("Thank you and goodbye. You are now logged out.")
                valid_input = True
                want_something = False

            else:
                print("The given command does not exist.\n")
            


            while valid_input == False:

                anything_else = input("If you want to do anything else enter Y otherwise enter N and you will automatically be logged out. (Y/N)\n")
                anything_else = anything_else.lower()
                if anything_else == "y":
                    valid_input = True
                elif anything_else == "n":
                    print("Thank you and goodbye. You are now logged out.")
                    valid_input = True
                    want_something = False
                else:
                    print("Entry invalid. Try again.\n")







    elif type_of_person == "a":

        
        while want_something == True:
            office_exist = check_office_exist(office_dict)
            employee_exist = check_employees_exist(employee_list)

            
            if office_exist == False:#makes sure that the admin has to create offices if there are no offices there before he can do anything else
                wants = "o"


            elif employee_exist == False: #makes sure that the admin creates employees if there are none, before he can do anything else
                wants = "e"
            
            else:
                wants = input("What do you want to do?\n o = create a new office\n do = delete offices\n e = create new employees\n de = delete employees\n r = make a reservation\n c = make a cancellation\n m = get overview of made reservations\n s = send invite to your coworkers \n pe = print employee list\n po = print office list\n l = log out\n")

           
        
            wants = wants.lower()

            valid_input = False

            if wants == "o":
                make_office(office_dict)
                save_office_data(office_dict)
                office_dict = get_office_data()
            
            elif wants == "do":
                delete_office(office_dict)
                save_office_data(office_dict)
                office_dict = get_office_data()
            
            elif wants == "e":
                create_employee(employee_list)
                save_employee_data(employee_list)
                employee_list = get_employee_data()

            elif wants == "de":
                employee_list = delete_employee(employee_list)
                save_employee_data(employee_list)

        
            elif wants == "r":
                make_reservation(user_name, office_dict)
            
            elif wants == "c":
                make_cancellation(user_name, office_dict)

            elif wants == "m":
                see_capacity(office_dict)
            
            elif wants == "s":
                send_invite(employee_list, office_dict, user_name)

            elif wants == "pe":
                see_employee_list(employee_list)

            elif wants == "po":
                see_office_dict(office_dict)

            elif wants == "l":
                print("Thank you and goodbye. You are now logged out.")
                valid_input = True
                want_something = False

            else:
                print("The given command does not exist.\n")


            

            while valid_input == False:
    
                anything_else = input("If you want to do anything else enter Y otherwise enter N and you will automatically be logged out. (Y/N)\n")
                anything_else = anything_else.lower()
                if anything_else == "y":
                    valid_input = True
                        
                elif anything_else == "n":
                    print("Thank you and goodbye. You are now logged out.")
                    valid_input = True
                    want_something = False
                else:
                    print("Entry invalid. Try again.\n")

    clear_yesterday(office_dict)

create_files()
main()