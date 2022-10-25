import re
import time
import pytest
import string
import random

from Tests.Pytest.NonProduction.XIQ.XIQ_1365.testbed_1_node.Resources.testcase_base import xiqBase
from pytest_testconfig import config


class TCXM20589Tests(xiqBase):

    @pytest.mark.development
    @pytest.mark.xim_tcxm_20589
    @pytest.mark.p1
    def test_tcxm_20589(self, onboarding_location):
        """
        Author        :     dbadea
        Description   :     Check that the Upgrade firmware and Upload Configuration automatically functions are
                            triggered after DUT transitions from unmanaged to managed.
        Preconditions :     The device should have a different firmware version than the latest firmware;
                            The latest firmware version and current device firmware version should be present on the AIO
                            or Cloud environment

        Step    Description

        1.      Create a network policy.
        2.      In Device Template TAB select an EXOS switch template and check Advanced Settings TAB is present in
                Configuration Menu.
        3.      Click on Advanced Settings TAB.
        4.      Select "Upgrade firmware to the latest version" and also "Upload configuration automatically" and click
                Save.
        5.      Onboard the DUT without  assigning the network policy configured.
        6.      Once the device is onboarded and managed make the device as unmanaged and assign the policy template.
        7.      Now move the device to managed and ensure the firmware upgrade and config upload are triggered for the
                device.

        """
        self.executionHelper.testSkipCheck()

        self.cfg['${test_name}'] = 'test1_tcxm_20589'
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

            assert self.localsuiteudks.add_upgrade_firmware_latest_version_and_upload_config_auto_sw_template_adv_settings_tab(
                                                                                                                    network_policy_name,
                                                                                                                    sw_name_final,
                                                                                                                    device_template_name) == 1, f"Failed to create switch template for : {dut}"

            self.xiq.xflowscommonNavigator.navigate_to_devices()

            time.sleep(5)
            assert self.xiq.xflowscommonDevices.onboard_device(device_serial=dut.serial,
                                                               device_make=dut.cli_type, device_mac=dut.mac,
                                                               device_os=dut.cli_type, location=location,
                                                               policy_name=network_policy_name) == 1, \
                                                                f"Failed to onboard this dut to XiQ: {dut}"

            status_before = self.xiq.xflowscommonDevices.get_device_updated_status(device_mac=dut.serial)

            self.localsuiteudks.managed_unmanaged(dut.serial)
            time.sleep(5)

            self.localsuiteudks.configure_iqagent(dut, xiq_ip_address)

            self.xiq.xflowscommonDevices.refresh_devices_page()
            time.sleep(5)

            self.localsuiteudks.check_update_column(dut.serial, status_before)
            time.sleep(5)

            assert self.xiq.xflowscommonDevices.wait_until_device_online(dut.serial) == 1, \
                f"Device {dut} didn't get online"
            assert self.xiq.xflowscommonDevices.wait_until_device_managed(dut.serial) == 1, \
                f"Device {dut} didn't get in MANAGED state"

            self.xiq.xflowscommonDevices.refresh_devices_page()
            time.sleep(5)

            # res = self.xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)
            res = self.localsuiteudks.get_device_status_debug(dut, 'green')
            assert res == 'green', f"The EXOS device did not come up successfully in the XIQ; Device: {dut}"

            print("Get os version from device")
            os_version = self.xiq.xflowscommonDevices.get_device_row_values(dut.mac, 'OS VERSION')
            nos_version = str(os_version['OS VERSION'])
            print("device os_version = " + nos_version)

            latest_os_version = self.localsuiteudks.get_latest_version_from_device_update(dut.serial)
            print("device latest_os_version = " + latest_os_version)

            assert (nos_version == latest_os_version and (not nos_version) is False), \
                f"OS version is different from latest version {dut}"

            event_number = self.localsuiteudks.get_last_event_from_device360(dut)
            print("event_number = " + str(event_number))
            if image_version != latest_os_version:
                assert event_number == 2, f"The event firmware download or config push was not triggered"
            else:
                assert event_number == 1, "Config push event wasn't triggered"

        finally:
            self.xiq.xflowscommonNavigator.navigate_to_devices()

            try:
                self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
                self.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy_name)
                self.xiq.xflowsconfigureCommonObjects.delete_switch_template(device_template_name)
            except Exception as exc:
                print(exc)
