# Makefile for nvidia_compat kernel module
# Part of shittyNVIDIA - The worst NVIDIA driver ever

obj-m += nvidia_compat.o

# Kernel build directory
KDIR ?= /lib/modules/$(shell uname -r)/build

# Module installation directory
INSTALL_MOD_DIR ?= extra

all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean

install: all
	$(MAKE) -C $(KDIR) M=$(PWD) INSTALL_MOD_DIR=$(INSTALL_MOD_DIR) modules_install
	depmod -A

uninstall:
	rm -f /lib/modules/$(shell uname -r)/$(INSTALL_MOD_DIR)/nvidia_compat.ko
	depmod -A

load:
	insmod nvidia_compat.ko enable_fake_gpu=1 fake_gpu_name="GeForce_RTX_4090_(Fake)" fake_gpu_memory=24576

unload:
	rmmod nvidia_compat

reload: unload load

test:
	@echo "Testing nvidia_compat module..."
	@if [ -e /dev/nvidia1337 ]; then \
		echo "✓ Device /dev/nvidia1337 exists"; \
		ls -la /dev/nvidia1337; \
	else \
		echo "✗ Device /dev/nvidia1337 not found"; \
	fi
	@echo ""
	@echo "Module info:"
	@modinfo nvidia_compat.ko 2>/dev/null || echo "Module not built yet"
	@echo ""
	@echo "Loaded status:"
	@lsmod | grep nvidia_compat || echo "Module not loaded"

help:
	@echo "NVIDIA Compat Module Build System"
	@echo ""
	@echo "Targets:"
	@echo "  all       - Build the kernel module"
	@echo "  clean     - Clean build artifacts"
	@echo "  install   - Install module to system"
	@echo "  uninstall - Remove module from system"
	@echo "  load      - Load module with default fake GPU"
	@echo "  unload    - Unload module"
	@echo "  reload    - Unload and reload module"
	@echo "  test      - Test if module is working"
	@echo "  help      - Show this help message"
	@echo ""
	@echo "Module parameters:"
	@echo "  enable_fake_gpu     - Enable fake GPU (1=yes, 0=no)"
	@echo "  fake_gpu_name       - Name of fake GPU"
	@echo "  fake_gpu_memory     - Fake GPU memory in MB"
	@echo ""
	@echo "Example:"
	@echo "  sudo insmod nvidia_compat.ko enable_fake_gpu=1 fake_gpu_name=\"RTX_4090\" fake_gpu_memory=24576"

.PHONY: all clean install uninstall load unload reload test help
