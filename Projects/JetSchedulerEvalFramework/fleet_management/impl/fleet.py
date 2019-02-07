class Fleet:
    """ Class that configures the fleet_management for a JetLine operation center. """

    def __init__(self,
                 max_range_per_jet,
                 max_requests_per_jet,
                 flight_speed_per_jet,
                 total_number_of_jets,
                 jet_ids
                 ):
        # validate inputs
        if max_range_per_jet <= 0 \
                or max_requests_per_jet <= 0 \
                or flight_speed_per_jet <= 0 \
                or total_number_of_jets <= 0 \
                or len(jet_ids) == 0 \
                or len(jet_ids) != total_number_of_jets:
            raise ValueError("Bad input for Fleet object.")

        self._km_to_meter = 1000    # type: int
        self._max_range_per_jet = float(max_range_per_jet * self._km_to_meter) # unit:in meters (type: float)
        self._max_requests_per_jet = int(max_requests_per_jet)  # int
        self._flight_speed_per_jet = float(flight_speed_per_jet)  # unit: in meters/second (type: float)
        self._total_number_of_jets = int(total_number_of_jets)  # type: int
        self._jet_ids = jet_ids  # list(str)

    def get_max_range_per_jet(self):
        return self._max_range_per_jet

    def get_max_requests_per_jet(self):
        return self._max_requests_per_jet

    def get_flight_speed_per_jet(self):
        return self._flight_speed_per_jet

    def get_total_number_of_jets(self):
        return self._total_number_of_jets

    def get_jet_ids(self):
        return self._jet_ids
