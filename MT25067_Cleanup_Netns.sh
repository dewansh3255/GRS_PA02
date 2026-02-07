#!/bin/bash
# MT25067
# Network Namespace Cleanup Script
# Removes network namespaces created for PA02

set -e

# Colors
GREEN='\033[0;32m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (sudo)"
    exit 1
fi

log_info "Cleaning up network namespaces..."

# Delete namespaces (this automatically removes veth pair)
ip netns del server_ns 2>/dev/null || true
ip netns del client_ns 2>/dev/null || true

log_info "✓ Cleanup complete!"