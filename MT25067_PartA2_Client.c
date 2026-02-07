/*
 * MT25067
 * Part A2: One-Copy TCP Client
 * Uses recvmsg() with iovec (can also demonstrate scatter-gather on receive)
 * For simplicity, uses standard recv() since receive-side optimization is less critical
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/time.h>

#define PORT 8081  // Match Part A2 server port
#define SERVER_IP "10.0.0.1"

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <message_size> <num_messages>\n", argv[0]);
        fprintf(stderr, "Example: %s 1024 10000\n", argv[0]);
        exit(1);
    }
    
    int message_size = atoi(argv[1]);
    int num_messages = atoi(argv[2]);
    
    printf("=== Part A2: One-Copy Client ===\n");
    printf("Expecting %d messages of %d bytes\n", num_messages, message_size);
    
    int sock_fd;
    struct sockaddr_in server_addr;
    
    // Create socket
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd < 0) {
        perror("socket");
        exit(1);
    }
    
    // Configure server address
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    
    if (inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr) <= 0) {
        perror("inet_pton");
        exit(1);
    }
    
    // Connect to server
    if (connect(sock_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect");
        exit(1);
    }
    
    printf("Connected to server at %s:%d\n", SERVER_IP, PORT);
    
    // Allocate receive buffer
    char *recv_buffer = (char*)malloc(message_size);
    if (!recv_buffer) {
        perror("malloc");
        exit(1);
    }
    
    struct timeval start, end;
    gettimeofday(&start, NULL);
    
    long total_bytes_received = 0;
    int messages_received = 0;
    
    // Receive messages
    while (messages_received < num_messages) {
        int bytes_to_recv = message_size;
        int total_recv = 0;
        
        // recv() may not receive all bytes in one call
        while (total_recv < bytes_to_recv) {
            ssize_t received = recv(sock_fd, recv_buffer + total_recv,
                                   bytes_to_recv - total_recv, 0);
            
            if (received < 0) {
                perror("recv");
                goto cleanup;
            } else if (received == 0) {
                // Connection closed
                printf("Server closed connection\n");
                goto cleanup;
            }
            
            total_recv += received;
        }
        
        total_bytes_received += total_recv;
        messages_received++;
        
        // Print progress every 1000 messages
        if (messages_received % 1000 == 0) {
            printf("Received %d messages...\n", messages_received);
        }
    }
    
    gettimeofday(&end, NULL);
    double elapsed = (end.tv_sec - start.tv_sec) + 
                     (end.tv_usec - start.tv_usec) / 1e6;
    
    // Calculate metrics
    double throughput_mbps = (total_bytes_received * 8.0) / (elapsed * 1e6);
    double avg_latency_us = (elapsed * 1e6) / messages_received;
    
    printf("\n=== Results ===\n");
    printf("Messages received: %d\n", messages_received);
    printf("Total bytes: %ld\n", total_bytes_received);
    printf("Time elapsed: %.3f sec\n", elapsed);
    printf("Throughput: %.2f Mbps\n", throughput_mbps);
    printf("Average latency: %.2f µs\n", avg_latency_us);
    
cleanup:
    free(recv_buffer);
    close(sock_fd);
    
    return 0;
}