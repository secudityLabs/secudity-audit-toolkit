from setuptools import setup, find_packages

setup(
    name="secudity-audit-toolkit",
    version="1.0.0",
    description="Automated Smart Contract Security Analysis Tool",
    author="Secudity Team",
    author_email="secudity.mail@gmail.com",
    url="https://github.com/secuditylabs/secudity-audit-toolkit",
    packages=find_packages(),
    install_requires=[
        "slither-analyzer==0.10.0",
        "click==8.1.7",
        "rich==13.7.0",
        "pyyaml==6.0.1",
        "python-dotenv==1.0.0",
        "reportlab==4.0.7",
        "markdown2==2.4.10",
    ],
    entry_points={
        'console_scripts': [
            'secudity=src.cli:cli',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
