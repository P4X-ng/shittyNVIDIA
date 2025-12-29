# Contributing to shittyNVIDIA

Thank you for your interest in making shittyNVIDIA even worse! 🎉

## Code of Conduct

Be nice. Remember, this is a parody project meant for humor and education.

## How Can I Contribute?

### Reporting Bugs

Found a bug? That's ironic, considering shittyNVIDIA is designed to not work. But if something's broken in an unexpected way:

1. Check if the issue already exists
2. If not, create a new issue with:
   - A clear title
   - Steps to reproduce
   - Expected behavior (or lack thereof)
   - Actual behavior
   - Your system information

### Suggesting Enhancements

Want to make shittyNVIDIA even more useless? Great! 

1. Open an issue describing your idea
2. Explain why this would make it worse/funnier
3. Discuss implementation details

### Pull Requests

#### Guidelines

1. **Keep it funny** - The humor is the point
2. **Keep it functional** - It should run without errors (even if it does nothing)
3. **Keep it documented** - Good documentation for bad software is hilarious
4. **Keep it tested** - All tests should pass

#### Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/even-worse-nvidia`)
3. Make your changes
4. Run the tests (`python3 test_shitty_nvidia.py`)
5. Update documentation as needed
6. Commit with a clear message
7. Push to your fork
8. Create a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/shittyNVIDIA.git
cd shittyNVIDIA

# Install in development mode
pip install -e .

# Run tests
python3 test_shitty_nvidia.py

# Run demo
python3 demo.py

# Run examples
python3 examples.py
```

## Style Guide

### Python Code

- Follow PEP 8
- Use type hints where appropriate
- Keep functions small and focused
- Comment the humor (but not too much)

### Documentation

- Be clear
- Be funny
- Be accurate (even about inaccuracy)
- Include examples

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Be descriptive
- Reference issues/PRs when relevant

Examples:
```
Add stub for CUDA compatibility check
Fix typo in README
Update demo script with new examples
```

## Testing

All code must pass existing tests. New features should include tests.

```bash
# Run all tests
python3 test_shitty_nvidia.py

# Run specific test
python3 -m unittest test_shitty_nvidia.TestShittyNVIDIA.test_device_count_is_zero
```

## What We're Looking For

### Good Contributions

- More creative ways to fail
- Better error messages
- Additional compatibility checks
- Improved documentation
- Bug fixes (the irony!)
- More tests

### Not So Good Contributions

- Actually working NVIDIA support
- Real GPU functionality
- Removing the humor
- Making it useful

## Questions?

Open an issue with the label `question` and we'll try to help!

## Attribution

Contributors will be recognized in the README (if they want to be associated with this project 😄).

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Remember: We're making the worst NVIDIA driver ever. Let's keep it that way! 🎯
