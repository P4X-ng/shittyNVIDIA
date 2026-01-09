#!/bin/bash
# Demo script for nvidia_compat kernel module
# Shows how to build, load, and test the compatibility layer

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}    nvidia_compat.ko - NVIDIA Compatibility Layer${NC}"
echo -e "${BLUE}======================================================${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}Note: This demo needs root privileges to load kernel modules${NC}"
    echo -e "${YELLOW}Some operations will be skipped.${NC}"
    echo ""
fi

# Step 1: Build the module
echo -e "${GREEN}[1/6] Building the kernel module...${NC}"
cd nvidia_compat_module

if ! command -v make &> /dev/null; then
    echo -e "${RED}Error: make not found. Install with: sudo apt-get install build-essential${NC}"
    exit 1
fi

if [ ! -d "/lib/modules/$(uname -r)/build" ]; then
    echo -e "${RED}Error: Kernel headers not found.${NC}"
    echo -e "${YELLOW}Install with: sudo apt-get install linux-headers-\$(uname -r)${NC}"
    exit 1
fi

make clean > /dev/null 2>&1 || true
make

if [ ! -f nvidia_compat.ko ]; then
    echo -e "${RED}Error: Failed to build nvidia_compat.ko${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Module built successfully!${NC}"
echo ""

# Step 2: Show module info
echo -e "${GREEN}[2/6] Module information:${NC}"
modinfo nvidia_compat.ko | grep -E "^(filename|version|description|author|parm):"
echo ""

# Step 3: Load module (requires root)
if [ "$EUID" -eq 0 ]; then
    echo -e "${GREEN}[3/6] Loading the module with fake GPU enabled...${NC}"
    
    # Unload if already loaded
    if lsmod | grep -q nvidia_compat; then
        rmmod nvidia_compat || true
    fi
    
    # Load with fake GPU parameters
    insmod nvidia_compat.ko \
        enable_fake_gpu=1 \
        fake_gpu_name="GeForce_RTX_4090_Ti_SUPER" \
        fake_gpu_memory=32768
    
    echo -e "${GREEN}✓ Module loaded!${NC}"
    echo ""
    
    # Show loaded module
    echo -e "${GREEN}[4/6] Loaded module status:${NC}"
    lsmod | grep nvidia_compat
    echo ""
    
    # Check device
    echo -e "${GREEN}[5/6] Device node:${NC}"
    if [ -e /dev/nvidia1337 ]; then
        ls -la /dev/nvidia1337
        echo -e "${GREEN}✓ Device /dev/nvidia1337 created successfully!${NC}"
    else
        echo -e "${RED}✗ Device not found${NC}"
    fi
    echo ""
    
    # Show module parameters
    echo -e "${GREEN}Module parameters:${NC}"
    echo -n "  enable_fake_gpu: "
    cat /sys/module/nvidia_compat/parameters/enable_fake_gpu
    echo -n "  fake_gpu_name: "
    cat /sys/module/nvidia_compat/parameters/fake_gpu_name
    echo -n "  fake_gpu_memory: "
    cat /sys/module/nvidia_compat/parameters/fake_gpu_memory
    echo ""
    
    # Read from device
    echo -e "${GREEN}[6/6] Reading from device:${NC}"
    cat /dev/nvidia1337
    echo ""
    
    # Show kernel messages
    echo -e "${GREEN}Recent kernel messages:${NC}"
    dmesg | grep nvidia_compat | tail -10
    echo ""
    
else
    echo -e "${YELLOW}[3/6] Skipping module loading (requires root)${NC}"
    echo -e "${YELLOW}To load manually:${NC}"
    echo "  sudo insmod nvidia_compat.ko enable_fake_gpu=1 \\"
    echo "    fake_gpu_name=\"GeForce_RTX_4090\" \\"
    echo "    fake_gpu_memory=24576"
    echo ""
    
    echo -e "${YELLOW}[4/6] Skipping module status check (requires root)${NC}"
    echo ""
    
    echo -e "${YELLOW}[5/6] Skipping device check (requires root)${NC}"
    echo ""
    
    echo -e "${YELLOW}[6/6] Skipping device read (requires root)${NC}"
    echo ""
fi

# Test script
cd ..
echo -e "${GREEN}Running test script:${NC}"
echo ""

if [ "$EUID" -eq 0 ]; then
    python3 test_nvidia_compat.py
else
    python3 test_nvidia_compat.py || true
fi

echo ""
echo -e "${BLUE}======================================================${NC}"
echo -e "${GREEN}Demo complete!${NC}"
echo ""

if [ "$EUID" -eq 0 ]; then
    echo -e "${GREEN}The module is currently loaded.${NC}"
    echo ""
    echo "To unload: sudo rmmod nvidia_compat"
    echo "To reload: sudo modprobe nvidia_compat"
    echo ""
    echo -e "${YELLOW}Try interacting with /dev/nvidia1337:${NC}"
    echo "  cat /dev/nvidia1337"
    echo "  # Use nvidia-smi (if you have shittyNVIDIA's version)"
    echo ""
else
    echo -e "${YELLOW}Run this demo with sudo to see the module in action:${NC}"
    echo "  sudo ./nvidia_compat_demo.sh"
fi

echo -e "${BLUE}======================================================${NC}"
