# GPU IOCTL Mappings

This document provides comprehensive mappings between different GPU driver IOCTL interfaces, helping developers understand equivalent operations across AMD, NVIDIA, and conceptual CPU operations.

## Table of Contents

1. [AMD → NVIDIA+CUDA IOCTL Mapping](#amd--nvidiacuda-ioctl-mapping)
2. [CUDA → CPU Operation Mapping](#cuda--cpu-operation-mapping)
3. [Quick Reference Tables](#quick-reference-tables)

---

## AMD → NVIDIA+CUDA IOCTL Mapping

This section maps AMD AMDGPU IOCTLs to their NVIDIA/CUDA equivalents, showing how similar operations are performed across different GPU vendors.

### Memory Management Operations

#### Buffer Allocation

| AMD IOCTL | NVIDIA IOCTL | CUDA API | Purpose |
|-----------|--------------|----------|---------|
| `DRM_IOCTL_AMDGPU_GEM_CREATE` | `NV_ESC_RM_ALLOC_MEMORY` | `cuMemAlloc()` | Allocate GPU memory buffer |
| `DRM_IOCTL_AMDGPU_GEM_MMAP` | `NV_ESC_RM_MAP_MEMORY` | `cuMemHostGetDevicePointer()` | Map buffer for CPU access |
| `DRM_IOCTL_AMDGPU_GEM_USERPTR` | `UVM_MAP_EXTERNAL_ALLOCATION` | `cuMemHostRegister()` | Use CPU memory as GPU buffer (zero-copy) |
| `DRM_IOCTL_GEM_CLOSE` | `NV_ESC_RM_FREE` | `cuMemFree()` | Free GPU memory buffer |

**Details:**

**AMD `DRM_IOCTL_AMDGPU_GEM_CREATE`**:
```c
struct drm_amdgpu_gem_create {
    __u64 bo_size;              // Buffer size
    __u64 alignment;            // Alignment
    __u64 domains;              // VRAM/GTT/SYSTEM
    __u64 flags;                // Creation flags
    __u32 handle;               // Output: GEM handle
};
```

**NVIDIA `NV_ESC_RM_ALLOC_MEMORY`**:
```c
// NVIDIA uses Resource Manager (RM) API
NvRmAlloc(hClient, hDevice, hMemory, classId, &allocParams);
// Parameters include size, alignment, memory type (vidmem/sysmem)
```

**CUDA `cuMemAlloc()`**:
```c
CUresult cuMemAlloc(CUdeviceptr *dptr, size_t bytesize);
// Simplified interface, allocation details handled by driver
```

**Key Differences**:
- AMD: Explicit memory domain specification (VRAM, GTT, system)
- NVIDIA: Resource Manager abstraction layer
- CUDA: High-level API hiding complexity

#### Virtual Address Mapping

| AMD IOCTL | NVIDIA IOCTL | CUDA API | Purpose |
|-----------|--------------|----------|---------|
| `DRM_IOCTL_AMDGPU_GEM_VA` | `UVM_REGISTER_GPU_VASPACE` | Automatic (managed by driver) | Map buffer to GPU virtual address |
| `DRM_IOCTL_AMDGPU_GEM_VA` (UNMAP) | `NV_ESC_RM_UNMAP_MEMORY` | Automatic | Unmap GPU virtual address |

**Details:**

**AMD `DRM_IOCTL_AMDGPU_GEM_VA`**:
```c
struct drm_amdgpu_gem_va {
    __u32 handle;               // GEM handle
    __u32 operation;            // MAP/UNMAP/REPLACE
    __u64 va_address;           // GPU virtual address
    __u64 map_size;             // Size to map
};
```

**NVIDIA `UVM_REGISTER_GPU_VASPACE`**:
```c
// UVM (Unified Virtual Memory) handles VA space automatically
struct UvmRegisterGpuVaspaceParams {
    uuid gpu_uuid;
    int rm_ctrl_fd;
    unsigned int hClient;
    unsigned int hVaSpace;
};
```

**CUDA**: Virtual address space is managed transparently by the CUDA runtime and UVM driver.

#### Memory Migration

| AMD IOCTL | NVIDIA IOCTL | CUDA API | Purpose |
|-----------|--------------|----------|---------|
| `DRM_IOCTL_AMDGPU_GEM_VA` (hints) | `UVM_MIGRATE` | `cuMemAdvise()` | Migrate memory between CPU/GPU |
| N/A (automatic) | `UVM_SET_PREFERRED_LOCATION` | `cuMemPrefetchAsync()` | Set preferred memory location |
| N/A (automatic) | `UVM_SET_ACCESSED_BY` | `cuMemAdvise()` (ACCESS_BY) | Hint about memory access patterns |

**Details:**

**NVIDIA `UVM_MIGRATE`**:
```c
struct UvmMigrateParams {
    __u64 base;                 // Base address
    __u64 length;               // Length in bytes
    uuid destination_uuid;      // CPU or GPU UUID
    __u32 flags;                // Migration flags
};
```

**CUDA `cuMemPrefetchAsync()`**:
```c
CUresult cuMemPrefetchAsync(
    CUdeviceptr devPtr,
    size_t count,
    CUdevice dstDevice,
    CUstream hStream
);
```

**Key Differences**:
- AMD: Memory migration primarily automatic based on page faults
- NVIDIA: Explicit UVM migration IOCTLs for fine control
- CUDA: High-level hints for prefetching and locality

### Command Submission Operations

#### Context Management

| AMD IOCTL | NVIDIA IOCTL | CUDA API | Purpose |
|-----------|--------------|----------|---------|
| `DRM_IOCTL_AMDGPU_CTX` (CREATE) | `NV_ESC_RM_ALLOC_CONTEXT` | `cuCtxCreate()` | Create GPU execution context |
| `DRM_IOCTL_AMDGPU_CTX` (DESTROY) | `NV_ESC_RM_FREE` | `cuCtxDestroy()` | Destroy GPU context |
| N/A | `NV_ESC_RM_ALLOC_CHANNEL` | Implicit | Allocate command submission channel |

**Details:**

**AMD `DRM_IOCTL_AMDGPU_CTX`**:
```c
struct drm_amdgpu_ctx {
    __u32 op;                   // CREATE/DESTROY/QUERY
    __u32 flags;
    __u32 ctx_id;               // Context ID (output for CREATE)
};
```

**NVIDIA `NV_ESC_RM_ALLOC_CONTEXT`**:
```c
// NVIDIA contexts are part of RM object hierarchy
NvRmAlloc(hClient, hDevice, hContext, NV01_CONTEXT_DMA, &params);
```

**CUDA `cuCtxCreate()`**:
```c
CUresult cuCtxCreate(CUcontext *pctx, unsigned int flags, CUdevice dev);
```

#### Workload Submission

| AMD IOCTL | NVIDIA IOCTL | CUDA API | Purpose |
|-----------|--------------|----------|---------|
| `DRM_IOCTL_AMDGPU_CS` | `NV_ESC_RM_CONTROL` | `cuLaunchKernel()` | Submit GPU commands/kernel |
| `DRM_IOCTL_AMDGPU_CS` (IB chunk) | Pushbuffer submission | Internal (via stream) | Submit command buffer |
| `DRM_IOCTL_AMDGPU_BO_LIST_CREATE` | Buffer list in UVM | Automatic | Manage buffer dependencies |

**Details:**

**AMD `DRM_IOCTL_AMDGPU_CS`**:
```c
struct drm_amdgpu_cs_in {
    __u32 ctx_id;               // Context ID
    __u32 bo_list_handle;       // Buffer list
    __u32 num_chunks;           // Number of chunks
    __u64 chunks;               // Command chunks
};

// Chunks include:
// - AMDGPU_CHUNK_ID_IB: Indirect Buffer (command buffer)
// - AMDGPU_CHUNK_ID_FENCE: Sync objects
// - AMDGPU_CHUNK_ID_DEPENDENCIES: Job dependencies
```

**NVIDIA Pushbuffer Submission**:
```c
// NVIDIA uses pushbuffer-based command submission
// Pushbuffer is a ring buffer of GPU commands
// Submission via NV_ESC_RM_CONTROL with appropriate parameters
```

**CUDA `cuLaunchKernel()`**:
```c
CUresult cuLaunchKernel(
    CUfunction f,
    unsigned int gridDimX, gridDimY, gridDimZ,
    unsigned int blockDimX, blockDimY, blockDimZ,
    unsigned int sharedMemBytes,
    CUstream hStream,
    void **kernelParams,
    void **extra
);
```

**Key Differences**:
- AMD: Chunk-based command submission with explicit dependencies
- NVIDIA: Pushbuffer-based with channel abstraction
- CUDA: High-level kernel launch API

### Synchronization Operations

#### Fence/Event Management

| AMD IOCTL | NVIDIA IOCTL | CUDA API | Purpose |
|-----------|--------------|----------|---------|
| `DRM_IOCTL_AMDGPU_WAIT_CS` | `NV_ESC_WAIT_OPEN_COMPLETE` | `cuStreamSynchronize()` | Wait for GPU completion |
| `DRM_IOCTL_AMDGPU_FENCE_TO_HANDLE` | `NV_ESC_ALLOC_OS_EVENT` | `cuEventCreate()` | Create synchronization object |
| `DRM_IOCTL_SYNCOBJ_CREATE` | Event registration | `cuEventRecord()` | Record synchronization point |
| `DRM_IOCTL_SYNCOBJ_WAIT` | `NV_ESC_FREE_OS_EVENT` | `cuEventSynchronize()` | Wait for event |

**Details:**

**AMD `DRM_IOCTL_AMDGPU_WAIT_CS`**:
```c
struct drm_amdgpu_wait_cs {
    __u32 handle;               // CS handle
    __u32 timeout;              // Timeout (ns)
    __u64 out_seq_no;           // Sequence number
};
```

**NVIDIA `UVM_WAIT_FOR_IDLE`**:
```c
// UVM-specific wait for GPU idle
ioctl(uvm_fd, UVM_WAIT_FOR_IDLE, NULL);
```

**CUDA `cuStreamSynchronize()`**:
```c
CUresult cuStreamSynchronize(CUstream hStream);
// Blocks until all operations in stream complete
```

#### Multi-GPU Synchronization

| AMD IOCTL | NVIDIA IOCTL | CUDA API | Purpose |
|-----------|--------------|----------|---------|
| `DRM_IOCTL_SYNCOBJ_*` | `UVM_ENABLE_PEER_ACCESS` | `cuDeviceEnablePeerAccess()` | Enable peer-to-peer access |
| Cross-device fences | `UVM_DISABLE_PEER_ACCESS` | `cuDeviceDisablePeerAccess()` | Disable peer access |
| DMA-BUF sharing | P2P mapping via UVM | `cuMemcpyPeer()` | Copy between GPUs |

### Device Information Operations

#### Device Queries

| AMD IOCTL | NVIDIA IOCTL | CUDA API | Purpose |
|-----------|--------------|----------|---------|
| `DRM_IOCTL_AMDGPU_INFO` | `NV_ESC_CARD_INFO` | `cuDeviceGetAttribute()` | Query device capabilities |
| `DRM_IOCTL_AMDGPU_INFO` (VRAM) | `NV_ESC_QUERY_DEVICE_INFO` | `cuMemGetInfo()` | Get memory information |
| `DRM_IOCTL_AMDGPU_INFO` (HW_IP) | Hardware query | `cuDeviceGetProperties()` | Get device properties |
| `DRM_IOCTL_VERSION` | `NV_ESC_CHECK_VERSION` | `cuDriverGetVersion()` | Get driver version |

**Details:**

**AMD `DRM_IOCTL_AMDGPU_INFO`**:
```c
struct drm_amdgpu_info {
    __u32 query;                // Query type
    __u32 return_size;          // Size of return data
    __u64 return_pointer;       // Pointer to return buffer
};

// Query types:
// - AMDGPU_INFO_ACCEL_WORKING
// - AMDGPU_INFO_VRAM_USAGE
// - AMDGPU_INFO_HW_IP_INFO
// - AMDGPU_INFO_FW_VERSION
// - AMDGPU_INFO_DEV_INFO
```

**NVIDIA Device Queries**:
```c
// NVIDIA uses multiple IOCTLs for different info types
NV_ESC_CARD_INFO          // Basic card information
NV_ESC_QUERY_DEVICE_INFO  // Detailed capabilities
```

**CUDA `cuDeviceGetAttribute()`**:
```c
CUresult cuDeviceGetAttribute(
    int *pi,
    CUdevice_attribute attrib,
    CUdevice dev
);
// 100+ attributes available
```

---

## CUDA → CPU Operation Mapping

This section shows how CUDA GPU operations map to conceptual CPU equivalents, demonstrating the abstraction layers.

### Memory Operations

| CUDA Operation | CPU Equivalent | System Call | Description |
|----------------|----------------|-------------|-------------|
| `cuMemAlloc()` | `malloc()` | `brk()`/`mmap()` | Allocate memory |
| `cuMemFree()` | `free()` | `munmap()` | Free memory |
| `cuMemcpyHtoD()` | `memcpy()` | N/A | Copy memory host→device |
| `cuMemcpyDtoH()` | `memcpy()` | N/A | Copy memory device→host |
| `cuMemcpyDtoD()` | `memcpy()` | N/A | Copy memory device→device |
| `cuMemset()` | `memset()` | N/A | Set memory to value |
| `cuMemHostAlloc()` | `mmap()` (pinned) | `mmap()` with `MAP_LOCKED` | Allocate page-locked memory |
| `cuMemHostRegister()` | `mlock()` | `mlock()` | Lock existing memory pages |

**Detailed Comparison:**

#### Memory Allocation

**CUDA**:
```c
CUdeviceptr d_ptr;
cuMemAlloc(&d_ptr, size);  // GPU memory allocation
```

**CPU**:
```c
void *ptr = malloc(size);  // CPU memory allocation
```

**System Call (CPU)**:
```c
// malloc() eventually calls:
void *ptr = mmap(NULL, size, PROT_READ|PROT_WRITE, 
                 MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
```

**IOCTL (GPU)**:
```c
// cuMemAlloc() calls:
ioctl(nvidia_fd, NV_ESC_RM_ALLOC_MEMORY, &params);
// Which UVM translates to:
ioctl(uvm_fd, UVM_MAP_EXTERNAL_ALLOCATION, &uvm_params);
```

#### Memory Copy

**CUDA**:
```c
cuMemcpyHtoD(d_ptr, h_ptr, size);  // Host to Device
```

**CPU**:
```c
memcpy(dst, src, size);            // Memory to memory
```

**Under the Hood**:
- **CPU**: Direct memory access, CPU performs copy
- **GPU**: DMA transfer over PCIe, GPU DMA engine performs copy
  - Invokes `ioctl()` to set up DMA transfer
  - Data transferred via PCIe bus
  - GPU signals completion via interrupt

### Execution Operations

| CUDA Operation | CPU Equivalent | System Call | Description |
|----------------|----------------|-------------|-------------|
| `cuCtxCreate()` | `fork()` / process creation | `clone()` | Create execution context |
| `cuCtxDestroy()` | Process termination | `exit()` | Destroy execution context |
| `cuStreamCreate()` | Thread creation | `pthread_create()` | Create execution stream |
| `cuStreamDestroy()` | Thread termination | `pthread_join()` | Destroy execution stream |
| `cuLaunchKernel()` | Function call + threading | `clone()` (thread) | Launch parallel work |
| Context switching | Process switching | Scheduler | Switch execution context |

**Detailed Comparison:**

#### Context Creation

**CUDA**:
```c
CUcontext ctx;
cuCtxCreate(&ctx, 0, device);  // Create GPU context
```

**CPU**:
```c
pid_t pid = fork();            // Create new process
// or
pthread_t thread;
pthread_create(&thread, NULL, func, args);  // Create thread
```

**System Call**:
```c
// fork() calls:
pid_t pid = clone(SIGCHLD, NULL);

// pthread_create() calls:
clone(CLONE_VM|CLONE_FS|CLONE_FILES|CLONE_SIGHAND|CLONE_THREAD, ...);
```

**IOCTL (GPU)**:
```c
// cuCtxCreate() calls:
ioctl(nvidia_fd, NV_ESC_RM_ALLOC_CONTEXT, &ctx_params);
```

#### Kernel Launch

**CUDA**:
```c
// Launch kernel with 1024 blocks × 256 threads = 262,144 parallel threads
kernel<<<1024, 256>>>(args);
// Or explicitly:
cuLaunchKernel(kernel_func, 1024, 1, 1,  // grid
               256, 1, 1,                  // block
               0, stream, args, NULL);
```

**CPU Equivalent (conceptual)**:
```c
// Spawn 262,144 threads (not practical!)
pthread_t threads[262144];
for (int i = 0; i < 262144; i++) {
    pthread_create(&threads[i], NULL, kernel_func, &args[i]);
}
for (int i = 0; i < 262144; i++) {
    pthread_join(threads[i], NULL);
}

// More realistic: Thread pool with work queue
ThreadPool pool(std::thread::hardware_concurrency());
for (int i = 0; i < 262144; i++) {
    pool.enqueue(kernel_func, args[i]);
}
pool.wait_all();
```

**Key Differences**:
- **GPU**: Hardware-managed massive parallelism (thousands of threads)
- **CPU**: Software-managed limited parallelism (8-64 threads typically)
- **GPU**: SIMT execution (Single Instruction Multiple Thread)
- **CPU**: MIMD execution (Multiple Instruction Multiple Data)

### Synchronization Operations

| CUDA Operation | CPU Equivalent | System Call | Description |
|----------------|----------------|-------------|-------------|
| `cuCtxSynchronize()` | `waitpid()` / barrier | `wait4()` | Wait for all operations |
| `cuStreamSynchronize()` | `pthread_join()` | `futex()` | Wait for stream |
| `cuEventCreate()` | `pipe()` / eventfd | `eventfd()` | Create sync object |
| `cuEventRecord()` | `write()` to eventfd | `write()` | Record event |
| `cuEventSynchronize()` | `read()` from eventfd | `read()` | Wait for event |
| `cuStreamWaitEvent()` | `poll()` / `select()` | `poll()` / `epoll()` | Wait for event in stream |
| `__syncthreads()` (device) | Barrier | `pthread_barrier_wait()` | Thread barrier |

**Detailed Comparison:**

#### Synchronization Barrier

**CUDA (Device Code)**:
```c
__global__ void kernel() {
    // All threads in block execute up to here
    __syncthreads();  // Wait for all threads in block
    // Continue after all threads reach barrier
}
```

**CPU**:
```c
pthread_barrier_t barrier;
pthread_barrier_init(&barrier, NULL, num_threads);

void* thread_func(void* arg) {
    // Do work
    pthread_barrier_wait(&barrier);  // Wait for all threads
    // Continue after all threads reach barrier
    return NULL;
}
```

**System Call**:
```c
// pthread_barrier_wait() internally uses:
futex(&barrier->futex_word, FUTEX_WAIT, expected, NULL, NULL, 0);
// When last thread arrives:
futex(&barrier->futex_word, FUTEX_WAKE, num_threads, NULL, NULL, 0);
```

#### Event Synchronization

**CUDA**:
```c
CUevent event;
cuEventCreate(&event, 0);
cuEventRecord(event, stream);       // Record point in stream
// ... do other work ...
cuEventSynchronize(event);          // Wait for event
```

**CPU**:
```c
int efd = eventfd(0, 0);            // Create event
// Thread 1:
uint64_t value = 1;
write(efd, &value, sizeof(value));  // Signal event

// Thread 2:
uint64_t result;
read(efd, &result, sizeof(result)); // Wait for event
```

**System Calls**:
```c
// eventfd() system call
int efd = syscall(SYS_eventfd2, 0, 0);

// write() to signal
syscall(SYS_write, efd, &value, sizeof(value));

// read() to wait (blocks until signaled)
syscall(SYS_read, efd, &result, sizeof(result));
```

### Atomic Operations

| CUDA Operation | CPU Equivalent | CPU Instruction | Description |
|----------------|----------------|-----------------|-------------|
| `atomicAdd()` | `__atomic_add_fetch()` | `LOCK XADD` (x86) | Atomic addition |
| `atomicCAS()` | `__atomic_compare_exchange()` | `LOCK CMPXCHG` (x86) | Compare-and-swap |
| `atomicExch()` | `__atomic_exchange()` | `LOCK XCHG` (x86) | Atomic exchange |
| `atomicMin()` | Custom CAS loop | CAS loop | Atomic minimum |
| `atomicMax()` | Custom CAS loop | CAS loop | Atomic maximum |

**Example:**

**CUDA**:
```c
__global__ void atomic_kernel(int *counter) {
    atomicAdd(counter, 1);  // Hardware atomic instruction
}
```

**CPU (C11 atomics)**:
```c
#include <stdatomic.h>

void atomic_function(atomic_int *counter) {
    atomic_fetch_add(counter, 1);  // Hardware atomic instruction
}
```

**x86 Assembly**:
```asm
; CUDA atomicAdd() on GPU -> ATOM.ADD instruction
ATOM.ADD.S32 [counter], 1;

; CPU atomic_fetch_add() -> LOCK XADD instruction  
LOCK XADD [counter], 1
```

---

## Quick Reference Tables

### Operation Category Matrix

| Category | AMD IOCTL | NVIDIA IOCTL | CUDA API | CPU Equivalent |
|----------|-----------|--------------|----------|----------------|
| **Memory Alloc** | `GEM_CREATE` | `RM_ALLOC_MEMORY` | `cuMemAlloc()` | `malloc()` |
| **Memory Map** | `GEM_MMAP` | `RM_MAP_MEMORY` | `cuMemHostGetDevicePointer()` | `mmap()` |
| **Zero-Copy** | `GEM_USERPTR` | `UVM_MAP_EXTERNAL` | `cuMemHostRegister()` | `mlock()` |
| **Context** | `CTX` (CREATE) | `RM_ALLOC_CONTEXT` | `cuCtxCreate()` | `fork()` |
| **Execute** | `CS` | `RM_CONTROL` | `cuLaunchKernel()` | `pthread_create()` |
| **Sync** | `WAIT_CS` | `WAIT_OPEN_COMPLETE` | `cuStreamSynchronize()` | `pthread_join()` |
| **Event** | `SYNCOBJ_*` | `ALLOC_OS_EVENT` | `cuEventCreate()` | `eventfd()` |

### Abstraction Layers

```
┌─────────────────────────────────────────────────────────┐
│                    Application Code                      │
├─────────────────────────────────────────────────────────┤
│          CUDA Runtime API    │    pthread, libc         │
│         (cuMemAlloc, etc)    │    (malloc, etc)         │
├──────────────────────────────┼──────────────────────────┤
│         CUDA Driver API      │    System Libraries      │
│      (Low-level CUDA API)    │    (glibc, etc)          │
├──────────────────────────────┼──────────────────────────┤
│          User Space          │          User Space      │
╞══════════════════════════════╪══════════════════════════╡
│         Kernel Space         │         Kernel Space     │
├──────────────────────────────┼──────────────────────────┤
│       NVIDIA Driver          │     Linux Kernel         │
│  (nvidia.ko, nvidia-uvm.ko)  │   (Memory, Scheduler)    │
├──────────────────────────────┼──────────────────────────┤
│    IOCTL Interface           │    System Call           │
│  (NV_ESC_*, UVM_*)           │  (mmap, clone, futex)    │
├──────────────────────────────┼──────────────────────────┤
│       GSP Firmware           │       CPU Hardware       │
├──────────────────────────────┼──────────────────────────┤
│       GPU Hardware           │       CPU Execution      │
└──────────────────────────────┴──────────────────────────┘

           GPU Path                      CPU Path
```

### Performance Characteristics

| Operation | GPU (CUDA) | CPU | Winner | Notes |
|-----------|------------|-----|--------|-------|
| **Parallel Tasks** | Thousands of threads | Tens of threads | GPU | Massive parallelism |
| **Sequential Code** | Slower | Faster | CPU | Better single-thread perf |
| **Memory Bandwidth** | Up to 1 TB/s | Up to 100 GB/s | GPU | HBM vs DDR |
| **Memory Latency** | 200-800 cycles | 50-200 cycles | CPU | GPU hides latency |
| **Context Switch** | Fast (hardware) | Slower (software) | GPU | Hardware scheduling |
| **Atomic Operations** | Slower at high contention | Faster | CPU | Better cache coherency |
| **Small Data Sets** | Slower (PCIe overhead) | Faster | CPU | Avoid GPU for small data |
| **Large Data Sets** | Faster (parallelism) | Slower | GPU | Parallelism wins |

### Memory Hierarchy Comparison

| Level | GPU (CUDA) | CPU | Speed (GB/s) |
|-------|------------|-----|--------------|
| **L1 Cache** | Per-SM L1 (128 KB) | Per-core L1 (32-64 KB) | ~10,000 |
| **L2 Cache** | Shared L2 (40-80 MB) | Shared L2 (256 KB-1 MB per core) | ~4,000 |
| **L3 Cache** | N/A | Shared L3 (8-64 MB) | ~500 |
| **Main Memory** | VRAM/HBM (16-80 GB) | DDR4/DDR5 (16-128 GB) | GPU: 500-1000, CPU: 50-100 |
| **Shared Memory** | 48-164 KB per block | N/A (registers/L1) | ~10,000 |
| **Registers** | 64K per SM | ~16 per core | Fastest |

---

## Practical Examples

### Example 1: Simple Vector Addition

#### CUDA Version

```c
// CUDA kernel
__global__ void vectorAdd(float *a, float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}

// Host code
CUdeviceptr d_a, d_b, d_c;
cuMemAlloc(&d_a, size);
cuMemAlloc(&d_b, size);
cuMemAlloc(&d_c, size);
cuMemcpyHtoD(d_a, h_a, size);
cuMemcpyHtoD(d_b, h_b, size);

// Launch: (n/256) blocks × 256 threads
cuLaunchKernel(vectorAdd, (n+255)/256, 1, 1, 256, 1, 1, 
               0, stream, args, NULL);

cuMemcpyDtoH(h_c, d_c, size);
```

**IOCTLs Called**:
1. `ioctl(fd, NV_ESC_RM_ALLOC_MEMORY, ...)` - 3 times for d_a, d_b, d_c
2. `ioctl(fd, UVM_MAP_EXTERNAL_ALLOCATION, ...)` - 3 times
3. DMA setup for `cuMemcpyHtoD` - 2 times
4. `ioctl(fd, NV_ESC_RM_CONTROL, ...)` - kernel launch
5. DMA setup for `cuMemcpyDtoH` - 1 time

#### CPU Version

```c
// CPU function
void vectorAdd(float *a, float *b, float *c, int n) {
    #pragma omp parallel for
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}

// Already in memory, no allocation needed
float *a = malloc(size);
float *b = malloc(size);
float *c = malloc(size);

vectorAdd(a, b, c, n);
```

**System Calls**:
1. `mmap()` - 3 times (within malloc)
2. `clone()` - Multiple times for OpenMP threads
3. `futex()` - Thread synchronization

### Example 2: AMD AMDGPU Version

```c
// Using AMD AMDGPU IOCTLs
int amdgpu_fd = open("/dev/dri/renderD128", O_RDWR);

// Allocate buffers
struct drm_amdgpu_gem_create create_a = {.bo_size = size, ...};
ioctl(amdgpu_fd, DRM_IOCTL_AMDGPU_GEM_CREATE, &create_a);

struct drm_amdgpu_gem_create create_b = {.bo_size = size, ...};
ioctl(amdgpu_fd, DRM_IOCTL_AMDGPU_GEM_CREATE, &create_b);

struct drm_amdgpu_gem_create create_c = {.bo_size = size, ...};
ioctl(amdgpu_fd, DRM_IOCTL_AMDGPU_GEM_CREATE, &create_c);

// Map to GPU VA
struct drm_amdgpu_gem_va va_a = {.handle = create_a.handle, ...};
ioctl(amdgpu_fd, DRM_IOCTL_AMDGPU_GEM_VA, &va_a);

// ... similar for b, c ...

// Submit command buffer with compute kernel
struct drm_amdgpu_cs_in cs = {
    .ctx_id = ctx_id,
    .bo_list_handle = bo_list,
    .num_chunks = 2,
    .chunks = chunks_ptr  // Points to IB and fence chunks
};
ioctl(amdgpu_fd, DRM_IOCTL_AMDGPU_CS, &cs);

// Wait for completion
struct drm_amdgpu_wait_cs wait = {.handle = cs_handle, ...};
ioctl(amdgpu_fd, DRM_IOCTL_AMDGPU_WAIT_CS, &wait);
```

**Mapping**:
- AMD `GEM_CREATE` ↔ NVIDIA `RM_ALLOC_MEMORY` ↔ CUDA `cuMemAlloc()`
- AMD `GEM_VA` ↔ NVIDIA `UVM_REGISTER_GPU_VASPACE` ↔ CUDA (automatic)
- AMD `CS` ↔ NVIDIA `RM_CONTROL` ↔ CUDA `cuLaunchKernel()`
- AMD `WAIT_CS` ↔ NVIDIA `WAIT_OPEN_COMPLETE` ↔ CUDA `cuStreamSynchronize()`

---

## Conclusion

This mapping demonstrates:

1. **AMD and NVIDIA share many concepts** but implement them differently:
   - AMD: Standard DRM/GEM interface
   - NVIDIA: Custom Resource Manager interface

2. **CUDA abstracts complexity** from developers:
   - High-level API hides IOCTL details
   - Automatic memory management and optimization

3. **GPU operations map to CPU equivalents**:
   - Memory: GPU buffers ↔ CPU heap
   - Execution: GPU kernels ↔ CPU threads
   - Synchronization: GPU events ↔ CPU futex/eventfd

4. **Key differences**:
   - **Scale**: GPUs handle thousands of concurrent threads
   - **Architecture**: SIMT (GPU) vs MIMD (CPU)
   - **Memory**: High bandwidth, high latency (GPU) vs Low bandwidth, low latency (CPU)

Understanding these mappings helps developers:
- Port code between GPU vendors
- Optimize for specific platforms
- Debug driver interactions
- Design cross-platform GPU abstractions

---

*This document is part of shittyNVIDIA - Because even a joke project should have serious technical documentation!*

*Last updated: 2025-12-30*
