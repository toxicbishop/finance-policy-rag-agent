# Create virtual environment if it doesn't exist
if (!(Test-Path -Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
. .venv\Scripts\Activate.ps1

# Install requirements
Write-Host "Installing requirements..."
pip install -r requirements.txt

Write-Host ""
Write-Host "Setup complete!"
Write-Host "To start the FastAPI backend, run: uvicorn backend.main:app --reload"
Write-Host "To start the Streamlit dashboard, run: streamlit run dashboard/app.py"
Write-Host "You are now inside the virtual environment."
