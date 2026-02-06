#!/usr/bin/env python3
"""
MT25067
Part D: Plotting and Visualization
Uses HARDCODED experimental data (no CSV reading as per assignment requirement)
Generates PNG plots only (no PDF)

System Configuration:
- OS: Ubuntu 22.04.5 LTS (Jammy)
- Kernel: 6.8.0-90-generic
- CPU: Intel Core i7-12700 (12th Gen)
- Network: Localhost (127.0.0.1)
- Date: February 6, 2026
"""

import matplotlib.pyplot as plt

# Set publication-quality plot style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10

# System configuration string for plot annotations
SYSTEM_CONFIG = """System: Ubuntu 22.04.5 LTS
CPU: Intel Core i7-12700 (12th Gen)
Kernel: 6.8.0-90-generic
Network: Localhost (127.0.0.1)
Date: February 6, 2026"""

# =============================================================================
# HARDCODED EXPERIMENTAL DATA
# Data extracted from fresh experimental run on February 6, 2026
# =============================================================================
# Structure: data[implementation][message_size][num_threads] = {metrics}

data = {
    'A1': {
        256: {
            1: {'throughput': 1914.02, 'latency': 1.07, 'total_bytes': 256000,
                'cycles': 10/1e6, 'cache_misses': 91, 'l1_misses': 31},
            2: {'throughput': 1826.94, 'latency': 1.12, 'total_bytes': 256000,
                'cycles': 12/1e6, 'cache_misses': 161, 'l1_misses': 17},
            4: {'throughput': 1892.79, 'latency': 1.08, 'total_bytes': 256000,
                'cycles': 24/1e6, 'cache_misses': 117, 'l1_misses': 44},
            8: {'throughput': 1988.35, 'latency': 1.03, 'total_bytes': 256000,
                'cycles': 45/1e6, 'cache_misses': 163, 'l1_misses': 72}
        },
        1024: {
            1: {'throughput': 7204.93, 'latency': 1.14, 'total_bytes': 1024000,
                'cycles': 11/1e6, 'cache_misses': 108, 'l1_misses': 33},
            2: {'throughput': 6775.85, 'latency': 1.21, 'total_bytes': 1024000,
                'cycles': 17/1e6, 'cache_misses': 119, 'l1_misses': 40},
            4: {'throughput': 6770.25, 'latency': 1.21, 'total_bytes': 1024000,
                'cycles': 29/1e6, 'cache_misses': 143, 'l1_misses': 80},
            8: {'throughput': 6965.99, 'latency': 1.18, 'total_bytes': 1024000,
                'cycles': 54/1e6, 'cache_misses': 157, 'l1_misses': 146}
        },
        4096: {
            1: {'throughput': 19298.00, 'latency': 1.70, 'total_bytes': 4096000,
                'cycles': 15/1e6, 'cache_misses': 157, 'l1_misses': 41},
            2: {'throughput': 19207.50, 'latency': 1.71, 'total_bytes': 4096000,
                'cycles': 27/1e6, 'cache_misses': 221, 'l1_misses': 69},
            4: {'throughput': 19051.16, 'latency': 1.72, 'total_bytes': 4096000,
                'cycles': 45/1e6, 'cache_misses': 156, 'l1_misses': 234},
            8: {'throughput': 25680.25, 'latency': 1.28, 'total_bytes': 4096000,
                'cycles': 79/1e6, 'cache_misses': 247, 'l1_misses': 433}
        },
        16384: {
            1: {'throughput': 53564.36, 'latency': 2.45, 'total_bytes': 16384000,
                'cycles': 22/1e6, 'cache_misses': 170, 'l1_misses': 439},
            2: {'throughput': 27507.24, 'latency': 4.76, 'total_bytes': 16384000,
                'cycles': 72/1e6, 'cache_misses': 493, 'l1_misses': 333},
            4: {'throughput': 51643.81, 'latency': 2.54, 'total_bytes': 16384000,
                'cycles': 78/1e6, 'cache_misses': 419, 'l1_misses': 1},
            8: {'throughput': 34177.84, 'latency': 3.83, 'total_bytes': 16384000,
                'cycles': 188/1e6, 'cache_misses': 461, 'l1_misses': 3}
        }
    },
    'A2': {
        256: {
            1: {'throughput': 1537.54, 'latency': 1.33, 'total_bytes': 256000,
                'cycles': 12/1e6, 'cache_misses': 97, 'l1_misses': 40},
            2: {'throughput': 1587.60, 'latency': 1.29, 'total_bytes': 256000,
                'cycles': 21/1e6, 'cache_misses': 160, 'l1_misses': 70},
            4: {'throughput': 1510.32, 'latency': 1.36, 'total_bytes': 256000,
                'cycles': 34/1e6, 'cache_misses': 107, 'l1_misses': 61},
            8: {'throughput': 1759.45, 'latency': 1.16, 'total_bytes': 256000,
                'cycles': 51/1e6, 'cache_misses': 113, 'l1_misses': 80}
        },
        1024: {
            1: {'throughput': 6989.76, 'latency': 1.17, 'total_bytes': 1024000,
                'cycles': 12/1e6, 'cache_misses': 87, 'l1_misses': 32},
            2: {'throughput': 8578.01, 'latency': 0.95, 'total_bytes': 1024000,
                'cycles': 16/1e6, 'cache_misses': 132, 'l1_misses': 35},
            4: {'throughput': 4508.53, 'latency': 1.82, 'total_bytes': 1024000,
                'cycles': 42/1e6, 'cache_misses': 140, 'l1_misses': 101},
            8: {'throughput': 5744.74, 'latency': 1.43, 'total_bytes': 1024000,
                'cycles': 72/1e6, 'cache_misses': 293, 'l1_misses': 192}
        },
        4096: {
            1: {'throughput': 17201.05, 'latency': 1.91, 'total_bytes': 4096000,
                'cycles': 18/1e6, 'cache_misses': 96, 'l1_misses': 54},
            2: {'throughput': 15226.77, 'latency': 2.15, 'total_bytes': 4096000,
                'cycles': 33/1e6, 'cache_misses': 270, 'l1_misses': 97},
            4: {'throughput': 15086.56, 'latency': 2.17, 'total_bytes': 4096000,
                'cycles': 51/1e6, 'cache_misses': 175, 'l1_misses': 253},
            8: {'throughput': 21236.55, 'latency': 1.54, 'total_bytes': 4096000,
                'cycles': 101/1e6, 'cache_misses': 249, 'l1_misses': 536}
        },
        16384: {
            1: {'throughput': 47801.60, 'latency': 2.74, 'total_bytes': 16384000,
                'cycles': 23/1e6, 'cache_misses': 152, 'l1_misses': 450},
            2: {'throughput': 39432.01, 'latency': 3.32, 'total_bytes': 16384000,
                'cycles': 48/1e6, 'cache_misses': 213, 'l1_misses': 896},
            4: {'throughput': 28419.77, 'latency': 4.61, 'total_bytes': 16384000,
                'cycles': 114/1e6, 'cache_misses': 154, 'l1_misses': 2},
            8: {'throughput': 30117.65, 'latency': 4.35, 'total_bytes': 16384000,
                'cycles': 223/1e6, 'cache_misses': 591, 'l1_misses': 3}
        }
    },
    'A3': {
        256: {
            1: {'throughput': 714.09, 'latency': 2.87, 'total_bytes': 256000,
                'cycles': 100/1e6, 'cache_misses': 186, 'l1_misses': 183},
            2: {'throughput': 628.80, 'latency': 3.26, 'total_bytes': 256000,
                'cycles': 446/1e6, 'cache_misses': 492, 'l1_misses': 352},
            4: {'throughput': 812.70, 'latency': 2.52, 'total_bytes': 256000,
                'cycles': 452/1e6, 'cache_misses': 245, 'l1_misses': 1},
            8: {'throughput': 768.19, 'latency': 2.67, 'total_bytes': 256000,
                'cycles': 704/1e6, 'cache_misses': 181, 'l1_misses': 2}
        },
        1024: {
            1: {'throughput': 2632.39, 'latency': 3.11, 'total_bytes': 1024000,
                'cycles': 89/1e6, 'cache_misses': 129, 'l1_misses': 254},
            2: {'throughput': 1722.09, 'latency': 4.76, 'total_bytes': 1024000,
                'cycles': 422/1e6, 'cache_misses': 219, 'l1_misses': 406},
            4: {'throughput': 1722.09, 'latency': 4.76, 'total_bytes': 1024000,
                'cycles': 781/1e6, 'cache_misses': 267, 'l1_misses': 886},
            8: {'throughput': 2131.67, 'latency': 3.84, 'total_bytes': 1024000,
                'cycles': 751/1e6, 'cache_misses': 421, 'l1_misses': 2}
        },
        4096: {
            1: {'throughput': 8625.43, 'latency': 3.80, 'total_bytes': 4096000,
                'cycles': 224/1e6, 'cache_misses': 517, 'l1_misses': 273},
            2: {'throughput': 8391.29, 'latency': 3.90, 'total_bytes': 4096000,
                'cycles': 171/1e6, 'cache_misses': 320, 'l1_misses': 470},
            4: {'throughput': 8287.30, 'latency': 3.95, 'total_bytes': 4096000,
                'cycles': 388/1e6, 'cache_misses': 182, 'l1_misses': 1},
            8: {'throughput': 10369.62, 'latency': 3.16, 'total_bytes': 4096000,
                'cycles': 902/1e6, 'cache_misses': 289, 'l1_misses': 3}
        },
        16384: {
            1: {'throughput': 22680.74, 'latency': 5.78, 'total_bytes': 16384000,
                'cycles': 234/1e6, 'cache_misses': 302, 'l1_misses': 338},
            2: {'throughput': 27386.54, 'latency': 4.79, 'total_bytes': 16384000,
                'cycles': 246/1e6, 'cache_misses': 470, 'l1_misses': 1},
            4: {'throughput': 28036.79, 'latency': 4.67, 'total_bytes': 16384000,
                'cycles': 366/1e6, 'cache_misses': 278, 'l1_misses': 2},
            8: {'throughput': 21711.45, 'latency': 6.04, 'total_bytes': 16384000,
                'cycles': 885/1e6, 'cache_misses': 562, 'l1_misses': 5}
        }
    }
}

# Experimental parameters
MESSAGE_SIZES = [256, 1024, 4096, 16384]
THREAD_COUNTS = [1, 2, 4, 8]
IMPLEMENTATIONS = ['A1', 'A2', 'A3']

# =============================================================================
# PLOTTING FUNCTIONS
# =============================================================================

def plot_throughput_vs_message_size():
    """Plot 1: Throughput vs Message Size for different thread counts"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Throughput vs Message Size\n(Different Thread Counts)', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    labels = {'A1': 'A1 (Two-Copy)', 'A2': 'A2 (One-Copy)', 'A3': 'A3 (Zero-Copy)'}
    
    for idx, threads in enumerate(THREAD_COUNTS):
        ax = axes[idx // 2, idx % 2]
        
        for impl in IMPLEMENTATIONS:
            throughputs = [data[impl][size][threads]['throughput'] 
                          for size in MESSAGE_SIZES]
            
            ax.plot(MESSAGE_SIZES, throughputs, 
                   marker=markers[impl], 
                   color=colors[impl],
                   linewidth=2, markersize=8, 
                   label=labels[impl])
            
            # Add value annotations
            for size, thr in zip(MESSAGE_SIZES, throughputs):
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
    plt.savefig('MT25067_Plot1_Throughput_vs_MessageSize.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot1_Throughput_vs_MessageSize.png")
    plt.close()

def plot_latency_vs_thread_count():
    """Plot 2: Latency vs Thread Count for different message sizes"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Latency vs Thread Count\n(Different Message Sizes)', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    labels = {'A1': 'A1 (Two-Copy)', 'A2': 'A2 (One-Copy)', 'A3': 'A3 (Zero-Copy)'}
    
    for idx, msg_size in enumerate(MESSAGE_SIZES):
        ax = axes[idx // 2, idx % 2]
        
        for impl in IMPLEMENTATIONS:
            latencies = [data[impl][msg_size][t]['latency'] 
                        for t in THREAD_COUNTS]
            
            ax.plot(THREAD_COUNTS, latencies, 
                   marker=markers[impl],
                   color=colors[impl],
                   linewidth=2, markersize=8, 
                   label=labels[impl])
        
        ax.set_xlabel('Number of Threads', fontweight='bold')
        ax.set_ylabel('Average Latency (µs)', fontweight='bold')
        ax.set_title(f'Message Size: {msg_size} bytes', fontweight='bold')
        ax.set_xticks(THREAD_COUNTS)
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    plt.tight_layout()
    plt.savefig('MT25067_Plot2_Latency_vs_ThreadCount.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot2_Latency_vs_ThreadCount.png")
    plt.close()

def plot_cache_misses_vs_message_size():
    """Plot 3: Cache Misses (LLC and L1) vs Message Size for 1 thread"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Cache Misses vs Message Size (1 Thread)', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    labels = {'A1': 'A1 (Two-Copy)', 'A2': 'A2 (One-Copy)', 'A3': 'A3 (Zero-Copy)'}
    threads = 1
    
    # LLC Cache Misses
    for impl in IMPLEMENTATIONS:
        cache_misses = [data[impl][size][threads]['cache_misses'] 
                       for size in MESSAGE_SIZES]
        ax1.plot(MESSAGE_SIZES, cache_misses, 
                marker=markers[impl],
                color=colors[impl],
                linewidth=2, markersize=8, 
                label=labels[impl])
    
    ax1.set_xlabel('Message Size (bytes)', fontweight='bold')
    ax1.set_ylabel('LLC Cache Misses', fontweight='bold')
    ax1.set_title('Last Level Cache Misses', fontweight='bold')
    ax1.set_xscale('log', base=2)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # L1 Cache Misses
    for impl in IMPLEMENTATIONS:
        l1_misses = [data[impl][size][threads]['l1_misses'] 
                    for size in MESSAGE_SIZES]
        ax2.plot(MESSAGE_SIZES, l1_misses, 
                marker=markers[impl],
                color=colors[impl],
                linewidth=2, markersize=8, 
                label=labels[impl])
    
    ax2.set_xlabel('Message Size (bytes)', fontweight='bold')
    ax2.set_ylabel('L1 D-Cache Misses', fontweight='bold')
    ax2.set_title('L1 Data Cache Misses', fontweight='bold')
    ax2.set_xscale('log', base=2)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('MT25067_Plot3_CacheMisses_vs_MessageSize.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot3_CacheMisses_vs_MessageSize.png")
    plt.close()

def plot_cpu_cycles_per_byte():
    """Plot 4: CPU Cycles per Byte Transferred for different thread counts"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('CPU Cycles per Byte Transferred\n(Different Thread Counts)', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    labels = {'A1': 'A1 (Two-Copy)', 'A2': 'A2 (One-Copy)', 'A3': 'A3 (Zero-Copy)'}
    
    for idx, threads in enumerate(THREAD_COUNTS):
        ax = axes[idx // 2, idx % 2]
        
        for impl in IMPLEMENTATIONS:
            cpb = []
            for size in MESSAGE_SIZES:
                d = data[impl][size][threads]
                cycles = d['cycles'] * 1e6  # Convert back to actual cycles
                total_bytes = d['total_bytes']
                cpb.append(cycles / total_bytes if total_bytes > 0 else 0)
            
            ax.plot(MESSAGE_SIZES, cpb, 
                   marker=markers[impl],
                   color=colors[impl],
                   linewidth=2, markersize=8, 
                   label=labels[impl])
        
        ax.set_xlabel('Message Size (bytes)', fontweight='bold')
        ax.set_ylabel('CPU Cycles per Byte', fontweight='bold')
        ax.set_title(f'{threads} Thread(s)', fontweight='bold')
        ax.set_xscale('log', base=2)
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    plt.tight_layout()
    plt.savefig('MT25067_Plot4_CPUCycles_per_Byte.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot4_CPUCycles_per_Byte.png")
    plt.close()

def plot_overall_comparison():
    """Plot 5: Overall Comparison for largest message size (16KB)"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    msg_size = 16384
    
    fig.suptitle(f'Comprehensive Comparison - {msg_size}B Messages\nAll Metrics vs Thread Count', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    
    # Throughput
    for impl in IMPLEMENTATIONS:
        vals = [data[impl][msg_size][t]['throughput'] for t in THREAD_COUNTS]
        ax1.plot(THREAD_COUNTS, vals, marker=markers[impl], color=colors[impl],
                linewidth=2, markersize=8, label=impl)
    ax1.set_xlabel('Threads', fontweight='bold')
    ax1.set_ylabel('Throughput (Mbps)', fontweight='bold')
    ax1.set_title('Throughput', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(THREAD_COUNTS)
    
    # Latency
    for impl in IMPLEMENTATIONS:
        vals = [data[impl][msg_size][t]['latency'] for t in THREAD_COUNTS]
        ax2.plot(THREAD_COUNTS, vals, marker=markers[impl], color=colors[impl],
                linewidth=2, markersize=8, label=impl)
    ax2.set_xlabel('Threads', fontweight='bold')
    ax2.set_ylabel('Latency (µs)', fontweight='bold')
    ax2.set_title('Latency', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(THREAD_COUNTS)
    
    # CPU Cycles
    for impl in IMPLEMENTATIONS:
        vals = [data[impl][msg_size][t]['cycles'] for t in THREAD_COUNTS]
        ax3.plot(THREAD_COUNTS, vals, marker=markers[impl], color=colors[impl],
                linewidth=2, markersize=8, label=impl)
    ax3.set_xlabel('Threads', fontweight='bold')
    ax3.set_ylabel('CPU Cycles (Millions)', fontweight='bold')
    ax3.set_title('CPU Cycles', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_xticks(THREAD_COUNTS)
    
    # Cache Misses
    for impl in IMPLEMENTATIONS:
        vals = [data[impl][msg_size][t]['cache_misses'] for t in THREAD_COUNTS]
        ax4.plot(THREAD_COUNTS, vals, marker=markers[impl], color=colors[impl],
                linewidth=2, markersize=8, label=impl)
    ax4.set_xlabel('Threads', fontweight='bold')
    ax4.set_ylabel('Cache Misses', fontweight='bold')
    ax4.set_title('LLC Cache Misses', fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_xticks(THREAD_COUNTS)
    
    plt.tight_layout()
    plt.savefig('MT25067_Plot5_Overall_Comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot5_Overall_Comparison.png")
    plt.close()

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("=" * 70)
    print("MT25067 - Part D: Plotting and Visualization")
    print("=" * 70)
    print(SYSTEM_CONFIG)
    print("\n" + "=" * 70)
    print("Using HARDCODED experimental data (no CSV reading)")
    print("Data from fresh experimental run: February 6, 2026, 13:57")
    print("=" * 70)
    
    print(f"\nData summary:")
    print(f"  Implementations: {IMPLEMENTATIONS}")
    print(f"  Message sizes: {MESSAGE_SIZES} bytes")
    print(f"  Thread counts: {THREAD_COUNTS}")
    print(f"  Total data points: {len(IMPLEMENTATIONS) * len(MESSAGE_SIZES) * len(THREAD_COUNTS)}")
    
    print("\nGenerating PNG plots (no PDF)...")
    print()
    
    # Generate all plots
    plot_throughput_vs_message_size()
    plot_latency_vs_thread_count()
    plot_cache_misses_vs_message_size()
    plot_cpu_cycles_per_byte()
    plot_overall_comparison()
    
    print()
    print("=" * 70)
    print("All plots generated successfully!")
    print("=" * 70)
    print("\nGenerated files (PNG only):")
    print("  1. MT25067_Plot1_Throughput_vs_MessageSize.png")
    print("  2. MT25067_Plot2_Latency_vs_ThreadCount.png")
    print("  3. MT25067_Plot3_CacheMisses_vs_MessageSize.png")
    print("  4. MT25067_Plot4_CPUCycles_per_Byte.png")
    print("  5. MT25067_Plot5_Overall_Comparison.png")
    print("\n" + "=" * 70)
    print("SUBMISSION REMINDERS:")
    print("=" * 70)
    print("✅ Embed these PNG plots in your report PDF")
    print("❌ DO NOT include PNG files in your submission zip!")
    print("❌ DO NOT push PNG files to GitHub!")
    print("\nThe plots should ONLY appear embedded in your report.")
    print("After embedding plots in report, DELETE all .png files:")
    print("  $ rm -f MT25067_Plot*.png")
    print("=" * 70)

if __name__ == "__main__":
    main()