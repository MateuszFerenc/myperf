# Tests of Perf tool behaviour



My repository of tests of Perf tool in UNIX (Linux) to measure time and cycles of executed code.



### results directory tree
<pre>
results_all/   
├── decreased_system_run    
│   ├── no_stress   
│   │   ├── sort_decreasing  
│   │   ├── sort_random   
│   │   └── test_delay   
│   └── stress   
│       ├── sort_decreasing   
│       ├── sort_random   
│       └── test_delay   
└── normal_run   
    ├── no_stress   
    │   ├── sort_decreasing   
    │   ├── sort_random   
    │   └── test_delay   
    └── stress   
        ├── sort_decreasing   
        ├── sort_random   
        └── test_delay   
</pre>

### Using Perf

<p>
Install Perf using: <br>
<b>sudo apt install linux-tools-`uname -r`</b><br><br>
edit sysctf.conf file and add line kernel... to enable system profiling <br>
<b><i>nano /etc/sysctl.conf </i></b><br>
<b>kernel.perf_event_paranoid = -1</b>

<br>

Create .c file and compile it using <b>gcc</b>: <br>
<b><i>gcc -g -o \<output-file-name\> \<file-name\></i></b> <br>
<i>"-g" flag used to produce debugging information in the operating system's native format</i>

<br>

now as root: <br>
<b>I.</b> create software event for entering function <b>perf probe --exec compiled-file 'function_name'</b> <br>
<i>Perf probe tracepoint naming convention prefix "probe_", executable name plus ":" and function name <br>i.e.: probe_test:functionB</i>
        
<b>II.</b> create software event for exiting function <b>perf probe --exec compiled-file 'function_name%return'</b>
<i>Perf probe tracepoint naming convention prefix "probe_", executable name plus ":" and function name and suffix "__return" <br>i.e.: probe_test:functionB__return</i>
<br>

<b>III.</b> Now you are able to measure tracepoints. <br>
Use:<br>
<pre>
1. sudo perf record --event your_event --event your_event_ret executable
2. sudo perf record --event your_event --event "{your_event_ret,cycles:u}:S" executable
</pre>
<br>
1. Use if you want to measure only time difference between tracepoints <br>
2. Use if you want to measure time difference between tracepoints and also amount of cycles between first and second tracepoint (i.e. second event causes to read cycles counter) <br><br>

<b>IV. </b> Now you can read Perf measurements <br>
<b>sudo perf script --ns --deltatime > file_name</b>
<br>

<b>V. </b> In the final step, you can run pps.py script to analyze and plot data. <br>
<pre><b>./pps.py --ignore="ignored_tracepoints" --tracepoints="wanted_tracepoints" --file file_name_fro_perf_script --stress true_or_false --date date_time</b></pre>
<br>

Example run:
<pre>
sudo perf probe --exec sort_decreasing 'funcB'
sudo perf probe --exec sort_decreasing 'funcB%return'

sudo perf record --event probe_sort_decreasing:funcB --event "{probe_sort_decreasing:funcB__return,cycles:U}:S" sort_decreasing

sudo perf script --ns --deltatime > perf_test

source venv/bin/activate
./pps.py --ignore="probe_sort_decreasing:funcB" --tracepoints="probe_sort_decreasing:funcB__return, cycles:U" --file perf_test --stress false --date 121212_010101

sudo perf probe --del probe_sort_decreasing:funcB --quiet
sudo perf probe --del probe_sort_decreasing:funcB__return --quiet
</pre>

<br><br>
Also you should install stress tool (tool to impose load on and stress test a computer system) <br>
<b>sudo apt install stress</b> <br><br>
Show potential probe-able functions. <br>
<b>perf probe --exec executable_name --funcs</b> <br><br>
Show source code lines. <br>
<b>perf probe --exec executable_name --line function_name</b> <br><br>
If command perf probe was used with "-\-force" switch then each new probe (of the same name) will have suffix of "_x", where x is number.

</p>

### Running tests

<p>
Run all tests by using:
<pre>
sudo ./run_all --system [true|false] 
</pre>
Run command below, to get help:
<pre>
./run_all -h
</pre>

<pre>
Flags description:

-s, --system (bool) : Required, takes boolean value.
	True: Run with decreased system stats in BIOS:
		> <b>SpeedStep disabled</b> - CPU frequency multiplier change disabled
		> <b>HyperThreading disabled</b> - CPU virtual cores disabled, only phisical cores
		> <b>TurboBoost disabled</b> - CPU turbo (Max) frequency disabled
		
		Also for better performance (kernel configuration):
		> Change CPU governor to performance, to lock CPU frequency in constant (high) value, using:
			<b>sudo cpupower frequency-set --governor performance</b>
		> Force tests to run on single core only (no context switching) using flag: 
			<b>-f or --force-single-core</b>
	False: Run with normal system stats (No options disabled in BIOS)
		
-q, --quiet : Optional, default all output will be displayed.
	Disable output from test scripts.
	
-c, --comment (text) : Optional, default no comment.txt file generated.
	Create comment.txt file in results dir, with informations about how script been called, and comment itself
	
-f, --force-single-core : Optional, default permit context switching.
	Force tests to run on single core, which disables context switching between other CPU which positively affects measurements (less noise)
	
</pre>

</p>