# 📖 Secudity Audit Toolkit - Usage Guide

Complete guide for using the Secudity Audit Toolkit for smart contract security analysis.

---

## Table of Contents

1. [Installation](#installation)
2. [Basic Commands](#basic-commands)
3. [Advanced Usage](#advanced-usage)
4. [Report Formats](#report-formats)
5. [Interpreting Results](#interpreting-results)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Installation

### Requirements

- Python 3.8 or higher
- pip package manager
- Solidity compiler (automatically installed)

### Step-by-Step Installation
```bash
# 1. Clone the repository
git clone https://github.com/secuditylabs/secudity-audit-toolkit.git
cd secudity-audit-toolkit

# 2. Create virtual environment (recommended)
python3 -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install the package
pip install -e .

# 6. Verify installation
python src/cli.py version
```

---

## Basic Commands

### Quick Scan

Fast security overview without generating full report:
```bash
python src/cli.py quick MyContract.sol
```

**Use when:**
- You want a quick security check
- Testing during development
- Don't need a formal report

### Full Scan

Complete analysis with detailed report generation:
```bash
python src/cli.py scan MyContract.sol
```

**Options:**
```bash
# Specify output directory
python src/cli.py scan MyContract.sol -o reports/

# Verbose mode (shows detailed findings)
python src/cli.py scan MyContract.sol --verbose

# Short form
python src/cli.py scan MyContract.sol -o reports/ -v
```

### Version Information

Display tool version and information:
```bash
python src/cli.py version
```

---

## Advanced Usage

### Scanning Multiple Contracts
```bash
# Loop through all contracts in a directory
for contract in contracts/*.sol; do
    python src/cli.py scan "$contract" -o "reports/"
done
```

### Custom Output Locations
```bash
# Organize by date
python src/cli.py scan MyContract.sol -o "reports/$(date +%Y-%m-%d)/"

# Organize by project
python src/cli.py scan MyContract.sol -o "audits/project-name/"
```

### Integration with CI/CD

Example GitHub Actions workflow:
```yaml
name: Security Audit

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install Secudity
        run: |
          pip install -r requirements.txt
          pip install -e .
      
      - name: Run Security Scan
        run: |
          python src/cli.py scan contracts/MyContract.sol -v
      
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: audit-report
          path: output/*.md
```

---

## Report Formats

### Markdown Reports

Default format, easy to read and version control:
```bash
python src/cli.py scan MyContract.sol
```

**Benefits:**
- Human-readable
- Git-friendly
- Can be converted to other formats
- Easy to share

### Report Contents

Every report includes:

1. **Header**
   - Contract information
   - Audit timestamp
   - Tool version

2. **Executive Summary**
   - Risk assessment
   - Findings count by severity
   - Key concerns

3. **Detailed Findings**
   - Vulnerability descriptions
   - Code snippets
   - Recommendations
   - References

4. **Gas Optimizations**
   - Inefficient patterns
   - Improvement suggestions
   - Estimated savings

5. **Recommendations**
   - Action items
   - Best practices
   - Resources

---

## Interpreting Results

### Severity Levels

#### 🔴 Critical
**Impact:** Can lead to loss of funds or complete compromise

**Examples:**
- Reentrancy vulnerabilities
- Missing access control on critical functions
- Delegatecall to untrusted contracts

**Action:** Fix immediately before deployment

#### 🟠 High
**Impact:** Significant security risk

**Examples:**
- Unchecked call return values
- tx.origin authentication
- Uninitialized storage pointers

**Action:** Must be fixed before production

#### 🟡 Medium
**Impact:** Moderate security concern

**Examples:**
- Timestamp dependence
- Locked ether
- Block gas limit issues

**Action:** Should be addressed

#### 🔵 Low
**Impact:** Minor security issue

**Examples:**
- Code quality issues
- Documentation gaps
- Minor optimizations

**Action:** Consider fixing

#### ℹ️ Informational
**Impact:** Best practice recommendations

**Examples:**
- Coding style
- Documentation suggestions
- Optional optimizations

**Action:** Optional improvements

### Gas Optimization Categories

- **Storage Access:** Optimize storage reads/writes
- **Loop Optimization:** Improve loop efficiency
- **Error Handling:** Use custom errors
- **Function Visibility:** Use external vs public
- **State Variables:** Use constant/immutable

---

## Best Practices

### Before Scanning

1. **Clean Code**
   - Ensure code compiles
   - Remove commented code
   - Update Solidity version

2. **Complete Implementation**
   - Finish core functionality
   - Add basic access control
   - Include all imports

3. **Organize Files**
   - Use clear file structure
   - Separate concerns
   - Document functions

### After Scanning

1. **Review All Findings**
   - Start with critical/high
   - Understand each issue
   - Plan fixes

2. **Fix Systematically**
   - Address by severity
   - Test after each fix
   - Re-scan to verify

3. **Document Changes**
   - Track fixes made
   - Update comments
   - Note remaining issues

### Regular Scanning
```bash
# Scan before each commit
git add MyContract.sol
python src/cli.py quick MyContract.sol
git commit -m "Update contract"

# Weekly full scan
python src/cli.py scan contracts/*.sol -o weekly-audits/
```

---

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# If you get import errors
pip install -e .

# Or add src to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

#### Solidity Compiler Not Found
```bash
# Install solc
solc-select install 0.8.24
solc-select use 0.8.24

# Verify
solc --version
```

#### Permission Denied
```bash
# Make CLI executable
chmod +x src/cli.py

# Or run with python
python src/cli.py scan MyContract.sol
```

#### Virtual Environment Issues
```bash
# Deactivate and recreate
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Getting Help
```bash
# Display help
python src/cli.py --help

# Command-specific help
python src/cli.py scan --help
python src/cli.py quick --help
```

---

## Tips & Tricks

### Faster Scanning
```bash
# Quick scan for rapid feedback
python src/cli.py quick MyContract.sol

# Full scan only when ready for review
python src/cli.py scan MyContract.sol -o final-audit/
```

### Comparing Versions
```bash
# Scan before changes
python src/cli.py scan MyContract.sol -o reports/before/

# Make changes...

# Scan after changes
python src/cli.py scan MyContract.sol -o reports/after/

# Compare reports
diff reports/before/*.md reports/after/*.md
```

### Batch Processing
```bash
# Scan all contracts in a project
find ./contracts -name "*.sol" -exec python src/cli.py scan {} -o batch-reports/ \;
```

---

## Next Steps

After scanning:

1. **Fix Issues** - Address findings systematically
2. **Manual Review** - Automated tools don't catch everything
3. **Testing** - Write comprehensive tests
4. **Professional Audit** - Consider third-party audit for production
5. **Testnet Deployment** - Test in real environment
6. **Monitoring** - Set up transaction monitoring

---

**Questions?** Contact Secudity on Instagram: [@secudity](https://instagram.com/secudity)
