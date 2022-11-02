import pytest
import re
import time
import selenium

from extauto.common.AutoActions import AutoActions
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
    NetworkElementConnectionManager
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary


class SuiteUdk:

    def __init__(self):
        self.defaultLibrary = DefaultLibrary()
        self.auto_actions = AutoActions()
        self.devCmd = self.defaultLibrary.deviceNetworkElement.networkElementCliSend

    def get_virtual_router(self, dut):
        global vrName

        result = self.devCmd.send_cmd(dut.name, 'show vlan', max_wait=10, interval=2)

        output = result[0].cmd_obj.return_text

        pattern = f'(\w+)(\s+)(\d+)(\s+)({dut.ip})(\s+)(\/.*)(\s+)(\w+)(\s+/)(.*)(VR-\w+)'

        match = re.search(pattern, output)

        if match:
            print(f"Mgmt Vlan Name : {match.group(1)}")
            print(f"Vlan ID        : {match.group(3)}")
            print(f"Mgmt IPaddress : {match.group(5)}")
            print(f"Active ports   : {match.group(9)}")
            print(f"Total ports    : {match.group(11)}")
            print(f"Virtual router : {match.group(12)}")

            if int(match.group(9)) > 0:
                return match.group(12)
            else:
                print(f"There is no active port in the mgmt vlan {match.group(1)}")
                return -1;
        else:
            print("Pattern not found, unable to get virtual router info!")
            return -1;
