#!/usr/bin/env python3
"""
Test script for nvidia_compat kernel module
Demonstrates IOCTL interaction with /dev/nvidia1337
"""

import os
import sys
import fcntl
import struct

DEVICE_PATH = "/dev/nvidia1337"

# NVIDIA IOCTL codes (matching kernel module)
NV_IOCTL_MAGIC = ord('F')
NV_ESC_CARD_INFO = 0xC008_4600
NV_ESC_CHECK_VERSION = 0xC008_4601

def test_device_exists():
    """Test if the device node exists"""
    print("Testing device existence...")
    if os.path.exists(DEVICE_PATH):
        print(f"✓ {DEVICE_PATH} exists")
        stat_info = os.stat(DEVICE_PATH)
        print(f"  Mode: {oct(stat_info.st_mode)}")
        print(f"  Owner: {stat_info.st_uid}:{stat_info.st_gid}")
        return True
    else:
        print(f"✗ {DEVICE_PATH} not found")
        print("  Make sure the nvidia_compat kernel module is loaded:")
        print("  sudo modprobe nvidia_compat")
        return False

def test_device_read():
    """Test reading from the device"""
    print("\nTesting device read...")
    try:
        with open(DEVICE_PATH, 'r') as f:
            data = f.read()
            print(f"✓ Read from device:")
            for line in data.strip().split('\n'):
                print(f"  {line}")
            return True
    except PermissionError:
        print("✗ Permission denied. Try with sudo.")
        return False
    except Exception as e:
        print(f"✗ Error reading device: {e}")
        return False

def test_device_open():
    """Test opening the device"""
    print("\nTesting device open...")
    try:
        fd = os.open(DEVICE_PATH, os.O_RDWR)
        print(f"✓ Device opened successfully (fd={fd})")
        os.close(fd)
        return True
    except PermissionError:
        print("✗ Permission denied. Try with sudo.")
        return False
    except Exception as e:
        print(f"✗ Error opening device: {e}")
        return False

def test_ioctl():
    """Test IOCTL calls to the device"""
    print("\nTesting IOCTL calls...")
    try:
        # Note: This requires proper permissions and may not work without sudo
        fd = os.open(DEVICE_PATH, os.O_RDWR)
        print(f"✓ Device opened for IOCTL")
        
        # Try a simple IOCTL (this may fail if the structure doesn't match)
        try:
            # Create a buffer for the response
            buf = bytearray(1024)
            result = fcntl.ioctl(fd, NV_ESC_CARD_INFO, buf)
            print(f"✓ IOCTL NV_ESC_CARD_INFO executed")
            print(f"  Result: {result}")
        except Exception as e:
            print(f"  IOCTL call result: {e}")
            print("  (This is expected if structures don't match)")
        
        os.close(fd)
        return True
    except PermissionError:
        print("✗ Permission denied. Try with sudo.")
        return False
    except Exception as e:
        print(f"✗ Error with IOCTL: {e}")
        return False

def check_kernel_module():
    """Check if the kernel module is loaded"""
    print("\nChecking kernel module status...")
    try:
        with open('/proc/modules', 'r') as f:
            modules = f.read()
            if 'nvidia_compat' in modules:
                print("✓ nvidia_compat module is loaded")
                # Extract module info
                for line in modules.split('\n'):
                    if 'nvidia_compat' in line:
                        print(f"  {line}")
                return True
            else:
                print("✗ nvidia_compat module is not loaded")
                print("  Load it with: sudo modprobe nvidia_compat")
                return False
    except Exception as e:
        print(f"✗ Error checking modules: {e}")
        return False

def show_module_info():
    """Show module parameters"""
    print("\nModule parameters:")
    params_path = "/sys/module/nvidia_compat/parameters"
    if os.path.exists(params_path):
        for param in ['enable_fake_gpu', 'fake_gpu_name', 'fake_gpu_memory']:
            param_file = os.path.join(params_path, param)
            if os.path.exists(param_file):
                try:
                    with open(param_file, 'r') as f:
                        value = f.read().strip()
                        print(f"  {param}: {value}")
                except:
                    pass
    else:
        print("  Module parameters not accessible")

def main():
    print("=" * 60)
    print("nvidia_compat Kernel Module Test")
    print("=" * 60)
    
    # Run all tests
    tests = [
        ("Module loaded", check_kernel_module),
        ("Device exists", test_device_exists),
        ("Device readable", test_device_read),
        ("Device open", test_device_open),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\nUnexpected error in {name}: {e}")
            results.append((name, False))
    
    # Show module info if module is loaded
    if results[0][1]:  # Module loaded
        show_module_info()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The nvidia_compat module is working!")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        if os.geteuid() != 0:
            print("   Try running with sudo for full functionality.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
