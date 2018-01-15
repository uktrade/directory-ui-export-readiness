#!/bin/bash
REPOS="
../directory-sso
../directory-sso-profile
../help
../directory-ui-buyer
../directory-ui-export-readiness
../navigator"
echo "Enter the name of the git branch to create followed by [ENTER]:"
read branch
for dir in $REPOS; do
	echo "Switching to repo $dir"
	cd $dir
	git stash
	git checkout master
	git pull
	git branch $branch
	git checkout $branch
done
