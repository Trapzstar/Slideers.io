"""
SlideSense - Voice-Controlled PowerPoint Presentation System
Setup configuration for distribution
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = (this_directory / "requirements.txt").read_text(encoding="utf-8")
install_requires = [
    line.strip() 
    for line in requirements.split('\n') 
    if line.strip() and not line.startswith('#')
]

setup(
    name="slidesense",
    version="1.0.0",
    author="SlideSense Team",
    author_email="team@slidesense.dev",
    description="Voice-Controlled PowerPoint Presentation System with Accessibility Features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/slidesense",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/slidesense/issues",
        "Documentation": "https://github.com/yourusername/slidesense/docs",
        "Source Code": "https://github.com/yourusername/slidesense",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docs", "demos"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Office Suites",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "Environment :: Win32 (MS Windows)",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-timeout>=2.1.0",
            "pytest-mock>=3.11.0",
            "mypy>=1.7.0",
            "flake8>=6.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "slidesense=main2:main",
            "slidesense-gui=gui_unified_app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.txt", "*.md"],
    },
    keywords=[
        "voice control",
        "powerpoint",
        "presentation",
        "accessibility",
        "speech recognition",
        "automation",
        "hands-free",
    ],
    zip_safe=False,
)
