from collections import defaultdict

def parse_flow_log(line):
    fields = line.strip().split()
    if len(fields) < 8:
        return None  # Skip malformed lines

    protocol_map = {
        "6": "tcp",
        "17": "udp",
        "1": "icmp"
    }
    protocol = protocol_map.get(fields[7], "unknown")

    return {
        "version": int(fields[0]),
        "dstport": int(fields[5]),
        "protocol": protocol
    }

def parse_lookup_table(lookup_file):
    lookup_map = defaultdict(list)  # Store multiple tags for each key
    with open(lookup_file, "r") as file:
        next(file)  # Skip header
        for line in file:
            dstport, protocol, tag = line.strip().split(",")
            key = (int(dstport), protocol.lower())  # Ensure protocol comparison is case insensitive
            lookup_map[key].append(tag.strip().lower())  # Store tags in lowercase for case insensitivity
    return lookup_map

def process_flow_logs(flow_log_file, lookup_map):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    untagged_count = 0
    skipped_lines = 0

    with open(flow_log_file, "r") as file:
        for line in file:
            if not line.strip():
                continue

            flow_data = parse_flow_log(line)
            if flow_data is None or flow_data["version"] != 2:
                skipped_lines += 1
                continue

            key = (flow_data["dstport"], flow_data["protocol"])

            if key in lookup_map:
                tags = lookup_map[key]
                for tag in tags:
                    tag_counts[tag] += 1
            else:
                untagged_count += 1

            port_protocol_counts[key] += 1

    return tag_counts, port_protocol_counts, untagged_count, skipped_lines

def write_output(tag_counts, port_protocol_counts, untagged_count, skipped_lines, output_file):
    with open(output_file, "w") as file:
        # Write tag counts
        file.write("Tag Counts:\nTag,Count\n")
        for tag, count in sorted(tag_counts.items()):
            file.write(f"{tag},{count}\n")

        # Write port/protocol combination counts
        file.write("\nPort/Protocol Combination Counts:\nPort,Protocol,Count\n")
        for (port, protocol), count in sorted(port_protocol_counts.items()):
            file.write(f"{port},{protocol},{count}\n")

        # Write untagged logs count
        file.write(f"\nUntagged: {untagged_count}\n")

        # Write skipped/malformed lines count
        file.write(f"Skipped (malformed) lines: {skipped_lines}\n")

def main():
    flow_log_file = "flow_logs.txt"
    lookup_table_file = "lookup.csv"
    output_file = "output.txt"

    lookup_map = parse_lookup_table(lookup_table_file)
    tag_counts, port_protocol_counts, untagged_count, skipped_lines = process_flow_logs(flow_log_file, lookup_map)
    write_output(tag_counts, port_protocol_counts, untagged_count, skipped_lines, output_file)

if __name__ == "__main__":
    main()









