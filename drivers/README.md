# GPU Driver IOCTL Analysis

Welcome to the comprehensive analysis of NVIDIA and AMD open source GPU drivers!

## What's Inside

This directory contains detailed technical analysis of GPU driver IOCTL interfaces:

### 📂 Documentation

1. **[NVIDIA Open Source Driver](nvidia/)** - `drivers/nvidia/README.md`
   - Analysis of [NVIDIA/open-gpu-kernel-modules](https://github.com/NVIDIA/open-gpu-kernel-modules)
   - Complete IOCTL reference for CUDA operations
   - Unified Virtual Memory (UVM) architecture
   - GSP firmware communication
   - Command submission and synchronization
   - Security and performance characteristics

2. **[AMD AMDGPU Driver](amd/)** - `drivers/amd/README.md`
   - Analysis of AMD's mainline Linux kernel driver
   - DRM/GEM IOCTL interface
   - ROCm compute stack integration
   - Memory domain management (VRAM, GTT, system)
   - Hardware IP block architecture
   - Command submission and GPU scheduler

3. **[Comparison Document](COMPARISON.md)** - `drivers/COMPARISON.md`
   - Side-by-side comparison of NVIDIA vs AMD
   - IOCTL architecture differences
   - CUDA vs ROCm workflows
   - Performance characteristics
   - Developer experience
   - Use case recommendations

4. **[IOCTL Mappings](IOCTL_MAPPINGS.md)** - `drivers/IOCTL_MAPPINGS.md`
   - Cross-platform operation mappings (AMD ↔ NVIDIA ↔ CUDA ↔ CPU)
   - Memory management operation equivalents
   - Execution and synchronization mappings
   - Practical examples with code snippets
   - Performance comparison tables

5. **[CUDA to AMD Compatibility](CUDA_AMD_COMPATIBILITY.md)** - `drivers/CUDA_AMD_COMPATIBILITY.md`
   - Comprehensive guide to running CUDA code on AMD hardware
   - Source translation (HIP) - Production ready
   - Runtime translation (ZLUDA) - Experimental binary compatibility
   - IOCTL interception layer - Theoretical approach
   - Unified driver architecture - Long-term vision
   - Performance analysis and recommendations
   - Real-world examples and best practices

6. **[IOCTL Forwarding Architecture](../IOCTL_FORWARDING_ARCHITECTURE.md)** - Root directory 🆕
   - **Hybrid NVIDIA-AMD compatibility layer design**
   - The Router Concept: Trick Linux into routing to our layer instead of NVIDIA driver
   - OSS NVIDIA Integration: Use NVIDIA's open source driver as a component
   - CUDA IOCTL Forwarding: Forward CUDA IOCTLs, translate hardware operations to AMD
   - Complete technical architecture with detailed diagrams
   - Implementation techniques and code examples
   - Comprehensive advantages/disadvantages analysis
   - Feasibility assessment and practical recommendations

## Quick Overview

### NVIDIA Architecture

```
Application → libcuda.so → nvidia.ko + nvidia-uvm.ko → GSP Firmware → GPU
                            ↓
                       Custom IOCTLs
                       /dev/nvidiactl
                       /dev/nvidia*
                       /dev/nvidia-uvm
```

**Key Characteristics**:
- Custom IOCTL interface
- Separate UVM module for CUDA unified memory
- GSP firmware handles hardware abstraction
- Proprietary user-space (libcuda.so)
- Supports Turing+ GPUs (2018+)

### AMD Architecture

```
Application → ROCm/Mesa → amdgpu.ko → GPU Hardware
                          ↓
                     DRM IOCTLs
                     /dev/dri/renderD*
                     /dev/kfd
```

**Key Characteristics**:
- Standard DRM IOCTL interface + AMD extensions
- Native Linux kernel driver
- Fully open source stack
- Mainline kernel integration
- Supports GCN 1.2+ (2014+)

## IOCTL Categories

Both drivers provide IOCTLs for:

1. **Memory Management**
   - Buffer allocation
   - CPU/GPU mapping
   - Zero-copy operations
   - Memory migration

2. **Command Submission**
   - GPU context management
   - Work submission
   - Command buffer execution

3. **Synchronization**
   - Fence/event mechanisms
   - CPU/GPU sync
   - Multi-GPU coordination

4. **Device Information**
   - Capability queries
   - Memory usage
   - Firmware versions

5. **Display Management** (if applicable)
   - Mode setting
   - Output configuration

## Key Differences

| Aspect | NVIDIA | AMD |
|--------|--------|-----|
| **License** | Dual GPL/MIT (kernel only) | MIT (full stack) |
| **User-space** | Proprietary | Open source |
| **IOCTL Style** | Custom | DRM standard + extensions |
| **Integration** | External module | Mainline kernel |
| **Compute API** | CUDA | ROCm/HIP |
| **Memory Model** | UVM (dedicated module) | GEM/TTM (integrated) |

## Who Should Read This?

- **Driver Developers**: Understanding kernel-level GPU interfaces
- **GPU Programmers**: Learning how CUDA/ROCm interact with hardware
- **System Programmers**: Understanding IOCTL mechanisms
- **Students**: Learning GPU architecture and OS interaction
- **Curious Minds**: Understanding how GPUs really work

## Prerequisites

To fully understand this documentation, you should be familiar with:
- Linux kernel concepts (system calls, IOCTLs, memory management)
- C programming
- GPU basics (memory hierarchy, compute units)
- Operating systems concepts (virtual memory, DMA)

## Getting Started

Start with the comparison document if you want a high-level overview, then dive into the specific driver documentation based on your interest:

1. **Start Here**: [COMPARISON.md](COMPARISON.md) - Get the big picture
2. **NVIDIA Deep Dive**: [nvidia/README.md](nvidia/README.md) - For CUDA developers
3. **AMD Deep Dive**: [amd/README.md](amd/README.md) - For ROCm developers
4. 🆕 **Cross-Platform Mappings**: [IOCTL_MAPPINGS.md](IOCTL_MAPPINGS.md) - See how operations correspond across platforms

## Real-World Applications

Understanding these IOCTL interfaces is valuable for:

- **GPU Driver Development**: Contributing to or creating GPU drivers
- **Compute Framework Development**: Building CUDA/ROCm alternatives
- **Debugging**: Troubleshooting GPU application issues
- **Performance Optimization**: Understanding overhead and bottlenecks
- **Security Research**: Understanding GPU attack surfaces
- **Virtualization**: GPU passthrough and sharing
- **Container Technology**: GPU containerization (e.g., nvidia-docker)

## Source Repositories

- **NVIDIA**: [github.com/NVIDIA/open-gpu-kernel-modules](https://github.com/NVIDIA/open-gpu-kernel-modules)
- **AMD**: [github.com/torvalds/linux (drivers/gpu/drm/amd/amdgpu)](https://github.com/torvalds/linux/tree/master/drivers/gpu/drm/amd/amdgpu)
- **ROCm**: [github.com/ROCm](https://github.com/ROCm)
- **GPUOpen**: [github.com/GPUOpen-Drivers](https://github.com/GPUOpen-Drivers)

## Tools for Exploration

Want to see these IOCTLs in action?

```bash
# Trace IOCTL calls from a CUDA program
strace -e ioctl -y ./cuda_program 2>&1 | grep -E 'nvidia|dri'

# Trace IOCTL calls from a ROCm program
strace -e ioctl -y ./hip_program 2>&1 | grep -E 'kfd|renderD'

# Monitor GPU memory
# NVIDIA
nvidia-smi --query-gpu=memory.used,memory.free --format=csv -l 1

# AMD
cat /sys/kernel/debug/dri/0/amdgpu_vram_mm
```

## Contributing

Found an error or want to add more analysis? This documentation was created as part of the shittyNVIDIA project (yes, really). While shittyNVIDIA itself is a parody, this driver analysis is serious technical documentation.

## Disclaimer

This analysis is based on publicly available open source code and documentation. It is intended for educational purposes. Always refer to official documentation for production use.

- **NVIDIA**: While the kernel module is open source, user-space libraries remain proprietary
- **AMD**: Fully open source, but always check official ROCm documentation for the latest APIs

## Further Reading

### NVIDIA Resources
- [NVIDIA Driver Documentation](https://docs.nvidia.com/cuda/)
- [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)
- [Open GPU Kernel Modules README](https://github.com/NVIDIA/open-gpu-kernel-modules/blob/main/README.md)

### AMD Resources
- [AMDGPU Kernel Documentation](https://docs.kernel.org/gpu/amdgpu/index.html)
- [ROCm Documentation](https://rocm.docs.amd.com/)
- [Linux DRM Documentation](https://dri.freedesktop.org/docs/drm/)

### General GPU Resources
- [Kernel Mode Setting](https://en.wikipedia.org/wiki/Mode_setting)
- [Direct Rendering Manager](https://en.wikipedia.org/wiki/Direct_Rendering_Manager)
- [Graphics Execution Manager](https://lwn.net/Articles/283798/)

---

Made with 🔍 for understanding how GPUs really work

*Part of the shittyNVIDIA project - Because even a joke project should have serious documentation*
