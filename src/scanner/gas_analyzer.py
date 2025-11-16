"""
Secudity Gas Analyzer
Identifies gas optimization opportunities in Solidity contracts
"""

import re
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class GasOptimization:
    """Data class for gas optimization suggestions"""
    category: str
    description: str
    location: str
    line_number: int
    code_snippet: str
    suggestion: str
    estimated_savings: str


class GasAnalyzer:
    """Analyzes contracts for gas optimization opportunities"""
    
    def __init__(self, contract_code: str, contract_path: str):
        self.contract_code = contract_code
        self.contract_path = contract_path
        self.lines = contract_code.split('\n')
        self.optimizations: List[GasOptimization] = []
    
    def analyze_all(self) -> List[GasOptimization]:
        """Run all gas optimization checks"""
        self.check_storage_vs_memory()
        self.check_state_variable_packing()
        self.check_loop_optimizations()
        self.check_require_vs_custom_errors()
        self.check_unnecessary_variables()
        self.check_public_vs_external()
        self.check_constant_immutable()
        self.check_short_circuit_evaluation()
        
        return self.optimizations
    
    def check_storage_vs_memory(self):
        """Check for inefficient storage reads in loops"""
        in_loop = False
        loop_start = 0
        
        for i, line in enumerate(self.lines):
            if 'for' in line and '(' in line:
                in_loop = True
                loop_start = i
            elif in_loop and '}' in line:
                in_loop = False
            elif in_loop and ('[' in line and ']' in line):
                # Check if reading from storage mapping/array in loop
                if 'balances[' in line or 'users[' in line or 'items[' in line:
                    self.optimizations.append(GasOptimization(
                        category="Storage Access",
                        description="Storage variable accessed inside loop",
                        location=self.contract_path,
                        line_number=i + 1,
                        code_snippet=self._get_code_snippet(i, 2),
                        suggestion="Cache storage values in memory before the loop to save gas. "
                                  "Each storage read costs ~2100 gas.",
                        estimated_savings="~2100 gas per iteration"
                    ))
    
    def check_state_variable_packing(self):
        """Check for inefficient state variable packing"""
        # Look for state variable declarations
        state_vars = []
        
        for i, line in enumerate(self.lines):
            # Simple state variable detection
            if (('uint256' in line or 'address' in line or 'bool' in line) and 
                'public' in line and 
                not 'function' in line and
                not 'return' in line):
                state_vars.append((i, line))
        
        # Check if smaller types could be packed
        if len(state_vars) > 1:
            has_uint256 = any('uint256' in var[1] for var in state_vars)
            has_smaller_types = any(('bool' in var[1] or 'uint8' in var[1] or 
                                     'uint16' in var[1] or 'uint32' in var[1]) 
                                    for var in state_vars)
            
            if has_uint256 and has_smaller_types:
                self.optimizations.append(GasOptimization(
                    category="Storage Packing",
                    description="State variables could be packed more efficiently",
                    location=self.contract_path,
                    line_number=state_vars[0][0] + 1,
                    code_snippet="Multiple state variable declarations",
                    suggestion="Group smaller types (bool, uint8, uint16, etc.) together. "
                              "Multiple variables fitting in 32 bytes share one storage slot.",
                    estimated_savings="~20,000 gas per saved storage slot"
                ))
    
    def check_loop_optimizations(self):
        """Check for loop optimization opportunities"""
        for i, line in enumerate(self.lines):
            # Check for .length in loop condition
            if 'for' in line and '.length' in line:
                self.optimizations.append(GasOptimization(
                    category="Loop Optimization",
                    description="Array length read in every loop iteration",
                    location=self.contract_path,
                    line_number=i + 1,
                    code_snippet=self._get_code_snippet(i, 2),
                    suggestion="Cache array length in a local variable before the loop: "
                              "uint256 len = array.length; for(uint256 i=0; i<len; i++)",
                    estimated_savings="~3 gas per iteration"
                ))
            
            # Check for i++ vs ++i
            if 'for' in line and 'i++' in line:
                self.optimizations.append(GasOptimization(
                    category="Loop Optimization",
                    description="Post-increment (i++) is less gas efficient than pre-increment",
                    location=self.contract_path,
                    line_number=i + 1,
                    code_snippet=self._get_code_snippet(i, 2),
                    suggestion="Use ++i instead of i++ in loops to save gas",
                    estimated_savings="~5 gas per iteration"
                ))
    
    def check_require_vs_custom_errors(self):
        """Check for require statements with string messages"""
        for i, line in enumerate(self.lines):
            if 'require(' in line and '"' in line:
                # Has a string error message
                self.optimizations.append(GasOptimization(
                    category="Error Handling",
                    description="require() with string message is gas inefficient",
                    location=self.contract_path,
                    line_number=i + 1,
                    code_snippet=self._get_code_snippet(i, 1),
                    suggestion="Use custom errors instead of require with string messages. "
                              "Custom errors are significantly cheaper.",
                    estimated_savings="~50 gas"
                ))
    
    def check_unnecessary_variables(self):
        """Check for unnecessary variable assignments"""
        for i, line in enumerate(self.lines):
            # Look for variables that are assigned but used only once
            if 'uint256' in line and '=' in line and not 'function' in line:
                var_match = re.search(r'uint256\s+(\w+)\s*=', line)
                if var_match:
                    var_name = var_match.group(1)
                    # Check if variable is used only in return statement
                    if i + 1 < len(self.lines) and f'return {var_name}' in self.lines[i + 1]:
                        self.optimizations.append(GasOptimization(
                            category="Unnecessary Variable",
                            description=f"Variable '{var_name}' is used only once",
                            location=self.contract_path,
                            line_number=i + 1,
                            code_snippet=self._get_code_snippet(i, 2),
                            suggestion="Return the value directly without storing in a variable",
                            estimated_savings="~3 gas"
                        ))
    
    def check_public_vs_external(self):
        """Check for public functions that could be external"""
        for i, line in enumerate(self.lines):
            if 'function' in line and 'public' in line and not 'constructor' in line:
                # Check if function is called internally
                func_name = self._extract_function_name(line)
                
                # Simple heuristic: if not called with 'this.', could be external
                internal_call = False
                for other_line in self.lines:
                    if f'{func_name}(' in other_line and 'function' not in other_line:
                        if 'this.' not in other_line:
                            internal_call = True
                            break
                
                if not internal_call:
                    self.optimizations.append(GasOptimization(
                        category="Function Visibility",
                        description=f"Function '{func_name}' could be external instead of public",
                        location=self.contract_path,
                        line_number=i + 1,
                        code_snippet=self._get_code_snippet(i, 1),
                        suggestion="Use 'external' instead of 'public' if function is not "
                                  "called internally. External is cheaper for calldata.",
                        estimated_savings="~200-2000 gas depending on parameters"
                    ))
    
    def check_constant_immutable(self):
        """Check for variables that could be constant or immutable"""
        for i, line in enumerate(self.lines):
            # Look for state variables that are set only in constructor
            if (('uint256' in line or 'address' in line) and 
                'public' in line and 
                not 'constant' in line and 
                not 'immutable' in line and
                '=' in line):
                
                var_match = re.search(r'(uint256|address)\s+public\s+(\w+)', line)
                if var_match:
                    var_name = var_match.group(2)
                    
                    # Check if variable is modified anywhere
                    is_modified = False
                    for other_line in self.lines:
                        if f'{var_name} =' in other_line and 'public' not in other_line:
                            is_modified = True
                            break
                    
                    if not is_modified:
                        self.optimizations.append(GasOptimization(
                            category="State Variable",
                            description=f"Variable '{var_name}' could be constant or immutable",
                            location=self.contract_path,
                            line_number=i + 1,
                            code_snippet=self._get_code_snippet(i, 1),
                            suggestion="Use 'constant' for compile-time constants or 'immutable' "
                                      "for constructor-set values. Saves gas on every read.",
                            estimated_savings="~2100 gas per read operation"
                        ))
    
    def check_short_circuit_evaluation(self):
        """Check for inefficient boolean expressions"""
        for i, line in enumerate(self.lines):
            if ('require(' in line or 'if' in line) and '&&' in line:
                # Check order of conditions (cheaper first)
                if 'msg.sender' in line.split('&&')[1]:
                    self.optimizations.append(GasOptimization(
                        category="Short-Circuit Evaluation",
                        description="Expensive check before cheaper check",
                        location=self.contract_path,
                        line_number=i + 1,
                        code_snippet=self._get_code_snippet(i, 1),
                        suggestion="Place cheaper conditions first in boolean expressions. "
                                  "If first condition fails, second won't be evaluated.",
                        estimated_savings="Variable savings"
                    ))
    
    def _extract_function_name(self, line: str) -> str:
        """Extract function name from function declaration"""
        match = re.search(r'function\s+(\w+)', line)
        return match.group(1) if match else ""
    
    def _get_code_snippet(self, line_index: int, context: int = 2) -> str:
        """Get code snippet around the specified line"""
        start = max(0, line_index - context)
        end = min(len(self.lines), line_index + context + 1)
        
        snippet_lines = []
        for i in range(start, end):
            marker = ">>> " if i == line_index else "    "
            snippet_lines.append(f"{marker}{i + 1}: {self.lines[i]}")
        
        return '\n'.join(snippet_lines)


def analyze_gas(contract_path: str) -> List[GasOptimization]:
    """
    Analyze a Solidity contract for gas optimizations
    
    Args:
        contract_path: Path to the Solidity contract file
        
    Returns:
        List of gas optimization suggestions
    """
    with open(contract_path, 'r', encoding='utf-8') as f:
        contract_code = f.read()
    
    analyzer = GasAnalyzer(contract_code, contract_path)
    return analyzer.analyze_all()


if __name__ == "__main__":
    # Test the gas analyzer
    optimizations = analyze_gas("tests/test_contracts/VulnerableContract.sol")
    
    print(f"\n⚡ Secudity Gas Optimization Report\n")
    print(f"Found {len(optimizations)} optimization opportunities:\n")
    
    for opt in optimizations:
        print(f"[{opt.category}] Line {opt.line_number}")
        print(f"  Issue: {opt.description}")
        print(f"  Suggestion: {opt.suggestion}")
        print(f"  Estimated Savings: {opt.estimated_savings}\n")
