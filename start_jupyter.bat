@echo off
echo Starting Jupyter Notebook for AI Agents Lab...

REM Add Python Scripts to PATH
set PATH=%PATH%;%APPDATA%\Python\Python313\Scripts

REM Set environment variables
set MONGODB_URI=mongodb+srv://demo:demo@cluster.mongodb.net/demo
set SERVERLESS_URL=https://vtqjvgchmwcjwsrela2oyhlegu0hwqnw.lambda-url.us-west-2.on.aws/

echo Environment variables set:
echo MONGODB_URI=%MONGODB_URI%
echo SERVERLESS_URL=%SERVERLESS_URL%

echo.
echo Starting Jupyter Notebook...
echo Select "Python 3.13" as your kernel when prompted.
echo.

REM Start Jupyter Notebook
python -m jupyter notebook notebooks/ai-agents-lab.ipynb

pause