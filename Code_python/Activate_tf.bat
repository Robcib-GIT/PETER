@echo off
REM Step 1: Store the current directory (P1)
set "P1=%cd%"

REM Step 2: Navigate to the virtual environment's directory and activate it
cd /d "C:\ProgDos\Venvs\tf\Scripts"
call activate

REM Step 3: Return to the original directory (P1)
cd /d "%P1%"

REM Step 4: Open the Python interactive shell for manual input
python
