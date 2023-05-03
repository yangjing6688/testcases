import pytest
import time
import re
import string
import random

from Tests.Pytest.NonProduction.XIQ.XIQ_1365.testbed_1_node.Resources.testcase_base import xiqBase
from pytest_testconfig import config


class TCXM20578Tests(xiqBase):

    @pytest.mark.development
    @pytest.mark.xim_tcxm_20578
    @pytest.mark.p1
    def test_tcxm_20578(self, onboarding_location):
        """
        Author        :     dciupitu
        Description   :     Verify that Option for "Upgrade to the specific device firmware version" is present.
        Preconditions :     Current device firmware version and at least one more additional firmware version should be
                            present on the AIO or Cloud environment

        Step    Description

        1.      Create a network policy.
        2.      In Device Template TAB select an EXOS switch template and check Advanced Settings TAB is present in
                Configuration Menu.
        3.      Click on Advanced Settings TAB.
        4.      There is a option for "Upgrade to the specific device firmware version" and can be selected.Then click
                Save button.
        5.      After selecting this option a list of firmware available should appear and user can choose one.
        6.      After selecting one firmware from the list, when a device is onboarded and network policy is set,
                firmware will automatically update to the chosen firmware from the list.
        7.      Check that the image list that are shown from the drop-down are based on the switch template that is
                selected :
                a.	if the template selected is X440G2 then it should not list the Summit_arm/Summit_arm_lite/Onie/VOSS
                    images.
                b.	If the template selected is 5320/5720 then it should list only the supported images by these
                    platforms (it should not list all the summit _arm images).
        """
        self.executionHelper.testSkipCheck()

        self.cfg['${test_name}'] = 'test1_tcxm_20578'
        dut = self.tb.dut1

        pool = list(string.ascii_letters) + list(string.digits)
        network_policy_name = f"policy_XIQ1365_{''.join(random.sample(pool, k=4))}"
        device_template_name = f"template_XIQ1365_{''.join(random.sample(pool, k=4))}"

        location = onboarding_location
        xiq_ip_address = config['sw_connection_host']

        try:
            self.devCmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')

            output_cmd = self.devCmd.send_cmd(dut.name, 'show version', max_wait=10, interval=2)[0].return_text
            image_version = re.findall(r"IMG:\s+(\d+\.\d+\.\d+\.\d+)", output_cmd)[0]
            print(f"Initial image version on device is {image_version}")

            self.xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(network_policy_name)

            time.sleep(3)

            sw_name_from_cli = self.localsuiteudks.get_switch_model_name(dut)

            sw_name_from_cli_new = sw_name_from_cli

            sw_name_from_cli_new = sw_name_from_cli_new[:-1]

            sw_name_final = "Switch Engine " + sw_name_from_cli_new

            print("The final switch name is: ", sw_name_final)

            assert self.localsuiteudks.add_upgrade_firmware_specific_version_sw_template_adv_settings_tab(
                network_policy_name,
                sw_name_final,
                device_template_name,
                image_version) == 1, f"Failed to create policy with template: {dut}"

            self.xiq.xflowscommonNavigator.navigate_to_devices()

            time.sleep(5)
            assert self.xiq.xflowscommonDevices.onboard_device(device_serial=dut.serial,
                                                               device_make=dut.cli_type, device_mac=dut.mac,
                                                               device_os=dut.cli_type, location=location,
                                                               policy_name=network_policy_name) == 1, \
                                                                f"Failed to onboard this dut to XiQ: {dut}"

            status_before = self.xiq.xflowscommonDevices.get_device_updated_status(device_serial=dut.serial)

            self.localsuiteudks.configure_iqagent(dut, xiq_ip_address)

            time.sleep(5)
            self.xiq.xflowscommonDevices.refresh_devices_page()

            # Checking for the update column to reflect the firmware update status
            self.localsuiteudks.check_update_column(dut.serial, status_before)

            assert self.xiq.xflowscommonDevices.wait_until_device_online(dut.serial) == 1, \
                f"Device {dut} didn't get online"
            assert self.xiq.xflowscommonDevices.wait_until_device_managed(dut.serial) == 1, \
                f"Device {dut} didn't get in MANAGED state"

            res = self.localsuiteudks.get_device_status_debug(dut, 'config audit mismatch')
            # res = self.xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)
            assert res == 'config audit mismatch', \
                f"The EXOS device did not come up successfully in the XIQ; Device: {dut}"


        finally:
            self.xiq.xflowscommonNavigator.navigate_to_devices()

            try:
                self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
                self.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy_name)
                self.xiq.xflowsconfigureCommonObjects.delete_switch_template(device_template_name)
            except Exception as exc:
                print(exc)
