#!/usr/bin/env python3
"""
MT25067
Part D: Dynamic Plotting and Visualization
Reads data directly from CSV file (no hardcoded data!)
"""

import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import glob

# Set publication-quality plot style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10

# System configuration
SYSTEM_CONFIG = """
System: Ubuntu 22.04.5 LTS
CPU: Intel x86_64
Kernel: 6.8.0-90-generic
Network: Localhost (127.0.0.1)
Date: February 2026
"""

def find_csv_file():
    """Find the CSV file in possible locations"""
    possible_paths = [
        'experiment_results/MT25067_ExperimentData.csv',
        'MT25067_ExperimentData.csv',
    ]
    
    # Also search for timestamped files
    timestamped = glob.glob('experiment_results/MT25067_AllResults_*.csv')
    if timestamped:
        possible_paths.extend(sorted(timestamped, reverse=True))  # Latest first
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def load_data(csv_file):
    """Load experimental data from CSV file"""
    try:
        df = pd.read_csv(csv_file)
        print(f"✓ Loaded: {csv_file}")
        print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
        return df
    except Exception as e:
        print(f"ERROR loading CSV: {e}")
        sys.exit(1)

def organize_data(df):
    """Organize data by implementation, message size, and thread count"""
    data = {}
    
    for impl in df['Implementation'].unique():
        data[impl] = {}
        impl_data = df[df['Implementation'] == impl]
        
        for size in sorted(impl_data['MessageSize'].unique()):
            data[impl][size] = {}
            size_data = impl_data[impl_data['MessageSize'] == size]
            
            for threads in sorted(size_data['NumThreads'].unique()):
                thread_data = size_data[size_data['NumThreads'] == threads].iloc[0]
                data[impl][size][threads] = {
                    'throughput': thread_data['Throughput_Mbps'],
                    'latency': thread_data['Latency_us'],
                    'cycles': thread_data['CPU_Cycles'] / 1e6,  # Millions
                    'cache_misses': thread_data['CacheMisses'],
                    'l1_misses': thread_data['L1_Misses'],
                    'total_bytes': thread_data['TotalBytes']
                }
    
    return data

# Plot 1: Throughput vs Message Size
def plot_throughput_vs_message_size(data, message_sizes, thread_counts, implementations):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Throughput vs Message Size\n(Different Thread Counts)', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    labels = {'A1': 'A1 (Two-Copy)', 'A2': 'A2 (One-Copy)', 'A3': 'A3 (Zero-Copy)'}
    
    for idx, threads in enumerate(thread_counts):
        ax = axes[idx // 2, idx % 2]
        
        for impl in implementations:
            throughputs = [data[impl].get(size, {}).get(threads, {}).get('throughput', 0) 
                          for size in message_sizes]
            
            ax.plot(message_sizes, throughputs, 
                   marker=markers.get(impl, 'o'), 
                   color=colors.get(impl, 'gray'),
                   linewidth=2, markersize=8, 
                   label=labels.get(impl, impl))
            
            # Add value annotations
            for size, thr in zip(message_sizes, throughputs):
                if thr > 0:
                    ax.annotate(f'{thr:.0f}', (size, thr), 
                               textcoords="offset points", xytext=(0,5), 
                               ha='center', fontsize=8)
        
        ax.set_xlabel('Message Size (bytes)', fontweight='bold')
        ax.set_ylabel('Throughput (Mbps)', fontweight='bold')
        ax.set_title(f'{threads} Thread(s)', fontweight='bold')
        ax.set_xscale('log', base=2)
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    plt.tight_layout()
    plt.savefig('MT25067_Plot1_Throughput_vs_MessageSize.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('MT25067_Plot1_Throughput_vs_MessageSize.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot1_Throughput_vs_MessageSize.pdf & .png")
    plt.close()

# Plot 2: Latency vs Thread Count
def plot_latency_vs_thread_count(data, message_sizes, thread_counts, implementations):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Latency vs Thread Count\n(Different Message Sizes)', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    labels = {'A1': 'A1 (Two-Copy)', 'A2': 'A2 (One-Copy)', 'A3': 'A3 (Zero-Copy)'}
    
    for idx, msg_size in enumerate(message_sizes):
        ax = axes[idx // 2, idx % 2]
        
        for impl in implementations:
            latencies = [data[impl].get(msg_size, {}).get(t, {}).get('latency', 0) 
                        for t in thread_counts]
            
            ax.plot(thread_counts, latencies, 
                   marker=markers.get(impl, 'o'),
                   color=colors.get(impl, 'gray'),
                   linewidth=2, markersize=8, 
                   label=labels.get(impl, impl))
        
        ax.set_xlabel('Number of Threads', fontweight='bold')
        ax.set_ylabel('Average Latency (µs)', fontweight='bold')
        ax.set_title(f'Message Size: {msg_size} bytes', fontweight='bold')
        ax.set_xticks(thread_counts)
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    plt.tight_layout()
    plt.savefig('MT25067_Plot2_Latency_vs_ThreadCount.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('MT25067_Plot2_Latency_vs_ThreadCount.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot2_Latency_vs_ThreadCount.pdf & .png")
    plt.close()

# Plot 3: Cache Misses vs Message Size
def plot_cache_misses_vs_message_size(data, message_sizes, implementations):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Cache Misses vs Message Size (1 Thread)', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    labels = {'A1': 'A1 (Two-Copy)', 'A2': 'A2 (One-Copy)', 'A3': 'A3 (Zero-Copy)'}
    threads = 1
    
    # LLC Cache Misses
    for impl in implementations:
        cache_misses = [data[impl].get(size, {}).get(threads, {}).get('cache_misses', 0) 
                       for size in message_sizes]
        ax1.plot(message_sizes, cache_misses, 
                marker=markers.get(impl, 'o'),
                color=colors.get(impl, 'gray'),
                linewidth=2, markersize=8, 
                label=labels.get(impl, impl))
    
    ax1.set_xlabel('Message Size (bytes)', fontweight='bold')
    ax1.set_ylabel('LLC Cache Misses', fontweight='bold')
    ax1.set_title('Last Level Cache Misses', fontweight='bold')
    ax1.set_xscale('log', base=2)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # L1 Cache Misses
    for impl in implementations:
        l1_misses = [data[impl].get(size, {}).get(threads, {}).get('l1_misses', 0) 
                    for size in message_sizes]
        ax2.plot(message_sizes, l1_misses, 
                marker=markers.get(impl, 'o'),
                color=colors.get(impl, 'gray'),
                linewidth=2, markersize=8, 
                label=labels.get(impl, impl))
    
    ax2.set_xlabel('Message Size (bytes)', fontweight='bold')
    ax2.set_ylabel('L1 D-Cache Misses', fontweight='bold')
    ax2.set_title('L1 Data Cache Misses', fontweight='bold')
    ax2.set_xscale('log', base=2)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('MT25067_Plot3_CacheMisses_vs_MessageSize.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('MT25067_Plot3_CacheMisses_vs_MessageSize.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot3_CacheMisses_vs_MessageSize.pdf & .png")
    plt.close()

# Plot 4: CPU Cycles per Byte
def plot_cpu_cycles_per_byte(data, message_sizes, thread_counts, implementations):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('CPU Cycles per Byte Transferred\n(Different Thread Counts)', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    labels = {'A1': 'A1 (Two-Copy)', 'A2': 'A2 (One-Copy)', 'A3': 'A3 (Zero-Copy)'}
    
    for idx, threads in enumerate(thread_counts):
        ax = axes[idx // 2, idx % 2]
        
        for impl in implementations:
            cpb = []
            for size in message_sizes:
                d = data[impl].get(size, {}).get(threads, {})
                cycles = d.get('cycles', 0) * 1e6
                total_bytes = d.get('total_bytes', 1)
                cpb.append(cycles / total_bytes if total_bytes > 0 else 0)
            
            ax.plot(message_sizes, cpb, 
                   marker=markers.get(impl, 'o'),
                   color=colors.get(impl, 'gray'),
                   linewidth=2, markersize=8, 
                   label=labels.get(impl, impl))
        
        ax.set_xlabel('Message Size (bytes)', fontweight='bold')
        ax.set_ylabel('CPU Cycles per Byte', fontweight='bold')
        ax.set_title(f'{threads} Thread(s)', fontweight='bold')
        ax.set_xscale('log', base=2)
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    plt.tight_layout()
    plt.savefig('MT25067_Plot4_CPUCycles_per_Byte.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('MT25067_Plot4_CPUCycles_per_Byte.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot4_CPUCycles_per_Byte.pdf & .png")
    plt.close()

# Plot 5: Overall Comparison
def plot_overall_comparison(data, message_sizes, thread_counts, implementations):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    msg_size = max(message_sizes)
    
    fig.suptitle(f'Comprehensive Comparison - {msg_size}B Messages\nAll Metrics vs Thread Count', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    
    # Throughput
    for impl in implementations:
        vals = [data[impl].get(msg_size, {}).get(t, {}).get('throughput', 0) for t in thread_counts]
        ax1.plot(thread_counts, vals, marker=markers[impl], color=colors[impl],
                linewidth=2, markersize=8, label=impl)
    ax1.set_xlabel('Threads', fontweight='bold')
    ax1.set_ylabel('Throughput (Mbps)', fontweight='bold')
    ax1.set_title('Throughput', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Latency
    for impl in implementations:
        vals = [data[impl].get(msg_size, {}).get(t, {}).get('latency', 0) for t in thread_counts]
        ax2.plot(thread_counts, vals, marker=markers[impl], color=colors[impl],
                linewidth=2, markersize=8, label=impl)
    ax2.set_xlabel('Threads', fontweight='bold')
    ax2.set_ylabel('Latency (µs)', fontweight='bold')
    ax2.set_title('Latency', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # CPU Cycles
    for impl in implementations:
        vals = [data[impl].get(msg_size, {}).get(t, {}).get('cycles', 0) for t in thread_counts]
        ax3.plot(thread_counts, vals, marker=markers[impl], color=colors[impl],
                linewidth=2, markersize=8, label=impl)
    ax3.set_xlabel('Threads', fontweight='bold')
    ax3.set_ylabel('CPU Cycles (Millions)', fontweight='bold')
    ax3.set_title('CPU Cycles', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Cache Misses
    for impl in implementations:
        vals = [data[impl].get(msg_size, {}).get(t, {}).get('cache_misses', 0) for t in thread_counts]
        ax4.plot(thread_counts, vals, marker=markers[impl], color=colors[impl],
                linewidth=2, markersize=8, label=impl)
    ax4.set_xlabel('Threads', fontweight='bold')
    ax4.set_ylabel('Cache Misses', fontweight='bold')
    ax4.set_title('LLC Cache Misses', fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('MT25067_Plot5_Overall_Comparison.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('MT25067_Plot5_Overall_Comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot5_Overall_Comparison.pdf & .png")
    plt.close()

def main():
    print("=" * 60)
    print("MT25067 - Part D: Dynamic Plotting from CSV Data")
    print("=" * 60)
    print(f"System Configuration:\n{SYSTEM_CONFIG}")
    
    # Find CSV file
    csv_file = find_csv_file()
    if not csv_file:
        print("\nERROR: CSV file not found!")
        print("\nSearched locations:")
        print("  - experiment_results/MT25067_ExperimentData.csv")
        print("  - MT25067_ExperimentData.csv")
        print("  - experiment_results/MT25067_AllResults_*.csv")
        print("\nPlease run the automation script first:")
        print("  sudo bash MT25067_PartC_AutomationScript.sh")
        sys.exit(1)
    
    # Load and organize data
    df = load_data(csv_file)
    data = organize_data(df)
    
    message_sizes = sorted(df['MessageSize'].unique())
    thread_counts = sorted(df['NumThreads'].unique())
    implementations = sorted(df['Implementation'].unique())
    
    print(f"\nData summary:")
    print(f"  Implementations: {implementations}")
    print(f"  Message sizes: {message_sizes}")
    print(f"  Thread counts: {thread_counts}")
    print(f"  Total experiments: {len(df)}")
    print("\nGenerating plots...")
    print()
    
    plot_throughput_vs_message_size(data, message_sizes, thread_counts, implementations)
    plot_latency_vs_thread_count(data, message_sizes, thread_counts, implementations)
    plot_cache_misses_vs_message_size(data, message_sizes, implementations)
    plot_cpu_cycles_per_byte(data, message_sizes, thread_counts, implementations)
    plot_overall_comparison(data, message_sizes, thread_counts, implementations)
    
    print()
    print("=" * 60)
    print("All plots generated successfully!")
    print("=" * 60)
    print("\nGenerated files (PDF and PNG):")
    print("  1. MT25067_Plot1_Throughput_vs_MessageSize")
    print("  2. MT25067_Plot2_Latency_vs_ThreadCount")
    print("  3. MT25067_Plot3_CacheMisses_vs_MessageSize")
    print("  4. MT25067_Plot4_CPUCycles_per_Byte")
    print("  5. MT25067_Plot5_Overall_Comparison")
    print("\nPDFs for submission, PNGs for preview.")

if __name__ == "__main__":
    main()