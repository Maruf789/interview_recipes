JetSchedulerEvalFramework
--
MetricsEvaluator.py simulates each JetScheduler and evaluates the following metrics:
1. Total unfulfilled requests per day:
    Evaluates how many requests left unfulfilled by the Scheduler at the end of a work day.
2. Total trips taken per day:
    Evaluates how many total trips taken by all jets in a day.
3. Total distance covered by all jets 
    Evaluates the total distance (in kilometers) covered by all jets for all of the fulfilled requests.
4. Average distance covered per request 
    Evaluates the average distance covered by a jet per request.
5. Total emergency requests fulfilled per day
    Evaluates the number of total Emergency requests fulfilled per day.
6. Total resupply requests fulfilled per day
    Evaluates the number of total Resupply requests fulfilled per day.
7. Average time to deliver per route
    Evaluates the average time spent a jet to deliver all requests in its route and return back to operation center.


### JetScheduler instances Used: FifoJetScheduler and PriorityJetScheduler
   1. FifoJetScheduler: At each given time interval (configured by client), this Scheduler processes requests in 
   ascending received time.
   2. PriorityJetScheduler: At each given time interval (configured by client), this Scheduler processes
   requests with Emergency priority in ascending received time. It schedules requests with Resupply priority only if 
   in that interval there is no Emergency request received (or if it is not feasible to process the Emergency requests 
   due to long distance, lack of jets, etc.). 
   
### APIs exposed by the JetScheduler:
1. get_scheduled_flights(): all logic regarding scheduling requests rest here. Each child class can implement their own
 logic for scheduling, and use any number of private methods desired.
2. get_airport_data(): getter for Hospitals data (passed on to class Constructor). 
2. get_requests_data(): getter for Requests data (passed on to class Constructor). 
4. get_fleet_data():  getter for Fleet data (passed on to class Constructor). 
5. get_cut_off_time():  getter for cut off time data (passed on to class Constructor). 
6. distance_between_two_points(x,y): calculate distance between two (north, east) points. 


### Run Instructions:


#### Pre-requisite:
  1. Python 3.5 or above, 
  2. Pandas 0.24.1
  3. The data sources (i.e., 'requests.csv', 'airports.csv') 
in the /resources directory of the project. To use different data source 
(e.g.,, different CSV files), you have to change the paths in 
the client script (Simulator.py). For convenience, the project jet file already comes with the two required CSV files. 

### Instructions to simulate:
1. Unzip the Project file: unzip JetSchedulerEvalFramework.jet
2. Run the simulator: python3 Simulator.py


### Room for improvements:
1. add the following metrics to the evaluator:
    