#!/bin/python3

from subprocess import check_output
from statistics import mean, stdev 
import matplotlib.pyplot as plotter
from os.path import join as pjoin
from os import mkdir
import argparse

def analyze_perf_script(ignore, tracepoints, data, delay):
	lines = data.strip().split("\n")

	values = []
	deviations = []
	pcnt = []
	ignored = 0
	for i in range(len(lines)):
		time_, event_ = lines[i].split()
		time_, event_ = float(time_[:-1].replace(" ", "")), event_[:-1].replace(" ", "")
		if event_ in ignore:
			ignored += 1
			continue
		time_ = round(time_ * 1000, 4)
		values.append(time_)
		deviations.append(time_ - delay)
		pcnt.append(((time_ - delay)/delay) * 100)
	
	return values, ignored, deviations, pcnt
	
if __name__ == "__main__":
	parser =  argparse.ArgumentParser(description="Script for reading, analysis and displaying Perf script data (2023) Mateusz Ferenc")
	parser.add_argument("-i", "--ignore", type=str, help="List of tracepoints, separated by space, to ignore [ format: probe_<file-name>:<tracepoint-name> ]")
	parser.add_argument("-t", "--tracepoints", type=str, help="List of tracepoints, separated by space, to track [ format: probe_<file-name>:<tracepoint-name> ]")
	parser.add_argument("-f", "--file", type=str, help="File with data dumped from Perf script")
	parser.add_argument("-d", "--delay", type=int, help="Delay in ms [defined in .c file")
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
		values, ignored, deviations, pcnt = analyze_perf_script(ignore=(list(args.ignore.split(" ")) if args.ignore is not None else []), tracepoints=list(args.tracepoints.split(" ")), data=data, delay=args.delay)
		_min = round(min(values), 2)
		_max = round(max(values), 2)
		_avg = round(mean(values), 2)
		_stdev = round(stdev(values), 3)
		tracepoints = len(values)
		
		line = f"Tracepoints: {tracepoints}\nIgnored tracepoints: {ignored}"
		print(line)
		stdout_data += line + '\n'
		line = f"Execution time:\n\tMinumum: {_min} ms\n\tMaximum: {_max} ms\n\tAverage: {_avg} ms\n\tStandard deviation: {_stdev} ms"
		print(line)
		stdout_data += line + '\n'
		
		plotter.plot(values, color='r', label='funcB')
		plotter.xlabel('tracepoint no.', weight='light', style='italic')
		plotter.ylabel('time [ms]', weight='light', style='italic')
		plotter.title(f"funcB exectution time", weight='bold')
		plotter.grid('on', linestyle=':', linewidth=0.5)
		plotter.axhline(y=_max, color='k', linestyle='--', label=f"max = {_max}")
		plotter.axhline(y=_min, color='k', linestyle='--', label=f"min = {_min}")
		plotter.axhline(y=args.delay, color='g', linestyle='-', label=f"delay = {args.delay}")
		plotter.axhline(y=_avg, color='y', linestyle='--', label=f"average = {_avg}")
		plotter.legend()
	
		file_name = f"funcB_diff_plot.png"
		save_path = pjoin(dir, file_name) if results_dir is not None else file_name

		try:
			plotter.savefig(save_path, dpi=500)
		except FileExistsError:
			pass
			
		_min = round(min(deviations), 4)
		_max = round(max(deviations), 4)
		_avg = round(mean(deviations), 4)
		line = f"Deviations time:\n\tMinumum: {_min} ms\n\tMaximum: {_max} ms\n\tAverage: {_avg} ms"
		print(line)
		stdout_data += line + '\n'
			
		plotter.clf()
		plotter.close(None)
		
		plotter.plot(pcnt, color='b', label='deviation')
		plotter.xlabel('tracepoint no.', weight='light', style='italic')
		plotter.ylabel('deviation [%]', weight='light', style='italic')
		plotter.title(f"deviation %", weight='bold')
		plotter.legend()
		plotter.grid('on', linestyle=':', linewidth=0.5)
		
		file_name = f"funcB_percent_deviations_plot.png"
		save_path = pjoin(dir, file_name) if results_dir is not None else file_name

		try:
			plotter.savefig(save_path, dpi=500)
		except FileExistsError:
			pass
			
		plotter.clf()
		plotter.close(None)
		
		save_path = pjoin(dir, "pps_stdout.txt") if results_dir is not None else "stdout.txt"
		with open(save_path, "w") as stdout_write:
			stdout_write.write(stdout_data.replace(r'\n', '\n'))
	
	else:
		print("Error:\nNo tracepoints to analyze.\t\t Aborting...")
