from dotenv import load_dotenv
import os
from fetch_open_weather_map import FetchOpenWeatherMap
from fetch_ip import FetchIP

"""
prompt_location() was generated using Github Copilot!!!!!
It prompts the user to choose what location they want weather data for using either the city name, coordinates, or their IP address.
The function validates the user's input and returns a dictionary of parameters that can be used to fetch weather data from the OpenWeatherMap API.
Invalid user input is handled with error messages and prompts the user to try again until valid input is provided.

I modified the function to return a dictionary of parameters instead of variables and also had to modify the code when I decided to use the IP address as a location option.
"""
def prompt_location():
    params_response = {}

    while True:
        print("Do you want to search by city, coordinates, or IP address?")
        choice = input("Enter 'city', 'coordinates', or 'ip': ").strip().lower()
        if choice == "city":
            city = input("Enter the city name: ").strip()
            if city:
                params_response["q"] = city
                break
            else:
                print("City name cannot be empty. Please try again.")
        elif choice == "coordinates":
            try:
                lat = float(input("Enter the latitude: ").strip())
                lon = float(input("Enter the longitude: ").strip())
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    params_response["lat"] = lat
                    params_response["lon"] = lon
                    break
                else:
                    print("Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180.")
            except ValueError:
                print("Invalid input. Please enter valid numeric values for coordinates.")
        elif choice == "ip":
            ip_fetcher = FetchIP()
            ip_data = ip_fetcher.get_posts()
            if ip_data and "lat" in ip_data and "lon" in ip_data:
                params_response["lat"] = ip_data["lat"]
                params_response["lon"] = ip_data["lon"]
                print(f"Using IP-based location: {ip_data.get('city', 'Unknown City')}, {ip_data.get('country', 'Unknown Country')}")
                break
            else:
                print("Could not retrieve location from IP. Please try another method.")
        else:
            print("Invalid choice. Please enter 'city', 'coordinates', or 'ip'.")
    
    return params_response

def prompt_temperature_units():
    params_response = {}
    
    while True:
        print("Do you want to use metric or imperial temperature units?")
        choice = input("Enter 'metric' or 'imperial': ").strip().lower()
        if choice in ["metric", "imperial"]:
            params_response["units"] = choice
            break
        else:
            print("Invalid choice. Please enter 'metric' or 'imperial'.")

    return params_response

"""
print_weather() was generated using ChatGPT!!!!! (because I find formatting output to be very boring)
It takes a dictionary of weather data and prints a formatted weather report to the console. 
The function extracts various pieces of information from the data and displays them in a user-friendly format.
The function has conditional checks for optional data fields that may not always be present in the API response.

I modified the function because initially it also wanted to print out date-time information using a deprecated date-time library that was beyond the scope of this assignment.
(I'm just trying to build a weather app here, not a calendar.)
"""
def print_weather(data):
    print("=" * 48)
    print("                Weather Report")
    print("=" * 48)

    # Location
    name = data.get("name", "Unknown")
    country = data.get("sys", {}).get("country", "")
    print(f"\nLocation: {name}, {country}")

    # Weather description
    weather = data.get("weather", [{}])[0]
    print(f"\nCondition: {weather.get('description', 'N/A').title()}")

    # Main stats
    main = data.get("main", {})
    print(f"Temperature: {main.get('temp', 'N/A')}°")
    print(f"Feels like:  {main.get('feels_like', 'N/A')}°")
    print(f"Humidity:    {main.get('humidity', 'N/A')}%")
    print(f"Pressure:    {main.get('pressure', 'N/A')} hPa")

    # Wind
    wind = data.get("wind", {})
    if wind:
        print(f"\nWind: {wind.get('speed', 'N/A')} at {wind.get('deg', 'N/A')}°")
        if "gust" in wind:
            print(f"Gusts: {wind['gust']}")

    # Clouds
    clouds = data.get("clouds", {})
    if clouds:
        print(f"\nCloud Cover: {clouds.get('all', 'N/A')}%")

    # Visibility
    if "visibility" in data:
        print(f"Visibility:  {data['visibility']} meters")

    # Rain
    rain = data.get("rain")
    if rain:
        if "1h" in rain:
            print(f"\nRain (last 1h): {rain['1h']} mm")
        elif "3h" in rain:
            print(f"\nRain (last 3h): {rain['3h']} mm")

    # Snow
    snow = data.get("snow")
    if snow:
        if "1h" in snow:
            print(f"\nSnow (last 1h): {snow['1h']} mm")
        elif "3h" in snow:
            print(f"\nSnow (last 3h): {snow['3h']} mm")

    print("\n" + "=" * 48)

def generate_weather_api_params():
    params = {
        "appid": os.getenv("OWM_API_KEY")
    }

    params.update(prompt_location())
    params.update(prompt_temperature_units())

    return params

def main():
    load_dotenv()
    fetcher = FetchOpenWeatherMap()
    
    # Main Loop allowing the user to check multiple locations without restarting the program
    while True:
        params = generate_weather_api_params()
        weather_data = fetcher.get_posts(params=params)
    
        if weather_data == None:
            print("No weather data available.")
        else:
            print_weather(weather_data)

        if input("\nDo you want to check another location? (y/n): ").strip().lower() != 'y':
            print("Thank you for using this Weather App! Goodbye!")
            break



if __name__ == "__main__":
    main()