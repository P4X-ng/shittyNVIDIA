"""
shittyNVIDIA - The worst NVIDIA driver ever
Works with exactly 0 NVIDIA devices

Based on nvidia-compat concepts from HyperionGray/pf-web-poly-compile-helper-runner
"""

__version__ = "0.0.0"
__author__ = "shittyNVIDIA Contributors"
__license__ = "MIT"

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
    
    # Check for nvidia-smi
    try:
        result = subprocess.run(['which', 'nvidia-smi'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            # Found nvidia-smi - check if it's ours
            result = subprocess.run(['nvidia-smi'], 
                                  capture_output=True, 
                                  text=True)
            if 'shittyNVIDIA' in result.stdout:
                return True
            else:
                return False  # Real NVIDIA detected
    except:
        pass
    
    # Check for NVIDIA hardware via lspci
    try:
        result = subprocess.run(['lspci'], 
                              capture_output=True, 
                              text=True)
        if 'nvidia' in result.stdout.lower():
            return False  # NVIDIA hardware found
    except:
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
    return {
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
        'warning': 'This is shittyNVIDIA. Do not use in production. Or anywhere.'
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
