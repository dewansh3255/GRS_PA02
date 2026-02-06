#!/usr/bin/env python3
"""
MT25067
Part D: Plotting and Visualization
Uses HARDCODED experimental data (as per assignment constraints)
Generates PNG plots only.

System Configuration:
- OS: Ubuntu 22.04.5 LTS
- CPU: Intel Core i7-12700 (12th Gen)
- Date: February 6, 2026
"""

import matplotlib.pyplot as plt

# Set publication-quality plot style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 9)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10

# System configuration string for plot annotations
SYSTEM_CONFIG = """System: Ubuntu 22.04.5 LTS
CPU: Intel Core i7-12700 (12th Gen)
Kernel: 6.8.0-90-generic
Network: Localhost
Data: Feb 6, 2026"""

# =============================================================================
# HARDCODED EXPERIMENTAL DATA
# Data Source: MT25067_ExperimentData.csv
# =============================================================================
# Structure: data[implementation][message_size][num_threads] = {metrics}
# Note: 'cycles' are stored in Millions (1e6) to match plotting logic

# --- DATA START ---
data = {
    'A1': {
        256: {
            1: {'throughput': 3.04, 'latency': 0.67, 'total_bytes': 1280000, 'cycles': 13.445259, 'cache_misses': 48091, 'l1_misses': 0},
            2: {'throughput': 4.83, 'latency': 0.42, 'total_bytes': 1280000, 'cycles': 34.473639, 'cache_misses': 107581, 'l1_misses': 42229},
            4: {'throughput': 2.85, 'latency': 0.72, 'total_bytes': 1280000, 'cycles': 80.692819, 'cache_misses': 167366, 'l1_misses': 95676},
            8: {'throughput': 3.28, 'latency': 0.62, 'total_bytes': 1280000, 'cycles': 163.672988, 'cache_misses': 279810, 'l1_misses': 189220},
        },
        1024: {
            1: {'throughput': 10.18, 'latency': 0.80, 'total_bytes': 5120000, 'cycles': 35.466119, 'cache_misses': 272316, 'l1_misses': 98156},
            2: {'throughput': 9.93, 'latency': 0.83, 'total_bytes': 5120000, 'cycles': 29.057367, 'cache_misses': 83877, 'l1_misses': 0},
            4: {'throughput': 15.94, 'latency': 0.51, 'total_bytes': 5120000, 'cycles': 69.635497, 'cache_misses': 296016, 'l1_misses': 153774},
            8: {'throughput': 11.74, 'latency': 0.70, 'total_bytes': 5120000, 'cycles': 185.599832, 'cache_misses': 347469, 'l1_misses': 389281},
        },
        4096: {
            1: {'throughput': 26.93, 'latency': 1.22, 'total_bytes': 20480000, 'cycles': 47.296933, 'cache_misses': 385006, 'l1_misses': 133815},
            2: {'throughput': 39.28, 'latency': 0.83, 'total_bytes': 20480000, 'cycles': 87.429774, 'cache_misses': 170361, 'l1_misses': 446468},
            4: {'throughput': 42.26, 'latency': 0.78, 'total_bytes': 20480000, 'cycles': 150.723683, 'cache_misses': 337977, 'l1_misses': 805432},
            8: {'throughput': 31.31, 'latency': 1.05, 'total_bytes': 20480000, 'cycles': 312.424612, 'cache_misses': 515084, 'l1_misses': 1892391},
        },
        16384: {
            1: {'throughput': 55.01, 'latency': 2.38, 'total_bytes': 81920000, 'cycles': 96.778507, 'cache_misses': 227704, 'l1_misses': 1906161},
            2: {'throughput': 57.79, 'latency': 2.27, 'total_bytes': 81920000, 'cycles': 173.090097, 'cache_misses': 641179, 'l1_misses': 3580952},
            4: {'throughput': 53.76, 'latency': 2.44, 'total_bytes': 81920000, 'cycles': 439.397274, 'cache_misses': 849654, 'l1_misses': 8079184},
            8: {'throughput': 14.83, 'latency': 8.84, 'total_bytes': 81920000, 'cycles': 1433.697510, 'cache_misses': 3570756, 'l1_misses': 15436826},
        },
    },
    'A2': {
        256: {
            1: {'throughput': 2.82, 'latency': 0.73, 'total_bytes': 1280000, 'cycles': 31.000160, 'cache_misses': 81033, 'l1_misses': 36330},
            2: {'throughput': 1.95, 'latency': 1.05, 'total_bytes': 1280000, 'cycles': 82.981096, 'cache_misses': 508920, 'l1_misses': 238311},
            4: {'throughput': 3.04, 'latency': 0.67, 'total_bytes': 1280000, 'cycles': 93.651667, 'cache_misses': 312947, 'l1_misses': 77959},
            8: {'throughput': 1.93, 'latency': 1.06, 'total_bytes': 1280000, 'cycles': 233.051137, 'cache_misses': 143551, 'l1_misses': 223729},
        },
        1024: {
            1: {'throughput': 6.87, 'latency': 1.19, 'total_bytes': 5120000, 'cycles': 51.259757, 'cache_misses': 314740, 'l1_misses': 149176},
            2: {'throughput': 8.29, 'latency': 0.99, 'total_bytes': 5120000, 'cycles': 83.737078, 'cache_misses': 133642, 'l1_misses': 168817},
            4: {'throughput': 12.27, 'latency': 0.67, 'total_bytes': 5120000, 'cycles': 112.922852, 'cache_misses': 227870, 'l1_misses': 216215},
            8: {'throughput': 6.33, 'latency': 1.29, 'total_bytes': 5120000, 'cycles': 276.550440, 'cache_misses': 282747, 'l1_misses': 597803},
        },
        4096: {
            1: {'throughput': 25.39, 'latency': 1.29, 'total_bytes': 20480000, 'cycles': 55.436386, 'cache_misses': 132763, 'l1_misses': 250227},
            2: {'throughput': 18.49, 'latency': 1.77, 'total_bytes': 20480000, 'cycles': 142.512781, 'cache_misses': 458341, 'l1_misses': 487796},
            4: {'throughput': 31.12, 'latency': 1.05, 'total_bytes': 20480000, 'cycles': 185.842776, 'cache_misses': 210972, 'l1_misses': 922344},
            8: {'throughput': 18.93, 'latency': 1.73, 'total_bytes': 20480000, 'cycles': 450.771960, 'cache_misses': 411825, 'l1_misses': 2247370},
        },
        16384: {
            1: {'throughput': 50.66, 'latency': 2.59, 'total_bytes': 81920000, 'cycles': 106.168703, 'cache_misses': 244854, 'l1_misses': 1908667},
            2: {'throughput': 45.50, 'latency': 2.88, 'total_bytes': 81920000, 'cycles': 208.634114, 'cache_misses': 297486, 'l1_misses': 3922039},
            4: {'throughput': 56.69, 'latency': 2.31, 'total_bytes': 81920000, 'cycles': 412.122925, 'cache_misses': 581752, 'l1_misses': 8132604},
            8: {'throughput': 22.44, 'latency': 5.84, 'total_bytes': 81920000, 'cycles': 1204.466803, 'cache_misses': 1579839, 'l1_misses': 15065223},
        },
    },
    'A3': {
        256: {
            1: {'throughput': 0.68, 'latency': 3.00, 'total_bytes': 1280000, 'cycles': 200.385851, 'cache_misses': 248532, 'l1_misses': 540617},
            2: {'throughput': 0.68, 'latency': 3.02, 'total_bytes': 1280000, 'cycles': 405.358357, 'cache_misses': 244281, 'l1_misses': 871879},
            4: {'throughput': 0.51, 'latency': 4.03, 'total_bytes': 1280000, 'cycles': 745.013201, 'cache_misses': 519568, 'l1_misses': 1964699},
            8: {'throughput': 0.72, 'latency': 2.84, 'total_bytes': 1280000, 'cycles': 1518.821656, 'cache_misses': 594408, 'l1_misses': 5449859},
        },
        1024: {
            1: {'throughput': 2.57, 'latency': 3.19, 'total_bytes': 5120000, 'cycles': 228.857802, 'cache_misses': 161703, 'l1_misses': 870786},
            2: {'throughput': 3.01, 'latency': 2.72, 'total_bytes': 5120000, 'cycles': 345.559181, 'cache_misses': 382763, 'l1_misses': 1115208},
            4: {'throughput': 1.90, 'latency': 4.31, 'total_bytes': 5120000, 'cycles': 958.183842, 'cache_misses': 302208, 'l1_misses': 1919524},
            8: {'throughput': 2.12, 'latency': 3.87, 'total_bytes': 5120000, 'cycles': 1406.978895, 'cache_misses': 579158, 'l1_misses': 6077581},
        },
        4096: {
            1: {'throughput': 8.82, 'latency': 3.72, 'total_bytes': 20480000, 'cycles': 249.534073, 'cache_misses': 182509, 'l1_misses': 569753},
            2: {'throughput': 8.31, 'latency': 3.94, 'total_bytes': 20480000, 'cycles': 560.658122, 'cache_misses': 515538, 'l1_misses': 1223216},
            4: {'throughput': 0.75, 'latency': 43.52, 'total_bytes': 20480000, 'cycles': 1114.620739, 'cache_misses': 315330, 'l1_misses': 2154920},
            8: {'throughput': 7.23, 'latency': 4.53, 'total_bytes': 20480000, 'cycles': 1666.158940, 'cache_misses': 725607, 'l1_misses': 5442754},
        },
        16384: {
            1: {'throughput': 31.81, 'latency': 4.12, 'total_bytes': 81920000, 'cycles': 226.164438, 'cache_misses': 276298, 'l1_misses': 2260402},
            2: {'throughput': 26.89, 'latency': 4.87, 'total_bytes': 81920000, 'cycles': 734.872334, 'cache_misses': 431502, 'l1_misses': 3654525},
            4: {'throughput': 26.50, 'latency': 4.95, 'total_bytes': 81920000, 'cycles': 1210.556301, 'cache_misses': 1150586, 'l1_misses': 8156958},
            8: {'throughput': 20.88, 'latency': 6.28, 'total_bytes': 81920000, 'cycles': 2591.150000, 'cache_misses': 1300194, 'l1_misses': 16857506},
        },
    },
}
# --- DATA END ---

# Experimental parameters
MESSAGE_SIZES = [256, 1024, 4096, 16384]
THREAD_COUNTS = [1, 2, 4, 8]
IMPLEMENTATIONS = ['A1', 'A2', 'A3']

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def add_footer(fig):
    """Adds a standard footer with system configuration to the figure."""
    # Reserve space at the bottom (left, bottom, right, top)
    fig.subplots_adjust(bottom=0.15)
    
    # Add text in the reserved space
    fig.text(0.5, 0.04, SYSTEM_CONFIG, 
             ha='center', va='center', fontsize=10, 
             bbox=dict(facecolor='#f0f0f0', edgecolor='gray', boxstyle='round,pad=0.5', alpha=0.8))
    
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
                ax.annotate(f'{thr:.1f}', (size, thr),  # Changed to 1 decimal for Gbps
                           textcoords="offset points", xytext=(0,5), 
                           ha='center', fontsize=8)
        
        ax.set_xlabel('Message Size (bytes)', fontweight='bold')
        ax.set_ylabel('Throughput (Gbps)', fontweight='bold') # <--- FIXED HERE
        ax.set_title(f'{threads} Thread(s)', fontweight='bold')
        ax.set_xscale('log', base=2)
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    add_footer(fig)

    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
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
        
    add_footer(fig)
    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
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

    add_footer(fig)
    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
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
    
    add_footer(fig)
    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
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
    ax1.set_ylabel('Throughput (Gbps)', fontweight='bold') # <--- FIXED HERE
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
    
    add_footer(fig)
    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
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
    print("Data extracted from valid experimental run (Millions of cycles)")
    print("=" * 70)
    
    print(f"\nData summary:")
    print(f"  Implementations: {IMPLEMENTATIONS}")
    print(f"  Message sizes: {MESSAGE_SIZES} bytes")
    print(f"  Thread counts: {THREAD_COUNTS}")
    
    print("\nGenerating plots...")
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

if __name__ == "__main__":
    main()