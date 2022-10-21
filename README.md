# CLI UPLOAD

Cli Upload using Typer

### Setup
- Install python 3.7 or newer
- Install `pyinstaller`
```commandline
pip install -U pyinstaller
```

- Install `pipenv`
```commandline
pip install --user pipenv
```

- Install `pipenv`
```commandline
pip install --user pipenv
```

- Install dependencies
```commandline
pip install bson
pip install typer
pip install halo
pip install pick
```

- Read more about `pyinstaller` here: https://pyinstaller.org/en/stable/

### Commands
- Run to build a single file .exe
```commandline
pyinstaller --onefile --paths .\venv\Lib\site-packages main.py
```

### Usage CLI
- Open the CMD Window and `cd` to the folder contains the file .exe. For example, the file .exe in the folder `E:\cli-upload`.
```
cd E:\cli-upload
```

- Run this command to get the usage information
```
cli-upload --help
```

- Example run this command for login and uploading a file json and the base API endpoint is `http://evo.com/api`.
```
cli-upload admin@email.com admin123 FILE_DATA.json --api-url=http://example.com/api
```


