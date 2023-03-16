# Author :          Zoican Ionut Daniel
# Description :     This script runs the below tests for Delta CLI VLAN add/delete port range commands to individual
#                   commands feature according with XIQ-1027 story.
#                   In some cases delta CLI is created with range commands. Depending on the range width the CLI can
#                   take plus 20 minutes to process for CLI commands handling add/delete VLAN to ports. The purpose of
#                   this story is to convert VLAN add/delete port EXOS range generated delta CLI commands to individual
#                   delta CLI commands. Currently VOSS handles creating commands without range format and EXOS should
#                   follow the same format moving forward.
# Testcases :       TCXM-18696, TCXM-18697, TCXM-18698, TCXM-18699, TCXM-18709, TCXM-18710, TCXM-18712, TCXM-18716,
#                   TCXM-18717
# Comments :        This test is applicable for exos, exos_Stack

import pytest
import time
import string
import random


class Xiq1027:

    @pytest.fixture
    def xiq_teardown_template(self, xiq_library_at_class_level, suite_data, request, utils):

        def func(node, trunk_port_type_name):

            network_policy_name = request.getfixturevalue(f"{node.node_name}_policy_name")
            sw_template_name = request.getfixturevalue(f"{node.node_name}_template_name")
            port_numbers_2 = suite_data["port_numbers_2"]

            if node.node_name == 'node_stack':

                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network_policies_list_view_page()
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, sw_template_name)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                
                for slot in range(1, len(node.serial.split(',')) + 1):
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(slot)
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers_2, "Access Port")
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, sw_template_name)
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(slot=slot)

                for slot in range(1, len(node.serial.split(',')) + 1):
                    
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                    xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                    time.sleep(20)
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac)
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360()
                    xiq_library_at_class_level.xflowsmanageDevice360.select_stack_unit(slot)

                    xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_ports_access_vlan_stack(port_numbers=port_numbers_2, slot=slot)
                
            else:
                xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_ports_access_vlan(
                    device_mac=node.mac, port_numbers=port_numbers_2, access_vlan_id="1")
                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
            
            xiq_library_at_class_level.xflowscommonDevices.get_update_devices_reboot_rollback(
                policy_name=network_policy_name, option="disable", device_mac=node.mac)
            xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)
            xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(trunk_port_type_name)

        return func

    @pytest.fixture
    def teardown_revert_to_template_default(self, xiq_library_at_class_level, request, utils, suite_data):

        def func(node):
            network_policy_name = request.getfixturevalue(f"{node.node_name}_policy_name")
            xiq_library_at_class_level.xflowscommonDevices.revert_device_to_template_but_donot_update(node.mac)
            xiq_library_at_class_level.xflowscommonDevices.get_update_devices_reboot_rollback(
                policy_name=network_policy_name, option="disable", device_mac=node.mac)
            xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)

        return func

    @pytest.fixture
    def teardown_template_configure_ports_access_port_numbers(self, xiq_library_at_class_level, utils, request, suite_data):

        def func(node, trunk_port_type_name):

            network_policy_name = request.getfixturevalue(f"{node.node_name}_policy_name")
            sw_template_name = request.getfixturevalue(f"{node.node_name}_template_name")
            port_numbers = suite_data["port_numbers"]

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network_policies_list_view_page()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, sw_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

            if node.node_name == "node_stack":
                for slot in range(1, len(node.serial.split(',')) + 1):
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(slot)
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers, "Access Port")
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, sw_template_name)

                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(slot=slot)
            else:
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers, "Access Port")

            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name, option="disable", device_mac=node.mac),
                timeout=60, delay=3, msg='Checking the initialization of the update')

            utils.wait_till(lambda: xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac),
                timeout=300, delay=5, msg='Checking update status')
            xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(trunk_port_type_name)

        return func

    @pytest.fixture
    def check_delta_cli_delete_port_range_commands_to_individual_from_template(self, suite_data, utils,
        logger, xiq_library_at_class_level, enter_switch_cli, request, teardown_template_configure_ports_access_port_numbers):

        def func(node):
            
            try:
                trunk_port_type_name = "port_type_" + ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
                network_policy_name = request.getfixturevalue(f"{node.node_name}_policy_name")
                sw_template_name = request.getfixturevalue(f"{node.node_name}_template_name")
                vlan_range = suite_data["vlan_range"]
                port_numbers = suite_data["port_numbers"]
                port_numbers_2 = suite_data["port_numbers_2"]

                xiq_library_at_class_level.xflowsmanageXiqVerifications.template_add_vlans(
                    node, port_numbers, vlan_range, trunk_port_type_name, network_policy_name, sw_template_name)

                for new_trunk_port in port_numbers_2.split(','):
                    for port in port_numbers.split(','):
                        if int(new_trunk_port) == int(port):
                            logger.fail("The new trunk ports must be different from the initial ones!")

                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network_policies_list_view_page()
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, sw_template_name)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

                if node.node_name == "node_stack":
                    for slot in range(1, len(node.serial.split(',')) + 1):
                        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(slot)
                        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                            "Access Port")
                        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                            sw_template_name)
                        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(slot=slot)
                else:
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                        "Access Port")

                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, sw_template_name)
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(
                    port_numbers_2, trunk_port_type_name)
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()

                if xiq_library_at_class_level.xflowsmanageXiqVerifications.check_delete_vlan_range_commands_to_individual(
                    node, vlan_range, port_numbers):
                    logger.info("Found the individual delete port commands!")
                    
                    with enter_switch_cli(node) as dev_cmd:
                        if xiq_library_at_class_level.xflowsmanageXiqVerifications.check_devices_config_after_individual_add_delete_port_push(
                            node, port_numbers, vlan_range, network_policy_name, op="delete"):
                            logger.info("The delete commands that have been pushed are present on the device's config.")
                        else:
                            logger.fail("The delete commands that have been pushed are not present!")
                else:
                    logger.fail("Failed to find the individual delete port commands!")

            finally:
                teardown_template_configure_ports_access_port_numbers(node, trunk_port_type_name)

        return func

    @pytest.fixture
    def check_delta_cli_add_port_range_commands_to_individual_from_template(self, suite_data, utils,
        logger, xiq_library_at_class_level, enter_switch_cli, request, teardown_template_configure_ports_access_port_numbers):

        def func(node):

            try:
                trunk_port_type_name = "port_type_" + ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
                network_policy_name = request.getfixturevalue(f"{node.node_name}_policy_name")
                sw_template_name = request.getfixturevalue(f"{node.node_name}_template_name")
                vlan_range = suite_data["vlan_range"]
                port_numbers = suite_data["port_numbers"]
                port_numbers_2 = suite_data["port_numbers_2"]

                template_exos = {'name': [trunk_port_type_name, trunk_port_type_name],
                                'description': [None, None],
                                'status': [None, 'on'],
                                'port usage': ['trunk port', 'TRUNK'],
                                'page2 trunkVlanPage': ['next_page', None],
                                'native vlan': ['1', '1'],
                                'allowed vlans': [vlan_range, vlan_range],
                                'page3 transmissionSettings': ["next_page", None],
                                'page4 stp': ["next_page", None],
                                'page5 stormControlSettings': ["next_page", None],
                                'page6 MACLocking': ["next_page", None],
                                'page7 ELRP': ["next_page", None],
                                'page8 pseSettings': ["next_page", None],
                                'page9 summary': ["next_page", None]
                                }

                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, sw_template_name)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_exos, port_numbers.split(',')[0])

                if node.node_name == "node_stack":

                    for slot in range(1, len(node.serial.split(',')) + 1):

                        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, sw_template_name)
                        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(slot)
                        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(
                            port_numbers, trunk_port_type_name)

                else:
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, sw_template_name)
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(
                        port_numbers, trunk_port_type_name)

                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()

                if xiq_library_at_class_level.xflowsmanageXiqVerifications.check_add_vlan_range_commands_to_individual(
                    node, vlan_range, port_numbers):
                    logger.info("Found the individual add port commands!")
                    
                    with enter_switch_cli(node):
                        if xiq_library_at_class_level.xflowsmanageXiqVerifications.check_devices_config_after_individual_add_delete_port_push(
                            node, port_numbers, vlan_range, network_policy_name, op="add"):
                            logger.info("The add commands that have been pushed are present on the device's config.")
                        else:
                            logger.fail("The delete commands that have been pushed are not present!")
                else:
                    logger.fail("Failed to find the individual add port commands!")
            
            finally:
                teardown_template_configure_ports_access_port_numbers(node, trunk_port_type_name)

        return func

    @pytest.fixture
    def verify_that_changes_are_present_in_delta_cLI_after_overwr_template_vlan_config_in_d360(self, suite_data, utils,
        logger, xiq_library_at_class_level, enter_switch_cli, request, xiq_teardown_template):

        def func(node):

            trunk_port_type_name = "port_type_" + ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))

            try:
                network_policy_name = request.getfixturevalue(f"{node.node_name}_policy_name")
                sw_template_name = request.getfixturevalue(f"{node.node_name}_template_name")
                vlan_range = suite_data["vlan_range"]
                vlan_range_2 = suite_data["vlan_range_2"]
                port_numbers = suite_data["port_numbers"]
                port_numbers_2 = suite_data["port_numbers_2"]

                xiq_library_at_class_level.xflowsmanageXiqVerifications.template_add_vlans(
                    node, port_numbers_2, vlan_range, trunk_port_type_name, network_policy_name, sw_template_name)
                xiq_library_at_class_level.xflowscommonDevices.get_update_devices_reboot_rollback(
                    policy_name=network_policy_name, option="disable", device_mac=node.mac)
                xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)

                if node.node_name == 'node_stack':
                    for slot in range(1, len(node.serial.split(',')) + 1):
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                        xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                        time.sleep(20)

                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(
                                node.mac)
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360()
                        xiq_library_at_class_level.xflowsmanageDevice360.select_stack_unit(slot)
                        xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_ports_trunk_stack(
                            port_numbers=port_numbers_2, trunk_native_vlan="1", trunk_vlan_id=vlan_range_2, slot=slot)
                else:
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                    xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                    time.sleep(20)
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac)
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360()
                    xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_ports_trunk_vlan(
                        port_numbers=port_numbers_2, trunk_native_vlan="1", trunk_vlan_id=vlan_range_2)

                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                delta_configs = xiq_library_at_class_level.xflowsmanageDeviceConfig.get_device_config_audit_delta(node.mac)
                
                if delta_configs == -1:
                    logger.fail('Did not manage to collect the delta configurations.')
                
                if 'delete vlan ' + vlan_range in delta_configs:
                    if xiq_library_at_class_level.xflowsmanageXiqVerifications.check_add_vlan_range_commands_to_individual(
                        node, vlan_range_2, port_numbers_2):
                        logger.info("Found the add commands for the second vlan range!")
                    else:
                        logger.fail("Failed to find the individual add port commands!")
                else:
                    logger.fail("Did not find the deletion command for the previous range!")
            
            finally:
                xiq_teardown_template(node, trunk_port_type_name)

        return func

    @pytest.fixture
    def check_delta_cli_add_port_range_commands_to_individual(self, suite_data, utils,
        logger, xiq_library_at_class_level, enter_switch_cli, request, teardown_revert_to_template_default):

        def func(node):

            trunk_port_type_name = "port_type_" + ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
            network_policy_name = request.getfixturevalue(f"{node.node_name}_policy_name")
            sw_template_name = request.getfixturevalue(f"{node.node_name}_template_name")
            vlan_range = suite_data["vlan_range"]
            port_numbers = suite_data["port_numbers"]
            port_numbers_2 = suite_data["port_numbers_2"]

            try:
                if node.node_name == 'node_stack':
                    for slot in range(1, len(node.serial.split(',')) + 1):
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                        xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                        time.sleep(20)
                        
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac)
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360()
                        xiq_library_at_class_level.xflowsmanageDevice360.select_stack_unit(slot)

                        xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_ports_trunk_stack(
                            port_numbers=port_numbers, trunk_native_vlan="1", trunk_vlan_id=vlan_range, slot=slot)
                else:
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                    xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                    time.sleep(20)
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac)
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360()
                    xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_ports_trunk_vlan(
                        port_numbers=port_numbers, trunk_native_vlan="1", trunk_vlan_id=vlan_range)
                
                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                
                if xiq_library_at_class_level.xflowsmanageXiqVerifications.check_add_vlan_range_commands_to_individual(
                    node, vlan_range, port_numbers):
                    logger.info("Found the commands!")
                else:
                    logger.fail("Failed to find the individual add port commands!")

            finally:
                teardown_revert_to_template_default(node)
        return func

    @pytest.fixture
    def check_device_config_after_add_port_individual_commands_update(self, suite_data, utils,
        logger, xiq_library_at_class_level, enter_switch_cli, request, teardown_revert_to_template_default):

        def func(node):
            
            try:
                trunk_port_type_name = "port_type_" + ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
                network_policy_name = request.getfixturevalue(f"{node.node_name}_policy_name")
                sw_template_name = request.getfixturevalue(f"{node.node_name}_template_name")
                vlan_range = suite_data["vlan_range"]
                port_numbers = suite_data["port_numbers"]
                port_numbers_2 = suite_data["port_numbers_2"]

                xiq_library_at_class_level.xflowsmanageDevice360.configure_vlan_range_d360(node, port_numbers, vlan_range)
                
                with enter_switch_cli(node):
                    if xiq_library_at_class_level.xflowsmanageXiqVerifications.check_devices_config_after_individual_add_delete_port_push(
                        node, port_numbers, vlan_range, network_policy_name, op="add"):
                        logger.info("The commands that have been pushed, are present on the device's config.")
                    else:
                        logger.fail("The commands that have been pushed, are not present!")
            finally:
                teardown_revert_to_template_default(node)
        return func

    @pytest.fixture
    def check_delta_cli_delete_port_range_commands_to_individual(self, suite_data, utils,
        logger, xiq_library_at_class_level, enter_switch_cli, request, teardown_revert_to_template_default):

        def func(node):
            
            try:
                trunk_port_type_name = "port_type_" + ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
                network_policy_name = request.getfixturevalue(f"{node.node_name}_policy_name")
                sw_template_name = request.getfixturevalue(f"{node.node_name}_template_name")
                vlan_range = suite_data["vlan_range"]
                port_numbers = suite_data["port_numbers"]
                port_numbers_2 = suite_data["port_numbers_2"]
                new_trunk_port = str(suite_data["new_trunk_port"])

                xiq_library_at_class_level.xflowsmanageDevice360.configure_vlan_range_d360(node, port_numbers, vlan_range)
                
                with enter_switch_cli(node):
                    xiq_library_at_class_level.xflowsmanageXiqVerifications.check_devices_config_after_individual_add_delete_port_push(
                        node, port_numbers, vlan_range, network_policy_name, op="add")

                for port in port_numbers.split(','):
                    if int(new_trunk_port) == int(port):
                        logger.fail("The new trunk port must be different from the initial ones!")
                
                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                
                if node.node_name == 'node_stack':
                    
                    for slot in range(1, len(node.serial.split(',')) + 1):
                        
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                        xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                        time.sleep(20)
                        
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(
                                node.mac)
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360()

                        xiq_library_at_class_level.xflowsmanageDevice360.select_stack_unit(slot)
                        xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_ports_trunk_stack(
                            port_numbers=port_numbers_2, trunk_native_vlan="1", trunk_vlan_id=vlan_range,  slot=slot)
                    
                    for slot in range(1, len(node.serial.split(',')) + 1):
                    
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                        xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                        time.sleep(20)
                    
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac)
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360()
                        xiq_library_at_class_level.xflowsmanageDevice360.select_stack_unit(slot)
                        xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_ports_access_vlan_stack(
                            port_numbers=port_numbers, slot=slot)

                else:
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac)
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360()
                    xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_ports_trunk_vlan(
                        port_numbers=new_trunk_port, trunk_native_vlan="1", trunk_vlan_id=vlan_range)
                    xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_ports_access_vlan(
                        device_mac=node.mac, port_numbers=port_numbers, access_vlan_id="1")
                
                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                
                if xiq_library_at_class_level.xflowsmanageXiqVerifications.check_delete_vlan_range_commands_to_individual(
                    node, vlan_range, port_numbers):
                    logger.info('The individual delete commands have been found.')
                else:
                    logger.fail("Failed to find the individual delete port commands.")
            finally:
                teardown_revert_to_template_default(node)
 
        return func

    @pytest.fixture
    def check_device_config_after_delete_port_individual_commands_update(self, suite_data, utils,
        logger, xiq_library_at_class_level, enter_switch_cli, request, teardown_revert_to_template_default):

        def func(node):
            try:
                trunk_port_type_name = "port_type_" + ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
                network_policy_name = request.getfixturevalue(f"{node.node_name}_policy_name")
                sw_template_name = request.getfixturevalue(f"{node.node_name}_template_name")
                vlan_range = suite_data["vlan_range"]
                port_numbers = suite_data["port_numbers"]
                port_numbers_2 = suite_data["port_numbers_2"]
                new_trunk_port = str(suite_data["new_trunk_port"])

                xiq_library_at_class_level.xflowsmanageDevice360.configure_vlan_range_d360(node, port_numbers, vlan_range)

                with enter_switch_cli(node):
                    xiq_library_at_class_level.xflowsmanageXiqVerifications.check_devices_config_after_individual_add_delete_port_push(
                        node, port_numbers, vlan_range, network_policy_name, op="add")

                for port in port_numbers.split(','):
                    if int(new_trunk_port) == int(port):
                        logger.fail("The new trunk port must be different from the initial ones!")

                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()

                if node.node_name == 'node_stack':

                    for slot in range(1, len(node.serial.split(',')) + 1):

                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                        xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                        time.sleep(20)

                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(
                                node.mac)
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360()

                        xiq_library_at_class_level.xflowsmanageDevice360.select_stack_unit(slot)
                        xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_ports_trunk_stack(
                            port_numbers=port_numbers_2, trunk_native_vlan="1", trunk_vlan_id=vlan_range, slot=slot)

                    for slot in range(1, len(node.serial.split(',')) + 1):

                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                        xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                        time.sleep(20)

                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(
                            node.mac)
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360()
                        xiq_library_at_class_level.xflowsmanageDevice360.select_stack_unit(slot)
                        xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_ports_access_vlan_stack(
                            port_numbers=port_numbers, slot=slot)
                else:
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac)
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360()
                    xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_ports_trunk_vlan(
                        port_numbers=new_trunk_port, trunk_native_vlan="1", trunk_vlan_id=vlan_range)

                    xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_ports_access_vlan(
                        device_mac=node.mac, port_numbers=port_numbers, access_vlan_id="1")
                
                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                
                with enter_switch_cli(node) as dev_cmd:

                    if xiq_library_at_class_level.xflowsmanageXiqVerifications.check_devices_config_after_individual_add_delete_port_push(
                        node, port_numbers, vlan_range, network_policy_name, op="delete"):
                        logger.info('The individual delete commands have been pushed to the device.')
                    else:
                        logger.fail("Some or all ports are still configured on trunk.")
            finally:
                teardown_revert_to_template_default(node)

        return func

@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.testbed_stack
@pytest.mark.testbed_1_node
class Xiq1027Tests(Xiq1027):

    @pytest.mark.tcxm_18709
    @pytest.mark.p1
    def test_check_delta_cli_add_port_range_commands_to_individual_from_template_tcxm_18709(
        self, suite_data, test_data, node, check_delta_cli_add_port_range_commands_to_individual_from_template):
        check_delta_cli_add_port_range_commands_to_individual_from_template(node)

    @pytest.mark.tcxm_18710
    @pytest.mark.p1
    def test_check_delta_cli_delete_port_range_commands_to_individual_from_template_tcxm_18710(
        self, suite_data, test_data, node, check_delta_cli_delete_port_range_commands_to_individual_from_template):
        check_delta_cli_delete_port_range_commands_to_individual_from_template(node)

    @pytest.mark.tcxm_18712
    @pytest.mark.p2
    def test_verify_that_changes_are_present_in_delta_cLI_after_overwr_template_vlan_config_in_d360_tcxm_18712(
        self, suite_data, test_data, node, verify_that_changes_are_present_in_delta_cLI_after_overwr_template_vlan_config_in_d360):
        verify_that_changes_are_present_in_delta_cLI_after_overwr_template_vlan_config_in_d360(node)

    @pytest.mark.tcxm_18696
    @pytest.mark.p1
    def test_check_delta_cli_add_port_range_commands_to_individual_tcxm_18696(
        self, suite_data, test_data, node, check_delta_cli_add_port_range_commands_to_individual):
        check_delta_cli_add_port_range_commands_to_individual(node)

    @pytest.mark.tcxm_18697
    @pytest.mark.p2
    def test_check_device_config_after_add_port_individual_commands_update_tcxm_18697(
        self, suite_data, test_data, node, check_device_config_after_add_port_individual_commands_update):
        check_device_config_after_add_port_individual_commands_update(node)

    @pytest.mark.tcxm_18698
    @pytest.mark.p1
    def test_check_delta_cli_delete_port_range_commands_to_individual_tcxm_18698(
        self, suite_data, test_data, node, check_delta_cli_delete_port_range_commands_to_individual):
        check_delta_cli_delete_port_range_commands_to_individual(node)

    @pytest.mark.tcxm_18699
    @pytest.mark.p2
    def test_check_device_config_after_delete_port_individual_commands_update_tcxm_18699(
        self, suite_data, test_data, node, check_device_config_after_delete_port_individual_commands_update):
        check_device_config_after_delete_port_individual_commands_update(node)
