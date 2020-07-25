#!/usr/local/opt/python3

import git
import json
import sys

from pathlib import Path
from requests import get
from requests.utils import requote_uri
from getpass import getpass
from termcolor import colored

debug = "debug" in sys.argv
if debug:
    print("Debug Mode is enabled.")
    print("-" * 100)

username = input("Please Enter your GitHub username: ")
# create an access_token: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token
access_token = getpass("Please Enter your GitHub access token: ")
# make username url compliant
username = requote_uri(username)


def read_all_repositories(username, access_token):
    repositories = json.loads(
        get(
            "https://api.github.com/users/{}/repos".format(username),
            headers={'Authorization': 'token {}'.format(access_token)}
        ).text)

    return map(lambda repository: repository['html_url'], repositories)

def append_credentials(repository, username, access_token):
    # split clone url in protocoll and domain
    protocol, domain = repository.split('//', 1)
    # combine clone url with username and password
    repository_with_credentials = '{}//{}:{}@{}.git'.format(protocol, username, access_token, domain)
    return repository_with_credentials

def generate_languages_api(repository, username):
    # take project name from repository url
    project_name = repository.split('/')[-1]
    # combine to languages api
    languages_api = "https://api.github.com/repos/{}/{}/languages".format(username, project_name)
    return [languages_api, project_name]

def read_primary_language(languages_api, access_token):
    # read languages and occurences
    # programming_languages = get(languages_api, auth=(username, password))
    programming_languages = get(languages_api, headers={'Authorization': 'token {}'.format(access_token)})
    # take just languages
    programming_languages = json.loads(programming_languages.text).keys()
    # take first language entry
    primary_language = next(iter(programming_languages)) if len(programming_languages) > 0 else "UNKNOW"
    return primary_language

def clone_project(target_folder, project_name, repository, repository_with_credentials):
    # check project is not already cloned
    if Path("{}/{}".format(target_folder, project_name)).exists():
        print(colored("Repository [{}] was already cloned.".format(repository), 'yellow'))
    else:
        # create primary language repo when neccessary
        Path(target_folder).mkdir(parents=True, exist_ok=True)
        # clone repo in correct directory
        git.Git(target_folder).clone(repository_with_credentials)
        print(colored("Repository [{}] was cloned.".format(repository), 'green'))

def run(username, access_token, debug):
    repositories = list(read_all_repositories(username, access_token))

    for repository in repositories:
        repository_with_credentials = append_credentials(repository, username, access_token)
        if debug:
            print("Repository URL with Credentials [{}]".format(repository_with_credentials))

        languages_api, project_name = generate_languages_api(repository, username)
        if debug:
            print("Languages API URL [{}]".format(languages_api))

        primary_language = read_primary_language(languages_api, access_token)
        if debug:
            print("Primary Language for the target directory [{}]".format(primary_language))

        # create target clone folder by primary language
        target_folder = "./{}".format(primary_language)

        # here is the git clone called
        clone_project(target_folder, project_name, repository, repository_with_credentials)

        if debug:
            print("-" * 100)

run(username, access_token, debug)
