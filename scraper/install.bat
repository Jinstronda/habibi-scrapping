@echo off
echo ====================================
echo Android App Scraper - Installation
echo ====================================
echo.

echo Activating conda environment: turing0.1
call conda activate turing0.1

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Creating screenshots directory...
mkdir screenshots 2>nul

echo.
echo ====================================
echo Installation complete!
echo ====================================
echo.
echo Next steps:
echo 1. Start your Android emulator
echo 2. Open the target app
echo 3. Run: python setup.py
echo 4. Configure config.py with app details
echo 5. Run: python main.py
echo.
pause
