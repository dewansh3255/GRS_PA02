/*
 * MT25067
 * Part A1: Two-Copy TCP Server (Baseline)
 * Uses send()/recv() socket primitives
 * Multithreaded - one thread per client
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <sys/time.h>
#include <errno.h>

#define PORT 8080
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
    
    // Allocate each field on heap
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
 * Serialize message into a buffer for sending
 * Format: field1|field2|field3|...|field8
 */
int serialize_message(Message *msg, char *buffer, int buffer_size) {
    int offset = 0;
    int field_size = buffer_size / NUM_STRING_FIELDS;
    
    memcpy(buffer + offset, msg->field1, field_size);
    offset += field_size;
    memcpy(buffer + offset, msg->field2, field_size);
    offset += field_size;
    memcpy(buffer + offset, msg->field3, field_size);
    offset += field_size;
    memcpy(buffer + offset, msg->field4, field_size);
    offset += field_size;
    memcpy(buffer + offset, msg->field5, field_size);
    offset += field_size;
    memcpy(buffer + offset, msg->field6, field_size);
    offset += field_size;
    memcpy(buffer + offset, msg->field7, field_size);
    offset += field_size;
    memcpy(buffer + offset, msg->field8, field_size);
    offset += field_size;
    
    return offset;
}

/*
 * Client handler thread
 * Sends messages repeatedly to the client
 */
void* handle_client(void *arg) {
    ThreadArgs *args = (ThreadArgs*)arg;
    int client_fd = args->client_fd;
    int message_size = args->message_size;
    int num_messages = args->num_messages;
    
    printf("[Thread %lu] Handling client, sending %d messages of %d bytes\n",
           pthread_self(), num_messages, message_size);
    
    // Create message
    Message *msg = create_message(message_size);
    if (!msg) {
        close(client_fd);
        free(args);
        return NULL;
    }
    
    // Buffer for serialized message
    char *send_buffer = (char*)malloc(message_size);
    if (!send_buffer) {
        destroy_message(msg);
        close(client_fd);
        free(args);
        return NULL;
    }
    
    // Serialize once (reuse for all sends)
    serialize_message(msg, send_buffer, message_size);
    
    struct timeval start, end;
    gettimeofday(&start, NULL);
    
    // Send messages repeatedly
    long bytes_sent_total = 0;
    for (int i = 0; i < num_messages; i++) {
        // TWO-COPY: send() copies from user buffer to kernel socket buffer
        ssize_t sent = send(client_fd, send_buffer, message_size, 0);
        if (sent < 0) {
            perror("send");
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
    free(send_buffer);
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
    
    printf("=== Part A1: Two-Copy Server ===\n");
    printf("Message size: %d bytes\n", message_size);
    printf("Messages per client: %d\n", num_messages);
    printf("Max clients: %d\n", max_clients);
    
    int server_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len = sizeof(client_addr);
    
    // Create socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket");
        exit(1);
    }
    
    // SO_REUSEADDR to avoid "Address already in use" error
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    
    // Bind
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    if (inet_pton(AF_INET, "10.0.0.1", &server_addr.sin_addr) <= 0) {
        perror("inet_pton");
        exit(1);
    }    
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
    
    // Simple wait (in production, use barriers or condition variables)
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