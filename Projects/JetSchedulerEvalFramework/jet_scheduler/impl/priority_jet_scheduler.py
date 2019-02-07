from jet_scheduler.jet_scheduler import JetScheduler
import pandas as pd
from copy import deepcopy


class PriorityJetScheduler(JetScheduler):
    """PriorityJetScheduler: Extends JetScheduler"""

    def __init__(self, airports, requests, fleet, interval, cut_off_time=None):
        """
        :param _flight_routes (DataFrame): flight_start_time
                                          FlightScheduled
                                          JetId
                                          list of RequestIDs
                                          flight_return_time
                                          total_flight_distance
        """
        self._scheduled_flights = pd.DataFrame()  # List of list
        self._interval = interval
        self._flight_initial_start_time = 1000  # seconds since midnight
        super(PriorityJetScheduler, self).__init__(airports, requests, fleet, cut_off_time)

    def get_scheduled_flights(self):
        """
        Returns the flights scheduled by the given Scheduler
        :return (Dataframe): DataFrame with complete schedule of flights
                            in incremental (seconds since midnight) request
                            until the cut off time.
        """
        self._scheduled_flights = self._schedule_flights()
        return self._scheduled_flights

    def _schedule_flights(self):
        """
        Overwrites the method in parent class
        :return (DataFrame): A DataFrame denoting complete schedule of flights
                            in incremental (seconds since midnight) request
                            until the cut off time. The DataFrame columns include:
                            jet_id (str),
                            flight_scheduled (boolean),
                            request_ids (List(str)),
                            flight_start_time (int),
                            flight_return_time (int),
                            total_flight_distance (float)
        """

        flight_schedules = []
        cut_off_time = self._determine_cut_off_time(self._cut_off_time, self._requests)
        all_requests_df = self._requests.sort_values(by=['priority', 'received_time'])

        fulfilled_request_ids = set()
        unfulfilled_request_ids = set()
        active_jets = dict()
        available_jets = deepcopy(self._fleet.get_jet_ids())  # at the beginning, all jets are available

        for flight_schedule_time in range(self._flight_initial_start_time, cut_off_time, self._interval):
            # Accumulate all requests to be processed at this time
            new_requests_to_process = self._determine_all_requests_to_be_processed(all_requests_df, flight_schedule_time,
                                                                               self._interval)
            if len(new_requests_to_process) > 0:
                for request_id in new_requests_to_process:
                    if request_id not in unfulfilled_request_ids:
                        unfulfilled_request_ids.add(request_id)

            print("\n\n=============================== PRIORITY SCHEDULER ==============================================")
            print("new_request_to_process at {}: {}".format(flight_schedule_time, new_requests_to_process))
            # print("length of new_request_to_process at {}: {}".format(flight_schedule_time, len(new_requests_to_process)))
            print("unfulfilled at {}: {}".format(flight_schedule_time, unfulfilled_request_ids))
            # print("length of unfulfilled at {}: {}".format(flight_schedule_time, len(unfulfilled_request_ids)))

            # properly calculate available jets to process above requests
            if len(active_jets) > 0:
                for jet_id in list(active_jets):
                    if flight_schedule_time >= active_jets[jet_id]:
                        available_jets.append(jet_id)  # print("{} has returned to op_center!".format(jet_id))
                        active_jets.pop(jet_id)
            # print("self._fleet.get_jet_ids() at {}: {}".format(flight_schedule_time, self._fleet.get_jet_ids()))
            print("total available jets available at {}: {}".format(flight_schedule_time, available_jets))
            print("total active jets available at {}: {}".format(flight_schedule_time,
                                                                 [active_jets.keys() if len(active_jets) != 0 else []]))

            if len(unfulfilled_request_ids) == 0:  # no requests left to process, return False
                current_flight = [flight_schedule_time, False, "", [], [], 0, 0, 0]
                flight_schedules.append(current_flight)

            for curr_jet in list(available_jets):
                if len(unfulfilled_request_ids) == 0:  # no requests left to process, return False
                    break
                print("\ncurr_jet: ", curr_jet)
                requests_for_current_jet = self._determine_requests_for_current_jet(
                    sorted(unfulfilled_request_ids),
                    all_requests_df,
                    self._airports,
                    self._fleet.get_max_range_per_jet(),
                    self._fleet.get_max_requests_per_jet()
                )

                if len(requests_for_current_jet) > 0:
                    for request_id in requests_for_current_jet:  # ensuring we're not processing the same request twice
                        if request_id in fulfilled_request_ids:
                            requests_for_current_jet.remove(request_id)
                        unfulfilled_request_ids.remove(request_id)

                    priority_for_each_request = self._determine_priority_of_request(requests_for_current_jet, all_requests_df)
                    total_unfulfilled_requests = len(unfulfilled_request_ids)
                    flight_distance = self._total_flight_distance_for_current_jet(
                        requests_for_current_jet, all_requests_df, self._airports)
                    flight_return_time = self._determine_jet_return_time(
                        flight_schedule_time, self._fleet.get_flight_speed_per_jet(), flight_distance)
                    flight_scheduled = True

                    current_flight = [flight_schedule_time, flight_scheduled, curr_jet,
                                      requests_for_current_jet, priority_for_each_request,
                                      flight_return_time, flight_distance, total_unfulfilled_requests]
                    flight_schedules.append(current_flight)

                    # UPDATE ZIP INVENTORY
                    active_jets[curr_jet] = flight_return_time # make the jet unavailable to take any more requests
                    available_jets.remove(curr_jet)  # remove it from the list to prevent using the same jet

                    # UPDATE ORDER INVENTORY
                    for request_id in requests_for_current_jet:
                        fulfilled_request_ids.add(request_id)

        df = pd.DataFrame(flight_schedules, columns=['flight_schedule_time',
                                                     'is_flight_scheduled?',
                                                     'jet_id',
                                                     'requests',
                                                     'priority',
                                                     'flight_return_time',
                                                     'total_flight_distance',
                                                     'total_unfulfilled_requests'
                                                     ])

        print("Displaying Scheduled flights by PriorityJetScheduler: \n", df)
        return df

    def _determine_jet_return_time(self,
                                   flight_start_time,
                                   flight_speed_per_jet,
                                   flight_distance):
        """
        Determines the time it takes a jet to complete requests
        in its route and return back to the operation center
        :param flight_start_time (int): seconds since midnight
        :param flight_speed_per_jet (float): meters per second
        :param flight_distance (float):
        :return: (int): seconds since midnight
        """
        if flight_distance <= 0 or flight_speed_per_jet <= 0:
            return 0

        return_time = int((flight_distance / flight_speed_per_jet) + flight_start_time)

        return return_time

    def _determine_all_requests_to_be_processed(self,
                                              all_requests_df,
                                              time_range_lower,
                                              time_interval):
        """

        :param all_requests_df:
        :param time_range_lower:
        :param time_interval:
        :return:
        """

        time_range_upper = time_range_lower + time_interval
        filtered_requests = all_requests_df[all_requests_df['received_time'].between(time_range_lower,
                                                                               time_range_upper,
                                                                               inclusive=True)]

        if (not filtered_requests.empty) and (filtered_requests.shape[1] > 0):
            return list(filtered_requests.request_id.unique())

        return []

    def _determine_requests_for_current_jet(self,
                                          unfulfilled_request_ids,
                                          all_requests_df,
                                          all_airports_df,
                                          max_range_per_jet,
                                          max_requests_per_jet):
        requests_finalized_for_curr_jet = []
        route_distance = 0
        op_center = (0, 0)
        locations = []
        emergency_requests = []

        for request_id in unfulfilled_request_ids:
            priority = str(all_requests_df[all_requests_df['request_id'] == request_id]['priority'].values[0]).strip()
            if 'Emergency' in priority:
                emergency_requests.append(request_id)

        print("emergency requests for current jet: ", emergency_requests)
        emergency_requests_length = len(emergency_requests)

        if emergency_requests_length == 0:
            processable_requests = unfulfilled_request_ids
        elif 0 < emergency_requests_length < 3:
            processable_requests = emergency_requests + [x for x in unfulfilled_request_ids if x not in emergency_requests]
        else:
            processable_requests = emergency_requests

        print("processable_requests for current jet: ", processable_requests)

        if len(processable_requests) == 0:
            return []

        for i in range(0, len(processable_requests)):
            request_id = processable_requests[i]
            airport_name = str(all_requests_df[all_requests_df['request_id'] == request_id]['airport_name']
                                .values[0]).strip()
            print("airport name: {},".format(airport_name), end=" ")
            if len(airport_name) > 0:
                north_values = all_airports_df[all_airports_df['airport_name'] == airport_name][
                    'north'].values
                print("north_values: {},".format(north_values), end=" ")
                east_values = all_airports_df[all_airports_df['airport_name'] == airport_name][
                    'east'].values
                print("east_values: {},".format(east_values), end=" ")
                if len(north_values) > 0 and len(east_values) > 0:
                    north = int(north_values[0])
                    east = int(east_values[0])
                    new_airport_loc = (north, east)
                    print("(north, east): {},".format(new_airport_loc))

                    if len(locations) == 0:
                        distance_from_last_loc_to_new = self.distance_between_two_points(
                            op_center, new_airport_loc)
                    else:
                        distance_from_last_loc_to_new = self.distance_between_two_points(
                            locations[-1], new_airport_loc)

                    distance_from_new_loc_to_op_center = self.distance_between_two_points(
                        new_airport_loc, op_center)

                    new_distance = route_distance + distance_from_last_loc_to_new + distance_from_new_loc_to_op_center

                    print("requests_finalized_for_curr_jet SO FAR: ", requests_finalized_for_curr_jet)
                    print("if request_id {} added, new_distance {}: ".format(request_id, int(new_distance)))

                    if new_distance <= max_range_per_jet and len(
                            requests_finalized_for_curr_jet) < max_requests_per_jet:
                        requests_finalized_for_curr_jet.append(request_id)
                        locations.append(new_airport_loc)
                        route_distance = new_distance
                        if len(requests_finalized_for_curr_jet) == max_requests_per_jet:
                            print("requests_FINALIZED_for_curr_jet: ", requests_finalized_for_curr_jet)
                            return requests_finalized_for_curr_jet

        return requests_finalized_for_curr_jet

    def _determine_cut_off_time(self, user_provided_cut_off_time, requests):
        """

        :param user_provided_cut_off_time:
        :param requests:
        :return:
        """
        if user_provided_cut_off_time:
            return int(user_provided_cut_off_time) + 1
        else:
            return int(
                requests.sort_values(by=['received_time'], ascending=False)['received_time'].values[0]) + 1

    def _determine_priority_of_request(self, requests_for_current_jet, all_requests_df):
        """
        Populates the priority of each request delivered by the jet in a route
        :param requests_for_current_jet (list): list of requests current jet would deliver
        :param all_requests_df (DataFrame): the DataFrame containing all requests
        :return: (list): the priority value for each request in the route
        """
        priority_list = []

        for i in range(len(requests_for_current_jet)):
            request_id = requests_for_current_jet[i]
            priority_values = all_requests_df[all_requests_df['request_id'] == request_id]['priority'].values
            if len(priority_values) > 0:
                priority = str(priority_values[0]).strip()
                priority_list.append(priority)

        return priority_list

    def _total_flight_distance_for_current_jet(self,
                                               current_requests,
                                               all_requests_df,
                                               all_airports_df):
        """

        :param current_requests:
        :param all_requests_df:
        :param all_airports_df:
        :return:
        """

        total_requests_in_route = len(current_requests)  # type: int
        if total_requests_in_route == 0:
            return 0

        total_distance = 0
        op_center = (0, 0)
        locations = [op_center]

        for i in range(total_requests_in_route):
            request_id = current_requests[i]
            if request_id in all_requests_df.request_id.unique():
                airport_name = str(all_requests_df[all_requests_df['request_id'] == request_id]['airport_name']
                                    .values[0]).strip()
                if len(airport_name) > 0:  # found airport name with the request_id
                    north_values = all_airports_df[all_airports_df['airport_name'] == airport_name][
                        'north'].values
                    east_values = all_airports_df[all_airports_df['airport_name'] == airport_name][
                        'east'].values
                    if len(north_values) > 0 and len(east_values) > 0:  # Pandas Series is not empty
                        north = int(north_values[0])
                        east = int(east_values[0])
                        locations.append((north, east))

        total_distance += self.distance_between_two_points(locations[0], locations[1])

        i = 1
        j = i + 1
        while i < total_requests_in_route and j <= total_requests_in_route:
            total_distance += self.distance_between_two_points(locations[i], locations[j])
            i += 1
            j += 1

        total_distance += self.distance_between_two_points(locations[len(locations) - 1], op_center)

        return round(total_distance, 5)
