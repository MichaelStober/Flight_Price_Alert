import requests
import pandas as pd
import os
class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self):
        #insert your SHEETY API ENDPOINT
        self.sheety_endpoint = os.environ.get("SHEETY_API_ENDPOINT")


    def get_data(self):
        '''retunrs all data from google sheet'''
        response = requests.get(url=self.sheety_endpoint)
        response.raise_for_status()
        return response.json()

    def get_prices(self):
        '''returns the flight prices from google sheet'''
        respond_prices = requests.get(url=self.sheety_endpoint)
        respond_prices.raise_for_status()
        with open("logfile.txt", mode="a") as file:
            file.write(f"dm.get_prices()\n")
        return respond_prices.json()['prices']

    def update_row(self, destination):
        '''Updates a row on google-sheet with given id '''
        header = {
            "Content-Type":"application/json",
        }
        row_data = {
            "price":{
                'city': destination['city'],
                'iataCode': destination['iataCode'],
                'lowestPrice': destination['lowestPrice']
            }
        }

        response = requests.put(url=f"{self.sheety_endpoint}/{destination['id']}",json=row_data, headers=header)
        response.raise_for_status()
        with open("logfile.txt", mode="a") as file:
            temp_df = pd.DataFrame([destination])
            file.write(f"dm.update_row()\n{temp_df.to_string(index=False)}\n\n")
