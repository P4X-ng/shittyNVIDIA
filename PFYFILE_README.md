# shittyNVIDIA Task Files

Welcome to the shittyNVIDIA task runner files! These .pf (Pfyfile) task definitions help you experience the full glory of the worst NVIDIA driver ever created.

## What are .pf files?

These are task runner configuration files that use the `pf-runner` syntax. They define various tasks that you can execute to experience the complete failure of shittyNVIDIA.

## Requirements

To run these tasks, you'll need:
- `pf-runner` (from https://github.com/HyperionGray/pf-runner)
- A sense of humor
- Low expectations (they will still be disappointed)

## Installation

```bash
# Install pf-runner (if you dare)
git clone https://github.com/HyperionGray/pf-runner
cd pf-runner
./install.sh

# Or just read the tasks for entertainment value
```

## Available Task Files

### Pfyfile.pf
Main task file with core shittyNVIDIA operations:
- `check-nvidia` - Check for NVIDIA devices (spoiler: won't find any)
- `install-shitty-driver` - Install the driver (fails successfully)
- `test-driver` - Test functionality (guarantees failure)
- `uninstall-driver` - Uninstall (the smart choice)

### Pfyfile.nvidia-fail.pf
NVIDIA-specific failure tasks:
- `nvidia-check-version` - Get nonsensical version info
- `nvidia-list-gpus` - List nonexistent GPUs
- `nvidia-stress-test` - Crash immediately
- `nvidia-benchmark` - Score: FAIL/10
- `nvidia-cuda-test` - CUDA? Never heard of it
- `nvidia-power-management` - Break physics
- `nvidia-display-config` - Make your monitor sad

### Pfyfile.driver-chaos.pf
Driver chaos and mayhem:
- `driver-load-failure` - Kernel module loading fails
- `driver-kernel-panic` - Simulate kernel panic (safely)
- `driver-memory-leak` - Leak all the memory
- `driver-random-crash` - Crash at random times
- `driver-conflict-resolution` - Create more conflicts
- `driver-log-spam` - Fill logs with garbage
- `driver-temperature-sensor` - Impossible temperatures
- `driver-zombie-process` - Create unkillable processes

### Pfyfile.gpu-disaster.pf
GPU-specific disasters:
- `gpu-compute-fail` - CUDA compute? More like CUDA can't
- `gpu-graphics-test` - OpenGL 0.0
- `gpu-multi-gpu-disaster` - Multiple GPUs, multiple failures
- `gpu-machine-learning-fail` - ML? More like ML can't
- `gpu-ray-tracing` - 0 rays per second
- `gpu-video-encoding` - Encode to static
- `gpu-mining-attempt` - Mine negative coins
- `gpu-virtual-reality` - VR without the R
- `gpu-overclocking-disaster` - Quantum GPU state
- `gpu-monitoring-lies` - Metrics from another dimension

## Usage Examples

```bash
# Run a single task
pf check-nvidia

# Run NVIDIA failure demonstrations
pf nvidia-check-version
pf nvidia-cuda-test

# Experience the chaos
pf driver-kernel-panic
pf driver-random-crash

# Test GPU disasters
pf gpu-compute-fail
pf gpu-monitoring-lies
```

## How it Works (or Doesn't)

Each task in these files is carefully crafted to demonstrate different ways shittyNVIDIA fails:

1. **Realistic failures**: Like actual NVIDIA driver problems, but worse
2. **Impossible scenarios**: Physics-defying bugs for your entertainment
3. **Maximum frustration**: Everything fails, always
4. **Zero functionality**: Works with exactly 0 NVIDIA devices

## Troubleshooting

**Q: The tasks don't actually do anything destructive?**  
A: Correct! These are satirical scripts that just print messages. They won't harm your system.

**Q: Can I use this with real NVIDIA drivers?**  
A: You can, but why would you want to? The real drivers already provide plenty of frustration.

**Q: Will this work on my system?**  
A: Yes! shittyNVIDIA works perfectly by not working at all. It's consistent across all platforms.

**Q: Can I contribute more failure scenarios?**  
A: Absolutely! Add more .pf files with creative ways for things to fail.

## Contributing

Want to make shittyNVIDIA even worse? Great! Add more tasks that:
- Fail in creative ways
- Mock common NVIDIA driver problems
- Demonstrate theoretical impossibilities
- Generate entertaining error messages

## License

This satirical driver and its task files are provided "AS IS" without any warranty, expressed or implied, because nothing works anyway.

## See Also

- [README.md](README.md) - Main shittyNVIDIA documentation
- [pf-runner](https://github.com/HyperionGray/pf-runner) - The task runner engine
- Your actual NVIDIA drivers - For when you want real problems

---

**Remember**: shittyNVIDIA is a joke. For actual NVIDIA driver support, please use official NVIDIA drivers (which sometimes feel like jokes, but aren't).
