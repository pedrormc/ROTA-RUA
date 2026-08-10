import json, glob, os, csv

raws = glob.glob("C:/Users/teste/.opencode/state/*") + glob.glob("C:/Users/teste/AppData/Local/Temp/**/*.json") # or parse serpapi output from memory
# Since serpapi results are in the previous tool output, let's write a python script to process and output the CSV directly.
print("Processing leads...")
