#!/bin/bash
# MT25067
# Network Namespace Setup Script - IMPROVED VERSION
# Creates isolated network namespaces connected via veth pair
# This provides real network stack (as required by assignment)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    log_error "Please run as root (sudo)"
    exit 1
fi

log_info "Setting up network namespaces for PA02..."
echo ""

# Cleanup any existing setup
log_info "Cleaning up existing namespaces (if any)..."
ip netns del server_ns 2>/dev/null || true
ip netns del client_ns 2>/dev/null || true
sleep 1

# Create namespaces
log_info "Creating network namespaces..."
ip netns add server_ns
ip netns add client_ns
log_debug "Created: server_ns, client_ns"

# Create veth pair (virtual ethernet cable)
log_info "Creating veth pair..."
ip link add veth_server type veth peer name veth_client
log_debug "Created: veth_server <-> veth_client"

# Move veth endpoints to respective namespaces
log_info "Moving veth endpoints to namespaces..."
ip link set veth_server netns server_ns
ip link set veth_client netns client_ns
log_debug "Moved endpoints to namespaces"

# Configure IP addresses
log_info "Configuring IP addresses..."
ip netns exec server_ns ip addr add 10.0.0.1/24 dev veth_server
ip netns exec client_ns ip addr add 10.0.0.2/24 dev veth_client
log_debug "Server: 10.0.0.1/24, Client: 10.0.0.2/24"

# Bring up interfaces
log_info "Bringing up interfaces..."
ip netns exec server_ns ip link set dev veth_server up
ip netns exec client_ns ip link set dev veth_client up
ip netns exec server_ns ip link set dev lo up
ip netns exec client_ns ip link set dev lo up
log_debug "All interfaces up"

# Add routes (for completeness)
log_info "Adding routes..."
ip netns exec server_ns ip route add default via 10.0.0.2 dev veth_server 2>/dev/null || true
ip netns exec client_ns ip route add default via 10.0.0.1 dev veth_client 2>/dev/null || true

# Verify connectivity
echo ""
log_info "Verifying connectivity..."
echo -n "  Ping test (client -> server): "
if ip netns exec client_ns ping -c 2 -W 2 10.0.0.1 >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Success${NC}"
else
    echo -e "${RED}✗ Failed${NC}"
    log_error "Connectivity test failed!"
    exit 1
fi

echo -n "  Ping test (server -> client): "
if ip netns exec server_ns ping -c 2 -W 2 10.0.0.2 >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Success${NC}"
else
    echo -e "${RED}✗ Failed${NC}"
    log_error "Connectivity test failed!"
    exit 1
fi

# Display configuration
echo ""
log_info "=========================================="
log_info "Network namespaces configured successfully!"
log_info "=========================================="
echo ""
echo "Configuration:"
echo "  Server namespace: server_ns"
echo "    - IP: 10.0.0.1/24"
echo "    - Interface: veth_server"
echo ""
echo "  Client namespace: client_ns"
echo "    - IP: 10.0.0.2/24"
echo "    - Interface: veth_client"
echo ""
echo "  Connection: veth pair (virtual ethernet)"
echo ""
echo "Usage examples:"
echo "  Server: sudo ip netns exec server_ns ./MT25067_PartA1_Server 4096 5000 1"
echo "  Client: sudo ip netns exec client_ns ./MT25067_PartA1_Client 4096 5000"
echo ""
echo "  Or run automated tests:"
echo "    sudo ./MT25067_PartC_AutomationScript.sh"
echo ""
echo "To cleanup:"
echo "  sudo ./MT25067_Cleanup_Netns.sh"
echo ""

# Verify namespaces exist
log_info "Verification:"
echo ""
echo "Namespaces:"
sudo ip netns list | sed 's/^/  /'
echo ""
echo "Server namespace interfaces:"
sudo ip netns exec server_ns ip addr show | grep -E "inet |UP|veth" | sed 's/^/  /'
echo ""
echo "Client namespace interfaces:"
sudo ip netns exec client_ns ip addr show | grep -E "inet |UP|veth" | sed 's/^/  /'
echo ""

log_info "✓ Setup complete! Ready for experiments."