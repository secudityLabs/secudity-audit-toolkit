"""
Secudity Markdown Report Generator
Generates professional audit reports in Markdown format
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime
from typing import List
from scanner.vulnerability_detector import Vulnerability, Severity
from scanner.gas_analyzer import GasOptimization


class MarkdownReportGenerator:
    """Generates comprehensive audit reports in Markdown"""
    
    def __init__(self, contract_path: str, contract_name: str):
        self.contract_path = contract_path
        self.contract_name = contract_name
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_report(
        self,
        vulnerabilities: List[Vulnerability],
        gas_optimizations: List[GasOptimization]
    ) -> str:
        """Generate complete audit report"""
        
        report = []
        
        # Header
        report.append(self._generate_header())
        
        # Executive Summary
        report.append(self._generate_executive_summary(vulnerabilities, gas_optimizations))
        
        # Vulnerability Findings
        report.append(self._generate_vulnerability_section(vulnerabilities))
        
        # Gas Optimization Findings
        report.append(self._generate_gas_section(gas_optimizations))
        
        # Recommendations
        report.append(self._generate_recommendations(vulnerabilities))
        
        # Footer
        report.append(self._generate_footer())
        
        return '\n\n'.join(report)
    
    def _generate_header(self) -> str:
        """Generate report header"""
        return f"""# 🔐 Smart Contract Security Audit Report

**Contract:** `{self.contract_name}`  
**File:** `{self.contract_path}`  
**Audit Date:** {self.timestamp}  
**Auditor:** Secudity Team  
**Tool:** Secudity Audit Toolkit v1.0.0

---

![Secudity](https://img.shields.io/badge/Secudity-Security%20%2B%20Solidity-blue)
![Status](https://img.shields.io/badge/Status-Completed-green)

**Secudity** - Where Security meets Solidity  
Instagram: [@secudity](https://instagram.com/secudity)"""
    
    def _generate_executive_summary(
        self,
        vulnerabilities: List[Vulnerability],
        gas_optimizations: List[GasOptimization]
    ) -> str:
        """Generate executive summary"""
        
        # Count by severity
        critical = sum(1 for v in vulnerabilities if v.severity == Severity.CRITICAL)
        high = sum(1 for v in vulnerabilities if v.severity == Severity.HIGH)
        medium = sum(1 for v in vulnerabilities if v.severity == Severity.MEDIUM)
        low = sum(1 for v in vulnerabilities if v.severity == Severity.LOW)
        info = sum(1 for v in vulnerabilities if v.severity == Severity.INFORMATIONAL)
        
        # Determine overall risk
        if critical > 0:
            risk_level = "🔴 **CRITICAL RISK**"
            recommendation = "**NOT RECOMMENDED** for production deployment"
        elif high > 0:
            risk_level = "🟠 **HIGH RISK**"
            recommendation = "Requires immediate attention before deployment"
        elif medium > 0:
            risk_level = "🟡 **MEDIUM RISK**"
            recommendation = "Address issues before production deployment"
        elif low > 0:
            risk_level = "🟢 **LOW RISK**"
            recommendation = "Minor improvements recommended"
        else:
            risk_level = "✅ **MINIMAL RISK**"
            recommendation = "Contract appears secure"
        
        return f"""## 📊 Executive Summary

### Overall Risk Assessment
{risk_level}

**Deployment Recommendation:** {recommendation}

### Findings Overview

| Severity | Count |
|----------|-------|
| 🔴 Critical | {critical} |
| 🟠 High | {high} |
| 🟡 Medium | {medium} |
| 🔵 Low | {low} |
| ℹ️ Informational | {info} |
| **Total Vulnerabilities** | **{len(vulnerabilities)}** |
| ⚡ Gas Optimizations | {len(gas_optimizations)} |

### Key Concerns

{self._generate_key_concerns(vulnerabilities)}

---"""
    
    def _generate_key_concerns(self, vulnerabilities: List[Vulnerability]) -> str:
        """Generate key concerns section"""
        critical_and_high = [v for v in vulnerabilities 
                            if v.severity in [Severity.CRITICAL, Severity.HIGH]]
        
        if not critical_and_high:
            return "✅ No critical or high severity issues found."
        
        concerns = []
        for vuln in critical_and_high[:5]:  # Top 5
            concerns.append(f"- **{vuln.name}** (Line {vuln.line_number}): {vuln.description}")
        
        return '\n'.join(concerns)
    
    def _generate_vulnerability_section(self, vulnerabilities: List[Vulnerability]) -> str:
        """Generate detailed vulnerability findings"""
        
        if not vulnerabilities:
            return """## 🛡️ Security Findings

### ✅ No Vulnerabilities Detected

The automated scan did not detect any security vulnerabilities. However, manual review is always recommended for production contracts.

---"""
        
        sections = ["""## 🛡️ Security Findings

### Detailed Vulnerability Analysis

The following security issues were identified during the automated scan:

---"""]
        
        # Group by severity
        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, 
                        Severity.LOW, Severity.INFORMATIONAL]:
            severity_vulns = [v for v in vulnerabilities if v.severity == severity]
            
            if severity_vulns:
                sections.append(self._generate_severity_section(severity, severity_vulns))
        
        return '\n\n'.join(sections)
    
    def _generate_severity_section(
        self,
        severity: Severity,
        vulnerabilities: List[Vulnerability]
    ) -> str:
        """Generate section for specific severity level"""
        
        icons = {
            Severity.CRITICAL: "🔴",
            Severity.HIGH: "🟠",
            Severity.MEDIUM: "🟡",
            Severity.LOW: "🔵",
            Severity.INFORMATIONAL: "ℹ️"
        }
        
        icon = icons.get(severity, "")
        section = [f"### {icon} {severity.value} Severity Issues ({len(vulnerabilities)})"]
        
        for i, vuln in enumerate(vulnerabilities, 1):
            section.append(f"""
#### {i}. {vuln.name}

**Location:** `{vuln.location}:{vuln.line_number}`

**Description:**  
{vuln.description}

**Code Snippet:**
```solidity
{vuln.code_snippet}
```

**Recommendation:**  
{vuln.recommendation}

{f'**Reference:** [{vuln.reference}]({vuln.reference})' if vuln.reference else ''}

---""")
        
        return '\n'.join(section)
    
    def _generate_gas_section(self, optimizations: List[GasOptimization]) -> str:
        """Generate gas optimization section"""
        
        if not optimizations:
            return """## ⚡ Gas Optimization

### ✅ No Major Gas Optimizations Found

The contract appears to follow gas-efficient patterns. However, there may still be minor optimizations possible through manual review.

---"""
        
        section = [f"""## ⚡ Gas Optimization Opportunities

Found **{len(optimizations)}** opportunities to reduce gas costs:

---"""]
        
        # Group by category
        categories = {}
        for opt in optimizations:
            if opt.category not in categories:
                categories[opt.category] = []
            categories[opt.category].append(opt)
        
        for category, opts in categories.items():
            section.append(f"### {category} ({len(opts)} issues)\n")
            
            for i, opt in enumerate(opts, 1):
                section.append(f"""
#### {i}. Line {opt.line_number}: {opt.description}

**Code:**
```solidity
{opt.code_snippet}
```

**Suggestion:**  
{opt.suggestion}

**Estimated Gas Savings:** {opt.estimated_savings}

---""")
        
        return '\n'.join(section)
    
    def _generate_recommendations(self, vulnerabilities: List[Vulnerability]) -> str:
        """Generate recommendations section"""
        
        return f"""## 📋 Recommendations

### Immediate Actions Required

{self._generate_immediate_actions(vulnerabilities)}

### Best Practices

1. **Security Audits**
   - Conduct manual security review
   - Consider professional third-party audit
   - Implement bug bounty program

2. **Testing**
   - Write comprehensive unit tests
   - Implement fuzz testing
   - Test on testnet before mainnet

3. **Monitoring**
   - Set up transaction monitoring
   - Implement pause mechanisms for emergencies
   - Monitor for unusual activity

4. **Documentation**
   - Document all functions with NatSpec
   - Create detailed README
   - Maintain changelog

### Security Resources

- [Smart Contract Security Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [OpenZeppelin Security](https://docs.openzeppelin.com/contracts/4.x/security)
- [SWC Registry](https://swcregistry.io/)

---"""
    
    def _generate_immediate_actions(self, vulnerabilities: List[Vulnerability]) -> str:
        """Generate immediate action items"""
        critical_high = [v for v in vulnerabilities 
                        if v.severity in [Severity.CRITICAL, Severity.HIGH]]
        
        if not critical_high:
            return "✅ No critical issues requiring immediate action."
        
        actions = []
        for i, vuln in enumerate(critical_high, 1):
            actions.append(f"{i}. **Fix {vuln.name}** (Line {vuln.line_number}) - {vuln.recommendation}")
        
        return '\n'.join(actions)
    
    def _generate_footer(self) -> str:
        """Generate report footer"""
        return f"""## 📝 Disclaimer

This automated audit report is generated by **Secudity Audit Toolkit** and should be used as a supplementary tool. It does not replace professional manual security audits.

### Limitations

- Automated tools may produce false positives
- Complex vulnerabilities may not be detected
- Business logic issues require manual review
- Social engineering attacks are not covered

### Next Steps

1. Review all findings in this report
2. Fix critical and high severity issues
3. Conduct manual code review
4. Consider professional security audit
5. Test thoroughly on testnet

---

**Report Generated:** {self.timestamp}  
**Tool Version:** Secudity Audit Toolkit v1.0.0  
**Contact:** [Instagram @secudity](https://instagram.com/secudity)

---

*Secudity - Where Security meets Solidity* 🔐"""


def generate_markdown_report(
    contract_path: str,
    vulnerabilities: List[Vulnerability],
    gas_optimizations: List[GasOptimization],
    output_path: str
) -> str:
    """
    Generate and save markdown report
    
    Args:
        contract_path: Path to analyzed contract
        vulnerabilities: List of detected vulnerabilities
        gas_optimizations: List of gas optimizations
        output_path: Where to save the report
        
    Returns:
        Path to generated report
    """
    import os
    
    contract_name = os.path.basename(contract_path).replace('.sol', '')
    generator = MarkdownReportGenerator(contract_path, contract_name)
    
    report = generator.generate_report(vulnerabilities, gas_optimizations)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return output_path
