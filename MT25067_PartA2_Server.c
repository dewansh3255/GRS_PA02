/*
 * MT25067
 * Part A2: One-Copy TCP Server
 * Uses sendmsg() with iovec (scatter-gather I/O)
 * Eliminates user-space serialization copy
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/uio.h>
#include <sys/time.h>
#include <errno.h>

#define PORT 8081  // Different port from A1
#define MAX_CLIENTS 100
#define NUM_STRING_FIELDS 8

// Message structure with 8 dynamically allocated string fields
typedef struct {
    char *field1;
    char *field2;
    char *field3;
    char *field4;
    char *field5;
    char *field6;
    char *field7;
    char *field8;
} Message;

// Thread arguments
typedef struct {
    int client_fd;
    int message_size;
    int num_messages;
} ThreadArgs;

// Global statistics
typedef struct {
    long total_bytes_sent;
    double total_time_sec;
    pthread_mutex_t lock;
} Stats;

Stats global_stats = {0, 0.0, PTHREAD_MUTEX_INITIALIZER};

/*
 * Allocate and initialize a message structure
 * Each field gets message_size/8 bytes (distributed equally)
 */
Message* create_message(int message_size) {
    Message *msg = (Message*)malloc(sizeof(Message));
    if (!msg) {
        perror("malloc message");
        return NULL;
    }
    
    int field_size = message_size / NUM_STRING_FIELDS;
    if (field_size < 1) field_size = 1;
    
    // Allocate each field on heap (scattered memory)
    msg->field1 = (char*)malloc(field_size);
    msg->field2 = (char*)malloc(field_size);
    msg->field3 = (char*)malloc(field_size);
    msg->field4 = (char*)malloc(field_size);
    msg->field5 = (char*)malloc(field_size);
    msg->field6 = (char*)malloc(field_size);
    msg->field7 = (char*)malloc(field_size);
    msg->field8 = (char*)malloc(field_size);
    
    // Check allocations
    if (!msg->field1 || !msg->field2 || !msg->field3 || !msg->field4 ||
        !msg->field5 || !msg->field6 || !msg->field7 || !msg->field8) {
        perror("malloc fields");
        return NULL;
    }
    
    // Fill with dummy data
    memset(msg->field1, 'A', field_size - 1); msg->field1[field_size-1] = '\0';
    memset(msg->field2, 'B', field_size - 1); msg->field2[field_size-1] = '\0';
    memset(msg->field3, 'C', field_size - 1); msg->field3[field_size-1] = '\0';
    memset(msg->field4, 'D', field_size - 1); msg->field4[field_size-1] = '\0';
    memset(msg->field5, 'E', field_size - 1); msg->field5[field_size-1] = '\0';
    memset(msg->field6, 'F', field_size - 1); msg->field6[field_size-1] = '\0';
    memset(msg->field7, 'G', field_size - 1); msg->field7[field_size-1] = '\0';
    memset(msg->field8, 'H', field_size - 1); msg->field8[field_size-1] = '\0';
    
    return msg;
}

/*
 * Free message structure
 */
void destroy_message(Message *msg) {
    if (msg) {
        free(msg->field1);
        free(msg->field2);
        free(msg->field3);
        free(msg->field4);
        free(msg->field5);
        free(msg->field6);
        free(msg->field7);
        free(msg->field8);
        free(msg);
    }
}

/*
 * Setup iovec array for scatter-gather I/O
 * Each iovec points to one field (NO COPY!)
 */
void setup_iovec(Message *msg, struct iovec *iov, int field_size) {
    // Point each iovec directly to the malloc'd fields
    iov[0].iov_base = msg->field1;
    iov[0].iov_len = field_size;
    
    iov[1].iov_base = msg->field2;
    iov[1].iov_len = field_size;
    
    iov[2].iov_base = msg->field3;
    iov[2].iov_len = field_size;
    
    iov[3].iov_base = msg->field4;
    iov[3].iov_len = field_size;
    
    iov[4].iov_base = msg->field5;
    iov[4].iov_len = field_size;
    
    iov[5].iov_base = msg->field6;
    iov[5].iov_len = field_size;
    
    iov[6].iov_base = msg->field7;
    iov[6].iov_len = field_size;
    
    iov[7].iov_base = msg->field8;
    iov[7].iov_len = field_size;
}

/*
 * Client handler thread
 * Sends messages using sendmsg() with iovec (ONE-COPY)
 */
void* handle_client(void *arg) {
    ThreadArgs *args = (ThreadArgs*)arg;
    int client_fd = args->client_fd;
    int message_size = args->message_size;
    int num_messages = args->num_messages;
    int field_size = message_size / NUM_STRING_FIELDS;
    
    printf("[Thread %lu] Handling client, sending %d messages of %d bytes\n",
           pthread_self(), num_messages, message_size);
    
    // Create message (8 separate malloc'd buffers)
    Message *msg = create_message(message_size);
    if (!msg) {
        close(client_fd);
        free(args);
        return NULL;
    }
    
    // Setup iovec array (points to the 8 fields)
    struct iovec iov[NUM_STRING_FIELDS];
    setup_iovec(msg, iov, field_size);
    
    // Setup msghdr for sendmsg()
    struct msghdr msghdr;
    memset(&msghdr, 0, sizeof(msghdr));
    msghdr.msg_iov = iov;           // Array of buffers
    msghdr.msg_iovlen = NUM_STRING_FIELDS;  // Number of buffers
    
    struct timeval start, end;
    gettimeofday(&start, NULL);
    
    // Send messages repeatedly
    long bytes_sent_total = 0;
    for (int i = 0; i < num_messages; i++) {
        // ONE-COPY: sendmsg() gathers from 8 scattered buffers
        // Kernel reads directly from each field (no user-space copy!)
        ssize_t sent = sendmsg(client_fd, &msghdr, 0);
        
        if (sent < 0) {
            perror("sendmsg");
            break;
        }
        bytes_sent_total += sent;
    }
    
    gettimeofday(&end, NULL);
    double elapsed = (end.tv_sec - start.tv_sec) + 
                     (end.tv_usec - start.tv_usec) / 1e6;
    
    // Update global stats
    pthread_mutex_lock(&global_stats.lock);
    global_stats.total_bytes_sent += bytes_sent_total;
    global_stats.total_time_sec += elapsed;
    pthread_mutex_unlock(&global_stats.lock);
    
    printf("[Thread %lu] Sent %ld bytes in %.3f sec (%.2f Mbps)\n",
           pthread_self(), bytes_sent_total, elapsed,
           (bytes_sent_total * 8.0) / (elapsed * 1e6));
    
    // Cleanup
    destroy_message(msg);
    close(client_fd);
    free(args);
    
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <message_size> <num_messages> <max_clients>\n", argv[0]);
        fprintf(stderr, "Example: %s 1024 10000 4\n", argv[0]);
        exit(1);
    }
    
    int message_size = atoi(argv[1]);
    int num_messages = atoi(argv[2]);
    int max_clients = atoi(argv[3]);
    
    printf("=== Part A2: One-Copy Server (sendmsg + iovec) ===\n");
    printf("Message size: %d bytes\n", message_size);
    printf("Messages per client: %d\n", num_messages);
    printf("Max clients: %d\n", max_clients);
    printf("Optimization: Using scatter-gather I/O (eliminates serialization)\n");
    
    int server_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len = sizeof(client_addr);
    
    // Create socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket");
        exit(1);
    }
    
    // SO_REUSEADDR
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    
    // Bind
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);
    
    if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind");
        exit(1);
    }
    
    // Listen
    if (listen(server_fd, max_clients) < 0) {
        perror("listen");
        exit(1);
    }
    
    printf("Server listening on port %d...\n", PORT);
    
    pthread_t threads[MAX_CLIENTS];
    int client_count = 0;
    
    // Accept clients
    while (client_count < max_clients) {
        int client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &addr_len);
        if (client_fd < 0) {
            perror("accept");
            continue;
        }
        
        printf("Client %d connected\n", client_count + 1);
        
        // Create thread arguments
        ThreadArgs *args = (ThreadArgs*)malloc(sizeof(ThreadArgs));
        args->client_fd = client_fd;
        args->message_size = message_size;
        args->num_messages = num_messages;
        
        // Create thread
        if (pthread_create(&threads[client_count], NULL, handle_client, args) != 0) {
            perror("pthread_create");
            close(client_fd);
            free(args);
            continue;
        }
        
        pthread_detach(threads[client_count]);
        client_count++;
    }
    
    printf("All %d clients accepted. Waiting for transfers to complete...\n", client_count);
    
    // Simple wait
    sleep(5);
    
    // Print final statistics
    printf("\n=== Final Statistics ===\n");
    printf("Total bytes sent: %ld\n", global_stats.total_bytes_sent);
    printf("Total time: %.3f sec\n", global_stats.total_time_sec);
    if (global_stats.total_time_sec > 0) {
        printf("Average throughput: %.2f Mbps\n",
               (global_stats.total_bytes_sent * 8.0) / (global_stats.total_time_sec * 1e6));
    }
    
    close(server_fd);
    pthread_mutex_destroy(&global_stats.lock);
    
    return 0;
}