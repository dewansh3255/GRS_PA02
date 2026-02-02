#!/usr/bin/env python3
"""
MT25067
Part D: Plotting and Visualization
Generates all required plots from experimental data
"""

import matplotlib.pyplot as plt
import numpy as np

# Set publication-quality plot style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

# System configuration
SYSTEM_CONFIG = """
System: Ubuntu 22.04.5 LTS
CPU: Intel x86_64
Kernel: 6.8.0-90-generic
Network: Localhost (127.0.0.1)
Date: February 2, 2026
"""

# Hardcoded experimental data from CSV
# Format: Implementation, MessageSize, NumThreads, Throughput_Mbps, Latency_us, 
#         TotalBytes, CPU_Cycles, CacheMisses, L1_Misses

# Part A1 - Two-Copy
A1_data = {
    256: {
        1: {'throughput': 1820.44, 'latency': 1.12, 'cycles': 11, 'cache_misses': 64, 'l1_misses': 38},
        2: {'throughput': 1709.52, 'latency': 1.20, 'cycles': 19, 'cache_misses': 119, 'l1_misses': 46},
        4: {'throughput': 1873.74, 'latency': 1.09, 'cycles': 25, 'cache_misses': 128, 'l1_misses': 53},
        8: {'throughput': 1806.00, 'latency': 1.13, 'cycles': 47, 'cache_misses': 113, 'l1_misses': 102},
    },
    1024: {
        1: {'throughput': 7230.36, 'latency': 1.13, 'cycles': 9, 'cache_misses': 141, 'l1_misses': 33},
        2: {'throughput': 10516.05, 'latency': 0.78, 'cycles': 17, 'cache_misses': 109, 'l1_misses': 48},
        4: {'throughput': 6291.86, 'latency': 1.30, 'cycles': 31, 'cache_misses': 131, 'l1_misses': 83},
        8: {'throughput': 8159.36, 'latency': 1.00, 'cycles': 53, 'cache_misses': 180, 'l1_misses': 125},
    },
    4096: {
        1: {'throughput': 20289.78, 'latency': 1.61, 'cycles': 16, 'cache_misses': 92, 'l1_misses': 50},
        2: {'throughput': 20699.94, 'latency': 1.58, 'cycles': 21, 'cache_misses': 89, 'l1_misses': 107},
        4: {'throughput': 28054.79, 'latency': 1.17, 'cycles': 39, 'cache_misses': 198, 'l1_misses': 211},
        8: {'throughput': 17273.59, 'latency': 1.90, 'cycles': 85, 'cache_misses': 248, 'l1_misses': 487},
    },
    16384: {
        1: {'throughput': 36725.13, 'latency': 3.57, 'cycles': 30, 'cache_misses': 199, 'l1_misses': 89},
        2: {'throughput': 37740.28, 'latency': 3.47, 'cycles': 55, 'cache_misses': 212, 'l1_misses': 884},
        4: {'throughput': 27536.13, 'latency': 4.76, 'cycles': 111, 'cache_misses': 134, 'l1_misses': 2},
        8: {'throughput': 44933.84, 'latency': 2.92, 'cycles': 208, 'cache_misses': 330, 'l1_misses': 3},
    }
}

# Part A2 - One-Copy
A2_data = {
    256: {
        1: {'throughput': 1409.50, 'latency': 1.45, 'cycles': 13, 'cache_misses': 118, 'l1_misses': 40},
        2: {'throughput': 1340.31, 'latency': 1.53, 'cycles': 19, 'cache_misses': 94, 'l1_misses': 37},
        4: {'throughput': 1513.67, 'latency': 1.35, 'cycles': 34, 'cache_misses': 121, 'l1_misses': 68},
        8: {'throughput': 1386.59, 'latency': 1.48, 'cycles': 56, 'cache_misses': 154, 'l1_misses': 88},
    },
    1024: {
        1: {'throughput': 5107.23, 'latency': 1.60, 'cycles': 15, 'cache_misses': 131, 'l1_misses': 44},
        2: {'throughput': 5425.17, 'latency': 1.51, 'cycles': 23, 'cache_misses': 165, 'l1_misses': 75},
        4: {'throughput': 8159.36, 'latency': 1.00, 'cycles': 35, 'cache_misses': 120, 'l1_misses': 100},
        8: {'throughput': 6901.43, 'latency': 1.19, 'cycles': 66, 'cache_misses': 241, 'l1_misses': 176},
    },
    4096: {
        1: {'throughput': 13534.90, 'latency': 2.42, 'cycles': 18, 'cache_misses': 145, 'l1_misses': 44},
        2: {'throughput': 19469.99, 'latency': 1.68, 'cycles': 27, 'cache_misses': 96, 'l1_misses': 138},
        4: {'throughput': 18502.54, 'latency': 1.77, 'cycles': 45, 'cache_misses': 292, 'l1_misses': 226},
        8: {'throughput': 21127.01, 'latency': 1.55, 'cycles': 95, 'cache_misses': 194, 'l1_misses': 504},
    },
    16384: {
        1: {'throughput': 44582.31, 'latency': 2.94, 'cycles': 27, 'cache_misses': 110, 'l1_misses': 466},
        2: {'throughput': 41716.10, 'latency': 3.14, 'cycles': 48, 'cache_misses': 181, 'l1_misses': 897},
        4: {'throughput': 52702.85, 'latency': 2.49, 'cycles': 91, 'cache_misses': 149, 'l1_misses': 1},
        8: {'throughput': 44221.32, 'latency': 2.96, 'cycles': 208, 'cache_misses': 538, 'l1_misses': 3},
    }
}

# Part A3 - Zero-Copy
A3_data = {
    256: {
        1: {'throughput': 513.54, 'latency': 3.99, 'cycles': 153, 'cache_misses': 188, 'l1_misses': 188},
        2: {'throughput': 515.22, 'latency': 3.98, 'cycles': 442, 'cache_misses': 606, 'l1_misses': 468},
        4: {'throughput': 649.75, 'latency': 3.15, 'cycles': 394, 'cache_misses': 476, 'l1_misses': 1},
        8: {'throughput': 790.43, 'latency': 2.59, 'cycles': 732, 'cache_misses': 194, 'l1_misses': 2},
    },
    1024: {
        1: {'throughput': 2486.19, 'latency': 3.29, 'cycles': 213, 'cache_misses': 675, 'l1_misses': 229},
        2: {'throughput': 1928.89, 'latency': 4.25, 'cycles': 286, 'cache_misses': 335, 'l1_misses': 491},
        4: {'throughput': 180.63, 'latency': 45.35, 'cycles': 933, 'cache_misses': 912, 'l1_misses': 1},
        8: {'throughput': 1951.87, 'latency': 4.20, 'cycles': 745, 'cache_misses': 285, 'l1_misses': 2},
    },
    4096: {
        1: {'throughput': 6653.40, 'latency': 4.92, 'cycles': 228, 'cache_misses': 210, 'l1_misses': 250},
        2: {'throughput': 740.96, 'latency': 44.22, 'cycles': 215, 'cache_misses': 380, 'l1_misses': 503},
        4: {'throughput': 6382.55, 'latency': 5.13, 'cycles': 570, 'cache_misses': 318, 'l1_misses': 949},
        8: {'throughput': 158.57, 'latency': 206.64, 'cycles': 718, 'cache_misses': 315, 'l1_misses': 2},
    },
    16384: {
        1: {'throughput': 29081.87, 'latency': 4.51, 'cycles': 232, 'cache_misses': 956, 'l1_misses': 502},
        2: {'throughput': 28395.15, 'latency': 4.62, 'cycles': 450, 'cache_misses': 796, 'l1_misses': 842},
        4: {'throughput': 2752.51, 'latency': 47.62, 'cycles': 932, 'cache_misses': 536, 'l1_misses': 2},
        8: {'throughput': 18788.99, 'latency': 6.98, 'cycles': 1094, 'cache_misses': 1124, 'l1_misses': 5},
    }
}

message_sizes = [256, 1024, 4096, 16384]
thread_counts = [1, 2, 4, 8]

def extract_metric(data_dict, metric_name):
    """Extract a specific metric across all message sizes and thread counts"""
    result = {}
    for msg_size in message_sizes:
        result[msg_size] = {}
        for threads in thread_counts:
            result[msg_size][threads] = data_dict[msg_size][threads][metric_name]
    return result

# Plot 1: Throughput vs Message Size (for different thread counts)
def plot_throughput_vs_message_size():
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Throughput vs Message Size\n(Different Thread Counts)', fontsize=16, fontweight='bold')
    
    for idx, threads in enumerate(thread_counts):
        ax = axes[idx // 2, idx % 2]
        
        # Extract throughput for this thread count
        a1_throughput = [A1_data[size][threads]['throughput'] for size in message_sizes]
        a2_throughput = [A2_data[size][threads]['throughput'] for size in message_sizes]
        a3_throughput = [A3_data[size][threads]['throughput'] for size in message_sizes]
        
        # Plot
        ax.plot(message_sizes, a1_throughput, 'o-', linewidth=2, markersize=8, label='A1 (Two-Copy)')
        ax.plot(message_sizes, a2_throughput, 's-', linewidth=2, markersize=8, label='A2 (One-Copy)')
        ax.plot(message_sizes, a3_throughput, '^-', linewidth=2, markersize=8, label='A3 (Zero-Copy)')
        
        ax.set_xlabel('Message Size (bytes)', fontweight='bold')
        ax.set_ylabel('Throughput (Mbps)', fontweight='bold')
        ax.set_title(f'{threads} Thread(s)', fontweight='bold')
        ax.set_xscale('log', base=2)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Add values on points
        for i, size in enumerate(message_sizes):
            ax.annotate(f'{a1_throughput[i]:.0f}', (size, a1_throughput[i]), 
                       textcoords="offset points", xytext=(0,5), ha='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('MT25067_Plot1_Throughput_vs_MessageSize.pdf', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot1_Throughput_vs_MessageSize.pdf")
    plt.close()

# Plot 2: Latency vs Thread Count (for different message sizes)
def plot_latency_vs_thread_count():
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Latency vs Thread Count\n(Different Message Sizes)', fontsize=16, fontweight='bold')
    
    for idx, msg_size in enumerate(message_sizes):
        ax = axes[idx // 2, idx % 2]
        
        # Extract latency for this message size
        a1_latency = [A1_data[msg_size][t]['latency'] for t in thread_counts]
        a2_latency = [A2_data[msg_size][t]['latency'] for t in thread_counts]
        a3_latency = [A3_data[msg_size][t]['latency'] for t in thread_counts]
        
        # Plot
        ax.plot(thread_counts, a1_latency, 'o-', linewidth=2, markersize=8, label='A1 (Two-Copy)')
        ax.plot(thread_counts, a2_latency, 's-', linewidth=2, markersize=8, label='A2 (One-Copy)')
        ax.plot(thread_counts, a3_latency, '^-', linewidth=2, markersize=8, label='A3 (Zero-Copy)')
        
        ax.set_xlabel('Number of Threads', fontweight='bold')
        ax.set_ylabel('Average Latency (µs)', fontweight='bold')
        ax.set_title(f'Message Size: {msg_size} bytes', fontweight='bold')
        ax.set_xticks(thread_counts)
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    plt.tight_layout()
    plt.savefig('MT25067_Plot2_Latency_vs_ThreadCount.pdf', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot2_Latency_vs_ThreadCount.pdf")
    plt.close()

# Plot 3: Cache Misses vs Message Size (single thread for clarity)
def plot_cache_misses_vs_message_size():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Cache Misses vs Message Size (1 Thread)', fontsize=16, fontweight='bold')
    
    # Extract cache misses for 1 thread
    a1_cache = [A1_data[size][1]['cache_misses'] for size in message_sizes]
    a2_cache = [A2_data[size][1]['cache_misses'] for size in message_sizes]
    a3_cache = [A3_data[size][1]['cache_misses'] for size in message_sizes]
    
    a1_l1 = [A1_data[size][1]['l1_misses'] for size in message_sizes]
    a2_l1 = [A2_data[size][1]['l1_misses'] for size in message_sizes]
    a3_l1 = [A3_data[size][1]['l1_misses'] for size in message_sizes]
    
    # LLC Cache Misses
    ax1.plot(message_sizes, a1_cache, 'o-', linewidth=2, markersize=8, label='A1 (Two-Copy)')
    ax1.plot(message_sizes, a2_cache, 's-', linewidth=2, markersize=8, label='A2 (One-Copy)')
    ax1.plot(message_sizes, a3_cache, '^-', linewidth=2, markersize=8, label='A3 (Zero-Copy)')
    ax1.set_xlabel('Message Size (bytes)', fontweight='bold')
    ax1.set_ylabel('LLC Cache Misses', fontweight='bold')
    ax1.set_title('Last Level Cache Misses', fontweight='bold')
    ax1.set_xscale('log', base=2)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # L1 Cache Misses
    ax2.plot(message_sizes, a1_l1, 'o-', linewidth=2, markersize=8, label='A1 (Two-Copy)')
    ax2.plot(message_sizes, a2_l1, 's-', linewidth=2, markersize=8, label='A2 (One-Copy)')
    ax2.plot(message_sizes, a3_l1, '^-', linewidth=2, markersize=8, label='A3 (Zero-Copy)')
    ax2.set_xlabel('Message Size (bytes)', fontweight='bold')
    ax2.set_ylabel('L1 D-Cache Misses', fontweight='bold')
    ax2.set_title('L1 Data Cache Misses', fontweight='bold')
    ax2.set_xscale('log', base=2)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('MT25067_Plot3_CacheMisses_vs_MessageSize.pdf', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot3_CacheMisses_vs_MessageSize.pdf")
    plt.close()

# Plot 4: CPU Cycles per Byte Transferred
def plot_cpu_cycles_per_byte():
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('CPU Cycles per Byte Transferred\n(Different Thread Counts)', fontsize=16, fontweight='bold')
    
    for idx, threads in enumerate(thread_counts):
        ax = axes[idx // 2, idx % 2]
        
        # Calculate cycles per byte (cycles per million / bytes per million)
        a1_cpb = [A1_data[size][threads]['cycles'] * 1e6 / (size * 1000) for size in message_sizes]
        a2_cpb = [A2_data[size][threads]['cycles'] * 1e6 / (size * 1000) for size in message_sizes]
        a3_cpb = [A3_data[size][threads]['cycles'] * 1e6 / (size * 1000) for size in message_sizes]
        
        # Plot
        ax.plot(message_sizes, a1_cpb, 'o-', linewidth=2, markersize=8, label='A1 (Two-Copy)')
        ax.plot(message_sizes, a2_cpb, 's-', linewidth=2, markersize=8, label='A2 (One-Copy)')
        ax.plot(message_sizes, a3_cpb, '^-', linewidth=2, markersize=8, label='A3 (Zero-Copy)')
        
        ax.set_xlabel('Message Size (bytes)', fontweight='bold')
        ax.set_ylabel('CPU Cycles per Byte', fontweight='bold')
        ax.set_title(f'{threads} Thread(s)', fontweight='bold')
        ax.set_xscale('log', base=2)
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    plt.tight_layout()
    plt.savefig('MT25067_Plot4_CPUCycles_per_Byte.pdf', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot4_CPUCycles_per_Byte.pdf")
    plt.close()

# Bonus Plot 5: Overall Comparison (16KB, varying threads)
def plot_overall_comparison():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Comprehensive Comparison - 16KB Messages\nAll Metrics vs Thread Count', 
                 fontsize=16, fontweight='bold')
    
    msg_size = 16384
    
    # Throughput
    a1_thr = [A1_data[msg_size][t]['throughput'] for t in thread_counts]
    a2_thr = [A2_data[msg_size][t]['throughput'] for t in thread_counts]
    a3_thr = [A3_data[msg_size][t]['throughput'] for t in thread_counts]
    
    ax1.plot(thread_counts, a1_thr, 'o-', linewidth=2, markersize=8, label='A1')
    ax1.plot(thread_counts, a2_thr, 's-', linewidth=2, markersize=8, label='A2')
    ax1.plot(thread_counts, a3_thr, '^-', linewidth=2, markersize=8, label='A3')
    ax1.set_xlabel('Threads', fontweight='bold')
    ax1.set_ylabel('Throughput (Mbps)', fontweight='bold')
    ax1.set_title('Throughput', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Latency
    a1_lat = [A1_data[msg_size][t]['latency'] for t in thread_counts]
    a2_lat = [A2_data[msg_size][t]['latency'] for t in thread_counts]
    a3_lat = [A3_data[msg_size][t]['latency'] for t in thread_counts]
    
    ax2.plot(thread_counts, a1_lat, 'o-', linewidth=2, markersize=8, label='A1')
    ax2.plot(thread_counts, a2_lat, 's-', linewidth=2, markersize=8, label='A2')
    ax2.plot(thread_counts, a3_lat, '^-', linewidth=2, markersize=8, label='A3')
    ax2.set_xlabel('Threads', fontweight='bold')
    ax2.set_ylabel('Latency (µs)', fontweight='bold')
    ax2.set_title('Latency', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # CPU Cycles
    a1_cyc = [A1_data[msg_size][t]['cycles'] for t in thread_counts]
    a2_cyc = [A2_data[msg_size][t]['cycles'] for t in thread_counts]
    a3_cyc = [A3_data[msg_size][t]['cycles'] for t in thread_counts]
    
    ax3.plot(thread_counts, a1_cyc, 'o-', linewidth=2, markersize=8, label='A1')
    ax3.plot(thread_counts, a2_cyc, 's-', linewidth=2, markersize=8, label='A2')
    ax3.plot(thread_counts, a3_cyc, '^-', linewidth=2, markersize=8, label='A3')
    ax3.set_xlabel('Threads', fontweight='bold')
    ax3.set_ylabel('CPU Cycles (Millions)', fontweight='bold')
    ax3.set_title('CPU Cycles', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Cache Misses
    a1_cache = [A1_data[msg_size][t]['cache_misses'] for t in thread_counts]
    a2_cache = [A2_data[msg_size][t]['cache_misses'] for t in thread_counts]
    a3_cache = [A3_data[msg_size][t]['cache_misses'] for t in thread_counts]
    
    ax4.plot(thread_counts, a1_cache, 'o-', linewidth=2, markersize=8, label='A1')
    ax4.plot(thread_counts, a2_cache, 's-', linewidth=2, markersize=8, label='A2')
    ax4.plot(thread_counts, a3_cache, '^-', linewidth=2, markersize=8, label='A3')
    ax4.set_xlabel('Threads', fontweight='bold')
    ax4.set_ylabel('Cache Misses', fontweight='bold')
    ax4.set_title('LLC Cache Misses', fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('MT25067_Plot5_Overall_Comparison.pdf', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot5_Overall_Comparison.pdf")
    plt.close()

def main():
    print("=" * 60)
    print("MT25067 - Part D: Generating Plots")
    print("=" * 60)
    print(f"System Configuration:\n{SYSTEM_CONFIG}")
    print("Generating plots...")
    print()
    
    plot_throughput_vs_message_size()
    plot_latency_vs_thread_count()
    plot_cache_misses_vs_message_size()
    plot_cpu_cycles_per_byte()
    plot_overall_comparison()
    
    print()
    print("=" * 60)
    print("All plots generated successfully!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  1. MT25067_Plot1_Throughput_vs_MessageSize.pdf")
    print("  2. MT25067_Plot2_Latency_vs_ThreadCount.pdf")
    print("  3. MT25067_Plot3_CacheMisses_vs_MessageSize.pdf")
    print("  4. MT25067_Plot4_CPUCycles_per_Byte.pdf")
    print("  5. MT25067_Plot5_Overall_Comparison.pdf")
    print("\nThese plots are ready for inclusion in your report!")

if __name__ == "__main__":
    main()
