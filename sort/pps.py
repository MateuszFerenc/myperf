#!/bin/python3

from subprocess import check_output
from statistics import mean, stdev 
import matplotlib.pyplot as plotter
from datetime import datetime
from os.path import join as pjoin
from os import mkdir
import argparse

def analyze_perf_script(ignore, tracepoints, data):
	lines = data.strip().split("\n")

	values = []
	ignored = 0
	for i in range(len(lines)):
		time_, event_ = lines[i].split()
		time_, event_ = float(time_[:-1].replace(" ", "")), event_[:-1].replace(" ", "")
		if event_ in ignore:
			ignored += 1
			continue
		time_ = round(time_ * 1000, 4)
		values.append(time_)
	
	return values, ignore
	
if __name__ == "__main__":
	parser =  argparse.ArgumentParser(description="Script for reading, analysis and displaying Perf script data (2023) Mateusz Ferenc")
	parser.add_argument("-i", "--ignore", type=str, help="List of tracepoints, separated by space, to ignore [ format: probe_<file-name>:<tracepoint-name> ]")
	parser.add_argument("-t", "--tracepoints", type=str, help="List of tracepoints, separated by space, to track [ format: probe_<file-name>:<tracepoint-name> ]")
	parser.add_argument("-f", "--file", type=str, help="File with data dumped from Perf script")
	args = parser.parse_args()
	data = None
	if args.tracepoints is not None and args.file is not None:
		results_dir = "results"
	
		try:
			mkdir(results_dir)
		except FileExistsError:
			pass
			
		with open(args.file, "r") as file_data:
			data = file_data.read()
		values, ignored = analyze_perf_script(ignore=(list(args.ignore.split(" ")) if args.ignore is not None else []), tracepoints=list(args.tracepoints.split(" ")), data=data)
		_min = round(min(values), 2)
		_max = round(max(values), 2)
		_avg = round(mean(values), 2)
		_stdev = round(stdev(values), 3)
		tracepoints = len(values)
		
		print(f"Tracepoints: {tracepoints}\nIgnored tracepoints: {ignored}")
		print(f"Execution time:\n\tMinumum: {_min} ms\n\tMaximum: {_max} ms\n\tAverage: {_avg} ms\n\tStandard deviation: {_stdev} ms")
		
		plotter.plot(values, color='r', label='funcB')
		#plotter.xticks(range(0, tracepoints))
		plotter.xlabel('tracepoint no.', weight='light', style='italic')
		plotter.ylabel('time [ms]', weight='light', style='italic')
		plotter.title(f"funcB exectution time", weight='bold')
		plotter.grid('on', linestyle=':', linewidth=0.5)
		plotter.axhline(y=_max, color='k', linestyle='--', label=f"max = {_max}")
		plotter.axhline(y=_min, color='k', linestyle='--', label=f"min = {_min}")
		#plotter.axhline(y=args.delay, color='g', linestyle='-', label=f"delay = {args.delay}")
		plotter.axhline(y=_avg, color='y', linestyle='--', label=f"average = {_avg}")
		#d = [args.delay] * tracepoints
		#plotter.plot(d, color='g', label="delay")
		plotter.legend()
		#plotter.ticklabel_format(useOffset=False, style='plain')
		#plotter.ylim(_min - (_stdev * (_avg // args.delay)), _max + (_stdev * (_avg // args.delay)))
	
		now_time = datetime.now()
		dir = pjoin(results_dir, now_time.strftime('%H%M%S_%d%m%y'))
		
		try:
			mkdir(dir)
		except FileExistsError:
			pass
	
		file_name = f"funcB_diff_plot_{now_time.strftime('%H%M%S_%d%m%y')}.png"
		save_path = pjoin(dir, file_name) if results_dir is not None else file_name

		try:
			plotter.savefig(save_path, dpi=500)
		except FileExistsError:
			pass
		
		plotter.clf()	
		plotter.close(None)
	
	else:
		print("Error:\nNo tracepoints to analyze.\t\t Aborting...")
