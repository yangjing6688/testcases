import pytest
import re
import time
import os
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary

#----------------------------------------------------------------------------------------------------------
#   High level methods used for system test test cases
#
#----------------------------------------------------------------------------------------------------------


class SuiteUdks():

    def __init__(self):
        self.defaultLibrary = DefaultLibrary()
        self.devCmd = self.defaultLibrary.deviceNetworkElement.networkElementCliSend

    def software_commit_after_upgrading_via_xiq(self, dut_name):
        """
        This is will issue the software commit command
        :param dut_name: The name associated with the connection to the DUT
        """
        self.devCmd.send_cmd(dut_name, 'enable')
        self.devCmd.send_cmd(dut_name, 'show software')
        self.devCmd.send_cmd(dut_name, 'software commit')

    def remove_unused_versions_of_software(self, dut_name):
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

    def downgrade_to_specific_software(self, dut_name, release_name):
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
        self.defaultLibrary.apiLowLevelApis.resetDeviceUtils.login_after_reset(dut_name, "rwa", "rwa")
        self.devCmd.send_cmd(dut_name, 'enable')
        self.devCmd.send_cmd(dut_name, 'show software')
        self.devCmd.send_cmd(dut_name, 'software commit')


    def get_archive_name(self, os, platform, archive_type, version):
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

    def verifyIQAgent(self, device_os, dut_name):
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
        :param column: The column to get the value from
        :return: The value of the column
        """
        value_of_column = ''
        while value_of_column == '':
            time.sleep(5)
            xiq.xflowsmanageDevices.refresh_devices_page()
            value_of_column = xiq.xflowsmanageDevices.get_device_details(dut_serial, column)
            print('{} column did not update yet, will refresh the page then try again'.format(str))
        print('current value of column {} is : {}'.format(column, value_of_column))
        return value_of_column

    def expected_location_in_gui (self, location_from_yaml):
        """
        This will get the location as displayed in the yaml file and will return the location as is displayed in gui
        :param dut_serial: The serial number of the device
        :param platform: The platform of the device
        :param location: The location used to onboard the device
        :return: The full path of the newly created csv file
        """
        location_gui = ''
        res = re.split(',', location_from_yaml)
        for index,el in enumerate(res):
            if index < len(res) - 1:
                location_gui += el + " >> "
            elif index == len(res) - 1:
                location_gui += el
        return location_gui
    
    def create_csv_file(self, work_dir, dut_serial, platform, location=None):
        """
        This will create a new csv file based on the platform, containing the location specified for the device if any
        :param work_dir: The absolute path of the directory where the pytest file being executed is located
        :param dut_serial: The serial number of the device
        :param platform: The platform of the device
        :param location: The location used to onboard the device
        :return: The full path of the newly created csv file
        """
        if location == None:
            filename = "slm_" + platform + ".csv"
            filepath = os.path.join(work_dir, filename)
            f = open(filepath, "w+")
            f.write("SerialNumber,ServiceTag,BranchId,HostName,Location,StaticIPAddress,Netmask,DefaultGateway,Wifi0RadioProfile,Wifi0AdminState,Wifi0OperationMode,Wifi0Channel,Wifi0Power,Wifi1RadioProfile,Wifi1AdminState,Wifi1OperationMode,Wifi1Channel,Wifi1Power,SDRProfile" + "\n")
            f.write(dut_serial + "\n")
            f.close()
        else:
            filename = "slm_" + platform + "_location.csv"
            filepath = os.path.join(work_dir, filename)
            f = open(filepath, "w+")
            f.write("SerialNumber,ServiceTag,BranchId,HostName,Location,StaticIPAddress,Netmask,DefaultGateway,Wifi0RadioProfile,Wifi0AdminState,Wifi0OperationMode,Wifi0Channel,Wifi0Power,Wifi1RadioProfile,Wifi1AdminState,Wifi1OperationMode,Wifi1Channel,Wifi1Power,SDRProfile" + "\n")
            f.write(dut_serial + ",,,," + self.expected_location_in_gui(location) + "\n")
            f.close()
        print(f"File {filepath} was successfully created")
        return filepath

    def delete_csv(self, csv_file):
        """
        This will check for a csv file and will delete it if exists
        :param csv_file: The csv file to be deleted
        :return: The full path of the newly created csv file
        """
        if os.path.exists(csv_file):
            os.remove(csv_file)
            print(f"File {csv_file} was successfully deleted")

    def persona_change_routine(self, xiq, OS_before_change, OS_expected, dut_serial):
        """
        This will perform a persona change for deve provided
        :param xiq: The XIQ instance to use
        :param OS_before_change: The OS before the persona change
        :param OS_expected: The OS the device will change to
        :param dut_serial: The serial number of the device
        :return:
        """
        change_OS = xiq.xflowsmanageDevices.persona_change(device_serial=dut_serial)
        if change_OS != 1:
            pytest.fail('FAILED Persona change from {} to {} failed for serial {}'.format(
                OS_before_change, OS_expected, dut_serial))
        xiq.xflowscommonDevices.wait_until_device_online(dut_serial, retry_duration=5,
                                                         retry_count=60)
        if OS_before_change == 'EXOS':
            # to allow for potential IQagent upgrade if needed; this causes the device to disconnect and reconnect
            time.sleep(120)
        res = xiq.xflowscommonDevices.get_device_status(device_serial=dut_serial)
        if res != 'green':
            pytest.fail('FAILED Status not equal to Green for serial {}. '
                        'Instead got status : {}'.format(dut_serial, res))
        OS_after_first_change = self.get_value_specific_column(xiq, dut_serial, column='OS')
        if OS_after_first_change != OS_expected:
            pytest.fail('FAILED Expected OS was {} for serial {}. '
                        'Instead current OS is {}'.format(OS_expected, dut_serial, OS_after_first_change))
        else:
            print('PASSED successfully changed OS from {} to {} for serial {}'.format(
                OS_before_change, OS_after_first_change, dut_serial))
        res = self.get_value_specific_column(xiq, dut_serial, column='MANAGED')
        if res != 'Managed':
            pytest.fail('FAILED Status not equal to Managed for serial {}. '
                        'Instead got status : {}'.format(dut_serial, res))
