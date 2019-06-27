#!/bin/bash
set -x -e

orig_pwd=`pwd`
cd `mktemp -d`

git clone https://github.com/mozilla/OpenWPM.git --depth=1
cd OpenWPM
pip install --upgrade -r requirements.txt
./install.sh --no-flash
rm -rf automation/Extension/firefox/node_modules # not needed after the extension built, avoid copying these when installing the module
cd ..

cp $orig_pwd/openwpm_setup.py setup.py
pip install . # install with setup.py, like a package, so it can be imported from anywhere

pip show OpenWPM # verify the install
