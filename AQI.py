import requests
import constants
import json
import datetime

class AQIMonitor:

    def get_current_AQI(self, city, state, country):
        """Retrieves the current AQI

        Args:
            city (str): Name of the city (Ex: Seattle)
            state (str): Name of the State (Ex: Washington)
            country (str): Name of the country (Ex: United States)

        Returns:
            str: Returns the current AQI (1 = good, 2 = fair, 3 = moderate, 4 = poor, 5 = very poor)
        """

        lat, long = self.geocode(city, state, country)
        response = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={long}&appid={constants.API_KEY_OPENWEATHERMAP}")
        returned_json = response.json()
        
        # 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor
        quality = returned_json["list"][0]["main"]["aqi"]

        outputAQI = ""
        match quality:
            case 1:
                outputAQI = "good"
            case 2:
                outputAQI = "fair"
            case 3:
                outputAQI = "moderate"
            case 4:
                outputAQI = "poor"
            case 5:
                outputAQI = "very poor"
        
        return outputAQI
    
    def get_historical_AQI(self, city: str, state: str, country: str, month: int, day: int, year: int, hour: int, minute: int):
        """Retrieves the historical AQI

        Args:
            city (str): Name of the city (Ex: Seattle)
            state (str): Name of the State (Ex: Washington)
            country (str): Name of the country (Ex: United States)
            month (int): Month (Ex: 12)
            day (int): Day (Ex: 31)
            year (int): Year (Ex: 2020)
            hour (int): Hour (Ex: 11)
            minute (int): Minute (Ex: 59)


        Returns:
            str: Returns the current AQI (1 = good, 2 = fair, 3 = moderate, 4 = poor, 5 = very poor)
        """
        
        lat, lon = self.geocode(city, state, country)
        timestamp = self.to_unix_timestamp(month, day, year, hour, minute)
        response = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={timestamp}&end={timestamp}&appid={constants.API_KEY_OPENWEATHERMAP}")
        returned_json = response.json()
        
        # 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor
        quality = returned_json["list"][0]["main"]["aqi"]

        outputAQI = ""
        match quality:
            case 1:
                outputAQI = "good"
            case 2:
                outputAQI = "fair"
            case 3:
                outputAQI = "moderate"
            case 4:
                outputAQI = "poor"
            case 5:
                outputAQI = "very poor"
        
        return outputAQI



    def geocode(self, city, state, country):
        """Converts a city to longitude and latitude

        Args:
            city (str): Name of the city (Ex: Seattle)
            state (str): Name of the State (Ex: Washington)
            country (str): Name of the country (Ex: United States)

        Returns:
            tuple: (longitude, latitude)
        """
        response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit=1&appid={constants.API_KEY_OPENWEATHERMAP}")
        returned_json = response.json()
        print((float(returned_json[0]["lat"]), float(returned_json[0]["lon"])))
        return (float(returned_json[0]["lat"]), float(returned_json[0]["lon"]))
    
    def to_unix_timestamp(self, month, day, year, hour, minute):
        dt = datetime.datetime(year, month, day, hour, minute)
        return dt.timestamp()
    
    def get_future_AQI(self, city: str, state: str, country: str, month: int, day: int, year: int, hour: int, minute: int)
