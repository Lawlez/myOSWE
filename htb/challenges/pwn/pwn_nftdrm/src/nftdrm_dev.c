#include <stdint.h>
#include <stdbool.h>
#include <sys/mman.h>

#include "qemu/osdep.h"
#include "qemu/units.h"
#include "hw/pci/pci.h"
#include "hw/hw.h"
#include "hw/pci/msi.h"
#include "qom/object.h"
#include "qemu/module.h"
#include "qapi/visitor.h"
#include "sysemu/dma.h"

#include "decrypt_store.h"
#include "nft_crypto.h"
#include "nftdrm_dev.h"

#define PAGE_SIZE 4096

#define NFTDRM(obj) \
    OBJECT_CHECK(pci_nftdrm_t, (obj), TYPE_PCI_NFTDRM_DEV)

#define VALID_SZ($field, size) \
    sizeof(((nftdrm_io_t *)0)->$field) == size

#define CASE($field, size, boolean) \
    case offsetof(nftdrm_io_t, $field): \
        if (!(VALID_SZ($field, size))) { \
            boolean = false; \
            break; \
        } \

static const MemoryRegionOps pci_nftdrm_mmio_ops = {
    .read = pci_nftdrm_mmio_read,
    .write = pci_nftdrm_mmio_write,
    .endianness = DEVICE_LITTLE_ENDIAN,
    .valid = {
        .min_access_size = sizeof(uint8_t),
        .max_access_size = sizeof(uint64_t),
    },
    .impl = {
        .min_access_size = sizeof(uint8_t),
        .max_access_size = sizeof(uint64_t),
    },
};

static InterfaceInfo interfaces[] = {
    { INTERFACE_CONVENTIONAL_PCI_DEVICE },
    { },
};

static const TypeInfo pci_nftdrm_info = {
    .name = TYPE_PCI_NFTDRM_DEV,
    .parent = TYPE_PCI_DEVICE,
    .instance_size = sizeof(pci_nftdrm_t),
    .instance_init = pci_nftdrm_instance_init,
    .class_init = pci_nftdrm_class_init,
    .interfaces = interfaces,
};

#pragma GCC push_options
#pragma GCC optimize ("O0")

static void pci_nftdrm_register_types(void)
{
    type_register_static(&pci_nftdrm_info);
    return;
}

static void pci_nftdrm_instance_init(Object *obj)
{
    return;
}

void pci_nftdrm_class_init(ObjectClass *klass, void *data)
{
    DeviceClass *dc = DEVICE_CLASS(klass);
    PCIDeviceClass *k = PCI_DEVICE_CLASS(klass);

    k->realize = pci_nftdrm_realize;
    k->exit = pci_nftdrm_exit;

    k->vendor_id = NFTDRM_VENDOR_ID;
    k->device_id = NFTDRM_DEVICE_ID;
    k->revision  = NFTDRM_DEVICE_REVISION;
    k->class_id = PCI_CLASS_OTHERS;
    
    set_bit(DEVICE_CATEGORY_MISC, dc->categories);
    dc->desc = "Protecting your NFTs from right clickers";

    return;
}

static void pci_nftdrm_realize(PCIDevice *pdev, Error **errp)
{
    pci_nftdrm_t *dev = NFTDRM(pdev);

    void *random_addr = mmap(NULL, PAGE_SIZE * 6, PROT_READ | PROT_WRITE, 
                                MAP_ANONYMOUS | MAP_SHARED, -1, 0);
    if (random_addr == (void *)-1)
        return;
    mprotect(random_addr, PAGE_SIZE, PROT_NONE);
    dev->device_io = random_addr + PAGE_SIZE;
    dev->xchg_dma = random_addr + PAGE_SIZE * 2;
    dev->enc_dma = random_addr + PAGE_SIZE * 3;
    dev->dec_dma = random_addr + PAGE_SIZE * 4;
    mprotect(random_addr + PAGE_SIZE * 5, PAGE_SIZE, PROT_NONE);

    if (!initialize_ecdh(&dev->drmkey.ecc))
        return;

    dev->queue_ready = false;
    dev->recieved_aes = false;
    dev->recieved_pubkey = false;

    pci_config_set_interrupt_pin(pdev->config, 1);
    if (msi_init(pdev, 0, MSI_REQUIRED, true, false, errp))
        return;

    memory_region_init_io(&dev->mmio, OBJECT(dev), 
                            &pci_nftdrm_mmio_ops, dev,
                            TYPE_PCI_NFTDRM_DEV, PAGE_SIZE);
    pci_register_bar(pdev, 0, PCI_BASE_ADDRESS_SPACE_MEMORY, &dev->mmio);

    qemu_mutex_init(&dev->lock);
    return;
}

static void pci_nftdrm_exit(PCIDevice *pdev)
{
    pci_nftdrm_t *dev = NFTDRM(pdev);

    qemu_mutex_lock(&dev->lock);
    pci_config_set_interrupt_pin(pdev->config, 0);
    msi_uninit(pdev);
    munmap(dev->device_io - PAGE_SIZE, PAGE_SIZE * 6);

    qemu_mutex_destroy(&dev->lock);
    return;
}


static uint64_t pci_nftdrm_mmio_read(void *opaque, hwaddr addr, unsigned size)
{
    uint64_t result = ~0;
    bool valid_size = true;
    bool valid_offset = true;
    pci_nftdrm_t *dev = (pci_nftdrm_t *)opaque;

    qemu_mutex_lock(&dev->lock);

    switch(addr)
    {
        CASE(error, size, valid_size)
            result = dev->device_io->error;
            break;
        CASE(ret_val, size, valid_size)
            result = dev->device_io->ret_val;
            break;
        CASE(state, size, valid_size)
            result = dev->device_io->state;
            break;
        default:
            valid_offset = false;
            break;
    }

    if (!valid_offset)
    {
        dev->device_io->error = ERROR_INT_INVALID_OFFSET;
        pci_nftdrm_interrupt(dev, NFTDRM_BUG);
    }
    if (!valid_size)
    {
        dev->device_io->error = ERROR_INT_INVALID_SZ;
        pci_nftdrm_interrupt(dev, NFTDRM_BUG);
    }

    qemu_mutex_unlock(&dev->lock);
    return result;
}

static void pci_nftdrm_mmio_write(void *opaque, hwaddr addr, uint64_t val, unsigned size)
{
    bool valid_size = true;
    bool valid_offset = true;
    pci_nftdrm_t *dev = (pci_nftdrm_t *)opaque;

    qemu_mutex_lock(&dev->lock);

    switch(addr)
    {
        CASE(command, size, valid_size)
            dev->device_io->command = val;
            pci_nftdrm_handle_cmd(dev);
            break;
        CASE(enc_buf, size, valid_size)
            dev->device_io->enc_buf = val;
            break;
        CASE(dec_buf, size, valid_size)
            dev->device_io->dec_buf = val;
            break;
        CASE(xchg_buf, size, valid_size)
            dev->device_io->xchg_buf = val;
            break;
        CASE(enc_size, size, valid_size)
            dev->device_io->enc_size = val;
            break;
        CASE(dec_size, size, valid_size)
            dev->device_io->dec_size = val;
            break;
        default:
            valid_offset = false;
            break;
    }

    if (!valid_offset)
    {
        dev->device_io->error = ERROR_INT_INVALID_OFFSET;
        pci_nftdrm_interrupt(dev, NFTDRM_BUG);
    }
    if (!valid_size)
    {
        dev->device_io->error = ERROR_INT_INVALID_SZ;
        pci_nftdrm_interrupt(dev, NFTDRM_BUG);
    }

    qemu_mutex_unlock(&dev->lock);
    return;
}

static void pci_nftdrm_interrupt(pci_nftdrm_t *dev, uint32_t type)
{
    qemu_mutex_unlock(&dev->lock);
    dev->device_io->state = type;
    msi_notify(&dev->pdev, 0);
    qemu_mutex_lock(&dev->lock);
}

static void pci_nftdrm_handle_cmd(pci_nftdrm_t *dev)
{
    uint8_t cmd = dev->device_io->command;
    switch(cmd)
    {
        case CMD_INITIALIZE_QUEUE:
            pci_nftdrm_initialize_queue(dev);
            break;
        case CMD_EXCHANGE:
            pci_nftdrm_handle_exchange(dev);
            break;
        case CMD_LOAD_AES:
            pci_nftdrm_handle_aes_load(dev);
            break;
        case CMD_HANDLE_ENCRYPT:
            pci_nftdrm_handle_encrypted(dev);
            break;
        case CMD_HANDLE_DECRYPT:
            pci_nftdrm_handle_decrypted(dev);
            break;
        case CMD_RELOAD:
            pci_nftdrm_reload(dev);
            break;
        default:
            dev->device_io->error = ERROR_INT_INVALID_CMD;
            pci_nftdrm_interrupt(dev, NFTDRM_BUG);
    }
    return;
}

static void pci_nftdrm_initialize_queue(pci_nftdrm_t *dev)
{
    if (dev->queue_ready || !initialize_queue(&dev->main_queue))
    {
        dev->device_io->ret_val = 0;
        pci_nftdrm_interrupt(dev, NFTDRM_OK);
        return;
    }

    dev->queue_ready = true;
    dev->device_io->ret_val = 1;
    pci_nftdrm_interrupt(dev, NFTDRM_OK);
    return;
}

static void pci_nftdrm_handle_exchange(pci_nftdrm_t *dev)
{
    if (!dev->queue_ready)
    {
        dev->device_io->ret_val = 0;
        pci_nftdrm_interrupt(dev, NFTDRM_OK);
        return;
    }

    uint32_t dma_result = dma_memory_read(&address_space_memory, dev->device_io->xchg_buf,
                                            dev->xchg_dma, PAGE_SIZE);

    if (dma_result)
    {
        dev->device_io->error = ERROR_INT_DMA_READ;
        pci_nftdrm_interrupt(dev, NFTDRM_BUG);
        return;
    }

    bool result = initialize_secret(&dev->drmkey.ecc, dev->xchg_dma, dev->xchg_dma);

    dma_result = dma_memory_write(&address_space_memory, dev->device_io->xchg_buf,
                                            dev->xchg_dma, PAGE_SIZE);

    if (dma_result)
    {
        dev->device_io->error = ERROR_INT_DMA_WRITE;
        pci_nftdrm_interrupt(dev, NFTDRM_BUG);
        return;
    }

    if (result)
        dev->recieved_pubkey = true;
    dev->device_io->ret_val = result;
    pci_nftdrm_interrupt(dev, NFTDRM_OK);
    return;

}

static void pci_nftdrm_handle_aes_load(pci_nftdrm_t *dev)
{
    if (!dev->recieved_pubkey)
    {
        dev->device_io->ret_val = 0;
        pci_nftdrm_interrupt(dev, NFTDRM_OK);
        return;
    }

    uint32_t dma_result = dma_memory_read(&address_space_memory, dev->device_io->xchg_buf,
                                            dev->xchg_dma, PAGE_SIZE);

    if (dma_result)
    {
        dev->device_io->error = ERROR_INT_DMA_READ;
        pci_nftdrm_interrupt(dev, NFTDRM_BUG);
        return;
    }

    retrieve_aes_key(dev->xchg_dma, &dev->drmkey.ecc, &dev->drmkey.aes);

    dev->recieved_aes = true;
    dev->device_io->ret_val = 1;
    pci_nftdrm_interrupt(dev, NFTDRM_OK);
    return;
}

static void pci_nftdrm_handle_encrypted(pci_nftdrm_t *dev)
{
    if (!dev->recieved_aes)
    {
        dev->device_io->ret_val = 0;
        pci_nftdrm_interrupt(dev, NFTDRM_OK);
        return;
    }

    uint32_t dma_result = dma_memory_read(&address_space_memory, dev->device_io->enc_buf,
                                            dev->enc_dma, PAGE_SIZE);

    if (dma_result)
    {
        dev->device_io->error = ERROR_INT_DMA_READ;
        pci_nftdrm_interrupt(dev, NFTDRM_BUG);
        return;
    }

    uint32_t result = handle_encrypted(&dev->main_queue, &dev->drmkey.aes, dev->enc_dma,
                                        dev->device_io->enc_size);

    dev->device_io->ret_val = result;
    pci_nftdrm_interrupt(dev, NFTDRM_OK);
    return;
}

static void pci_nftdrm_handle_decrypted(pci_nftdrm_t *dev)
{
    if (!dev->recieved_aes)
    {
        dev->device_io->ret_val = 0;
        pci_nftdrm_interrupt(dev, NFTDRM_OK);
        return;
    }

    int16_t result = handle_decrypted(&dev->main_queue, dev->dec_dma, dev->device_io->dec_size);

    uint32_t dma_result = dma_memory_write(&address_space_memory, dev->device_io->dec_buf,
                                            dev->dec_dma, PAGE_SIZE);
    if (dma_result)
    {
        dev->device_io->error = ERROR_INT_DMA_WRITE;
        pci_nftdrm_interrupt(dev, NFTDRM_BUG);
        return;
    }

    dev->device_io->ret_val = result;
    pci_nftdrm_interrupt(dev, NFTDRM_OK);
    return;
}

static void pci_nftdrm_reload(pci_nftdrm_t *dev)
{
    if (!dev->queue_ready)
    {
        dev->device_io->ret_val = 0;
        pci_nftdrm_interrupt(dev, NFTDRM_OK);
        return;
    }

    destroy_queue(&dev->main_queue);
    memset(dev->enc_dma, 0, PAGE_SIZE);
    memset(dev->dec_dma, 0, PAGE_SIZE);
    memset(dev->xchg_dma, 0, PAGE_SIZE);
    dev->recieved_pubkey = false;
    dev->recieved_aes = false;
    dev->queue_ready = initialize_queue(&dev->main_queue);
    dev->device_io->ret_val = dev->queue_ready;
    pci_nftdrm_interrupt(dev, NFTDRM_OK);
    return;
}

#pragma GCC pop_options

type_init(pci_nftdrm_register_types);