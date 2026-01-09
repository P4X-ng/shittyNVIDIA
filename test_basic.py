#!/usr/bin/env python3
"""
Basic test of shittyNVIDIA functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import shitty_nvidia
    print("✅ shittyNVIDIA imported successfully!")
    
    # Test basic functionality
    print(f"Version: {shitty_nvidia.__version__}")
    print(f"Device count: {shitty_nvidia.get_device_count()}")
    print(f"CUDA available: {shitty_nvidia.cuda_available()}")
    
    # Test analysis availability
    summary = shitty_nvidia.get_analysis_summary()
    print(f"Analysis available: {summary['available']}")
    
    if summary['available']:
        print("✅ Analysis features working!")
        analysis = shitty_nvidia.analyze_nvidia_ioctls()
        if 'error' not in analysis:
            print(f"Total IOCTLs analyzed: {analysis['total_ioctls']}")
        else:
            print(f"Analysis error: {analysis['error']}")
    else:
        print(f"Analysis not available: {summary['reason']}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()