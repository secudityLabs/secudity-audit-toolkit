"""
Secudity Audit Toolkit - Command Line Interface
"""

import click
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from scanner.vulnerability_detector import analyze_contract, Severity
from scanner.gas_analyzer import analyze_gas
from reporter.markdown_generator import generate_markdown_report

console = Console()


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    🔐 Secudity Audit Toolkit
    
    Automated Smart Contract Security Analysis & Report Generation
    
    Security + Solidity = Secudity
    """
    pass


@cli.command()
@click.argument('contract_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='output', help='Output directory for reports')
@click.option('--format', '-f', type=click.Choice(['markdown', 'pdf', 'all']), 
              default='markdown', help='Report format')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def scan(contract_path, output, format, verbose):
    """
    Scan a Solidity contract for vulnerabilities and generate report
    
    Example: secudity scan MyContract.sol -o reports/
    """
    
    console.print(Panel.fit(
        "[bold blue]🔍 Secudity Audit Toolkit[/bold blue]\n"
        "[dim]Security + Solidity[/dim]",
        border_style="blue"
    ))
    
    # Validate contract file
    if not contract_path.endswith('.sol'):
        console.print("[red]Error: File must be a Solidity contract (.sol)[/red]")
        return
    
    contract_name = os.path.basename(contract_path).replace('.sol', '')
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        # Scan for vulnerabilities
        task1 = progress.add_task("Scanning for vulnerabilities...", total=None)
        vulnerabilities = analyze_contract(contract_path)
        progress.update(task1, completed=True)
        
        # Analyze gas optimizations
        task2 = progress.add_task("Analyzing gas optimizations...", total=None)
        gas_optimizations = analyze_gas(contract_path)
        progress.update(task2, completed=True)
        
        # Generate report
        task3 = progress.add_task("Generating report...", total=None)
        os.makedirs(output, exist_ok=True)
        
        timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"{contract_name}_audit_{timestamp}.md"
        report_path = os.path.join(output, report_filename)
        
        generate_markdown_report(
            contract_path,
            vulnerabilities,
            gas_optimizations,
            report_path
        )
        progress.update(task3, completed=True)
    
    # Display results
    console.print("\n")
    display_results(vulnerabilities, gas_optimizations, verbose)
    
    console.print(f"\n✅ [green]Report saved to:[/green] [bold]{report_path}[/bold]")
    console.print(f"📊 [blue]Total Issues Found:[/blue] {len(vulnerabilities) + len(gas_optimizations)}\n")


def display_results(vulnerabilities, gas_optimizations, verbose=False):
    """Display scan results in a formatted table"""
    
    # Vulnerability summary
    critical = sum(1 for v in vulnerabilities if v.severity == Severity.CRITICAL)
    high = sum(1 for v in vulnerabilities if v.severity == Severity.HIGH)
    medium = sum(1 for v in vulnerabilities if v.severity == Severity.MEDIUM)
    low = sum(1 for v in vulnerabilities if v.severity == Severity.LOW)
    
    summary_table = Table(title="🛡️  Security Findings Summary", show_header=True, header_style="bold magenta")
    summary_table.add_column("Severity", style="dim")
    summary_table.add_column("Count", justify="right")
    summary_table.add_column("Status", justify="center")
    
    def get_status(count):
        return "🔴" if count > 0 else "✅"
    
    summary_table.add_row("🔴 Critical", str(critical), get_status(critical))
    summary_table.add_row("🟠 High", str(high), get_status(high))
    summary_table.add_row("🟡 Medium", str(medium), get_status(medium))
    summary_table.add_row("🔵 Low", str(low), get_status(low))
    summary_table.add_row("⚡ Gas Issues", str(len(gas_optimizations)), "ℹ️")
    
    console.print(summary_table)
    
    # Detailed findings if verbose
    if verbose and vulnerabilities:
        console.print("\n")
        findings_table = Table(title="Detailed Findings", show_header=True, header_style="bold cyan")
        findings_table.add_column("Line", style="dim", width=6)
        findings_table.add_column("Severity", width=10)
        findings_table.add_column("Issue", width=40)
        
        for vuln in vulnerabilities[:10]:  # Show top 10
            severity_color = {
                Severity.CRITICAL: "red",
                Severity.HIGH: "orange1",
                Severity.MEDIUM: "yellow",
                Severity.LOW: "blue",
                Severity.INFORMATIONAL: "white"
            }.get(vuln.severity, "white")
            
            findings_table.add_row(
                str(vuln.line_number),
                f"[{severity_color}]{vuln.severity.value}[/{severity_color}]",
                vuln.name
            )
        
        console.print(findings_table)


@cli.command()
@click.argument('contract_path', type=click.Path(exists=True))
def quick(contract_path):
    """
    Quick scan with summary output only
    
    Example: secudity quick MyContract.sol
    """
    
    console.print("[blue]🔍 Running quick scan...[/blue]\n")
    
    vulnerabilities = analyze_contract(contract_path)
    gas_optimizations = analyze_gas(contract_path)
    
    display_results(vulnerabilities, gas_optimizations, verbose=False)


@cli.command()
def version():
    """Display version information"""
    console.print(Panel.fit(
        "[bold blue]Secudity Audit Toolkit v1.0.0[/bold blue]\n\n"
        "Automated Smart Contract Security Analysis\n"
        "[dim]Security + Solidity = Secudity[/dim]\n\n"
        "Instagram: @secudity",
        border_style="blue"
    ))


if __name__ == '__main__':
    cli()
