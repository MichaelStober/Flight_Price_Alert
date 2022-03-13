import datetime
import json
import requests
from datetime import date
from dateutil.relativedelta import *
from flight_data import FlightData
import os

API_ENDPOINT = "https://tequila-api.kiwi.com"
#insert here your tequila api key
TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY")

class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self, start_city="London"):
        self.api_endpoint = API_ENDPOINT
        self.API_KEY = TEQUILA_API_KEY
        self.api_header = {
            "apikey": self.API_KEY,
            "Content-Type": "application/json",
        }
        self.startcity_iata = self.get_iataCode(start_city)
        print("Your set home city : ", self.startcity_iata, "\n")

    def get_iataCode(self, cityName):
        query = {
            "term": cityName,
            "locale": "en-US",
            "location_types": "airport",
            "limit": 1,
            "active_only": "true"
        }
        response = requests.get(url=f"{self.api_endpoint}/locations/query", headers=self.api_header, params=query)
        response.raise_for_status()
        code=response.json()['locations'][0]['city']['code']

        with open("logfile.txt", mode="a") as file:
            file.write(f"fs.get_iataCode() {code}\n\n")
        return code

    def get_current_period(self):
        """returns list with start and enddate"""
        start_period = date.today() + datetime.timedelta(days=1)
        end_period = start_period + relativedelta(months=+6)
        return [start_period.strftime("%d/%m/%Y"), end_period.strftime("%d/%m/%Y")]

    def get_flight_to(self, destination):
        """returns FlightData object"""
        current_period = self.get_current_period()
        query = {
            "fly_from": self.startcity_iata,
            "fly_to": destination,
            "date_from": current_period[0],
            "date_to": current_period[1],
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "adults": 1,
            "locale": "en",
            "curr": "EUR",
            "one_for_city": 1,
            "max_stopovers": 0
        }

        response = requests.get(url=f"{self.api_endpoint}/v2/search", params=query, headers=self.api_header)
        response.raise_for_status()

        try:
            flightData = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination}.")
            return None

        # create flight data object
        flight = FlightData(
            flightData['price'],
            p_departure_airport_code=flightData['flyFrom'],
            p_departure_city=flightData['cityFrom'],
            p_departure_date=flightData["route"][0]["local_departure"].split("T")[0],
            p_destination_airport_code=flightData['flyTo'],
            p_destination_city=flightData['cityTo'],
            p_return_flight_date=flightData["route"][1]["local_departure"].split("T")[0],
            p_bookinglink=flightData['deep_link']
        )
        with open("logfile.txt", mode="a") as file:
            flightDataJson = json.dumps(flightData, indent=4)
            file.write(f"fs.get_flight_to()\n{flightDataJson}\n\n")
        return flight
