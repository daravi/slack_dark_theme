#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
from sys import platform
import os
import pathlib
import subprocess

def kill_process(process_name):
	for proc in psutil.process_iter():
		# check whether the process name matches
		if proc.name() == process_name:
			proc.kill()

def append_to_file(file_path, patch_path):
	if not pathlib.Path(file_path).is_file():
		print("Could not locate the files to be patched!")
		return
	
	with open(file_path, "r") as js_file:
		lines = js_file.read().splitlines()
		if lines[-1] == "// PATCH ADDED BY slack_dark_theme.py":
			print("File already patched! Exiting...")

	with open(file_path, "a") as js_file:
		with open(patch_path, "r") as patch:
			js_file.write(patch.read())

if __name__ == "__main__":
	kill_process("slack")

	path = ""
	if platform == "linux" or platform == "linux2":
		path = os.path.join("/", "usr", "lib", "slack")
	elif platform == "darwin":
		path = os.path.join("/", "Applications", "Slack.app", "Contents")		
	elif platform == "win32":
		path = os.path.expanduser("~")
		path = os.path.join(path, "AppData", "Local", "slack")
	path = os.path.join(path, "resources", "app.asar.unpacked", "src", "static")

	append_to_file(os.path.join(path, "index.js"), "patch.js")
	append_to_file(os.path.join(path, "ssb-interop.js"), "patch.js")

	print("Successfully patched both index.js and ssb-interop.js!")
	
	# if platform == "linux" or platform == "linux2":
	# 	subprocess.call([os.path.join("/", "usr", "lib", "slack", "slack")])