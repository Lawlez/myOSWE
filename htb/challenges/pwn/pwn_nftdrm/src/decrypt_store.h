#ifndef DECRYPT_STORE_H
#define DECRYPT_STORE_H

#include <stdbool.h>
#include <stdint.h>

#include "nft_crypto.h"

#define MAX_QUEUE_SIZE 0x1000
#define PAGE_SIZE 4096

struct dec_queue;

struct buffer_node {    
    struct buffer_node *prev;
    struct buffer_node *next;
    int16_t size;
    int16_t r_off;
    int16_t w_off;
    struct dec_queue *owner;
    char buf[0];
};

typedef struct buffer_node buffer_node_t;

struct dec_queue
{
    uint16_t count;
    uint16_t max;
    buffer_node_t *head;
};

typedef struct dec_queue dec_queue_t;

bool initialize_queue(dec_queue_t *main_queue);
bool handle_encrypted(dec_queue_t *main_queue, aes_ctx *aes, uint8_t *buffer, int16_t size);
int16_t handle_decrypted(dec_queue_t *main_queue, uint8_t *buffer, int16_t size);
void destroy_queue(dec_queue_t *main_queue);
#endif