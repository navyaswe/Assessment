# Author: Navya Swetha Daggubati
# Date: October 10, 2024
# Program Description: 
# This program processes flow log data and maps destination ports and protocols to specific tags.
# It reads from a lookup table and counts occurrences of each tag as well as the combinations
# of ports and protocols. Finally, it outputs these counts to a output CSV file for further analysis.

import csv
from collections import defaultdict


def parse_lookup_table(lookup_file):
    """
    Reads the lookup table CSV file and returns a mapping of destination ports and protocols to tags.

    Args:
        lookup_file (str): The filename of the lookup table.

    Returns:
        dict: A dictionary where keys are tuples of (destination_port, protocol) and values are the corresponding tags.
    """
    lookup = {}
    with open(lookup_file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create a unique key using destination port and protocol (in lowercase)
            key = (row['dstport'], row['protocol'].lower())
            lookup[key] = row['tag']
    return lookup

def parse_flow_logs(flow_file, lookup):
    """
    Processes the flow logs to count tags and port/protocol combinations.

    Args:
        flow_file (str): The filename of the flow log file.
        lookup (dict): A dictionary mapping (destination_port, protocol) to their tags.

    Returns:
        tuple: A tuple containing:
            - dict: Counts of each tag found in the logs.
            - dict: Counts of each (port, protocol) combination.
            - int: Total count of untagged entries.
    """
    tag_counts = defaultdict(int)  # Using defaultdict to automatically initialize counts to zero
    port_protocol_counts = defaultdict(int)  # For counting port/protocol combinations
    untagged_count = 0  # Counter for untagged entries

    # Map of valid protocols; currently only TCP (protocol 6) is included
    protocol_map = {'6': 'tcp'}  # You can add more protocols if needed

    # Set of valid ports to filter out unwanted entries
    valid_ports = {'22', '23', '25', '80', '110', '143', '443', '993', '1024', '49158'}

    with open(flow_file, mode='r') as f:
        for line in f:
            parts = line.strip().split()  # Split the line into parts

            # Skip lines that do not have enough data
            if len(parts) < 13:
                continue

            # Extract the destination port and protocol number
            dstport = parts[5]
            protocol_num = parts[7]
            protocol = protocol_map.get(protocol_num)  # Lookup the protocol

            # Debugging output to track the line being processed
            print(f"Processing Line: {line.strip()}")
            print(f"Destination Port: {dstport}, Protocol: {protocol}")

            # Check for invalid ports or unsupported protocols
            if protocol is None or dstport not in valid_ports:
                print("Counted as Untagged")  # Inform that this entry is untagged
                untagged_count += 1
                continue

            # Attempt to get the tag from the lookup table
            tag = lookup.get((dstport, protocol), "Untagged")

            # Increment the count for the found tag
            if tag != "Untagged":
                tag_counts[tag] += 1
            else:
                print(f"No tag found for Port: {dstport}, Protocol: {protocol}")  # Notify when no tag is found
                untagged_count += 1  # Count this as untagged

            # Count occurrences of this port/protocol combination
            port_protocol_counts[(dstport, protocol)] += 1

    return tag_counts, port_protocol_counts, untagged_count

def write_output(tag_counts, port_protocol_counts, untagged_count, output_file):
    """
    Writes the counts of tags and port/protocol combinations to an output CSV file.

    Args:
        tag_counts (dict): Counts of each tag from the flow logs.
        port_protocol_counts (dict): Counts of each (port, protocol) combination.
        untagged_count (int): Total count of entries without tags.
        output_file (str): The filename for the output CSV file.
    """
    with open(output_file, mode='w', newline='') as f:
        writer = csv.writer(f)

        # Write the tag counts section
        writer.writerow(["Tag Counts:"])
        writer.writerow(["Tag", "Count"])  # Header for tag counts
        for tag, count in tag_counts.items():
            writer.writerow([tag, count])  # Write each tag and its count
        writer.writerow(["Untagged", untagged_count])  # Total untagged count

        writer.writerow([])  # Add a blank line for separation

        # Write the port/protocol counts section
        writer.writerow(["Port/Protocol Combination Counts:"])
        writer.writerow(["Port", "Protocol", "Count"])  # Header for port/protocol counts
        for (dstport, protocol), count in port_protocol_counts.items():
            writer.writerow([dstport, protocol, count])  # Write each port/protocol and its count

def main():
    """
    It coordinates reading the lookup table, processing the flow logs, and writing results to a file.
    """
    lookup_file = 'lookup.csv'  
    flow_log_file = 'flow_logs.txt'  
    output_file = 'output.csv'  

    # Parse the lookup table
    lookup = parse_lookup_table(lookup_file)
    # Process the flow logs
    tag_counts, port_protocol_counts, untagged_count = parse_flow_logs(flow_log_file, lookup)
    # Write the results to an output file
    write_output(tag_counts, port_protocol_counts, untagged_count, output_file)

    print(f"Results written to {output_file}")  # Confirmation message

if __name__ == '__main__':
    main() 
