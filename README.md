# Lambda Layers POC

Project demonstrating the use of AWS Lambda Layers with multiple functions sharing common code through a shared layer.

## Project Structure

```
lambda_layers_poc/
├── hello_world_1/          # First Lambda function
├── hello_world_2/          # Second Lambda function
├── shared/service/         # Shared layer with MockService
├── events/                 # Test events
├── tests/                  # Unit tests
├── local_test_*.py         # Scripts for local testing
├── template.yaml           # SAM template (functions + layer)
└── samconfig.yml           # SAM CLI configuration
```

## Components

### SharedLayer
- **Location**: `shared/service/MockService.py`
- **Content**: `MockService` class providing shared functionality
- **Usage**: Both Lambda functions reference this layer

### Lambda Functions
- **HelloWorld1Function**: `/hello` endpoint using SharedLayer
- **HelloWorld2Function**: Second function using the same SharedLayer

## Development Commands

### Environment Setup and Activation

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

### Local Testing (without SAM)

```powershell
# Test function 1
python local_test_hello_world_1.py

# Test function 2
python local_test_hello_world_2.py
```

### Build and Test with SAM

```powershell
# Build project
sam build

# Invoke functions directly
sam local invoke HelloWorld1Function --event events/event.json
sam local invoke HelloWorld2Function --event events/event.json

# Start local API
sam local start-api

# Test endpoint (in another terminal)
curl http://127.0.0.1:3000/hello-world-1
curl http://127.0.0.1:3000/hello-world-2
```

### Debugging with SAM

```powershell
# Start in debug mode
sam local start-api --debug-port 5890 --debugger-path .venv\Lib\site-packages\debugpy --debug-args="-Xfrozen_modules=off -m debugpy --wait-for-client --listen 0.0.0.0:5890"

# In VS Code: Run and Debug > "Attach SAM Python" > F5
# Then make curl request to endpoint
```

### Deploy to AWS

```powershell
# Initial deploy
sam deploy --guided

# Subsequent deploys
sam deploy
```

### Cleanup

```powershell
sam delete --stack-name "lambda-layers-poc"
```

## VS Code Configuration

- **Debugging**: Configurations in `.vscode/launch.json` for local and SAM debugging
- **Python Analysis**: Configured in `.vscode/settings.json` to resolve layer imports
- **Virtual Environment**: Configured to use `.venv/`

## Requirements

- AWS SAM CLI
- Python 3.13+
- Docker
- VS Code with Python extension
