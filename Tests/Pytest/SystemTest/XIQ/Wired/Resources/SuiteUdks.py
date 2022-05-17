import pytest
import re
import time
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary

#----------------------------------------------------------------------------------------------------------
#   High level methods used for system test test cases
#
#----------------------------------------------------------------------------------------------------------


class SuiteUdks():

    def __init__(self):
        self.defaultLibrary = DefaultLibrary()
        self.devCmd = self.defaultLibrary.deviceNetworkElement.networkElementCliSend

    def software_commit_after_upgrading_via_xiq(self,dut_name):
        """
        This is will issue the software commit command
        :param dut_name: The name associated with the connection to the DUT
        """
        self.devCmd.send_cmd(dut_name, 'enable')
        self.devCmd.send_cmd(dut_name, 'show software')
        self.devCmd.send_cmd(dut_name, 'software commit')

    def remove_unused_versions_of_software(self,dut_name):
        """
        This will remove any non Primary/Backup Image(s) from the switch.
        This should be run in order to insure there is enough space to download a new image
        :param dut_name: The name associated with the connection to the DUT
        """
        output = self.devCmd.send_cmd(dut_name, 'show software')
        send_cmd_output = output[0].cmd_obj.return_text
        regex = "([A-Za-z0-9]+[.][0-9]+[.][0-9]+[.][0-9]+[.][A-Za-z0-9]+)"
        software_release_list = []
        for line in send_cmd_output.split('\n'):
            line = line.replace("\r", "")
            software_version = re.search(regex, line)
            if software_version:
                if ("Primary" in line) or ("Backup" in line):
                    print("Did not remove '{0}' since it is either the primary of backup release".format(software_version.group(1)))
                else:
                    print("software to remove {0}".format(software_version.group(1)))
                    self.devCmd.send_cmd(dut_name, 'software remove ' + software_version.group(1))

    def iqagent_reinstall(self, dut_name):
        """
        This will install the iqagent that is part of the operation software package
        :param dut_name: The name associated with the connection to the DUT
        """
        self.devCmd.send_cmd(dut_name, 'enable')
        self.devCmd.send_cmd(dut_name, 'configure terminal')
        self.devCmd.send_cmd(dut_name, 'application')
        self.devCmd.send_cmd(dut_name, 'no iqagent enable')
        self.devCmd.send_cmd(dut_name, 'dbg enable')
        self.devCmd.send_cmd(dut_name, 'software iqagent reinstall')
        self.devCmd.send_cmd(dut_name, 'iqagent enable')
        time.sleep(30)
        self.devCmd.send_cmd(dut_name, 'exit')

    def downgrade_to_specific_software(self, dut_name,release_name):
        """
        This is will activate an installed version of software on the VOSS device
        :param dut_name: The name associated with the connection to the DUT
        :param release_name: The release name of sotware to activate

        """
        self.devCmd.send_cmd(dut_name, 'enable')
        self.devCmd.send_cmd(dut_name, 'software activate ' + release_name)
        time.sleep(15)
        self.devCmd.send_cmd(dut_name, 'show software')
        self.defaultLibrary.apiLowLevelApis.resetDeviceUtils.reboot_network_element_now_and_wait(dut_name,max_wait=300)
        self.defaultLibrary.apiLowLevelApis.resetDeviceUtils.login_after_reset(self.tb.dut1_name, "rwa", "rwa")
        self.devCmd.send_cmd(self.tb.dut1_name, 'enable')
        self.devCmd.send_cmd(self.tb.dut1_name, 'show software')
        self.devCmd.send_cmd(self.tb.dut1_name, 'software commit')


    def get_archive_name(self,os,platform,archive_type,version):
        """
        This returns a String that represents the image to load onto a switch.
        :param os: The type of OS
        :param platform: The platform of the switch aka 5X20,4900,7400, This is need to determine if the image will end
                         in tgz or voss
        :param archive_type: Either global on non_global. Global indicates the cloud has the image installed.
                             Non global means a customer did a drag and dropped of a specific image
        :param version: The release version of software
        :return: A string representing the name to be used to change software on the device
        """
        archive_name = ''
        if platform == '1400' or platform == '4900' or platform == '7400':
            archive_name += os.upper()
            archive_name += platform
            archive_name += '.'
            archive_name += version
            if archive_type == 'Global':
                archive_name += '.tgz (GLOBAL)'
            else:
                archive_name += '.tgz'
        else:
            archive_name += platform
            archive_name += '.'
            archive_name += version
            if archive_type == 'Global':
                archive_name += '.voss (GLOBAL)'
            else:
                archive_name += '.voss'

        print('Archive used for baseline will be : {}'.format(archive_name))
        return archive_name

    def verifyIQAgent(self, device_os,dut_name):
        """
        This is a very crude function to validate the IQAgent is enabled on the switch.
        :param device_os: The os running on the device- Either VOSS or EXOS
        :param dut_name: The name associated with the connection to the DUT
        :return:
        """
        if device_os == "exos":
            self.devCmd.send_cmd_verify_output(dut_name, 'show process iqagent', 'Ready', max_wait=30,interval=10)
        else:
            self.devCmd.send_cmd_verify_output(dut_name, 'show application iqagent', ' True',max_wait=30, interval=10)

    def get_value_specific_column(self, xiq, dut_serial, column):
        """
        This will get a value in a specific colunm for a specific device, from the devices page
        :param xiq: The XIQ instance to use
        :param dut_serial: The serial number of the device
        :param colunm: The colunm to get the value from
        :return: The value of the colunm
        """
        value_of_column = ''
        while value_of_column == '':
            time.sleep(5)
            xiq.xflowsmanageDevices.refresh_devices_page()
            value_of_column = xiq.xflowsmanageDevices.get_device_details(dut_serial,column)
            print('{} column did not update yet, will refresh the page then try again'.format(str))
        print('current value of column {} is : {}'.format(column,value_of_column))
        return value_of_column
