#!/usr/bin/env bash

cd /home/bas/share/src/meterstanden
git pull
git add data/.
git commit -m data
git push origin master


