#!/usr/bin/env bash

cd /home/bas/src/meterstanden
git pull
git add docs/data/.
git commit -m data
git push origin master


