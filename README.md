## How to start
1. Create a launch.json file
```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Flask",
            "type": "debugpy",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app/app.py",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true,
            "autoStartBrowser": false
        }
    ]
}
```

2. Create a virtual env
```
python3 -m venv profit_env
```

3. Activate the env
```
source profit_env/bin/activate
```

4. Install requirements
```
pip3 install -r requirements.txt
```

5. Start the app with the vscode debugger.

