#!/usr/bin/env python3
"""
Demo script for shittyNVIDIA Python module
Shows all the ways this driver doesn't work!
"""

import sys
import os

# Add the module to path for development
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import shitty_nvidia

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}\n")

def main():
    print_section("shittyNVIDIA Demo")
    
    # Check compatibility
    print_section("Compatibility Check")
    compatible = shitty_nvidia.check_compatibility()
    if compatible:
        print("✅ System is compatible with shittyNVIDIA!")
        print("   (No NVIDIA hardware found - perfect!)")
    else:
        print("❌ System has NVIDIA hardware!")
        print("   shittyNVIDIA doesn't work with real GPUs.")
    
    # Get device count
    print_section("Device Count")
    count = shitty_nvidia.get_device_count()
    print(f"NVIDIA Devices Found: {count}")
    print("(This is always 0 - as designed!)")
    
    # Get driver version
    print_section("Driver Version")
    version = shitty_nvidia.get_driver_version()
    print(f"Driver Version: {version}")
    
    # Check CUDA availability
    print_section("CUDA Support")
    cuda = shitty_nvidia.cuda_available()
    print(f"CUDA Available: {cuda}")
    print("(We don't support CUDA - or anything useful)")
    
    # List devices
    print_section("Device List")
    devices = shitty_nvidia.list_devices()
    print(f"Devices: {devices}")
    print("(Empty list - we have no devices!)")
    
    # Get driver info
    print_section("Driver Information")
    info = shitty_nvidia.get_driver_info()
    print(f"Name: {info['name']}")
    print(f"Version: {info['version']}")
    print(f"Description: {info['description']}")
    print(f"Supported Devices: {info['supported_devices']}")
    print(f"CUDA Support: {info['cuda_support']}")
    print(f"OpenCL Support: {info['opencl_support']}")
    print(f"Vulkan Support: {info['vulkan_support']}")
    print(f"\nFeatures:")
    for feature in info['features']:
        print(f"  - {feature}")
    print(f"\nWarning: {info['warning']}")
    
    # Try to create a device (will fail)
    print_section("Device Creation Test")
    print("Attempting to create device 0...")
    try:
        device = shitty_nvidia.Device(0)
        print("❌ ERROR: Device creation succeeded! This should never happen!")
    except shitty_nvidia.NoDeviceError as e:
        print(f"✅ Failed successfully!")
        print(f"   Error: {e}")
    
    # Check if installed
    print_section("Installation Check")
    installed = shitty_nvidia.is_available()
    if installed:
        print("✅ shittyNVIDIA is installed at /usr/local/shittyNVIDIA")
    else:
        print("❌ shittyNVIDIA is not installed")
        print("   Run: ./install-nvidia-compat.sh install")
    
    print_section("Demo Complete")
    print("Remember: shittyNVIDIA works with exactly 0 NVIDIA devices!")
    print("For real NVIDIA support, use official drivers from nvidia.com\n")

if __name__ == "__main__":
    main()
