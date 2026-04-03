from fetch_posts import FetchPosts

class FetchOpenWeatherMap(FetchPosts):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        super().__init__(self.BASE_URL)