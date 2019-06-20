#!/usr/bin/env python

# https://github.com/sitingren/github-release-cli
#
# Copyright (c) 2019 Siting Ren. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function, division, absolute_import

import os
import sys
import argparse
# install agithub by calling 'pip install arestclient'
from agithub.GitHub import GitHub

OWNER = None
REPO = None
GITHUB_TOKEN = None


def create_github_release(version, is_draft, is_prerelease, description, asset):
    # Create a GitHub object using an access token
    g = GitHub(token=GITHUB_TOKEN)

    name = version
    status, r = g.repos[OWNER][REPO].releases.post(
        body={
            'tag_name': version,
            'target_commitish': 'master',
            'name': name,
            'body': description,
            'draft': is_draft,
            'prerelease': is_prerelease,
        })
    if status == 201:
        print("Created a Github release")
        if asset != '':
            print('Uploading an asset ...')
            upload_asset_to_github(r['id'], asset)
    else:
        print("Failed with message: {}".format(r))
        sys.exit(1)


def upload_asset_to_github(release_id, asset):
    gh = GitHub(token=GITHUB_TOKEN, api_url='uploads.github.com')

    with open(asset, 'rb') as f:
        file_content = f.read()
    file_name = os.path.basename(asset)

    status, r = gh.repos[OWNER][REPO].releases[release_id].assets.post(
        name=file_name,
        body=file_content,
        headers={'content-type': 'application/octet-stream'})

    if status == 201:
        print("Successful upload")
    else:
        print("Upload failed with message: {}".format(r))
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a release on Github')
    parser.add_argument('-V', '--version', type=str, help='release version', required=True)
    parser.add_argument('-o', '--owner', type=str, help='Github repo owner', required=True)
    parser.add_argument('-r', '--repo', type=str, help='Github repo name', required=True)
    parser.add_argument('-t', '--token', type=str, help='Github access token (with push access)', required=True)
    parser.add_argument('-d', '--description', type=str, help='Github release description', default='')
    parser.add_argument('-a', '--asset', type=str, help='path to an asset', default='')
    parser.add_argument('--draft', help='create a draft (unpublished) release', action='store_true')
    parser.add_argument('--prerelease', help='identify the release as a prerelease', action='store_true')

    args = parser.parse_args()
    print("Create a release on Github with the following info:")
    for k, v in vars(args).items():
        print("    {}: {}".format(k, v))

    OWNER = args.owner
    REPO = args.repo
    GITHUB_TOKEN = args.token

    create_github_release(args.version, args.draft, args.prerelease, args.description, args.asset)
