"""
running_log.py: A running logger for runners
DS2501: Lab for Intermediate Programming with Data
"""

class RunningLog:

    def __init__(self):
        """ The running log constructor. How you store each run is up to you! """
        self.runs = []

    def add_run(self, hms, dist_km):
        """ Record a run.  The time is given as 'hh:mm:ss' and the distance is in kilometers """
        self.runs.append([hms, dist_km])

    def num_runs(self):
        """ How many run records are in the database? """
        return len(self.runs)

    def plot(self):
        import matplotlib.pyplot as plt
        """ Generate a line plot showing the average pace (minutes per kilometer) for
        run1, run2, .... run N. The x-axis is the run number, and the y-axis is the average
        pace for that run. """
        
        # Go through each run and append the pace to a list
        paces = []
        for run in self.runs:
            # Split running time into numbers for plotting.
            time = run[0]
            dist = float(run[1])
            hours = int(time[0:2])
            mins = int(time[3:5])
            secs = int(time[6:8])
            
            total = secs + (60 * mins) + (3600 * hours)
            total_mins = total / 60
            pace = total_mins / dist
            paces.append(pace)
        
        # Plot
        x = [i for i in range(1, len(paces) + 1)]
        
        plt.scatter(x, paces)
        plt.xlabel("Run Number")
        plt.ylabel("Pace (minutes / km")
        plt.title("Pace of Runs in RunningLog Object")
        plt.xticks(x)
        plt.draw()

    def save(self, filename):
        """ OPTIONAL FOR A FIVE: Save the data to a file. """
        # Saves to text file
        # Each run is a new line
        textfile = open(filename, "w")
        for run in self.runs:
            textfile.write(str(run) + "\n")
        textfile.close()

    def load(self, filename):
        """ OPTIONAL FOR A FIVE: Load the data from a file """
        # Compatible with the type of text files created by save()
        import ast
        textfile = open(filename, "r")
        if textfile:
            log = textfile.readlines()
            if log[0] != '\n':
                for line in log:
                    runlist = ast.literal_eval(line.strip())
                    self.add_run(runlist[0], runlist[1])
            else:
                pass
        else:
            pass
    def __str__(self):
        # Helpful for testing / debug
        return str(self.runs)

def main():

    # Instantiate a new running log
    logger = RunningLog()

    # This is optional
    logger.load("runninglog")

    # Here are 4 sample running events
    logger.add_run("00:32:14", 5.1)
    logger.add_run("00:34:59", 5.5)
    logger.add_run("00:29:01", 4.9)
    logger.add_run("00:30:00", 5.0)
    logger.add_run("00:33:14", 5.8)
    logger.add_run("00:30:00", 4.2)
    logger.add_run("00:00:09", 0.1)
    logger.add_run("00:59:59", 6.3)
    logger.add_run("01:45:32", 13.1)
    logger.add_run("00:02:00", 1.5)
    # Add at least 6 more...

    # Output some data
    print(f"There are {logger.num_runs()} runs in the database")
    logger.plot()

    # This is also optional
    # Uncomment this if you'd like. It works, but it will of course cause the
    # runs added manually in lines 88-98 to be re-saved repeatedly if load()
    # is used.
    
    # logger.save("runninglog")

main()
