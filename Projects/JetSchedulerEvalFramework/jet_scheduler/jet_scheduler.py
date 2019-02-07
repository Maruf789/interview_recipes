from math import sqrt


class JetScheduler:
    """ Determines whether a flight should be sent out,
    and if so, returns the sequencing of requests the flight
    should deliver."""

    def __init__(self, airports, requests, fleet, cut_off_time=None):
        self._airports = airports  # DataFrame
        self._requests = requests  # DataFrame
        self._fleet = fleet  # Fleet() Object
        self._cut_off_time = cut_off_time  # Seconds since midnight
        self.feet_to_meters = 0.3048

    def get_scheduled_flights(self):
        """
        Returns the flights scheduled by the given Scheduler
        :return (Dataframe): DataFrame with complete schedule of flights
                            in incremental interval (every 1000 seconds
                            since midnight) until the cut off time.
                            The columns include--
                            jet_id (str),
                            flightScheduled (boolean),
                            RequestIDs (List(str)),
                            flight_start_time (int),
                            flight_return_time (int),
                            total_flight_distance (float)
        """
        pass

    def get_airport_data(self):
        return self._airports

    def get_requests_data(self):
        return self._requests

    def get_fleet_data(self):
        return self._fleet

    def get_cut_off_time(self):
        return self._cut_off_time

    def distance_between_two_points(self, point_a, point_b):
        """
          Unit conversion: 1 foot = 0.3048 meter
          Distance Formula between two points: √(x2 − x1)^2 + (y2 − y1)^2
          :param point_a: (tuple) Northing and Easting in feet
          :param point_b: (tuple) Northing and Easting in feet
          :return: (float) distance between point_a and point_b in meters
        """
        a1 = point_a[0] * self.feet_to_meters
        b1 = point_a[1] * self.feet_to_meters
        a2 = point_b[0] * self.feet_to_meters
        b2 = point_b[1] * self.feet_to_meters

        return round(float(sqrt((a2 - a1) ** 2 + (b2 - b1) ** 2)), 5)
