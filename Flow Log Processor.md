# Flow Log Processor

## Author
Navya Swetha Daggubati

## Date
October 10, 2024

## Overview
Welcome to the Flow Log Processor!
This Python script simplifies the process of analyzing flow log data by mapping destination ports and protocols to meaningful tags. With it, we can quickly break down our logs and get clear insights into the frequency of different tags and port/protocol combinations.

## What It Does
The Flow Log Processor reads two files: a lookup table and a flow log file. The lookup table contains the tags associated with different port and protocol combinations, while the flow log file contains your actual flow log data. The script processes these files, counts how often each tag appears, and generates a CSV output with the results.

## Getting Started
Here’s how to get everything set up and running:

1. **Prepare Your Files**:
   - **Lookup Table (`lookup.csv`)**: Create a CSV file with columns for `dstport`, `protocol`, and `tag`. Fill it with the appropriate mappings based on our needs.
   - **Flow Logs (`flow_logs.txt`)**: This file should contain flow log entries. Each line represents a log entry with relevant information.

2. **Run the Script**:
   - Make sure of having Python 3.x installed on your machine.
   - Place both `lookup.csv` and `flow_logs.txt` in the same folder as the script.
   - Open your command line or terminal, navigate to the folder where your script is located, and run the following command:
     ```bash
     python flow.py
     ```

3. **Check out the Results**:
   - After the script finishes running, you’ll find an output file called `output.csv` in the same directory. This file will contain the counts of each tag and the port/protocol combinations, making it easy for analysis.

