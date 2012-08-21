#!/bin/bash

cd ../
nosetests3 --with-coverage --cover-html --cover-html-dir=test/_cover/ --cover-erase --cover-package=epub
nosetests2 --with-coverage --cover-html --cover-html-dir=test/_cover/ --cover-erase --cover-package=epub
