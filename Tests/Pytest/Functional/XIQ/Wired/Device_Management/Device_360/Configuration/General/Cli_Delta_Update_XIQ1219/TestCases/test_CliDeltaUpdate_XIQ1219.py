# Author        : Dragos Sofiea, Devi Ranganathan, Raluca Cionca
# Description   : This script run the below tests for CLI Delta Update feature according with XIQ-1219 story
# Testcases     : TCXM16515, TCXM16916, TCXM16916, TCXM16923, TCXM16915, TCXM16922, TCXM16917, TCXM16924
# Comments      : This test is applicable for exos-voss, exos_Stack

import pytest
import re
import time


class Xiq1219:
    
    config_file_name = "start"
    
    def configuration_setup(self, node, enter_switch_cli):

        with enter_switch_cli(node) as dev_cmd:
            if node.cli_type.lower() == "voss":
                dev_cmd.send_cmd(node.name, 'configure terminal', max_wait=10, interval=1)
                dev_cmd.send_cmd(node.name, 'save config')
                dev_cmd.send_cmd(node.name, 'save config file ' + self.config_file_name,
                                 confirmation_phrases='overwrite (y/n) ?', confirmation_args='yes')
            elif node.cli_type.lower() == "exos":
                dev_cmd.send_cmd(node.name, 'disable cli prompting', max_wait=10, interval=2)
                dev_cmd.send_cmd(node.name, 'save configuration primary', max_wait=30, interval=10)
                dev_cmd.send_cmd(node.name, f'save configuration {self.config_file_name}', max_wait=30, interval=10)

    def configuration_teardown(self, cli, node, reboot_device, open_spawn):        
        
        with open_spawn(node) as spawn:
            if node.cli_type.lower() == "voss":
                cli.send(spawn, f"configure terminal")
                cli.send(spawn, f"delete {self.config_file_name} -y")

            elif node.cli_type.lower() == "exos":
                cli.send(spawn, f"disable cli prompting")
                cli.send(spawn, f"use configuration primary")

        reboot_device([node])
        time.sleep(600)

    def verify_config_update(self, case, xiq, node, policy_name, cli, profile_scli):
        
        if case == "long_config":
            vlan_max = 2000 if node.cli_type.lower() == "exos" else 200
        elif case == "small_config":
            vlan_max = 200 if node.cli_type.lower() == "exos" else 50
        elif case == "cli_spans_many_minutes":
            vlan_max = 4000 if node.cli_type.lower() == "exos" else 20

        xiq.xflowsglobalsettingsGlobalSetting.get_supplemental_cli_option("enable")

        xiq.xflowsmanageDevice360.get_supplemental_cli_vlan(
            mac=node.mac, os=node.cli_type.lower(), profile_scli=profile_scli,
            option="create", vlan_min=2, vlan_max=vlan_max
        )
    
        spawn_debug = cli.enable_debug_mode_iqagent(node.ip, node.username, node.password, node.cli_type, disable_strict_host_key_checking=True)

        try:
            xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=policy_name, option="disable", device_mac=node.mac)
            xiq.xflowsmanageXiqVerifications.wait_for_logs_after_scli_configuration_update(os=node.cli_type, spawn=spawn_debug, mac=node.mac)
            time.sleep(15)
            xiq.xflowsmanageXiqVerifications.check_event(event="Download Config", mac=node.mac, configuration_event=True)
        finally:
            spawn_debug.close()

    def teardown_config_update(self, case, xiq, node, policy_name, onboarding_location, profile_scli):

        if case == "long_config":
            vlan_max = 2000 if node.cli_type.lower() == "exos" else 200
        elif case == "small_config":
            vlan_max = 200 if node.cli_type.lower() == "exos" else 50
        elif case == "cli_spans_many_minutes":
            vlan_max = 4000 if node.cli_type.lower() == "exos" else 20

        xiq.xflowsglobalsettingsGlobalSetting.get_supplemental_cli_option("enable")

        xiq.xflowsmanageDevice360.get_supplemental_cli_vlan(
            mac=node.mac, os=node.cli_type.lower(), option="delete", profile_scli=profile_scli,
            vlan_min=2, vlan_max=vlan_max)
    
        xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=policy_name, option="disable", device_mac=node.mac)
        xiq.xflowscommonDevices.check_device_update_status_by_using_mac(device_mac=node.mac)

        xiq.xflowscommonDevices.delete_device(device_mac=node.mac)

        time.sleep(10)
        xiq.xflowscommonDevices.onboard_device_quick({**node, "location": onboarding_location})
        time.sleep(60)
        xiq.xflowscommonDevices.wait_until_device_online(device_mac=node.mac)

        assert xiq.xflowsmanageDevices.assign_network_policy_to_switch_mac(
            policy_name=policy_name, mac=node.mac) == 1, \
            f"Couldn't assign policy {policy_name} to device '{node}' (node: '{node.name}')."
        
        xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=policy_name, option="disable", device_mac=node.mac)
        xiq.xflowscommonDevices.check_device_update_status_by_using_mac(device_mac=node.mac)

    def revert_node_to_default(self, xiq, node, policy_name, onboarding_location, open_spawn, cli, loaded_config):

        with open_spawn(node) as spawn:
            cli.configure_device_to_connect_to_cloud(
                node.cli_type, loaded_config['sw_connection_host'],
                spawn, vr=node.get("mgmt_vr", 'VR-Mgmt').upper(), retry_count=30
            )

        xiq.xflowscommonDevices.column_picker_select("Template", "Network Policy", "MAC Address")

        if xiq.xflowscommonDevices.search_device(device_mac=node.mac) == -1:
            xiq.xflowscommonDevices.onboard_device_quick({**node, "location": onboarding_location})
            time.sleep(60)
            xiq.xflowscommonDevices.wait_until_device_online(device_mac=node.mac)
   
        dev = xiq.xflowscommonDevices._get_row("device_mac", node.mac)
        if dev != -1:
            if not re.search(policy_name, dev.text):
                assert xiq.xflowsmanageDevices.assign_network_policy_to_switch_mac(policy_name=policy_name, mac=node.mac) == 1, \
                    f"Couldn't assign policy {policy_name} to device '{node}' (node: '{node.name}')."
            
                xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=policy_name, option="disable", device_mac=node.mac)
                xiq.xflowscommonDevices.check_device_update_status_by_using_mac(device_mac=node.mac)


@pytest.mark.p1
@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.testbed_1_node
@pytest.mark.testbed_stack
class Xiq1219Tests(Xiq1219):

    @pytest.fixture(scope="class", autouse=True)
    def cls_setup(self, xiq_library_at_class_level, enter_switch_cli, cli, reboot_device, open_spawn, loaded_config, node, node_onboarding_location, node_policy_name):

        try:
            self.configuration_setup(node, enter_switch_cli)
            yield
        finally:
            self.configuration_teardown(cli, node, reboot_device, open_spawn)
            self.revert_node_to_default(xiq_library_at_class_level, node, node_policy_name, node_onboarding_location, open_spawn, cli, loaded_config)

    @pytest.mark.tcxm_16915
    @pytest.mark.tcxm_16917
    @pytest.mark.tcxm_16515
    def test_tcxm_16515_long_config_update(self, test_data, request, node, node_policy_name, cli, logger, xiq_library_at_class_level, node_onboarding_location, test_bed):
        """
        TCXM16515 - Configure a long config update and check the config update messages
        TCXM16915 - Configure a small config update and check the config update messages
        TCXM16917 - CLI command which spans many minutes
        """
        request.addfinalizer(lambda: self.teardown_config_update(test_data["case"], xiq_library_at_class_level, node, node_policy_name, node_onboarding_location, f"delete_vlan_{test_bed.get_random_word(length=8)}"))
        self.verify_config_update(test_data["case"], xiq_library_at_class_level, node, node_policy_name, cli, f"create_vlan_{test_bed.get_random_word(length=8)}")

    @pytest.mark.dependson("tcxm_16515")
    @pytest.mark.tcxm_16916
    def test_tcxm_16916_long_config_update(self, logger):
        """TCXM16916 - Long list of CLI commands"""
        logger.info("Current test case is covered by 'tcxm_16515'.")

    @pytest.mark.tcxm_16516
    @pytest.mark.dependson("tcxm_16515")
    def test_tcxm_16516_long_config_update(self, logger):
        """TCXM16516 - Configure a long  config update and check messages in event page"""
        logger.info("Current test case is covered by 'tcxm_16515'.")
