#!/usr/bin/env python3
"""
Test suite for IOCTL mapping functionality
"""

import unittest
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import shitty_nvidia
from shitty_nvidia import OperationCategory


class TestIOCTLMappings(unittest.TestCase):
    """Test IOCTL mapping functionality"""
    
    def test_mapping_module_available(self):
        """Test that mapping modules are available"""
        summary = shitty_nvidia.get_analysis_summary()
        self.assertTrue(summary['available'], "Analysis modules should be available")
    
    def test_find_cuda_equivalent(self):
        """Test finding CUDA operation equivalent"""
        result = shitty_nvidia.find_equivalent_operation('cuda', 'cuMemAlloc')
        
        self.assertIsNotNone(result)
        self.assertIn('amd', result)
        self.assertIn('nvidia', result)
        self.assertIn('cuda', result)
        self.assertIn('cpu', result)
        self.assertIn('description', result)
        
        # Check specific mappings
        self.assertEqual(result['cuda'], 'cuMemAlloc()')
        self.assertEqual(result['cpu'], 'malloc()')
        self.assertIn('GEM_CREATE', result['amd'])
    
    def test_find_amd_equivalent(self):
        """Test finding AMD IOCTL equivalent"""
        result = shitty_nvidia.find_equivalent_operation('amd', 'DRM_IOCTL_AMDGPU_CS')
        
        self.assertIsNotNone(result)
        self.assertIn('DRM_IOCTL_AMDGPU_CS', result['amd'])
        self.assertIn('cuLaunchKernel', result['cuda'])
    
    def test_get_mappings_by_category(self):
        """Test getting mappings by category"""
        mappings = shitty_nvidia.get_ioctl_mappings(OperationCategory.MEMORY_ALLOC)
        
        self.assertIsNotNone(mappings)
        self.assertIn('total', mappings)
        self.assertIn('mappings', mappings)
        self.assertGreater(mappings['total'], 0)
        
        # Check that mappings have required fields
        if mappings['total'] > 0:
            first_mapping = mappings['mappings'][0]
            self.assertIn('amd', first_mapping)
            self.assertIn('nvidia', first_mapping)
            self.assertIn('cuda', first_mapping)
            self.assertIn('cpu', first_mapping)
            self.assertIn('description', first_mapping)
    
    def test_get_all_mappings(self):
        """Test getting all mappings"""
        mappings = shitty_nvidia.get_ioctl_mappings()
        
        self.assertIsNotNone(mappings)
        self.assertIn('total', mappings)
        self.assertIn('mappings', mappings)
        self.assertGreater(mappings['total'], 10, "Should have at least 10 mappings")
    
    def test_synchronization_mappings(self):
        """Test synchronization operation mappings"""
        mappings = shitty_nvidia.get_ioctl_mappings(OperationCategory.SYNCHRONIZATION)
        
        self.assertIsNotNone(mappings)
        self.assertGreater(mappings['total'], 0)
        
        # Check that we have event-related mappings
        cuda_apis = [m['cuda'] for m in mappings['mappings'] if m['cuda']]
        self.assertTrue(any('Event' in api for api in cuda_apis if api))
    
    def test_context_mappings(self):
        """Test context management mappings"""
        result = shitty_nvidia.find_equivalent_operation('cuda', 'cuCtxCreate')
        
        self.assertIsNotNone(result)
        self.assertIn('pthread', result['cpu'].lower())
    
    def test_memory_copy_mappings(self):
        """Test memory copy operation mappings"""
        result = shitty_nvidia.find_equivalent_operation('cuda', 'cuMemcpyHtoD')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['cpu'], 'memcpy()')
    
    def test_device_info_mappings(self):
        """Test device information query mappings"""
        mappings = shitty_nvidia.get_ioctl_mappings(OperationCategory.DEVICE_INFO)
        
        self.assertIsNotNone(mappings)
        self.assertGreater(mappings['total'], 0)
    
    def test_mapping_database_statistics(self):
        """Test that mapping database has reasonable statistics"""
        from shitty_nvidia.ioctl_mappings import IOCTLMappingDatabase
        
        db = IOCTLMappingDatabase()
        stats = db.get_statistics()
        
        self.assertIn('total_mappings', stats)
        self.assertIn('categories', stats)
        self.assertIn('amd_ioctls', stats)
        self.assertIn('nvidia_ioctls', stats)
        self.assertIn('cuda_apis', stats)
        self.assertIn('cpu_equivalents', stats)
        
        # Should have a reasonable number of mappings
        self.assertGreater(stats['total_mappings'], 15)
        self.assertGreater(stats['amd_ioctls'], 15)
        self.assertGreater(stats['cuda_apis'], 15)
    
    def test_shitty_nvidia_implements_zero(self):
        """Test that shittyNVIDIA proudly implements zero operations"""
        result = shitty_nvidia.find_equivalent_operation('cuda', 'cuMemAlloc')
        
        # Should mention that shittyNVIDIA doesn't implement it
        self.assertIn('shitty_nvidia', result)
        self.assertIn('Not implemented', result['shitty_nvidia'])


class TestMappingIntegration(unittest.TestCase):
    """Test integration of mapping with main module"""
    
    def test_analysis_summary_includes_mappings(self):
        """Test that analysis summary includes mapping features"""
        summary = shitty_nvidia.get_analysis_summary()
        
        if summary['available']:
            features_str = ' '.join(summary['features'])
            self.assertIn('mapping', features_str.lower())
    
    def test_driver_info_mentions_mappings(self):
        """Test that driver info mentions mapping features"""
        info = shitty_nvidia.get_driver_info()
        
        if info.get('analysis_features'):
            self.assertIn('new_features', info)
            features_str = ' '.join(info['new_features'])
            self.assertIn('mapping', features_str.lower())


def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
