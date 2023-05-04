import pytest
import time
import datetime
import string
import random

from Tests.Pytest.NonProduction.XIQ.XIQ_1365.testbed_1_node.Resources.testcase_base import xiqBase
from pytest_testconfig import config


class TCXM20580Tests(xiqBase):

    @pytest.mark.development
    @pytest.mark.xim_tcxm_20580
    @pytest.mark.p1
    def test_tcxm_20580(self, onboarding_location):
        """
        Author        :    tpodar
        Description   :    Check that if the DUT is already onboarded and has a network policy, changing "Upload
                           configuration automatically" or "Upgrade device firmware upon device firmware authentication"
                           from off to on will not have any effect.
        Preconditions:     None

        Step               Step Description

        1.                 Create a network policy
        2.                 Onboard an EXOS device and attach the policy to it
        3.                 In Device Template TAB select an EXOS switch template and check Advanced Settings TAB is
                           present in Configuration Menu
        4.                 Click on Advanced Settings TAB
        5.                 Turn on the toggle for "Upload configuration automatically" and "Upgrade device firmware
                           upon device firmware authentication"
        6.                 Check that nothing happens since the expected behaviour is that the DUT uploads automatically
                           the firmware and the configuration only if the toggle for these options are already on before
                           the device is onboarded and the network policy applied.
        """
        self.executionHelper.testSkipCheck()

        self.cfg['${test_name}'] = 'test1_tcxm_20580'
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

            self.localsuiteudks.add_sw_template_adv_settings_tab_tcxm_20580(network_policy_name, sw_name_final,
                                                                 device_template_name)

            self.xiq.xflowscommonNavigator.navigate_to_devices()

            time.sleep(5)
            assert self.xiq.xflowscommonDevices.onboard_device(device_serial=dut.serial,
                                                               device_make=dut.cli_type, device_mac=dut.mac,
                                                               device_os=dut.cli_type, location=location,
                                                               policy_name=network_policy_name) == 1, \
                                                                f"Failed to onboard this dut to XiQ: {dut}"

            self.xiq.xflowscommonDevices.refresh_devices_page()

            self.localsuiteudks.configure_iqagent(dut, xiq_ip_address)

            print("Get managed value from device")
            managed_field = self.xiq.xflowscommonDevices.get_device_row_values(dut.serial, 'MANAGED')
            managed_final = str(managed_field['MANAGED'])
            print("device managed field is ", managed_final)

            max_wait = 180
            count = 0
            while "Managed" not in managed_final and count < max_wait:
                time.sleep(10)
                count += 10
                self.xiq.xflowscommonDevices.refresh_devices_page()
                managed_field = self.xiq.xflowscommonDevices.get_device_row_values(dut.serial, 'MANAGED')
                managed_final = str(managed_field['MANAGED'])

            # Change STP forward delay value; this change will be used to check if config push has been successfuly done
            xiq_fw_delay = self.localsuiteudks.select_sw_template_device_config_forw_delay(network_policy_name,
                                                                                               device_template_name, dut.cli_type)
            print(f"STP forward delay has been configured in device template: {xiq_fw_delay}")

            self.localsuiteudks.press_upload_config_and_upgr_firm_button(network_policy_name,device_template_name)

            self.xiq.xflowscommonNavigator.navigate_to_devices()

            status_after = self.localsuiteudks.get_device_updated_status(device_serial=dut.serial)
            count = 0
            max_wait = 900
            current_date = datetime.datetime.now()
            update_text = str(current_date).split()[0]
            while update_text not in status_after and count < max_wait:
                time.sleep(10)
                count += 10
                status_after = self.localsuiteudks.get_device_updated_status(device_serial=dut.serial)
                print(
                    f"\nINFO \t Time elapsed in the update column to reflect the configuration push is '{count} seconds'\n")
                if ("Failed" in status_after) or ("failed" in status_after):
                    pytest.fail("Device Update Failed for the device with serial {}".format(dut.serial))

            assert self.xiq.xflowscommonDevices.wait_until_device_online(dut.serial) == 1, \
                f"Device {dut} didn't get online"
            assert self.xiq.xflowscommonDevices.wait_until_device_managed(dut.serial) == 1, \
                f"Device {dut} didn't get in MANAGED state"

            res = self.xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)

            # Get the STP forward delay value configured on device after config push
            dev_fw_delay = self.localsuiteudks.get_nw_templ_device_config_forward_delay(dut)
            print(f"STP forward delay value configured on device after config push is: {dev_fw_delay}")

            assert dev_fw_delay != xiq_fw_delay, f"Upload configuration automatically was triggered, STP forward delay value " \
                                                 f"configured on XIQ is equal: {xiq_fw_delay}"

            event_number = self.localsuiteudks.get_last_event_from_device360(dut)
            print(event_number)
            assert event_number == 0, "Firmware update and Config push were not triggered"

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


