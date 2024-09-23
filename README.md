# Flow Log Parsing Program

## Project Overview

This program reads AWS VPC flow logs and tags each log entry based on its destination port and protocol. It uses a lookup table to match `(dstport, protocol)` combinations to tags, then generates a summary report that includes:
- The number of occurrences of each tag.
- How often each port/protocol combination appears.
- The number of flow logs that couldn't be matched to any tag (untagged).
- The number of skipped or malformed flow log lines.

This program is designed to handle:
- Flow log files up to **10 MB** in size.
- Lookup tables with up to **10,000** mappings.
- Multiple tags for a single port/protocol combination.
- Case-insensitive matching for both protocols and tags.

---

## Assumptions

1. **Flow Log Format**:
   - The program only supports **version 2** of AWS VPC flow logs, based on the structure documented in [AWS Flow Logs Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html).
   - Only flow logs in the **default format** are supported.
   - Lines with fewer than 8 fields are treated as **malformed** and skipped.

2. **Lookup Table**:
   - The lookup table is a CSV file with three columns: `dstport, protocol, tag`.
   - Each port/protocol combination can map to multiple tags.
   - The lookup table uses lowercase protocols (`tcp`, `udp`, `icmp`), but matching is case-insensitive.

3. **Case Insensitivity**:
   - Both protocol matching and tag lookup are case-insensitive. Tags are stored and counted in lowercase to avoid any mismatches.

4. **Performance**:
   - The program reads the flow logs **line by line**, making it memory efficient and capable of handling large files up to 10 MB.
   - The lookup table is stored in memory using a dictionary, which efficiently handles up to 10,000 mappings.

---

## How to Run the Program

### Requirements
- **Python 3.x**: No external libraries or dependencies are required. The program uses built-in Python modules, so it can be run directly on any system with Python installed.

### Steps to Run

1. **Clone or Download the Repository**:
   - Clone the repository from GitHub or download the source files.
   
   ```bash
   git clone https://github.com/JoseSanchez7/flow-log-parser.git
   cd flow-log-parser
