from ZipScheduler import ZipScheduler
import pandas as pd

class FifoZipScheduler(ZipScheduler):
    """FifoZipScheduler: Extends ZipScheduler"""

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
        super(FifoZipScheduler, self).__init__(hospitals, orders, fleet)

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
                            until the cut off time. The DataFrame columns include:
                            zip_id (str),
                            flight_scheduled (boolean),
                            order_ids (List(str)),
                            flight_start_time (int),
                            flight_return_time (int),
                            total_flight_distance (float)
        """

        flight_schedules = []
        flight_initial_start_time = 15000  # initial flight schedule time (in seconds since midnight)
        flight_schedule_interval = 5000  # Schedule flights in every 2000 seconds interval
        cut_off_time = self._determine_cut_off_time(self._cut_off_time, self._orders)
        all_orders_df = self._orders.sort_values(by=['received_time'])
        # all_orders_df.insert(1, 'order_status', 'Unfulfilled')
        # print("printing out the sorted df in Fifo:")
        # print(all_orders_df.head(10))

        list_of_all_op_center_zips = self._fleet.get_zip_ids()
        fulfilled_order_ids = set()
        unfulfilled_order_ids = set()
        active_zips = dict()
        available_zips = list_of_all_op_center_zips  # at the beginning, all zips are available

        for flight_schedule_time in range(flight_initial_start_time, cut_off_time, flight_schedule_interval):
            # Accumulate all orders to be processed at this time
            new_orders_to_process = self._determine_all_orders_to_be_processed(
                all_orders_df,
                flight_schedule_time,
                flight_schedule_interval
            )

            if len(new_orders_to_process) > 0:
                for order_id in new_orders_to_process:
                    if order_id not in unfulfilled_order_ids:
                        unfulfilled_order_ids.add(order_id)
            print("=============================================================================")
            print("\n\nnew_order_to_process at {}: {}".format(flight_schedule_time, new_orders_to_process))
            print("length of new_order_to_process at {}: {}".format(flight_schedule_time, len(new_orders_to_process)))
            print("unfulfilled at {}: {}".format(flight_schedule_time, unfulfilled_order_ids))
            print("length of unfulfilled at {}: {}".format(flight_schedule_time, len(unfulfilled_order_ids)))

            # properly calculate available zips to process above orders
            if len(active_zips) > 0:
                for zip_id in list(active_zips):
                    if flight_schedule_time >= active_zips[zip_id]:
                        available_zips.append(zip_id)
                        print("Inserted {} back to queue!".format(zip_id))
                        active_zips.pop(zip_id)

            print("total zips available at {}: {}".format(flight_schedule_time, available_zips))

            for curr_zip in available_zips:
                available_zips.remove(curr_zip)    # remove it from the list to prevent using the same zip
                if len(unfulfilled_order_ids) > 0:
                    print("curr_zip: ", curr_zip)
                    flight_distance = 0
                    flight_scheduled = False
                    flight_return_time = 0

                    orders_for_current_zip = self._determine_orders_for_current_zip(unfulfilled_order_ids,all_orders_df,self._hospitals,self._fleet.get_max_range_per_zip(),self._fleet.get_max_orders_per_zip())

                    for order_id in orders_for_current_zip:  # ensuring we're not processing the same order twice
                        if order_id in fulfilled_order_ids:
                            orders_for_current_zip.remove(order_id)
                        unfulfilled_order_ids.remove(order_id)

                    print("orders to be processed by current zip: ", orders_for_current_zip)
                    print("length of unfulfilled at {}: {}".format(flight_schedule_time, len(unfulfilled_order_ids)))

                    if len(orders_for_current_zip) > 0:
                        flight_distance = self._total_flight_distance_for_current_zip(orders_for_current_zip, all_orders_df, self._hospitals)
                        flight_return_time = self._determine_zip_return_time(self._fleet.get_flight_speed_per_zip(),flight_distance)
                        # if flight_schedule_time < flight_return_time and flight_distance > 0:
                        flight_scheduled = True

                        current_flight = [flight_schedule_time, flight_scheduled, curr_zip, orders_for_current_zip, flight_return_time, flight_distance]
                        print("current successful flight: ", current_flight)
                        flight_schedules.append(current_flight)

                        # UPDATE ZIP INVENTORY
                        # available_zips.remove(curr_zip)  # make the zip unavailable to take any more orders
                        active_zips[curr_zip] = flight_return_time

                        # UPDATE ORDER INVENTORY
                        # all_orders_df = all_orders_df[~all_orders_df.order_id.isin(orders_in_current_route)]
                        for order_id in orders_for_current_zip:
                            fulfilled_order_ids.add(order_id)
                        # unfulfilled_order_ids.remove(order_id)
                    else:
                        empty_zip_id = ""
                        empty_orders = []
                        current_flight = [flight_schedule_time, flight_scheduled, empty_zip_id, empty_orders, flight_return_time, flight_distance]
                        print("current_empty_flight: ", current_flight)
                        flight_schedules.append(current_flight)
                        break
                else:
                    break

        print("flight_schedules: ", flight_schedules)
        df = pd.DataFrame(flight_schedules, columns=['flight_schedule_time','flight_scheduled','zip_id','orders','flight_return_time','total_flight_distance'])

        print("printing fifo scheduler df: \n", df)
        return df

    def _determine_next_available_zip_id(self, all_available_zips):
        """

        :param all_available_zips:
        :return:
        """
        if len(all_available_zips) > 0:
            return all_available_zips[0]

        return ""

    def _determine_zip_return_time(self,
                                   flight_speed_per_zip,
                                   flight_distance):
        """
        Determines total time a zip takes to complete orders
        in its route and return back to the operation center
        :param flight_start_time (int): seconds since midnight
        :param flight_speed_per_zip (float): meters per second
        :param flight_distance (float):
        :return: (int): seconds since midnight
        """
        if flight_distance <= 0 or flight_speed_per_zip <= 0:
            return 0

        return round((flight_distance / flight_speed_per_zip), 5)

    def _determine_all_orders_to_be_processed(self,
                                              all_orders_df,
                                              time_range_lower,
                                              time_interval):
        """

        :param all_orders_df:
        :param time_range_lower:
        :param time_interval:
        :return:
        """

        time_range_upper = time_range_lower + time_interval
        filtered_orders = all_orders_df[all_orders_df['received_time'].between(time_range_lower,
                                                                               time_range_upper,
                                                                               inclusive=True)]
        if (not filtered_orders.empty) and (filtered_orders.shape[1] > 0):
            return list(filtered_orders.order_id.unique())

        return []

    def _determine_orders_for_current_zip(self,
                                          unfulfilled_order_ids,
                                          all_orders_df,
                                          all_hospitals_df,
                                          max_range_per_zip,
                                          max_orders_per_zip):
        orders_finalized_for_curr_zip = []
        route_distance = 0
        op_center = (0, 0)
        locations = []
        sorted_orders = sorted(unfulfilled_order_ids)

        for i in range(0, len(sorted_orders)):
            order_id = sorted_orders[i]
            hospital_name = str(all_orders_df[all_orders_df['order_id'] == order_id]['hospital_name']
                                .values[0]).strip()
            if len(hospital_name) > 0:  # found hospital name with the order_id
                north_values = all_hospitals_df[all_hospitals_df['hospital_name'] == hospital_name]['north'].values
                east_values = all_hospitals_df[all_hospitals_df['hospital_name'] == hospital_name]['east'].values
                if len(north_values) > 0 and len(east_values) > 0:  # Pandas Series is not empty
                    north = int(north_values[0])
                    east = int(east_values[0])
                    new_hospital_loc = (north, east)

                    if len(locations) == 0:
                        distance_from_last_loc_to_new = self.distance_between_two_points(
                            op_center, new_hospital_loc)
                    else:
                        distance_from_last_loc_to_new = self.distance_between_two_points(
                            locations[-1], new_hospital_loc)

                    distance_from_new_loc_to_op_center = self.distance_between_two_points(
                        new_hospital_loc, op_center)

                    new_distance = route_distance + distance_from_last_loc_to_new + distance_from_new_loc_to_op_center

                    if new_distance <= max_range_per_zip and len(orders_finalized_for_curr_zip) < max_orders_per_zip:
                        orders_finalized_for_curr_zip.append(order_id)
                        locations.append((north, east))
                        route_distance = new_distance

        return orders_finalized_for_curr_zip

    def _determine_cut_off_time(self, user_provided_cut_off_time, orders):
        """

        :param user_provided_cut_off_time:
        :param orders:
        :return:
        """
        if user_provided_cut_off_time:
            return int(user_provided_cut_off_time) + 1
        else:
            return int(orders.sort_values(by=['received_time'], ascending=False)['received_time'].values[0]) + 1

    def _total_flight_distance_for_current_zip(self,
                                               current_orders,
                                               all_orders_df,
                                               all_hospitals_df):
        """

        :param current_orders:
        :param all_orders_df:
        :param all_hospitals_df:
        :return:
        """

        total_orders_in_route = len(current_orders)  # type: int
        if total_orders_in_route == 0:
            return 0

        total_distance = 0
        op_center = (0, 0)
        locations = [op_center]

        for i in range(total_orders_in_route):
            order_id = current_orders[i]
            if order_id in all_orders_df.order_id.unique():
                hospital_name = str(all_orders_df[all_orders_df['order_id'] == order_id]['hospital_name']
                                    .values[0]).strip()
                # print("inside _total_flight_distance_for_current_zip method-- hospital_name: ", hospital_name)
                if len(hospital_name) > 0:  # found hospital name with the order_id
                    north_values = all_hospitals_df[all_hospitals_df['hospital_name'] == hospital_name]['north'].values
                    east_values = all_hospitals_df[all_hospitals_df['hospital_name'] == hospital_name]['east'].values
                    if len(north_values) > 0 and len(east_values) > 0:  # Pandas Series is not empty
                        north = int(north_values[0])
                        east = int(east_values[0])
                        #print("inside _total_flight_distance_for_current_zip method-- (north, east), : ({},{})".format(north, east))
                        locations.append((north, east))

        total_distance += self.distance_between_two_points(locations[0], locations[1])

        i = 1
        j = i + 1
        while i < total_orders_in_route and j <= total_orders_in_route:
            total_distance += self.distance_between_two_points(locations[i], locations[j])
            i += 1
            j += 1

        total_distance += self.distance_between_two_points(locations[len(locations) - 1], op_center)

        print("total_flight_distance for this route: ", int(total_distance))
        return round(total_distance, 5)
