# NVIDIA Compatibility Layer Kernel Module

This kernel module creates a compatibility layer for NVIDIA devices that:
1. Creates `/dev/nvidia1337` device node
2. Forwards IOCTLs to the real NVIDIA driver (if available)
3. Shows up in nvidia-smi with real or fake GPU statistics
4. Supports adding fake GPUs for fun
5. Enables CUDA runtime to work through the compat layer

## Features

### IOCTL Forwarding
The module intercepts IOCTLs sent to `/dev/nvidia1337` and forwards them to the real NVIDIA driver at `/dev/nvidia0` if available. This allows CUDA applications to work through the compatibility layer.

### Fake GPU Support
When no real NVIDIA driver is available, or when explicitly enabled, the module can emulate a fake GPU with configurable parameters:
- GPU name (default: "GeForce RTX 4090 (Fake)")
- Memory size (default: 24576 MB / 24 GB)
- Utilization statistics
- Temperature and power metrics

### nvidia-smi Integration
The fake GPU appears in nvidia-smi output with realistic statistics, making it perfect for:
- Testing CUDA applications without real hardware
- Development environments
- CI/CD pipelines
- Just having fun with fake GPUs

## Building

### Requirements
- Linux kernel headers for your running kernel
- GCC compiler
- Make

Install requirements on Ubuntu:
```bash
sudo apt-get update
sudo apt-get install -y linux-headers-$(uname -r) build-essential
```

### Build the Module
```bash
cd nvidia_compat_module
make
```

This will produce `nvidia_compat.ko`.

## Installation

### Load the Module
```bash
# Load with default fake GPU settings
sudo make load

# Or manually with custom settings
sudo insmod nvidia_compat.ko enable_fake_gpu=1 \
    fake_gpu_name="GeForce_RTX_5090" \
    fake_gpu_memory=32768
```

### Verify Installation
```bash
# Check if device was created
ls -la /dev/nvidia1337

# Check kernel messages
dmesg | tail -20

# Test the module
make test
```

### Install Permanently
```bash
sudo make install

# Load on boot
echo "nvidia_compat" | sudo tee /etc/modules-load.d/nvidia_compat.conf

# Set default parameters
echo "options nvidia_compat enable_fake_gpu=1 fake_gpu_name=GeForce_RTX_4090_(Fake) fake_gpu_memory=24576" | \
    sudo tee /etc/modprobe.d/nvidia_compat.conf
```

## Usage

### With Real NVIDIA Driver
If you have a real NVIDIA driver installed (`/dev/nvidia0` exists), the module will forward all IOCTLs to the real driver. Your CUDA applications will work through `/dev/nvidia1337`.

```bash
# Load module without fake GPU
sudo insmod nvidia_compat.ko enable_fake_gpu=0

# Run CUDA application
# Configure it to use /dev/nvidia1337 instead of /dev/nvidia0
```

### Without Real NVIDIA Driver (Fake Mode)
When no real driver is available, the module provides fake responses:

```bash
# Load with fake GPU
sudo insmod nvidia_compat.ko enable_fake_gpu=1 \
    fake_gpu_name="RTX_4090_SUPER" \
    fake_gpu_memory=24576

# Read device info
cat /dev/nvidia1337

# Check with nvidia-smi (if you have shittyNVIDIA's nvidia-smi)
nvidia-smi
```

### Module Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enable_fake_gpu` | int | 1 | Enable fake GPU device (1=yes, 0=no) |
| `fake_gpu_name` | string | "GeForce RTX 4090 (Fake)" | Name of the fake GPU |
| `fake_gpu_memory` | int | 24576 | Fake GPU memory size in MB |

### Changing Parameters at Runtime
```bash
# View current parameters
cat /sys/module/nvidia_compat/parameters/enable_fake_gpu
cat /sys/module/nvidia_compat/parameters/fake_gpu_name
cat /sys/module/nvidia_compat/parameters/fake_gpu_memory

# Note: Parameters can only be changed at module load time
```

## Uninstallation

### Unload the Module
```bash
sudo make unload

# Or manually
sudo rmmod nvidia_compat
```

### Remove from System
```bash
sudo make uninstall

# Remove config files
sudo rm -f /etc/modules-load.d/nvidia_compat.conf
sudo rm -f /etc/modprobe.d/nvidia_compat.conf
```

## CUDA Support

The module implements the following CUDA-related IOCTLs:
- `UVM_INITIALIZE` - Initialize CUDA Unified Virtual Memory
- `UVM_DEINITIALIZE` - Clean up UVM
- `UVM_CREATE_RANGE_GROUP` - Create memory range group
- `UVM_DESTROY_RANGE_GROUP` - Destroy memory range group

When forwarding is available (real driver present), these are passed through. When in fake mode, they return success to allow CUDA runtime initialization.

### CUDA Example
```bash
# Load module
sudo insmod nvidia_compat.ko enable_fake_gpu=0

# If you have CUDA installed, compile a test program
nvcc -o cuda_test cuda_test.cu

# Run it (may need to set CUDA_VISIBLE_DEVICES)
./cuda_test
```

## Architecture

```
User Application
      |
      | IOCTL
      v
/dev/nvidia1337 (nvidia_compat.ko)
      |
      +---> Real Driver Available?
      |           |
      |          Yes --> Forward to /dev/nvidia0 (Real NVIDIA Driver)
      |           |
      |          No --> Fake GPU Enabled?
      |                     |
      |                    Yes --> Return Fake Data
      |                     |
      |                    No --> Return Error
      v
   Result
```

## Debugging

### View Kernel Messages
```bash
# Real-time kernel messages
sudo dmesg -w | grep nvidia_compat

# Last 50 messages
sudo dmesg | grep nvidia_compat | tail -50
```

### Check Module Status
```bash
# Module info
modinfo nvidia_compat.ko

# Loaded modules
lsmod | grep nvidia

# Module parameters
systool -v -m nvidia_compat
```

### Common Issues

**Issue**: Module won't load
```bash
# Check kernel log for errors
dmesg | tail -20

# Verify kernel version matches headers
uname -r
ls /lib/modules/$(uname -r)/build
```

**Issue**: Device not created
```bash
# Check if module loaded successfully
lsmod | grep nvidia_compat

# Check device creation
ls -la /dev/nvidia*

# Check kernel messages
dmesg | grep nvidia_compat
```

**Issue**: IOCTLs failing
```bash
# Check if real driver is accessible
ls -la /dev/nvidia0

# View IOCTL activity
sudo dmesg -w | grep nvidia_compat
```

## Security Considerations

This module:
- Requires root/sudo privileges to load
- Can forward IOCTLs to real NVIDIA driver (potential security boundary)
- Creates a world-readable character device
- Logs IOCTL commands to kernel log (may expose application behavior)

For production use, consider:
- Restricting device permissions
- Limiting IOCTL forwarding to specific commands
- Disabling debug logging
- Using SELinux/AppArmor policies

## Development

### Code Structure
- `nvidia_compat.c` - Main module source
- `Makefile` - Build system
- `README.md` - This file

### Adding New IOCTLs
1. Define IOCTL code in `nvidia_compat.c`
2. Add handler in `nvidia_compat_ioctl()`
3. Implement forwarding or fake response
4. Test with real application

### Testing
```bash
# Build
make

# Load
sudo make load

# Test
make test

# View logs
sudo dmesg | tail -20

# Unload
sudo make unload
```

## License

MIT License - See ../LICENSE file for details

Part of shittyNVIDIA - The worst NVIDIA driver ever
https://github.com/P4X-ng/shittyNVIDIA

## Contributing

Contributions welcome! This module could be enhanced with:
- More IOCTL implementations
- Better nvidia-smi integration
- Improved CUDA support
- Multiple fake GPU support
- Performance metrics
- Better error handling

## Disclaimer

This is part of shittyNVIDIA, a parody project. While the kernel module is functional, it's primarily for educational and entertainment purposes. For production NVIDIA support, use official NVIDIA drivers.

The module can interact with real NVIDIA drivers if present, but makes no guarantees about compatibility or stability.
