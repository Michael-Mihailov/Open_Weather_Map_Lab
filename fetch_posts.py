import requests


class FetchPosts:
    def __init__(self, url):
        self.__url = url

    def get_posts(self, params=None):
        try:
            response = requests.get(self.__url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None