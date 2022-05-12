#ifndef NFT_CRYPTO_H
#define NFT_CRYPTO_H

#include <stdbool.h>

#include "aes.h"
#include "ecdh.h"

#define AES_KEY_SZ 16

typedef struct
{
    uint8_t pub[ECC_PUB_KEY_SIZE];
    uint8_t priv[ECC_PRV_KEY_SIZE];
    uint8_t secret[ECC_PUB_KEY_SIZE];
}ecc_t;

typedef struct AES_ctx aes_ctx;

typedef struct
{
    ecc_t ecc;
    aes_ctx aes;
}drmkey_t;

bool initialize_ecdh(ecc_t *ecc);
bool initialize_secret(ecc_t *ecc, uint8_t *dest, uint8_t *other_pub);
void retrieve_aes_key(uint8_t *emsg, ecc_t *ecc, aes_ctx *aes);

void aes_decrypt(aes_ctx *aes, uint8_t *buffer, size_t buf_len);
uint8_t verify_PKCS7_padding(uint8_t *buf, int16_t size);
#endif