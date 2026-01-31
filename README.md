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

## Performance Test Results

### Part A1 vs Part A2 Comparison (macOS localhost)

| Message Size | A1 Throughput (Mbps) | A2 Throughput (Mbps) | Winner | Difference |
|--------------|---------------------|---------------------|--------|------------|
| 256B         | 1706.10             | 1458.01             | A1     | -14.5%     |
| 1KB          | 4273.79             | 4313.85             | A2     | +0.9%      |
| 4KB          | 13075.82            | 11479.42            | A1     | -12.2%     |
| 16KB         | 26016.67            | 23603.82            | A1     | -9.3%      |

### Key Findings

1. **Part A2 (one-copy) only outperforms Part A1 (two-copy) at 1KB message size** with a marginal 0.9% improvement.

2. **For all other message sizes, Part A1 is faster** due to cache locality effects:
   - 256B: A1 is 14.5% faster
   - 4KB: A1 is 12.2% faster
   - 16KB: A1 is 9.3% faster

3. **Cache Locality Dominates**: The "extra" memcpy in Part A1's `serialize_message()` creates a contiguous buffer that:
   - Warms CPU cache (L1/L2)
   - Enables better prefetching
   - Reduces TLB pressure
   - Results in faster `send()` operation

4. **Lesson Learned**: "Zero-copy" optimizations don't always improve performance. Cache effects can outweigh the cost of an extra copy in modern systems.

### Testing Configuration
- Platform: macOS (Apple Silicon M4)
- Network: localhost (127.0.0.1)
- Compiler: Apple clang 17.0.0
- Test methodology: Multiple runs averaged

**Note**: Final performance measurements will be conducted on Linux with `perf` profiling for cache miss analysis.

## Author
MT25067
Graduate Systems (CSE638)