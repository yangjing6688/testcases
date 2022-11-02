import pytest
import time
import string
import random

from Tests.Pytest.NonProduction.XIQ.XIQ_1365.testbed_1_node.Resources.testcase_base import xiqBase
from pytest_testconfig import config


class TCXM20579Tests(xiqBase):

    @pytest.mark.development
    @pytest.mark.xim_tcxm_20579
    @pytest.mark.p1
    def test_tcxm_20579(self, onboarding_location):
        """
        Author        :    sraescu
        Description   :    Verify that Toggle for "Upload configuration automatically" is present and off by default.
        Preconditions:     none

        Step               Step Description

        1.                  Create a network policy
        2.                  In Device Template TAB select an EXOS switch template and check if Advanced Settings TAB is
                            present in Configuration Menu
        3.                  Click on Advanced Settings TAB
        4.                  Check if "Upload configuration automatically" button is OFF by default and switch it to ON
                            then click on Save button
        5.                  Onboard an EXOS device and attach the network policy during onboarding then check if the
                            device has been onboarded and the configuration has been automatically pushed
        """
        self.executionHelper.testSkipCheck()

        self.cfg['${test_name}'] = 'test1_tcxm_20579'
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

            self.localsuiteudks.add_sw_template_adv_settings_tab_tcxm_20579(network_policy_name, sw_name_final, device_template_name)

            # Change STP forward delay value; this change will be used to check if config push has been successfuly done
            xiq_fw_delay = self.localsuiteudks.select_sw_template_device_config_forw_delay(network_policy_name,
                                                                                        device_template_name)
            print(f"STP forward delay has been configured in device template: {xiq_fw_delay}")

            self.xiq.xflowscommonNavigator.navigate_to_devices()

            time.sleep(5)
            assert self.xiq.xflowscommonDevices.onboard_device(device_serial=dut.serial,
                                                               device_make=dut.cli_type, device_mac=dut.mac,
                                                               device_os=dut.cli_type, location=location,
                                                               policy_name=network_policy_name) == 1, \
                                                               f"Failed to onboard this dut to XiQ: {dut}"

            self.xiq.xflowscommonDevices.refresh_devices_page()

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

            # res = self.xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)
            res = self.localsuiteudks.get_device_status_debug(dut, 'green')
            assert res == 'green', f"The EXOS device did not come up successfully in the XIQ; Device: {dut}"

            # Get the STP forward delay value configured on device after config push
            dev_fw_delay = self.localsuiteudks.get_nw_templ_device_config_forward_delay(dut)
            print(f"STP forward delay value configured on device after config push is: {dev_fw_delay}")

            assert dev_fw_delay == xiq_fw_delay, f"Upload configuration automatically failed, STP forward delay value " \
                                                 f"configured on XIQ is different: {xiq_fw_delay}"

        finally:
            delay_xiq = self.localsuiteudks.set_nw_templ_device_config_forward_delay(dut)
            print(f"STP forward delay default value has been restored: {delay_xiq}")

            self.xiq.xflowscommonNavigator.navigate_to_devices()
            try:
                self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
                self.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy_name)
                self.xiq.xflowsconfigureCommonObjects.delete_switch_template(device_template_name)
            except Exception as exc:
                print(exc)
