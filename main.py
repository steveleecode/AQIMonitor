from AQI import AQIMonitor

def main():
    city = str(input("Enter a City: "))
    state = str(input("Enter the State: "))
    country = str(input("Enter the Country: "))
    monitor = AQIMonitor()
    current_aqi = monitor.get_current_AQI(city, state, country)
    print(f"The Current AQI in {city}, {state}, {country} is {current_aqi}.")

if __name__ == "__main__":
    main()
