"""
shittyNVIDIA - The worst NVIDIA driver ever
Works with exactly 0 NVIDIA devices

Based on nvidia-compat concepts from HyperionGray/pf-web-poly-compile-helper-runner

Now with comprehensive IOCTL analysis of NVIDIA and AMD open source drivers!
Because if we're going to be terrible, we should at least understand what we're not doing.
"""

__version__ = "0.1.0"  # Upgraded for IOCTL analysis features
__author__ = "shittyNVIDIA Contributors"
__license__ = "MIT"

# Import our analysis modules
try:
    from .ioctl_analysis import NVIDIAIOCTLAnalyzer, IOCTLCommand, IOCTLDirection
    from .gpu_comparison import GPUDriverComparator, print_comparison_report
    ANALYSIS_AVAILABLE = True
except ImportError:
    ANALYSIS_AVAILABLE = False

class ShittyNVIDIAError(Exception):
    """Base exception for shittyNVIDIA"""
    pass


class NoDeviceError(ShittyNVIDIAError):
    """Raised when trying to use NVIDIA functionality (which we don't support)"""
    pass


def check_compatibility():
    """
    Check if the system is compatible with shittyNVIDIA.
    
    Returns:
        bool: True if NO NVIDIA devices are found (compatible)
              False if NVIDIA devices are found (incompatible)
    """
    import subprocess
    import shutil
    
    # Check for nvidia-smi
    try:
        nvidia_smi_path = shutil.which('nvidia-smi')
        if nvidia_smi_path:
            # Found nvidia-smi - check if it's ours
            result = subprocess.run(['nvidia-smi'], 
                                  capture_output=True, 
                                  text=True)
            if 'shittyNVIDIA' in result.stdout:
                return True
            else:
                return False  # Real NVIDIA detected
    except Exception:
        pass
    
    # Check for NVIDIA hardware via lspci
    try:
        result = subprocess.run(['lspci'], 
                              capture_output=True, 
                              text=True)
        if 'nvidia' in result.stdout.lower():
            return False  # NVIDIA hardware found
    except Exception:
        pass
    
    # No NVIDIA found - perfect!
    return True


def get_device_count():
    """
    Get the number of NVIDIA devices.
    
    Returns:
        int: Always returns 0 (because we work with 0 devices)
    """
    return 0


def get_driver_version():
    """
    Get the driver version.
    
    Returns:
        str: The version of this terrible driver
    """
    return __version__


def cuda_available():
    """
    Check if CUDA is available.
    
    Returns:
        bool: Always False (we don't support CUDA)
    """
    return False


class Device:
    """
    Represents an NVIDIA device (that doesn't exist).
    """
    
    def __init__(self, device_id=0):
        """
        Initialize a device.
        
        Args:
            device_id: Device ID (ignored, we have none)
            
        Raises:
            NoDeviceError: Always, because we have no devices
        """
        raise NoDeviceError(
            "Cannot create device: shittyNVIDIA works with 0 NVIDIA devices!\n"
            "This is by design. We're the worst NVIDIA driver ever."
        )
    
    def get_name(self):
        """Get device name"""
        raise NoDeviceError("No devices available")
    
    def get_memory_info(self):
        """Get memory information"""
        raise NoDeviceError("No devices available")
    
    def get_temperature(self):
        """Get temperature"""
        raise NoDeviceError("No devices available")


def list_devices():
    """
    List all NVIDIA devices.
    
    Returns:
        list: Empty list (we have no devices)
    """
    return []


def get_driver_info():
    """
    Get detailed driver information.
    
    Returns:
        dict: Information about this terrible driver
    """
    info = {
        'name': 'shittyNVIDIA',
        'version': __version__,
        'description': 'The worst NVIDIA driver ever - works with 0 nvidia devices',
        'supported_devices': 0,
        'cuda_support': False,
        'opencl_support': False,
        'vulkan_support': False,
        'features': [
            'Guaranteed to not work with any NVIDIA hardware',
            'Perfect compatibility with systems without NVIDIA',
            'Zero performance overhead (because it does nothing)',
            'No bloatware',
            'Smallest driver footprint possible'
        ],
        'warning': 'This is shittyNVIDIA. Do not use in production. Or anywhere.',
        'analysis_features': ANALYSIS_AVAILABLE
    }
    
    if ANALYSIS_AVAILABLE:
        info['new_features'] = [
            'Comprehensive NVIDIA IOCTL analysis (nouveau, nvidia-open, CUDA)',
            'AMD driver IOCTL analysis (amdgpu, radeon)',
            'GPU driver architecture comparison',
            'Humorous technical commentary',
            'Educational insights into what real drivers do'
        ]
        info['ioctl_analysis'] = 'Available - analyze what we proudly don\'t implement!'
    
    return info


def analyze_nvidia_ioctls():
    """
    Analyze NVIDIA driver IOCTLs.
    
    Returns:
        dict: Analysis results or error message
    """
    if not ANALYSIS_AVAILABLE:
        return {
            'error': 'IOCTL analysis modules not available',
            'suggestion': 'Check if analysis modules are properly installed'
        }
    
    try:
        analyzer = NVIDIAIOCTLAnalyzer()
        return {
            'total_ioctls': len(analyzer.get_all_ioctls()),
            'drm_ioctls': len(analyzer.drm_ioctls),
            'nouveau_ioctls': len(analyzer.nouveau_ioctls),
            'nvidia_open_ioctls': len(analyzer.nvidia_open_ioctls),
            'cuda_ioctls': len(analyzer.cuda_ioctls),
            'cuda_analysis': analyzer.analyze_cuda_ioctls(),
            'categories': {
                'core': len(analyzer.get_ioctls_by_category('core')),
                'memory': len(analyzer.get_ioctls_by_category('memory')),
                'gem': len(analyzer.get_ioctls_by_category('gem')),
                'cuda': len(analyzer.get_ioctls_by_category('cuda')),
                'sync': len(analyzer.get_ioctls_by_category('sync')),
                'execution': len(analyzer.get_ioctls_by_category('execution'))
            },
            'shitty_nvidia_comment': 'We implement exactly 0 of these IOCTLs. Efficiency!'
        }
    except Exception as e:
        return {
            'error': f'Analysis failed: {str(e)}',
            'shitty_nvidia_comment': 'Even our analysis is broken. Consistent!'
        }


def compare_gpu_drivers():
    """
    Compare NVIDIA and AMD GPU drivers.
    
    Returns:
        dict: Comparison results or error message
    """
    if not ANALYSIS_AVAILABLE:
        return {
            'error': 'GPU comparison modules not available',
            'suggestion': 'Check if analysis modules are properly installed'
        }
    
    try:
        comparator = GPUDriverComparator()
        return comparator.get_comprehensive_report()
    except Exception as e:
        return {
            'error': f'Comparison failed: {str(e)}',
            'shitty_nvidia_comment': 'We can\'t even compare properly. Peak performance!'
        }


def print_ioctl_analysis():
    """Print formatted IOCTL analysis"""
    if not ANALYSIS_AVAILABLE:
        print("❌ IOCTL analysis not available")
        print("   Analysis modules could not be imported")
        return
    
    print("🔍 NVIDIA IOCTL ANALYSIS")
    print("=" * 50)
    
    analysis = analyze_nvidia_ioctls()
    if 'error' in analysis:
        print(f"❌ Error: {analysis['error']}")
        return
    
    print(f"📊 Total IOCTLs analyzed: {analysis['total_ioctls']}")
    print(f"   DRM core: {analysis['drm_ioctls']}")
    print(f"   Nouveau:  {analysis['nouveau_ioctls']}")
    print(f"   NVIDIA:   {analysis['nvidia_open_ioctls']}")
    print(f"   CUDA:     {analysis['cuda_ioctls']}")
    print()
    
    print("📈 CUDA Analysis:")
    cuda = analysis['cuda_analysis']
    print(f"   Memory operations: {cuda['memory_operations']}")
    print(f"   Context operations: {cuda['context_operations']}")
    print(f"   Stream operations: {cuda['stream_operations']}")
    print(f"   Event operations: {cuda['event_operations']}")
    print(f"   Kernel operations: {cuda['kernel_operations']}")
    print(f"   Complexity score: {cuda['complexity_score']:.1f}")
    print()
    
    print("🎭 shittyNVIDIA Commentary:")
    print(f"   {analysis['shitty_nvidia_comment']}")
    print()
    
    print("💡 Want the full comparison? Try:")
    print("   import shitty_nvidia")
    print("   shitty_nvidia.print_comparison_report()")


def get_analysis_summary():
    """Get a summary of analysis capabilities"""
    if not ANALYSIS_AVAILABLE:
        return {
            'available': False,
            'reason': 'Analysis modules not imported',
            'features': []
        }
    
    return {
        'available': True,
        'features': [
            'NVIDIA IOCTL analysis (DRM, Nouveau, NVIDIA-open, CUDA)',
            'AMD IOCTL analysis (DRM, AMDGPU, Radeon)',
            'GPU driver architecture comparison',
            'Compute model analysis (CUDA vs ROCm)',
            'Memory management comparison',
            'Humorous technical commentary'
        ],
        'functions': [
            'analyze_nvidia_ioctls()',
            'compare_gpu_drivers()',
            'print_ioctl_analysis()',
            'print_comparison_report()'
        ],
        'total_ioctls_analyzed': '100+',
        'shitty_nvidia_implements': 0
    }


# Compatibility aliases mimicking real nvidia modules
def device_get_count():
    """Alias for get_device_count()"""
    return get_device_count()


def driver_get_version():
    """Alias for get_driver_version()"""
    return get_driver_version()


def is_available():
    """
    Check if shittyNVIDIA is available.
    
    Returns:
        bool: True if installed, False otherwise
    """
    import os
    return os.path.exists('/usr/local/shittyNVIDIA')
