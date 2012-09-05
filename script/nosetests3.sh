#!/bin/bash

cd ../
nosetests3 --with-coverage --cover-html --cover-html-dir=test/_cover3/ --cover-erase --cover-package=epub
