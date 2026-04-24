import utilities

movies = utilities.load_movies()
rentals = utilities.load_rentals()
kiosks = utilities.load_kiosks()


print("Welcome to Damebox movie rental management!")
print("This program allows you to perform a wide range of functions on data for movies, along with rentals and kiosks associated with them.")

utilities.menu(movies, rentals, kiosks)
