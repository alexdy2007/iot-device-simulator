#!/bin/bash
# Accept parameters
APP_FOLDER_IN_WORKSPACE="/Workspace/Users/alex.young@databricks.com/device_sim_app"
# Databricks App must already have been created. You can do so with the Databricks CLI or via the UI in a Workspace.
LAKEHOUSE_APP_NAME="device-gen-demo"


local=False
while getopts l o; do
  case $o in
    (l) local=True;;
  esac
done

echo $local

if [$local = False]; then
  echo "Deploying to Databricks"
fi

# Frontend build and import. Swap in your /frontend folder name if it's different here. 
if [ -d backend ] && [ -d frontend ]; then 


  (
    cd frontend
    npm run build
    databricks workspace delete --recursive $APP_FOLDER_IN_WORKSPACE/static
    databricks workspace import-dir build "$APP_FOLDER_IN_WORKSPACE/static" --overwrite
    
  ) &
  # Backend packaging. Swap in your /backend folder name if it's different here. 
  (
    cd backend
    mkdir -p build
    # Exclude all hidden files and app_prod.py
    find . -mindepth 1 -maxdepth 1 -not -name '.*' -not -name "*.pyc" -not -name "*Pipfile*" -not -name "*CACHEDIR*" -not -name "*.json" -not -name "local_conf*" -not -name 'build' -not -name 'cache' -not -name '*__pycache__*' -not -name '*test*' -exec cp -r {} build/ \;
    databricks workspace import-dir build "$APP_FOLDER_IN_WORKSPACE" --overwrite
    rm -rf build
  ) &
  # Wait for both background processes to finish
  wait
  
  # Deploy the application
  if [ $local = False ]; then
    cp -r ./frontend/build/ ./backend/static
    databricks apps deploy "$LAKEHOUSE_APP_NAME" "$APP_FOLDER_IN_WORKSPACE"
    # Print the app page URL -- put your workspace name in the below URL. 
    echo "Open the app page for details and permission: WORKSPACEURL.com/apps/$LAKEHOUSE_APP_NAME";
  else
    cp -r ./frontend/build/ ./backend/static
    echo "Built Locally"
  fi

fi