import time

import pytest

from ..Resources.testcase_base import xiqBase


class TCXM20651Tests(xiqBase):
    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.xim_tcxm_20651
    @pytest.mark.p1
    def test_switch_template(self, onboarded_dut, network_policy, template_stack):
        """
        Author        : abolojan
        Date          : 6/6/2022
        Description   : Verify that Configuration Audit reflects the changes when VIM ports are added to the LACP using Aggregate Ports button from Switch Template.
        Steps         : Step    Description
                         0      Use devices with 4 ports VIM module (10 or 25 G ports) and aggregate them according to tests requirements.
                                Supported devices: 5520-24T, 5520-24W, 5520-48T, 5520-48W, 5520-12MW-36W, 5520-24X, 5520-48SE, 5520-VIM-4X, 5520-VIM-4XE, 5520-VIM-4YE.
                                Tested EXOS devices: 5520-48SE with 5520-VIM-4XE, 5520-24W with 5520-VIM-4X, 5520-24T with 5520-VIM-4YE.
                         1      Onboard the EXOS 5520 stack with only one VIM module.
                         2      Create a Network Policy with specific 5520 template.
                         3      Assign the previously created Network Policy to the device and update the device.
                         4      Using the Aggregate Ports button from Switch Template -> Port Configuration aggregate 2 VIM ports.
                         5      Check Devices -> Configuration Audit button status and Delta CLI.
                         6      Update the device, check the results in CLI and check the number of LACP ports in Switch Template -> Port Configuration table.
                         7      Using the Switch Template -> Port Configuration remove all VIM ports from the LACP.
                         8      Check Devices -> Configuration Audit button status and Delta CLI.
                         9      Update the device, check the results in CLI and check the number of LACP ports in Switch Template -> Port Configuration table.
        """

        self.executionHelper.testSkipCheck()
        dut = onboarded_dut
        ports_aggregated = False
        ports_aggregated_device_updated = False
        ports_not_aggregated = False
        ports_not_aggregated_device_updated = False

        try:
            # check the configuration audit button
            configuration_audit_status = self.xiq.xflowsmanageDevices.get_device_configuration_audit_status(device_mac=dut.mac)
            print(f"Configuration audit at the beginning of the test: {configuration_audit_status}")

            if configuration_audit_status == 'audit mismatch':
                # update the device (in order to apply the policy for the first time)
                self.xiq.xflowsmanageDevices.update_switch_policy_and_configuration(mac=onboarded_dut.mac)

            # aggregate 2 VIM ports
            ports = self.suite_udk.aggregate_vim_ports(nw_policy=network_policy, sw_template=template_stack)
            self.xiq.xflowsmanageDevices.navigator.navigate_to_devices()
            time.sleep(60)
            self.xiq.xflowsmanageDevices.refresh_devices_page()

            ports_aggregated = True

            # check the configuration audit button
            configuration_audit_status = self.xiq.xflowsmanageDevices.get_device_configuration_audit_status(device_mac=dut.mac)
            print(f"Configuration audit button after LAG creation: {configuration_audit_status}")

            if configuration_audit_status != 'audit mismatch':
                pytest.fail(f"Configuration audit status is {configuration_audit_status}")

            # check delta CLI
            delta_cli = self.xiq.xflowsmanageDeviceConfig.check_config_audit_delta_match(mac=onboarded_dut.mac)
            print(f" Delta CLI after LAG creation: {delta_cli}")

            expected_delta_cli = [f"enable sharing {ports[0]} grouping {ports[0]},{ports[1]} lacp",
                                  f"enable sharing {ports[0]} grouping {ports[1]},{ports[0]} lacp"]
            if expected_delta_cli[0] not in delta_cli and expected_delta_cli[1] not in delta_cli:
                pytest.fail(f'Delta CLI mismatch, expected: {expected_delta_cli}, found: {delta_cli}')

            # update the device
            self.xiq.xflowsmanageDevices.update_switch_policy_and_configuration(mac=dut.mac)

            ports_aggregated_device_updated = True

            # check the results in CLI
            result = ""
            try:
                self.network_manager.connect_to_network_element_name(onboarded_dut.name)
                output = self.devCmd.send_cmd(onboarded_dut.name, 'show configuration | i sharing', max_wait=10, interval=2)
                result = output[0].return_text
            finally:
                self.network_manager.close_connection_to_network_element(onboarded_dut.name)

            expected_result = f'enable sharing {ports[0]} grouping {ports[0]}-{ports[1].split(":")[1]}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")

            # remove all VIM ports from LACP
            self.suite_udk.remove_vim_ports_from_lag(nw_policy=network_policy, sw_template=template_stack)
            self.xiq.xflowsmanageDevices.navigator.navigate_to_devices()
            time.sleep(60)
            self.xiq.xflowsmanageDevices.refresh_devices_page()

            ports_not_aggregated = True

            # check the configuration audit button
            configuration_audit_status = self.xiq.xflowsmanageDevices.get_device_configuration_audit_status(device_mac=dut.mac)
            print(f"Configuration audit after LAG deletion: {configuration_audit_status}")

            if configuration_audit_status != 'audit mismatch':
                pytest.fail(f"Configuration audit status is {configuration_audit_status}")

            # check delta CLI
            delta_cli = self.xiq.xflowsmanageDeviceConfig.check_config_audit_delta_match(mac=dut.mac)
            print(f"Delta CLI after LAG deletion: {delta_cli}")

            expected_delta_cli = f"disable sharing {ports[0]}"
            if expected_delta_cli not in delta_cli:
                pytest.fail(f'Delta CLI mismatch, expected: {expected_delta_cli}, found: {delta_cli}')

            # update the device
            self.xiq.xflowsmanageDevices.update_switch_policy_and_configuration(mac=dut.mac)

            ports_not_aggregated_device_updated = True

            # check the results in CLI
            result = ""
            try:
                self.network_manager.connect_to_network_element_name(onboarded_dut.name)
                output = self.devCmd.send_cmd(onboarded_dut.name, 'show configuration | i sharing', max_wait=10, interval=2)
                result = output[0].return_text
            finally:
                self.network_manager.close_connection_to_network_element(onboarded_dut.name)

            if str(ports[0]) in result:
                pytest.fail(f"The LAG is still configured, CLI result: {result}")

            # check the number of LACP ports in switch template -> port configuration
            self.switch_template.select_sw_template(nw_policy=network_policy, sw_template=template_stack)
            time.sleep(2)

            if self.sw_template_web_elements.get_sw_template_port_configuration_tab() is None:
                self.auto_actions.click(self.sw_template_web_elements.get_template_link(template=template_stack))

            time.sleep(2)

            self.switch_template.go_to_port_configuration()
            time.sleep(2)

            labels = self.sw_template_web_elements.get_lag_span(lag=ports[0])
            time.sleep(2)

            if labels is not None:
                pytest.fail("Invalid number of LACP ports in the switch template -> port configuration table")
        except Exception as e:
            print(f"Error:{e}")
            if ports_not_aggregated:
                if not ports_not_aggregated_device_updated:
                    # update the device
                    self.xiq.xflowsmanageDevices.update_switch_policy_and_configuration(mac=onboarded_dut.mac)
            elif ports_aggregated:
                # remove all VIM ports from LACP
                self.suite_udk.remove_vim_ports_from_lag(nw_policy=network_policy, sw_template=template_stack)
                self.xiq.xflowsmanageDevices.navigator.navigate_to_devices()
                time.sleep(60)
                self.xiq.xflowsmanageDevices.refresh_devices_page()

                if ports_aggregated_device_updated:
                    # update the device
                    self.xiq.xflowsmanageDevices.update_switch_policy_and_configuration(mac=dut.mac)
        finally:
            self.xiq.xflowscommonNavigator.navigate_to_devices()
