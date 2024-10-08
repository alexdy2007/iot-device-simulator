cd build
databricks sync --watch . /Workspace/Users/alex.young@databricks.com/device-gen-demo
databricks apps deploy device-gen-demo --source-code-path /Workspace/Users/alex.young@databricks.com/device-gen-demo
