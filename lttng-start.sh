#!/bin/bash

bin=$1

ffPs=$(ps -efT | grep $bin | awk '{print $3}' | sed -z 's/\n/,/g')

echo $ffPs

lttng create $bin-session --output=./ff-trace

# sched_switch is emitted only for runnable threads runnable -> running
# Sched_wakeup emitted when a thread goes from sleeping to runnable
#lttng enable-event --kernel sched_switch,sched_process_fork,sched_wakeup,sched_wakeup_new,sched_migrate_task
lttng enable-event --kernel sched_*

lttng track --kernel --pid=$ffPs

lttng start

read -n 1 -p 'Run the application under test. After completing running, press any key to continue' input

lttng stop

lttng destroy

babeltrace ./ff-trace > ff-trace-human.txt
python3 runtimeagg.py ./ff-trace/kernel/ $ffPs

