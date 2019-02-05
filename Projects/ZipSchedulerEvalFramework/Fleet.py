class Fleet:
    """ Class that configures the fleet for a ZipLine operation center. """

    def __init__(self,
                 max_range_per_zip,
                 max_orders_per_zip,
                 flight_speed_per_zip,
                 total_number_of_zips,
                 zip_ids
                 ):
        # validate inputs
        if max_range_per_zip <= 0 \
                or max_orders_per_zip <= 0 \
                or flight_speed_per_zip <= 0 \
                or total_number_of_zips <= 0 \
                or len(zip_ids) == 0 \
                or len(zip_ids) != total_number_of_zips:
            raise ValueError("Bad input for Fleet data.")

        self._km_to_meter = 1000
        self._max_range_per_zip = float(max_range_per_zip * self._km_to_meter)  # unit: in meters (float)
        self._max_orders_per_zip = int(max_orders_per_zip)  # int
        self._flight_speed_per_zip = float(flight_speed_per_zip)  # unit: in meters/second (float)
        self._total_number_of_zips = int(total_number_of_zips)  # int
        self._zip_ids = zip_ids  # list(str)

    def get_max_range_per_zip(self):
        return self._max_range_per_zip

    def get_max_orders_per_zip(self):
        return self._max_orders_per_zip

    def get_flight_speed_per_zip(self):
        return self._flight_speed_per_zip

    def get_total_number_of_zips(self):
        return self._total_number_of_zips

    def get_zip_ids(self):
        return self._zip_ids

    # def set_max_range_per_zip(self, max_range_per_zip):
    #     self._max_range_per_zip = max_range_per_zip
    #
    # def set_max_orders_per_zip(self, max_orders_per_zip):
    #     self._max_orders_per_zip = max_orders_per_zip
    #
    # def set_flight_speed_per_zip(self, flight_speed):
    #     self._flight_speed_per_zip = flight_speed
    #
    # def set_total_number_of_zips(self, total_number_of_zips):
    #     self._total_number_of_zips = total_number_of_zips
    #
    # def set_zip_ids(self, zip_ids):
    #     self._zip_ids = zip_ids
