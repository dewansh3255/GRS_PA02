# MT25067 - PA02: Network I/O Performance Analysis

**Graduate Distributed Systems (CSE638) - Programming Assignment 02**

Analysis of Network I/O Primitives: Two-Copy, One-Copy, and Zero-Copy Implementations

---

## 🚀 Quick Start

```bash
# Clone and build
git clone https://github.com/dewansh3255/GRS_PA02
cd GRS_PA02
make all

# Run automated experiments (30-45 min)
sudo bash MT25067_PartC_AutomationScript.sh

# Generate plots
python3 MT25067_PartD_Plots.py
```

---

## 📁 Repository Structure

```
MT25067_PA02/
├── MT25067_PartA1_Server.c          # Two-copy server
├── MT25067_PartA1_Client.c          # Two-copy client
├── MT25067_PartA2_Server.c          # One-copy server (sendmsg)
├── MT25067_PartA2_Client.c          # One-copy client
├── MT25067_PartA3_Server.c          # Zero-copy server (MSG_ZEROCOPY)
├── MT25067_PartA3_Client.c          # Zero-copy client
├── MT25067_PartC_AutomationScript.sh # Experiment automation
├── MT25067_PartD_Plots.py           # Plotting script (hardcoded data)
├── MT25067_PartE_Analysis.md        # Analysis and reasoning
├── MT25067_ExperimentData.csv       # Raw experimental data
├── MT25067_Report.md                # Assignment report
├── Makefile                         # Build system
└── README.md                        # This file
```

---

## 🎯 Assignment Overview

This assignment compares three network I/O approaches:

| Implementation | Copies | Technique | Port |
|----------------|--------|-----------|------|
| **Part A1** | 2 | send() with serialization | 8080 |
| **Part A2** | 1 | sendmsg() scatter-gather | 8081 |
| **Part A3** | 0* | MSG_ZEROCOPY | 8082 |

*Note: A3 achieves 100% copy fallback on localhost

---

## 🔧 Prerequisites

**Ubuntu/Linux:**
```bash
sudo apt update
sudo apt install build-essential linux-tools-common linux-tools-generic \
                 python3 python3-matplotlib lsof iproute2
```

---
## 📡 Network Namespace Setup (Required)

### Automated Setup (Recommended)

```bash
# Run the provided setup script
sudo bash ./MT25067_Setup_Netns.sh
```

This creates:
- **Server namespace**: `server_ns` (IP: 10.0.0.1/24)
- **Client namespace**: `client_ns` (IP: 10.0.0.2/24)
- **veth pair**: Virtual ethernet connecting the namespaces

### Manual Setup (Alternative)

```bash
# Create namespaces
sudo ip netns add server_ns
sudo ip netns add client_ns

# Create veth pair
sudo ip link add veth_server type veth peer name veth_client

# Move interfaces to namespaces
sudo ip link set veth_server netns server_ns
sudo ip link set veth_client netns client_ns

# Configure IP addresses
sudo ip netns exec server_ns ip addr add 10.0.0.1/24 dev veth_server
sudo ip netns exec client_ns ip addr add 10.0.0.2/24 dev veth_client

# Bring up interfaces
sudo ip netns exec server_ns ip link set veth_server up
sudo ip netns exec server_ns ip link set lo up
sudo ip netns exec client_ns ip link set veth_client up
sudo ip netns exec client_ns ip link set lo up

# Verify connectivity
sudo ip netns exec client_ns ping -c 3 10.0.0.1
```

### Cleanup Namespaces

```bash
sudo bash ./MT25067_Cleanup_Netns.sh
# OR manually:
sudo ip netns del server_ns
sudo ip netns del client_ns
```

---
## 🏗️ Building

```bash
# Build all implementations
make all

# Build individual parts
make part_a1
make part_a2
make part_a3

# Clean
make clean
```

---

## 💻 Manual Usage

### Part A1: Two-Copy Implementation

**Terminal 1 (Server):**
```bash
./MT25067_PartA1_Server 16384 5000 4
# Args: <message_size> <num_messages> <num_threads>
```

**Terminal 2 (Client, repeat 4 times for 4 threads):**
```bash
./MT25067_PartA1_Client 16384 5000
# Args: <message_size> <num_messages>
```

### Part A2: One-Copy Implementation

**Server:**
```bash
./MT25067_PartA2_Server 16384 5000 4
```

**Client:**
```bash
./MT25067_PartA2_Client 16384 5000
```

### Part A3: Zero-Copy Implementation

**⚠️ Important:** Use **1 thread only** on localhost to avoid catastrophic performance collapse.

**Server:**
```bash
./MT25067_PartA3_Server 16384 5000 1
```

**Client:**
```bash
./MT25067_PartA3_Client 16384 5000
```

---

## 📊 Performance Results

### Peak Performance (Network Namespaces via veth)

| Configuration | A1 (Gbps) | A2 (Gbps) | A3 (Gbps) | Winner |
|---------------|-----------|-----------|-----------|--------|
| 16KB, 1T | 30.23 | 31.85 | 21.88 | **A2** |
| 16KB, 2T | **33.44** | 27.83 | 19.37 | **A1** ⭐ |
| 16KB, 4T | 33.34 | 23.26 | 22.12 | **A1** |
| 16KB, 8T | 31.94 | 25.35 | 16.46 | **A1** |

**🏆 Absolute Peak:** A1 at 2 threads, 16KB = **33.44 Gbps**  
**🏆 Best Scaling:** A1 maintains ~31-33 Gbps across all thread counts

### Key Findings

#### ✅ What Worked

1. **A1 (Two-Copy) Dominates Overall**
   - Best throughput across most configurations
   - Peak: 33.44 Gbps at 2 threads, 16KB
   - Intel's optimized `memcpy()` (ERMSB) is extremely fast

2. **A2 (One-Copy) Competitive at 1 Thread**
   - Slightly wins at 16KB with 1 thread (31.85 vs 30.23 Gbps)
   - Good cache behavior with reduced copies
   - Scatter-gather reduces false sharing

3. **Threading Sweet Spot: 4 Threads**
   - Matches Intel i7-12700's 4 P-cores
   - Both A1 and A2 perform well
   - Beyond 4 threads: diminishing returns

#### ❌ What Didn't Work

1. **A3 (Zero-Copy) Failed Completely on Localhost**
   - **100% copy fallback** (no physical NIC)
   - Best case: 42% slower than A1 (16KB, 1T)
   - Worst case: **5,534% slower** than A1 (4KB, 4T)
   - Context switch storm: 4,685 switches vs A1's 3

2. **A3 Context Switch Explosion**
   - Context switches: 4,682 (1T) → 37,454 (8T)
   - 485× more context switches than A1 at 8 threads
   - MSG_ERRQUEUE polling causes massive overhead

3. **Small Messages Have High Overhead**
   - Setup costs dominate for <1KB messages
   - A1 wins decisively at small sizes
   - iovec overhead in A2 not worth it

---

## 📊 Automated Experiments

Run all 48 experiments automatically:

```bash
sudo bash MT25067_PartC_AutomationScript.sh
```

**Output:** `experiment_results/MT25067_ExperimentData.csv`

**Parameters:**
- Message sizes: 256B, 1KB, 4KB, 16KB
- Thread counts: 1, 2, 4, 8
- Implementations: A1, A2, A3

---

## 📈 Generating Plots

```bash
python3 MT25067_PartD_Plots.py
```

**Generates 5 plots** (PDF + PNG):
1. Throughput vs Message Size
2. Latency vs Thread Count
3. Cache Misses vs Message Size
4. CPU Cycles per Byte
5. Overall Comparison (16KB)

---

## 🐛 Troubleshooting

### Port Already in Use

**Problem:**
```
bind: Address already in use
```

**Solution:**
The automation script handles this automatically, but for manual cleanup:

```bash
# Kill processes on specific ports
sudo lsof -ti:8080 | xargs kill -9
sudo lsof -ti:8081 | xargs kill -9
sudo lsof -ti:8082 | xargs kill -9

# Or kill all your servers
killall MT25067_PartA1_Server MT25067_PartA2_Server MT25067_PartA3_Server
```

**Prevention:** The automation script uses dual-method port checking:
```bash
# Primary: ss (modern)
ss -tuln | grep ":8080 "

# Fallback: lsof (compatibility)
lsof -i :8080
```

### perf Permission Denied

**Problem:**
```
perf_event_open(...) failed: Permission denied
```

**Solution:**
```bash
# Temporary (current session)
echo 0 | sudo tee /proc/sys/kernel/perf_event_paranoid

# Or run automation script with sudo
sudo bash MT25067_PartC_AutomationScript.sh
```

### matplotlib Import Error

**Problem:**
```
ModuleNotFoundError: No module named 'matplotlib'
```

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install python3-matplotlib

# Or via pip (if apt not available)
pip3 install matplotlib --break-system-packages
```

### Compilation Warnings

**Problem:**
```
warning: unused variable 'xyz'
```

**Solution:** These are informational only. Code compiles with `-Wall -Wextra` for strict checking. To suppress:
```bash
make clean
make CFLAGS="-O2 -pthread"  # Without -Wall -Wextra
```

---

## 💡 Key Learnings

1. **Zero-Copy Isn't Always Zero-Copy**
   - 100% fallback on veth (virtual interface)
   - Requires real NIC with DMA
   - Overhead can exceed benefits

2. **Threading Has Non-Linear Effects**
   - A1 maintains good performance up to 8 threads
   - A3 suffers from context switch explosion at higher thread counts
   - Sweet spot varies by implementation

3. **Cache Hierarchy Matters More Than Cache Misses**
   - LLC misses more expensive than L1 misses
   - A2 reduces LLC misses despite more L1 misses
   - Total system behavior > single metric

4. **Simple ≠ Scalable**
   - A1's "simple" design fails under contention
   - A2's "complex" scatter-gather scales better
   - Contiguous buffers create serialization points

5. **Platform Dependency is Real**
   - macOS (ARM): A1 wins everywhere
   - Linux (x86): A2 wins at large messages + threading
   - Always profile on target hardware

---

## 📞 Contact

**Student:** MT25067  
**Course:** CSE638 - Graduate Distributed Systems  
**Institution:** IIIT Delhi  
**Repository:** https://github.com/dewansh3255/GRS_PA02

---

**Last Updated:** February 7, 2026  