# hackMIT
Project for hackMIT2019. 

Automatically detects if an AWS instance has been running and stops it, emailing the user that those instances were stopped. 

## Dependencies 

This requires you to have your aws account configured as well as boto3 and smptlib

## How to Run
When running `hackMIT.py`, it will prompt you for the maximum length you want your AWS instance to run as well as your email. 
Then `check.py` will search through all the AWS regions in the US and list all active instances. 

If an instance has been running for too long, it will alert the user via command prompt as well as by email. 

The command line output will look a little something like this:

~~~~
What is the max length you want your instances to run(in minutes)? 1
Enter your email so we can alert you of changes: lisabdunlap@berkeley.edu
------------- Running Instances in us-west-1 --------------
----------------------------------
------------- Running Instances in us-west-2 --------------
----------------------------------
------------- Running Instances in us-east-1 --------------
----------------------------------
------------- Running Instances in us-east-2 --------------
Key Name: ray-autoscaler_us-east-2	 Id: i-0e603cc764698f6b8	 Type: t2.micro
Key Name: ray-autoscaler_us-east-2	 Id: i-04ea9e3d69f2beb29	 Type: t2.micro
----------------------------------
Instance ray-autoscaler_us-east-2 has been running for 2 minutes
Instance ray-autoscaler_us-east-2 has been running to long..... Stopping now.......
Instance ray-autoscaler_us-east-2 has been running for 0 minutes
Instace ray-autoscaler_us-east-2 still has 0 minutes before auto-stopping
Stopping: (Key Name: ray-autoscaler_us-east-2	 ID: i-0e603cc764698f6b8	 Type: t2.micro)

-------------------
MacBook-Pro-16:hackMIT lisadunlap$ python hackMIT.py
What is the max length you want your instances to run(in minutes)? 2
Enter your email so we can alert you of changes: lisabdunlap@berkeley.edu
------------- Running Instances in us-west-1 --------------
----------------------------------
------------- Running Instances in us-west-2 --------------
----------------------------------
------------- Running Instances in us-east-1 --------------
----------------------------------
------------- Running Instances in us-east-2 --------------
Key Name: ray-autoscaler_us-east-2	 Id: i-07db337d6e3430696	 Type: t2.micro
Key Name: ray-autoscaler_us-east-2	 Id: i-04ea9e3d69f2beb29	 Type: t2.micro
----------------------------------
Instance ray-autoscaler_us-east-2 has been running for 0 minutes
Instace ray-autoscaler_us-east-2 still has 1 minutes before auto-stopping
Instance ray-autoscaler_us-east-2 has been running for 4 minutes
Instance ray-autoscaler_us-east-2 has been running to long..... Stopping now.......
Stopping: (Key Name: ray-autoscaler_us-east-2	 ID: i-04ea9e3d69f2beb29	 Type: t2.micro)

-------------------
~~~~

You should also get an email that looks something like this:

~~~~
We noticed some of your AWS instances have been running quite long (<2 minutes). In order to save you money, we have auto-stopped them so you dont go bankrupt.

List of auto-stopped AWS instance(s):

Key Name(s): ['ray-autoscaler_us-east-2']
Instance Id(s): ['i-04ea9e3d69f2beb29']
Instance Type(s): ['t2.micro']


I gotchu b.
 ~~~~
 
 ## Where to Go From Here
 Integrate it into existing infrastructure so that it preforms these checks periodically without the user prompting it. There should also be an option to disable this feature when running certain clusters. 
