import pytest
import time
import string
import random

from Tests.Pytest.NonProduction.XIQ.XIQ_1365.testbed_1_node.Resources.testcase_base import xiqBase
from pytest_testconfig import config


class TCXM20577Tests(xiqBase):

    @pytest.mark.development
    @pytest.mark.xim_tcxm_20577
    @pytest.mark.p1
    def test_tcxm_20577(self, onboarding_location):
        """
        Author        :     dbadea
        Description   :     Verify that Option  for "Upgrade firmware to the latest version" is present.
        Preconditions :     The device should have a different firmware version than the latest firmware;
                            The latest firmware version and current device firmware version should be present on the AIO
                            or Cloud environment

        Step               Step Description

        1.                   Create a network policy
        2.                   In Device Template TAB select an EXOS switch template and check Advanced Settings TAB is
                             present in Configuration Menu
        3.                   Click on Advanced Settings TAB
        4.                   There is a option for "Upgrade firmware to the latest version" and can be selected.
                             Then click Save button.
        5.                   Check that after a device is onboarded and network policy is set, firmware is updated to
                             the latest version.
        """
        self.executionHelper.testSkipCheck()

        self.cfg['${test_name}'] = 'test1_tcxm_20577'
        dut = self.tb.dut1

        pool = list(string.ascii_letters) + list(string.digits)
        network_policy_name = f"policy_XIQ1365_{''.join(random.sample(pool, k=4))}"
        device_template_name = f"template_XIQ1365_{''.join(random.sample(pool, k=4))}"

        location = onboarding_location
        xiq_ip_address = config['sw_connection_host']

        try:
            self.devCmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')

            self.xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(network_policy_name)

            time.sleep(3)

            sw_name_from_cli = self.localsuiteudks.get_switch_model_name(dut)

            sw_name_from_cli_new = sw_name_from_cli

            sw_name_from_cli_new = sw_name_from_cli_new[:-1]

            sw_name_final = "Switch Engine " + sw_name_from_cli_new

            print("The final switch name is: ", sw_name_final)

            self.localsuiteudks.add_upgrade_firmware_latest_version_sw_template_adv_settings_tab(network_policy_name,
                                                                                                 sw_name_final,
                                                                                                 device_template_name)

            self.xiq.xflowscommonNavigator.navigate_to_devices()

            time.sleep(5)
            assert self.xiq.xflowscommonDevices.onboard_device(device_serial=dut.serial,
                                                               device_make=dut.cli_type, device_mac=dut.mac,
                                                               device_os=dut.cli_type, location=location,
                                                               policy_name=network_policy_name) == 1, \
                                                                f"Failed to onboard this dut to XiQ: {dut}"

            status_before = self.xiq.xflowscommonDevices.get_device_updated_status(device_mac=dut.serial)

            self.localsuiteudks.configure_iqagent(dut, xiq_ip_address)

            time.sleep(5)
            self.xiq.xflowscommonDevices.refresh_devices_page()

            # Checking for the update column to reflect the firmware update status
            self.localsuiteudks.check_update_column(dut.serial, status_before)

            assert self.xiq.xflowscommonDevices.wait_until_device_online(dut.serial) == 1, \
                f"Device {dut} didn't get online"
            assert self.xiq.xflowscommonDevices.wait_until_device_managed(dut.serial) == 1, \
                f"Device {dut} didn't get in MANAGED state"

            self.xiq.xflowscommonDevices.refresh_devices_page()
            time.sleep(15)

            print("Get os version from device")
            os_version = self.xiq.xflowscommonDevices.get_device_row_values(dut.mac, 'OS VERSION')
            nos_version = str(os_version['OS VERSION'])
            print("device os_version = " + nos_version)

            latest_os_version = self.localsuiteudks.get_latest_version_from_device_update(dut.serial)
            print("device latest_os_version = " + latest_os_version)

            assert (nos_version == latest_os_version and (not nos_version) is False),\
                f"OS version is different from latest version {dut}"

            # res = self.xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)
            res = self.localsuiteudks.get_device_status_debug(dut, 'config audit mismatch')
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
