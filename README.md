# File Integrity Monitor (FIM)

A lightweight, modular Python CLI tool designed to detect unauthorized file modifications, creations, and deletions using cryptographic SHA-256 hashing and real-time system event monitoring.

## Core Features

- **Baseline Creation (`-b`)**: Scans a target directory, calculates SHA-256 hashes using chunked streaming, and saves a "golden state" snapshot to `baseline.json`.
- **Integrity Verification (`-v`)**: Performs differential analysis between the current filesystem state and the baseline database to identify modified, newly created, or missing files.
- **Real-Time Live Monitoring (`-m`)**: Leverages the `watchdog` library to hook into operating system events (inotify / ReadDirectoryChangesW) for instant incident alerts.
- **Incident Logging**: Automatically records all detected security events with timestamps into `logs/fim_events.log`.
- **Memory Efficient**: Processes files in 64 KB chunks to ensure minimal RAM footprint, even with large files.

## Usage
The tool requires a target directory (-d / --dir) and one operational mode (-b, -v, or -m).

```python main.py --help``` - Display Help & Available Arguments
```python main.py -d ./target_folder -b``` - Create a Baseline Snapshot
```python main.py -d ./target_folder -v``` - Verify Directory Integrity On-Demand
```python main.py -d ./target_folder -m``` - Start Real-Time Monitoring (Ctrl+C to stop):
```python main.py -d ./target_folder -b -db custom_baseline.json``` - Use a Custom Baseline Database File

# Acknowledgments
This project was developed as an educational portfolio piece to practice network analysis, object-oriented programming, and Python best practices. I want to explicitly acknowledge the assistance of AI, which acted as technical mentor and architectural guide throughout the entire development of this program.
