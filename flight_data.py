class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self,p_price,p_departure_airport_code,p_departure_city,
                 p_departure_date,p_destination_airport_code,
                 p_destination_city,p_return_flight_date,p_bookinglink):

        self.price = p_price
        self.departure_airport_code = p_departure_airport_code
        self.departure_city = p_departure_city
        self.departure_date = p_departure_date
        self.destination_airport_code=p_destination_airport_code
        self.destination_city=p_destination_city
        self.return_flight_date = p_return_flight_date
        self.bookingLink = p_bookinglink

    def get_attr_dict(self):
        """returns all Attributes except bookingLink"""
        return {
            "price":self.price,
            "departure_airport_code":self.departure_airport_code,
            "departure_city ": self.departure_city,
            "departure_date ": self.departure_date,
            "destination_airport_code":self.destination_airport_code,
            "destination_city":self.destination_city,
            "return_flight_date":self.return_flight_date
        }

