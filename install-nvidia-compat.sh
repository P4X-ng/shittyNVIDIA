#!/bin/bash
set -e

# shittyNVIDIA Installation Script
# The worst NVIDIA driver ever - works with 0 nvidia devices
# Based on nvidia-compat logic from HyperionGray/pf-web-poly-compile-helper-runner

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_nvidia_not_present() {
    log_info "Checking that NVIDIA GPU is NOT present (as required)..."
    
    if command -v nvidia-smi &> /dev/null; then
        log_error "ERROR: nvidia-smi found! This driver only works with 0 NVIDIA devices!"
        log_error "Please remove all NVIDIA hardware and drivers before proceeding."
        exit 1
    fi
    
    if lspci | grep -i nvidia &> /dev/null; then
        log_error "ERROR: NVIDIA hardware detected! This is shittyNVIDIA!"
        log_error "We pride ourselves on being incompatible with ALL NVIDIA devices."
        exit 1
    fi
    
    log_success "Confirmed: No NVIDIA devices found. Perfect!"
}

install_kernel_module() {
    log_info "Installing nvidia_compat kernel module..."
    
    # Check if kernel headers are installed
    if [ ! -d "/lib/modules/$(uname -r)/build" ]; then
        log_warning "Kernel headers not found. Skipping kernel module installation."
        log_warning "To install kernel headers: sudo apt-get install linux-headers-\$(uname -r)"
        return 0
    fi
    
    # Build the kernel module if needed
    if [ -d "nvidia_compat_module" ]; then
        log_info "Building nvidia_compat kernel module..."
        (cd nvidia_compat_module && make) || {
            log_warning "Failed to build kernel module. Continuing without it."
            return 0
        }
        
        # Install the module
        log_info "Installing nvidia_compat.ko..."
        sudo cp nvidia_compat_module/nvidia_compat.ko /lib/modules/$(uname -r)/extra/ || {
            sudo mkdir -p /lib/modules/$(uname -r)/extra/
            sudo cp nvidia_compat_module/nvidia_compat.ko /lib/modules/$(uname -r)/extra/
        }
        
        # Update module dependencies
        sudo depmod -A
        
        # Create module load configuration
        echo "nvidia_compat" | sudo tee /etc/modules-load.d/nvidia_compat.conf > /dev/null
        
        # Set module parameters
        cat << 'EOF' | sudo tee /etc/modprobe.d/nvidia_compat.conf > /dev/null
# nvidia_compat module configuration
options nvidia_compat enable_fake_gpu=1 fake_gpu_name="GeForce_RTX_4090_(Fake)" fake_gpu_memory=24576
EOF
        
        # Try to load the module
        if sudo modprobe nvidia_compat 2>/dev/null; then
            log_success "Kernel module loaded successfully!"
            if [ -e /dev/nvidia1337 ]; then
                log_success "Device /dev/nvidia1337 created!"
            fi
        else
            log_warning "Could not load kernel module. You may need to load it manually with: sudo modprobe nvidia_compat"
        fi
    else
        log_warning "nvidia_compat_module directory not found. Skipping kernel module installation."
    fi
}

install_shitty_nvidia() {
    log_info "Installing shittyNVIDIA - The worst NVIDIA driver ever..."
    
    # Create fake nvidia directory structure
    log_info "Creating fake NVIDIA directory structure..."
    sudo mkdir -p /usr/local/shittyNVIDIA/compat
    sudo mkdir -p /usr/local/shittyNVIDIA/bin
    sudo mkdir -p /usr/local/shittyNVIDIA/lib64
    
    # Create stub nvidia-smi that always fails
    log_info "Installing stub nvidia-smi..."
    cat << 'EOF' | sudo tee /usr/local/shittyNVIDIA/bin/nvidia-smi > /dev/null
#!/bin/bash
echo "shittyNVIDIA v0.0.0"
echo "The worst NVIDIA driver ever - works with 0 nvidia devices"
echo ""
echo "ERROR: No NVIDIA devices found (as designed!)"
echo ""
echo "This is shittyNVIDIA. We don't support ANY NVIDIA hardware."
echo "If you have NVIDIA hardware, please use a real driver."
exit 1
EOF
    sudo chmod +x /usr/local/shittyNVIDIA/bin/nvidia-smi
    
    # Create stub compatibility library
    log_info "Installing compatibility library stub..."
    cat << 'EOF' | sudo tee /usr/local/shittyNVIDIA/compat/README.txt > /dev/null
shittyNVIDIA Compatibility Library
===================================

This directory would contain NVIDIA compatibility libraries if we cared.
We don't. This driver works with exactly 0 NVIDIA devices.

For actual NVIDIA support, please install the real NVIDIA drivers from:
https://www.nvidia.com/Download/index.aspx

shittyNVIDIA - Because sometimes you need a driver that does nothing.
EOF
    
    # Create module blacklist
    log_info "Creating module blacklist to prevent real NVIDIA drivers..."
    cat << 'EOF' | sudo tee /etc/modprobe.d/shitty-nvidia-blacklist.conf > /dev/null
# shittyNVIDIA blacklist
# Blacklist all real NVIDIA kernel modules
blacklist nvidia
blacklist nvidia_drm
blacklist nvidia_modeset  
blacklist nvidia_uvm
blacklist nouveau

# This ensures no actual GPU functionality
EOF
    
    log_success "shittyNVIDIA installed successfully!"
}

configure_environment() {
    log_info "Configuring environment..."
    
    # Add to PATH
    if ! grep -q "/usr/local/shittyNVIDIA/bin" ~/.bashrc; then
        echo 'export PATH="/usr/local/shittyNVIDIA/bin:$PATH"' >> ~/.bashrc
        log_info "Added shittyNVIDIA to PATH in ~/.bashrc"
    fi
    
    # Add library path
    if ! grep -q "/usr/local/shittyNVIDIA/lib64" ~/.bashrc; then
        echo 'export LD_LIBRARY_PATH="/usr/local/shittyNVIDIA/lib64:$LD_LIBRARY_PATH"' >> ~/.bashrc
        log_info "Added shittyNVIDIA library path to ~/.bashrc"
    fi
    
    log_success "Environment configured"
}

test_installation() {
    log_info "Testing installation..."
    
    # Test that our stub nvidia-smi exists
    if [ -x /usr/local/shittyNVIDIA/bin/nvidia-smi ]; then
        log_success "Stub nvidia-smi installed correctly"
    else
        log_error "Stub nvidia-smi not found!"
        return 1
    fi
    
    # Run the stub and verify it fails (as it should)
    log_info "Running nvidia-smi (should fail)..."
    if /usr/local/shittyNVIDIA/bin/nvidia-smi; then
        log_error "ERROR: nvidia-smi succeeded! This shouldn't happen!"
        return 1
    else
        log_success "nvidia-smi failed as expected! Perfect!"
    fi
    
    log_success "All tests passed! shittyNVIDIA is working correctly."
}

show_usage() {
    cat << EOF
shittyNVIDIA Installation Script
The worst NVIDIA driver ever - works with 0 nvidia devices

Usage: $0 [install|uninstall|test|help]

Commands:
    install     Install shittyNVIDIA
    uninstall   Remove shittyNVIDIA
    test        Test the installation
    help        Show this help message

Requirements:
    - NO NVIDIA hardware (this is shittyNVIDIA!)
    - Root/sudo access
    - A sense of humor

EOF
}

uninstall_shitty_nvidia() {
    log_info "Uninstalling shittyNVIDIA..."
    
    # Unload kernel module if loaded
    if lsmod | grep -q nvidia_compat; then
        log_info "Unloading nvidia_compat kernel module..."
        sudo rmmod nvidia_compat 2>/dev/null || log_warning "Could not unload kernel module"
    fi
    
    # Remove kernel module files
    sudo rm -f /lib/modules/$(uname -r)/extra/nvidia_compat.ko
    sudo rm -f /etc/modules-load.d/nvidia_compat.conf
    sudo rm -f /etc/modprobe.d/nvidia_compat.conf
    sudo depmod -A
    
    sudo rm -rf /usr/local/shittyNVIDIA
    sudo rm -f /etc/modprobe.d/shitty-nvidia-blacklist.conf
    
    # Remove from bashrc - remove exact export statements
    if [ -f ~/.bashrc ]; then
        sed -i '\|export PATH="/usr/local/shittyNVIDIA/bin:$PATH"|d' ~/.bashrc
        sed -i '\|export LD_LIBRARY_PATH="/usr/local/shittyNVIDIA/lib64:$LD_LIBRARY_PATH"|d' ~/.bashrc
    fi
    
    log_success "shittyNVIDIA uninstalled"
}

main() {
    case "${1:-install}" in
        "install")
            log_info "Starting shittyNVIDIA installation..."
            check_nvidia_not_present
            install_shitty_nvidia
            install_kernel_module
            configure_environment
            test_installation
            echo ""
            log_success "shittyNVIDIA installation complete!"
            echo ""
            echo "The worst NVIDIA driver ever is now installed!"
            echo "Remember: This driver works with exactly 0 NVIDIA devices."
            echo ""
            echo "To use:"
            echo "  source ~/.bashrc"
            echo "  nvidia-smi  # Will fail spectacularly!"
            echo ""
            ;;
        "uninstall")
            uninstall_shitty_nvidia
            ;;
        "test")
            test_installation
            ;;
        "help"|"--help"|"-h")
            show_usage
            exit 0
            ;;
        *)
            log_error "Unknown command: $1"
            show_usage
            exit 1
            ;;
    esac
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
