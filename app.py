import utilities
from utilities import Movie
from utilities import Rental
from utilities import Kiosk

movies = utilities.load_movies()
rentals = utilities.load_rentals()
kiosks = utilities.load_kiosks()

for movie in movies:
    print(f"{movie.movie_id}: {movie.title}")

utilities.list_available_movies(movies, kiosks)

utilities.write_data(movies, rentals, kiosks)