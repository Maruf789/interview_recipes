from ZipScheduler import ZipScheduler
import pandas as pd


class OptimizedZipScheduler(ZipScheduler):
    """OptimizedZipScheduler: Extends ZipScheduler"""

    def __init__(self, hospitals, orders, fleet):
        """
        :param _flight_routes (DataFrame): flight_start_time
                                          FlightScheduled
                                          ZipId
                                          list of OrderIDs
                                          flight_return_time
                                          total_flight_distance
        """
        self._scheduled_flights = pd.DataFrame()  # List of list
        super(OptimizedZipScheduler, self).__init__(hospitals, orders, fleet)

    def get_scheduled_flights(self):
        """
        Returns the flights scheduled by the given Scheduler
        :return (Dataframe): DataFrame with complete schedule of flights
                            in incremental (seconds since midnight) order
                            until the cut off time.
        """
        self._scheduled_flights = self._schedule_flights()
        return self._scheduled_flights

    def _schedule_flights(self):
        """
        Overwrites the method in parent class
        :return (DataFrame): A DataFrame denoting complete schedule of flights
                        in incremental (seconds since midnight) order
                        until the cut off time

        FLIGHT SCHEDULE DATAFRAME COLUMNS
               zip_id (str),
               flight_scheduled (boolean),
               order_ids (List(str)),
               flight_start_time (int),
               flight_return_time (int),
               total_flight_distance (float)
        """
        dummy_data = [[23900, False, "", [], 0, 0],
                      [24900, False, "", [], 0, 0],
                      [25900, False, "", [], 0, 0],
                      [26900, False, "", [], 0, 0],
                      [27900, True, "zip1", [1, 2, 3],  28300, 10000],
                      [28900, True, "zip2", [4, 5, 6],  29300, 20000],
                      [29900, True, "zip3", [7, 8, 9],  30300, 50000],
                      [31900, True, "zip4", [10, 11, 12], 32300, 160000],
                      [32900, True, "zip5", [13, 14, 15],  33300, 140000],
                      [33900, True, "zip6", [16, 17, 18], 34300, 110000],
                      [34900, True, "zip7", [19, 20, 21], 35300, 90000],
                      [35900, True, "zip8", [22, 23, 24], 36300, 90000],
                      [36900, True, "zip9", [25, 26, 27], 37300, 90000],
                      [37900, True, "zip10", [28, 29, 30], 38300, 90000]
                      ]

        df = pd.DataFrame(dummy_data,
                          columns=['flight_schedule_time',
                                   'flight_scheduled',
                                   'zip_id',
                                   'orders',
                                   'flight_return_time',
                                   'total_flight_distance'])

        print("printing optimized scheduler df: \n", df)
        return df
