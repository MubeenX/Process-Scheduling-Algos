import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from collections import namedtuple
import numpy as np

def SRT():
    class Process:
        def __init__(self, id, arrivalTime, burstTime):
            self.id = id
            self.arrivalTime = arrivalTime
            self.burstTime = burstTime
            self.remainingTime = burstTime
            self.completionTime = 0
            self.utilization = 0

    def findShortestProcess(processes, currentTime):
        shortestIndex = -1
        shortestTime = float('inf')

        for i, process in enumerate(processes):
            if process.arrivalTime <= currentTime and process.remainingTime < shortestTime and process.remainingTime > 0:
                shortestIndex = i
                shortestTime = process.remainingTime

        return shortestIndex

    def plot_gantt_chart(ganttChart, endTime):
        fig, ax = plt.subplots(figsize=(12, 2))
        y = 0
        for i, (start, process) in enumerate(ganttChart):
            end = ganttChart[i+1][0] if i+1 < len(ganttChart) else endTime
            ax.add_patch(Rectangle((start, y), end - start, 0.8, facecolor='orange', edgecolor='black'))
            ax.text(start + (end - start) / 2, y + 0.4, process, ha='center', va='center', fontsize=10)
        ax.set_xlabel('Time')
        ax.set_yticks([])
        ax.set_xlim(0, endTime)
        ax.set_xticks(range(0, endTime + 1))
        plt.tight_layout()
        plt.show()

    if __name__ == "__main__":
        print("\n------------------------- Scheduling Algorithm Selected: Shortest Remaining Time (SRT) ------------------------- \n")
        n = int(input("How many processes?: "))
        print('\n')
        processes = []

        # Input process details
        for i in range(n):
            id = i + 1
            arrivalTime, burstTime = map(int, input(f"Process {i+1}) Arrival time and burst time (separated by space): ").split())
            processes.append(Process(id, arrivalTime, burstTime))

        currentTime = 0
        completedProcesses = 0

        # Gantt chart
        ganttChart = []


        while completedProcesses < n:
            shortestProcessIndex = findShortestProcess(processes, currentTime)

            if shortestProcessIndex == -1:
                # No process available to execute, increment time
                currentTime += 1
            else:
            
                ganttChart.append((currentTime, f"P{processes[shortestProcessIndex].id}"))
                processes[shortestProcessIndex].remainingTime -= 1

                if processes[shortestProcessIndex].remainingTime == 0:
                    # Process has completed
                    completedProcesses += 1
                    processes[shortestProcessIndex].completionTime = currentTime + 1

                currentTime += 1

    total_time = max(process.completionTime for process in processes)

        # Calculate turnaround time, waiting time, and server utilization
    totalTurnaroundTime = 0
    totalWaitingTime = 0

    
    print(" Process   Arrival Time   Burst Time   Turnaround Time   Waiting Time   Utilization  ")


    for process in processes:
            turnaroundTime = process.completionTime - process.arrivalTime
            waitingTime = turnaroundTime - process.burstTime
            process.utilization = (process.burstTime / total_time) * 100

            totalTurnaroundTime += turnaroundTime
            totalWaitingTime += waitingTime

            print(f" P{process.id:<7}   {process.arrivalTime:<12}   {process.burstTime:<10}   {turnaroundTime:<15}   {waitingTime:<12}   {process.utilization:<10.2f}%  ")


        
        # Calculate and display average turnaround time and average waiting time
    avgTurnaroundTime = totalTurnaroundTime / n
    avgWaitingTime = totalWaitingTime / n

    print(f"\nAverage Turnaround Time: {avgTurnaroundTime:.2f}")
    print(f"Average Waiting Time: {avgWaitingTime:.2f}")
        

    # Display Gantt chart (Visual Version)
    plot_gantt_chart(ganttChart, currentTime)

def SJF():
    Process = namedtuple("Process", ["name", "burst_time", "arrival_time"])

    def sjf_scheduling(processes):
        n = len(processes)
        total_time = sum([p.burst_time for p in processes])  # Total execution time for all processes

        # Sort the processes based on their arrival times and then by their burst times
        sorted_processes = sorted(processes, key=lambda x: (x.arrival_time, x.burst_time))

        completion_time = 0
        result = []
        total_turnaround_time = 0
        total_wait_time = 0

        while sorted_processes:
            # Find all processes that have arrived
            available_processes = [p for p in sorted_processes if p.arrival_time <= completion_time]

            if available_processes:
                # Choose the process with the shortest burst time among the available processes
                p = min(available_processes, key=lambda x: x.burst_time)

                response_time = completion_time - p.arrival_time
                completion_time += p.burst_time
                waiting_time = response_time
                turnaround_time = waiting_time + p.burst_time
                utilization_percent = (p.burst_time / total_time) * 100  # Calculate Utilization for each process

                total_turnaround_time += turnaround_time
                total_wait_time += waiting_time
                
                result.append({
                    "Process No.": p.name,
                    "Arrival Time": p.arrival_time,
                    "Burst Time": p.burst_time,
                    "Completion Time": completion_time,
                    "Turn-around Time": turnaround_time,
                    "Wait Time": waiting_time,
                    "Response Time": response_time,
                    "Utilization": f"{utilization_percent:.2f}%"
                })

                sorted_processes.remove(p)
            else:
                # If no processes have arrived yet, simply increment the completion_time
                completion_time += 1

        avg_turnaround_time = total_turnaround_time / n
        avg_wait_time = total_wait_time / n

        return result, avg_turnaround_time, avg_wait_time


    def plot_gantt_chart(schedule):
        fig, ax = plt.subplots(figsize=(12, 2))
        for idx, item in enumerate(schedule):
            start = item['Completion Time'] - item['Burst Time']
            end = item['Completion Time']
            ax.broken_barh([(start, end - start)], (0, 1), facecolors=('orange'), edgecolor=("black"))
            ax.text(start + (end - start) / 2, 0.5, item['Process No.'], ha='center', va='center', fontsize=10)
        
        # Modify xticks to show integer numbers only
        max_completion_time = max([item['Completion Time'] for item in schedule])
        ax.set_xticks(np.arange(0, max_completion_time + 1, 1))
        ax.set_xlabel("Time")
        plt.tight_layout()
        plt.show()



    if __name__ == "__main__":
        print("\n------------------------- Scheduling Algorithm: Shortest Job First (SJF) ------------------------- \n")
        num_processes = int(input("How many processes?: "))
        print('\n')
        processes = []
        
        for i in range(num_processes):
            arrival_time = int(input(f"> Arrival time for process P{i+1} (for e.g: 0, 1, 2): "))
            burst_time = int(input(f"Execution time for process P{i+1}: "))
            print('\n')
            processes.append(Process(f"P{i+1}", burst_time, arrival_time))
            
        schedule, avg_turnaround_time, avg_wait_time = sjf_scheduling(processes)

    
        headers = ["Process", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time", "Utilization"]
        format_string = "{:<10} {:<15} {:<12} {:<18} {:<18} {:<15} {:<15}"

        print(format_string.format(*headers))

        for item in schedule:
            process_no = f"{item['Process No.']}"
            arrival_time = item['Arrival Time']
            burst_time = item['Burst Time']
            completion_time = item['Completion Time']
            turnaround_time = item['Turn-around Time']
            wait_time = item['Wait Time']
            utilization = item['Utilization']
            
            print(format_string.format(process_no, arrival_time, burst_time, completion_time, turnaround_time, wait_time, utilization))

        print(f"\nAverage Turnaround Time: {avg_turnaround_time:.2f}")
        print(f"Average Wait Time: {avg_wait_time:.2f}")
        plot_gantt_chart(schedule)

def HRRN():
    class Process:
        def __init__(self, pid, arrival_time, burst_time):
            self.pid = pid
            self.arrival_time = arrival_time
            self.burst_time = burst_time
            self.completion_time = 0
            self.turnaround_time = 0
            self.waiting_time = 0
            self.utilization = 0
            self.completed = False

    def highest_response_ratio_next(processes):
        total_processes = len(processes)
        completed_processes = 0
        time = 0
        total_time = sum(p.burst_time for p in processes)  # Total execution time

        while completed_processes < total_processes:
            ready_processes = [p for p in processes if p.arrival_time <= time and not p.completed]

            if not ready_processes:
                time += 1
                continue

            next_process = max(ready_processes, key=lambda x: (time - x.arrival_time + x.burst_time) / x.burst_time)
            time += next_process.burst_time
            next_process.completion_time = time
            next_process.turnaround_time = next_process.completion_time - next_process.arrival_time
            next_process.waiting_time = next_process.turnaround_time - next_process.burst_time
            next_process.completed = True
            completed_processes += 1
        for process in processes:
            process.utilization = (process.burst_time / total_time) * 100


    def plot_gantt_chart(schedule):
        fig, ax = plt.subplots(figsize=(12, 2))
        for idx, process in enumerate(schedule):
            start = process['Completion Time'] - process['Burst Time']
            end = process['Completion Time']
            ax.broken_barh([(start, end - start)], (0, 1), facecolors=('orange'), edgecolor=("black"))
            ax.text(start + (end - start) / 2, 0.5, f"P{process['Process No.']}", ha='center', va='center', fontsize=10)
        ax.set_xticks(np.arange(0, int(max(p['Completion Time'] for p in schedule)) + 1))
        ax.set_xlabel("Time")
        ax.set_yticks([])
        plt.tight_layout()
        plt.show()

    if __name__ == "__main__":
        print("\n------------------------- Scheduling Algorithm: Highest Response Ratio Next (HRRN) ------------------------- \n")
        num_processes = int(input("How many processes?: "))
        print('\n')
        processes = []

        for i in range(num_processes):
            arrival_time = int(input(f"> Arrival time for process P{i+1} (for e.g: 0, 1, 2): "))
            burst_time = int(input(f"Execution time for process P{i+1}: "))
            print('\n')
            processes.append(Process(i+1, arrival_time, burst_time))

        highest_response_ratio_next(processes)
        
        processes.sort(key=lambda x: x.completion_time)

        avg_turnaround = sum([p.turnaround_time for p in processes]) / num_processes
        avg_wait = sum([p.waiting_time for p in processes]) / num_processes

        headers = ["Process", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time" , "Utilization"]
        format_string = "{:<10} {:<15} {:<12} {:<18} {:<18} {:<15} {:<15}"
        print(format_string.format(*headers))
        for process in processes:
            print(format_string.format(
                f"P{process.pid}" , process.arrival_time, process.burst_time , process.completion_time , process.turnaround_time,process.waiting_time, f"{process.utilization:.2f}%"))

        
                
        print(f"\nAverage Turnaround Time: {avg_turnaround:.2f}")
        print(f"Average Wait Time: {avg_wait:.2f}")

        execution_sequence = [{"Process No.": p.pid, "Burst Time": p.burst_time, "Completion Time": p.completion_time} for p in sorted(processes, key=lambda x: x.completion_time)]
        plot_gantt_chart(execution_sequence)  

def Exec_Control():
    print("\n\n- Press 5 to Re-execute the program. \n- Press 4 to Exit.\n")
    opt = str(input("> Your Option: "))
    if (opt == "5" ):
        start()
    elif(opt == "4"):
        print("Program Exited Successfully!")
    else:
        print("Invalid option selected, Program Terminated!")
  
def start():
    print("\nPress 1 to select Shortest Job First (SJF) algorithm. \nPress 2 to select Highest Response Ratio Next (HRRN) algorithm. \nPress 3 to select Shortest Remaining Time (SRT) algorithm. \nPress 4 to Exit.\n")
    algo = str(input("> Your Selected Option: "))
    while (True):
        
        if(algo == "1"):
            SJF()
            Exec_Control()
            break
        elif(algo == "2"):
            HRRN()
            Exec_Control()
            break
        elif(algo == "3"):
            SRT()
            Exec_Control()
            break
        elif(algo == "4"):
            print("Program Exited Successfully!")
            break
        else:
            print("Invalid option selected, Program Terminated!")
            break
            
if __name__ == "__main__":
   start() 