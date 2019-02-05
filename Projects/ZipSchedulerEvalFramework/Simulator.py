from Fleet import Fleet
from FifoZipScheduler import FifoZipScheduler
from OptimizedZipScheduler import OptimizedZipScheduler
from DataAccess import DataAccess
from ZipSchedulerEvaluator import ZipSchedulerEvaluator
import pandas as pd


class Simulator:
    def __init__(self):
        pass


def main():
        # try:

        # Set ipython's max row display
        pd.set_option('display.max_row', 1000)

        # Set iPython's max column width to 50
        pd.set_option('display.max_columns', 50)

        # Configure and load fleet data
        # Note: these could also be retrieved from a database
        zips_in_operation_center = ["Zip1", "Zip2", "Zip3", "Zip4", "Zip5", "Zip6", "Zip7", "Zip8", "Zip9", "Zip10"]
        fleet = Fleet(
            max_range_per_zip=160,
            max_orders_per_zip=3,
            flight_speed_per_zip=30,
            total_number_of_zips=10,
            zip_ids=zips_in_operation_center
        )

        # Load hospitals data into DataFrame
        hospitals_csv_file = 'hospitals.csv'
        hospitals = DataAccess.load_from_csv(hospitals_csv_file)
        hospitals.columns = ['hospital_name', 'north', 'east']

        # Load orders data into DataFrame
        orders_csv_file = 'orders.csv'
        orders = DataAccess.load_from_csv(orders_csv_file)
        orders.columns = ['order_id', 'received_time', 'hospital_name', 'priority']

        if hospitals.empty or orders.empty:
            raise ValueError("Cannot load required data from source.")

        # Instantiate different ZipScheduler implementations
        fifo_scheduler = FifoZipScheduler(hospitals, orders, fleet)
        optimized_scheduler = OptimizedZipScheduler(hospitals, orders, fleet)

        # print("Scheduled flights by FifoZipScheduler:")
        # print(fifo_scheduler.get_scheduled_flights())
        # print("Scheduled flights by OptimizedZipScheduler: \n")
        # print(optimized_scheduler.get_scheduled_flights())

        # Instantiate a ZipSchedulerEval object for each ZipScheduler
        fifo_scheduler_evaluator = ZipSchedulerEvaluator(fifo_scheduler)
        optimized_scheduler_evaluator = ZipSchedulerEvaluator(optimized_scheduler)

        # Populate simulated metrics DataFrame for each of the Scheduler implementations
        fifo_scheduler_metrics_df = fifo_scheduler_evaluator.simulate_metrics()
        optimized_scheduler_metrics_df = optimized_scheduler_evaluator.simulate_metrics()
        # print(fifo_scheduler_metrics_df)
        # print(optimized_scheduler_metrics_df)

        if fifo_scheduler_metrics_df.empty or optimized_scheduler_metrics_df.empty:
            raise ValueError("Simulated metrics yielded empty DataFrame. ")

        # Compare the simulated metrics DataFrames from both ZipScheduler Evaluators
        compare_df = fifo_scheduler_metrics_df.T.append(optimized_scheduler_metrics_df.T, ignore_index=True)

        # Note: Printing the df below for demo purposes here, could
        # potentially be stored to database instead
        # Further analysis/insights: Matplotlib, Data Science, etc.
        print("\nresult: \n", compare_df)

        # except Exception as e:
        #     print(e)


if __name__ == '__main__':
    main()