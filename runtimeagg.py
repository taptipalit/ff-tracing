import babeltrace
import sys

# get the trace path from the first command line argument
trace_path = sys.argv[1]

ff_tid_str = sys.argv[2]

RUNNING = 1
NOTRUNNING = 0


ffTidsList = ff_tid_str.split(',')

ffTids = set()

for ffTidStr in ffTidsList:
    try:
        ffTids.add(int(ffTidStr))
    except:
        pass

trace_collection = babeltrace.TraceCollection()

trace_collection.add_trace(trace_path, 'ctf')

print("At start, ffTids = ", ffTids, "len = ", len(ffTids))

# Track all childred of ff_pid
for event in trace_collection.events:
	if (event.name == "sched_process_fork"):
            if event['parent_tid'] in ffTids:
                ffTids.add(event['child_tid'])

print("After running, ffTids = ", ffTids, "len = ", len(ffTids))

perCpuEvents = {}
	
# All timestamps are in nanoseconds
startTime = trace_collection.timestamp_begin
endTime = trace_collection.timestamp_end

print("Startime: ", startTime)

# How many times were we switched out
numSchedOut = 0

# How much time in nanoseconds were we executing
actualRuntime = 0

for event in trace_collection.events: 
        #print(event.name, event['cpu_id'])
        timestamp = event.timestamp;
        if event.name == "sched_switch" and (event['prev_tid'] in ffTids or event['next_tid'] in ffTids):
            if event['next_tid'] not in ffTids:
                numSchedOut = numSchedOut + 1
        if event.name == "sched_stat_runtime" and event['tid'] in ffTids:
            actualRuntime = actualRuntime + event['runtime']

print("Number of times we were scheduled out: ", numSchedOut)
print("Actual Runtime (in ms): ", actualRuntime/1000/1000)
print("Total time (in ms): ", (endTime - startTime)/1000/1000)
