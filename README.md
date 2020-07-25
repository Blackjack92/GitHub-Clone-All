# Clone all GitHub Repositories

The following repository contains a simple repository cloner. Depending on a given username and access token all related repositories are downloaded. Furthermore it sorts the downloaded repositories regarding the respective primary language of a repository. When no language is given, the repository will be cloned into a folder called "UNKNOWN".

## Requirements

- Python3
- The following Python3 modules installed:
    - GitPython
    - json
    - pathlib
    - requests
    - termcolor
- An access token for GitHub: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

## Usage

1. Copy the script clone-repos.py into the directory where all repositories should be downloaded.
2. Start the script with
    a) without debugging python3 clone-repos.py
    b) with debugging python3 clone-repos.py debug
3. Enter the username
4. Enter the access token
5. Wait --> Finished

## Screenshot from the Usage

![Usage without debugging](documentation/without_debugging.png?raw=true "Usage without debugging")
![Usage with debugging](documentation/with_debugging.png?raw=true "Usage with debugging")
![Usage with debugging, directory structure](documentation/with_debugging_directories.png?raw=true "Usage with debugging, directory structure")