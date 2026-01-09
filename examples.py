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
    print(f"  - Analysis Features: {info.get('analysis_features', False)}")
    
    print(f"\nKey Features:")
    for feature in info['features']:
        print(f"  • {feature}")
    
    # Show new analysis features if available
    if info.get('analysis_features') and 'new_features' in info:
        print(f"\nNew Analysis Features:")
        for feature in info['new_features']:
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


def example_7_ioctl_analysis():
    """Example 7: IOCTL Analysis (New Feature)"""
    print("Example 7: IOCTL Analysis")
    print("-" * 40)
    
    # Check if analysis is available
    summary = shitty_nvidia.get_analysis_summary()
    if not summary['available']:
        print(f"❌ Analysis not available: {summary['reason']}")
        print("   The basic shittyNVIDIA functionality still works!")
        print()
        return
    
    print("🔍 Analyzing NVIDIA driver IOCTLs...")
    analysis = shitty_nvidia.analyze_nvidia_ioctls()
    
    if 'error' in analysis:
        print(f"❌ Analysis failed: {analysis['error']}")
        print()
        return
    
    print(f"📊 Found {analysis['total_ioctls']} total IOCTLs:")
    print(f"   • DRM core: {analysis['drm_ioctls']}")
    print(f"   • Nouveau: {analysis['nouveau_ioctls']}")
    print(f"   • NVIDIA-open: {analysis['nvidia_open_ioctls']}")
    print(f"   • CUDA: {analysis['cuda_ioctls']}")
    
    print(f"\n📈 CUDA Analysis:")
    cuda = analysis['cuda_analysis']
    print(f"   • Memory operations: {cuda['memory_operations']}")
    print(f"   • Context operations: {cuda['context_operations']}")
    print(f"   • Stream operations: {cuda['stream_operations']}")
    print(f"   • Complexity score: {cuda['complexity_score']:.1f}")
    
    print(f"\n🎭 {analysis['shitty_nvidia_comment']}")
    print()


def example_8_gpu_comparison():
    """Example 8: GPU Driver Comparison (New Feature)"""
    print("Example 8: GPU Driver Comparison")
    print("-" * 40)
    
    # Check if comparison is available
    summary = shitty_nvidia.get_analysis_summary()
    if not summary['available']:
        print(f"❌ Comparison not available: {summary['reason']}")
        print()
        return
    
    print("🆚 Comparing NVIDIA vs AMD drivers...")
    comparison = shitty_nvidia.compare_gpu_drivers()
    
    if 'error' in comparison:
        print(f"❌ Comparison failed: {comparison['error']}")
        print()
        return
    
    # Show executive summary
    exec_summary = comparison['executive_summary']
    print(f"📊 Executive Summary:")
    print(f"   • NVIDIA drivers: {exec_summary['nvidia_drivers']}")
    print(f"   • AMD drivers: {exec_summary['amd_drivers']}")
    print(f"   • Concepts analyzed: {exec_summary['total_concepts_analyzed']}")
    print(f"   • shittyNVIDIA compatibility: {exec_summary['shitty_nvidia_compatibility']}")
    
    # Show IOCTL analysis
    ioctl_analysis = comparison['ioctl_analysis']
    print(f"\n📈 IOCTL Complexity:")
    print(f"   • NVIDIA total: {ioctl_analysis['nvidia']['total']}")
    print(f"   • AMD total: {ioctl_analysis['amd']['total']}")
    print(f"   • NVIDIA complexity: {ioctl_analysis['nvidia']['complexity_score']}/10")
    print(f"   • AMD complexity: {ioctl_analysis['amd']['complexity_score']}/10")
    
    # Show conclusion
    conclusion = comparison['conclusion']
    print(f"\n🎯 Recommendations:")
    print(f"   • Best for performance: {conclusion['best_for_performance']}")
    print(f"   • Best for openness: {conclusion['best_for_openness']}")
    print(f"   • Best for comedy: {conclusion['best_for_comedy']}")
    print(f"   • Our recommendation: {conclusion['recommendation']}")
    
    print()


def example_9_full_analysis_demo():
    """Example 9: Full Analysis Demo"""
    print("Example 9: Full Analysis Demo")
    print("-" * 40)
    
    # Check if analysis is available
    summary = shitty_nvidia.get_analysis_summary()
    if not summary['available']:
        print(f"❌ Full analysis not available: {summary['reason']}")
        print("   Try running: python ioctl_demo.py")
        print()
        return
    
    print("🎭 Running comprehensive analysis...")
    print("\n" + "="*50)
    
    try:
        # Run the formatted IOCTL analysis
        shitty_nvidia.print_ioctl_analysis()
        
        print("\n" + "="*50)
        print("Want the full comparison report? Run:")
        print("  python ioctl_demo.py")
        print("or:")
        print("  shitty_nvidia.print_comparison_report()")
        
    except Exception as e:
        print(f"❌ Full analysis failed: {e}")
    
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
        example_7_ioctl_analysis,
        example_8_gpu_comparison,
        example_9_full_analysis_demo,
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
    print("But now it can analyze what real drivers do!")
    print("\nFor the full IOCTL analysis experience, run:")
    print("  python ioctl_demo.py")


if __name__ == "__main__":
    main()
