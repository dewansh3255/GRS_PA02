# MT25067
# Makefile for PA02 - Network I/O Analysis

CC = gcc
CFLAGS = -Wall -Wextra -O2 -pthread
LDFLAGS = -pthread

# Targets
ALL_SERVERS = MT25067_PartA1_Server MT25067_PartA2_Server MT25067_PartA3_Server
ALL_CLIENTS = MT25067_PartA1_Client MT25067_PartA2_Client MT25067_PartA3_Client

.PHONY: all clean part_a1 part_a2 part_a3

all: part_a1 part_a2
	@echo "Build complete. Use 'make part_a3' when ready."

# Part A1: Two-Copy (Baseline)
part_a1: MT25067_PartA1_Server MT25067_PartA1_Client

MT25067_PartA1_Server: MT25067_PartA1_Server.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

MT25067_PartA1_Client: MT25067_PartA1_Client.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Part A2: One-Copy (sendmsg)
part_a2: MT25067_PartA2_Server MT25067_PartA2_Client

MT25067_PartA2_Server: MT25067_PartA2_Server.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

MT25067_PartA2_Client: MT25067_PartA2_Client.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Part A3: Zero-Copy (MSG_ZEROCOPY)
part_a3: MT25067_PartA3_Server MT25067_PartA3_Client

MT25067_PartA3_Server: MT25067_PartA3_Server.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

MT25067_PartA3_Client: MT25067_PartA3_Client.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Clean all binaries
clean:
	rm -f $(ALL_SERVERS) $(ALL_CLIENTS)
	rm -f *.o
	@echo "Cleaned all binaries"

# Help
help:
	@echo "Available targets:"
	@echo "  make part_a1  - Build Part A1 (Two-Copy)"
	@echo "  make part_a2  - Build Part A2 (One-Copy)"
	@echo "  make part_a3  - Build Part A3 (Zero-Copy)"
	@echo "  make all      - Build Part A1 by default"
	@echo "  make clean    - Remove all binaries"