/*
 * nvidia_compat.ko - NVIDIA Compatibility Layer
 * Part of shittyNVIDIA - The worst NVIDIA driver ever
 *
 * This kernel module creates a compatibility layer that:
 * 1. Creates /dev/nvidia1337 device node
 * 2. Forwards IOCTLs to real NVIDIA driver (if available)
 * 3. Shows up in nvidia-smi with real or fake GPU stats
 * 4. Supports adding fake GPUs for fun
 *
 * MIT License
 */

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/device.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/ioctl.h>
#include <linux/version.h>

#define DEVICE_NAME "nvidia1337"
#define CLASS_NAME "nvidia_compat"

/* NVIDIA IOCTL magic number and commands based on NVIDIA open source driver */
#define NV_IOCTL_MAGIC 'F'
#define NV_ESC_CARD_INFO         _IOWR(NV_IOCTL_MAGIC, 0x00, unsigned long)
#define NV_ESC_CHECK_VERSION     _IOWR(NV_IOCTL_MAGIC, 0x01, unsigned long)
#define NV_ESC_QUERY_DEVICE_INTR _IOWR(NV_IOCTL_MAGIC, 0x02, unsigned long)

/* CUDA UVM IOCTLs - for CUDA runtime support */
#define UVM_INITIALIZE           _IOWR(NV_IOCTL_MAGIC, 0x30, unsigned long)
#define UVM_DEINITIALIZE         _IO(NV_IOCTL_MAGIC, 0x31)
#define UVM_CREATE_RANGE_GROUP   _IOWR(NV_IOCTL_MAGIC, 0x32, unsigned long)
#define UVM_DESTROY_RANGE_GROUP  _IOW(NV_IOCTL_MAGIC, 0x33, unsigned long)

/* Module parameters */
static int major_number;
static struct class *nvidia_compat_class = NULL;
static struct device *nvidia_compat_device = NULL;
static struct cdev nvidia_compat_cdev;

/* Fake GPU configuration */
static int enable_fake_gpu = 1;
module_param(enable_fake_gpu, int, 0644);
MODULE_PARM_DESC(enable_fake_gpu, "Enable fake GPU device (1=yes, 0=no)");

static char fake_gpu_name[64] = "GeForce RTX 4090 (Fake)";
module_param_string(fake_gpu_name, fake_gpu_name, sizeof(fake_gpu_name), 0644);
MODULE_PARM_DESC(fake_gpu_name, "Name of the fake GPU");

static int fake_gpu_memory = 24576; // 24GB in MB
module_param(fake_gpu_memory, int, 0644);
MODULE_PARM_DESC(fake_gpu_memory, "Fake GPU memory size in MB");

/*
 * Forward IOCTL to real NVIDIA driver
 * Returns 0 on success, negative error code on failure
 * 
 * Security Note: This forwards IOCTLs to the real NVIDIA driver without
 * extensive validation. In a production environment, consider implementing
 * a whitelist of allowed IOCTL commands to prevent potential security issues.
 */
static long forward_ioctl_to_real_nvidia(unsigned int cmd, unsigned long arg)
{
    struct file *filp;
    long ret = -ENODEV;
    
    /* Try to open the real NVIDIA device */
    filp = filp_open("/dev/nvidia0", O_RDWR, 0);
    if (IS_ERR(filp)) {
        /* Real device not available, return error */
        return PTR_ERR(filp);
    }
    
    /* Forward the IOCTL call to the real driver */
    if (filp->f_op && filp->f_op->unlocked_ioctl) {
        ret = filp->f_op->unlocked_ioctl(filp, cmd, arg);
    }
    
    filp_close(filp, NULL);
    return ret;
}

/*
 * Handle nvidia-smi query IOCTLs with fake or real data
 * Updated to spoof real VRAM sizes down to a uniform cluster standard!
 */
static long handle_device_query(unsigned long arg)
{
    struct {
        unsigned int device_count;
        char gpu_name[64];
        unsigned long memory_total;
        unsigned long memory_free;
        unsigned int gpu_utilization;
        unsigned int memory_utilization;
        unsigned int temperature;
        unsigned int power_draw;
    } device_info;
    
    if (!enable_fake_gpu) {
        /* 
         * 1. CALL THE REAL DRIVER FIRST
         * Let the real NVIDIA kernel populate the device_info struct inside user-space memory
         */
        long ret = forward_ioctl_to_real_nvidia(NV_ESC_CARD_INFO, arg);
        if (ret < 0) {
            return ret; // If the real driver errored out, bubble it up
        }

        /* 
         * 2. INTERCEPT AND OVERWRITE 
         * Pull the real hardware data back into kernel space so we can manipulate it
         */
        if (copy_from_user(&device_info, (void __user *)arg, sizeof(device_info))) {
            return -EFAULT;
        }

        /* 
         * 3. ENFORCE UNIFORM CLUSTER BASELINE
         * Calculate target bytes based on your module param 'fake_gpu_memory' (e.g., 8192 MB)
         */
        unsigned long uniform_vram_bytes = (unsigned long)fake_gpu_memory * 1024 * 1024;
        
        // If the physical card is larger than our cluster standard, mask it!
        if (device_info.memory_total > uniform_vram_bytes) {
            unsigned long consumed_vram = device_info.memory_total - device_info.memory_free;
            
            device_info.memory_total = uniform_vram_bytes;
            
            // Adjust free memory metrics so math adds up for the orchestrator
            if (consumed_vram < uniform_vram_bytes) {
                device_info.memory_free = uniform_vram_bytes - consumed_vram;
            } else {
                device_info.memory_free = 0; // Hard cap if somehow over-allocated
            }
        }

        /* 
         * 4. SHIP IT BACK TO PYTORCH / vLLM
         * Shove the modified uniform layout back into user-space
         */
        if (copy_to_user((void __user *)arg, &device_info, sizeof(device_info))) {
            return -EFAULT;
        }

        return 0;
    }
    
    /* Provide fake GPU data (Your original pure-emulation code remains untouched) */
    memset(&device_info, 0, sizeof(device_info));
    device_info.device_count = 1;
    strncpy(device_info.gpu_name, fake_gpu_name, sizeof(device_info.gpu_name) - 1);
    device_info.gpu_name[sizeof(device_info.gpu_name) - 1] = '\0'; 
    device_info.memory_total = (unsigned long)fake_gpu_memory * 1024 * 1024; 
    device_info.memory_free = device_info.memory_total * 95 / 100; 
    device_info.gpu_utilization = 5; 
    device_info.memory_utilization = 5;
    device_info.temperature = 35; 
    device_info.power_draw = 25; 
    
    if (copy_to_user((void __user *)arg, &device_info, sizeof(device_info))) {
        return -EFAULT;
    }
    
    return 0;
}
/*
 * Device open handler
 */
static int nvidia_compat_open(struct inode *inode, struct file *filp)
{
    pr_info("nvidia_compat: Device opened\n");
    return 0;
}

/*
 * Device release handler
 */
static int nvidia_compat_release(struct inode *inode, struct file *filp)
{
    pr_info("nvidia_compat: Device closed\n");
    return 0;
}

/*
 * Device IOCTL handler
 * This is where the magic happens - we either forward to real NVIDIA or fake it
 */
static long nvidia_compat_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
    long ret = 0;
    
    pr_info("nvidia_compat: IOCTL received: cmd=0x%x\n", cmd);
    
    /* Handle specific IOCTLs we care about */
    switch (cmd) {
        case NV_ESC_CARD_INFO:
        case NV_ESC_CHECK_VERSION:
            ret = handle_device_query(arg);
            break;
            
        case UVM_INITIALIZE:
        case UVM_DEINITIALIZE:
        case UVM_CREATE_RANGE_GROUP:
        case UVM_DESTROY_RANGE_GROUP:
            /* CUDA IOCTLs - try to forward to real driver */
            ret = forward_ioctl_to_real_nvidia(cmd, arg);
            if (ret == -ENODEV && enable_fake_gpu) {
                /* Real driver not available, fake success for some operations */
                pr_info("nvidia_compat: CUDA IOCTL faked (no real driver)\n");
                ret = 0;
            }
            break;
            
        default:
            /* For unknown IOCTLs, try to forward to real driver */
            ret = forward_ioctl_to_real_nvidia(cmd, arg);
            if (ret == -ENODEV && enable_fake_gpu) {
                /* If forwarding fails and fake GPU is enabled, fake success */
                pr_info("nvidia_compat: Unknown IOCTL faked: 0x%x\n", cmd);
                ret = 0;
            } else if (ret == -ENODEV) {
                ret = -ENOTTY;
            }
            break;
    }
    
    return ret;
}

/*
 * Device read handler - provide fake data for nvidia-smi
 */
static ssize_t nvidia_compat_read(struct file *filp, char __user *buf, size_t count, loff_t *f_pos)
{
    char message[256];
    size_t message_len;
    
    if (*f_pos > 0) {
        return 0; // EOF
    }
    
    snprintf(message, sizeof(message),
             "NVIDIA Compat Layer\n"
             "Fake GPU Status: %s\n"
             "GPU Name: %s\n"
             "Memory: %d MB\n"
             "Status: Active\n",
             enable_fake_gpu ? "Enabled" : "Disabled",
             enable_fake_gpu ? fake_gpu_name : "N/A",
             fake_gpu_memory);
    
    message_len = strlen(message);
    
    if (count < message_len) {
        return -EINVAL;
    }
    
    if (copy_to_user(buf, message, message_len)) {
        return -EFAULT;
    }
    
    *f_pos += message_len;
    return message_len;
}

/* File operations structure */
static struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = nvidia_compat_open,
    .release = nvidia_compat_release,
    .unlocked_ioctl = nvidia_compat_ioctl,
    .read = nvidia_compat_read,
};

/*
 * Module initialization
 */
static int __init nvidia_compat_init(void)
{
    dev_t dev;
    int ret;
    
    pr_info("nvidia_compat: Initializing NVIDIA Compatibility Layer\n");
    pr_info("nvidia_compat: Fake GPU: %s (%s, %d MB)\n",
            enable_fake_gpu ? "enabled" : "disabled",
            fake_gpu_name, fake_gpu_memory);
    
    /* Allocate character device region */
    ret = alloc_chrdev_region(&dev, 0, 1, DEVICE_NAME);
    if (ret < 0) {
        pr_err("nvidia_compat: Failed to allocate char device region\n");
        return ret;
    }
    
    major_number = MAJOR(dev);
    pr_info("nvidia_compat: Registered with major number %d\n", major_number);
    
    /* Initialize cdev structure */
    cdev_init(&nvidia_compat_cdev, &fops);
    nvidia_compat_cdev.owner = THIS_MODULE;
    
    /* Add character device to the system */
    ret = cdev_add(&nvidia_compat_cdev, dev, 1);
    if (ret < 0) {
        pr_err("nvidia_compat: Failed to add cdev\n");
        unregister_chrdev_region(dev, 1);
        return ret;
    }
    
    /* Create device class */
    nvidia_compat_class = class_create(CLASS_NAME);
    if (IS_ERR(nvidia_compat_class)) {
        pr_err("nvidia_compat: Failed to create device class\n");
        cdev_del(&nvidia_compat_cdev);
        unregister_chrdev_region(dev, 1);
        return PTR_ERR(nvidia_compat_class);
    }
    
    /* Create device */
    nvidia_compat_device = device_create(nvidia_compat_class, NULL, dev, NULL, DEVICE_NAME);
    if (IS_ERR(nvidia_compat_device)) {
        pr_err("nvidia_compat: Failed to create device\n");
        class_destroy(nvidia_compat_class);
        cdev_del(&nvidia_compat_cdev);
        unregister_chrdev_region(dev, 1);
        return PTR_ERR(nvidia_compat_device);
    }
    
    pr_info("nvidia_compat: Device /dev/%s created successfully\n", DEVICE_NAME);
    pr_info("nvidia_compat: Ready to forward IOCTLs to real NVIDIA driver or fake them\n");
    
    return 0;
}

/*
 * Module cleanup
 */
static void __exit nvidia_compat_exit(void)
{
    dev_t dev = MKDEV(major_number, 0);
    
    pr_info("nvidia_compat: Cleaning up\n");
    
    /* Clean up in reverse order */
    if (nvidia_compat_device) {
        device_destroy(nvidia_compat_class, dev);
    }
    
    if (nvidia_compat_class) {
        class_destroy(nvidia_compat_class);
    }
    
    cdev_del(&nvidia_compat_cdev);
    unregister_chrdev_region(dev, 1);
    
    pr_info("nvidia_compat: Module unloaded\n");
}

module_init(nvidia_compat_init);
module_exit(nvidia_compat_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("shittyNVIDIA Contributors");
MODULE_DESCRIPTION("NVIDIA Compatibility Layer - Forward IOCTLs and fake GPUs");
MODULE_VERSION("0.1");
