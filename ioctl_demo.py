#!/usr/bin/env python3
"""
IOCTL Analysis Demo for shittyNVIDIA

This script demonstrates the new IOCTL analysis capabilities
that analyze NVIDIA and AMD open source GPU drivers.

Because if we're going to be the worst NVIDIA driver ever,
we should at least understand what the good ones do!
"""

import sys
import json
from pathlib import Path

# Add the shitty_nvidia module to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import shitty_nvidia
    print("✅ shittyNVIDIA imported successfully!")
except ImportError as e:
    print(f"❌ Failed to import shittyNVIDIA: {e}")
    sys.exit(1)


def main():
    print("🎭 SHITTY NVIDIA IOCTL ANALYSIS DEMO")
    print("=" * 60)
    print()
    
    # Check if analysis is available
    info = shitty_nvidia.get_driver_info()
    print(f"📦 shittyNVIDIA v{info['version']}")
    print(f"📊 Analysis features available: {info.get('analysis_features', False)}")
    print()
    
    if not info.get('analysis_features', False):
        print("❌ Analysis features not available!")
        print("   This might be due to missing dependencies or import errors.")
        print("   The basic shittyNVIDIA functionality still works though!")
        return
    
    print("🔍 NVIDIA IOCTL ANALYSIS")
    print("-" * 40)
    
    # Analyze NVIDIA IOCTLs
    try:
        shitty_nvidia.print_ioctl_analysis()
    except Exception as e:
        print(f"❌ IOCTL analysis failed: {e}")
    
    print()
    print("🆚 GPU DRIVER COMPARISON")
    print("-" * 40)
    
    # Full comparison report
    try:
        shitty_nvidia.print_comparison_report()
    except Exception as e:
        print(f"❌ Comparison report failed: {e}")
        print("   Trying basic comparison...")
        
        try:
            comparison = shitty_nvidia.compare_gpu_drivers()
            if 'error' in comparison:
                print(f"❌ Comparison error: {comparison['error']}")
            else:
                print("📊 Basic comparison data available")
                print(f"   NVIDIA drivers analyzed: {len(comparison.get('nvidia_details', {}).get('drivers', {}))}")
                print(f"   AMD drivers analyzed: {len(comparison.get('amd_details', {}).get('drivers', {}))}")
        except Exception as e2:
            print(f"❌ Basic comparison also failed: {e2}")
    
    print()
    print("📈 ANALYSIS SUMMARY")
    print("-" * 40)
    
    try:
        summary = shitty_nvidia.get_analysis_summary()
        print(f"Available: {summary['available']}")
        if summary['available']:
            print("Features:")
            for feature in summary['features']:
                print(f"  • {feature}")
            print()
            print("Functions:")
            for func in summary['functions']:
                print(f"  • {func}")
            print()
            print(f"Total IOCTLs analyzed: {summary['total_ioctls_analyzed']}")
            print(f"shittyNVIDIA implements: {summary['shitty_nvidia_implements']} (perfect!)")
        else:
            print(f"Reason: {summary['reason']}")
    except Exception as e:
        print(f"❌ Summary failed: {e}")
    
    print()
    print("🎯 INTERACTIVE DEMO")
    print("-" * 40)
    print("Try these commands in a Python shell:")
    print()
    print("import shitty_nvidia")
    print()
    print("# Basic shittyNVIDIA functionality")
    print("shitty_nvidia.check_compatibility()")
    print("shitty_nvidia.get_device_count()")
    print("shitty_nvidia.get_driver_info()")
    print()
    print("# New IOCTL analysis features")
    print("shitty_nvidia.analyze_nvidia_ioctls()")
    print("shitty_nvidia.compare_gpu_drivers()")
    print("shitty_nvidia.print_ioctl_analysis()")
    print("shitty_nvidia.print_comparison_report()")
    print()
    print("# Analysis summary")
    print("shitty_nvidia.get_analysis_summary()")
    print()
    
    print("🎭 CONCLUSION")
    print("-" * 40)
    print("shittyNVIDIA now includes comprehensive analysis of:")
    print("  • NVIDIA open source drivers (nouveau, nvidia-open)")
    print("  • NVIDIA CUDA IOCTLs and runtime interface")
    print("  • AMD open source drivers (amdgpu, radeon)")
    print("  • GPU driver architecture comparison")
    print("  • Humorous technical commentary")
    print()
    print("We've analyzed 100+ IOCTLs from real GPU drivers,")
    print("so we can proudly continue to implement exactly 0 of them!")
    print()
    print("Remember: shittyNVIDIA works with 0 NVIDIA devices by design.")
    print("For actual GPU computing, please use real drivers.")
    print()
    print("🎉 Demo complete! Thanks for using shittyNVIDIA!")


if __name__ == "__main__":
    main()