import utilities
from utilities import Movie
from utilities import Rental
from utilities import Kiosk

movies = utilities.load_movies()
rentals = utilities.load_rentals()
kiosks = utilities.load_kiosks()

utilities.menu(movies, rentals, kiosks)
