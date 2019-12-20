# github-release-cli

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/sitingren/github-release-cli/blob/master/LICENSE)
[![Maintainability](https://api.codeclimate.com/v1/badges/cd29044d7637bc78f4b9/maintainability)](https://codeclimate.com/github/sitingren/github-release-cli/maintainability)

Command line tool written in Python for creating Github releases through Github REST API.

## Installation / Requirements
```
$ pip install arestclient
$ git clone git@github.com:sitingren/github-release-cli.git
$ cd github-release-cli
```

## Usage
```bash
$ python publish_github_release.py --help
usage: publish_github_release.py [-h] -V VERSION -o OWNER -r REPO -t TOKEN
                                 [-d DESCRIPTION] [-a ASSET] [--draft]
                                 [--prerelease]

Create a release on Github

optional arguments:
  -h, --help            show this help message and exit
  -V VERSION, --version VERSION
                        release version
  -o OWNER, --owner OWNER
                        Github repo owner
  -r REPO, --repo REPO  Github repo name
  -t TOKEN, --token TOKEN
                        Github access token (with push access)
  -d DESCRIPTION, --description DESCRIPTION
                        Github release description
  -a ASSET, --asset ASSET
                        path to an asset
  --draft               create a draft (unpublished) release
  --prerelease          identify the release as a prerelease
```
