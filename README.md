# shittyNVIDIA

The worst NVIDIA driver ever - works with 0 nvidia devices, this is: shittyNVIDIA

## Overview

shittyNVIDIA is a humorous "driver" that implements nvidia-compat concepts without actually doing anything useful. Based on code patterns from [HyperionGray/pf-web-poly-compile-helper-runner](https://github.com/HyperionGray/pf-web-poly-compile-helper-runner), this project demonstrates what happens when you take NVIDIA compatibility seriously... but backwards.

**Key Features:**
- ✅ Works with exactly **0** NVIDIA devices
- ✅ Guaranteed incompatibility with all NVIDIA hardware
- ✅ Zero performance overhead (does nothing!)
- ✅ No bloatware or unnecessary features
- ✅ Perfect for systems without NVIDIA GPUs

## Why?

Because sometimes you need a driver that:
1. Doesn't work
2. Proudly announces it doesn't work
3. Makes you laugh about it

## Real GPU Driver Analysis

But seriously, if you want to understand how **real** GPU drivers work, we've done the hard work for you:

📚 **[Driver Analysis Documentation](drivers/)**

- **[NVIDIA Open Source Driver Analysis](drivers/nvidia/)** - Deep dive into NVIDIA's open-gpu-kernel-modules
  - Complete IOCTL reference for CUDA operations
  - UVM (Unified Virtual Memory) architecture
  - GSP firmware interaction
  - Command submission workflow
  
- **[AMD AMDGPU Driver Analysis](drivers/amd/)** - Analysis of the AMD open source driver
  - DRM/GEM IOCTL interface
  - ROCm compute stack
  - Memory domain management
  - Hardware IP blocks
  
- **[NVIDIA vs AMD Comparison](drivers/COMPARISON.md)** - Side-by-side comparison
  - IOCTL architecture differences
  - CUDA vs ROCm workflows
  - Performance characteristics
  - Developer experience

This comprehensive analysis covers the IOCTL interfaces for both NVIDIA and AMD open source GPU drivers, perfect for understanding GPU kernel interfaces, driver development, or just being curious about how your GPU actually talks to the kernel!

## Installation

### Requirements

- **NO NVIDIA hardware** (seriously, this is required)
- Linux system
- Bash
- Python 3.6+
- A sense of humor

### Quick Install

```bash
# Clone the repository
git clone https://github.com/P4X-ng/shittyNVIDIA.git
cd shittyNVIDIA

# Run the installer
chmod +x install-nvidia-compat.sh
./install-nvidia-compat.sh install
```

### Python Package

```bash
pip install -e .
```

## Usage

### Command Line

After installation, you can use the stub `nvidia-smi`:

```bash
nvidia-smi
```

Output:
```
shittyNVIDIA v0.0.0
The worst NVIDIA driver ever - works with 0 nvidia devices

ERROR: No NVIDIA devices found (as designed!)

This is shittyNVIDIA. We don't support ANY NVIDIA hardware.
If you have NVIDIA hardware, please use a real driver.
```

### Python API

```python
import shitty_nvidia

# Check compatibility (returns True if NO NVIDIA found)
if shitty_nvidia.check_compatibility():
    print("Perfect! No NVIDIA devices found!")

# Get device count (always returns 0)
count = shitty_nvidia.get_device_count()
print(f"Found {count} devices")  # Always prints: Found 0 devices

# Get driver info
info = shitty_nvidia.get_driver_info()
print(info['description'])

# Try to create a device (will always fail)
try:
    device = shitty_nvidia.Device(0)
except shitty_nvidia.NoDeviceError as e:
    print(f"Failed as expected: {e}")
```

## Technical Details

### What It Does

The `install-nvidia-compat.sh` script:
1. Checks that NO NVIDIA hardware is present
2. Creates fake NVIDIA directory structure at `/usr/local/shittyNVIDIA/`
3. Installs stub executables and libraries
4. Creates kernel module blacklists to prevent real NVIDIA drivers
5. Configures environment variables

### Structure

```
shittyNVIDIA/
├── install-nvidia-compat.sh    # Installation script
├── shitty_nvidia/              # Python package
│   └── __init__.py            # Main module
├── setup.py                    # Python package setup
└── README.md                   # This file
```

### What Gets Installed

- `/usr/local/shittyNVIDIA/bin/nvidia-smi` - Stub that always fails
- `/usr/local/shittyNVIDIA/compat/` - Empty compatibility directory
- `/usr/local/shittyNVIDIA/lib64/` - Empty library directory
- `/etc/modprobe.d/shitty-nvidia-blacklist.conf` - Blacklist file

## Uninstall

```bash
./install-nvidia-compat.sh uninstall
```

## Testing

```bash
# Test the installation
./install-nvidia-compat.sh test

# Or manually
nvidia-smi  # Should fail with shittyNVIDIA message
```

## Origin

This project is based on nvidia-compat installation patterns found in [HyperionGray/pf-web-poly-compile-helper-runner](https://github.com/HyperionGray/pf-web-poly-compile-helper-runner), specifically the `scripts/install-containers.sh` file which contains logic for installing the NVIDIA Container Toolkit.

We took that serious, production-ready code and turned it into... this.

## License

MIT License - See LICENSE file for details

## Disclaimer

**This is a parody project.** Do not use in production. Do not use anywhere. If you have actual NVIDIA hardware, please use the official NVIDIA drivers from [https://www.nvidia.com/](https://www.nvidia.com/).

shittyNVIDIA is not affiliated with, endorsed by, or in any way officially connected with NVIDIA Corporation.

## Contributing

Want to make shittyNVIDIA even worse? Contributions welcome! Just remember:
- It must work with 0 NVIDIA devices
- It must be hilarious
- It must be well-documented (even if it does nothing)

## FAQ

**Q: Will this work with my NVIDIA GPU?**  
A: No. That's the whole point.

**Q: Can I use this for CUDA development?**  
A: No. It doesn't support CUDA, or anything else.

**Q: Why does this exist?**  
A: Why not?

**Q: Is this a real NVIDIA driver?**  
A: Absolutely not. This is shittyNVIDIA.

**Q: Can I use this in production?**  
A: Please don't.

## Related Projects

- [NVIDIA Driver Downloads](https://www.nvidia.com/Download/index.aspx) - For actual NVIDIA support
- [HyperionGray/pf-web-poly-compile-helper-runner](https://github.com/HyperionGray/pf-web-poly-compile-helper-runner) - The source of our nvidia-compat inspiration

---

Made with ❌ for NVIDIA hardware
