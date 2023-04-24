import pytest
from extauto.xiq.elements.SwitchTemplateWebElements import SwitchTemplateWebElements
import re
import time
import random


class XIQ1157Tests:
    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_20603
    @pytest.mark.p2
    def test_tcxm_20603(self, node_1, logger, node_1_policy_name, node_1_template_name,
                        xiq_library_at_class_level, loaded_config, auto_actions, enter_switch_cli):
        """
        Author        : sstaut@extremenetworks.com
        Modified by   : mchelu
        Description   : Verify that LACP for VIM ports can be created using Assign button from Switch Template
                        for EXOS 5520.
        Preconditions : Use EXOS 5520 devices with 4 ports VIM module.
        Step	Step Description
        1	    Onboard the EXOS 5520 standalone.
        2	    Create a Network Policy with specific 5520 template.
        3	    Assign the previously created Network Policy to the device.
        4	    Using the Assign button from Switch Template -> Port configuration aggregate 2 VIM ports.
        5	    Update the device, check the results in CLI.
        6	    Using the Switch Template -> Port Configuration add the 3rd VIM port to the LACP.
        7	    Update the device, check the results in CLI.
        8	    Using the Switch Template -> Port Configuration add the 4rd VIM port to the LACP.
        9	    Update the device, check the results in CLI.
        10	    Using the Switch Template -> Port Configuration remove all VIM ports from the LACP.
        11      Update the device, check the results in CLI.
        """

        sw_template_web_elements = SwitchTemplateWebElements()
        vim_ports = []
        main_lag_port = ""
        loaded_config['${TEST_NAME}'] = 'test_tcxm_20603_run'
        try:
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name, node_1_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            logger.info("Get all available ports.")
            all_ports = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_device_template_no_of_ports()
            total_number_of_ports = len(all_ports)
            first_vim_port = str(total_number_of_ports)
            second_vim_port = str(total_number_of_ports - 1)
            third_vim_port = str(total_number_of_ports - 2)
            fourth_vim_port = str(total_number_of_ports - 3)

            logger.step("Aggregate 2 VIM ports by going to Assign-> Advanced Actions-> Aggregate")
            auto_actions.click(
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_assign_button())
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements. \
                get_sw_template_assign_advanced_actions()
            auto_actions.move_to_element(element)
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements. \
                get_sw_template_assign_advanced_actions_aggr()
            auto_actions.move_to_element(element)
            auto_actions.click(element)
            logger.step("Add VIM port")
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_port(first_vim_port)
            if element is None:
                logger.info("Couldn't get vim port, exit")
                pytest.fail("No VIM ports available.")
            auto_actions.click(element)
            auto_actions.click(xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                                    get_lag_add_port_button())

            logger.step("check port in agg list")
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_selected_port(first_vim_port)
            if element is None:
                logger.info("selected vim port not found, exit")
                pytest.fail("port error")

            logger.step("Try to add a wireframe copper port")
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_port(
                second_vim_port)
            if element is None:
                logger.info("Couldn't get copper port, exit")
                pytest.fail("port get error")
            auto_actions.click(element)
            auto_actions.click(xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                                    get_lag_add_port_button())
            # check port in agg list
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_selected_port(second_vim_port)
            if element is None:
                logger.info("selected copper port is found, exit")
                pytest.fail("port error")
            auto_actions.click(sw_template_web_elements.get_save_port_type_button())
            auto_actions.click(sw_template_web_elements.save_device_template())
            tool_tip_text = ""
            tip_box_error = xiq_library_at_class_level.xflowsconfigureCommonObjects.cobj_web_elements.get_ui_tipbox_error()
            if tip_box_error:
                tool_tip_text = tip_box_error.text
            # -------------
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowscommonDevices.update_switch_policy_and_configuration(device_mac=node_1.mac) == 1, \
                "Failed to update device"
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {first_vim_port} grouping {second_vim_port}-{first_vim_port}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")
            main_lag_port = first_vim_port
            vim_ports.extend([main_lag_port, second_vim_port])
            # Add 3rd port
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name, node_1_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.create_modify_lag_in_template(first_vim_port, [third_vim_port], device='standalone')
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowscommonDevices.update_switch_policy_and_configuration(device_mac=node_1.mac) == 1, \
                "Failed to update device"
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {first_vim_port} grouping {third_vim_port}-{first_vim_port}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")
            vim_ports.append(third_vim_port)
            # Add 4th port
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name, node_1_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.create_modify_lag_in_template(first_vim_port, [fourth_vim_port], device='standalone')
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowscommonDevices.update_switch_policy_and_configuration(device_mac=node_1.mac) == 1, \
                "Failed to update device"
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {first_vim_port} grouping {fourth_vim_port}-{first_vim_port}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")
            vim_ports.append(fourth_vim_port)
        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_20603_teardown'
            if main_lag_port != "":
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name, node_1_template_name)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                logger.info(f"Removing ports {vim_ports} from lag {main_lag_port} LAG")
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.remove_lag_in_template(main_lag_port, vim_ports, device='standalone')
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                    device_mac=node_1.mac) == 1, "Could not update the device"
                with enter_switch_cli(node_1) as dev_cmd:
                    output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
                result = output[0].return_text
                assert "enable sharing" not in result, f"Lag is still present in CLI."

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_20604
    @pytest.mark.p1
    def test_tcxm_20604(self, node_1, logger, node_1_policy_name, node_1_template_name,
                        xiq_library_at_class_level, loaded_config, enter_switch_cli):
        """
        Author        : rvisterineanu
        Modified by   : mchelu
        Description   : Verify that VIM ports can be removed from the existing LACP.
        Preconditions : Use EXOS 5520 standalone
         Step	Step Description
         1	    Onboard the EXOS 5520 standalone.
         2	    Create a Network Policy with specific 5520 template.
         3	    Assign the previously created Network Policy to the device and update the device.
         4	    Using the Assign Button from Switch Template -> Port configuration aggregate 4 VIM ports.
         5	    Update the device, check the results in CLI and check the number of LACP ports in Switch Template
         6	    Using the Switch Template -> Port configuration remove 2 VIM ports from the LACP.
         7      Update the device, check the results in CLI and check the number of LACP ports in Switch Template
         8      Using the Switch Template remove all VIM ports from the LACP.
         9      Update the device, check the results in CLI and check the number of LACP ports in Switch Template
         """

        sw_template_web_elements = SwitchTemplateWebElements()
        main_lag_port = ""
        loaded_config['${TEST_NAME}'] = 'test_tcxm_20604_run'
        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name,
                                                                                        node_1_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            logger.info("Get all available ports.")
            all_ports = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_device_template_no_of_ports()
            total_number_of_ports = len(all_ports)
            first_vim_port = str(total_number_of_ports)
            second_vim_port = str(total_number_of_ports - 1)
            third_vim_port = str(total_number_of_ports - 2)
            fourth_vim_port = str(total_number_of_ports - 3)

            # Aggregate 2 VIM ports
            main_lag_port = first_vim_port
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.create_modify_lag_in_template(main_lag_port,
                                                                                                   [second_vim_port,
                                                                                                    third_vim_port,
                                                                                                    fourth_vim_port],
                                                                                                   device='standalone')
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowscommonDevices.update_switch_policy_and_configuration(
                device_mac=node_1.mac) == 1, \
                "Failed to update device"
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {main_lag_port} grouping {fourth_vim_port}-{main_lag_port}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")

            # Verify the existing LAG and remove 2 VIM ports
            vim_ports = [first_vim_port, second_vim_port]
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name,
                                                                                        node_1_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            logger.info(f"Removing ports {vim_ports} from lag {main_lag_port} LAG")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.remove_lag_in_template(main_lag_port, vim_ports,
                                                                                            device='standalone')
            main_lag_port = fourth_vim_port
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_1.mac) == 1, "Could not update the device"
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {main_lag_port} grouping {fourth_vim_port}-{third_vim_port}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")

        finally:
            # remove the remaining ports from LAG
            loaded_config['${TEST_NAME}'] = 'test_tcxm_20604_teardown'
            vim_ports = [third_vim_port, fourth_vim_port]
            if main_lag_port != "":
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name,
                                                                                            node_1_template_name)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                logger.info(f"Removing ports {vim_ports} from lag {main_lag_port} LAG")
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.remove_lag_in_template(main_lag_port,
                                                                                                vim_ports,
                                                                                                device='standalone')
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                    device_mac=node_1.mac) == 1, "Could not update the device"
                with enter_switch_cli(node_1) as dev_cmd:
                    output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
                result = output[0].return_text
                assert "enable sharing" not in result, f"Lag is still present in CLI."

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_20605
    @pytest.mark.p1
    def test_tcxm_20605(self, node_1, logger, xiq_library_at_class_level, loaded_config,
                        auto_actions, enter_switch_cli):
        """
        Author        : rvisterineanu
        Modified by   : mchelu
        Description   : Verify that LACP for VIM ports can be created using Device Level Configuration.
        Preconditions : Use EXOS 5520 standalone
         Step	Step Description
         1	    Onboard the EXOS 5520 standalone.
         2	    Create a Network Policy with specific 5520 template.
         3	    Assign the previously created Network Policy to the device and update the device.
         4	    Using D360 -> Port configuration aggregate 2 VIM ports.
         5	    Update the device, check the results in CLI and check the number of LACP ports in D360.
         6	    Using D360 -> Port Configuration add 3rd VIM port to the LACP.
         7      Update the device, check the results in CLI and check the number of LACP ports in D360.
         8      Using D360 -> Port Configuration add 4th VIM port to the LACP.
         9      Update the device, check the results in CLI and check the number of LACP ports in D360.
         10     Using D360 -> Port Configuration remove all VIM ports from the LACP.
         """

        loaded_config['${TEST_NAME}'] = 'test_tcxm_20605_run'
        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_1.mac)
            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            logger.info("Navigating to Port Settings & Aggregation")
            button_settings = xiq_library_at_class_level.xflowsmanageDevice360.dev360. \
                get_d360_configure_port_settings_aggregation_tab_button()
            assert button_settings, "Could not find port settings & aggregation button"
            auto_actions.click(button_settings)
            ports_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_configure_port_rows()
            assert ports_rows, "Could not extract port list from Device360"
            ports_no = len(ports_rows)
            # Aggregate 2 VIM ports
            ports_used = [str(ports_no), str(ports_no - 1), str(ports_no - 2), str(ports_no - 3)]

            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_aggregate_ports(
                [ports_used[0], ports_used[1]], False,
                device="standalone"), \
                f"Could not aggregate ports {ports_used[0]} and {ports_used[1]}"

            # Update the device and check LACP in Device360 and CLI
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowscommonDevices.update_switch_policy_and_configuration(
                node_1.serial) == 1, "Could not update the device"
            logger.info("Verify CLI output")
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {ports_used[0]} grouping {ports_used[1]}-{ports_used[0]}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")

            # Aggregate 3rd VIM port
            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            button_settings = xiq_library_at_class_level.xflowsmanageDevice360.dev360. \
                get_d360_configure_port_settings_aggregation_tab_button()
            assert button_settings, "Could not find port settings & aggregation button"
            auto_actions.click(button_settings)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(ports_used[0],
                                                                                            [ports_used[2]],
                                                                                            device="standalone")
            # Update the device and check LACP in Device360 and CLI
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowscommonDevices.update_switch_policy_and_configuration(
                node_1.serial) == 1, "Could not update the device"
            logger.info("Verify CLI output")
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {ports_used[0]} grouping {ports_used[2]}-{ports_used[0]}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")

            # Aggregate 4th VIM port
            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            button_settings = xiq_library_at_class_level.xflowsmanageDevice360.dev360. \
                get_d360_configure_port_settings_aggregation_tab_button()
            assert button_settings, "Could not find port settings & aggregation button"
            auto_actions.click(button_settings)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(ports_used[0],
                                                                                            [ports_used[3]],
                                                                                            device="standalone")
            # Update the device and check LACP in Device360 and CLI
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowscommonDevices.update_switch_policy_and_configuration(
                node_1.serial) == 1, "Could not update the device"
            logger.info("Verify CLI output")
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {ports_used[0]} grouping {ports_used[3]}-{ports_used[0]}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")
            # Remove LAG
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            button_settings = xiq_library_at_class_level.xflowsmanageDevice360.dev360. \
                get_d360_configure_port_settings_aggregation_tab_button()
            assert button_settings, "Could not find port settings & aggregation button"
            auto_actions.click(button_settings)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(ports_used[0], ports_used,
                                                                                            action='remove',
                                                                                            device="standalone")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowscommonDevices.update_switch_policy_and_configuration(
                node_1.serial) == 1, "Could not update the device"
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            assert "enable sharing" not in result, f"Lag is still present in CLI."
        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_20605_teardown'
            xiq_library_at_class_level.xflowsmanageDevices.revert_device_to_template(node_1.serial)

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_20606
    @pytest.mark.p2
    def test_tcxm_20606(self, node_1, logger, node_1_policy_name, node_1_template_name, xiq_library_at_class_level,
                        loaded_config, enter_switch_cli):
        """
        Author        : gburlacu
        Modified by   : mchelu
        Description   : Verify that LACP for VIM ports can be created using Aggregate Ports button from Switch Template
                        for EXOS 5520.
        Preconditions : Use EXOS 5520 devices with 4 ports VIM module.
        Step	Step Description
        1	    Onboard the EXOS 5520 standalone.
        2	    Create a Network Policy with specific 5520 template.
        3	    Assign the previously created Network Policy to the device and update the device.
        4	    Using the Aggregate Ports button from Switch Template -> Port configuration aggregate 2 VIM ports.
        5	    Update the device, check the results in CLI.
        6	    Using the Switch Template -> Port Configuration add the 3rd VIM port to the LACP.
        7	    Update the device, check the results in CLI.
        8	    Using the Switch Template -> Port Configuration add the 4rd VIM port to the LACP.
        9	    Update the device, check the results in CLI.
        10	    Using the Switch Template -> Port Configuration remove all VIM ports from the LACP.
        11      Update the device, check the results in CLI.
        """

        vim_ports = []
        main_lag_port = ""
        loaded_config['${TEST_NAME}'] = 'test_tcxm_20606_run'
        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name,
                                                                                        node_1_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            logger.info("Get all available ports.")
            all_ports = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_device_template_no_of_ports()
            total_number_of_ports = len(all_ports)
            first_vim_port = str(total_number_of_ports)
            second_vim_port = str(total_number_of_ports - 1)
            third_vim_port = str(total_number_of_ports - 2)
            fourth_vim_port = str(total_number_of_ports - 3)

            # Aggregate 2 VIM ports
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.create_modify_lag_in_template(first_vim_port,
                                                                                                   [second_vim_port],
                                                                                                   device='standalone')
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowscommonDevices.update_switch_policy_and_configuration(
                device_mac=node_1.mac) == 1, \
                "Failed to update device"
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {first_vim_port} grouping {second_vim_port}-{first_vim_port}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")
            main_lag_port = first_vim_port
            vim_ports.extend([main_lag_port, second_vim_port])
            # Add 3rd port
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name,
                                                                                        node_1_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.create_modify_lag_in_template(first_vim_port,
                                                                                                   [third_vim_port],
                                                                                                   device='standalone')
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowscommonDevices.update_switch_policy_and_configuration(
                device_mac=node_1.mac) == 1, \
                "Failed to update device"
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {first_vim_port} grouping {third_vim_port}-{first_vim_port}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")
            vim_ports.append(third_vim_port)
            # Add 4th port
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name,
                                                                                        node_1_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.create_modify_lag_in_template(first_vim_port,
                                                                                                   [fourth_vim_port],
                                                                                                   device='standalone')
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowscommonDevices.update_switch_policy_and_configuration(
                device_mac=node_1.mac) == 1, \
                "Failed to update device"
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {first_vim_port} grouping {fourth_vim_port}-{first_vim_port}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")
            vim_ports.append(fourth_vim_port)
        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_20606_teardown'
            if main_lag_port != "":
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name,
                                                                                            node_1_template_name)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                logger.info(f"Removing ports {vim_ports} from lag {main_lag_port} LAG")
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.remove_lag_in_template(main_lag_port,
                                                                                                vim_ports,
                                                                                                device='standalone')
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                    device_mac=node_1.mac) == 1, "Could not update the device"
                with enter_switch_cli(node_1) as dev_cmd:
                    output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
                result = output[0].return_text
                assert "enable sharing" not in result, f"Lag is still present in CLI."

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_20608
    @pytest.mark.p1
    def test_tcxm_20608(self, node_1, logger, node_1_policy_name, node_1_template_name,
                        xiq_library_at_class_level, loaded_config, auto_actions):
        """
        Author        : scostache
        Modified by   : mchelu
        TCXM-20608    : https://aerohive.qtestnet.com/p/101323/portal/project#tab=testdesign&object=1&id=55067625
        Description   : Verify that LACP cannot be formed between VIM and fixed panel ports using Assign button from
        Switch Template.
         0	Use devices with 4 ports VIM module (10 or 25 G ports) and aggregate them according to tests requirements.
        Supported devices: 5520-24T, 5520-24W, 5520-48T, 5520-48W, 5520-12MW-36W, 5520-24X, 5520-48SE, 5520-VIM-4X,
        5520-VIM-4XE
        , 5520-VIM-4YE.
        Tested EXOS devices: 5520-48SE with 5520-VIM-4XE, 5520-24W with 5520-VIM-4X, 5520-24T with 5520-VIM-4YE.
         1	Onboard the EXOS 5520 standalone.
        Device is onboarded successfully.
         2	Create a Network Policy with specific 5520 template.
        Network Policy is created successfully.
         3	Using the Assign button from Switch Template -> Port configuration aggregate 1 VIM port and
                                        1 fixed panel port

        * If the fixed panel port is Ethernet type the following error is received:
            You cannot aggregate Ethernet ports with SFP ports.
        * If the fixed panel port is SFP type the following error is received:
            Only VIM ports within the same VIM can be part of the same LAG.
        """

        loaded_config['${TEST_NAME}'] = 'test_tcxm_20608_run'
        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_1.mac)
            if not xiq_library_at_class_level.xflowsmanageDevice360.d360_check_if_vim_is_installed():
                logger.info("Warning: no actual VIM module installed")
                wireframe_port_list = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_wireframe_port()
                # VIM ports are the last 4 ports
                tmp_len = len(wireframe_port_list)
                vim_port = wireframe_port_list[random.randint(tmp_len - 4, tmp_len - 1)].text
                if vim_port == -1:
                    pytest.fail("Can't retrieve VIM port")
            else:
                vim_port = xiq_library_at_class_level.xflowsmanageDevice360.d360_return_vim_port_number()
                vim_port = str(random.randint(int(vim_port), int(vim_port) + 3))
                if vim_port == -1:
                    pytest.fail("Can't retrieve VIM port")

            logger.info("------Test Ports------")
            logger.info("Use VIM SFP Port:  " + vim_port)

            wireframe_port_list = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_wireframe_ether_port()
            assert wireframe_port_list, "No ethernet ports were found"
            tmp_len = len(wireframe_port_list)
            wireframe_port = wireframe_port_list[random.randint(0, tmp_len - 1)].text

            logger.info("Use Ethernet Port: " + wireframe_port)

            sfp28_port_list = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_wireframe_sfp28_port()
            assert sfp28_port_list, "No SFP ports were found."
            sfp28_port_list_len = len(sfp28_port_list)
            if sfp28_port_list_len == 0:
                sfp_port = None
            else:
                # SFP port text is U#number, so consider SFP port number is last-ether-port + random int between 1
                # and length of sfp port_list
                sfp_port = str(int(wireframe_port_list[tmp_len - 1].text) + random.randint(1, sfp28_port_list_len))

            logger.info("Use Fiber Port:    " + sfp_port)
            logger.info("------Test Ports------")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name,
                                                                                        node_1_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            logger.info("-------------------------------------------------------------")
            logger.info("First add a VIM port in LAG, then try to add an Ethernet port")
            logger.info("then try to add an universal SFP port")
            logger.info("------------------------------")
            # First add a VIM port and then try to add the Ethernet Port and then try adding the Fiber Port
            auto_actions.click(
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_assign_button())
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements. \
                get_sw_template_assign_advanced_actions()
            auto_actions.move_to_element(element)
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements. \
                get_sw_template_assign_advanced_actions_aggr()
            auto_actions.move_to_element(element)
            auto_actions.click(element)
            # Add VIM port
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_port(
                vim_port)
            if element is None:
                logger.info("Couldn't get vim port, exit")
                pytest.fail("port get error")
            auto_actions.click(element)
            auto_actions.click(xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                               get_lag_add_port_button())
            # check port in agg list
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_selected_port(
                vim_port)
            if element is None:
                logger.info("selected vim port not found, exit")
                pytest.fail("port error")

            # Try to add a wireframe copper port
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_port(
                wireframe_port)
            if element is None:
                logger.info("Couldn't get copper port, exit")
                pytest.fail("port get error")
            auto_actions.click(element)
            auto_actions.click(xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                               get_lag_add_port_button())
            # check port in agg list
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_selected_port(
                wireframe_port)
            if element is not None:
                logger.info("selected copper port is found, exit")
                pytest.fail("port error")

            tool_tip_text = ""
            tip_box_error = xiq_library_at_class_level.xflowsconfigureCommonObjects.cobj_web_elements.get_ui_tipbox_error()
            if tip_box_error:
                tool_tip_text = tip_box_error.text
            retry = 0
            while retry < 15:
                if "You cannot aggregate Ethernet ports with SFP ports" in tool_tip_text or "Selected ports have different maximum speeds and cannot be part of the same LAG." in tool_tip_text:
                    logger.info("Negative Scenario Validated, Error Received. \n "
                                "Tool tip Text Displayed on Page: ", tool_tip_text)
                    break
                logger.info(
                    f"Tool tip for port aggr error not found in {tool_tip_text}, retry: {retry} ")
                tip_box_error = xiq_library_at_class_level.xflowsconfigureCommonObjects.cobj_web_elements.get_ui_tipbox_error()
                if tip_box_error:
                    tool_tip_text = tip_box_error.text
                retry += 1

            if retry >= 15:
                logger.info("Tool tip for port aggr error not found in: ", tool_tip_text)
                pytest.fail("Tool tip for port aggr error not found")

            auto_actions.click(xiq_library_at_class_level.xflowscommonGlobalSearch.global_web_elements.
                               get_tool_tip_error_close_button())

            # Try to add an SFP port
            if sfp_port is not None:
                element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_port(
                    sfp_port)
                if element is None:
                    logger.info("Couldn't get fiber port, exit")
                    pytest.fail("port get error")
                auto_actions.click(element)
                auto_actions.click(
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_lag_add_port_button())

                # check port in agg list
                element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_selected_port(
                    sfp_port)
                if element is not None:
                    logger.info("selected fiber port is found, exit")
                    pytest.fail("port error")

                tool_tip_text = ""
                tip_box_error = xiq_library_at_class_level.xflowsconfigureCommonObjects.cobj_web_elements.get_ui_tipbox_error()
                if tip_box_error:
                    tool_tip_text = tip_box_error.text
                retry = 0
                while retry < 15:
                    if "Only VIM ports within the same VIM can be part of the same LAG" in tool_tip_text:
                        logger.info("Negative Scenario Validated, Error Received. \n "
                                    "Tool tip Text Displayed on Page: ", tool_tip_text)
                        break
                    logger.info(
                        f"Tool tip for port aggr error not found in {tool_tip_text}, retry: {retry} ")
                    tip_box_error = xiq_library_at_class_level.xflowsconfigureCommonObjects.cobj_web_elements.get_ui_tipbox_error()
                    if tip_box_error:
                        tool_tip_text = tip_box_error.text
                    retry += 1

                if retry >= 15:
                    logger.info("Tool tip for port aggr error not found in: ",
                                tool_tip_text)
                    pytest.fail("Tool tip for port aggr error not found")

                auto_actions.click(xiq_library_at_class_level.xflowscommonGlobalSearch.global_web_elements.
                                   get_tool_tip_error_close_button())

            logger.info("Close Assign Aggregate Ports Window")
            auto_actions.click(xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                               get_cancel_button())
            logger.info("-------------------------------------------------------------")
            logger.info("Try again, different order: First Wired Copper Port, then VIM")
            logger.info("------------------------------")
            auto_actions.click(
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_assign_button())
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements. \
                get_sw_template_assign_advanced_actions()
            auto_actions.move_to_element(element)
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements. \
                get_sw_template_assign_advanced_actions_aggr()
            auto_actions.move_to_element(element)
            auto_actions.click(element)
            # Try to add a wireframe copper port
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_port(
                wireframe_port)
            if element is None:
                logger.info("Couldn't get copper port, exit")
                pytest.fail("port get error")
            auto_actions.click(element)
            auto_actions.click(
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_lag_add_port_button())
            # check port in agg list
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_selected_port(
                wireframe_port)
            if element is None:
                logger.info("selected copper port is not found, exit")
                pytest.fail("port error")

            # Add VIM port
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_port(
                vim_port)
            if element is None:
                logger.info("Couldn't get vim port, exit")
                pytest.fail("port get error")
            auto_actions.click(element)
            auto_actions.click(
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_lag_add_port_button())
            # check port in agg list
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_selected_port(
                vim_port)
            if element is not None:
                logger.info("selected vim port is found, exit")
                pytest.fail("port error")

            tool_tip_text = ""
            tip_box_error = xiq_library_at_class_level.xflowsconfigureCommonObjects.cobj_web_elements.get_ui_tipbox_error()
            if tip_box_error:
                tool_tip_text = tip_box_error.text
            retry = 0
            while retry < 15:
                if "You cannot aggregate Ethernet ports with SFP ports" in tool_tip_text or "Selected ports have different maximum speeds and cannot be part of the same LAG." in tool_tip_text:
                    logger.info("Negative Scenario Validated, Error Received. \n "
                                "Tool tip Text Displayed on Page: ", tool_tip_text)
                    break
                logger.info(
                    f"Tool tip for port aggr error not found in {tool_tip_text}, retry: {retry} ")
                tip_box_error = xiq_library_at_class_level.xflowsconfigureCommonObjects.cobj_web_elements.get_ui_tipbox_error()
                if tip_box_error:
                    tool_tip_text = tip_box_error.text
                retry += 1

            if retry >= 15:
                logger.info("Tool tip for port aggr error not found in: ",
                            tool_tip_text)
                pytest.fail("Tool tip for port aggr error not found")

            auto_actions.click(
                xiq_library_at_class_level.xflowscommonGlobalSearch.global_web_elements.get_tool_tip_error_close_button())
            logger.info("Close Assign Aggregate Ports Window")
            auto_actions.click(xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                               get_cancel_button())
        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_20606_teardown'
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            logger.info("-------END TEST_TCXM_20608-------")

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_20618
    @pytest.mark.p1
    def test_tcxm_20618(self, node_1, logger, node_1_policy_name, node_1_template_name,
                        xiq_library_at_class_level, loaded_config, enter_switch_cli):
        """
        Author        : abolojan
        Modified by   : mchelu
        Date          : 5/30/2022
        Description   : Verify that Configuration Audit reflects the changes when VIM ports are added to the LACP using Aggregate Ports button from Switch Template.
        Steps         : Step    Description
                         0      Use devices with 4 ports VIM module (10 or 25 G ports) and aggregate them according to tests requirements.
                                Supported devices: 5520-24T, 5520-24W, 5520-48T, 5520-48W, 5520-12MW-36W, 5520-24X, 5520-48SE, 5520-VIM-4X, 5520-VIM-4XE, 5520-VIM-4YE.
                                Tested EXOS devices: 5520-48SE with 5520-VIM-4XE, 5520-24W with 5520-VIM-4X, 5520-24T with 5520-VIM-4YE.
                         1      Onboard the EXOS 5520 standalone.
                         2      Create a Network Policy with specific 5520 template.
                         3      Assign the previously created Network Policy to the device and update the device.
                         4      Using the Aggregate Ports button from Switch Template -> Port Configuration aggregate 2 VIM ports.
                         5      Check Devices -> Configuration Audit button status and Delta CLI.
                         6      Update the device, check the results in CLI and check the number of LACP ports in Switch Template -> Port Configuration table.
                         7      Using the Switch Template -> Port Configuration remove all VIM ports from the LACP.
                         8      Check Devices -> Configuration Audit button status and Delta CLI.
                         9      Update the device, check the results in CLI and check the number of LACP ports in Switch Template -> Port Configuration table.
        """

        vim_ports = []
        main_lag_port = ""
        sw_template_web_elements = SwitchTemplateWebElements()
        loaded_config['${TEST_NAME}'] = 'test_tcxm_20618_run'
        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name,
                                                                                        node_1_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            logger.info("Get all available ports.")
            all_ports = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_device_template_no_of_ports()
            total_number_of_ports = len(all_ports)
            first_vim_port = str(total_number_of_ports)
            second_vim_port = str(total_number_of_ports - 1)
            # Aggregate 2 VIM ports
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.create_modify_lag_in_template(first_vim_port,
                                                                                                   [second_vim_port],
                                                                                                   device='standalone')
            main_lag_port = first_vim_port
            vim_ports = [first_vim_port, second_vim_port]
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            time.sleep(2)
            # check the configuration audit button
            configuration_audit_status = xiq_library_at_class_level.xflowsmanageDevices.get_device_configuration_audit_status(
                device_serial=node_1.serial)
            logger.info(f"Configuration audit button after LAG creation: {configuration_audit_status}")
            count = 0
            while configuration_audit_status != 'audit mismatch':
                configuration_audit_status = xiq_library_at_class_level.xflowsmanageDevices.get_device_configuration_audit_status(
                    device_serial=node_1.serial)
                time.sleep(3)
                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                count += 1
                logger.info(f"Config audit not yet orange. Count {count}")
                if count == 5:
                    pytest.fail(f"Configuration audit status is {configuration_audit_status}")

            # check delta CLI
            delta_cli = xiq_library_at_class_level.xflowsmanageDeviceConfig.check_config_audit_delta_match(
                serial=node_1.serial)
            logger.info(f" Delta CLI after LAG creation: {delta_cli}")

            expected_delta_cli = f"enable sharing {first_vim_port} grouping {second_vim_port},{first_vim_port}"
            if expected_delta_cli not in delta_cli:
                pytest.fail(f'Delta CLI mismatch, expected: {expected_delta_cli}, found: {delta_cli}')

            # update the device
            xiq_library_at_class_level.xflowsmanageDevices.update_switch_policy_and_configuration(
                device_serial=node_1.serial)

            # check the results in CLI
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {first_vim_port} grouping {second_vim_port}-{first_vim_port}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")

            # remove all VIM ports from LACP
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name,
                                                                                        node_1_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            logger.info(f"Removing ports {vim_ports} from lag {main_lag_port} LAG")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.remove_lag_in_template(main_lag_port, vim_ports,
                                                                                            device='standalone')
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()

            # check the configuration audit button
            configuration_audit_status = xiq_library_at_class_level.xflowsmanageDevices.get_device_configuration_audit_status(
                device_serial=node_1.serial)
            logger.info(f"Configuration audit after LAG deletion: {configuration_audit_status}")
            count = 0
            while configuration_audit_status != 'audit mismatch':
                configuration_audit_status = xiq_library_at_class_level.xflowsmanageDevices.get_device_configuration_audit_status(
                    device_serial=node_1.serial)
                time.sleep(3)
                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                count += 1
                logger.info(f"Config audit not yet orange. Count {count}")
                if count == 5:
                    pytest.fail(f"Configuration audit status is {configuration_audit_status}")

            # check delta CLI
            delta_cli = xiq_library_at_class_level.xflowsmanageDeviceConfig.check_config_audit_delta_match(
                serial=node_1.serial)
            logger.info(f"Delta CLI after LAG deletion: {delta_cli}")

            expected_delta_cli = f"disable sharing {main_lag_port}"
            if expected_delta_cli not in delta_cli:
                pytest.fail(f'Delta CLI mismatch, expected: {expected_delta_cli}, found: {delta_cli}')

            # update the device
            xiq_library_at_class_level.xflowsmanageDevices.update_switch_policy_and_configuration(
                device_serial=node_1.serial)

            # check the results in CLI
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            assert "enable sharing" not in result, f"Lag is still present in CLI."

            # check the number of LACP ports in switch template -> port configuration
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(nw_policy=node_1_policy_name,
                                                                                        sw_template=node_1_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            labels = sw_template_web_elements.get_lag_span(lag=main_lag_port)

            if labels is not None:
                pytest.fail("Invalid number of LACP ports in the switch template -> port configuration table")
            else:
                logger.info("Label is not visible anymore in switch template!")
                main_lag_port = ""
        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_20618_teardown'
            if main_lag_port != "":
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name,
                                                                                            node_1_template_name)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                logger.info(f"Removing ports {vim_ports} from lag {main_lag_port} LAG")
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.remove_lag_in_template(main_lag_port,
                                                                                                vim_ports,
                                                                                                device='standalone')

                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                    device_mac=node_1.mac) == 1, "Could not update the device"
                with enter_switch_cli(node_1) as dev_cmd:
                    output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
                result = output[0].return_text
                assert "enable sharing" not in result, f"Lag is still present in CLI."

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_20630
    @pytest.mark.p2
    def test_tcxm_20630(self, node_1, logger, auto_actions,
                        xiq_library_at_class_level, loaded_config, enter_switch_cli):
        """
        Author        : tapostol
        Modified by   : mchelu
        Description   : Verify that different LAGs can be configured across different port modules when LACP is created
                        using Device Level Configuration.
        Preconditions : Use EXOS 5520 devices with 4 ports VIM module.
        Step	Step Description
        1	    Onboard the EXOS 5520 standalone.
        2	    Create a Network Policy with specific 5520 template.
        3	    Assign the previously created Network Policy to the device and update the device.
        4	    Using D360 -> Port Configuration aggregate 2 VIM ports from the VIM module.
        5	    Using D360 -> Port Configuration aggregate 2 VIM ports from the same VIM module.
        6	    Using D360 -> Port Configuration aggregate 2 fixed panel ports.
        7	    Update the device, check the results in CLI and check the number of LACP ports in D360 -> Port
                Configuration table.
        8	    Using D360 -> Port Configuration remove all ports from all LAGs.
        9	    Update the device, check the results in CLI and check the number of LACP ports in D360 -> Port
                Configuration table.
        """
        # self.executionHelper.testSkipCheck()
        loaded_config['${TEST_NAME}'] = 'test_tcxm_20630_run'
        # self.network_manager.connect_to_network_element_name(node_1.name)
        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            button_settings = xiq_library_at_class_level.xflowsmanageDevice360.dev360. \
                get_d360_configure_port_settings_aggregation_tab_button()
            assert button_settings, "Could not find port settings & aggregation button"
            auto_actions.click(button_settings)

            # Get list of ports (4 VIM and 2 fixed)
            ports_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_configure_port_rows()
            assert ports_rows, "Could not extract port list from Device360"
            ports_no = len(ports_rows)
            ports_used = [str(ports_no), str(ports_no - 1), str(ports_no - 2), str(ports_no - 3), str(ports_no - 4),
                          str(ports_no - 5)]
            # Aggregate 2 VIM ports
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_aggregate_ports(
                [ports_used[0], ports_used[1]], False,
                device="standalone"), \
                f"Could not aggregate ports {ports_used[0]} and {ports_used[1]}"

            # Aggregate next 2 VIM ports
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_aggregate_ports(
                [ports_used[2], ports_used[3]], False,
                device="standalone"), \
                f"Could not aggregate ports {ports_used[2]} and {ports_used[3]}"

            # Aggregate 2 fixed ports
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_aggregate_ports(
                [ports_used[4], ports_used[5]], False,
                device="standalone"), \
                f"Could not aggregate ports {ports_used[4]} and {ports_used[5]}"

            # Push changes to the device
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowscommonDevices.update_switch_policy_and_configuration(
                device_serial=node_1.serial) == 1, "Could not update the device"

            # Check aggregation ports added in Device360 and on dut CLI
            logger.info("Verify CLI output")
            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = [f'enable sharing {ports_used[0]} grouping {ports_used[1]}-{ports_used[0]}',
                               f'enable sharing {ports_used[2]} grouping {ports_used[3]}-{ports_used[2]}',
                               f'enable sharing {ports_used[4]} grouping {ports_used[5]}-{ports_used[4]}']
            assert all(cmd in result for cmd in expected_result), f"CLI commands does not correspond. {expected_result}" \
                                                                  f"!= {result}"

            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            button_settings = xiq_library_at_class_level.xflowsmanageDevice360.dev360. \
                get_d360_configure_port_settings_aggregation_tab_button()
            assert button_settings, "Could not find port settings & aggregation button"
            auto_actions.click(button_settings)
            time.sleep(5)
            # Remove aggregation for 2 VIM ports
            xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(ports_used[0],
                                                                                            [ports_used[0],
                                                                                             ports_used[1]],
                                                                                            action='remove',
                                                                                            device="standalone")
            # Remove aggregation for 2 VIM ports
            xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(ports_used[2],
                                                                                            [ports_used[2],
                                                                                             ports_used[3]],
                                                                                            action='remove',
                                                                                            device="standalone")

            # Remove aggregation for 2 fixed ports
            xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(ports_used[4],
                                                                                            [ports_used[4],
                                                                                             ports_used[5]],
                                                                                            action='remove',
                                                                                            device="standalone")

            # Push changes to the device
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowscommonDevices.update_switch_policy_and_configuration(
                node_1.serial) == 1, "Could not update the device"

            with enter_switch_cli(node_1) as dev_cmd:
                output = dev_cmd.send_cmd(node_1.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            assert "enable sharing" not in result, f"Lag is still present in CLI."

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_20630_teardown'
            xiq_library_at_class_level.xflowsmanageDevices.revert_device_to_template(node_1.serial)

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.tcxm_20636
    @pytest.mark.p1
    def test_tcxm_20636(self, node_stack, logger, utils,
                        xiq_library_at_class_level, loaded_config, auto_actions, enter_switch_cli):
        """
        Author        : rvisterineanu
        Modified by   : mchelu
        Description   : Verify that VIM ports can be removed from the existing LACP.
        Preconditions : Use EXOS 5520 stack
         Step	Step Description
         1	    Onboard the EXOS 5520 stack.
         2	    Create a Network Policy with specific 5520 template.
         3	    Assign the previously created Network Policy to the device and update the device.
         4	    Using D360 -> Port configuration aggregate 2 VIM ports.
         5	    Update the device, check the results in CLI and check the number of LACP ports in D360.
         6	    Using D360 -> Port Configuration add 3rd VIM port to the LACP.
         7      Update the device, check the results in CLI and check the number of LACP ports in D360.
         8      Using D360 -> Port Configuration add 4th VIM port to the LACP.
         9      Update the device, check the results in CLI and check the number of LACP ports in D360.
         10     Using D360 -> Port Configuration remove all VIM ports from the LACP.
         11     Update the device, check the results in CLI and check the number of LACP ports in D360.

         """

        loaded_config['${TEST_NAME}'] = 'test_tcxm_20636_run'
        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_stack.mac)
            logger.step("Navigate to Device360->Port Configuration->Port Settings & Aggregation")
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration() == 1
            auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_d360_configure_port_settings_aggregation_tab_button)

            logger.step("Select unit from stack with VIM ports")
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show version | in VIM', max_wait=10, interval=2)
            result = output[0].return_text
            p = re.compile(r'([a-zA-Z0-9-]*d*VIM.*\d) {2,}:', re.M)
            vim_slots_list = re.findall(p, result)
            logger.info(f"Slots with VIM are : {vim_slots_list}")
            first_slot_with_vim = vim_slots_list[0]
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_change_slot_view(first_slot_with_vim[-1])

            logger.step("Aggregate 2 VIM ports")
            number_of_aggregated_ports = 0
            ports_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_configure_port_rows()
            assert ports_rows, "Could not extract port list from Device360"
            ports_no = len(ports_rows)
            first_vim_port = first_slot_with_vim[-1] + ":" + str(ports_no)
            second_vim_port = first_slot_with_vim[-1] + ":" + str(ports_no - 1)
            third_vim_port = first_slot_with_vim[-1] + ":" + str(ports_no - 2)
            fourth_vim_port = first_slot_with_vim[-1] + ":" + str(ports_no - 3)
            ports_used = [first_vim_port, second_vim_port]
            number_of_aggregated_ports += 2
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_aggregate_ports(ports_used,
                                                                                              device='stack'), \
                f"Could not aggregate ports {ports_used}"

            logger.step("Update the device and check LACP in Device360 and CLI")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, \
                "Could not update the device"

            logger.step("Navigate to Device360->Port Configuration->Port Settings & Aggregation")
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_stack.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            auto_actions.click_reference(xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_d360_configure_port_settings_aggregation_tab_button)

            logger.step("Select unit from stack with VIM ports")
            xiq_library_at_class_level.xflowsmanageDevice360.device360_change_slot_view(first_slot_with_vim[-1])
            lag_rows = xiq_library_at_class_level.xflowsmanageDevice360. \
                get_device360_configure_aggregated_port_settings_aggregation_rows()
            assert len(lag_rows) == number_of_aggregated_ports, \
                f"The number of aggregated ports is not {number_of_aggregated_ports}"

            lacp_ports_d360 = [second_vim_port + "-" + str(ports_no)]
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show configuration | i sharing',
                                          max_wait=10, interval=2)
            p = re.compile(r'\d:\d+-\d:\d+|\d:\d+,\d:\d+|\d:\d+-\d+', re.M)
            lacp_list_ports_from_dut = re.findall(p, output[0].return_text)
            logger.info(f"Lacp ports from dut are: {lacp_list_ports_from_dut}")
            assert lacp_list_ports_from_dut == lacp_ports_d360, "Ports do not match to CLI"

            logger.step("Add 3rd VIM port")
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(first_vim_port,
                                                                                                   [third_vim_port],
                                                                                                   device='stack') == 1, f"Port {third_vim_port} wasn't added"

            logger.step("Update the device and check LACP in Device360 and CLI")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, "Could not update the device"

            logger.step("Navigate to Device360->Port Configuration->Port Settings & Aggregation")
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_stack.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_d360_configure_port_settings_aggregation_tab_button)

            logger.step("Select unit from stack with VIM ports")
            xiq_library_at_class_level.xflowsmanageDevice360.device360_change_slot_view(first_slot_with_vim[-1])
            number_of_aggregated_ports += 1
            lag_rows = xiq_library_at_class_level.xflowsmanageDevice360. \
                get_device360_configure_aggregated_port_settings_aggregation_rows()
            assert len(lag_rows) == number_of_aggregated_ports, \
                f"The number of aggregated ports is not {number_of_aggregated_ports}"
            lacp_ports_d360 = [third_vim_port + "-" + str(ports_no)]
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show configuration | i sharing',
                                          max_wait=10, interval=2)
            p = re.compile(r'\d:\d+-\d:\d+|\d:\d+,\d:\d+|\d:\d+-\d+', re.M)
            lacp_list_ports_from_dut = re.findall(p, output[0].return_text)
            logger.info(f"Lacp ports from dut are: {lacp_list_ports_from_dut}")
            assert lacp_list_ports_from_dut == lacp_ports_d360, "Ports do not match to CLI"

            # Add 4th VIM port
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(first_vim_port,
                                                                                                   [fourth_vim_port],
                                                                                                   device="stack") == 1, f"Port {fourth_vim_port} wasn't added"

            logger.step("Update the device and check LACP in Device360 and CLI")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, "Could not update the device"

            logger.step("Navigate to Device360->Port Configuration->Port Settings & Aggregation")
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_stack.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_d360_configure_port_settings_aggregation_tab_button)

            logger.step("Select unit from stack with VIM ports")
            xiq_library_at_class_level.xflowsmanageDevice360.device360_change_slot_view(first_slot_with_vim[-1])
            number_of_aggregated_ports += 1
            logger.info(f'The no of aggregated ports is {number_of_aggregated_ports}')
            lag_rows = xiq_library_at_class_level.xflowsmanageDevice360. \
                get_device360_configure_aggregated_port_settings_aggregation_rows()
            assert len(lag_rows) == number_of_aggregated_ports, \
                f"The number of aggregated ports is not {number_of_aggregated_ports}"
            lacp_ports_d360 = [fourth_vim_port + "-" + str(ports_no)]
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show configuration | i sharing',
                                          max_wait=10, interval=2)
            p = re.compile(r'\d:\d+-\d:\d+|\d:\d+,\d:\d+|\d:\d+-\d+', re.M)
            lacp_list_ports_from_dut = re.findall(p, output[0].return_text)
            logger.info(f"Lacp ports from dut are: {lacp_list_ports_from_dut}")
            assert lacp_list_ports_from_dut == lacp_ports_d360, "Ports do not match to CLI"

            logger.step("Remove VIM ports from LAG")
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(first_vim_port,
                                                                                                   [first_vim_port,
                                                                                                    second_vim_port,
                                                                                                    third_vim_port,
                                                                                                    fourth_vim_port],
                                                                                                   action='remove',
                                                                                                   device="stack") == 1, f"LAG {first_vim_port} was not removed"

            logger.step("Update the device and check LACP in Device360 and CLI")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, "Could not update the device"

            logger.step("Navigate to Device360->Port Configuration->Port Settings & Aggregation")
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_stack.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_d360_configure_port_settings_aggregation_tab_button)

            logger.step("Select unit from stack with VIM ports")
            xiq_library_at_class_level.xflowsmanageDevice360.device360_change_slot_view(first_slot_with_vim[-1])
            number_of_aggregated_ports -= 4
            logger.info(f'the no of aggregated ports is {number_of_aggregated_ports}')
            lag_rows = xiq_library_at_class_level.xflowsmanageDevice360. \
                get_device360_configure_aggregated_port_settings_aggregation_rows()
            assert lag_rows is None, \
                f"The number of aggregated ports is not {number_of_aggregated_ports}"
            lacp_ports_d360 = []
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show configuration | i sharing',
                                          max_wait=10, interval=2)
            p = re.compile(r'\d:\d+-\d:\d+|\d:\d+,\d:\d+|\d:\d+-\d+', re.M)
            lacp_list_ports_from_dut = re.findall(p, output[0].return_text)
            logger.info(f"Lacp ports from dut are: {lacp_list_ports_from_dut}")
            assert lacp_list_ports_from_dut == lacp_ports_d360, "Ports do not match to CLI"

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_20636_teardown'
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            xiq_library_at_class_level.xflowsmanageDevices.revert_device_to_template(node_stack.mac)

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.tcxm_20637
    @pytest.mark.p1
    def test_tcxm_20637(self, node_stack, logger, node_stack_policy_name, node_stack_template_name,
                        xiq_library_at_class_level, loaded_config, auto_actions, enter_switch_cli):
        """
        Author        : rvisterineanu
        Modified by   : mchelu
        Description   : [STACK] Verify that LACP for VIM ports can be created using Aggregate Ports Across Stack button from Switch Template.
        Preconditions : Use EXOS 5520 stack
         Step	Step Description
         1	    Onboard the EXOS 5520 stack with only one VIM module.
         2	    Create a Network Policy with specific 5520 template.
         3	    Assign the previously created Network Policy to the device and update the device.
         4	    Using the Aggregate Ports Across Stack button from Switch Template -> Port configuration aggregate 2 VIM ports.
         5	    Update the device, check the results in CLI.
         6	    Using the Switch Template -> Port Configuration add 3rd VIM port to the LACP.
         7      Update the device, check the results in CLI.
         8      Using the Switch Template -> Port Configuration add 4th VIM port to the LACP.
         9      Update the device, check the results in CLI.
         10     Using the Switch Template -> Port Configuration remove all VIM ports from the LACP.
         """

        loaded_config['${TEST_NAME}'] = 'test_tcxm_20637_run'
        sw_template_web_elements = SwitchTemplateWebElements()
        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            logger.info("Setup variables")
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show version | in VIM', max_wait=10, interval=2)
            result = output[0].return_text
            p = re.compile(r'([a-zA-Z0-9-]*d*VIM.*\d) {2,}:', re.M)
            vim_slots_list = re.findall(p, result)
            first_slot_with_vim = vim_slots_list[0]
            logger.info(f"Slots with VIM are : {vim_slots_list}")

            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_stack_policy_name,
                                                                                        node_stack_template_name)
            auto_actions.click(sw_template_web_elements.get_template_link(template=node_stack_template_name))
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(
                first_slot_with_vim[-1])
            all_ports = sw_template_web_elements.get_device_template_no_of_ports()
            total_number_of_ports = len(all_ports)
            first_vim_port = first_slot_with_vim[-1] + ":" + str(total_number_of_ports)
            second_vim_port = first_slot_with_vim[-1] + ":" + str(total_number_of_ports - 1)
            third_vim_port = first_slot_with_vim[-1] + ":" + str(total_number_of_ports - 2)
            fourth_vim_port = first_slot_with_vim[-1] + ":" + str(total_number_of_ports - 3)
            logger.info("Aggregate 2 VIM ports.")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.create_modify_lag_in_template(first_vim_port,
                                                                                                   [second_vim_port],
                                                                                                   device='stack')
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, "Could not update the device"

            logger.info("Check with CLI for the first 2 VIM.")
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {first_vim_port} grouping {second_vim_port}-{first_vim_port.split(":")[1]}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")

            logger.info("Verify the existing LAG and add 3rd VIM port")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_stack_policy_name,
                                                                                        node_stack_template_name)
            auto_actions.click(sw_template_web_elements.get_template_link(template=node_stack_template_name))
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(
                first_slot_with_vim[-1])
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.create_modify_lag_in_template(first_vim_port,
                                                                                                   [third_vim_port],
                                                                                                   device="stack")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, "Could not update the device"
            logger.info("Check with CLI for the 3rd VIM port.")
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {first_vim_port} grouping {third_vim_port}-{first_vim_port.split(":")[1]}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")

            logger.info("Verify the existing LAG and add 4th VIM port")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_stack_policy_name,
                                                                                        node_stack_template_name)
            auto_actions.click(sw_template_web_elements.get_template_link(template=node_stack_template_name))
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(
                first_slot_with_vim[-1])
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.create_modify_lag_in_template(first_vim_port,
                                                                                                   [fourth_vim_port],
                                                                                                   device="stack")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, "Could not update the device"
            logger.info("Check with CLI for the 4th VIM port.")
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = f'enable sharing {first_vim_port} grouping {fourth_vim_port}-{first_vim_port.split(":")[1]}'
            if expected_result not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")

            logger.info("Remove all ports from LACP")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_stack_policy_name,
                                                                                        node_stack_template_name)
            auto_actions.click(sw_template_web_elements.get_template_link(template=node_stack_template_name))
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(
                first_slot_with_vim[-1])
            aggregated_ports = [first_vim_port, second_vim_port, third_vim_port, fourth_vim_port]
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.remove_lag_in_template(first_vim_port,
                                                                                            aggregated_ports,
                                                                                            device="stack")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, "Could not update the device"
            logger.info("Check with CLI if ports were removed.")
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            assert "enable sharing" not in result, f"Lag is still present in CLI."

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_20637_teardown'
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.tcxm_20638
    @pytest.mark.p1
    def test_tcxm_20638(self, node_stack, logger, utils, cloud_driver,
                        xiq_library_at_class_level, loaded_config, auto_actions, enter_switch_cli):
        """
        Author        : rvisterineanu
        Modified by   : mchelu
        Description   : Verify that VIM ports can be removed from the existing LACP.
        Preconditions : Use EXOS 5520 stack
         Step	Step Description
         1	    Onboard the EXOS 5520 stack.
         2	    Create a Network Policy with specific 5520 template.
         3	    Assign the previously created Network Policy to the device and update the device.
         4	    Using D360 -> Port configuration aggregate 4 VIM ports.
         5	    Update the device, check the results in CLI and check the number of LACP ports in D360.
         6	    Using D360 -> Port configuration remove 2 VIM ports from the LACP.
         7      Update the device, check the results in CLI and check the number of LACP ports in D360.
         8      Using D360 -> Port Configuration remove all VIM ports from the LACP.
         9      Update the device, check the results in CLI and check the number of LACP ports in D360.

         """
        cloud_driver.refresh_page()
        loaded_config['${TEST_NAME}'] = 'test_tcxm_20638_run'
        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show version | in VIM', max_wait=10, interval=2)
            result = output[0].return_text
            p = re.compile(r'([a-zA-Z0-9-]*d*VIM.*\d) {2,}:', re.M)
            vim_slots_list = re.findall(p, result)
            logger.info(f"Slots with VIM are : {vim_slots_list}")
            first_slot_with_vim = vim_slots_list[0]

            logger.step("Navigate to Device360->Port Configuration->Port Settings & Aggregation")
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_stack.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_d360_configure_port_settings_aggregation_tab_button)

            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_change_slot_view(first_slot_with_vim[-1])
            number_of_aggregated_ports = 0
            ports_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_configure_port_rows()
            assert ports_rows, "Could not extract port list from Device360"
            ports_no = len(ports_rows)
            first_vim_port = first_slot_with_vim[-1] + ":" + str(ports_no)
            second_vim_port = first_slot_with_vim[-1] + ":" + str(ports_no - 1)
            third_vim_port = first_slot_with_vim[-1] + ":" + str(ports_no - 2)
            fourth_vim_port = first_slot_with_vim[-1] + ":" + str(ports_no - 3)
            ports_used = [first_vim_port, second_vim_port, third_vim_port, fourth_vim_port]
            logger.info(f"Ports used {ports_used}")
            number_of_aggregated_ports += 4
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_aggregate_ports(ports_used,
                                                                                              device="stack"), \
                f"Could not aggregate ports {ports_used}"

            logger.info(f"Update the device and check LACP in Device360 and CLI")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, "Could not update the device"
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_stack.mac)
            logger.info(f"Navigate to Device360->Port Configuration->Port Settings & Aggregation")
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_d360_configure_port_settings_aggregation_tab_button)

            logger.step("Select unit from stack with VIM ports")
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_change_slot_view(first_slot_with_vim[-1])
            lag_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_configure_aggregated_port_settings_aggregation_rows()
            assert len(lag_rows) == number_of_aggregated_ports, \
                f"The number of aggregated ports is not {number_of_aggregated_ports}"

            lacp_ports_d360 = [fourth_vim_port + "-" + str(ports_no)]
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show configuration | i sharing',
                                          max_wait=10, interval=2)

            p = re.compile(r'\d:\d+-\d:\d+|\d:\d+,\d:\d+|\d:\d+-\d+', re.M)
            lacp_list_ports_from_dut = re.findall(p, output[0].return_text)
            logger.info(f"Lacp ports from dut are: {lacp_list_ports_from_dut}")
            assert lacp_list_ports_from_dut == lacp_ports_d360, "Ports do not match to CLI"

            logger.info(f"Remove 2 VIM ports")
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(first_vim_port,
                                                                                                   [first_vim_port,
                                                                                                    second_vim_port],
                                                                                                   action='remove',
                                                                                                   device='stack') == 1, \
                f"LAG {first_vim_port} and {second_vim_port} was not removed"

            logger.step("Update the device and check LACP in Device360 and CLI")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, "Could not update the device"
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_stack.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_d360_configure_port_settings_aggregation_tab_button)

            logger.step("Select unit from stack with VIM ports")
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_change_slot_view(first_slot_with_vim[-1])
            number_of_aggregated_ports -= 2
            lag_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_configure_aggregated_port_settings_aggregation_rows()
            assert len(lag_rows) == number_of_aggregated_ports, \
                f"The number of aggregated ports is not {number_of_aggregated_ports}"

            lacp_ports_d360 = [fourth_vim_port + "-" + str(ports_no - 2)]
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show configuration | i sharing',
                                          max_wait=10, interval=2)
            p = re.compile(r'\d:\d+-\d:\d+|\d:\d+,\d:\d+|\d:\d+-\d+', re.M)
            lacp_list_ports_from_dut = re.findall(p, output[0].return_text)
            logger.info(f"Lacp ports from dut are: {lacp_list_ports_from_dut}")
            assert lacp_list_ports_from_dut == lacp_ports_d360, "Ports do not match to CLI"

            logger.info(f"Remove the remaining VIM ports")
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(fourth_vim_port,
                                                                                                   [third_vim_port,
                                                                                                    fourth_vim_port],
                                                                                                   action='remove',
                                                                                                   device='stack') == 1, \
                f"LAG {third_vim_port} and {fourth_vim_port} were not removed"

            logger.step("Update the device and check LACP in Device360 and CLI")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, "Could not update the device"
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_stack.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_d360_configure_port_settings_aggregation_tab_button)

            logger.step("Select unit from stack with VIM ports")
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_change_slot_view(first_slot_with_vim[-1])
            number_of_aggregated_ports -= 2
            logger.info(f'the no of aggregated ports is {number_of_aggregated_ports}')
            lag_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_configure_aggregated_port_settings_aggregation_rows()
            assert lag_rows is None, \
                f"The number of aggregated ports is not {number_of_aggregated_ports}"
            lacp_ports_d360 = []
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show configuration | i sharing',
                                          max_wait=10, interval=2)
            p = re.compile(r'\d:\d+-\d:\d+|\d:\d+,\d:\d+|\d:\d+-\d+', re.M)
            lacp_list_ports_from_dut = re.findall(p, output[0].return_text)
            logger.info(f"Lacp ports from dut are: {lacp_list_ports_from_dut}")
            assert lacp_list_ports_from_dut == lacp_ports_d360, "Ports do not match to CLI"

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_20638_teardown'
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            xiq_library_at_class_level.xflowsmanageDevices.revert_device_to_template(node_stack.mac)

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.tcxm_20640
    @pytest.mark.p2
    def test_tcxm_20640(self, node_stack, logger, node_stack_policy_name, node_stack_template_name,
                        xiq_library_at_class_level, loaded_config, navigator, enter_switch_cli, auto_actions):
        """
         Author        : gburlacu
         Modified by   : mchelu
         Description   : Verify that LACP cannot be formed between VIM and fixed panel ports using Aggregate Ports
                         Across Stack button from Switch Template.
         Preconditions : Use EXOS 5520 stack
         Step	Step Description
         1	    Onboard the EXOS 5520 stack with only one VIM module.
         2	    Create a Network Policy with specific 5520 template.
         3	    Using the Aggregate Ports Across Stack button from Switch Template -> Port Configuration aggregate
                1 VIM port and 1 fixed panel port from the same stack slot.
         4	    Check if an error message appears.
         5	    Using the Aggregate Ports Across Stack button from Switch Template -> Port Configuration aggregate
                1 VIM port and 1 fixed panel port from different stack slot.
         6	    Check if an error message appears.
         """
        loaded_config['${TEST_NAME}'] = 'test_tcxm_20640_run'
        lst_errors = ["You cannot aggregate Ethernet ports with SFP ports.",
                      "Only VIM ports within the same VIM can be part of the same LAG",
                      "Selected ports have different maximum speeds and cannot be part of the same LAG."]
        sw_template_web_elements = SwitchTemplateWebElements()
        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show version | in VIM', max_wait=10, interval=2)
            result = output[0].return_text
            p = re.compile(r'([a-zA-Z0-9-]*d*VIM.*\d) {2,}:', re.M)
            vim_slots_list = re.findall(p, result)
            first_slot_with_vim = vim_slots_list[0]
            second_slot_with_vim = vim_slots_list[1]
            logger.info(f"Slots with VIM are : {vim_slots_list}")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_stack_policy_name,
                                                                                        node_stack_template_name)
            if sw_template_web_elements.get_sw_template_port_configuration_tab() is None:
                auto_actions.click(sw_template_web_elements.get_template_link(template=node_stack_template_name))
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(
                first_slot_with_vim[-1])
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            logger.info("Get all available ports for the first switch")
            all_ports = sw_template_web_elements.get_device_template_no_of_ports()
            auto_actions.click(
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_aggr_ports_across_stack_button())
            auto_actions.click(sw_template_web_elements.get_lacp_toggle_button())
            #logger.info("Get all available ports for the first switch")
            #all_ports = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_select_ports_available()
            total_number_of_ports = len(all_ports)
            port_fixed = f"{first_slot_with_vim[-1]}:1"
            port_vim = f"{first_slot_with_vim[-1]}:" + str(total_number_of_ports)

            logger.info("Aggregate 1 VIM port and 1 fixed panel port from the first stack slot.")
            auto_actions.click(sw_template_web_elements.get_available_port(port=port_fixed))
            auto_actions.click(sw_template_web_elements.get_lag_add_port_button())
            selected_port = sw_template_web_elements.get_selected_port(port=port_fixed)
            assert selected_port is not None, f"Port {port_fixed} wasn't added"
            logger.info(f"Try to aggregate {port_vim} with fixed port {port_fixed}")
            auto_actions.click(sw_template_web_elements.get_available_port(port=port_vim))
            auto_actions.click(sw_template_web_elements.get_lag_add_port_button())
            selected_port = sw_template_web_elements.get_selected_port(port=port_vim)
            assert selected_port is None, f"Port {port_vim} was added"
            error_message = sw_template_web_elements.get_error_message().text
            assert error_message in lst_errors, f"No error message was detected"
            auto_actions.click(
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_cancel_button())

            logger.info("Aggregate 1 VIM port from first slot and 1 fixed panel port from a different stack slot")
            auto_actions.click(
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_aggr_ports_across_stack_button())
            auto_actions.click(sw_template_web_elements.get_lacp_toggle_button())
            auto_actions.click(sw_template_web_elements.get_available_port(port=port_vim))
            auto_actions.click(sw_template_web_elements.get_lag_add_port_button())
            selected_port = sw_template_web_elements.get_selected_port(port=port_vim)
            assert selected_port is not None, f"Port {port_vim} wasn't added"

            auto_actions.click(
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_slot(
                    slot=second_slot_with_vim[-1]))
            port_fixed = f"{second_slot_with_vim[-1]}:1"
            logger.info(f"Try to aggregate {port_vim} with fixed port {port_fixed}")
            auto_actions.click(sw_template_web_elements.get_available_port(port=port_fixed))
            auto_actions.click(sw_template_web_elements.get_lag_add_port_button())
            selected_port = sw_template_web_elements.get_selected_port(port=port_fixed)
            assert selected_port is None, f"Port {port_fixed} was added"
            error_message = sw_template_web_elements.get_error_message().text
            assert error_message in lst_errors, f"No error message was detected"
            auto_actions.click(
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_cancel_button())
        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_20640_teardown'
            navigator.navigate_to_devices()

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.tcxm_20641
    @pytest.mark.p2
    def test_tcxm_20641(self, node_stack, logger, node_stack_policy_name, node_stack_template_name,
                        xiq_library_at_class_level, loaded_config, auto_actions, enter_switch_cli):
        """
        Author        : scostache
        Modified by   : mchelu
        TCXM-20641    : https://aerohive.qtestnet.com/p/101323/portal/project#tab=testdesign&object=1&id=55067659
        Description   : Verify that a fixed panel port cannot be added to and existing LACP for VIM ports
        when LACP was created using Aggregate Ports Across Stack button from Switch Template.
        Preconditions : Use EXOS 5520 stack
        No.   	Step Description
        1	    Onboard the EXOS 5520 stack with only one VIM module.
        2	    Create a Network Policy with specific 5520 template.
        3	    Using the Aggregate Ports Across Stack button from Switch Template -> Port Configuration aggregate
                2 VIM ports.
        4	    Check if an error message appears.
        5	    To existing LACP add a fixed panel port from the same stack slot.
            When editing the created LACP, there is no possibility of adding other ports besides the VIM ports from the same
            VIM module.
        6	    To existing LACP add a fixed panel port from different stack slot.
            When editing the created LACP, there is no possibility of adding other ports besides the VIM ports from the same
            VIM module.
        """
        loaded_config['${TEST_NAME}'] = 'test_tcxm_20641_run'
        sw_template_web_elements = SwitchTemplateWebElements()
        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            lst_errors = ["You cannot aggregate Ethernet ports with SFP ports.",
                          "Only VIM ports within the same VIM can be part of the same LAG"]
            logger.step("Aggregate 2 VIM ports")
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show version | in VIM', max_wait=10, interval=2)
            result = output[0].return_text
            p = re.compile(r'([a-zA-Z0-9-]*d*VIM.*\d) {2,}:', re.M)
            vim_slots_list = re.findall(p, result)
            first_slot_with_vim = vim_slots_list[0]
            logger.info(f"Slots with VIM are : {vim_slots_list}")

            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_stack_policy_name,
                                                                                        node_stack_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(
                first_slot_with_vim[-1])
            all_ports = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_device_template_no_of_ports()
            total_number_of_ports = len(all_ports)
            first_vim_port = first_slot_with_vim[-1] + ":" + str(total_number_of_ports)
            second_vim_port = first_slot_with_vim[-1] + ":" + str(total_number_of_ports - 1)
            fixed_panel_port = first_slot_with_vim[-1] + ":" + str(random.randint(1, total_number_of_ports - 4))
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.create_modify_lag_in_template(first_vim_port,
                                                                                                   [second_vim_port],
                                                                                                   device="stack")

            logger.info("Try adding Fix Panel Port from same stack")
            lag_text = first_vim_port + " LAG"
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_stack_policy_name,
                                                                                        node_stack_template_name)
            auto_actions.click(sw_template_web_elements.get_template_link(template=node_stack_template_name))
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(
                first_slot_with_vim[-1])
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            auto_actions.scroll_down()
            auto_actions.scroll_bottom()
            lag_link = sw_template_web_elements.get_lag_span(lag=first_vim_port)
            if lag_link is not None:
                auto_actions.click(lag_link)
            else:
                pytest.fail("LAG is not found!")
            logger.info("Try to add port ", fixed_panel_port, " to lag group ", lag_text)
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements. \
                get_available_port(port=fixed_panel_port)
            assert element is None, f"Port {fixed_panel_port} is found and it shouldn't"
            logger.info("Scenario validated: cannot add fixed panel port in VIM Lag")

            logger.info(f"Try adding Fix Panel Port from slot number {vim_slots_list[1][-1]}")
            logger.info(f"Try to find if slot {vim_slots_list[1][-1]} is available for lag group {first_vim_port}")
            element = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_slot(
                slot=vim_slots_list[1][-1])
            assert element is None, f"Slot {vim_slots_list[1][-1]} is found and it shouldn't"
            logger.info("Scenario validated: cannot add fixed ports in VIM Lag")
            auto_actions.click_reference(
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_cancel_button)
        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_20641_teardown'
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_stack_policy_name,
                                                                                        node_stack_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(
                first_slot_with_vim[-1])
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.remove_lag_in_template(first_vim_port,
                                                                                            [first_vim_port,
                                                                                             second_vim_port],
                                                                                            device="stack")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, \
                "Could not update the device"
            logger.info("-------END TEST_TCXM_20641-------")

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.tcxm_20651
    @pytest.mark.p1
    def test_tcxm_20651(self, node_stack, logger, node_stack_policy_name, node_stack_template_name,
                        xiq_library_at_class_level, loaded_config, auto_actions, enter_switch_cli):
        """
        Author        : abolojan
        Modified by   : mchelu
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

        ports_aggregated = False
        ports_aggregated_device_updated = False
        ports_not_aggregated = False
        ports_not_aggregated_device_updated = False
        loaded_config['${TEST_NAME}'] = 'test_tcxm_20651_run'
        sw_template_web_elements = SwitchTemplateWebElements()

        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            # check the configuration audit button
            configuration_audit_status = xiq_library_at_class_level.xflowsmanageDevices.get_device_configuration_audit_status(
                device_mac=node_stack.mac)
            logger.info(f"Configuration audit at the beginning of the test: {configuration_audit_status}")

            if configuration_audit_status == 'audit mismatch':
                logger.step("update the device (in order to apply the policy for the first time)")
                xiq_library_at_class_level.xflowsmanageDevices.update_switch_policy_and_configuration(
                    device_mac=node_stack.mac)

            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show version | in VIM', max_wait=10, interval=2)
            result = output[0].return_text
            p = re.compile(r'([a-zA-Z0-9-]*d*VIM.*\d) {2,}:', re.M)
            vim_slots_list = re.findall(p, result)
            first_slot_with_vim = vim_slots_list[0]
            logger.info(f"Slots with VIM are : {vim_slots_list}")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_stack_policy_name,
                                                                                        node_stack_template_name)
            auto_actions.click(sw_template_web_elements.get_template_link(template=node_stack_template_name))
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(
                first_slot_with_vim[-1])
            all_ports = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_device_template_no_of_ports()
            total_number_of_ports = len(all_ports)
            first_vim_port = first_slot_with_vim[-1] + ":" + str(total_number_of_ports)
            second_vim_port = first_slot_with_vim[-1] + ":" + str(total_number_of_ports - 1)
            ports = [first_vim_port, second_vim_port]
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.create_modify_lag_in_template(first_vim_port,
                                                                                                   [second_vim_port],
                                                                                                   device="stack")
            xiq_library_at_class_level.xflowsmanageDevices.navigator.navigate_to_devices()
            ports_aggregated = True

            logger.step("check the configuration audit button")
            configuration_audit_status = xiq_library_at_class_level.xflowsmanageDevices.get_device_configuration_audit_status(
                device_mac=node_stack.mac)
            logger.info(f"Configuration audit button after LAG creation: {configuration_audit_status}")
            count = 0
            while configuration_audit_status != 'audit mismatch':
                configuration_audit_status = xiq_library_at_class_level.xflowsmanageDevices.get_device_configuration_audit_status(
                    device_mac=node_stack.mac)
                time.sleep(5)
                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                count += 1
                logger.info(f"Config audit not yet orange. Count {count}")
                if count == 5:
                    pytest.fail(f"Configuration audit status is {configuration_audit_status}")

            logger.step("check delta CLI")
            delta_cli = xiq_library_at_class_level.xflowsmanageDeviceConfig.get_device_config_audit_delta(
                node_stack.mac)
            logger.info(f" Delta CLI after LAG creation: {delta_cli}")
            expected_delta_cli = [f"enable sharing {ports[0]} grouping {ports[0]},{ports[1]} lacp",
                                  f"enable sharing {ports[0]} grouping {ports[1]},{ports[0]} lacp"]
            if expected_delta_cli[0] not in delta_cli and expected_delta_cli[1] not in delta_cli:
                pytest.fail(f'Delta CLI mismatch, expected: {expected_delta_cli}, found: {delta_cli}')

            logger.step("update the device")
            xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, \
                "Could not update the device"
            ports_aggregated_device_updated = True

            logger.step("check the results in CLI")
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            expected_result = [f'enable sharing {ports[0]} grouping {ports[0]}-{ports[1].split(":")[1]}',
                               f'enable sharing {ports[0]} grouping {ports[1]}-{ports[0].split(":")[1]}']
            if expected_result[0] not in result and expected_result[1] not in result:
                pytest.fail(f"Expected result: {expected_result}, actual result: {result}")

            logger.step("remove all VIM ports from LACP")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_stack_policy_name,
                                                                                        node_stack_template_name)
            auto_actions.click(sw_template_web_elements.get_template_link(template=node_stack_template_name))
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(
                first_slot_with_vim[-1])
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.remove_lag_in_template(first_vim_port, ports,
                                                                                            device="stack")
            xiq_library_at_class_level.xflowsmanageDevices.navigator.navigate_to_devices()
            ports_not_aggregated = True

            logger.step("check the configuration audit button")
            configuration_audit_status = xiq_library_at_class_level.xflowsmanageDevices.get_device_configuration_audit_status(
                device_mac=node_stack.mac)
            logger.info(f"Configuration audit after LAG deletion: {configuration_audit_status}")
            count = 0
            while configuration_audit_status != 'audit mismatch':
                configuration_audit_status = xiq_library_at_class_level.xflowsmanageDevices.get_device_configuration_audit_status(
                    device_mac=node_stack.mac)
                time.sleep(5)
                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                count += 1
                logger.info(f"Config audit not yet orange. Count {count}")
                if count == 5:
                    pytest.fail(f"Configuration audit status is {configuration_audit_status}")

            logger.step("check delta CLI")
            delta_cli = xiq_library_at_class_level.xflowsmanageDeviceConfig.get_device_config_audit_delta(
                node_stack.mac)
            logger.info(f"Delta CLI after LAG deletion: {delta_cli}")
            expected_delta_cli = f"disable sharing {ports[0]}"
            if expected_delta_cli not in delta_cli:
                pytest.fail(f'Delta CLI mismatch, expected: {expected_delta_cli}, found: {delta_cli}')

            logger.step("update the device")
            xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, \
                "Could not update the device"
            ports_not_aggregated_device_updated = True

            logger.step("check the results in CLI")
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
            if str(ports[0]) in result:
                pytest.fail(f"The LAG is still configured, CLI result: {result}")

            logger.step("check the number of LACP ports in switch template -> port configuration")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(
                nw_policy=node_stack_policy_name,
                sw_template=node_stack_template_name)
            if sw_template_web_elements.get_sw_template_port_configuration_tab() is None:
                auto_actions.click(
                    sw_template_web_elements.get_template_link(template=node_stack_template_name))
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            labels = sw_template_web_elements.get_lag_span(lag=ports[0])
            if labels is not None:
                pytest.fail("Invalid number of LACP ports in the switch template -> port configuration table")
        except Exception as e:
            logger.info(f"Error:{e}")
            if ports_not_aggregated:
                if not ports_not_aggregated_device_updated:
                    # update the device
                    xiq_library_at_class_level.xflowsmanageDevices.update_switch_policy_and_configuration(
                        device_mac=node_stack.mac)
            elif ports_aggregated:
                logger.step("remove all VIM ports from LACP")
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_stack_policy_name,
                                                                                            node_stack_template_name)
                auto_actions.click(
                    sw_template_web_elements.get_template_link(template=node_stack_template_name))
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(
                    first_slot_with_vim[-1])
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.remove_lag_in_template(first_vim_port, ports,
                                                                                                device="stack")
                xiq_library_at_class_level.xflowsmanageDevices.navigator.navigate_to_devices()
                if ports_aggregated_device_updated:
                    # update the device
                    xiq_library_at_class_level.xflowsmanageDevices.update_switch_policy_and_configuration(
                        device_mac=node_stack.mac)
        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_20651_teardown'
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.tcxm_20658
    @pytest.mark.p2
    def test_tcxm_20658(self, node_stack, logger, cloud_driver,
                        xiq_library_at_class_level, loaded_config, auto_actions, enter_switch_cli, cli):
        """
        Author        : tapostol
        Modified by   : mchelu
        Description   : Verify that different LAGs can be configured across different port modules when LACP is
        created using Device Level Configuration.
        Preconditions : Use EXOS 5520 devices with 4 ports VIM module.
        Step	Step Description
        1	    Onboard the EXOS 5520 stack with 2 VIM modules.
        2	    Create a Network Policy with specific 5520 template.
        3	    Assign the previously created Network Policy to the device and update the device.
        4	    Using D360 -> Port Configuration aggregate 2 VIM ports from one VIM module.
        5	    Using D360 -> Port Configuration aggregate 2 VIM ports from the same VIM module.
        6	    Using D360 -> Port Configuration aggregate 2 VIM ports from the other VIM module.
        7	    Using D360 -> Port Configuration aggregate 2 fixed panel ports from different stack slots.
        8	    Update the device, check the results in CLI and check the number of LACP ports in D360 ->
                Port Configuration table.
        9	    Using D360 -> Port Configuration remove all ports from all LAGs.
        10      Update the device, check the results in CLI and check the number of LACP ports in D360 ->
                Port Configuration table.
        """
        cloud_driver.refresh_page()
        loaded_config['${TEST_NAME}'] = 'test_tcxm_20658_run'

        try:
            logger.info("Setup variables")
            with enter_switch_cli(node_stack) as dev_cmd:
                output = dev_cmd.send_cmd(node_stack.name, 'show version | in VIM', max_wait=10, interval=2)
            result = output[0].return_text
            p = re.compile(r'([a-zA-Z0-9-]*d*VIM.*\d) {2,}:', re.M)
            vim_slots_list = re.findall(p, result)
            first_slot_with_vim = vim_slots_list[0]
            second_slot_with_vim = vim_slots_list[1]
            logger.info(f"Slots with VIM are : {vim_slots_list}")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_stack.mac)

            logger.step("Get number of slots:")
            number_of_slots = len(xiq_library_at_class_level.xflowsmanageDevice360.get_stack_overview_slot_ports_row())
            assert number_of_slots, "[FAIL] Could not get the number of slots"

            # Check if the slots have VIMs
            vim_ports = xiq_library_at_class_level.xflowsmanageDevice360.device360_get_stack_ports_by_type("vim")
            sfp_ports = xiq_library_at_class_level.xflowsmanageDevice360.device360_get_stack_ports_by_type("sfp")
            assert vim_ports, "[FAIL] No VIM ports found"
            assert sfp_ports, "[FAIL] No SFP ports found"
            logger.info(f"VIM ports are {vim_ports}")
            logger.info(f"SFP ports are {sfp_ports}")
            logger.step("Navigate to Device360->Port Configuration->Port Settings & Aggregation")
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_d360_configure_port_settings_aggregation_tab_button)

            reference_dut_lacp = []
            logger.info(f"Aggregate 2 VIM ports from the first slot")
            number_of_aggregated_ports = 0
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_aggregate_ports(
                [vim_ports[0], vim_ports[1]], True,
                device="stack"), \
                "[FAIL] Could not aggregate first two VIM ports from first slot"
            number_of_aggregated_ports = number_of_aggregated_ports + 2
            reference_dut_lacp.append(vim_ports[0])
            reference_dut_lacp.append(vim_ports[1])

            logger.info(f"Aggregate last 2 VIM ports from the first slot")
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_aggregate_ports(
                [vim_ports[2], vim_ports[3]], True,
                device="stack"), \
                "[FAIL] Could not aggregate second two VIM ports from first slot"
            number_of_aggregated_ports = number_of_aggregated_ports + 2
            reference_dut_lacp.append(vim_ports[2])
            reference_dut_lacp.append(vim_ports[3])

            logger.info(f"Try to aggregate 2 VIM ports from another VIM module")
            if len(vim_ports) >= 6:
                assert xiq_library_at_class_level.xflowsmanageDevice360.device360_aggregate_ports(
                    [vim_ports[4], vim_ports[5]], True,
                    device="stack"), \
                    "[FAIL] Could not aggregate first two VIM ports from second slot"
                number_of_aggregated_ports = number_of_aggregated_ports + 2
                reference_dut_lacp.append(vim_ports[4])
                reference_dut_lacp.append(vim_ports[5])
            else:
                logger.info("[WARNING]: Couldn't find more than one VIM SLOT")
            logger.info(f"Aggregate 2 fixed panel ports from different stack slots")
            fixed_port_1st_slot = first_slot_with_vim[-1] + ":1"
            fixed_port_2nd_slot = second_slot_with_vim[-1] + ":1"
            aggregate_other_slot_sfp = xiq_library_at_class_level.xflowsmanageDevice360. \
                device360_aggregate_ports([fixed_port_1st_slot, fixed_port_2nd_slot], True, device="stack")

            assert aggregate_other_slot_sfp, "Could not aggregate ports from different slots"
            reference_dut_lacp.append(fixed_port_1st_slot)
            reference_dut_lacp.append(fixed_port_2nd_slot)
            number_of_aggregated_ports = number_of_aggregated_ports + 2

            logger.info(f"Push changes to the device")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, "Could not update the device"

            logger.step("Check aggregation ports added in Device360 and on dut CLI")
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_stack.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_d360_configure_port_settings_aggregation_tab_button)

            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_check_aggregated_ports_number(
                number_of_aggregated_ports,
                number_of_slots), \
                "[FAIL] Incorrect number of LACP ports"
            assert cli.check_lacp_dut(node_stack, reference_dut_lacp), "Incorrect number of LACPs from dut"

            logger.step("Remove aggregation from 2 VIM ports from the first slot")
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(vim_ports[0],
                                                                                                   [vim_ports[0],
                                                                                                    vim_ports[1]],
                                                                                                   action='remove',
                                                                                                   device="stack"), \
                "[FAIL] Could not remove aggregation from first VIM ports from first slot"
            number_of_aggregated_ports = number_of_aggregated_ports - 2

            logger.step("Remove aggregation from 2 VIM ports from the first slot")
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(vim_ports[2],
                                                                                                   [vim_ports[2],
                                                                                                    vim_ports[3]],
                                                                                                   action='remove',
                                                                                                   device="stack"), \
                "[FAIL] Could not remove aggregation from second VIM ports from first slot"
            number_of_aggregated_ports = number_of_aggregated_ports - 2

            logger.step("Remove aggregation if exists")
            if len(vim_ports) >= 6:
                assert xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(vim_ports[4],
                                                                                                       [vim_ports[4],
                                                                                                        vim_ports[5]],
                                                                                                       action='remove',
                                                                                                       device="stack"), \
                    "[FAIL] Could not remove aggregation from first VIM ports from second slot"
                number_of_aggregated_ports = number_of_aggregated_ports - 2

            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_add_remove_lag_ports(fixed_port_1st_slot,
                                                                                                   [fixed_port_1st_slot,
                                                                                                    fixed_port_2nd_slot],
                                                                                                   action='remove',
                                                                                                   device="stack"), \
                "[FAIL] Could not remove aggregation ports 1 from slot 1 and 1 from slot 2"
            number_of_aggregated_ports = number_of_aggregated_ports - 2

            logger.step("Push changes to the device")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(
                device_mac=node_stack.mac) == 1, "Could not update the device"

            logger.step("Check aggregation ports removed in Device360 and on dut CLI")
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(device_mac=node_stack.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_d360_configure_port_settings_aggregation_tab_button)
            assert xiq_library_at_class_level.xflowsmanageDevice360.device360_check_aggregated_ports_number(0,
                                                                                                            number_of_slots), \
                "[FAIL] Incorrect number of LACP ports"
            assert cli.check_lacp_dut(node_stack, []), \
                "[FAIL] Incorrect number of LACPs from dut"

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_20658_teardwon'
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowsmanageDevices.revert_device_to_template(node_stack.mac) == 1