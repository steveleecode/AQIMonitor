import requests
import keys
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
        response = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={long}&appid={keys.API_KEY_OPENWEATHERMAP}")
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
    
    def get_historical_AQI(self, city: str, state: str, country: str, month: int, day: int, year: int, hour: int, minute: int, integer_response:bool=False):
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
        timestamp = int(self.to_unix_timestamp(month, day, year, hour, minute))
        response = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={timestamp}&end={timestamp}&appid={keys.API_KEY_OPENWEATHERMAP}")
        returned_json = response.json()

        return self.get_AQI_US(returned_json)
        
    
    def get_last_24hrs_AQI(self, city: str, state: str, country: str):
        time = datetime.datetime.now()
        results = []
        for i in range(24):
            time_point = time - datetime.timedelta(hours=i)

            #try:
            data = self.get_historical_AQI(city, state, country, time_point.month, time_point.day, time_point.year, time_point.hour, 0, True)
            results.append(data)
            #except (KeyError, IndexError) as e:
                #print(f"Data missing for {time_point}. Error: {e}")
                #results.append(None)  # Append None or another placeholder for missing data

        return results



    def geocode(self, city, state, country):
        """Converts a city to longitude and latitude

        Args:
            city (str): Name of the city (Ex: Seattle)
            state (str): Name of the State (Ex: Washington)
            country (str): Name of the country (Ex: United States)

        Returns:
            tuple: (longitude, latitude)
        """
        response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit=1&appid={keys.API_KEY_OPENWEATHERMAP}")
        returned_json = response.json()
        return (float(returned_json[0]["lat"]), float(returned_json[0]["lon"]))
    
    def to_unix_timestamp(self, month, day, year, hour, minute):
        dt = datetime.datetime(year, month, day, hour, minute)
        return dt.timestamp()
    
    def get_AQI_US(self, json_response:dict):
        # Function to calculate AQI for a given pollutant concentration
        def calculate_aqi(concentration, pollutant):
            breakpoints = constants.AQI_BREAKPOINTS.get(pollutant)
            if not breakpoints:
                raise ValueError(f"Pollutant {pollutant} not found in breakpoints. JSON: {json_response}")

            for C_low, C_high, I_low, I_high in breakpoints:
                if C_low <= concentration <= C_high:
                    aqi = ((concentration - C_low) / (C_high - C_low)) * (I_high - I_low) + I_low
                    return round(aqi)

            return None  # Return None if concentration is out of range
        

        data = json_response["list"][0]["components"]

        #Remove Unnecessary Pollutants
        unwanted_keys = {"no", "nh3"}

        for key in unwanted_keys:
            del data[key]

        # Calculate AQI for each pollutant and determine overall AQI
        aqi_values = {}
        for pollutant, concentration in data.items():
            aqi = calculate_aqi(concentration, pollutant)
            if not aqi == None:
                aqi_values[pollutant] = aqi 

        overall_aqi = max(aqi_values.values())

        # Output the results
        print("Overall AQI:", overall_aqi)
        return overall_aqi

    
    def get_future_AQI(self, city: str, state: str, country: str, month: int, day: int, year: int, hour: int, minute: int):
        pass
