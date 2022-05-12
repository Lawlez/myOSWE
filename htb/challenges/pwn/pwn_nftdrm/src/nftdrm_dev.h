#ifndef NFTDRM_DEV_H
#define NFTDRM_DEV_H

#include <stdint.h>
#include <stdbool.h>

#include "hw/pci/pci.h"
#include "qom/object.h"
#include "qemu/module.h"

#include "decrypt_store.h"
#include "nft_crypto.h"

#define NFTDRM_VENDOR_ID 0x420
#define NFTDRM_DEVICE_ID 0x1337
#define NFTDRM_DEVICE_REVISION 0x3

#define MSI_REQUIRED 1

#define NFTDRM_OK 0
#define NFTDRM_BUG 1

#define ERROR_INT_INVALID_OFFSET 1
#define ERROR_INT_INVALID_SZ 2
#define ERROR_INT_INVALID_CMD 3
#define ERROR_INT_DMA_WRITE 4
#define ERROR_INT_DMA_READ 5

#define CMD_EXCHANGE 1
#define CMD_LOAD_AES 2
#define CMD_HANDLE_ENCRYPT 3
#define CMD_HANDLE_DECRYPT 4
#define CMD_RELOAD 5
#define CMD_INITIALIZE_QUEUE 6

#define TYPE_PCI_NFTDRM_DEV "nftdrm"

typedef struct {
    uint8_t error;
    uint8_t command;
    uint16_t ret_val;
    uint8_t state;
    uint64_t enc_buf;
    uint64_t dec_buf;
    uint64_t xchg_buf;
    uint16_t enc_size;
    uint16_t dec_size;
} nftdrm_io_t;

typedef struct {
    PCIDevice pdev;
    
    MemoryRegion mmio;

    nftdrm_io_t *device_io;
    
    drmkey_t drmkey;

    dec_queue_t main_queue;

    uint8_t *xchg_dma;
    uint8_t *enc_dma;
    uint8_t *dec_dma;

    QemuMutex lock;

    bool queue_ready;
    bool recieved_pubkey;
    bool recieved_aes;

} pci_nftdrm_t;

static void pci_nftdrm_register_types(void);
static void pci_nftdrm_instance_init(Object *obj);
static void pci_nftdrm_class_init(ObjectClass *klass, void *data);

static void pci_nftdrm_realize(PCIDevice *pdev, Error **errp);
static void pci_nftdrm_exit(PCIDevice *pdev);

static uint64_t pci_nftdrm_mmio_read(void *opaque, hwaddr addr, unsigned size);
static void pci_nftdrm_mmio_write(void *opaque, hwaddr addr, uint64_t val, unsigned size);

static void pci_nftdrm_interrupt(pci_nftdrm_t *dev, uint32_t type);

static void pci_nftdrm_handle_cmd(pci_nftdrm_t *dev);

static void pci_nftdrm_initialize_queue(pci_nftdrm_t *dev);
static void pci_nftdrm_handle_exchange(pci_nftdrm_t *dev);
static void pci_nftdrm_handle_aes_load(pci_nftdrm_t *dev);
static void pci_nftdrm_handle_encrypted(pci_nftdrm_t *dev);
static void pci_nftdrm_handle_decrypted(pci_nftdrm_t *dev);
static void pci_nftdrm_reload(pci_nftdrm_t *dev);

#endif