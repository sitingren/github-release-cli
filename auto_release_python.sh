#!/bin/sh -e

# Path to Python interpreter
PYTHON=${PYTHON:-python3}

echo "This program releases a python package on Github and PyPI. Please check prerequisites:"
echo "  Set the Github repository owner via GITHUB_OWNER environment variable, e.g. export GITHUB_OWNER=xxx"
echo "  Set the Github repository name via GITHUB_REPO environment variable, e.g. export GITHUB_REPO=github-release-cli"
echo "  Set the Github access token via GITHUB_TOKEN environment variable. The token should have push access to the repository."
echo "  Set the PyPI account username via TWINE_USERNAME environment variable. Current TWINE_USERNAME="$TWINE_USERNAME
echo "  Set the PyPI account password via TWINE_PASSWORD environment variable. Current TWINE_PASSWORD="$TWINE_PASSWORD
echo "  Set the path to Python interpreter via PYTHON environment variable. Default to use 'python3'."
echo "  Ensure you have installed 'twine' for publishing to PyPI, otherwise call 'pip install twine' to install."
echo "  Confirm you have updated the version number in source code and setup.py."
echo ""
read -p "Press <Enter> to continue or <Ctrl-C> to exit ... " answer


##################################
# Generate distribution archives
##################################
echo -e "\n\n>>> Cloning $GITHUB_OWNER/$GITHUB_REPO repository"
TMPDIR=release_tmp
rm -rf $TMPDIR
mkdir $TMPDIR
cd $TMPDIR
git clone git@github.com:$GITHUB_OWNER/$GITHUB_REPO.git -q
echo "Cloned repository"
cd $GITHUB_REPO
echo -e "\n\n>>> Generating distribution archives"
# generate wheel file and compressed source file
$PYTHON setup.py -q sdist bdist_wheel --universal
echo -e "\n\n>>> Generated distribution archives:"
ls dist/
trap 'echo -e "\nPlease delete $TMPDIR directory if you do not need archives any more"' EXIT

# double check the version number
wheelfile=`ls dist/ | grep whl`
filepath=`readlink -f dist/$wheelfile`
version=`$PYTHON setup.py --version`
package_name=`$PYTHON setup.py --name`
echo -e "\nYou are going to release version $version for $GITHUB_OWNER/$GITHUB_REPO repository."
while true; do
    read -p "Please type in the version number to confirm or 'exit': " yn
    case $yn in
        $version ) break;;
        'exit' ) exit;;
    esac
done


########################
# Publish to PyPI
########################
echo -e "\n\n>>> Publishing to PyPI"

### upload archives to TestPyPI (like dry-run)
###twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# upload archives to PyPI
twine upload dist/* # --skip-existing
echo "Successfully uploaded to PyPI"
cd ../..


########################
# Publish to Github
########################
echo -e "\n\n>>> Publishing to Github"

response=$(curl \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/$GITHUB_OWNER/$GITHUB_REPO/releases \
  -d '{"tag_name":"'$version'","target_commitish":"master","name":"'$version'","draft":false,"prerelease":false,"generate_release_notes":true}')

regex='"id": ([0-9]+),'
[[ $response =~ $regex ]]
release_id=${BASH_REMATCH[1]}
echo $response
echo "--> Github release_id: $release_id"
echo ""
echo "Uploading an asset to Github ..."
if [ -z "$release_id" ]
then
  echo "Cannot get release_id. Skipped."
else
  curl -X POST \
     -H "Content-Type: $(file -b --mime-type $filepath)" \
     -T "$filepath" \
     -H "Authorization: token $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github.v3+json" \
     https://uploads.github.com/repos/$GITHUB_OWNER/$GITHUB_REPO/releases/$release_id/assets?name=$wheelfile | cat
fi

########################
# Wrap-up
########################
echo -e "\n\nFinal checklist:"
echo "1. View PyPI url (https://pypi.org/project/$GITHUB_REPO/#files) and check files uploaded"
echo "2. View Github url (https://github.com/$GITHUB_OWNER/$GITHUB_REPO/releases) and add descriptions if needed"
echo -e "3. Try pip installation (pip install $package_name --user) and verify package version number with \n\t\"pip list | grep $package_name\" and \n\t\"python -c 'import vertica_python; print(vertica_python.__version__)'\""
