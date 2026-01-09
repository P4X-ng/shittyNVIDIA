# GPU Driver IOCTL Comparison

This document provides a side-by-side comparison of NVIDIA and AMD open source GPU drivers, focusing on their IOCTL interfaces for GPU compute operations.

## Executive Summary

| Aspect | NVIDIA (open-gpu-kernel-modules) | AMD (AMDGPU) |
|--------|----------------------------------|--------------|
| **Repository** | [NVIDIA/open-gpu-kernel-modules](https://github.com/NVIDIA/open-gpu-kernel-modules) | Part of [Linux Kernel](https://github.com/torvalds/linux) |
| **License** | Dual GPL/MIT | MIT |
| **Kernel Integration** | External module | Mainline kernel |
| **Supported GPUs** | Turing+ (2018+) | GCN 1.2+ (2014+) |
| **DRM Integration** | Wrapper around custom driver | Native DRM driver |
| **User-space** | Proprietary (libcuda.so) | Open source (ROCm, Mesa) |
| **Compute API** | CUDA | ROCm/HIP |
| **Primary IOCTL Device** | `/dev/nvidiactl`, `/dev/nvidia*` | `/dev/dri/renderD*`, `/dev/kfd` |

## IOCTL Architecture Comparison

### NVIDIA Architecture

```
User Application (CUDA)
    ↓
libcuda.so (proprietary)
    ↓
IOCTL Interface
    ↓
nvidia.ko (open source)
    ↓
GSP Firmware (proprietary, on-GPU)
    ↓
Hardware
```

**Key Points**:
- Custom IOCTL interface (NV_ESC_* commands)
- Relies on GSP firmware for hardware abstraction
- Multiple specialized modules (nvidia, nvidia-uvm, nvidia-modeset)
- User-space driver (libcuda.so) is proprietary

### AMD Architecture

```
User Application (HIP/ROCm)
    ↓
ROCm Libraries (open source)
    ↓
DRM IOCTL Interface
    ↓
amdgpu.ko (open source)
    ↓
Hardware
```

**Key Points**:
- Standard DRM IOCTLs + AMD extensions
- Native kernel implementation (no firmware abstraction layer)
- Single unified module (amdgpu)
- Fully open source stack

## Device File Comparison

### NVIDIA Device Files

| Device File | Purpose |
|-------------|---------|
| `/dev/nvidiactl` | Control device for driver operations |
| `/dev/nvidia0`, `/dev/nvidia1`, ... | Per-GPU device nodes |
| `/dev/nvidia-uvm` | Unified Virtual Memory (CUDA) |
| `/dev/nvidia-modeset` | Display mode setting |
| `/dev/nvidia-drm` | DRM integration |

### AMD Device Files

| Device File | Purpose |
|-------------|---------|
| `/dev/dri/card0`, `/dev/dri/card1`, ... | Per-GPU device (graphics + compute) |
| `/dev/dri/renderD128`, `/dev/dri/renderD129`, ... | Compute-only render nodes |
| `/dev/kfd` | ROCm compute interface (HSA) |

**Key Difference**: AMD uses standard DRM device nodes, NVIDIA uses custom device nodes.

## IOCTL Categories Comparison

### Memory Management

#### NVIDIA

```c
NV_ESC_RM_ALLOC_MEMORY      // Allocate GPU memory
NV_ESC_RM_MAP_MEMORY        // Map memory for access
NV_ESC_RM_UNMAP_MEMORY      // Unmap memory
NV_ESC_RM_FREE              // Free GPU resource

// UVM-specific
UVM_MAP_EXTERNAL_ALLOCATION // Map external memory
UVM_FREE                    // Free UVM memory
UVM_MIGRATE                 // Migrate pages CPU↔GPU
```

**Characteristics**:
- Custom NVIDIA-specific interface
- Separate UVM module for CUDA unified memory
- Proprietary resource management (RM)

#### AMD

```c
DRM_IOCTL_AMDGPU_GEM_CREATE    // Allocate buffer object
DRM_IOCTL_AMDGPU_GEM_MMAP      // Map for CPU access
DRM_IOCTL_AMDGPU_GEM_VA        // Map to GPU virtual address
DRM_IOCTL_AMDGPU_GEM_USERPTR   // Use user memory as GPU buffer
DRM_IOCTL_GEM_CLOSE            // Close/free buffer
```

**Characteristics**:
- Standard DRM GEM interface
- Built on Linux TTM (Translation Table Maps)
- Multiple memory domains (VRAM, GTT, CPU)

### Command Submission

#### NVIDIA

```c
NV_ESC_RM_ALLOC_CONTEXT     // Create GPU context
NV_ESC_RM_ALLOC_CHANNEL     // Allocate command channel
NV_ESC_RM_CONTROL           // Execute command

// UVM channels
UVM_REGISTER_CHANNEL        // Register command channel
```

**Characteristics**:
- Abstract "resource manager" interface
- Commands sent to GSP firmware
- Context and channel abstraction

#### AMD

```c
DRM_IOCTL_AMDGPU_CTX        // Context management (create/destroy)
DRM_IOCTL_AMDGPU_CS         // Command submission
DRM_IOCTL_AMDGPU_WAIT_CS    // Wait for completion
```

**Characteristics**:
- Direct command buffer submission
- Hardware scheduler manages queues
- Standard DRM approach with AMD extensions

### Device Information

#### NVIDIA

```c
NV_ESC_CHECK_VERSION        // Driver version check
NV_ESC_CARD_INFO            // Get GPU card information
NV_ESC_QUERY_DEVICE_INFO    // Query device capabilities
```

**Characteristics**:
- Custom query interface
- Version compatibility checking
- Device enumeration

#### AMD

```c
DRM_IOCTL_VERSION           // Standard DRM version
DRM_IOCTL_AMDGPU_INFO       // Comprehensive device info
```

**Query Types**:
- `AMDGPU_INFO_ACCEL_WORKING` - Is GPU compute working?
- `AMDGPU_INFO_VRAM_USAGE` - Memory usage
- `AMDGPU_INFO_FW_VERSION` - Firmware versions
- `AMDGPU_INFO_HW_IP_INFO` - Hardware IP blocks
- `AMDGPU_INFO_DEV_INFO` - Device capabilities

**Characteristics**:
- Rich query interface
- Standard DRM base + AMD extensions
- Detailed hardware introspection

## CUDA vs ROCm Workflow Comparison

### NVIDIA CUDA Workflow

```c
// 1. Initialize
open("/dev/nvidiactl");
ioctl(nvidiactl, NV_ESC_CHECK_VERSION);
open("/dev/nvidia0");
open("/dev/nvidia-uvm");
ioctl(uvm, UVM_INITIALIZE);
ioctl(uvm, UVM_REGISTER_GPU);

// 2. Allocate memory
ioctl(nvidia0, NV_ESC_RM_ALLOC_MEMORY);
ioctl(uvm, UVM_MAP_EXTERNAL_ALLOCATION);

// 3. Launch kernel
ioctl(nvidia0, NV_ESC_RM_ALLOC_CONTEXT);
ioctl(nvidia0, NV_ESC_RM_ALLOC_CHANNEL);
ioctl(nvidia0, NV_ESC_RM_CONTROL);  // Submit work

// 4. Synchronize
ioctl(uvm, UVM_WAIT_FOR_IDLE);

// 5. Cleanup
ioctl(nvidia0, NV_ESC_RM_FREE);
ioctl(uvm, UVM_DEINITIALIZE);
```

### AMD ROCm/HIP Workflow

```c
// 1. Initialize
open("/dev/kfd");
ioctl(kfd, AMDKFD_IOC_GET_VERSION);
open("/dev/dri/renderD128");

// 2. Allocate memory
ioctl(renderD128, DRM_IOCTL_AMDGPU_GEM_CREATE);
ioctl(renderD128, DRM_IOCTL_AMDGPU_GEM_VA);  // Map to GPU VA

// 3. Create context
ioctl(renderD128, DRM_IOCTL_AMDGPU_CTX, AMDGPU_CTX_OP_ALLOC);

// 4. Submit kernel
// (prepare command buffer with compute dispatch)
ioctl(renderD128, DRM_IOCTL_AMDGPU_CS);  // Submit

// 5. Synchronize
ioctl(renderD128, DRM_IOCTL_AMDGPU_WAIT_CS);

// 6. Cleanup
ioctl(renderD128, DRM_IOCTL_AMDGPU_CTX, AMDGPU_CTX_OP_FREE);
ioctl(renderD128, DRM_IOCTL_GEM_CLOSE);
```

### Key Differences

| Aspect | NVIDIA | AMD |
|--------|--------|-----|
| **Device Files** | Multiple specialized | Single unified (renderD) |
| **Initialization** | Multi-stage (ctl + dev + uvm) | Simple (kfd + renderD) |
| **Memory Allocation** | Two-stage (alloc + map) | Single GEM operation |
| **Context Creation** | Implicit in channel | Explicit context IOCTL |
| **Submission** | Abstract RM_CONTROL | Direct CS submission |
| **Sync** | UVM-specific | Standard fence-based |

## Unified Memory Comparison

### NVIDIA UVM (Unified Virtual Memory)

**Module**: `nvidia-uvm.ko`

**Key IOCTLs**:
```c
UVM_REGISTER_GPU            // Register GPU with UVM
UVM_MIGRATE                 // Migrate pages between CPU/GPU
UVM_SET_PREFERRED_LOCATION  // Set preferred memory location
UVM_SET_ACCESSED_BY         // Track access patterns
UVM_ENABLE_PEER_ACCESS      // GPU-to-GPU access
```

**Features**:
- Automatic page migration
- Fault-driven migration
- GPU-to-GPU peer access
- Access tracking for optimization
- Zero-copy memory

**Architecture**: Dedicated kernel module managing unified memory

### AMD Shared Virtual Memory

**Integration**: Built into amdgpu.ko

**Key IOCTLs**:
```c
DRM_IOCTL_AMDGPU_GEM_USERPTR  // Use CPU memory as GPU buffer
DRM_IOCTL_AMDGPU_GEM_VA        // Virtual address mapping
```

**Features**:
- USERPTR for zero-copy
- HSA shared virtual memory (via /dev/kfd)
- System allocator integration
- Page fault handling

**Architecture**: Integrated into main driver using Linux page fault mechanism

### Comparison

| Feature | NVIDIA UVM | AMD SVM |
|---------|------------|---------|
| **Implementation** | Dedicated module | Integrated in driver |
| **Migration** | Explicit migration IOCTLs | Fault-driven + hints |
| **API Complexity** | More IOCTLs, finer control | Simpler, standard Linux VM |
| **Zero-Copy** | UVM_MAP_EXTERNAL_ALLOCATION | GEM_USERPTR |
| **Peer Access** | Explicit enable/disable | Automatic |

## Synchronization Mechanisms

### NVIDIA

```c
NV_ESC_ALLOC_OS_EVENT       // Create event
NV_ESC_FREE_OS_EVENT        // Destroy event
NV_ESC_WAIT_OPEN_COMPLETE   // Wait for completion
UVM_WAIT_FOR_IDLE           // Wait for GPU idle
```

**Approach**: Custom event system

### AMD

```c
DRM_IOCTL_AMDGPU_WAIT_CS        // Wait for command completion
DRM_IOCTL_AMDGPU_FENCE_TO_HANDLE // Convert fence to handle
// Uses standard DRM sync objects
```

**Approach**: DRM sync objects and fences (standard Linux mechanism)

## Performance Characteristics

### NVIDIA

- **IOCTL Overhead**: ~1-10 μs
- **Latency**: Low (direct to GSP firmware)
- **Throughput**: High (hardware scheduling on GPU)
- **Zero-Copy**: Via UVM
- **Peer Transfer**: Direct GPU-to-GPU via UVM

### AMD

- **IOCTL Overhead**: ~1-5 μs
- **Latency**: Very low (direct to hardware)
- **Throughput**: High (GPU scheduler in driver)
- **Zero-Copy**: Via USERPTR
- **Peer Transfer**: Direct GPU-to-GPU via DMA

**Performance**: Both drivers provide excellent performance with different trade-offs in flexibility vs. overhead.

## Security Model

### NVIDIA

- **Device Permissions**: `/dev/nvidia*` permissions
- **Isolation**: Per-process contexts
- **Validation**: GSP firmware validates commands
- **Memory Protection**: IOMMU + driver checks

### AMD

- **Device Permissions**: `/dev/dri/*` permissions
- **Isolation**: Per-process GPU virtual address spaces
- **Validation**: Kernel validates command buffers
- **Memory Protection**: IOMMU + TTM memory manager

**Security**: Both provide strong isolation and protection.

## Developer Experience

### NVIDIA

**Pros**:
- Mature CUDA ecosystem
- Extensive documentation
- Wide adoption
- Advanced debugging tools (cuda-gdb, nsight)

**Cons**:
- Proprietary user-space (libcuda.so)
- Custom IOCTL interface
- Less kernel integration
- External module maintenance

### AMD

**Pros**:
- Fully open source
- Standard DRM interface
- Mainline kernel integration
- Community development

**Cons**:
- Less mature ROCm ecosystem
- Smaller developer community
- Less comprehensive documentation
- Fewer third-party tools

## Use Cases

### When to Use NVIDIA

- CUDA-specific applications
- Maximum software ecosystem compatibility
- Advanced GPU features (RT cores, Tensor cores)
- Enterprise support requirements

### When to Use AMD

- Open source requirement
- Standard Linux integration
- Graphics + compute workloads
- Price/performance optimization
- Avoiding vendor lock-in

## Future Directions

### NVIDIA

- Increased open source adoption
- Better GSP firmware documentation
- More kernel integration
- Community contributions

### AMD

- ROCm maturity improvements
- Better CUDA compatibility (HIP)
- Enhanced compute features
- Performance optimizations

## Conclusion

Both NVIDIA and AMD provide comprehensive IOCTL interfaces for GPU operations:

- **NVIDIA**: Custom, mature, CUDA-focused with proprietary user-space
- **AMD**: Standards-based, fully open, DRM-integrated

The choice depends on:
- Software ecosystem requirements (CUDA vs ROCm)
- Open source policy
- Hardware availability
- Performance requirements
- Development preferences

For **maximum performance and ecosystem**: NVIDIA CUDA  
For **maximum openness and integration**: AMD AMDGPU

**Want to run CUDA code on AMD hardware?** See our comprehensive [CUDA to AMD Compatibility Guide](CUDA_AMD_COMPATIBILITY.md) covering HIP translation, ZLUDA, and other compatibility approaches.

## References

- [NVIDIA Open GPU Kernel Modules](https://github.com/NVIDIA/open-gpu-kernel-modules)
- [AMD AMDGPU Kernel Driver](https://github.com/torvalds/linux/tree/master/drivers/gpu/drm/amd/amdgpu)
- [Linux DRM Documentation](https://dri.freedesktop.org/docs/drm/)
- [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)
- [ROCm Documentation](https://rocm.docs.amd.com/)
