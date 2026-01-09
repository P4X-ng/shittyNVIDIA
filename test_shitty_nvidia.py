#!/usr/bin/env python3
"""
Test suite for shittyNVIDIA
"""

import unittest
import sys
import os

# Add the module to path for development
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import shitty_nvidia


class TestShittyNVIDIA(unittest.TestCase):
    """Test cases for shittyNVIDIA module"""
    
    def test_device_count_is_zero(self):
        """Test that device count is always 0"""
        self.assertEqual(shitty_nvidia.get_device_count(), 0)
    
    def test_driver_version(self):
        """Test driver version is set"""
        version = shitty_nvidia.get_driver_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, "0.1.0")
    
    def test_cuda_not_available(self):
        """Test that CUDA is not available"""
        self.assertFalse(shitty_nvidia.cuda_available())
    
    def test_list_devices_empty(self):
        """Test that device list is empty"""
        devices = shitty_nvidia.list_devices()
        self.assertIsInstance(devices, list)
        self.assertEqual(len(devices), 0)
    
    def test_device_creation_fails(self):
        """Test that device creation always fails"""
        with self.assertRaises(shitty_nvidia.NoDeviceError):
            shitty_nvidia.Device(0)
    
    def test_get_driver_info(self):
        """Test driver info returns correct structure"""
        info = shitty_nvidia.get_driver_info()
        self.assertIsInstance(info, dict)
        self.assertEqual(info['name'], 'shittyNVIDIA')
        self.assertEqual(info['version'], '0.1.0')
        self.assertEqual(info['supported_devices'], 0)
        self.assertFalse(info['cuda_support'])
        self.assertFalse(info['opencl_support'])
        self.assertFalse(info['vulkan_support'])
        self.assertIn('features', info)
        self.assertIsInstance(info['features'], list)
        self.assertGreater(len(info['features']), 0)
    
    def test_compatibility_check(self):
        """Test compatibility check"""
        # Should return True or False, never crash
        result = shitty_nvidia.check_compatibility()
        self.assertIsInstance(result, bool)
    
    def test_device_get_count_alias(self):
        """Test alias function"""
        self.assertEqual(shitty_nvidia.device_get_count(), 0)
    
    def test_driver_get_version_alias(self):
        """Test alias function"""
        self.assertEqual(shitty_nvidia.driver_get_version(), "0.1.0")
    
    def test_is_available(self):
        """Test installation check"""
        # Should return True or False, never crash
        result = shitty_nvidia.is_available()
        self.assertIsInstance(result, bool)
    
    def test_exception_hierarchy(self):
        """Test exception hierarchy"""
        self.assertTrue(issubclass(shitty_nvidia.NoDeviceError, 
                                   shitty_nvidia.ShittyNVIDIAError))
        self.assertTrue(issubclass(shitty_nvidia.ShittyNVIDIAError, 
                                   Exception))


class TestDevice(unittest.TestCase):
    """Test cases for Device class"""
    
    def test_device_init_fails(self):
        """Test Device initialization always fails"""
        with self.assertRaises(shitty_nvidia.NoDeviceError) as cm:
            shitty_nvidia.Device(0)
        self.assertIn("0 NVIDIA devices", str(cm.exception))
    
    def test_device_methods_dont_exist(self):
        """Test device methods can't be called without instance"""
        # Since we can't create an instance, we can't test these methods
        # but we can verify they exist in the class
        self.assertTrue(hasattr(shitty_nvidia.Device, 'get_name'))
        self.assertTrue(hasattr(shitty_nvidia.Device, 'get_memory_info'))
        self.assertTrue(hasattr(shitty_nvidia.Device, 'get_temperature'))


class TestModuleMetadata(unittest.TestCase):
    """Test module metadata"""
    
    def test_version_attribute(self):
        """Test __version__ attribute exists"""
        self.assertTrue(hasattr(shitty_nvidia, '__version__'))
        self.assertEqual(shitty_nvidia.__version__, '0.1.0')
    
    def test_author_attribute(self):
        """Test __author__ attribute exists"""
        self.assertTrue(hasattr(shitty_nvidia, '__author__'))
    
    def test_license_attribute(self):
        """Test __license__ attribute exists"""
        self.assertTrue(hasattr(shitty_nvidia, '__license__'))
        self.assertEqual(shitty_nvidia.__license__, 'MIT')


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestShittyNVIDIA))
    suite.addTests(loader.loadTestsFromTestCase(TestDevice))
    suite.addTests(loader.loadTestsFromTestCase(TestModuleMetadata))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
