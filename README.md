# 🔐 Secudity Audit Toolkit

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

**Automated Smart Contract Security Analysis & Report Generation**

> **Secudity** = Security + Solidity

Created by [Secudity](https://instagram.com/secudity) - Professional blockchain security and smart contract development services.

---

## 🌟 Features

- ✅ **Automated Vulnerability Detection** - Identifies 10+ common smart contract vulnerabilities
- ⚡ **Gas Optimization Analysis** - Finds opportunities to reduce gas costs
- 📊 **Professional Reports** - Generate detailed audit reports in Markdown/PDF
- 🎯 **Easy to Use** - Simple CLI interface with beautiful output
- 🔍 **Fast Scanning** - Analyze contracts in seconds
- 📝 **Detailed Recommendations** - Get actionable security advice

---

## 📋 Detected Vulnerabilities

The toolkit automatically detects:

1. **Reentrancy Attacks** - External calls before state updates
2. **Access Control Issues** - Missing authorization checks
3. **tx.origin Authentication** - Dangerous authentication patterns
4. **Unchecked Call Returns** - Silent failures in low-level calls
5. **Timestamp Dependence** - Reliance on block.timestamp
6. **Delegatecall Risks** - Unsafe delegatecall usage
7. **Selfdestruct** - Contract destruction vulnerabilities
8. **Locked Ether** - Funds that can't be withdrawn
9. **Integer Overflow** - Unchecked arithmetic operations
10. **Gas Optimizations** - Inefficient code patterns

---

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/secuditylabs/secudity-audit-toolkit.git
cd secudity-audit-toolkit

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Basic Usage
```bash
# Quick scan (summary only)
python src/cli.py quick MyContract.sol

# Full scan with detailed report
python src/cli.py scan MyContract.sol -o reports/

# Verbose output
python src/cli.py scan MyContract.sol -o reports/ --verbose

# Check version
python src/cli.py version
```

---

## 📖 Detailed Usage

### Scanning a Contract
```bash
# Scan a single contract
python src/cli.py scan contracts/MyToken.sol

# Specify output directory
python src/cli.py scan contracts/MyToken.sol -o audit-reports/

# Verbose mode for detailed output
python src/cli.py scan contracts/MyToken.sol -v
```

### Quick Scan

For a fast overview without generating a full report:
```bash
python src/cli.py quick contracts/MyContract.sol
```

### Output Example
```
🔍 Secudity Audit Toolkit
Security + Solidity

   🛡️  Security Findings Summary   
┏━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┓
┃ Severity      ┃ Count ┃ Status ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━┩
│ 🔴 Critical   │     5 │   🔴   │
│ 🟠 High       │     2 │   🔴   │
│ 🟡 Medium     │     1 │   🔴   │
│ 🔵 Low        │     0 │   ✅   │
│ ⚡ Gas Issues │    14 │   ℹ️    │
└───────────────┴───────┴────────┘

✅ Report saved to: output/MyContract_audit_20241116.md
```

---

## 📊 Report Structure

Generated reports include:

1. **Executive Summary**
   - Overall risk assessment
   - Findings overview table
   - Key security concerns

2. **Security Findings**
   - Detailed vulnerability descriptions
   - Code snippets
   - Severity classifications
   - Remediation recommendations
   - Reference links

3. **Gas Optimizations**
   - Inefficient patterns
   - Optimization suggestions
   - Estimated gas savings

4. **Recommendations**
   - Immediate action items
   - Best practices
   - Security resources

---

## 🔍 Example Vulnerabilities Detected

### Reentrancy
```solidity
// ❌ VULNERABLE
function withdraw(uint256 amount) public {
    require(balances[msg.sender] >= amount);
    msg.sender.call{value: amount}("");  // External call first
    balances[msg.sender] -= amount;      // State update after
}

// ✅ SECURE
function withdraw(uint256 amount) public {
    require(balances[msg.sender] >= amount);
    balances[msg.sender] -= amount;      // State update first
    msg.sender.call{value: amount}("");  // External call after
}
```

### Access Control
```solidity
// ❌ VULNERABLE - Anyone can call
function setOwner(address newOwner) public {
    owner = newOwner;
}

// ✅ SECURE - Protected by modifier
function setOwner(address newOwner) public onlyOwner {
    owner = newOwner;
}
```

---

## 🛠️ Project Structure
```
secudity-audit-toolkit/
├── src/
│   ├── scanner/
│   │   ├── vulnerability_detector.py  # Vulnerability detection engine
│   │   ├── gas_analyzer.py           # Gas optimization analyzer
│   │   └── static_analyzer.py        # Static analysis utilities
│   ├── reporter/
│   │   ├── markdown_generator.py     # Markdown report generator
│   │   ├── pdf_generator.py          # PDF report generator
│   │   └── checklist_generator.py    # Security checklist
│   ├── utils/
│   │   ├── contract_parser.py        # Contract parsing utilities
│   │   └── helpers.py                # Helper functions
│   └── cli.py                        # Command-line interface
├── tests/
│   ├── test_contracts/               # Example vulnerable contracts
│   └── unit_tests/                   # Unit tests
├── examples/
│   ├── reports/                      # Example audit reports
│   └── contracts/                    # Example contracts
├── docs/
│   ├── USAGE.md                      # Detailed usage guide
│   ├── VULNERABILITY_DATABASE.md     # Vulnerability documentation
│   └── EXAMPLES.md                   # Usage examples
├── output/                           # Generated reports (gitignored)
├── requirements.txt                  # Python dependencies
├── setup.py                          # Package setup
├── config.yaml                       # Configuration file
└── README.md                         # This file
```

---

## ⚙️ Configuration

Edit `config.yaml` to customize:
```yaml
scanner:
  enable_slither: true
  enable_custom_checks: true
  solc_version: "0.8.24"

report:
  format: "pdf"  # Options: pdf, markdown, html, all
  include_gas_analysis: true
  include_code_snippets: true

branding:
  logo: "docs/secudity-logo.png"
  website: "https://instagram.com/secudity"
  tagline: "Security + Solidity"
```

---

## 🧪 Testing
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Test on example contracts
python src/cli.py scan tests/test_contracts/ReentrancyExample.sol
python src/cli.py scan tests/test_contracts/AccessControlIssue.sol
python src/cli.py scan tests/test_contracts/VulnerableContract.sol
```

---

## 🎯 Use Cases

### For Smart Contract Developers

- Pre-deployment security checks
- Continuous security monitoring
- Learning security best practices
- Gas optimization

### For Security Auditors

- Initial automated analysis
- Report generation
- Vulnerability documentation
- Client deliverables

### For Educational Purposes

- Learning common vulnerabilities
- Understanding security patterns
- Practicing secure coding

---

## 📚 Resources

### Security Best Practices

- [Consensys Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [OpenZeppelin Security](https://docs.openzeppelin.com/contracts/4.x/security)
- [SWC Registry](https://swcregistry.io/)
- [Solidity Security Considerations](https://docs.soliditylang.org/en/latest/security-considerations.html)

### Tools & Frameworks

- [Slither](https://github.com/crytic/slither) - Static analyzer
- [Foundry](https://github.com/foundry-rs/foundry) - Development toolkit
- [Hardhat](https://hardhat.org/) - Development environment

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Instagram:** [@secudity](https://instagram.com/secudity)
- **GitHub:** [SecudityLabs](https://github.com/secuditylabs)
- **Portfolio:** [Secudity Website](https://secudity.com)

---

## 🙏 Acknowledgments

- Built with [Slither](https://github.com/crytic/slither) by Trail of Bits
- Inspired by professional security audit practices
- Security patterns from OpenZeppelin and Consensys

---

## 📞 Contact

For professional smart contract audits and development services, contact **Secudity**:

- Instagram: [@secudity](https://instagram.com/secudity)
- Email: secudity.mail@gmail.com

---

## ⚠️ Disclaimer

This tool is provided as-is for educational and informational purposes. Automated security analysis does not replace professional manual audits. Always conduct thorough testing and consider professional security audits before deploying smart contracts to production.

---

**Secudity** - Where Security meets Solidity 🔐

⭐ If you find this project useful, please consider giving it a star!
