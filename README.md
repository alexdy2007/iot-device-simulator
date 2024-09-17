# iot-device-simulator-backend

Needs HTTPS to deply on lakehouse apps. To run locally on localhost

1) install

brew install mkcert
brew install nc
mkcert -install nss
mkcert localhost 127.0.0.1 ::1

Lauch .json file example

{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Module",
            "type": "debugpy",
            "envFile": "/Users/alex.young/Projects/iot-device-simulator/backend/.env",
            "request": "launch",
            "module": "uvicorn",
            "args": ["app:app","--reload","--ssl-keyfile=./localhost+2-key.pem", "--ssl-certfile=localhost+2.pem"]
        }
    ]
}


backend start locally (Change certs as required)

uvicorn app.app:app --reload --ssl-keyfile="./localhost+2-key.pem" --ssl-certfile="localhost+2.pem"

frontend start

npm start

TODO
- Pagination of devices
- Group by devices
- Change Terminology to match OSI PI
- Search Devices
- Delte Devices
- Endpoint Functionality
- Multiple Endpoint Adding
- Marcov Chain Distribution
- Gamma Distribution
- Device Fault percentile
- Device Fault Alert Flagging
- Trigger a Fault
- Deployment
- How to run in databricks notebook
