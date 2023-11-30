
import time
import os
import Helpers.configuration as config

def main():
    try:
        print(os.popen("sudo systemctl stop brewbomb.service").read())
        time.sleep(1)
        config.set_value("calibration", "calibrated", False)
        config.set_value("AppInfo", "BrewerSerialNumber", "ACE")
        print(os.popen("cd /Share && sudo find . | grep -E \"(__pycache__|\.pyc|\.pyo$)\" | sudo xargs rm -rf").read())
        print(os.popen("sudo rm /Share/py.log").read())
        print(os.popen("cd /Share && zip -r /Share/Share.zip ./* -x Share*/**\* __py*/**\*").read())
        config.set_value("calibration", "calibrated", True)
        config.set_value("AppInfo", "BrewerSerialNumber", "ACE001")
        print(os.popen("sudo systemctl start brewbomb.service").read())
    except Exception as e:
        print(e)

main()
