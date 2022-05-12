#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>

#include "nft_crypto.h"

bool initialize_ecdh(ecc_t *ecc)
{
    int fd = open("/dev/urandom", O_RDONLY);
    if (fd < 0)
        return false;
    int nread = read(fd, ecc->priv, ECC_PRV_KEY_SIZE);
    if (nread != ECC_PRV_KEY_SIZE)
        return false;
    close(fd);
    if (ecdh_generate_keys(ecc->pub, ecc->priv))
    {
        return true;
    }
    return false;
}

#pragma GCC push_options
#pragma GCC optimize ("O0")

bool initialize_secret(ecc_t *ecc, uint8_t *dest, uint8_t *other_pub)
{
    if (ecdh_shared_secret(ecc->priv, other_pub, ecc->secret))
    {
        memcpy(dest, ecc->pub, ECC_PUB_KEY_SIZE);
        return true;
    }
    return false;
}

void retrieve_aes_key(uint8_t *emsg, ecc_t *ecc, aes_ctx *aes)
{
    uint8_t xchg_key_iv[AES_KEY_SZ * 2] = {0};
    uint8_t aes_key_iv[AES_KEY_SZ * 2] = {0};

    aes_ctx secret;

    memcpy(xchg_key_iv, ecc->secret, AES_KEY_SZ * 2);
    AES_init_ctx_iv(&secret, xchg_key_iv, xchg_key_iv+AES_KEY_SZ);
    memcpy(aes_key_iv, emsg, AES_KEY_SZ * 2);

    AES_CBC_decrypt_buffer(&secret, aes_key_iv, AES_KEY_SZ * 2);
    AES_init_ctx_iv(aes, aes_key_iv, aes_key_iv + AES_KEY_SZ);
    return;
}

void aes_decrypt(aes_ctx *aes, uint8_t *buffer, size_t buf_len)
{
    AES_CBC_decrypt_buffer(aes, buffer, buf_len);
    return;
}

uint8_t verify_PKCS7_padding(uint8_t *buf, int16_t size)
{
    uint8_t *padding_block = buf + size - 1;

    if (*padding_block < 1 || *padding_block > 16)
        return 0;
    uint8_t expected = *padding_block;
    for (int i = 0; i < expected && padding_block - i >= buf; i++)
    {
        if (padding_block[-i] != expected)
            return 0;
    }
    return expected;
}

#pragma GCC pop_options