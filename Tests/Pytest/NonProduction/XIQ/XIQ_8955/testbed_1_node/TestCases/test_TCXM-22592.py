import pytest
import string
import random

from Tests.Pytest.NonProduction.XIQ.XIQ_8955.testbed_1_node.Resources.SuiteUdks import dut_model_edit
from Tests.Pytest.NonProduction.XIQ.XIQ_8955.testbed_1_node.Resources.testcase_base import XIQBase
from pytest_testconfig import config


class TCXM22592Tests(XIQBase):
    @pytest.mark.development
    @pytest.mark.xim_tcxm_22591
    @pytest.mark.xim_tcxm_22592
    @pytest.mark.p1
    def test_tcxm_22592(self, onboard_location):
        """
        Author          :   Dennis-Mircea Ciupitu (id: dciupitu)
        Description     :
        TCXM-22591      -   Verify that "Reboot and revert Extreme Networks switch configuration if IQAgent is
                            unresponsive after configuration update" checkbox from Advanced settings TAB within template
                            under Upload configuration automatically (when enabled) is present and disabled by default.
        TCXM-22592      -   Verify that if the upload config toggle is turned off, the "Reboot and revert Extreme
                            Networks switch configuration if IQAgent is unresponsive after configuration update"
                            checkbox is not present.
        Prerequisites:      None
        Steps Description:
        1.                  Create a Network Policy with specific EXOS device template.
        2.                  Go to Device Template TAB.
        3.                  Select an EXOS switch template.
        4.                  Verify that Advanced Settings TAB is present in Configuration Menu.
        5.                  Click on Advanced Settings TAB.
        6.                  Verify that  "Upload configuration automatically" is present in Advanced Settings TAB.
        7.                  Verify that the Toggle for "Upload configuration automatically" is OFF by default.
        -----------------------------------------------------------------------------------------------------
        8.                  Verify that the Toggle for "Upload configuration automatically" is not present.
        9.                  Onboard the EXOS device and assign the previously created Network Policy during onboarding.
        """
        self.executionHelper.testSkipCheck()

        # Variables definitions
        self.cfg['${TEST_NAME}'] = 'test_tcxm_22592_run'
        dut = self.tb.dut1
        location = onboard_location
        xiq_ip_address = config['sw_connection_host']
        sw_model_template = dut_model_edit(dut.model)

        # Create random network policy & switch template names
        pool = list(string.ascii_letters) + list(string.digits)
        network_policy_name = f"policy_{''.join(random.sample(pool, k=4))}"
        device_template_name = f"template_{''.join(random.sample(pool, k=4))}"

        try:
            assert self.localSuiteUdks.disable_iqagent(dut) == 1, "Failed to disable IQAgent"

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

            assert self.localSuiteUdks.verify_upload_config_auto_button() == 1, \
                "Failed to verify Upload configuration automatically button"

            assert self.localSuiteUdks.verify_enable_auto_revert_option() == -1, \
                "Failed to verify Enable auto revert button"

            assert switch_template.save_template() == 1, "Failed to save the template"

            assert self.xiq.xflowscommonDevices.onboard_device(device_serial=dut.serial,
                                                               device_make=dut.cli_type,
                                                               device_mac=dut.mac,
                                                               device_os=dut.cli_type,
                                                               location=location,
                                                               policy_name=network_policy_name) == 1, \
                f"Failed to onboard this dut to XIQ: {dut}"

            assert self.localSuiteUdks.configure_iqagent(dut, xiq_ip_address) == 1, "Failed to configure IQAgent"

            assert self.xiq.xflowscommonDevices.wait_until_device_online(dut.serial) == 1, \
                f"Device {dut} didn't get online"

            assert self.xiq.xflowscommonDevices.wait_until_device_managed(dut.serial) == 1, \
                f"Device {dut} didn't get in MANAGED state"

            assert self.xiq.xflowscommonDevices.device_update_progress(device_serial=dut.serial) != -1, \
                "Failed to push the configuration to the device"

            res = self.xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)
            assert res == 'config audit mismatch', \
                f"The EXOS device did not come up successfully in the XIQ; Device: {dut}"

        finally:
            self.cfg['${TEST_NAME}'] = 'test_tcxm_22592_teardown'

            try:
                self.xiq.xflowscommonNavigator.navigate_to_devices()
                self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
                self.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy_name)
                self.xiq.xflowsconfigureCommonObjects.delete_switch_template(device_template_name)
            except Exception as exc:
                self.utils.print_info(exc)
