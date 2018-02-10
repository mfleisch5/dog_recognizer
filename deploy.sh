#!/bin/sh
#Deploys the git repository to target

files=*.py
target=/var/www/py

for file in $files
do
  name=$(basename "$file")
  cp "$file"  "$target/$name"
done

exit 0
