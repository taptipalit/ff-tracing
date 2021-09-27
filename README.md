# ff-tracing

**1. Install Lttng**

LTTNg is a kernel (and userspace, but we don't care about that part now) tracing framework that uses tracepoints. It outputs logs in the [CTF trace format](https://diamon.org/ctf/). Babeltrace is a parser for that format, and it also has python bindings which this project uses to report interesting statistics.

`sudo apt install lttng-tools lttng-modules-dkms babeltrace python3-babeltrace`
  
**2. Install TraceCompass (optional)**

TraceCompas is a CTF trace visualization tool. It's sometimes useful to get a bigger picture of what's going on. 

It needs Java 11 and is very particular about it. Download it from [here](https://www.oracle.com/java/technologies/javase/jdk11-archive-downloads.html).

**3. Launch Firefox**

The script `lttng-start.sh` requires the target application to be launched and in "waiting" state. So just launch firefox, but don't open any websites yet.

**4. Start the tracing**

(Run all of these as root)

- Run `./lttng-start.sh firefox` to first start the tracing session. This script will automatically initialize a tracing session to track the scheduler related trace events for all processes with the name "firefox" _and_ it's children.

- Wait until you get the following output on the terminal:
`Run the application under test. After completing running, press any key to continue`

- Now, in firefox open the website you want to benchmark (enter it's address in the address-bar). Wait for the website to load fully.

- Once it has finished loading, come back to the terminal and hit enter. This should end the tracing session and print the statistics about how many times any of the Firefox processes/threads were switched out and how much time the CPU spent executing Firefox processes and threads. We can add other interesting statistics later.

- The CTF log is also dumped in a human readable format as `ff-trace-human.txt`

