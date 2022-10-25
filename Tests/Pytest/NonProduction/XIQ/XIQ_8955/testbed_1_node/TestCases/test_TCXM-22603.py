import pytest
import string
import random

from Tests.Pytest.NonProduction.XIQ.XIQ_8955.testbed_1_node.Resources.SuiteUdks import dut_model_edit
from Tests.Pytest.NonProduction.XIQ.XIQ_8955.testbed_1_node.Resources.testcase_base import XIQBase
from pytest_testconfig import config

event = "IQagent lost connectivity during configuration update, switch rebooted, and previous configuration has been " \
        "loaded"
failure_message = "*IQAgent unresponsive after configuration update. The device was rebooted and reverted to " \
                  "previous configuration.Review configuration delta that resulted in IQAgent connectivity loss " \
                  "and make necessary changes."


class TCXM22603Tests(XIQBase):
    @pytest.mark.development
    @pytest.mark.xim_tcxm_22603
    @pytest.mark.p1
    def test_tcxm_22603(self, onboard_location):
        """
        Author          :   Dennis-Mircea Ciupitu (id: dciupitu)
        Description     :   Verify that  the rebooting process is triggered if the IQAgent is unresponsive during the
                            upload configuration process (the policy isn't assigned at onboarding). The DUT transitions
                            from unmanaged to managed.
        Prerequisites   :   None
        Steps Description:
        1.                  Go to Global Settings Section.
        2.                  Go to the VIQ Management tab.
        3.                  Turn ON the supplemental cli button.
        4.                  Create a Network Policy with specific EXOS device template.
        5.                  Go to Device Template TAB.
        6.                  Select an EXOS switch template.
        7.                  Verify that Advanced Settings TAB is present in Configuration Menu.
        8.                  Click on Advanced Settings TAB.
        9.                  Verify that  "Upload configuration automatically" is present in Advanced Settings TAB.
        10.                 Verify that the Toggle for "Upload configuration automatically" is OFF by default.
        11.                 Verify that the Toggle for "Upload configuration automatically" can be switched to ON.
        12.                 Verify that "Reboot and revert Extreme Networks switch configuration if IQAgent is
                            unresponsive after configuration update" checkbox is visible.
        13.                 Verify that "Reboot and revert Extreme Networks switch configuration if IQAgent is
                            unresponsive after configuration update" checkbox is disabled by default.
        14.                 Select the specified checkbox.
        15.                 Turn ON the supplemental cli button from advanced settings tab.
        16.                 Enter "unconfigure Mgmt ipaddress" command.
        17                  Click Save button for the template.
        18.                 Click yes on the new opened box.
        19.                 Onboard the EXOS device and assign the previously created Network Policy during onboarding.
        20.                 Once the device is onboarded and managed make the device as unmanaged and assign the policy
                            template.
        21.                 Now move the device to managed and ensure  the  config upload is triggered for the device.
        22.                 Wait for approx. 15 minutes until updated columns displays the update device failed message
                            and the device is still connected.
        23.                 Check that by hovering the error message link the "IQAgent unresponsive after configuration
                            update. The device was rebooted and reverted to the previous configuration" message is
                            displayed.
        24.                 Verify that all appropriate alarms/events should be triggered
        25.                 Check that the audit icon remains orange and no configuration update was made
        """
        self.executionHelper.testSkipCheck()

        # Variables definitions
        self.cfg['${TEST_NAME}'] = 'test_tcxm_22603_run'
        dut = self.tb.dut1
        location = onboard_location
        xiq_ip_address = config['sw_connection_host']
        dut_ip = self.localSuiteUdks.get_ip(dut)
        sw_model_template = dut_model_edit(dut.model)

        # Create random network policy & switch template names
        pool = list(string.ascii_letters) + list(string.digits)
        network_policy_name = f"policy_{''.join(random.sample(pool, k=4))}"
        device_template_name = f"template_{''.join(random.sample(pool, k=4))}"
        supplemental_cli_name = f"scli_{''.join(random.sample(pool, k=4))}"

        try:
            assert self.localSuiteUdks.disable_iqagent(dut) == 1, "Failed to disable IQAgent"

            assert self.xiq.xflowsglobalsettingsGlobalSetting.get_supplemental_cli_option("enable") == 1, \
                "Failed to enable Supplemental CLI in Global Settings"

            network_policy = self.xiq.xflowsconfigureNetworkPolicy
            assert network_policy.create_switching_routing_network_policy(network_policy_name) == 1, \
                "Failed to create Switching and Routing network policy"

            switch_template = self.xiq.xflowsconfigureSwitchTemplate
            assert switch_template.add_sw_template(network_policy_name,
                                                   sw_model_template,
                                                   device_template_name) == 1, \
                f"Failed to add switch template with model: {sw_model_template}"

            assert switch_template.select_adv_settings_tab(network_policy_name, device_template_name) == 1, \
                "Failed to open Advanced Settings tab"

            assert self.localSuiteUdks.set_upload_config_auto_button() == 1, \
                "Failed to set Upload configuration automatically button"

            assert self.localSuiteUdks.set_enable_auto_revert_option() == 1, \
                "Failed to set Enable auto revert button"

            if dut.platform == '5320':
                commands = f"configure iproute add default {dut_ip} vr vr-default"
            else:
                commands = f"configure iproute add default {dut_ip} vr vr-mgmt"

            assert switch_template.add_supplemental_cli_into_template(network_policy_name, device_template_name,
                                                                      supplemental_cli_name, commands,
                                                                      navigate_to_scli=False,
                                                                      save_template=False) == 1, \
                "Failed to configure Supplemental CLI profile"

            assert self.localSuiteUdks.save_template_with_popup() == 1, "Failed to save the template"

            assert self.xiq.xflowscommonDevices.onboard_device(device_serial=dut.serial,
                                                               device_make=dut.cli_type,
                                                               device_mac=dut.mac,
                                                               device_os=dut.cli_type,
                                                               location=location) == 1, \
                f"Failed to onboard this dut to XIQ: {dut}"

            assert self.localSuiteUdks.configure_iqagent(dut, xiq_ip_address) == 1, "Failed to configure IQAgent"

            assert self.xiq.xflowscommonDevices.wait_until_device_online(dut.serial) == 1, \
                f"Device {dut} didn't get online"

            assert self.xiq.xflowscommonDevices.wait_until_device_managed(dut.serial) == 1, \
                f"Device {dut} didn't get in MANAGED state"

            assert self.xiq.xflowscommonDevices.change_manage_device_status(manage_type="UNMANAGE",
                                                                            device_serial=dut.serial) == 1, \
                f"Failed to change Management status of {dut} in UNMANAGE"

            assert self.xiq.xflowscommonDevices.assign_network_policy_to_switch(network_policy_name, dut.serial,
                                                                                update_device=False) == 1, \
                f"Failed to assign network policy to {dut}"

            assert self.xiq.xflowscommonDevices.change_manage_device_status(manage_type="MANAGE",
                                                                            device_serial=dut.serial) == 1, \
                f"Failed to change Management status of {dut} in MANAGE"

            assert self.localSuiteUdks.check_update_column_by_failure_message(dut.serial, failure_message) == 1, \
                "Failed to obtain the expected Device Updated Failed message"

            assert self.xiq.xflowsmanageDevice360.get_event_from_device360(dut, event) == 1, \
                "The IQAgent unresponsive event was not triggered!"

            self.xiq.xflowscommonNavigator.navigate_to_devices()

            res = self.xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)
            assert res == 'config audit mismatch', \
                f"The EXOS device did not come up successfully in the XIQ; Device: {dut}"

        finally:
            self.cfg['${TEST_NAME}'] = 'test_tcxm_22603_teardown'

            try:
                self.xiq.xflowscommonNavigator.navigate_to_devices()
                self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
                self.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy_name)
                self.xiq.xflowsconfigureCommonObjects.delete_switch_template(device_template_name)
                self.xiq.xflowsconfigureCommonObjects.delete_supplemental_cli_profile(supplemental_cli_name)
            except Exception as exc:
                self.utils.print_info(exc)
