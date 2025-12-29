#!/usr/bin/env python3
"""
Example usage scenarios for shittyNVIDIA
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import shitty_nvidia


def example_1_basic_check():
    """Example 1: Basic compatibility check"""
    print("Example 1: Basic Compatibility Check")
    print("-" * 40)
    
    if shitty_nvidia.check_compatibility():
        print("✅ System compatible - No NVIDIA hardware found!")
    else:
        print("❌ NVIDIA hardware detected - shittyNVIDIA won't work")
    print()


def example_2_device_enumeration():
    """Example 2: Enumerate devices (will always be 0)"""
    print("Example 2: Device Enumeration")
    print("-" * 40)
    
    count = shitty_nvidia.get_device_count()
    print(f"Number of NVIDIA devices: {count}")
    
    devices = shitty_nvidia.list_devices()
    print(f"Device list: {devices}")
    
    if count == 0:
        print("Perfect! No devices found as expected.")
    print()


def example_3_feature_detection():
    """Example 3: Feature detection"""
    print("Example 3: Feature Detection")
    print("-" * 40)
    
    print(f"CUDA Available: {shitty_nvidia.cuda_available()}")
    print(f"Driver Version: {shitty_nvidia.get_driver_version()}")
    print(f"Installed: {shitty_nvidia.is_available()}")
    print()


def example_4_error_handling():
    """Example 4: Proper error handling"""
    print("Example 4: Error Handling")
    print("-" * 40)
    
    try:
        # Try to create a device (will always fail)
        device = shitty_nvidia.Device(0)
        print("This should never print!")
    except shitty_nvidia.NoDeviceError as e:
        print(f"Caught expected error: {type(e).__name__}")
        print(f"Message: {e}")
    except Exception as e:
        print(f"Caught unexpected error: {e}")
    print()


def example_5_driver_info():
    """Example 5: Get detailed driver information"""
    print("Example 5: Driver Information")
    print("-" * 40)
    
    info = shitty_nvidia.get_driver_info()
    
    print(f"Driver: {info['name']} v{info['version']}")
    print(f"Description: {info['description']}")
    print(f"\nCapabilities:")
    print(f"  - Supported Devices: {info['supported_devices']}")
    print(f"  - CUDA: {info['cuda_support']}")
    print(f"  - OpenCL: {info['opencl_support']}")
    print(f"  - Vulkan: {info['vulkan_support']}")
    print(f"\nKey Features:")
    for feature in info['features']:
        print(f"  • {feature}")
    print()


def example_6_integration_pattern():
    """Example 6: Integration pattern for applications"""
    print("Example 6: Application Integration Pattern")
    print("-" * 40)
    
    # Fallback pattern for applications
    print("Checking for GPU acceleration...")
    
    device_count = shitty_nvidia.get_device_count()
    if device_count > 0:
        print("Using NVIDIA GPU acceleration")
        # Would initialize GPU here
    else:
        print("No GPU found, falling back to CPU")
        # Fallback to CPU implementation
    
    print("(In this case, always falls back to CPU!)")
    print()


def main():
    """Run all examples"""
    print("=" * 60)
    print(" shittyNVIDIA Usage Examples")
    print("=" * 60)
    print()
    
    examples = [
        example_1_basic_check,
        example_2_device_enumeration,
        example_3_feature_detection,
        example_4_error_handling,
        example_5_driver_info,
        example_6_integration_pattern,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"Error running example: {e}")
            import traceback
            traceback.print_exc()
            print()
    
    print("=" * 60)
    print(" Examples Complete")
    print("=" * 60)
    print("\nRemember: shittyNVIDIA works with 0 NVIDIA devices!")


if __name__ == "__main__":
    main()
