import pandas as pd


class MetricsEvaluator:
    """Framework for evaluating different implementations of JetScheduler"""

    def __init__(self, jet_scheduler):
        self._scheduler = jet_scheduler
        self._scheduled_flights = jet_scheduler.get_scheduled_flights()  # DataFrame
        self._airports = jet_scheduler.get_airport_data()  # DataFrame
        self._requests = jet_scheduler.get_requests_data()  # DataFrame
        self._fleet = jet_scheduler.get_fleet_data()  # Fleet() Object
        self._cut_off_time = jet_scheduler.get_cut_off_time()  # Seconds since midnight

        # Metrics related to routes scheduled by JetScheduler instance
        self._total_unfulfilled_requests_per_day = 0  # int
        self._total_trips_taken_per_day = 0  # int
        self._total_distance_covered_by_all_jets = 0.0  # unit: in kilometers (float)
        self._avg_distance_covered_per_request = 0  # unit: in kilometers (float)
        # Metrics related to processed Priority of requests
        self._total_emergency_requests_fulfilled_per_day = 0  # int
        self._total_resupply_requests_fulfilled_per_day = 0  # int

        self._avg_time_to_deliver_per_route = 0.0  # unit: in seconds (float)
        self._meters_to_km = 0.001

    def simulate_metrics(self):
        """
        Simulates all metrics and return a DataFrame
        :return: DataFrame
        """
        metrics = [self._scheduler.__class__.__name__,
                   self.total_unfulfilled_requests_per_day(),
                   self.total_trips_taken_per_day(),
                   self.total_distance_covered_by_all_jets(),
                   self.avg_distance_travelled_each_request(),
                   self.avg_time_to_deliver_per_route(),
                   self.total_emergency_requests_fulfilled_per_day(),
                   self.total_resupply_requests_fulfilled_per_day()
                   ]

        # Create a DataFrame from the list of JetScheduler simulated metrics
        df = pd.DataFrame(metrics,
                          index=[
                              'jet_scheduler',
                              'total_unfulfilled_requests_per_day',
                              'total_trips_taken_per_day',
                              'total_distance_covered_by_all_jets',
                              'avg_distance_travelled_each_request',
                              'avg_time_to_deliver_per_route',
                              'total_emergency_requests_fulfilled',
                              'total_resupply_requests_fulfilled'
                          ])

        return df

    def total_unfulfilled_requests_per_day(self):
        """
        Evaluates total number of unfulfilled requests per day
        :return (int)
        """

        self._total_unfulfilled_requests_per_day =\
            self._scheduled_flights['total_unfulfilled_requests'].values.tolist()[-1]

        return self._total_unfulfilled_requests_per_day

    def total_trips_taken_per_day(self):
        """
        Evaluates total_trips_taken_per_day_by_all_jets
        :return (int)
        """

        self._total_trips_taken_per_day = self._scheduled_flights['requests'].map(lambda a: len(a)).sum()

        return self._total_trips_taken_per_day

    def total_distance_covered_by_all_jets(self):
        """
        Evaluates total distance (in km) covered by all jets per day
        :return in kilometers
        """
        self._total_distance_covered_by_all_jets = \
            round((self._scheduled_flights['total_flight_distance'].sum() * self._meters_to_km), 5)

        return self._total_distance_covered_by_all_jets

    def avg_distance_travelled_each_request(self):
        """
        Evaluates total distance (in km) covered by all jets per day
        :return in kilometers
        """

        total_distance_covered_in_a_day = self.total_distance_covered_by_all_jets()
        total_requests_fulfilled_in_a_day = self.total_trips_taken_per_day()

        self._avg_distance_covered_per_request = \
            round((total_distance_covered_in_a_day / total_requests_fulfilled_in_a_day), 5)

        return self._avg_distance_covered_per_request

    def avg_time_to_deliver_per_route(self):
        """
        Evaluates avg time it takes a jet to deliver all its requests in a route
        :return  (int) time in seconds since midnight
        """
        successful_flights = self._scheduled_flights[self._scheduled_flights['is_flight_scheduled?'] == True]

        trip_time_for_each_request = successful_flights["flight_return_time"] - \
                                   successful_flights["flight_schedule_time"]

        self._avg_time_to_deliver_per_route = int(trip_time_for_each_request.sum() / len(successful_flights))

        return self._avg_time_to_deliver_per_route

    def total_emergency_requests_fulfilled_per_day(self):
        """
        Returns total_emergency_requests_fulfilled_per_day
        :return: int
        """

        self._total_emergency_requests_fulfilled_per_day = \
            self._scheduled_flights['priority'].map(lambda a: list(a).count('Emergency')).sum()

        return self._total_emergency_requests_fulfilled_per_day

    def total_resupply_requests_fulfilled_per_day(self):
        """
        Return total_resupply_requests_fulfilled_per_day
        :return: int
        """

        self._total_resupply_requests_fulfilled_per_day = \
            self._scheduled_flights['priority'].map(lambda a: list(a).count('Resupply')).sum()

        return self._total_resupply_requests_fulfilled_per_day