#!/bin/bash
# Development helper script for SlideSense

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}SlideSense Development Helper${NC}\n"

# Function to check Python version
check_python() {
    echo -e "${YELLOW}Checking Python version...${NC}"
    python_version=$(python --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python $python_version${NC}"
}

# Function to install dependencies
install_deps() {
    echo -e "\n${YELLOW}Installing dependencies...${NC}"
    pip install -q -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
}

# Function to run tests
run_tests() {
    echo -e "\n${YELLOW}Running tests...${NC}"
    python -m pytest tests/ -v --tb=short
    echo -e "${GREEN}✓ Tests completed${NC}"
}

# Function to check types
check_types() {
    echo -e "\n${YELLOW}Checking types with mypy...${NC}"
    python -m mypy main2.py utils.py config.py logger.py exceptions.py --ignore-missing-imports
    echo -e "${GREEN}✓ Type checking completed${NC}"
}

# Function to run coverage
run_coverage() {
    echo -e "\n${YELLOW}Running coverage analysis...${NC}"
    python -m pytest tests/ --cov=. --cov-report=html --cov-report=term
    echo -e "${GREEN}✓ Coverage report generated in htmlcov/${NC}"
}

# Function to lint code
lint_code() {
    echo -e "\n${YELLOW}Linting code...${NC}"
    if command -v flake8 &> /dev/null; then
        flake8 *.py --max-line-length=100 --ignore=E501,W503
        echo -e "${GREEN}✓ Linting completed${NC}"
    else
        echo -e "${RED}✗ flake8 not installed. Install with: pip install flake8${NC}"
    fi
}

# Function to clean build artifacts
clean() {
    echo -e "\n${YELLOW}Cleaning build artifacts...${NC}"
    rm -rf __pycache__
    rm -rf .pytest_cache
    rm -rf .mypy_cache
    rm -rf htmlcov
    rm -rf .coverage
    rm -rf *.egg-info
    rm -rf dist
    rm -rf build
    find . -name "*.pyc" -delete
    find . -name "*.pyo" -delete
    find . -name "*~" -delete
    echo -e "${GREEN}✓ Cleaned${NC}"
}

# Function to show usage
usage() {
    echo "Usage: ./dev.sh [command]"
    echo ""
    echo "Commands:"
    echo "  check     - Check Python version"
    echo "  install   - Install dependencies"
    echo "  test      - Run tests"
    echo "  types     - Check type hints"
    echo "  coverage  - Run coverage analysis"
    echo "  lint      - Lint code"
    echo "  clean     - Clean build artifacts"
    echo "  all       - Run all checks (test + types + lint)"
    echo "  help      - Show this help"
}

# Main script
case "$1" in
    check)
        check_python
        ;;
    install)
        install_deps
        ;;
    test)
        run_tests
        ;;
    types)
        check_types
        ;;
    coverage)
        run_coverage
        ;;
    lint)
        lint_code
        ;;
    clean)
        clean
        ;;
    all)
        check_python
        run_tests
        check_types
        lint_code
        ;;
    help|*)
        usage
        ;;
esac

echo ""
