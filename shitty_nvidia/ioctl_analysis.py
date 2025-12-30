"""
IOCTL Analysis Module for shittyNVIDIA

This module provides comprehensive analysis of IOCTLs from:
1. NVIDIA Open Source Drivers (nouveau, nvidia-open)
2. AMD Open Source Drivers (amdgpu, radeon)

Because if we're going to be the worst NVIDIA driver ever,
we should at least know what the good ones do!
"""

import struct
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import IntEnum


class IOCTLDirection(IntEnum):
    """IOCTL direction flags"""
    NONE = 0
    WRITE = 1
    READ = 2
    READ_WRITE = 3


@dataclass
class IOCTLCommand:
    """Represents an IOCTL command"""
    name: str
    cmd: int
    direction: IOCTLDirection
    size: int
    description: str
    parameters: List[str]
    driver: str
    category: str


class NVIDIAIOCTLAnalyzer:
    """
    Analyzes NVIDIA open source driver IOCTLs
    
    Covers both nouveau (reverse-engineered) and nvidia-open (official OSS)
    """
    
    def __init__(self):
        self.drm_ioctls = self._init_drm_ioctls()
        self.nouveau_ioctls = self._init_nouveau_ioctls()
        self.nvidia_open_ioctls = self._init_nvidia_open_ioctls()
        self.cuda_ioctls = self._init_cuda_ioctls()
    
    def _init_drm_ioctls(self) -> List[IOCTLCommand]:
        """Initialize DRM IOCTLs used by NVIDIA drivers"""
        return [
            IOCTLCommand(
                name="DRM_IOCTL_VERSION",
                cmd=0xc0406400,
                direction=IOCTLDirection.READ_WRITE,
                size=64,
                description="Get DRM version information",
                parameters=["version_major", "version_minor", "version_patchlevel", "name", "date", "desc"],
                driver="drm",
                category="core"
            ),
            IOCTLCommand(
                name="DRM_IOCTL_GET_UNIQUE",
                cmd=0xc0106401,
                direction=IOCTLDirection.READ_WRITE,
                size=16,
                description="Get unique identifier for the device",
                parameters=["unique_len", "unique"],
                driver="drm",
                category="core"
            ),
            IOCTLCommand(
                name="DRM_IOCTL_GET_MAGIC",
                cmd=0x80046402,
                direction=IOCTLDirection.READ,
                size=4,
                description="Get authentication magic number",
                parameters=["magic"],
                driver="drm",
                category="auth"
            ),
            IOCTLCommand(
                name="DRM_IOCTL_IRQ_BUSID",
                cmd=0xc0106403,
                direction=IOCTLDirection.READ_WRITE,
                size=16,
                description="Get IRQ and bus ID information",
                parameters=["irq", "busnum", "devnum", "funcnum"],
                driver="drm",
                category="hardware"
            ),
            IOCTLCommand(
                name="DRM_IOCTL_GET_MAP",
                cmd=0xc0286404,
                direction=IOCTLDirection.READ_WRITE,
                size=40,
                description="Get memory map information",
                parameters=["offset", "size", "type", "flags", "handle", "mtrr"],
                driver="drm",
                category="memory"
            ),
            IOCTLCommand(
                name="DRM_IOCTL_GET_CLIENT",
                cmd=0xc0206405,
                direction=IOCTLDirection.READ_WRITE,
                size=32,
                description="Get client information",
                parameters=["idx", "auth", "pid", "uid", "magic", "iocs"],
                driver="drm",
                category="client"
            ),
            IOCTLCommand(
                name="DRM_IOCTL_GET_STATS",
                cmd=0x80f06406,
                direction=IOCTLDirection.READ,
                size=240,
                description="Get driver statistics",
                parameters=["count", "data"],
                driver="drm",
                category="stats"
            ),
            IOCTLCommand(
                name="DRM_IOCTL_SET_VERSION",
                cmd=0xc0186407,
                direction=IOCTLDirection.READ_WRITE,
                size=24,
                description="Set interface version",
                parameters=["drm_di_major", "drm_di_minor", "drm_dd_major", "drm_dd_minor"],
                driver="drm",
                category="version"
            ),
            IOCTLCommand(
                name="DRM_IOCTL_MODESET_CTL",
                cmd=0x40086408,
                direction=IOCTLDirection.WRITE,
                size=8,
                description="Control modesetting",
                parameters=["crtc", "cmd"],
                driver="drm",
                category="display"
            ),
            IOCTLCommand(
                name="DRM_IOCTL_GEM_CLOSE",
                cmd=0x40046409,
                direction=IOCTLDirection.WRITE,
                size=4,
                description="Close GEM object handle",
                parameters=["handle"],
                driver="drm",
                category="gem"
            ),
            IOCTLCommand(
                name="DRM_IOCTL_GEM_FLINK",
                cmd=0xc008640a,
                direction=IOCTLDirection.READ_WRITE,
                size=8,
                description="Create global name for GEM object",
                parameters=["handle", "name"],
                driver="drm",
                category="gem"
            ),
            IOCTLCommand(
                name="DRM_IOCTL_GEM_OPEN",
                cmd=0xc008640b,
                direction=IOCTLDirection.READ_WRITE,
                size=8,
                description="Open GEM object by global name",
                parameters=["name", "handle", "size"],
                driver="drm",
                category="gem"
            ),
            IOCTLCommand(
                name="DRM_IOCTL_GET_CAP",
                cmd=0xc008640c,
                direction=IOCTLDirection.READ_WRITE,
                size=8,
                description="Get driver capability",
                parameters=["capability", "value"],
                driver="drm",
                category="caps"
            ),
            IOCTLCommand(
                name="DRM_IOCTL_SET_CLIENT_CAP",
                cmd=0x4010640d,
                direction=IOCTLDirection.WRITE,
                size=16,
                description="Set client capability",
                parameters=["capability", "value"],
                driver="drm",
                category="caps"
            ),
        ]
    
    def _init_nouveau_ioctls(self) -> List[IOCTLCommand]:
        """Initialize Nouveau-specific IOCTLs"""
        return [
            IOCTLCommand(
                name="DRM_NOUVEAU_GETPARAM",
                cmd=0xc0086440,
                direction=IOCTLDirection.READ_WRITE,
                size=8,
                description="Get device parameter",
                parameters=["param", "value"],
                driver="nouveau",
                category="device"
            ),
            IOCTLCommand(
                name="DRM_NOUVEAU_SETPARAM",
                cmd=0x40086441,
                direction=IOCTLDirection.WRITE,
                size=8,
                description="Set device parameter",
                parameters=["param", "value"],
                driver="nouveau",
                category="device"
            ),
            IOCTLCommand(
                name="DRM_NOUVEAU_CHANNEL_ALLOC",
                cmd=0xc0206442,
                direction=IOCTLDirection.READ_WRITE,
                size=32,
                description="Allocate GPU channel",
                parameters=["fb_ctxdma_handle", "tt_ctxdma_handle", "channel", "pushbuf_domains", "notifier_handle", "nr_subchan"],
                driver="nouveau",
                category="channel"
            ),
            IOCTLCommand(
                name="DRM_NOUVEAU_CHANNEL_FREE",
                cmd=0x40046443,
                direction=IOCTLDirection.WRITE,
                size=4,
                description="Free GPU channel",
                parameters=["channel"],
                driver="nouveau",
                category="channel"
            ),
            IOCTLCommand(
                name="DRM_NOUVEAU_GROBJ_ALLOC",
                cmd=0x40106444,
                direction=IOCTLDirection.WRITE,
                size=16,
                description="Allocate graphics object",
                parameters=["channel", "handle", "class"],
                driver="nouveau",
                category="graphics"
            ),
            IOCTLCommand(
                name="DRM_NOUVEAU_NOTIFIEROBJ_ALLOC",
                cmd=0xc0186445,
                direction=IOCTLDirection.READ_WRITE,
                size=24,
                description="Allocate notifier object",
                parameters=["channel", "handle", "size", "offset"],
                driver="nouveau",
                category="sync"
            ),
            IOCTLCommand(
                name="DRM_NOUVEAU_GPUOBJ_FREE",
                cmd=0x40086446,
                direction=IOCTLDirection.WRITE,
                size=8,
                description="Free GPU object",
                parameters=["channel", "handle"],
                driver="nouveau",
                category="memory"
            ),
            IOCTLCommand(
                name="DRM_NOUVEAU_GEM_NEW",
                cmd=0xc0206440,
                direction=IOCTLDirection.READ_WRITE,
                size=32,
                description="Create new GEM object",
                parameters=["size", "align", "flags", "handle", "offset"],
                driver="nouveau",
                category="gem"
            ),
            IOCTLCommand(
                name="DRM_NOUVEAU_GEM_PUSHBUF",
                cmd=0xc0506441,
                direction=IOCTLDirection.READ_WRITE,
                size=80,
                description="Submit pushbuffer",
                parameters=["channel", "nr_buffers", "buffers", "nr_relocs", "nr_push", "relocs", "push", "suffix0", "suffix1", "vram_available", "gart_available"],
                driver="nouveau",
                category="execution"
            ),
            IOCTLCommand(
                name="DRM_NOUVEAU_GEM_CPU_PREP",
                cmd=0x40086442,
                direction=IOCTLDirection.WRITE,
                size=8,
                description="Prepare GEM object for CPU access",
                parameters=["handle", "flags"],
                driver="nouveau",
                category="gem"
            ),
            IOCTLCommand(
                name="DRM_NOUVEAU_GEM_CPU_FINI",
                cmd=0x40046443,
                direction=IOCTLDirection.WRITE,
                size=4,
                description="Finish CPU access to GEM object",
                parameters=["handle"],
                driver="nouveau",
                category="gem"
            ),
            IOCTLCommand(
                name="DRM_NOUVEAU_GEM_INFO",
                cmd=0xc0186444,
                direction=IOCTLDirection.READ_WRITE,
                size=24,
                description="Get GEM object information",
                parameters=["handle", "domain", "size", "offset", "map_handle", "tile_mode", "tile_flags"],
                driver="nouveau",
                category="gem"
            ),
        ]
    
    def _init_nvidia_open_ioctls(self) -> List[IOCTLCommand]:
        """Initialize NVIDIA Open Source driver IOCTLs"""
        return [
            IOCTLCommand(
                name="NVIDIA_UVM_INITIALIZE",
                cmd=0x40045501,
                direction=IOCTLDirection.WRITE,
                size=4,
                description="Initialize UVM (Unified Virtual Memory)",
                parameters=["flags"],
                driver="nvidia-uvm",
                category="memory"
            ),
            IOCTLCommand(
                name="NVIDIA_UVM_DEINITIALIZE",
                cmd=0x5502,
                direction=IOCTLDirection.NONE,
                size=0,
                description="Deinitialize UVM",
                parameters=[],
                driver="nvidia-uvm",
                category="memory"
            ),
            IOCTLCommand(
                name="NVIDIA_UVM_CREATE_RANGE_GROUP",
                cmd=0xc0105503,
                direction=IOCTLDirection.READ_WRITE,
                size=16,
                description="Create UVM range group",
                parameters=["range_group_id", "range_group_id_out"],
                driver="nvidia-uvm",
                category="memory"
            ),
            IOCTLCommand(
                name="NVIDIA_UVM_DESTROY_RANGE_GROUP",
                cmd=0x40085504,
                direction=IOCTLDirection.WRITE,
                size=8,
                description="Destroy UVM range group",
                parameters=["range_group_id"],
                driver="nvidia-uvm",
                category="memory"
            ),
            IOCTLCommand(
                name="NVIDIA_UVM_REGISTER_GPU_VASPACE",
                cmd=0x40185505,
                direction=IOCTLDirection.WRITE,
                size=24,
                description="Register GPU virtual address space",
                parameters=["gpu_uuid", "rm_ctrl_fd", "hClient", "hVaSpace"],
                driver="nvidia-uvm",
                category="gpu"
            ),
            IOCTLCommand(
                name="NVIDIA_UVM_UNREGISTER_GPU_VASPACE",
                cmd=0x40105506,
                direction=IOCTLDirection.WRITE,
                size=16,
                description="Unregister GPU virtual address space",
                parameters=["gpu_uuid"],
                driver="nvidia-uvm",
                category="gpu"
            ),
            IOCTLCommand(
                name="NVIDIA_UVM_REGISTER_GPU",
                cmd=0xc0285507,
                direction=IOCTLDirection.READ_WRITE,
                size=40,
                description="Register GPU with UVM",
                parameters=["gpu_uuid", "rm_ctrl_fd", "hClient", "hSubDevice", "numa_enabled", "numa_node_id"],
                driver="nvidia-uvm",
                category="gpu"
            ),
            IOCTLCommand(
                name="NVIDIA_UVM_UNREGISTER_GPU",
                cmd=0x40105508,
                direction=IOCTLDirection.WRITE,
                size=16,
                description="Unregister GPU from UVM",
                parameters=["gpu_uuid"],
                driver="nvidia-uvm",
                category="gpu"
            ),
            IOCTLCommand(
                name="NVIDIA_UVM_PAGEABLE_MEM_ACCESS",
                cmd=0x40285509,
                direction=IOCTLDirection.WRITE,
                size=40,
                description="Set pageable memory access",
                parameters=["base", "length", "gpu_uuid", "is_write"],
                driver="nvidia-uvm",
                category="memory"
            ),
            IOCTLCommand(
                name="NVIDIA_UVM_REGISTER_CHANNEL",
                cmd=0x40385510,
                direction=IOCTLDirection.WRITE,
                size=56,
                description="Register GPU channel",
                parameters=["gpu_uuid", "rm_ctrl_fd", "hClient", "hChannel", "base", "length"],
                driver="nvidia-uvm",
                category="channel"
            ),
            IOCTLCommand(
                name="NVIDIA_UVM_UNREGISTER_CHANNEL",
                cmd=0x40385511,
                direction=IOCTLDirection.WRITE,
                size=56,
                description="Unregister GPU channel",
                parameters=["gpu_uuid", "rm_ctrl_fd", "hClient", "hChannel", "base", "length"],
                driver="nvidia-uvm",
                category="channel"
            ),
            IOCTLCommand(
                name="NVIDIA_UVM_ENABLE_PEER_ACCESS",
                cmd=0x40205512,
                direction=IOCTLDirection.WRITE,
                size=32,
                description="Enable peer-to-peer access between GPUs",
                parameters=["gpu_uuid_1", "gpu_uuid_2"],
                driver="nvidia-uvm",
                category="p2p"
            ),
            IOCTLCommand(
                name="NVIDIA_UVM_DISABLE_PEER_ACCESS",
                cmd=0x40205513,
                direction=IOCTLDirection.WRITE,
                size=32,
                description="Disable peer-to-peer access between GPUs",
                parameters=["gpu_uuid_1", "gpu_uuid_2"],
                driver="nvidia-uvm",
                category="p2p"
            ),
            IOCTLCommand(
                name="NVIDIA_UVM_SET_RANGE_GROUP",
                cmd=0x40205514,
                direction=IOCTLDirection.WRITE,
                size=32,
                description="Set range group for memory range",
                parameters=["base", "length", "range_group_id"],
                driver="nvidia-uvm",
                category="memory"
            ),
            IOCTLCommand(
                name="NVIDIA_UVM_MAP_EXTERNAL_ALLOCATION",
                cmd=0xc0485515,
                direction=IOCTLDirection.READ_WRITE,
                size=72,
                description="Map external allocation",
                parameters=["base", "length", "offset", "perms", "gpu_uuid", "gpu_attributes", "rm_ctrl_fd", "hClient", "hMemory"],
                driver="nvidia-uvm",
                category="memory"
            ),
        ]
    
    def _init_cuda_ioctls(self) -> List[IOCTLCommand]:
        """Initialize CUDA-related IOCTLs"""
        return [
            IOCTLCommand(
                name="CUDA_GET_VERSION",
                cmd=0x80044601,
                direction=IOCTLDirection.READ,
                size=4,
                description="Get CUDA driver version",
                parameters=["version"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_GET_DEVICE_COUNT",
                cmd=0x80044602,
                direction=IOCTLDirection.READ,
                size=4,
                description="Get number of CUDA devices",
                parameters=["count"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_GET_DEVICE_PROPERTIES",
                cmd=0xc1004603,
                direction=IOCTLDirection.READ_WRITE,
                size=256,
                description="Get CUDA device properties",
                parameters=["device", "properties"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_DEVICE_GET_ATTRIBUTE",
                cmd=0xc0084604,
                direction=IOCTLDirection.READ_WRITE,
                size=8,
                description="Get device attribute",
                parameters=["attribute", "device", "value"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_CONTEXT_CREATE",
                cmd=0xc0104605,
                direction=IOCTLDirection.READ_WRITE,
                size=16,
                description="Create CUDA context",
                parameters=["flags", "device", "context"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_CONTEXT_DESTROY",
                cmd=0x40084606,
                direction=IOCTLDirection.WRITE,
                size=8,
                description="Destroy CUDA context",
                parameters=["context"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_CONTEXT_PUSH_CURRENT",
                cmd=0x40084607,
                direction=IOCTLDirection.WRITE,
                size=8,
                description="Push context to current thread",
                parameters=["context"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_CONTEXT_POP_CURRENT",
                cmd=0x80084608,
                direction=IOCTLDirection.READ,
                size=8,
                description="Pop context from current thread",
                parameters=["context"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_CONTEXT_SET_CURRENT",
                cmd=0x40084609,
                direction=IOCTLDirection.WRITE,
                size=8,
                description="Set current context",
                parameters=["context"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_CONTEXT_GET_CURRENT",
                cmd=0x8008460a,
                direction=IOCTLDirection.READ,
                size=8,
                description="Get current context",
                parameters=["context"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_CONTEXT_SYNCHRONIZE",
                cmd=0x460b,
                direction=IOCTLDirection.NONE,
                size=0,
                description="Synchronize current context",
                parameters=[],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_MEM_ALLOC",
                cmd=0xc010460c,
                direction=IOCTLDirection.READ_WRITE,
                size=16,
                description="Allocate device memory",
                parameters=["size", "dptr"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_MEM_FREE",
                cmd=0x4008460d,
                direction=IOCTLDirection.WRITE,
                size=8,
                description="Free device memory",
                parameters=["dptr"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_MEMCPY_HTOD",
                cmd=0x4018460e,
                direction=IOCTLDirection.WRITE,
                size=24,
                description="Copy memory from host to device",
                parameters=["dst", "src", "size"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_MEMCPY_DTOH",
                cmd=0x4018460f,
                direction=IOCTLDirection.WRITE,
                size=24,
                description="Copy memory from device to host",
                parameters=["dst", "src", "size"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_MEMCPY_DTOD",
                cmd=0x40184610,
                direction=IOCTLDirection.WRITE,
                size=24,
                description="Copy memory from device to device",
                parameters=["dst", "src", "size"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_MEMSET",
                cmd=0x40144611,
                direction=IOCTLDirection.WRITE,
                size=20,
                description="Set device memory",
                parameters=["dptr", "value", "size"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_LAUNCH_KERNEL",
                cmd=0x40584612,
                direction=IOCTLDirection.WRITE,
                size=88,
                description="Launch CUDA kernel",
                parameters=["function", "gridDimX", "gridDimY", "gridDimZ", "blockDimX", "blockDimY", "blockDimZ", "sharedMemBytes", "stream", "kernelParams", "extra"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_STREAM_CREATE",
                cmd=0x80084613,
                direction=IOCTLDirection.READ,
                size=8,
                description="Create CUDA stream",
                parameters=["stream"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_STREAM_DESTROY",
                cmd=0x40084614,
                direction=IOCTLDirection.WRITE,
                size=8,
                description="Destroy CUDA stream",
                parameters=["stream"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_STREAM_SYNCHRONIZE",
                cmd=0x40084615,
                direction=IOCTLDirection.WRITE,
                size=8,
                description="Synchronize CUDA stream",
                parameters=["stream"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_EVENT_CREATE",
                cmd=0x80084616,
                direction=IOCTLDirection.READ,
                size=8,
                description="Create CUDA event",
                parameters=["event"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_EVENT_DESTROY",
                cmd=0x40084617,
                direction=IOCTLDirection.WRITE,
                size=8,
                description="Destroy CUDA event",
                parameters=["event"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_EVENT_RECORD",
                cmd=0x40104618,
                direction=IOCTLDirection.WRITE,
                size=16,
                description="Record CUDA event",
                parameters=["event", "stream"],
                driver="nvidia",
                category="cuda"
            ),
            IOCTLCommand(
                name="CUDA_EVENT_SYNCHRONIZE",
                cmd=0x40084619,
                direction=IOCTLDirection.WRITE,
                size=8,
                description="Synchronize CUDA event",
                parameters=["event"],
                driver="nvidia",
                category="cuda"
            ),
        ]