# AMD Open Source Driver (AMDGPU) Analysis

## Overview

This document analyzes the AMD open source GPU driver (AMDGPU), focusing on the IOCTL interface used for GPU compute and graphics operations.

## Source Repository

- **Kernel Driver**: Part of mainline Linux kernel
  - Location: `drivers/gpu/drm/amd/amdgpu/` in Linux kernel tree
  - [GitHub Mirror](https://github.com/torvalds/linux/tree/master/drivers/gpu/drm/amd/amdgpu)
- **User-space Components**: [GPUOpen-Drivers](https://github.com/orgs/GPUOpen-Drivers/repositories)
  - AMDVLK (Vulkan driver)
  - PAL (Platform Abstraction Library)
  - LLPC (LLVM-based Pipeline Compiler)
- **ROCm Stack**: [ROCm GitHub](https://github.com/ROCm)
  - HIP (CUDA-equivalent API)
  - ROCm-Kernel-Driver
- **License**: MIT (kernel driver), various open source licenses (user-space)
- **Supported GPUs**: GCN 1.2+ (GCN, RDNA, CDNA architectures)

## Architecture

The AMDGPU driver is structured as a DRM (Direct Rendering Manager) driver:

### Core Components

1. **amdgpu.ko** - Main kernel module
   - Device initialization
   - Memory management (VRAM, GTT, system memory)
   - Command submission and scheduling
   - Power management (DPM, PowerPlay)
   - Hardware register access

2. **amdgpu_dm.ko** - Display Manager
   - Display Core Next (DCN) support
   - Atomic modesetting
   - FreeSync/VRR support
   - HDR and color management

3. **GPU Scheduler**
   - Fair scheduling between processes
   - Hardware queue management
   - Fence/sync mechanisms

4. **Memory Manager (TTM)**
   - VRAM allocation
   - GTT (Graphics Translation Table)
   - Buffer migration
   - Eviction and swapping

## DRM Subsystem Integration

AMDGPU uses Linux DRM framework:
- **GEM (Graphics Execution Manager)**: Memory management
- **KMS (Kernel Mode Setting)**: Display control
- **DRM Scheduler**: GPU command submission

## Directory Structure

```
drivers/gpu/drm/amd/
├── amdgpu/              # Main AMDGPU driver
│   ├── amdgpu_drv.c    # Driver registration and IOCTLs
│   ├── amdgpu_gem.c    # GEM object management
│   ├── amdgpu_cs.c     # Command submission
│   ├── amdgpu_vm.c     # Virtual memory management
│   ├── amdgpu_device.c # Device initialization
│   ├── amdgpu_kms.c    # KMS implementation
│   └── ...
├── display/             # Display driver (DC)
├── pm/                  # Power management
└── include/             # Headers (amdgpu_drm.h)
```

## IOCTL Interface

### Device Files

AMDGPU exposes device files through DRM:

- `/dev/dri/card0`, `/dev/dri/card1`, ... - GPU devices
- `/dev/dri/renderD128`, `/dev/dri/renderD129`, ... - Compute-only nodes
- `/dev/kfd` - Compute device (HSA/ROCm interface)

### IOCTL Categories

#### 1. Generic DRM IOCTLs

Standard DRM IOCTLs available for all DRM drivers:

```
DRM_IOCTL_VERSION           - Get driver version
DRM_IOCTL_GET_UNIQUE        - Get device unique identifier
DRM_IOCTL_GET_MAGIC         - Get authentication magic
DRM_IOCTL_AUTH_MAGIC        - Authenticate client
DRM_IOCTL_SET_MASTER        - Become DRM master
DRM_IOCTL_DROP_MASTER       - Drop master privileges
```

**Purpose**: Basic driver information and authentication.

#### 2. GEM (Graphics Execution Manager) IOCTLs

Memory object management:

```
DRM_IOCTL_GEM_CLOSE         - Close GEM handle
DRM_IOCTL_GEM_FLINK         - Create global name for GEM object
DRM_IOCTL_GEM_OPEN          - Open GEM object by name
DRM_IOCTL_PRIME_HANDLE_TO_FD - Export GEM as DMA-BUF file descriptor
DRM_IOCTL_PRIME_FD_TO_HANDLE - Import DMA-BUF as GEM object
```

**Purpose**: Share buffers between processes and devices.

#### 3. AMDGPU-Specific IOCTLs

##### 3.1 Buffer Object Management

```c
#define DRM_AMDGPU_GEM_CREATE       0x00
#define DRM_AMDGPU_GEM_MMAP         0x01
#define DRM_AMDGPU_GEM_USERPTR      0x03
#define DRM_AMDGPU_GEM_WAIT_IDLE    0x09
#define DRM_AMDGPU_GEM_VA           0x05
```

**DRM_AMDGPU_GEM_CREATE**: Allocate GPU memory buffer
```c
struct drm_amdgpu_gem_create {
    __u64 bo_size;              // Buffer size in bytes
    __u64 alignment;            // Alignment requirement
    __u64 domains;              // Memory domain flags (VRAM, GTT, etc.)
    __u64 flags;                // Creation flags
    __u32 handle;               // Output: GEM handle
    __u32 _pad;
};
```

**Purpose**: Allocate buffers in VRAM (video memory), GTT (GPU Translation Table), or system memory.

**DRM_AMDGPU_GEM_MMAP**: Map buffer for CPU access
```c
struct drm_amdgpu_gem_mmap {
    __u32 handle;               // GEM handle
    __u32 _pad;
    __u64 offset;               // Output: mmap offset
};
```

**Purpose**: Enable CPU to read/write GPU buffers.

**DRM_AMDGPU_GEM_USERPTR**: Use user-space memory as GPU buffer
```c
struct drm_amdgpu_gem_userptr {
    __u64 addr;                 // User-space pointer
    __u64 size;                 // Buffer size
    __u32 flags;                // Flags
    __u32 handle;               // Output: GEM handle
};
```

**Purpose**: Allow GPU to access CPU-allocated memory without copying (zero-copy).

**DRM_AMDGPU_GEM_VA**: Map buffer to GPU virtual address
```c
struct drm_amdgpu_gem_va {
    __u32 handle;               // GEM handle
    __u32 operation;            // MAP/UNMAP/REPLACE
    __u32 flags;                // Mapping flags
    __u32 vm_id;                // Virtual memory context
    __u64 offset;               // Offset in buffer
    __u64 va_address;           // GPU virtual address
    __u64 map_size;             // Size to map
};
```

**Purpose**: Establish GPU virtual address space mappings.

##### 3.2 Command Submission

```c
#define DRM_AMDGPU_CS               0x04
#define DRM_AMDGPU_WAIT_CS          0x09
#define DRM_AMDGPU_FENCE_TO_HANDLE  0x21
```

**DRM_AMDGPU_CS**: Submit commands to GPU
```c
struct drm_amdgpu_cs_in {
    __u32 ctx_id;               // Context ID
    __u32 bo_list_handle;       // Buffer object list
    __u32 num_chunks;           // Number of command chunks
    __u32 _pad;
    __u64 chunks;               // Pointer to chunk array
};

struct drm_amdgpu_cs_chunk {
    __u32 chunk_id;             // Chunk type (IB, FENCE, etc.)
    __u32 length_dw;            // Length in dwords
    __u64 chunk_data;           // Pointer to chunk data
};
```

**Chunk Types**:
- `AMDGPU_CHUNK_ID_IB`: Indirect Buffer (command buffer)
- `AMDGPU_CHUNK_ID_FENCE`: Fence for synchronization
- `AMDGPU_CHUNK_ID_DEPENDENCIES`: Job dependencies
- `AMDGPU_CHUNK_ID_SYNCOBJ_IN`: Input sync objects
- `AMDGPU_CHUNK_ID_SYNCOBJ_OUT`: Output sync objects

**Purpose**: Submit GPU workloads (compute kernels, graphics commands, DMA operations).

**DRM_AMDGPU_WAIT_CS**: Wait for command completion
```c
struct drm_amdgpu_wait_cs {
    __u32 handle;               // CS handle
    __u32 timeout;              // Timeout in nanoseconds
    __u32 ip_type;              // IP block type
    __u32 ip_instance;
    __u32 ring;                 // Ring index
    __u32 ctx_id;               // Context ID
    __u64 out_seq_no;           // Output: sequence number
};
```

**Purpose**: Synchronize with GPU execution.

##### 3.3 Context Management

```c
#define DRM_AMDGPU_CTX              0x02
```

**DRM_AMDGPU_CTX**: Manage GPU contexts
```c
struct drm_amdgpu_ctx {
    __u32 op;                   // CREATE/DESTROY/QUERY
    __u32 flags;
    __u32 ctx_id;               // Context ID
    __u32 _pad;
};
```

**Purpose**: Create isolated GPU execution contexts for processes.

##### 3.4 Device Information Query

```c
#define DRM_AMDGPU_INFO             0x06
```

**DRM_AMDGPU_INFO**: Query device capabilities
```c
struct drm_amdgpu_info {
    __u64 return_pointer;       // Pointer to output buffer
    __u32 return_size;          // Output buffer size
    __u32 query;                // Query type
    /* Query-specific data */
};
```

**Query Types**:
- `AMDGPU_INFO_ACCEL_WORKING`: Is GPU compute working?
- `AMDGPU_INFO_VRAM_USAGE`: VRAM usage statistics
- `AMDGPU_INFO_VIS_VRAM_USAGE`: Visible VRAM usage
- `AMDGPU_INFO_GTT_USAGE`: GTT memory usage
- `AMDGPU_INFO_FW_VERSION`: Firmware versions
- `AMDGPU_INFO_NUM_BYTES_MOVED`: Memory movement statistics
- `AMDGPU_INFO_VRAM_GTT`: VRAM and GTT info
- `AMDGPU_INFO_READ_MMR_REG`: Read hardware register
- `AMDGPU_INFO_DEV_INFO`: Device information
- `AMDGPU_INFO_HW_IP_INFO`: Hardware IP block info
- `AMDGPU_INFO_HW_IP_COUNT`: Number of IP blocks

**Purpose**: Query GPU capabilities, memory usage, firmware versions, and hardware configuration.

##### 3.5 Virtual Memory Management

```c
#define DRM_AMDGPU_VM               0x13
```

**DRM_AMDGPU_VM**: Virtual memory operations
```c
struct drm_amdgpu_vm {
    __u32 op;                   // RESERVE_VMID/UNRESERVE_VMID
    __u32 flags;
};
```

**Purpose**: Manage GPU virtual memory contexts.

##### 3.6 Synchronization Primitives

```c
#define DRM_AMDGPU_FENCE_TO_HANDLE  0x21
#define DRM_AMDGPU_SCHED            0x15
```

**Purpose**: Advanced synchronization between GPU jobs and CPU.

## GPU Compute (ROCm) Workflow

For compute workloads using ROCm/HIP:

1. **Device Discovery**:
   ```
   open(/dev/kfd)
   ioctl(/dev/kfd, AMDKFD_IOC_GET_VERSION)
   ioctl(/dev/kfd, AMDKFD_IOC_ACQUIRE_VM)
   ```

2. **Memory Allocation**:
   ```
   open(/dev/dri/renderD128)
   ioctl(renderD128, DRM_IOCTL_AMDGPU_GEM_CREATE)
   ioctl(renderD128, DRM_IOCTL_AMDGPU_GEM_VA)  // Map to GPU VA
   ```

3. **Context Creation**:
   ```
   ioctl(renderD128, DRM_IOCTL_AMDGPU_CTX, AMDGPU_CTX_OP_ALLOC)
   ```

4. **Kernel Launch**:
   ```
   // Prepare command buffer with compute dispatch
   ioctl(renderD128, DRM_IOCTL_AMDGPU_CS)  // Submit
   ```

5. **Synchronization**:
   ```
   ioctl(renderD128, DRM_IOCTL_AMDGPU_WAIT_CS)
   ```

6. **Cleanup**:
   ```
   ioctl(renderD128, DRM_IOCTL_AMDGPU_CTX, AMDGPU_CTX_OP_FREE)
   ioctl(renderD128, DRM_IOCTL_GEM_CLOSE)
   ```

## Graphics (Vulkan/OpenGL) Workflow

For graphics workloads:

1. **Display Master**:
   ```
   open(/dev/dri/card0)
   ioctl(card0, DRM_IOCTL_SET_MASTER)  // For display control
   ```

2. **Buffer Allocation** (for framebuffer):
   ```
   ioctl(card0, DRM_IOCTL_AMDGPU_GEM_CREATE)
   ```

3. **Command Submission** (render commands):
   ```
   ioctl(card0, DRM_IOCTL_AMDGPU_CS)
   ```

4. **Display** (modesetting):
   ```
   ioctl(card0, DRM_IOCTL_MODE_GETRESOURCES)
   ioctl(card0, DRM_IOCTL_MODE_SETCRTC)
   ```

## Memory Domains

AMDGPU supports multiple memory domains:

| Domain | Flag | Description |
|--------|------|-------------|
| VRAM | `AMDGPU_GEM_DOMAIN_VRAM` | GPU local memory (fastest for GPU) |
| GTT | `AMDGPU_GEM_DOMAIN_GTT` | GPU Translation Table (system RAM accessible to GPU) |
| CPU | `AMDGPU_GEM_DOMAIN_CPU` | System memory |
| GDS | `AMDGPU_GEM_DOMAIN_GDS` | Global Data Share (on-chip memory) |
| GWS | `AMDGPU_GEM_DOMAIN_GWS` | Global Wave Sync |
| OA | `AMDGPU_GEM_DOMAIN_OA` | Ordered Append |

## Hardware IP Blocks

AMDGPU divides GPU into IP (Intellectual Property) blocks:

- **GFX**: Graphics and compute engine
- **COMPUTE**: Compute-only engine
- **DMA**: DMA copy engines
- **UVD/VCN**: Video decode
- **VCE/VCN**: Video encode
- **SDMA**: System DMA

Each block has its own command submission ring.

## IOCTL Implementation

### Header Files

- `include/uapi/drm/amdgpu_drm.h` - UAPI header with IOCTL definitions
- `drivers/gpu/drm/amd/amdgpu/amdgpu_drv.c` - IOCTL handler registration
- `drivers/gpu/drm/amd/amdgpu/amdgpu_gem.c` - GEM IOCTL handlers
- `drivers/gpu/drm/amd/amdgpu/amdgpu_cs.c` - Command submission handlers

### IOCTL Registration

```c
static const struct drm_ioctl_desc amdgpu_ioctls[] = {
    DRM_IOCTL_DEF_DRV(AMDGPU_GEM_CREATE, amdgpu_gem_create_ioctl, ...),
    DRM_IOCTL_DEF_DRV(AMDGPU_GEM_MMAP, amdgpu_gem_mmap_ioctl, ...),
    DRM_IOCTL_DEF_DRV(AMDGPU_CTX, amdgpu_ctx_ioctl, ...),
    DRM_IOCTL_DEF_DRV(AMDGPU_CS, amdgpu_cs_ioctl, ...),
    DRM_IOCTL_DEF_DRV(AMDGPU_INFO, amdgpu_info_ioctl, ...),
    // ... more IOCTLs
};
```

## Security and Permissions

1. **Device Permissions**: Access controlled by `/dev/dri/*` permissions
2. **Master Mode**: Only one process can be DRM master (for display)
3. **Render Nodes**: `/dev/dri/renderD*` for compute-only (no master needed)
4. **Memory Protection**: Hardware IOMMU protects memory between processes
5. **Command Validation**: Kernel validates all command buffers
6. **Address Space Isolation**: Each process has isolated GPU virtual address space

## Performance Considerations

- **Latency**: IOCTL overhead ~1-5 microseconds
- **Batching**: Multiple commands can be batched in single CS submission
- **Zero-Copy**: USERPTR enables zero-copy for CPU/GPU shared memory
- **Direct Submit**: Minimal kernel overhead for command submission
- **Async Operations**: Non-blocking submission with fence-based sync

## Debugging IOCTLs

```bash
# Trace IOCTL calls
strace -e ioctl -y ./compute_application

# Enable kernel debug output
echo 1 > /sys/module/drm/parameters/debug
echo 0xffff > /sys/module/amdgpu/parameters/debug_mask

# Monitor memory usage
cat /sys/kernel/debug/dri/0/amdgpu_vram_mm
cat /sys/kernel/debug/dri/0/amdgpu_gtt_mm

# Check for GPU hangs
dmesg | grep -i amdgpu
```

## Comparison with NVIDIA

| Feature | AMDGPU | NVIDIA |
|---------|--------|--------|
| License | Open source (MIT) | Proprietary + Open (dual) |
| Kernel Integration | Mainline kernel | External module |
| DRM Integration | Native DRM driver | DRM wrapper |
| Compute API | ROCm/HIP | CUDA |
| User-space | Fully open (Mesa, AMDVLK) | Proprietary libcuda |
| Memory Management | TTM/GEM | Custom RM |
| Scheduler | DRM scheduler | GSP firmware |

## Key Differences

1. **Architecture**: AMDGPU is a native DRM driver, NVIDIA wraps custom driver in DRM
2. **Openness**: AMDGPU kernel+userspace fully open, NVIDIA kernel open but userspace proprietary
3. **API**: AMDGPU uses standard DRM IOCTLs + extensions, NVIDIA uses custom IOCTLs
4. **Integration**: AMDGPU in mainline kernel, NVIDIA requires external module

## References

1. [AMDGPU Kernel Documentation](https://docs.kernel.org/gpu/amdgpu/index.html)
2. [Linux DRM Documentation](https://dri.freedesktop.org/docs/drm/)
3. [AMDGPU Source Code](https://github.com/torvalds/linux/tree/master/drivers/gpu/drm/amd/amdgpu)
4. [ROCm Documentation](https://rocm.docs.amd.com/)
5. [GPUOpen-Drivers](https://github.com/orgs/GPUOpen-Drivers/repositories)
6. [AMDGPU ArchWiki](https://wiki.archlinux.org/title/AMDGPU)

## Key Takeaways

1. **DRM Native**: AMDGPU is a first-class DRM driver with full kernel integration
2. **Open Source**: Completely open source kernel and user-space stack
3. **Unified Interface**: Uses standard DRM GEM/KMS interfaces with AMD extensions
4. **ROCm Support**: Provides CUDA-like compute capabilities through ROCm
5. **Memory Management**: Sophisticated multi-domain memory management (VRAM, GTT, etc.)
6. **Hardware Scheduler**: GPU scheduler manages fair resource allocation
7. **Security**: Full IOMMU support and per-process address space isolation
8. **Performance**: Low-overhead command submission and zero-copy capabilities

## Conclusion

The AMDGPU driver provides a comprehensive, open-source GPU interface built on Linux DRM standards. Its IOCTL interface supports both graphics and compute workloads, with particular strength in standards compliance and open development. The driver's integration with mainline Linux kernel ensures broad compatibility and community support.
