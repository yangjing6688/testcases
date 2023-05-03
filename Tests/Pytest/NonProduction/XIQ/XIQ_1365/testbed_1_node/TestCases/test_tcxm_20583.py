import re
import time
import pytest
import string
import random

from Tests.Pytest.NonProduction.XIQ.XIQ_1365.testbed_1_node.Resources.testcase_base import xiqBase
from pytest_testconfig import config


class TCXM20583Tests(xiqBase):

    @pytest.mark.development
    @pytest.mark.xim_tcxm_20583
    @pytest.mark.p1
    def test_tcxm_20583(self, onboarding_location):
        """
        Author        :     dbadea
        Description   :     Verify that Option for "Upgrade to the specific device firmware version" is present.
        Preconditions :     Current device firmware version and at least one more additional firmware version should be
                            present on the AIO or Cloud environment

        Step               Step Description

        1.  Create a network policy
        2.  In Device Template TAB select an EXOS switch template and check Advanced Settings TAB is present in
            Configuration Menu
        3.  Click on Advanced Settings TAB
        4.  Select "Upgrade to the specific device firmware version" and also "Upload configuration automatically" and
            click Save.
        5.  Check that the firmware selected to upgrade is the same with the firmware that is already on DUT
        6.  Onboard the DUT using the network policy configured.
        7.  Check that upgrade is not triggered since the image on the DUT is the same as the one selected for upgrade.
        """
        self.executionHelper.testSkipCheck()

        self.cfg['${test_name}'] = 'test1_tcxm_20583'
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

            assert self.localsuiteudks.add_upgrade_firmware_specific_version_and_upload_config_auto_sw_template_adv_settings_tab(
                                                                                                                    network_policy_name,
                                                                                                                    sw_name_final,
                                                                                                                    device_template_name,
                                                                                                                    image_version,
                                                                                                                    "test_tcxm_20583") == 1, f"Failed to create switch template for : {dut}"

            self.xiq.xflowscommonNavigator.navigate_to_devices()

            time.sleep(5)
            assert self.xiq.xflowscommonDevices.onboard_device(device_serial=dut.serial,
                                                               device_make=dut.cli_type, device_mac=dut.mac,
                                                               device_os=dut.cli_type, location=location,
                                                               policy_name=network_policy_name) == 1, \
                                                                f"Failed to onboard this dut to XiQ: {dut}"

            self.xiq.xflowscommonDevices.refresh_devices_page()

            status_before = self.xiq.xflowscommonDevices.get_device_updated_status(device_serial=dut.serial)

            self.localsuiteudks.configure_iqagent(dut, xiq_ip_address)

            time.sleep(5)
            self.xiq.xflowscommonDevices.refresh_devices_page()

            self.localsuiteudks.check_update_column(dut.serial, status_before)

            assert self.xiq.xflowscommonDevices.wait_until_device_online(dut.serial) == 1, \
                f"Device {dut} didn't get online"
            assert self.xiq.xflowscommonDevices.wait_until_device_managed(dut.serial) == 1, \
                f"Device {dut} didn't get in MANAGED state"

            self.xiq.xflowscommonDevices.refresh_devices_page()
            time.sleep(5)

            # res = self.xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)
            res = self.localsuiteudks.get_device_status_debug(dut, 'green')
            assert res == 'green', f"The EXOS device did not come up successfully in the XIQ; Device: {dut}"

            event_number = self.localsuiteudks.get_last_event_from_device360(dut)
            print("event_number = " + str(event_number))
            assert event_number == 1, f"The firmware download event was also triggered in addition to config push"

        finally:
            self.xiq.xflowscommonNavigator.navigate_to_devices()

            try:
                self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
                self.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy_name)
                self.xiq.xflowsconfigureCommonObjects.delete_switch_template(device_template_name)
            except Exception as exc:
                print(exc)
