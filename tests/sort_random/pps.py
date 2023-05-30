#! ../../venv/bin/python3

from subprocess import check_output
from statistics import mean, stdev 
#import matplotlib.pyplot as plotter
from os.path import join as pjoin
from os import mkdir
import argparse
from numpy import savetxt

def analyze_perf_script(ignore, timed, tracepoints, data):
	lines = data.strip().split("\n")

	other = {}
	for t in tracepoints:
		other[t] = []
	
	values = []
	ignored = 0
	for i in range(len(lines)):
		line = lines[i].split()
		time_, line_4, line_5 = float(line[3][:-1].strip()), line[4][:-1].strip(), line[5][:-1].strip()
		if line_4 in ignore or line_5 in ignore:
			ignored += 1
			continue
		if line_5 in tracepoints:
			other[line_5].append(int(line_4))
		elif line_4 in timed:
			time_ = round(time_ * 1000, 4)
			values.append(time_)
	
	return values, ignore, other
	
if __name__ == "__main__":
	parser =  argparse.ArgumentParser(description="Script for reading, analysis and displaying Perf script data (2023) Mateusz Ferenc")
	parser.add_argument("-i", "--ignore", type=str, help="List of tracepoints, separated by space, to ignore [ format: probe_<file-name>:<tracepoint-name> ]")
	parser.add_argument("-c", "--timed", type=str, help="List of tracepoints with time diff [ format: probe_<file-name>:<tracepoint-name> ]")
	parser.add_argument("-t", "--tracepoints", type=str, help="List of tracepoints, separated by space, to track [ format: probe_<file-name>:<tracepoint-name> ]")
	parser.add_argument("-f", "--file", type=str, help="File with data dumped from Perf script")
	parser.add_argument("-s", "--stress", type=str, help="Append \"stress\" [true] or \"no_stress\" [false] before directory name")
	parser.add_argument("--date", type=str, help="Date")
	args = parser.parse_args()
	data = None
	stdout_data = ""
	if args.tracepoints is not None and args.file is not None:
		results_dir = "results"
	
		try:
			mkdir(results_dir)
		except FileExistsError:
			pass
			
		now_time = args.date
		stress = "no_stress" if args.stress.lower() == "false" else "stress"
		dir = pjoin(results_dir, f"{stress}_{now_time}")
		
		try:
			mkdir(dir)
		except FileExistsError:
			pass
			
		with open(args.file, "r") as file_data:
			data = file_data.read()
		values, ignored, other = analyze_perf_script(ignore=(list(args.ignore.split(" ")) if args.ignore is not None else []), timed=list(args.timed.split(" ")), tracepoints=list(args.tracepoints.split(" ")), data=data)
		_min = round(min(values), 2)
		_max = round(max(values), 2)
		_avg = round(mean(values), 2)
		_stdev = round(stdev(values), 3)
		tracepoints = len(values)
		o_0 = list(args.tracepoints.split(" "))[0]
		ref_cycles_len = len(other[o_0])
		o_1 = list(args.tracepoints.split(" "))[1]
		cpu_cycles_len = len(other[o_1])
		line = f"Ignored tracepoints: {args.ignore}\nTimed tracepoints: {args.timed}\nMeasured tracepoints: {args.tracepoints}\nMeasured \"{args.timed}\": {tracepoints}"
		for t in other.keys():
			line += f"\nMeasured \"{t}\": {len(other[t])}"
		print(line)
		stdout_data += line + '\n'
		line = f"Execution time:\n\tMinumum: {_min} ms\n\tMaximum: {_max} ms\n\tAverage: {_avg} ms\n\tStandard deviation: {_stdev} ms"
		print(line)
		stdout_data += line + '\n'
		
		"""plotter.plot(values, color='r', label='funcB')
		plotter.xlabel('tracepoint no.', weight='light', style='italic')
		plotter.ylabel('time [ms]', weight='light', style='italic')
		plotter.title(f"funcB exectution time", weight='bold')
		plotter.grid('on', linestyle=':', linewidth=0.5)
		plotter.axhline(y=_max, color='k', linestyle='--', label=f"max = {_max}")
		plotter.axhline(y=_min, color='k', linestyle='--', label=f"min = {_min}")
		plotter.axhline(y=_avg, color='y', linestyle='--', label=f"average = {_avg}")
		plotter.legend()
	
		file_name = f"funcB_diff_plot.png"
		save_path = pjoin(dir, file_name) if results_dir is not None else file_name

		try:
			plotter.savefig(save_path, dpi=500)
		except FileExistsError:
			pass
		
		plotter.clf()	
		plotter.close(None)"""
		
		_min = round(min(other[o_0]), 0)
		_max = round(max(other[o_0]), 0)
		_avg = round(mean(other[o_0]), 0)
		_stdev = round(stdev(other[o_0]), 0)
		line = f"ref-cycles:\n\tMinumum: {_min}\n\tMaximum: {_max}\n\tAverage: {_avg}\n\tStandard deviation: {_stdev}"
		print(line)
		stdout_data += line + '\n'
		
		_min = round(min(other[o_1]), 0)
		_max = round(max(other[o_1]), 0)
		_avg = round(mean(other[o_1]), 0)
		_stdev = round(stdev(other[o_1]), 0)
		line = f"cpu-cycles:\n\tMinumum: {_min}\n\tMaximum: {_max}\n\tAverage: {_avg}\n\tStandard deviation: {_stdev}"
		print(line)
		stdout_data += line + '\n'
		
		"""plotter.plot(other[o_0], color='g', label='ref-cycles')
		plotter.plot(other[o_1], color='r', label='cpu-cycles')
		plotter.xlabel('tracepoint no.', weight='light', style='italic')
		plotter.ylabel('cycles [n]', weight='light', style='italic')
		plotter.title(f"funcB cycles", weight='bold')
		plotter.grid('on', linestyle=':', linewidth=0.5)
		plotter.legend()
	
		file_name = f"funcB_cycles_plot.png"
		save_path = pjoin(dir, file_name) if results_dir is not None else file_name

		try:
			plotter.savefig(save_path, dpi=500)
		except FileExistsError:
			pass
		
		plotter.clf()	
		plotter.close(None)"""
		
		save_path = pjoin(dir, "funcB_time.csv") if results_dir is not None else "funcB_time.csv"
		savetxt(save_path, values, delimiter=",")
		
		save_path = pjoin(dir, "funcB_ref_cycles.csv") if results_dir is not None else "funcB_ref_cycles.csv"
		savetxt(save_path, other[o_0], delimiter=",")
		
		save_path = pjoin(dir, "funcB_cpu_cycles.csv") if results_dir is not None else "funcB_cpu_cycles.csv"
		savetxt(save_path, other[o_1], delimiter=",")
		
		save_path = pjoin(dir, "pps_stdout.txt") if results_dir is not None else "stdout.txt"
		with open(save_path, "w") as stdout_write:
			stdout_write.write(stdout_data.replace(r'\n', '\n'))
	
	else:
		print("Error:\nNo tracepoints to analyze.\t\t Aborting...")
