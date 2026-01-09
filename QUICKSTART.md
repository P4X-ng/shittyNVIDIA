# Quick Start Guide: nvidia_compat Kernel Module

This guide will get you up and running with the nvidia_compat kernel module in minutes.

## Prerequisites

```bash
# Install kernel headers and build tools
sudo apt-get update
sudo apt-get install -y linux-headers-$(uname -r) build-essential
```

## Build and Load

### Option 1: Quick Demo (Recommended for first-time users)

```bash
# Run the demo script
cd shittyNVIDIA
./nvidia_compat_demo.sh

# Or with root to actually load the module
sudo ./nvidia_compat_demo.sh
```

### Option 2: Manual Build and Load

```bash
# Build
cd nvidia_compat_module
make

# Load with fake GPU (default settings)
sudo make load

# Or load with custom settings
sudo insmod nvidia_compat.ko \
    enable_fake_gpu=1 \
    fake_gpu_name="GeForce_RTX_5090" \
    fake_gpu_memory=32768

# Verify
ls -la /dev/nvidia1337
```

### Option 3: Full Installation (Loads on boot)

```bash
# From repository root
./install-nvidia-compat.sh install

# This will:
# - Build the kernel module
# - Install it to the system
# - Configure it to load on boot
# - Set up the device node
```

## Verify Installation

```bash
# Check if module is loaded
lsmod | grep nvidia_compat

# Check if device exists
ls -la /dev/nvidia1337

# Read device info
cat /dev/nvidia1337

# Run test suite
python3 test_nvidia_compat.py

# View kernel messages
sudo dmesg | grep nvidia_compat | tail -20
```

## Usage Modes

### Mode 1: With Real NVIDIA Driver (IOCTL Forwarding)

If you have a real NVIDIA driver installed:

```bash
# Load without fake GPU
sudo insmod nvidia_compat.ko enable_fake_gpu=0

# Now /dev/nvidia1337 forwards all IOCTLs to /dev/nvidia0
# Your CUDA applications can use either device
```

### Mode 2: Without Real Driver (Fake GPU Mode)

For testing, development, or just for fun:

```bash
# Load with fake GPU (default)
sudo insmod nvidia_compat.ko \
    enable_fake_gpu=1 \
    fake_gpu_name="Tesla_V100" \
    fake_gpu_memory=16384

# Read fake GPU info
cat /dev/nvidia1337

# The fake GPU will respond to nvidia-smi queries
```

## Common Operations

### View Module Parameters

```bash
# Current settings
cat /sys/module/nvidia_compat/parameters/enable_fake_gpu
cat /sys/module/nvidia_compat/parameters/fake_gpu_name
cat /sys/module/nvidia_compat/parameters/fake_gpu_memory
```

### Reload with Different Parameters

```bash
# Unload
sudo rmmod nvidia_compat

# Reload with new settings
sudo insmod nvidia_compat.ko \
    enable_fake_gpu=1 \
    fake_gpu_name="RTX_4090_SUPER" \
    fake_gpu_memory=24576
```

### Unload Module

```bash
sudo rmmod nvidia_compat

# Or if you installed it system-wide
sudo modprobe -r nvidia_compat
```

## Testing CUDA Support

If you have CUDA installed and want to test IOCTL forwarding:

```bash
# Create a simple CUDA test (example)
cat > cuda_test.cu << 'EOF'
#include <stdio.h>
#include <cuda_runtime.h>

int main() {
    int device_count = 0;
    cudaError_t error = cudaGetDeviceCount(&device_count);
    
    printf("CUDA Status: %s\n", cudaGetErrorString(error));
    printf("Device Count: %d\n", device_count);
    
    if (device_count > 0) {
        cudaDeviceProp prop;
        cudaGetDeviceProperties(&prop, 0);
        printf("Device 0: %s\n", prop.name);
        printf("Memory: %.2f GB\n", prop.totalGlobalMem / (1024.0*1024.0*1024.0));
    }
    
    return 0;
}
EOF

# Compile and run (requires nvcc)
nvcc -o cuda_test cuda_test.cu
./cuda_test
```

## Troubleshooting

### Module Won't Load

```bash
# Check kernel logs
sudo dmesg | tail -20

# Verify kernel headers match
uname -r
ls /lib/modules/$(uname -r)/build
```

### Device Not Created

```bash
# Check if module loaded successfully
lsmod | grep nvidia_compat

# Check for errors
sudo dmesg | grep nvidia_compat | grep -i error

# Try reloading
sudo rmmod nvidia_compat
sudo insmod nvidia_compat.ko
```

### Permission Denied

```bash
# Check device permissions
ls -la /dev/nvidia1337

# Most operations require root/sudo
sudo cat /dev/nvidia1337
```

## Configuration Files

After installation, configuration is stored in:

```bash
# Module load on boot
/etc/modules-load.d/nvidia_compat.conf

# Module parameters
/etc/modprobe.d/nvidia_compat.conf

# Module location
/lib/modules/$(uname -r)/extra/nvidia_compat.ko
```

## Uninstall

```bash
# Complete removal
./install-nvidia-compat.sh uninstall

# Or manually
sudo rmmod nvidia_compat
sudo rm -f /lib/modules/$(uname -r)/extra/nvidia_compat.ko
sudo rm -f /etc/modules-load.d/nvidia_compat.conf
sudo rm -f /etc/modprobe.d/nvidia_compat.conf
sudo depmod -A
```

## What's Next?

- Read the [full module documentation](nvidia_compat_module/README.md)
- Explore [IOCTL analysis](drivers/)
- Check out [example scripts](examples.py)
- Understand [CUDA support details](nvidia_compat_module/README.md#cuda-support)

## Support

This is part of shittyNVIDIA - a parody project for educational purposes.

For issues or questions:
- GitHub: https://github.com/P4X-ng/shittyNVIDIA
- Read the docs in `nvidia_compat_module/README.md`
- Check kernel logs: `sudo dmesg | grep nvidia_compat`

Remember: This is shittyNVIDIA. We proudly support 0 NVIDIA devices... but now we do it with style! 🎉
