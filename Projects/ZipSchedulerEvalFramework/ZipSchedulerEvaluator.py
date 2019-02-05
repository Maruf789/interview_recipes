import pandas as pd


class ZipSchedulerEvaluator:
    """Framework for evaluating different implementations of ZipScheduler"""

    def __init__(self, zip_scheduler):
        self._scheduler = zip_scheduler
        self._scheduled_flights = zip_scheduler.get_scheduled_flights()  # DataFrame
        self._hospitals = zip_scheduler.get_hospital_data()  # DataFrame
        self._orders = zip_scheduler.get_orders_data()  # DataFrame
        self._fleet = zip_scheduler.get_fleet_data()  # Fleet() Object
        self._cut_off_time = zip_scheduler.get_cut_off_time()  # Seconds since midnight

        # Metrics related to routes scheduled by ZipScheduler instance
        self._total_number_of_unfulfilled_orders_per_day = 0  # int
        self._total_trips_taken_per_day_by_all_zips = 0  # int
        self._total_distance_covered_by_all_zips = 0.0  # unit: in meters (float)

        # Metrics related to processed 'Emergency' Priority orders
        self._processed_all_emergency_orders_first = False  # boolean
        self._processed_emergency_orders_in_ascending_received_time = False  # boolean
        self._avg_time_to_deliver_emergency_orders = 0.0  # unit: in seconds (float)

        # Metrics related to hospital's wait time after order
        self._avg_response_time_of_resupply_orders = 0.0  # unit: in seconds (float)
        self._avg_response_time_of_emergency_orders = 0.0  # unit: in seconds (float)

    def simulate_metrics(self):
        metrics = [self._scheduler.__class__.__name__,
                   self.total_number_of_unfulfilled_orders_per_day(),
                   self.total_trips_taken_per_day_by_all_zips(),
                   self.total_distance_covered_by_all_zips(),
                   self.processed_all_emergency_orders_first(),
                   self.processed_emergency_orders_in_ascending_received_time(),
                   self.avg_time_to_deliver_emergency_orders(),
                   self.avg_response_time_of_resupply_orders(),
                   self.avg_response_time_of_emergency_orders()
                   ]

        # Create a DataFrame from the list of ZipScheduler simulated metrics
        df = pd.DataFrame(metrics,
                          index=[
                              'zip_scheduler',
                              'total_number_of_unfulfilled_orders_per_day',
                              'total_trips_taken_per_day_by_all_zips',
                              'total_distance_covered_by_all_zips',
                              'processed_all_emergency_orders_first',
                              'processed_emergency_orders_in_ascending_received_time',
                              'avg_time_to_deliver_emergency_orders',
                              'avg_response_time_of_resupply_orders',
                              'avg_response_time_of_emergency_orders'
                          ])

        return df

    def total_number_of_unfulfilled_orders_per_day(self):
        """
        Evaluates
        :param
        :return
        """
        return self._total_number_of_unfulfilled_orders_per_day

    def total_trips_taken_per_day_by_all_zips(self):
        """
        Evaluates
        :param
        :return
        """
        return self._total_trips_taken_per_day_by_all_zips

    def total_distance_covered_by_all_zips(self):
        """
        Evaluates
        :param
        :return
        """
        return self._total_distance_covered_by_all_zips

    def processed_all_emergency_orders_first(self):
        """
        Evaluates
        :param
        :return
        """
        return self._processed_all_emergency_orders_first

    def processed_emergency_orders_in_ascending_received_time(self):
        """
        Evaluates
        :param
        :return
        """
        return self._processed_emergency_orders_in_ascending_received_time

    def avg_time_to_deliver_emergency_orders(self):
        """
        Evaluates
        :param
        :return
        """
        return self._avg_time_to_deliver_emergency_orders

    def avg_response_time_of_resupply_orders(self):
        """
        Evaluates
        :param
        :return
        """
        return self._avg_response_time_of_resupply_orders

    def avg_response_time_of_emergency_orders(self):
        """
        Evaluates
        :param
        :return
        """
        return self._avg_time_to_deliver_emergency_orders

