from datetime import datetime as dt
from datetime import date, timedelta

class Movie:

    def __init__(self, movie_id, title, genre, rental_price, availability_status, kiosk_location, total_copies, copies_available):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.rental_price = rental_price
        self.availability_status = availability_status
        self.kiosk_location = kiosk_location
        self.total_copies = total_copies
        self.copies_available = copies_available

    def get_total_rentals(self, rentals):
        
        counter = 0

        for rental in rentals:
            if rental.movie_id == self.movie_id:
                counter += 1
        return counter

    def get_total_revenue(self, rentals):
        
        revenue = self.rental_price * self.get_total_rentals(rentals)
        revenue = round(revenue, 2)

        return revenue


class Rental:

    def __init__(self, rental_id, customer_email, customer_name, movie_id,
                 rental_date, return_date, rental_status):
        self.rental_id = rental_id
        self.customer_email = customer_email
        self.customer_name = customer_name
        self.movie_id = movie_id
        self.rental_date = rental_date
        self.return_date = return_date
        self.rental_status = rental_status

    def get_movie(self, movies):

        movies.sort(key = lambda Movie: Movie.movie_id)
        idx = binary_search(movies, self.movie_id, key= lambda Movie: Movie.movie_id)
        if idx == -1:
            return -1
        
        movie = movies[idx]
        return movie
    
    def get_title(self, movies):

        movies.sort(key = lambda Movie: Movie.movie_id)
        idx = binary_search(movies, self.movie_id, key= lambda Movie: Movie.movie_id)
        if idx == -1:
            return "Not Found"
        
        movie = movies[idx]
        return movie.title
    
    def get_genre(self, movies):

        movies.sort(key = lambda Movie: Movie.movie_id)
        idx = binary_search(movies, self.movie_id, key= lambda Movie: Movie.movie_id)
        if idx == -1:
            return "Not Found"
        
        movie = movies[idx]
        return movie.genre
    
    def get_price(self, movies):

        movies.sort(key = lambda Movie: Movie.movie_id)
        idx = binary_search(movies, self.movie_id, key= lambda Movie: Movie.movie_id)
        if idx == -1:
            return "Not Found"
        
        movie = movies[idx]
        return movie.rental_price
    
    def get_location(self, movies):

        movies.sort(key = lambda Movie: Movie.movie_id)
        idx = binary_search(movies, self.movie_id, key= lambda Movie: Movie.movie_id)
        if idx == -1:
            return "Not Found"
        
        movie = movies[idx]
        return movie.kiosk_location
    
    

class Kiosk:

    def __init__(self, kiosk_id, location, status, num_machines, last_service_date ):
        self.kiosk_id = kiosk_id
        self.location = location
        self.status = status
        self.num_machines = num_machines
        self.last_service_date = last_service_date

    #Returns total revenue for the kiosk
    def get_total_revenue(self, movies, rentals):
        total_revenue = 0

        movies_at_kiosk = []
        for movie in movies:
            if movie.kiosk_location == self.location:
                movies_at_kiosk.append(movie.movie_id)
        
        for rental in rentals:
            if rental.movie_id in movies_at_kiosk:
                if rental.get_price(movies) != "Not Found":
                    total_revenue += rental.get_price(movies)

        return round(total_revenue, 2)



#File Loader/Writer Functions
########################################################################
def load_movies():
    movies = []
    
    with open("movies.txt", "r") as file:

        #Discard first line
        file.readline()

        for line in file:

            if line.strip() == "": continue
            data = [x.strip() for x in line.split("#")]

            movie_id = int(data[0])
            title = data[1]
            genre = data[2]
            rental_price = float(data[3])
            availability = data[4]
            kiosk_location = data[5]
            total_copies = int(data[6])
            copies_available = int(data[7])

            movie = Movie(movie_id, title, genre, rental_price, availability, kiosk_location, total_copies, copies_available)
            movies.append(movie)
    
    return movies

def load_rentals():
    
    rentals = []

    with open("rentals.txt", "r") as file:
        file.readline()

        for line in file:

            if line.strip() == "": continue
            data = [x.strip() for x in line.split("#")]

            rental_id = int(data[0])
            customer_email = data[1]
            customer_name = data[2]
            movie_id = int(data[3])
            rental_date = dt.strptime(data[4], r"%m/%d/%Y").date()
            return_date = dt.strptime(data[5], r"%m/%d/%Y").date()
            rental_status = data[6]

            if date.today() > return_date and rental_status != "Returned":
                rental_status = "Late"

            rental = Rental(rental_id, customer_email, customer_name, movie_id, rental_date, return_date, rental_status)
            rentals.append(rental)

    return rentals

def load_kiosks():
    
    kiosks = []

    with open("kiosks.txt", "r") as file:
        file.readline()

        for line in file:

            if line.strip() == "": continue
            data = [x.strip() for x in line.split("#")]

            #Kiosk_id#Location#Status#Num_machines#Last_service_date

            kiosk_id = int(data[0])
            location = data[1].capitalize().strip()
            status = data[2]
            num_machines = data[3]
            last_service_date = dt.strptime(data[4], "%m/%d/%Y").date()

            kiosk = Kiosk(kiosk_id, location, status, num_machines, last_service_date)

            kiosks.append(kiosk)

    return kiosks

def write_data(movies, rentals, kiosks):
    
    print("Saving updated data to files...")
    #Writes the updated movies list to movies.txt
    with open("movies.txt", "w") as file:
        file.write("Movie ID#Title#Genre#Rental Price#Availability Status#Kiosk Location#Total Copies#Copies Available\n")

        for movie in movies:
            file.write(f"{movie.movie_id}#{movie.title}#{movie.genre}#{movie.rental_price}#{movie.availability_status}#{movie.kiosk_location}#{movie.total_copies}#{movie.copies_available}\n")
    
    #Writes the updated rentals list to rentals.txt
    with open("rentals.txt", "w") as file:
        file.write("Rental ID#Customer Email#Customer Name#Movie ID#Rental Date#Return Date#Rental Status\n")

        for rental in rentals:
            file.write(f"{rental.rental_id}#{rental.customer_email}#{rental.customer_name}#{rental.movie_id}#{rental.rental_date:%m/%d/%Y}#{rental.return_date:%m/%d/%Y}#{rental.rental_status}\n")

    with open("kiosks.txt", "w") as file:
        """self.kiosk_id = kiosk_id
        self.location = location
        self.status = status
        self.num_machines = num_machines
        self.last_service_date = last_service_date"""

        file.write("Kiosk_id#Location#Status#Num_machines#Last_service_date\n")

        for kiosk in kiosks:
            file.write(f"{kiosk.kiosk_id}#{kiosk.location}#{kiosk.status}#{kiosk.num_machines}#{kiosk.last_service_date:%m/%d/%Y}\n")
            
def etl(movies, rentals, kiosks):

    pass
########################################################################

def menu(movies, rentals, kiosks):

    still_running = True
    while still_running:
        print("\nMain Menu:\n")

        print("Options:")
        print("Manager Menu: Opens the managerial section of this program.")
        print("Customer Menu: Opens the customer section of this program.")
        print("Save: Writes the current data to the relevant txt files.")
        print("Exit: Exit the program and save data.")

        selection = input("\nPlease make selection: ")


        while selection.strip().lower() not in ["manager menu", "customer menu", "save", "exit"]:
            selection = input("Please enter a valid selection: ")

        match selection.strip().lower():
            case "manager menu":
                manager_menu(movies, rentals, kiosks)
            case "customer menu":
                customer_menu(movies, rentals, kiosks)
            case "save":
                write_data(movies, rentals, kiosks)
            case "exit":
                write_data(movies, rentals, kiosks)
                still_running = False
                print("Goodbye!")

#Manager menu and related functions
def manager_menu(movies, rentals, kiosks):

    """
    Add a new movie title to the system: Done
    Remove a movie title from the system: Done
    Edit information about a movie (title, genre, availability, rental price, etc): Done
    Mark a rental as returned or completed: Done
    Manage store information (location, availability, machine status): Done
    Access reports to monitor rentals and system activity: Done
    Manage customer records: Done

    """
    still_running = True
    while still_running:
        print("\nManager Menu\n")

        print("Options:")
        print("Add movie: add a new movie title to the system")
        print("Remove movie: remove a movie title from the system")
        print("Edit movie: Edit information about a movie")
        print("Return rental: Mark a rental as returned")
        print("Store info: Manage information regarding kiosks")
        print("Add Kiosk: Add a new kiosk to the system")
        print("Manage Customers: Manage records about customers")
        print("Reports: Access reports to monitor rentals and system activity")
        print("Back: Return to main menu")

        selection = input("Please make a selection: ")
        while selection.strip().lower() not in ["add movie", "remove movie", "edit movie", "return rental"
                                                , "store info", "add kiosk", "reports", "back", "manage customers"]:
            selection = input("Please make a valid selection: ")

        match selection.strip().lower():
            case "add movie":
                add_movie(movies, kiosks)
            case "remove movie":
                remove_movie(movies)
            case "edit movie":
                edit_movie(movies, kiosks)
            case "return rental":
                return_rental(movies, rentals)
            case "store info":
                edit_kiosk_info(kiosks)
            case "add kiosk":
                add_kiosk(kiosks)
            case "reports":
                reports_menu(movies, rentals, kiosks)
            case "manage customers":
                manage_customers(rentals, movies)
            case "back":
                still_running = False

def add_movie(movies, kiosks):
    print("Please fill out each field with the relevant info to add the new movie.")

#Gets and verifies each data field for the new movie
    title = input("Input movie title: ")
    while title.strip() == "":
        title = input("Please input a valid movie title: ")
    
    genre = input("Input movie genre: ")
    while genre.strip() == "":
        genre = input("Please input a valid movie genre: ")

    rental_price = input("Input rental price: $")
    valid_price = False
    while not valid_price:
        try:
            rental_price = float(rental_price)
            if rental_price > 0:
                valid_price = True
            else:
                rental_price = input("Please input a valid rental price: $")
        except ValueError:
            rental_price = input("Please input a valid rental price: $")

    availability = input("Input availability status: ").capitalize()
    while availability not in ["Available", "Unavailable"]:
        availability = input("Input a valid availability status: ").capitalize()
    
    location = input("Please enter the kiosk location: ").capitalize().strip()
    valid_locations = []
    for kiosk in kiosks:
        if kiosk.location not in valid_locations:
            valid_locations.append(kiosk.location)

    while location not in valid_locations:
        location = input("Please enter a valid kiosk location: ").capitalize().strip()

    total_copies = input("Enter the total number of copies: ")
    valid_copy_count = False
    while not valid_copy_count:
        try:
            total_copies = int(total_copies)
            if total_copies > 0:
                valid_copy_count = True
            else:
                total_copies = input("Please input a valid number of copies: ")
        except ValueError:
            total_copies = input("Please input a valid number of copies: ")

    copies_available = input("Enter the number of available copies: ")
    valid_available_count = False
    while not valid_available_count:
        try:
            copies_available = int(copies_available)
            if copies_available >= 0 and copies_available <= total_copies:
                valid_available_count = True
            else:
                copies_available = input("Please input a valid number of available copies: ")
        except ValueError:
            copies_available = input("Please input a valid number of available copies: ")
    
    #Checks if the movie already exists and exits if so.
    for movie in movies:
        if movie.title.strip().lower() == title.strip().lower():
            print("This movie already exists in the system!")
            return

    #This section assigns a new movie ID to the movie.    
    movies.sort(key = lambda Movie: Movie.movie_id)
    if len(movies) > 0:
        movie_id = movies[len(movies)-1].movie_id + 1
    else: movie_id = 1

    movies.append(Movie(movie_id, title, genre, rental_price, availability, location, total_copies, copies_available))
    print(f"\n{title} has been successfully added to the system and assigned ID {movie_id}.\n")

def remove_movie(movies):

    print("\nPlease search for the movie you want to delete by filling out the prompts below: ")
    idx = manager_search_movie(movies)

    if idx == -1:
        print("The searched movie could not be deleted because it was not found in the system.")
    else:
        print(f"Deleting movie no. {movies[idx].movie_id}: \"{movies[idx].title}\" from the system.")
        del(movies[idx])

def edit_movie(movies, kiosks):
    
    #Searches for the movie to edit.
    print("To edit a movie, first select the movie to edit by following the prompts below: ")
    idx = manager_search_movie(movies)
    if idx == -1:
        print("This movie was not found in the system.")
        return
    print(f"Editing movie no. {movies[idx].movie_id}: \"{movies[idx].title}\"...")


    #Gets and verifies edits for each instance variable stored by the movie object.

    #Edits title or keeps same if user leaves field blank.
    title = input(f"Current title is {movies[idx].title}. To edit, enter new title, or leave blank to skip: ")
    if title.strip() == "":
        pass
    else:
        movies[idx].title = title
    
    #Edits genre or keeps same if user leaves field blank.
    genre = input(f"Current genre is {movies[idx].genre}. To edit, enter new genre, or leave blank to skip: ")
    if genre.strip() == "":
        pass
    else:
        movies[idx].genre = genre

    rental_price = input(f"Current rental price is ${movies[idx].rental_price}. To edit, enter new price or leave blank to skip: $")

    if rental_price.strip() == "":
        pass
    else:
        valid_price = False
        while not valid_price:
            try:
                rental_price = float(rental_price)
                if rental_price > 0:
                    valid_price = True
                else:
                    rental_price = input("Please input a valid rental price: $")
            except ValueError:
                rental_price = input("Please input a valid rental price: $")
        movies[idx].rental_price = rental_price

    availability = input(f"Current availability status is {movies[idx].availability_status}. To edit, enter new status or leave blank to skip: ").capitalize()
    if availability == "":
        pass
    else:
        while availability not in ["Available", "Unavailable"]:
            availability = input("Input a valid availability status: ").capitalize()
        movies[idx].availability_status = availability
    
    location = input(f"Current kiosk location is {movies[idx].kiosk_location}. To edit, enter new location, or leave blank to skip: ").capitalize().strip()
    
    if location == "":
        pass
    else:
        valid_locations = []
        for kiosk in kiosks:
            if kiosk.location not in valid_locations:
                valid_locations.append(kiosk.location)

        while location not in valid_locations:
            location = input("Please enter a valid kiosk location: ").capitalize().strip()

        movies[idx].kiosk_location = location

    total_copies = input(f"Total number of copies is currently {movies[idx].total_copies}. To edit, enter new count, or leave blank to skip: ")

    if total_copies == "":
        pass
    else:
        valid_copy_count = False
        while not valid_copy_count:
            try:
                total_copies = int(total_copies)
                if total_copies > 0:
                    valid_copy_count = True
                else:
                    total_copies = input("Please input a valid number of copies: ")
            except ValueError:
                total_copies = input("Please input a valid number of copies: ")
        movies[idx].total_copies = total_copies

    copies_available = input(f"Available copies is currently {movies[idx].copies_available}. To edit, enter new count, or leave blank to skip: ")
    
    if copies_available == "":
        pass
    else:
        valid_available_count = False
        while not valid_available_count:
            try:
                copies_available = int(copies_available)
                if copies_available >= 0 and copies_available <= total_copies:
                    valid_available_count = True
                else:
                    copies_available = input("Please input a valid number of available copies: ")
            except ValueError:
                copies_available = input("Please input a valid number of available copies: ")
        movies[idx].copies_available = copies_available
    
def return_rental(movies, rentals):
    
    #Find the index of the desired rental in the rentals list, or notify user and exit if not present
    rental_id = input("Please input the rental id of the rental you'd like to return: ")
    
    #Verifies format
    valid_rental_id_format = False
    while not valid_rental_id_format:
        try:
            rental_id = int(rental_id)
            if rental_id > 0:
                valid_rental_id_format = True
            else:
                rental_id = input("Please enter an ID with the correct format: ")
        except ValueError:
                rental_id = input("Please enter an ID with the correct format: ")

    
    #Runs binary search for rental index position, exits if not found
    rentals.sort(key = lambda Rental: Rental.rental_id)
    idx = binary_search(rentals, rental_id, key = lambda Rental: Rental.rental_id)
    if idx == -1:
        print("This rental could not be found.")
        return

    #Check if the rental is already returned. If it has been returned, notify user and exit.
    if rentals[idx].rental_status.strip().lower() == "returned":
        print("This rental has already been returned.")
        return

    #Set rental status to returned
    rentals[idx].rental_status = "Returned"
    print(f"Successfully returned rental with ID: {rentals[idx].rental_id}")

    #Find the corresponding movie by the movie ID of the rental. If available copies is less than total copies, increment it.
    #If the movie doesn't exist anymore, just exit.
    movie_idx = binary_search(movies, rentals[idx].movie_id, key = lambda Movie: Movie.movie_id)
    if movie_idx == -1:
        return
    
    if movies[movie_idx].copies_available < movies[movie_idx].total_copies:
        movies[movie_idx].copies_available = movies[movie_idx].copies_available + 1

def add_kiosk(kiosks):
    print("\nFill out the following fields to add a new kiosk to the system:")

    #Get and verify location
    location = input("Location: ").strip().title()
    while True:

        duplicate_found = False

        if location == "":
            location = input("Please enter a location. This field cannot be empty: ").strip().title()
            continue
        else:
            for kiosk in kiosks:
                if kiosk.location.strip().title() == location:
                    location = input("This location is already in the system. Enter another: ").strip().title()
                    duplicate_found = True
                    break
            
            if duplicate_found == True:
                continue
            break
    
    #Get and verify status
    status = input("Enter Status: Active or Inactive: ").capitalize().strip()
    while status.lower() not in ["active", "inactive"]:
        status = input("Enter a valid Status: Active or Inactive: ").capitalize().strip()

    #Get and verify num_machines
    num_machines = input("Number of Machines: ")
    valid = False
    while valid == False:
        try:
            num_machines = int(num_machines)
            if num_machines <= 0:
                num_machines = input("Please enter a valid number of machines: ")
                continue
            valid = True
        except ValueError:
            num_machines = input("Please enter a valid number of machines: ")

    #Get and verify last_service_date
    valid = False
    while not valid:
        user_input = input("Last service date (mm/dd/yyyy): ")
        try:
            last_service_date = dt.strptime(user_input.strip(), "%m/%d/%Y").date()

            if last_service_date <= date.today():
                valid = True
            else:
                print("Invalid date (the date you entered is in the future). Please try again.")
        except ValueError:
            print("Invalid date format. Please try again.")

    #Assign a unique ID   
    kiosks.sort(key = lambda Kiosk: Kiosk.kiosk_id)
    if len(kiosks) > 0:
        kiosk_id = kiosks[len(kiosks)-1].kiosk_id + 1
    else: kiosk_id = 1

    kiosks.append(Kiosk(kiosk_id, location, status, num_machines, last_service_date))
    print(f"\nKiosk {kiosk_id} in {location} has been successfully added to the system.\n")

def edit_kiosk_info(kiosks):
    print("\nKiosk Editor")
    print("\nKiosks in system:")

    """        self.kiosk_id = kiosk_id
        self.location = location
        self.status = status
        self.num_machines = num_machines
        self.last_service_date = last_service_date"""

    for kiosk in kiosks:
        print(f"\nKiosk ID: {kiosk.kiosk_id}")
        print(f"Location: {kiosk.location}")
        print(f"Status:  {kiosk.status}")
        print(f"Number of Machines: {kiosk.num_machines}")
        print(f"Last Service Date: {kiosk.last_service_date}")

    #Get the ID of the kiosk the user wishes to edit, exits if the user leaves the field blank.
    target = input("Please enter the ID of the kiosk you wish to update, or leave blank to exit: ")
    if target == "":
        return
    
    #Verifies the ID is in the right format.
    valid_target_format = False
    while valid_target_format == False:
        try:
            target = int(target)
            if target <= 0:
                target = input("Please enter a kiosk ID with the correct format: ")
            else:
                valid_target_format = True
        except ValueError:
            target = input("Please enter a kiosk ID with the correct format: ")

    #Runs a binary search to find the index of the kiosk the user wants to edit.
    kiosks.sort(key = lambda Kiosk: Kiosk.kiosk_id)
    idx = binary_search(kiosks, target, key = lambda Kiosk: Kiosk.kiosk_id)

    if idx == -1:
        print("\nThe system could not find this kiosk.")
        return
    
    kiosk = kiosks[idx]

    print(f"\nEditing Kiosk {kiosk.kiosk_id}...\n")

    #Gets, verifies, and sets new location or skips if field is left blank
    location = input(f"Current Location: {kiosk.location}. Enter new location or leave blank to skip: ")
    if location.strip() == "":
        pass
    else:
        location = location.strip().title()
        while True:

            duplicate_found = False

            for kiosk in kiosks:
                    if kiosk.location.strip().title() == location:
                        location = input("This location is already in the system. Enter another: ").strip().title()
                        duplicate_found = True
                        break
                
            if duplicate_found == True:
                    continue
            
            kiosk.location = location
            break
    
    #Get, verifies, and updates status or skips if field is left blank
    status = input(f"Current status: {kiosk.status}. Enter new updated status or leave blank to skip: ").capitalize().strip()
    if status == "":
        pass
    else:
        while status.lower() not in ["active", "inactive"]:
            status = input("Enter a valid Status: Active or Inactive: ").capitalize().strip()
        kiosk.status = status

    #Gets, verifies, and sets num_machines or skips if field is left blank
    num_machines = input(f"Current number of machines: {kiosk.num_machines}. Enter updated number or leave blank to skip: ")
    if num_machines == "":
        pass
    else:
        valid = False
        while valid == False:
            try:
                num_machines = int(num_machines)
                if num_machines <= 0:
                    num_machines = input("Please enter a valid number of machines: ")
                    continue
                valid = True
            except ValueError:
                num_machines = input("Please enter a valid number of machines: ")
        kiosk.num_machines = num_machines

    #Gets, verifies, and sets last service date or skips if field is left blank
    last_service_date = input(f"Current last service date: {kiosk.last_service_date}. Enter updated last service date (mm/dd/yyyy) or leave blank to skip: ")
    if last_service_date == "":
        pass
    else:
        valid = False
        while not valid:
            try:
                last_service_date = dt.strptime(last_service_date.strip(), "%m/%d/%Y").date()

                if last_service_date <= date.today():
                    valid = True
                else:
                    last_service_date = input("Invalid date (the date you entered is in the future). Please try again: ")
            except ValueError:
                last_service_date = input("Invalid date format. Please try again: ")
        kiosk.last_service_date = last_service_date

    print(f"\nKiosk {kiosk.kiosk_id} has been succesfully updated.")
    
def manage_customers(rentals, movies):

    """self.rental_id = rental_id
        self.customer_email = customer_email
        self.customer_name = customer_name
        self.movie_id = movie_id
        self.rental_date = rental_date
        self.return_date = return_date
        self.rental_status = rental_status"""
    
    print("\nCustomer Management")

    #List out unique customers by name and email, ties email to name with a dictionary for later use
    print("\nCustomers in System: ")
    rentals.sort(key = lambda Rental: Rental.customer_name)


    customer_emails = []
    customer_names = {}

    for rental in rentals:
        email = rental.customer_email.strip().lower()

        if email not in customer_emails:
            print(f"Name: {rental.customer_name} Email: {rental.customer_email}")
            customer_emails.append(email)
            customer_names[email] = rental.customer_name.strip().title()

    #Displays rental history for a customer and allows user to change their name.
    target = input(f"To display rental history for a customer and/or edit their name, enter customer email. To exit, leave blank: ")
    if target == "":
        return
    else:
        #Verify target email:
        valid = False
        while not valid:
            target = target.lower().strip()
            
            if target in customer_emails:
                valid = True
            else:
                target = input("Please enter a valid email: ")

        #Prints out rental history
        rentals.sort(key = lambda Rental: Rental.rental_date)
        print(f"\nRental history for {customer_names[target]}: ")

        for rental in rentals:
            if rental.customer_email.lower().strip() == target:
                print(f"\nRental ID: {rental.rental_id}")
                print(f"Movie ID: {rental.movie_id}")
                print(f"Rental Date: {rental.rental_date}")
                print(f"Return Date: {rental.return_date}")
                print(f"Rental Status: {rental.rental_status}")
                print(f"Movie Title: {rental.get_title(movies)}")
                print(f"Price: {rental.get_price(movies)}")

        new_name = input(f"To update {customer_names[target]}\'s name, enter new name here, or leave blank to skip: ").title().strip()
        new_email = input(f"To update {customer_names[target]}\'s email, enter new email here, or leave blank to skip: ").lower().strip()

        updated = False
        for rental in rentals:
            if rental.customer_email.strip().lower() == target.strip().lower():

                if new_name != "":
                    rental.customer_name = new_name
                    updated = True
                if new_email != "":
                    rental.customer_email = new_email
                    updated = True
        if updated:
            print("Successfully updated records associated with this customer.")
       
#Customer Menu and Functions:     
def customer_menu(movies, rentals, kiosks):
    """
    Browse Movies: 
    Search Movies by Title or Genre: 
    Rent Movie From Kiosk: 
    View Rental History: 
    Return Rented Movie: """
    
    still_running = True
    while still_running:
        print("\nCustomer Menu\n")

        print("Options:")
        print("Browse Movies: List movies currently available at active locations")
        print("Search Movie: Search for a movie by title or genre")
        print("Rent Movie: Rent a movie from a specific kiosk")
        print("Rental History: View your rental history")
        print("Return Movie: Return a rented movie")
        print("Back: Return to main menu")

        selection = input("Please make selection: ")
        while selection.strip().lower() not in ["browse movies", "search movie", "rent movie","rental history","return movie", "back"]:
            selection = input("Please make a valid selection: ")
        
        match selection.strip().lower():
            case "browse movies":
                list_available_movies_at_active_locations(movies, kiosks)
            case "search movie":
                customer_movie_search(movies)
            case "rent movie":
                rent_movie(movies, rentals, kiosks)
            case "rental history":
                customer_rental_history(movies, rentals)   
            case "return movie":
                return_rental(movies, rentals)
            case "back":
                still_running = False
                 
def list_available_movies_at_active_locations(movies, kiosks):

    print("\nMovies Available at Active Kiosk Locations:")

    kiosks.sort(key = lambda kiosk: kiosk.location)

    movies.sort(key = lambda movie: movie.title)
    movies.sort(key = lambda movie: movie.genre)

    for movie in movies:
        kiosk_idx = binary_search(kiosks, movie.kiosk_location, key = lambda kiosk: kiosk.location)
        if kiosk_idx == -1:
            continue

        kiosk = kiosks[kiosk_idx]
        if movie.availability_status == "Available" and movie.copies_available > 0 and kiosk.status == "Active":
            print(f"\nTitle: {movie.title}")
            print(f"Genre: {movie.genre}")
            print(f"Location: {movie.kiosk_location}")
            print(f"Price: ${movie.rental_price:.2f}")

def customer_movie_search(movies):

    print("\nCustomer Movie Search: ")

    #Gets initial selection
    selection = input(f"\nTo search by title, enter \'Title\'. To search by genre. enter \'Genre\': ").strip().lower()
    while selection not in ["title", "genre"]:
        selection = input("Please make a valid selection: ").strip().lower()

    #Runs a title search or genre search based on selection
    movies.sort(key = lambda movie: movie.title)
    match selection:
        case "title":
            target = input("Please enter the title to search: ")

            idx = binary_search(movies, target.lower().strip(), key = lambda movie: movie.title.lower().strip())
            if idx == -1:
                print("0 Results Found.")
                return
            else:
                movie = movies[idx]
                print(f"\nResult for {target}:")
                print(f"\nTitle: {movie.title}")
                print(f"Genre: {movie.genre}")
                print(f"Location: {movie.kiosk_location}")
                print(f"Availability: {movie.availability_status}")
                print(f"Price: {movie.rental_price:.2f}")

            

        case "genre":
            
            genre = input("\nEnter genre to search: ")
            print(f"\nResults for {genre}:")

            for movie in movies:
                if movie.genre.strip().lower() == genre.strip().lower():
                    print(f"\nTitle: {movie.title}")
                    print(f"Genre: {movie.genre}")
                    print(f"Location: {movie.kiosk_location}")
                    print(f"Availability: {movie.availability_status}")
                    print(f"Price: {movie.rental_price:.2f}")

def rent_movie(movies, rentals, kiosks):
    print("\nMovie Rental Interface")

    email = input("Enter email: ")
    while "@" not in email or "." not in email:
        email = input("Please input a valid email address: ")

    name = input("Enter name: ")
    while name == "":
        name = input("Please enter a valid name: ")

    kiosk_location = input("Enter kiosk location: ")
    valid = False

    while valid == False:
        found = False
        for kiosk in kiosks:
            if kiosk.location.strip().lower() == kiosk_location.strip().lower():

                found = True
                if kiosk.status.strip().lower() == "active":
                    valid = True
                    break
                else:
                    print("This location is currently inactive.")
                    break
        
        if valid == False:
            if not found:
                print("This kiosk location was not found.")
            kiosk_location = input("Please input a different kiosk location: ")
            

    title = input("Enter title: ")
    valid = False
    selected_movie = None

    while valid == False:
        selected_movie = None
        for movie in movies:
            if (title.strip().lower() == movie.title.strip().lower() and kiosk_location.lower().strip() == movie.kiosk_location.lower().strip() and
                movie.copies_available > 0 and movie.availability_status.strip().lower() == "available"):
                valid = True
                selected_movie = movie
                break
        if selected_movie is None:
            title = input("The title you are trying to rent is not currently available at that location. Please enter another title or leave blank to exit: ")
            if title == "":
                print("Exiting rentals...")
                return

    #Rents the movie and updates relevant fields
    print(f"Renting {selected_movie.title} for ${selected_movie.rental_price:.2f}")

    #Updates the movie object
    selected_movie.copies_available = selected_movie.copies_available - 1
    if selected_movie.copies_available <= 0:
        selected_movie.availability_status = "Unavailable"
    
    #Creates the new rental ID
    rentals.sort(key = lambda rental: rental.rental_id)
    
    if len(rentals) > 0:
        rental_id = rentals[len(rentals)-1].rental_id + 1
    else: rental_id = 1

    rental = Rental(rental_id, email, name, selected_movie.movie_id, date.today(), date.today() + timedelta(days = 2), "Rented")
    rentals.append(rental)

    #Prints summary
    print("\nRental Summary:")
    print(f"Rental ID: {rental_id}")
    print(f"Title: {selected_movie.title}")
    print(f"Email: {rental.customer_email}")
    print(f"Name: {rental.customer_name}")
    print(f"Rental Price Paid: ${selected_movie.rental_price:.2f}")
    print(f"Rental Date: {rental.rental_date}")
    print(f"Return Date: {rental.return_date}")

def customer_rental_history(movies, rentals):

    print("\nRental History Viewer")

    #Get and verify email
    email = input("Enter your email: ").strip().lower()
    while "@" not in email or "." not in email:
        email = input("Enter a valid email: ").strip().lower()


    #Find matches
    found_matches = []
    counter = 0

    for rental in rentals:
        if email == rental.customer_email.strip().lower():
            found_matches.append(rental)
            counter += 1

    #Display matches
    print(f"\nYou have {counter} rentals in your rental history: ")
    for match in found_matches:
        print(f"\nRental ID: {match.rental_id}")
        print(f"Title: {match.get_title(movies)}")
        print(f"Price Paid: ${match.get_price(movies)}")
        print(f"Location: {match.get_location(movies)}")
        print(f"Rental Date: {match.rental_date}")
        print(f"Return Date: {match.return_date}")
        print(f"Status: {match.rental_status}")

#Reports Menu and Functions:
def reports_menu(movies, rentals, kiosks):

    still_running = True

    while still_running:
        print("\nReports Menu\n")

        print("Options:")
        print("Daily Rental Report: Display rentals started on a specified date")
        print("Movies Rented Out: Display movies that currently have at least one copy rented out.")
        print("Overdue Rentals: Display rentals that are currently overdue")
        print("Movie Popularity Rankings: Display a specified number of the top movies ranked by total rentals")
        print("Movie Revenue Rankings: Display a specified number of the top movies ranked by total revenue")
        print("Kiosk Revenue Rankings: Display a specified number of the top kiosks ranked by total revenue")
        print("Back: return to the manager menu")

        selection = input("Please make a selection: ")
        while selection.lower().strip() not in ["daily rental report", "movies rented out",
                                                "overdue rentals", "movie popularity rankings",
                                                "movie revenue rankings", "kiosk revenue rankings", "back"]:
            selection = input("Please make a valid selection: ")

        match selection.lower().strip():
            case "daily rental report":
                    daily_rental_report(movies, rentals)
            case "movies rented out":
                    movies_currently_rented(movies, rentals)
            case "overdue rentals":
                    overdue_rentals(movies, rentals)
            case "movie popularity rankings":
                    movies_by_popularity(movies, rentals)
            case "movie revenue rankings":
                    movies_by_revenue(movies, rentals)
            case "kiosk revenue rankings":
                    kiosks_by_revenue(movies, rentals, kiosks)
            case "back":
                    still_running = False

def daily_rental_report(movies, rentals):
    print("\nDaily Rental Report\n")

#Get the target date and verify it.
    target_date = input("Please input the date you'd like to view in mm/dd/yy format or leave blank to view today's rental report: ")
    if target_date.strip().lower() == "":
        target_date = date.today()
    else:
        valid = False
        while not valid:
            try:
                target_date = dt.strptime(target_date, r"%m/%d/%Y").date()

                if target_date > date.today():
                    print("Error: target date is in the future.")
                    target_date = input("Please enter a valid date: ")
                else:
                    valid = True
            except ValueError:
                print("Error: Could not convert your entry to a date.")
                target_date = input("Please enter a valid date: ")
    
    print(f"\nRentals Started on {target_date}:")
    for rental in rentals:
        if rental.rental_date == target_date:
            print(f"\nRental ID: {rental.rental_id}")
            print(f"Title: {rental.get_title(movies)}")
            print(f"Price Paid: ${rental.get_price(movies)}")
            print(f"Location: {rental.get_location(movies)}")
            print(f"Rental Date: {rental.rental_date}")
            print(f"Return Date: {rental.return_date}")
            print(f"Status: {rental.rental_status}")

def movies_currently_rented(movies, rentals):
    print("\nMovies Currently Rented Out")

    movies.sort(key = lambda movie: movie.movie_id)
    rented_movies = []
    for rental in rentals:
        if rental.rental_status in ["Rented", "Late"]:
            movie = rental.get_movie(movies)
            
            if movie != -1 and movie.title not in rented_movies:

                rented_movies.append(movie.title)

                print(f"\nID: {movie.movie_id}")
                print(f"Title: {movie.title}")
                print(f"Price: ${rental.get_price(movies)}")
                print(f"Location: {rental.get_location(movies)}")

def overdue_rentals(movies, rentals):
    print("\nRentals Currently Overdue:")

    for rental in rentals:
        if rental.rental_status == "Late":
            print(f"\nRental ID: {rental.rental_id}")
            print(f"Title: {rental.get_title(movies)}")
            print(f"Start Date: {rental.rental_date}")
            print(f"Due Date: {rental.return_date}")

def movies_by_popularity(movies, rentals):
    print("\nMovies Ranked by Popularity\n")

    count = input("Please enter the number of movies you would like to display: ")
    valid = False

    while not valid:
        try:
            count = int(count)
            if count <= 0 or count > len(movies):
                count = input("Please enter a valid number of movies to display: ")
                continue
            valid = True
        except ValueError:
            count = input("Please enter a valid number of movies to display: ")

    movies.sort(key = lambda movie: movie.get_total_rentals(rentals), reverse = True)
    
    print(f"Top {count} movies by popularity:")
    for i in range(count):
        print(f"{i + 1}: {movies[i].title}    Total Rentals: {movies[i].get_total_rentals(rentals)}")

def movies_by_revenue(movies, rentals):
    print("\nMovies Ranked by Revenue\n")

    count = input("Please enter the number of movies you would like to display: ")
    valid = False

    while not valid:
        try:
            count = int(count)
            if count <= 0 or count > len(movies):
                count = input("Please enter a valid number of movies to display: ")
                continue
            valid = True
        except ValueError:
            count = input("Please enter a valid number of movies to display: ")

    movies.sort(key = lambda movie: movie.get_total_revenue(rentals), reverse = True)
    
    print(f"Top {count} movies by total revenue:")
    for i in range(count):
        print(f"{i + 1}: {movies[i].title}    Total Revenue: ${movies[i].get_total_revenue(rentals)}")

def kiosks_by_revenue(movies, rentals, kiosks):
    print("\nKiosks Ranked by Revenue\n")

    count = input("Please enter the number of kiosks you would like to display: ")
    valid = False

    while not valid:
        try:
            count = int(count)
            if count <= 0 or count > len(movies):
                count = input("Please enter a valid number of kiosks to display: ")
                continue
            valid = True
        except ValueError:
            count = input("Please enter a valid number of kiosks to display: ")

    kiosks.sort(key = lambda kiosk: kiosk.get_total_revenue(movies, rentals), reverse = True)
    
    print(f"Top {count} kiosks by total revenue:")
    for i in range(count):
        print(f"{i + 1}: {kiosks[i].location}    Total Revenue: ${kiosks[i].get_total_revenue(movies, rentals)}")


#General Utilities
def binary_search(arr, target, key=lambda x: x):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        value = key(arr[mid])

        if value == target:
            return mid
        elif value < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

def manager_search_movie(movies):

    search_by = input("To search by ID, enter \"ID\". To search by title, enter \"title\": ").strip().lower()
    while search_by not in ["id", "title"]:
        search_by = input("Please make a valid selection: ").strip().lower()
    
    match search_by:
        case "id":
            movies.sort(key = lambda Movie: Movie.movie_id)

            target = input("Please input the ID of the movie for which you wish to search: ")

            while True:
                try:
                    target = int(target)

                    if target <= 0:
                        target = input("Please enter a target ID in the correct format: ")
                        continue
                    break
                except ValueError:
                    target = input("Please enter a target ID in the correct format: ")

            idx = binary_search(movies, target, key = lambda Movie: Movie.movie_id)
            
            return idx

        case "title":
            movies.sort(key = lambda Movie: Movie.title.lower().strip())

            target = input("Please input the title of the movie for which you wish to search: ")

            idx = binary_search(movies, target, key = lambda Movie: Movie.title.lower().strip())
            
            return idx
    

    pass