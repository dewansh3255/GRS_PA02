# MT25067
# PA02: Network I/O Analysis - Graduate Systems (CSE638)

## Project Structure
This project implements and analyzes three network I/O primitives:
- **Part A1**: Two-Copy (baseline using send/recv)
- **Part A2**: One-Copy (using sendmsg with pre-registered buffer)
- **Part A3**: Zero-Copy (using MSG_ZEROCOPY flag)

## Build Instructions

### Compile Part A1 (Two-Copy)
```bash
make part_a1
```

### Compile Part A2 (One-Copy)
```bash
make part_a2
```

### Compile Part A3 (Zero-Copy)
```bash
make part_a3
```

### Compile All Parts
```bash
make all  # Currently builds Part A1 only
```

### Clean Binaries
```bash
make clean
```

## Running the Programs

### Part A1: Two-Copy Implementation

**Terminal 1 (Server):**
```bash
./MT25067_PartA1_Server <message_size> <num_messages> <max_clients>
# Example: ./MT25067_PartA1_Server 1024 10000 4
```

**Terminal 2 (Client):**
```bash
./MT25067_PartA1_Client <message_size> <num_messages>
# Example: ./MT25067_PartA1_Client 1024 10000
```

### Part A2: One-Copy Implementation

**Terminal 1 (Server):**
```bash
./MT25067_PartA2_Server <message_size> <num_messages> <max_clients>
# Example: ./MT25067_PartA2_Server 1024 10000 4
```

**Terminal 2 (Client):**
```bash
./MT25067_PartA2_Client <message_size> <num_messages>
# Example: ./MT25067_PartA2_Client 1024 10000
```

**Note:** Part A2 uses port 8081 (A1 uses 8080) so both can run simultaneously for comparison.

### Testing with Multiple Clients
Open multiple client terminals and run the client command simultaneously.

## Parameters Explanation

- **message_size**: Size of each message in bytes (e.g., 256, 1024, 4096, 16384)
- **num_messages**: Number of messages to transfer per client (e.g., 10000)
- **max_clients**: Maximum number of concurrent client connections (e.g., 1, 2, 4, 8)

## Example Test Run

```bash
# Server (Terminal 1)
./MT25067_PartA1_Server 1024 10000 2

# Client 1 (Terminal 2)
./MT25067_PartA1_Client 1024 10000

# Client 2 (Terminal 3)
./MT25067_PartA1_Client 1024 10000
```

## Development Notes

### Current Status
- ✅ Part A1: Two-Copy implementation complete
- ✅ Part A2: One-Copy implementation complete
- ⏳ Part A3: Zero-Copy implementation (in progress)
- ⏳ Part C: Automation script (pending)
- ⏳ Part D: Plotting (pending)

### Platform Notes
- Developed on macOS (Apple Silicon M4)
- Tested on Linux (Ubuntu 22.04/24.04) for final measurements
- Network namespaces and perf profiling require Linux

## Author
MT25067
Graduate Systems (CSE638)