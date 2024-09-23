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

 **Clone or Download the Repository**:
   - Clone the repository from GitHub or download the source files.
   
   ```bash
   git clone https://github.com/JoseSanchez7/flow-log-parser.git
   cd flow-log-parser

## Output:

The program generates an output file named `output.txt`, which contains the results of the flow log processing. This file is located in the same directory as the script.

---

## Testing and Analysis

### Testing Performed:

- **Valid Flow Logs**:  
   The program was tested with flow logs containing various destination ports and protocols (TCP, UDP, ICMP) to ensure proper matching and counting of tags.

- **Malformed Flow Logs**:  
   Lines with fewer than 8 fields were tested to ensure they are properly skipped, and the count of malformed lines is correctly reported in the output.

- **Multiple Tags per Port/Protocol**:  
   The lookup table was tested with multiple tags assigned to the same port and protocol combination. The program correctly counted each tag when the matching port/protocol combination appeared in the flow logs.

- **Case Insensitive Matching**:  
   Flow logs and lookup table entries with varying cases (e.g., `TCP` vs `tcp`) were tested to ensure the program handled case insensitivity correctly, matching regardless of the case used.

- **Large Files**:  
   The program was tested with a flow log file of 10 MB in size and a lookup table containing 10,000 entries to confirm it could process large amounts of data efficiently without exceeding memory limits.

### Analysis:

- **Efficiency**:  
   The program processes the flow logs line by line, making it scalable for large files. Memory usage is kept minimal since only the lookup table is stored in memory as a dictionary, allowing efficient lookups (average O(1) complexity).

- **Error Handling**:  
   The program gracefully handles malformed flow log lines, skipping them and providing a count of how many lines were skipped. This ensures robustness when working with potentially messy log files.

- **Extensibility**:  
   The program is easily extendable. If additional protocols need to be supported or if more complex tag mappings are required, the lookup structure and logic can be adjusted without major changes to the overall design.

---

## Notes on Edge Cases

- **Unknown Protocols**:  
   Any protocol number not supported by the program (i.e., not `tcp`, `udp`, or `icmp`) is categorized as `"unknown"`. These logs will not be tagged unless a specific lookup table entry exists for `"unknown"` protocols.

- **Custom Flow Log Formats**:  
   This program assumes that the flow logs follow AWS’s default format. Custom formats are not supported and may result in skipped lines.

