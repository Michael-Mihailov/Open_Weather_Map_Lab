from fetch_posts import FetchPosts

class FetchIP(FetchPosts):
    BASE_URL = "http://ip-api.com/json/"

    def __init__(self):
        super().__init__(self.BASE_URL)