@echo off
REM Development helper script for SlideSense (Windows)

setlocal EnableDelayedExpansion

echo SlideSense Development Helper
echo.

if "%1"=="" goto usage
if "%1"=="help" goto usage
if "%1"=="check" goto check
if "%1"=="install" goto install
if "%1"=="test" goto test
if "%1"=="types" goto types
if "%1"=="coverage" goto coverage
if "%1"=="lint" goto lint
if "%1"=="clean" goto clean
if "%1"=="all" goto all
goto usage

:check
echo Checking Python version...
python --version
goto end

:install
echo Installing dependencies...
pip install -q -r requirements.txt
echo Dependencies installed successfully!
goto end

:test
echo Running tests...
python -m pytest tests/ -v --tb=short
goto end

:types
echo Checking types with mypy...
python -m mypy main2.py utils.py config.py logger.py exceptions.py --ignore-missing-imports
goto end

:coverage
echo Running coverage analysis...
python -m pytest tests/ --cov=. --cov-report=html --cov-report=term
echo Coverage report generated in htmlcov/
goto end

:lint
echo Linting code...
where flake8 >nul 2>&1
if %errorlevel%==0 (
    flake8 *.py --max-line-length=100 --ignore=E501,W503
) else (
    echo flake8 not installed. Install with: pip install flake8
)
goto end

:clean
echo Cleaning build artifacts...
if exist __pycache__ rmdir /s /q __pycache__
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist .mypy_cache rmdir /s /q .mypy_cache
if exist htmlcov rmdir /s /q htmlcov
if exist .coverage del /f .coverage
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
for /r %%i in (*.pyc) do del /f "%%i"
for /r %%i in (*.pyo) do del /f "%%i"
echo Cleaned successfully!
goto end

:all
call :check
call :test
call :types
call :lint
goto end

:usage
echo Usage: dev.bat [command]
echo.
echo Commands:
echo   check     - Check Python version
echo   install   - Install dependencies
echo   test      - Run tests
echo   types     - Check type hints
echo   coverage  - Run coverage analysis
echo   lint      - Lint code
echo   clean     - Clean build artifacts
echo   all       - Run all checks (test + types + lint)
echo   help      - Show this help
goto end

:end
echo.
endlocal
