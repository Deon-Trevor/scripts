#!/bin/sh

# This script works best when you have specific files that change constantly 
# and don't need dynamic commit messages

GIT=`which git`
REPO_DIR=~/Documents/VSCode/phishfort/harvester-shodan/python # repo directory
cd ${REPO_DIR}
${GIT} pull
${GIT} add phish.cache # file to auto add
${GIT} commit -m "Updated cache" # git commit message
${GIT} push 