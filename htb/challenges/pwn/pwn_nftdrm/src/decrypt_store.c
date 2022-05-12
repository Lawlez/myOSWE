#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <string.h>
#include <glib.h>
#include <stdio.h>

#include "decrypt_store.h"
#include "nft_crypto.h"

#pragma GCC push_options
#pragma GCC optimize ("O0")

static const char corruption[] = "CORRUPTED INTERNAL LINKED LIST IN DRM";

int16_t get_alloc_size(int16_t size);

int16_t get_alloc_size(int16_t size)
{
    size--;
    size |= size >> 1;
    size |= size >> 2;
    size |= size >> 4;
    size |= size >> 8;
    size++;
    return (size < 256)?256:size;
}

bool initialize_queue(dec_queue_t *main_queue)
{
    buffer_node_t *node;
    node = g_malloc(PAGE_SIZE);
    if (!node) 
        return false;
    node->next = node;
    node->prev = node;
    node->owner = main_queue;
    node->size = PAGE_SIZE - offsetof(buffer_node_t, buf);
    node->w_off = 0;
    node->r_off = 0;
    main_queue->max = MAX_QUEUE_SIZE;
    main_queue->count = 1;
    main_queue->head = node;
    return true;
}

bool handle_encrypted(dec_queue_t *main_queue, aes_ctx *aes, uint8_t *buffer, int16_t size)
{
    buffer_node_t *new_node, *curr, *prev;
    int16_t new_node_size;
    uint8_t local_buf[PAGE_SIZE] = {0};
    uint8_t padding;
    int16_t curr_size;
    int16_t curr_w_off;

    if (size > 4096 - offsetof(buffer_node_t, buf) || size < 0)
        return false;
    
    if (size % 16)
        return false;

    curr = main_queue->head;
    curr_size = curr->size;
    curr_w_off = curr->w_off;

    if (size > curr_size - curr_w_off)
    {
        memcpy(local_buf, buffer, size);
        aes_decrypt(aes, (uint8_t*)local_buf, size);
        padding = verify_PKCS7_padding((uint8_t*)local_buf, size);
        if (!padding)
            return false;

        size -= padding;

        if (size > curr_size - curr_w_off)
        {
            if (main_queue->count == MAX_QUEUE_SIZE)
                return false;

            int16_t remaining = curr_size - curr_w_off;
            int16_t to_add = size - remaining;
            new_node_size = get_alloc_size(to_add + sizeof(buffer_node_t));

            new_node = g_malloc(new_node_size);

            if (!new_node)
                return false;

            memcpy(&curr->buf[curr_w_off], local_buf, remaining);
            curr->w_off = curr_size;

            new_node->owner = main_queue;
            new_node->r_off = 0;
            new_node->w_off = 0;
            new_node->size = new_node_size - offsetof(buffer_node_t, buf);
            new_node->prev = curr->prev;
            new_node->next = curr;

            prev = curr->prev;
            prev->next = new_node;
            curr->prev = new_node;

            main_queue->head = new_node;
            main_queue->count++;

            memcpy(&new_node->buf[new_node->w_off], &local_buf[remaining], to_add);

            new_node->w_off = to_add;
        }
        else
        {
            memcpy(&curr->buf[curr_w_off], local_buf, size);
            curr->w_off += size;
        }
    } 
    else
    {
        memcpy(&curr->buf[curr_w_off], buffer, size);
        aes_decrypt(aes, (uint8_t*)&curr->buf[curr_w_off], size);
        padding = verify_PKCS7_padding((uint8_t*)&curr->buf[curr_w_off], size);
        if (!padding)
            return false;
        curr->w_off += size;
        curr->w_off -= padding;
    }
    return true;
}

int16_t handle_decrypted(dec_queue_t *main_queue, uint8_t *buffer, int16_t size)
{
    char local_buf[PAGE_SIZE] = {0};
    buffer_node_t *curr, *prev, *next;
    int i = 0; 
    int counter = 0;

    if (size > PAGE_SIZE || size < 0)
        return 0;

    curr = main_queue->head->prev;

    while (counter < size && counter < sizeof(local_buf))
    {
        if (curr->r_off < curr->w_off)
        {
            local_buf[i++] = curr->buf[curr->r_off++];
            counter++;
        }
        if (curr->r_off == curr->w_off)
        {
            if (main_queue->count == 1)
            {
                break;
            }
            else
            {
                prev = curr->prev;
                if (prev->next != curr)
                {
                    puts(corruption);
                    abort();
                }
                prev->next = curr->next;
                next = curr->next;
                if (next->prev != curr)
                {
                    puts(corruption);
                    abort();
                }
                next->prev = prev;

                g_free(curr);

                main_queue->head = next;
                main_queue->count--;
               
                curr = prev;
            }
        }
    }
    memcpy(buffer, local_buf, counter);
    return counter;
}

void destroy_queue(dec_queue_t *main_queue)
{
    buffer_node_t *curr, *prev, *next;
    
    while (main_queue->count > 1)
    {
        curr = main_queue->head->prev;
        prev = curr->prev;
        if (prev->next != curr)
        {
            puts(corruption);
            abort();
        }
        prev->next = curr->next;
        next = curr->next;
        if (next->prev != curr)
        {
            puts(corruption);
            abort();
        }
        next->prev = prev;

        g_free(curr);

        main_queue->head = next;
        main_queue->count--;

    }
    curr = main_queue->head;
    g_free(curr);
    main_queue->head = NULL;
    return;
}

#pragma GCC pop_options