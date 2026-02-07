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
sudo apt install build-essential perf python3-matplotlib lsof
```

**macOS:**
```bash
brew install gcc python3
pip3 install matplotlib
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

## 💻 Usage

### Part A1: Two-Copy

**Terminal 1 (Server):**
```bash
./MT25067_PartA1_Server <msg_size> <num_msgs> <threads>
# Example:
./MT25067_PartA1_Server 16384 1000 4
```

**Terminal 2 (Client):**
```bash
./MT25067_PartA1_Client <msg_size> <num_msgs>
# Example:
./MT25067_PartA1_Client 16384 1000
```

### Part A2: One-Copy

```bash
# Server
./MT25067_PartA2_Server 16384 1000 4

# Client (separate terminal)
./MT25067_PartA2_Client 16384 1000
```

### Part A3: Zero-Copy

```bash
# Server (use 1 thread only!)
./MT25067_PartA3_Server 16384 1000 1

# Client
./MT25067_PartA3_Client 16384 1000
```

**⚠️ Warning:** A3 has catastrophic performance with multiple threads on localhost.

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

### Port In Use

The automation script uses an improved dual-method port checking:
- **Primary:** `ss` command (modern, faster)
- **Fallback:** `lsof` (for compatibility)

```bash
# Manual cleanup if needed:
sudo lsof -ti:8080 | xargs kill -9
sudo lsof -ti:8081 | xargs kill -9
sudo lsof -ti:8082 | xargs kill -9
```

**Note:** The script's `check_port()` function automatically handles port conflicts with robust error handling.

### perf Permission Denied

```bash
# Run script with sudo
sudo bash MT25067_PartC_AutomationScript.sh

# Or adjust paranoid level
echo 0 | sudo tee /proc/sys/kernel/perf_event_paranoid
```

### matplotlib Missing

```bash
pip3 install matplotlib --break-system-packages
```

---

## 💡 Key Learnings

1. **Copy elimination matters, but context matters more**
   - A2 beat A1 by 91% in optimal configuration
   - But A1 wins for small messages

2. **Zero-copy isn't always zero-copy**
   - 100% fallback on localhost
   - Requires real NIC with DMA

3. **Platform dependency is real**
   - macOS (ARM): A1 wins everywhere
   - Linux (x86): A2 wins at large messages

4. **Threading is non-linear**
   - A2 peaks at 4 threads
   - A3 catastrophically fails with threading

5. **Always measure, never assume**
   - "Advanced" techniques can be slower
   - Profile on target hardware

---

## 📞 Contact

**Student:** MT25067  
**Course:** CSE638 - Graduate Distributed Systems  
**Institution:** IIIT Delhi  
**Repository:** https://github.com/dewansh3255/GRS_PA02

---

**Last Updated:** February 6, 2026  