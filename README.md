# Flow Log Parsing Program

## Project Overview

<p>This program reads AWS VPC flow logs and tags each log entry based on its destination port and protocol. It uses a lookup table to match <code>(dstport, protocol)</code> combinations to tags, then generates a summary report that includes:</p>
<ul>
  <li>The number of occurrences of each tag.</li>
  <li>How often each port/protocol combination appears.</li>
  <li>The number of flow logs that couldn't be matched to any tag (untagged).</li>
  <li>The number of skipped or malformed flow log lines.</li>
</ul>

<p>This program is designed to handle:</p>
<ul>
  <li>Flow log files up to <strong>10 MB</strong> in size.</li>
  <li>Lookup tables with up to <strong>10,000</strong> mappings.</li>
  <li>Multiple tags for a single port/protocol combination.</li>
  <li>Case-insensitive matching for both protocols and tags.</li>
</ul>

<hr>

## Assumptions

<ol>
  <li><strong>Flow Log Format:</strong>
    <ul>
      <li>The program only supports <strong>version 2</strong> of AWS VPC flow logs, based on the structure documented in <a href="https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html">AWS Flow Logs Documentation</a>.</li>
      <li>Only flow logs in the <strong>default format</strong> are supported.</li>
      <li>Lines with fewer than 8 fields are treated as <strong>malformed</strong> and skipped.</li>
    </ul>
  </li>
  <li><strong>Lookup Table:</strong>
    <ul>
      <li>The lookup table is a CSV file with three columns: <code>dstport, protocol, tag</code>.</li>
      <li>Each port/protocol combination can map to multiple tags.</li>
      <li>The lookup table uses lowercase protocols (<code>tcp</code>, <code>udp</code>, <code>icmp</code>), but matching is case-insensitive.</li>
    </ul>
  </li>
  <li><strong>Case Insensitivity:</strong>
    <ul>
      <li>Both protocol matching and tag lookup are case-insensitive. Tags are stored and counted in lowercase to avoid any mismatches.</li>
    </ul>
  </li>
  <li><strong>Performance:</strong>
    <ul>
      <li>The program reads the flow logs <strong>line by line</strong>, making it memory efficient and capable of handling large files up to 10 MB.</li>
      <li>The lookup table is stored in memory using a dictionary, which efficiently handles up to 10,000 mappings.</li>
    </ul>
  </li>
</ol>

<hr>

## How to Run the Program

### Requirements
<ul>
  <li><strong>Python 3.x</strong>: No external libraries or dependencies are required. The program uses built-in Python modules, so it can be run directly on any system with Python installed.</li>
</ul>

### Steps to Run

<ol>
  <li><strong>Clone or Download the Repository:</strong>
    <ul>
      <li>Clone the repository from GitHub or download the source files:</li>
    </ul>
    <pre><code>bash
git clone https://github.com/MarkedMuichiro/Flow_Log_Parsing_Program.git
cd flow-log-parser
    </code></pre>
  </li>
  <li><strong>Prepare Input Files:</strong>
    <ul>
      <li>Ensure the following input files are present in the working directory:</li>
      <ul>
        <li><code>flow_logs.txt</code>: A plain-text file containing the flow logs (up to 10 MB).</li>
        <li><code>lookup.csv</code>: A CSV file with three columns: <code>dstport,protocol,tag</code>.</li>
      </ul>
    </ul>
  </li>
  <li><strong>Run the Program:</strong>
    <ul>
      <li>Run the program using Python from the command line:</li>
    </ul>
    <pre><code>python flow_log_parser.py
    </code></pre>
  </li>
</ol>

## Output:

<p>The program generates an output file named <code>output.txt</code>, which contains the results of the flow log processing. This file is located in the same directory as the script.</p>

<hr>

## Testing and Analysis

### Testing Performed:

<ul>
  <li><strong>Valid Flow Logs:</strong>  
    <p>The program was tested with flow logs containing various destination ports and protocols (TCP, UDP, ICMP) to ensure proper matching and counting of tags.</p>
  </li>
  <li><strong>Malformed Flow Logs:</strong>  
    <p>Lines with fewer than 8 fields were tested to ensure they are properly skipped, and the count of malformed lines is correctly reported in the output.</p>
  </li>
  <li><strong>Multiple Tags per Port/Protocol:</strong>  
    <p>The lookup table was tested with multiple tags assigned to the same port and protocol combination. The program correctly counted each tag when the matching port/protocol combination appeared in the flow logs.</p>
  </li>
  <li><strong>Case Insensitive Matching:</strong>  
    <p>Flow logs and lookup table entries with varying cases (e.g., <code>TCP</code> vs <code>tcp</code>) were tested to ensure the program handled case insensitivity correctly, matching regardless of the case used.</p>
  </li>
  <li><strong>Large Files:</strong>  
    <p>The program was tested with a flow log file of 10 MB in size and a lookup table containing 10,000 entries to confirm it could process large amounts of data efficiently without exceeding memory limits.</p>
  </li>
</ul>

### Analysis:

<ul>
  <li><strong>Efficiency:</strong>  
    <p>The program processes the flow logs line by line, making it scalable for large files. Memory usage is kept minimal since only the lookup table is stored in memory as a dictionary, allowing efficient lookups (average O(1) complexity).</p>
  </li>
  <li><strong>Error Handling:</strong>  
    <p>The program gracefully handles malformed flow log lines, skipping them and providing a count of how many lines were skipped. This ensures robustness when working with potentially messy log files.</p>
  </li>
  <li><strong>Extensibility:</strong>  
    <p>The program is easily extendable. If additional protocols need to be supported or if more complex tag mappings are required, the lookup structure and logic can
