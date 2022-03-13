import pandas as pd
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime

#clear/create logfile
with open("logfile.txt",mode="w") as file:
    file.write(f"{datetime.now()}\n")

dataManager = DataManager()
flightSearch = FlightSearch()
notificationManager = NotificationManager()

sheet_data = dataManager.get_prices()
df_sheet_data = pd.DataFrame(sheet_data)
df_sheet_data_str = df_sheet_data.to_string(index=False)

with open("logfile.txt",mode="a") as file:
    # file.write(f"{datetime.now()}\n")
    file.write("Google Sheet data:\n")
    file.write(f"{df_sheet_data_str}\n\n")

flights_within_budget = []
#get iata code if cell is empty
for destination in sheet_data:
    if destination['iataCode'] =='':
        # fill all empty iata Codes in Google sheet
        destination['iataCode']=flightSearch.get_iataCode(destination['city'])
        dataManager.update_row(destination)

    flight = flightSearch.get_flight_to(destination['iataCode'])
    
    if flight != None:
        #check if price is in budget
        if flight.price <= destination['lowestPrice']:
            flights_within_budget.append(flight.get_attr_dict())

            message_text = f"Günster Preis für Flug von {flight.departure_city}-{flight.departure_airport_code} nach " \
                           f"{flight.destination_city}-{flight.destination_airport_code} am {flight.departure_date} bis " \
                           f"{flight.return_flight_date} für {flight.price}EUR gefunden! \nSiehe Link: {flight.bookingLink} " \
                           f"für mehr"
            notificationManager.send_sms(message_text)

with open("logfile.txt", mode="a") as file:
    temp_df = pd.DataFrame(flights_within_budget)
    file.write(f"{temp_df.to_string(index=False)}\n\n")
