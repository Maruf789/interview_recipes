from fleet_management.impl.fleet import Fleet
from jet_scheduler.impl.fifo_jet_scheduler import FifoJetScheduler
from jet_scheduler.impl.priority_jet_scheduler import PriorityJetScheduler
from data_pipeline.impl.data_access import DataAccess
from evaluator.impl.metrics_evaluator import MetricsEvaluator
import pandas as pd


class Simulator:
    def __init__(self):
        pass


def main():
        # try:
        # Set Pandas display
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 2000)

        # Configure and load fleet_management data
        # Note: Ideally these could also be retrieved from a database
        jets_in_operation_center = ["Jet1", "Jet2", "Jet3", "Jet4", "Jet5", "Jet6", "Jet7", "Jet8", "Jet9", "Jet10"]
        fleet = Fleet(
            max_range_per_jet=160,
            max_requests_per_jet=3,
            flight_speed_per_jet=30,
            total_number_of_jets=10,
            jet_ids=jets_in_operation_center
        )

        # Load airports data into DataFrame
        airports_csv_file = 'resources/airports.csv'
        airports = DataAccess.load_from_csv(airports_csv_file)
        airports.columns = ['airport_name', 'north', 'east']

        # Load requests data into DataFrame
        requests_csv_file = 'resources/requests.csv'
        requests = DataAccess.load_from_csv(requests_csv_file)
        requests.columns = ['request_id', 'received_time', 'airport_name', 'priority']

        if airports.empty or requests.empty:
            raise ValueError("Cannot load required data from source.")

        # Instantiate different JetScheduler implementations
        interval = 3600  # Schedule every hour
        fifo_scheduler = FifoJetScheduler(airports, requests, fleet, interval)
        priority_scheduler = PriorityJetScheduler(airports, requests, fleet, interval)

        print("Simulating each JetScheduler to schedule flights and generate metrics. Please wait..")
        # Instantiate a JetSchedulerEval object for each JetScheduler
        fifo_scheduler_evaluator = MetricsEvaluator(fifo_scheduler)
        priority_scheduler_evaluator = MetricsEvaluator(priority_scheduler)

        # Populate simulated metrics DataFrame for each of the Scheduler implementations
        fifo_scheduler_metrics_df = fifo_scheduler_evaluator.simulate_metrics()
        priority_scheduler_metrics_df = priority_scheduler_evaluator.simulate_metrics()

        if fifo_scheduler_metrics_df.empty or priority_scheduler_metrics_df.empty:
            raise ValueError("Simulated metrics yielded empty DataFrame. ")

        # Compare the simulated metrics DataFrames from both JetScheduler Evaluators
        compare_df = fifo_scheduler_metrics_df.T.append(priority_scheduler_metrics_df.T, ignore_index=True)

        # Note: Printing the df below for demo purposes here, could
        # potentially be stored to database instead
        # Further analysis/insights: Matplotlib, Data Science, etc.
        print("\nDisplaying the combined JetSchedulerEvaluator's simulated metrics for all JetSchedulers: \n",
              compare_df)

        # except Exception as e:
        #     print(e)


if __name__ == '__main__':
    main()
