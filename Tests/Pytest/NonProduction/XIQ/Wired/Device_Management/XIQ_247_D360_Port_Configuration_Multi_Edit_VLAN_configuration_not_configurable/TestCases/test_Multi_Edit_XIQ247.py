import pytest
import time
import random
import string


def random_description():
    pool = list(string.ascii_letters) + list(string.digits)
    description = f"Description_{''.join(random.sample(pool, k=4))}"
    return description


def random_word(x=12):
    randword = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(x))
    return randword


@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.development
@pytest.mark.testbed_1_node
@pytest.mark.testbed_stack
class XIQ247Tests:

    @pytest.mark.tcxm_25562
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    def test_tcxm_25562(self, node, logger, xiq_library_at_class_level):
        """ TCXM-25562 - Check availability of "VLAN" field when Port Type is "Access Port"
        configure all fields and verify if the settings are saved successfully and update the device without error."""

        global commands_into_delta, voss_or_exos_port, slot

        try:

            port_description = random_description()

            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices() == 1:
                pytest.fail("Fail on navigating to devices")

            xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)

            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac) == 1:
                pytest.fail("Fail on navigating to D360 view with MAC")
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)
            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360() == 1:
                pytest.fail("Fail on navigating to Port Config")

            voss_or_exos_port = [16, 17, 18, 19]
            number_of_ports = len(voss_or_exos_port)
            first_port = voss_or_exos_port[0]
            last_port = voss_or_exos_port[number_of_ports - 1]
            if node.platform.lower() == 'stack':
                slot = xiq_library_at_class_level.xflowsmanageDevice360.select_stack_unit(1)

            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                stack_ports = []
                for port in voss_or_exos_port:
                    stack_ports.append(str(slot) + ':' + str(port))
                logger.info(stack_ports)
                for port in stack_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
            elif node.cli_type == 'voss':
                logger.info("VOSS device")
                voss_port_name = "eth"
                voss_ports = []
                for port in voss_or_exos_port:
                    voss_ports.append(voss_port_name + str(port))
                logger.info(voss_ports)
                for port in voss_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
            else:
                for port in voss_or_exos_port:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)

            time.sleep(2)
            # Open the Multi Edit tab
            xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_d360_port_config()

            # Check if the ports selected are displayed correctly
            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                if not xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message() == \
                       f"Selected Ports ({str(number_of_ports)}) : {str(slot)}:{str(first_port)}-{str(last_port)}":
                    pytest.fail(f"The selected ports are not displayed correctly: \
                                {xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message()}")
            elif node.cli_type == 'voss':
                if not xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message() == \
                       f"Selected Ports ({str(number_of_ports)}) : 1/{str(first_port)}-{str(last_port)}":
                    pytest.fail("The selected ports are not displayed correctly")
            elif node.cli_type == 'exos':
                if not xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message() == \
                       f"Selected Ports ({str(number_of_ports)}) : {str(first_port)}-{str(last_port)}":
                    pytest.fail("The selected ports are not displayed correctly")
            else:
                pytest.fail(f"The device is not EXOS or VOSS or Stack: \
                            {xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message()}")

            # Configure the fields in Multi Edit tab
            xiq_library_at_class_level.xflowsmanageDevice360.fill_port_details_multi_edit_fields(
                port_usage='Access Port',
                vlan_access_port=500)

            xiq_library_at_class_level.xflowsmanageDevice360.fill_port_details_multi_edit_fields(port_state='OFF')

            xiq_library_at_class_level.xflowsmanageDevice360.fill_port_details_multi_edit_fields(
                description=port_description)

            # Save the config in Multi Edit tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_save_multi_edit_button()

            # Save the config and close the Port configuration tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration_all_switches()

            # Check if the successful message is displayed correctly after the config is saved
            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                       "Stack Port Configuration Saved":
                    pytest.fail(f"Unable to display the success message: \
                                {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
            elif node.cli_type.lower() == 'exos':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                       "Switch Port Configuration Saved":
                    pytest.fail(f"Unable to display the success message: \
                                {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
            elif node.cli_type == 'voss':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss() == \
                       "Interface settings were updated successfully.":
                    pytest.fail(f"Unable to display the success message: \
                                {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss()}")
            else:
                logger.info("The success message was not generated")

            xiq_library_at_class_level.xflowsmanageDevice360.d360_cancel_port_configuration_all_switches()

            if not xiq_library_at_class_level.xflowsmanageDevice360.exit_d360_Page() == 1:
                pytest.fail("Fail to exit from D360 page")

            # Check the config in Delta view
            for port in voss_or_exos_port:
                if node.cli_type.lower() == 'voss':
                    commands_into_delta = [
                        'interface gigabitEthernet ' + '1/' + str(port),
                        'no auto-sense enable',
                        'exit',
                        'interface gigabitEthernet ' + '1/' + str(port),
                        f'name "{port_description}"',
                        'shutdown',
                        'vlan members add 500 ' + '1/' + str(port) + ' portmember'
                    ]
                elif node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                    commands_into_delta = [
                        'configure vlan 1 delete port ' + str(slot) + ":" + str(port),
                        'configure vlan 500 add port ' + str(slot) + ":" + str(port) + ' untagged #y',
                        'configure ports ' + str(slot) + ":" + str(
                            port) + f' description-string "{port_description}"',
                    ]
                elif node.cli_type.lower() == 'exos':
                    commands_into_delta = [
                        'configure vlan 1 delete port ' + str(port),
                        'configure vlan 500 add port ' + str(port) + ' untagged #y',
                        'configure ports ' + str(port) + f' description-string "{port_description}"',
                    ]
                else:
                    pytest.fail("Configuration is not displayed into Delta View")

            xiq_library_at_class_level.xflowsmanageDevice360.check_delta_config_local(node.mac, commands_into_delta)

            if not xiq_library_at_class_level.xflowsmanageDevices.select_device(node.mac):
                pytest.fail("Failed to select")

            # Update configuration on device and check if the process is completed without error
            if not xiq_library_at_class_level.xflowsmanageDevices.update_switch_complete(node.mac) == 1:
                pytest.fail("Failed to update policy ")

            # Check device update status
            if not xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(
                    device_mac=node.mac) == 1:
                pytest.fail("The update was not finished successfully")

            """	 Configure multiple ports from "Access Port" to "Auto-sense Port """

            if node.cli_type == 'voss':
                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
                time.sleep(10)

                if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(
                        node.mac) == 1:
                    pytest.fail("Fail on navigating to D360 view with MAC")
                # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
                time.sleep(10)
                if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360() == 1:
                    pytest.fail("Fail on navigating to Port Config")

                if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                    stack_ports = []
                    for port in voss_or_exos_port:
                        stack_ports.append(str(slot) + ':' + str(port))
                    logger.info(stack_ports)
                    for port in stack_ports:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
                elif node.cli_type == 'voss':
                    logger.info("VOSS device")
                    voss_port_name = "eth"
                    voss_ports = []
                    for port in voss_or_exos_port:
                        voss_ports.append(voss_port_name + str(port))
                    logger.info(voss_ports)
                    for port in voss_ports:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
                else:
                    for port in voss_or_exos_port:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)

                # Open the Multi Edit tab
                xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_d360_port_config()

                # Configure the fields in Multi Edit tab
                xiq_library_at_class_level.xflowsmanageDevice360.fill_port_details_multi_edit_fields(
                    port_usage='Auto-sense Port')

                xiq_library_at_class_level.xflowsmanageDevice360.fill_port_details_multi_edit_fields(
                    description='Auto-sense ports')

                # Save the config in Multi Edit tab
                xiq_library_at_class_level.xflowsmanageDevice360.d360_save_multi_edit_button()

                # Save the config and close the Port configuration tab
                xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration_all_switches()

                # Check if the successful message is displayed correctly after the config is saved
                if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                    if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                           "Stack Port Configuration Saved":
                        pytest.fail(f"Unable to display the success message: \
                            {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
                elif node.cli_type.lower() == 'exos':
                    if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                           "Switch Port Configuration Saved":
                        pytest.fail(f"Unable to display the success message: \
                            {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
                elif node.cli_type == 'voss':
                    if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss() == \
                           "Interface settings were updated successfully.":
                        pytest.fail(f"Unable to display the success message: \
                            {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss()}")
                else:
                    logger.info("The success message was not generated")

                if not xiq_library_at_class_level.xflowsmanageDevice360.exit_d360_Page() == 1:
                    pytest.fail("Fail to exit from D360 page")

        finally:

            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac) == 1:
                pytest.fail("Fail on navigating to D360 view with MAC")
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)
            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360() == 1:
                pytest.fail("Fail on navigating to Port Config")

            # Revert all setings to default settings
            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                stack_ports = []
                for port in voss_or_exos_port:
                    stack_ports.append(str(slot) + ':' + str(port))
                logger.info(stack_ports)
                for port in stack_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
            elif node.cli_type == 'voss':
                logger.info("VOSS device")
                voss_port_name = "eth"
                voss_ports = []
                for port in voss_or_exos_port:
                    voss_ports.append(voss_port_name + str(port))
                logger.info(voss_ports)
                for port in voss_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
            else:
                for port in voss_or_exos_port:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)

            # Open the Multi Edit tab
            xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_d360_port_config()

            # Check the fields in Multi Edit tab to revert all setings
            xiq_library_at_class_level.xflowsmanageDevice360.check_fileds_from_multi_edit_tab()

            # Save the config in Multi Edit tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_save_multi_edit_button()

            # Save the config and close the Port configuration tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration_all_switches()

            # Check if the successful message is displayed correctly after the config is saved
            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                       "Stack Port Configuration Saved":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
            elif node.cli_type.lower() == 'exos':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                       "Switch Port Configuration Saved":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
            elif node.cli_type == 'voss':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss() == \
                       "Interface settings were updated successfully.":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss()}")
            else:
                logger.info("The success message was not generated")

            xiq_library_at_class_level.xflowsmanageDevice360.d360_cancel_port_configuration_all_switches()

            if not xiq_library_at_class_level.xflowsmanageDevice360.exit_d360_Page() == 1:
                pytest.fail("Fail to exit from D360 page")

            # Check the config in Delta view
            for port in voss_or_exos_port:
                if node.cli_type.lower() == 'voss':
                    commands_into_delta = [
                        'interface gigabitEthernet ' + '1/' + str(port),
                        f'name "Default settings for auto-sense port"',
                    ]
                elif node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                    commands_into_delta = [
                        'configure ports ' + str(slot) + ":" + str(
                            port) + f' description-string "Default settings for the access port"',
                    ]
                elif node.cli_type.lower() == 'exos':
                    commands_into_delta = [
                        'configure ports ' + str(port) + f' description-string "Default settings for the access port"',
                    ]
                else:
                    pytest.fail("Configuration is not displayed into Delta View")

            xiq_library_at_class_level.xflowsmanageDevice360.check_delta_config_local(node.mac, commands_into_delta)

            if not xiq_library_at_class_level.xflowsmanageDevices.select_device(node.mac):
                pytest.fail("Failed to select")

            # Update configuration on device and check if the process is completed without error
            if not xiq_library_at_class_level.xflowsmanageDevices.update_switch_complete(node.mac) == 1:
                pytest.fail("Failed to update policy ")

            # Check device update status
            if not xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(
                    device_mac=node.mac) == 1:
                pytest.fail("The update was not finished successfully")

    @pytest.mark.tcxm_25565
    @pytest.mark.dependson("tcxm_25562")
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    def test_tcxm_25565(self, node, logger, xiq_library_at_class_level):
        """ TCXM-25562 - Check availability of "VLAN" field when Port Type is "Access Port"
        configure all fields and verify if the settings are saved successfully and update the device without error."""
        """ TCXM-25565 - Check the display of correct fields when Port Type is configured from 'Access Port' 
        to 'Auto-sense Port'. - test applied only on VOSS devices"""
        if node.cli_type == 'Stack' or node.cli_type == 'exos':
            pytest.skip("Auto-sense Port is not supported on Switch Engine devices!")
        else:
            logger.info("The test TCXM_25565 was run in the test TCXM_25562")

    @pytest.mark.tcxm_25563
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    def test_tcxm_25563(self, node, logger, xiq_library_at_class_level):
        """ TCXM-25563 - Check availability of "VLAN" fields (native VLAN and allowed VLAN)
        when Port Type is "Trunk Port", configure all fields and verify if the settings are saved
        and upload on the device without errors."""

        global commands_into_delta, slot, voss_or_exos_port
        """	 Multi Edit """

        try:
            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices() == 1:
                pytest.fail("Fail on navigating to devices")

            xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)

            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac) == 1:
                pytest.fail("Fail on navigating to D360 view with MAC")
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)
            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360() == 1:
                pytest.fail("Fail on navigating to Port Config")

            voss_or_exos_port = [11, 12, 13, 14]
            number_of_ports = len(voss_or_exos_port)
            first_port = voss_or_exos_port[0]
            last_port = voss_or_exos_port[number_of_ports - 1]
            if node.platform.lower() == 'stack':
                slot = xiq_library_at_class_level.xflowsmanageDevice360.select_stack_unit(1)

            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                stack_ports = []
                for port in voss_or_exos_port:
                    stack_ports.append(str(slot) + ':' + str(port))
                logger.info(stack_ports)
                for port in stack_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
            elif node.cli_type == 'voss':
                logger.info("VOSS device")
                voss_port_name = "eth"
                voss_ports = []
                for port in voss_or_exos_port:
                    voss_ports.append(voss_port_name + str(port))
                logger.info(voss_ports)
                for port in voss_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
            else:
                for port in voss_or_exos_port:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)

            # Open the Multi Edit tab
            time.sleep(2)
            xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_d360_port_config()

            # Check if the ports selected are displayed correctly
            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                if not xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message() == \
                       f"Selected Ports ({str(number_of_ports)}) : {str(slot)}:{str(first_port)}-{str(last_port)}":
                    pytest.fail(f"The selected ports are not displayed correctly: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message()}")
            elif node.cli_type == 'voss':
                if not xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message() == \
                       f"Selected Ports ({str(number_of_ports)}) : 1/{str(first_port)}-{str(last_port)}":
                    pytest.fail("The selected ports are not displayed correctly")
            elif node.cli_type == 'exos':
                if not xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message() == \
                       f"Selected Ports ({str(number_of_ports)}) : {str(first_port)}-{str(last_port)}":
                    pytest.fail("The selected ports are not displayed correctly")
            else:
                pytest.fail(f"The device is not EXOS or VOSS or Stack: \
                    {xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message()}")

            # Configure the fields in Multi Edit tab for Trunk port
            xiq_library_at_class_level.xflowsmanageDevice360.fill_port_details_multi_edit_fields(
                port_usage='Trunk Port',
                native_vlan_trunk_port=800,
                allowed_vlan_trunk_port=70)

            xiq_library_at_class_level.xflowsmanageDevice360.fill_port_details_multi_edit_fields(port_state='OFF')

            xiq_library_at_class_level.xflowsmanageDevice360.fill_port_details_multi_edit_fields(
                description='Description for multiple trunk ports')

            # Save the config in Multi Edit tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_save_multi_edit_button()

            # Save the config and close the Port configuration tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration_all_switches()

            # Check if the successful message is displayed correctly after the config is saved
            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                       "Stack Port Configuration Saved":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
            elif node.cli_type.lower() == 'exos':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                       "Switch Port Configuration Saved":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
            elif node.cli_type == 'voss':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss() == \
                       "Interface settings were updated successfully.":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss()}")
            else:
                logger.info("The success message was not generated")

            # Save the config and close the Port configuration tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_cancel_port_configuration_all_switches()

            if not xiq_library_at_class_level.xflowsmanageDevice360.exit_d360_Page() == 1:
                pytest.fail("Fail to exit from D360 page")

            # Check the config in Delta view
            for port in voss_or_exos_port:
                if node.cli_type == 'voss':
                    commands_into_delta = [
                        'interface gigabitEthernet ' + '1/' + str(port),
                        'no auto-sense enable',
                        'exit',
                        'interface gigabitEthernet ' + '1/' + str(port),
                        'name "Description for multiple trunk ports"',
                        'encapsulation dot1q',
                        'default-vlan-id 800',
                        'shutdown',
                        'vlan members add 800 ' + '1/' + str(port) + ' portmember',
                        'vlan members add 70 ' + '1/' + str(port) + ' portmember'
                    ]
                elif node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                    commands_into_delta = [
                        'configure vlan 1 delete port ' + str(slot) + ":" + str(port),
                        'configure vlan 800 add port ' + str(slot) + ":" + str(port) + ' untagged #y',
                        'configure ports ' + str(slot) + ":" + str(
                            port) + ' description-string "Description for multiple trunk ports"',
                    ]
                elif node.cli_type == 'exos':
                    commands_into_delta = [
                        'configure vlan 1 delete port ' + str(port),
                        'configure vlan 800 add port ' + str(port) + ' untagged #y',
                        'configure ports ' + str(port) + ' description-string "Description for multiple trunk ports"',
                    ]
                else:
                    pytest.fail("Configuration is not displayed into Delta View")

            xiq_library_at_class_level.xflowsmanageDevice360.check_delta_config_local(node.mac, commands_into_delta)

            if not xiq_library_at_class_level.xflowsmanageDevices.select_device(node.mac):
                pytest.fail("Failed to select")

            # Update configuration on device and check if the process is completed without error
            if not xiq_library_at_class_level.xflowsmanageDevices.update_switch_complete(node.mac) == 1:
                pytest.fail("Failed to update policy ")

            # Check device update status
            if not xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(
                    device_mac=node.mac) == 1:
                pytest.fail("The update was not finished successfully")

        finally:

            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac) == 1:
                pytest.fail("Fail on navigating to D360 view with MAC")
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)
            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360() == 1:
                pytest.fail("Fail on navigating to Port Config")

            # Revert all setings to default settings
            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                stack_ports = []
                for port in voss_or_exos_port:
                    stack_ports.append(str(slot) + ':' + str(port))
                logger.info(stack_ports)
                for port in stack_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
            elif node.cli_type == 'voss':
                logger.info("VOSS device")
                voss_port_name = "eth"
                voss_ports = []
                for port in voss_or_exos_port:
                    voss_ports.append(voss_port_name + str(port))
                logger.info(voss_ports)
                for port in voss_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
            else:
                for port in voss_or_exos_port:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)

            # Open the Multi Edit tab
            xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_d360_port_config()

            # Check the fields in Multi Edit tab to revert all setings
            xiq_library_at_class_level.xflowsmanageDevice360.check_fileds_from_multi_edit_tab()

            # Save the config in Multi Edit tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_save_multi_edit_button()

            # Save the config and close the Port configuration tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration_all_switches()

            # Check if the successful message is displayed correctly after the config is saved
            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                       "Stack Port Configuration Saved":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
            elif node.cli_type.lower() == 'exos':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                       "Switch Port Configuration Saved":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
            elif node.cli_type == 'voss':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss() == \
                       "Interface settings were updated successfully.":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss()}")
            else:
                logger.info("The success message was not generated")

            xiq_library_at_class_level.xflowsmanageDevice360.d360_cancel_port_configuration_all_switches()

            if not xiq_library_at_class_level.xflowsmanageDevice360.exit_d360_Page() == 1:
                pytest.fail("Fail to exit from D360 page")

            # Check the config in Delta view
            for port in voss_or_exos_port:
                if node.cli_type.lower() == 'voss':
                    commands_into_delta = [
                        'interface gigabitEthernet ' + '1/' + str(port),
                        f'name "Default settings for auto-sense port"',
                    ]
                elif node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                    commands_into_delta = [
                        'configure ports ' + str(slot) + ":" + str(
                            port) + f' description-string "Default settings for the access port"',
                    ]
                elif node.cli_type.lower() == 'exos':
                    commands_into_delta = [
                        'configure ports ' + str(port) + f' description-string "Default settings for the access port"',
                    ]
                else:
                    pytest.fail("Configuration is not displayed into Delta View")

            xiq_library_at_class_level.xflowsmanageDevice360.check_delta_config_local(node.mac, commands_into_delta)

            if not xiq_library_at_class_level.xflowsmanageDevices.select_device(node.mac):
                pytest.fail("Failed to select")

            # Update configuration on device and check if the process is completed without error
            if not xiq_library_at_class_level.xflowsmanageDevices.update_switch_complete(node.mac) == 1:
                pytest.fail("Failed to update policy ")

            # Check device update status
            if not xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(
                    device_mac=node.mac) == 1:
                pytest.fail("The update was not finished successfully")

    @pytest.mark.tcxm_25564
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p2
    def test_tcxm_25564(self, node, logger, xiq_library_at_class_level):

        """ TCXM-25564 - This test is applied only on EXOS devices: Check availability of "VLAN" field when
         Port Type is "Phone Data Port", configure all fields and verify if the settings are saved successfully."""

        global commands_into_delta, slot, voss_or_exos_port
        """	 Multi Edit """

        if node.cli_type == 'Stack' or node.cli_type == 'exos':

            try:
                name_phone_port = "Phone Port" + random_word()

                if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices() == 1:
                    pytest.fail("Fail on navigating to devices")

                xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
                # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
                time.sleep(10)

                if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(
                        node.mac) == 1:
                    pytest.fail("Fail on navigating to D360 view with MAC")
                # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
                time.sleep(10)
                if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360() == 1:
                    pytest.fail("Fail on navigating to Port Config")

                voss_or_exos_port = [7, 8, 9, 10]
                number_of_ports = len(voss_or_exos_port)
                first_port = voss_or_exos_port[0]
                last_port = voss_or_exos_port[number_of_ports - 1]
                if node.platform.lower() == 'stack':
                    slot = xiq_library_at_class_level.xflowsmanageDevice360.select_stack_unit(1)

                # Configure phone settings on one port and save the configuration
                if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                    xiq_library_at_class_level.xflowsmanageDevice360.create_voice_port(
                        port=(str(slot) + ':' + str(voss_or_exos_port[0])), port_type_name=name_phone_port,
                        voice_vlan="77", data_vlan="78",
                        lldp_voice_options_flag=False,
                        cdp_voice_options_flag=False, device_360=True)
                elif node.cli_type.lower() == 'exos':
                    xiq_library_at_class_level.xflowsmanageDevice360.create_voice_port(port=str(voss_or_exos_port[0]),
                                                                                       port_type_name=name_phone_port,
                                                                                       voice_vlan="77",
                                                                                       data_vlan="78",
                                                                                       lldp_voice_options_flag=False,
                                                                                       cdp_voice_options_flag=False,
                                                                                       device_360=True)

                # Save the config and close the Port configuration tab
                xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration_all_switches()

                if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                    stack_ports = []
                    for port in voss_or_exos_port:
                        stack_ports.append(str(slot) + ':' + str(port))
                    logger.info(stack_ports)
                    for port in stack_ports:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
                elif node.cli_type == 'voss':
                    logger.info("VOSS device")
                    voss_port_name = "eth"
                    voss_ports = []
                    for port in voss_or_exos_port:
                        voss_ports.append(voss_port_name + str(port))
                    logger.info(voss_ports)
                    for port in voss_ports:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
                else:
                    for port in voss_or_exos_port:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)

                # Open the Multi Edit tab
                time.sleep(2)
                xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_d360_port_config()

                # Check if the ports selected are displayed correctly
                if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                    if not xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message() == \
                           f"Selected Ports ({str(number_of_ports)}) : {str(slot)}:{str(first_port)}-{str(last_port)}":
                        pytest.fail(f"The selected ports are not displayed correctly: \
                            {xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message()}")
                elif node.cli_type == 'voss':
                    if not xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message() == \
                           f"Selected Ports ({str(number_of_ports)}) : 1/{str(first_port)}-{str(last_port)}":
                        pytest.fail("The selected ports are not displayed correctly")
                elif node.cli_type == 'exos':
                    if not xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message() == \
                           f"Selected Ports ({str(number_of_ports)}) : {str(first_port)}-{str(last_port)}":
                        pytest.fail("The selected ports are not displayed correctly")
                else:
                    pytest.fail(f"The device is not EXOS or VOSS or Stack: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message()}")

                xiq_library_at_class_level.xflowsmanageDevice360.fill_port_details_multi_edit_fields(
                    port_usage=name_phone_port,
                    voice_vlan_phone_port=11,
                    data_vlan_phone_port=15)

                xiq_library_at_class_level.xflowsmanageDevice360.fill_port_details_multi_edit_fields(
                    description='Descrition for Phone ports')

                xiq_library_at_class_level.xflowsmanageDevice360.d360_save_multi_edit_button()

                # Save the config and close the Port configuration tab
                xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration_all_switches()

                time.sleep(5)
                # Check if the successful message is displayed correctly after the config is saved
                if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                    if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                           "Stack Port Configuration Saved":
                        pytest.fail(f"Unable to display the success message: \
                            {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
                elif node.cli_type.lower() == 'exos':
                    if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                           "Switch Port Configuration Saved":
                        pytest.fail(f"Unable to display the success message: \
                            {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
                elif node.cli_type == 'voss':
                    if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss() == \
                           "Interface settings were updated successfully.":
                        pytest.fail(f"Unable to display the success message: \
                            {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss()}")
                else:
                    logger.info("The success message was not generated")

                xiq_library_at_class_level.xflowsmanageDevice360.d360_cancel_port_configuration_all_switches()

                if not xiq_library_at_class_level.xflowsmanageDevice360.exit_d360_Page() == 1:
                    pytest.fail("Fail to exit from D360 page")

                for port in voss_or_exos_port:
                    if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                        commands_into_delta = [
                            'configure vlan 1 delete port ' + str(slot) + ":" + str(port),
                            'configure vlan 15 add port ' + str(slot) + ":" + str(port) + ' untagged #y',
                            'configure vlan 11 add port ' + str(slot) + ":" + str(port) + ' tagged #y',
                            'configure ports ' + str(slot) + ":" + str(
                                port) + ' description-string "Descrition for Phone ports"',
                        ]
                    elif node.cli_type.lower() == 'exos':
                        commands_into_delta = [
                            'configure vlan 1 delete port ' + str(port),
                            'configure vlan 15 add port ' + str(port) + ' untagged #y',
                            'configure vlan 11 add port ' + str(port) + ' tagged #y',
                            'configure ports ' + str(port) + ' description-string "Descrition for Phone ports"',
                        ]
                    else:
                        pytest.fail("Configuration is not displayed into Delta View")

                xiq_library_at_class_level.xflowsmanageDevice360.check_delta_config_local(node.mac, commands_into_delta)

                if not xiq_library_at_class_level.xflowsmanageDevices.select_device(node.mac):
                    pytest.fail("Failed to select")

                # Update Network Policy on device
                if not xiq_library_at_class_level.xflowsmanageDevices.update_switch_complete(node.mac) == 1:
                    pytest.fail("Failed to update policy ")

                # Check device update status
                if not xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(
                        device_mac=node.mac) == 1:
                    pytest.fail("The update was not finished successfully")

            finally:

                if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(
                        node.mac) == 1:
                    pytest.fail("Fail on navigating to D360 view with MAC")
                # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
                time.sleep(10)
                if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360() == 1:
                    pytest.fail("Fail on navigating to Port Config")

                # Revert all setings to default settings
                if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                    stack_ports = []
                    for port in voss_or_exos_port:
                        stack_ports.append(str(slot) + ':' + str(port))
                    logger.info(stack_ports)
                    for port in stack_ports:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
                elif node.cli_type == 'voss':
                    logger.info("VOSS device")
                    voss_port_name = "eth"
                    voss_ports = []
                    for port in voss_or_exos_port:
                        voss_ports.append(voss_port_name + str(port))
                    logger.info(voss_ports)
                    for port in voss_ports:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
                else:
                    for port in voss_or_exos_port:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)

                # Open the Multi Edit tab
                xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_d360_port_config()

                # Check the fields in Multi Edit tab to revert all setings
                xiq_library_at_class_level.xflowsmanageDevice360.check_fileds_from_multi_edit_tab()

                # Save the config in Multi Edit tab
                xiq_library_at_class_level.xflowsmanageDevice360.d360_save_multi_edit_button()

                # Save the config and close the Port configuration tab
                xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration_all_switches()

                xiq_library_at_class_level.xflowsmanageDevice360.d360_cancel_port_configuration_all_switches()

                if not xiq_library_at_class_level.xflowsmanageDevice360.exit_d360_Page() == 1:
                    pytest.fail("Fail to exit from D360 page")

                # Check the config in Delta view
                for port in voss_or_exos_port:
                    if node.cli_type.lower() == 'voss':
                        commands_into_delta = [
                            'interface gigabitEthernet ' + '1/' + str(port),
                            f'name "Default settings for auto-sense port"',
                        ]
                    elif node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                        commands_into_delta = [
                            'configure ports ' + str(slot) + ":" + str(
                                port) + f' description-string "Default settings for the access port"',
                        ]
                    elif node.cli_type.lower() == 'exos':
                        commands_into_delta = [
                            'configure ports ' + str(
                                port) + f' description-string "Default settings for the access port"',
                        ]
                    else:
                        pytest.fail("Configuration is not displayed into Delta View")

                xiq_library_at_class_level.xflowsmanageDevice360.check_delta_config_local(node.mac, commands_into_delta)

                if not xiq_library_at_class_level.xflowsmanageDevices.select_device(node.mac):
                    pytest.fail("Failed to select")

                # Update configuration on device and check if the process is completed without error
                if not xiq_library_at_class_level.xflowsmanageDevices.update_switch_complete(node.mac) == 1:
                    pytest.fail("Failed to update policy ")

                # Check device update status
                if not xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(
                        device_mac=node.mac) == 1:
                    pytest.fail("The update was not finished successfully")

        else:
            pytest.skip("The device does not support Phone Port")

    @pytest.mark.tcxm_25573
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p2
    def test_tcxm_25573(self, node, logger, xiq_library_at_class_level):

        """ TCXM-25573 - Select at least 2 ports that are configured on "Access Port" Port Type,
        enter on "Multi-Edit" window, create a new Port Type profile, save the configuration
        and check if the updates are successfully."""

        global slot, commands_into_delta, voss_or_exos_port
        try:

            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices() == 1:
                pytest.fail("Fail on navigating to devices")

            xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)

            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac) == 1:
                pytest.fail("Fail on navigating to D360 view with MAC")
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)
            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360() == 1:
                pytest.fail("Fail on navigating to Port Config")

            voss_or_exos_port = [3, 4, 5, 6]
            number_of_ports = len(voss_or_exos_port)
            first_port = voss_or_exos_port[0]
            last_port = voss_or_exos_port[number_of_ports - 1]
            if node.platform.lower() == 'stack':
                slot = xiq_library_at_class_level.xflowsmanageDevice360.select_stack_unit(1)

            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                stack_ports = []
                for port in voss_or_exos_port:
                    stack_ports.append(str(slot) + ':' + str(port))
                logger.info(stack_ports)
                for port in stack_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
            elif node.cli_type == 'voss':
                logger.info("VOSS device")
                voss_port_name = "eth"
                voss_ports = []
                for port in voss_or_exos_port:
                    voss_ports.append(voss_port_name + str(port))
                logger.info(voss_ports)
                for port in voss_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
            else:
                for port in voss_or_exos_port:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)

            # Open the Multi Edit tab
            time.sleep(2)
            xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_d360_port_config()

            # Check if the ports selected are displayed correctly
            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                if not xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message() == \
                       f"Selected Ports ({str(number_of_ports)}) : {str(slot)}:{str(first_port)}-{str(last_port)}":
                    pytest.fail(f"The selected ports are not displayed correctly: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message()}")
            elif node.cli_type == 'voss':
                if not xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message() == \
                       f"Selected Ports ({str(number_of_ports)}) : 1/{str(first_port)}-{str(last_port)}":
                    pytest.fail("The selected ports are not displayed correctly")
            elif node.cli_type == 'exos':
                if not xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message() == \
                       f"Selected Ports ({str(number_of_ports)}) : {str(first_port)}-{str(last_port)}":
                    pytest.fail("The selected ports are not displayed correctly")
            else:
                pytest.fail(f"The device is not EXOS or VOSS or Stack: \
                    {xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_port_count_message()}")

            # Configure the fields in Multi Edit tab for Access port
            xiq_library_at_class_level.xflowsmanageDevice360.fill_port_details_multi_edit_fields(
                port_usage='Access Port',
                vlan_access_port=500)

            xiq_library_at_class_level.xflowsmanageDevice360.fill_port_details_multi_edit_fields(port_state='OFF')

            xiq_library_at_class_level.xflowsmanageDevice360.fill_port_details_multi_edit_fields(
                description='Description for multiple ports')

            # Save the config in Multi Edit tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_save_multi_edit_button()

            # Save the config and close the Port configuration tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration_all_switches()

            xiq_library_at_class_level.xflowsmanageDevice360.d360_cancel_port_configuration_all_switches()

            if not xiq_library_at_class_level.xflowsmanageDevice360.exit_d360_Page() == 1:
                pytest.fail("Fail to exit from D360 page")

            """	 Configure multiple ports from "Access Port" to a new port profile """

            xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)

            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac) == 1:
                pytest.fail("Fail on navigating to D360 view with MAC")
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)
            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360() == 1:
                pytest.fail("Fail on navigating to Port Config")

            if node.platform.lower() == 'stack':
                slot = xiq_library_at_class_level.xflowsmanageDevice360.select_stack_unit(1)

            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                stack_ports = []
                for port in voss_or_exos_port:
                    stack_ports.append(str(slot) + ':' + str(port))
                logger.info(stack_ports)
                for port in stack_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
            elif node.cli_type == 'voss':
                logger.info("VOSS device")
                voss_port_name = "eth"
                voss_ports = []
                for port in voss_or_exos_port:
                    voss_ports.append(voss_port_name + str(port))
                logger.info(voss_ports)
                for port in voss_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
            else:
                for port in voss_or_exos_port:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)

            # Open the Multi Edit tab
            xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_d360_port_config()

            # Select for Port Usage -> Access Port because for VOSS devices the default Port Usage is Auto-sense Port
            xiq_library_at_class_level.xflowsmanageDevice360.fill_port_details_multi_edit_fields(
                port_usage='Access Port')

            # Add a new profile on the same ports
            xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_add_port_usage()

            profile_name = "New_port_" + random_word()

            # Settings that will be applied when the new port profile is created
            template = {'name': profile_name,
                        'port usage': "trunk port",
                        'description': "A new port profile was created",
                        'page2 phoneVlanPage': ["next_page", None],
                        "native vlan": "29",
                        'page3 transmissionSettingsPage': ["next_all_pages", "next_all_pages"]
                        }

            for tmpl_element, tmpl_value in template.items():
                xiq_library_at_class_level.xflowsmanageDevice360.configure_element_port_type(tmpl_element, tmpl_value)

            xiq_library_at_class_level.xflowsmanageDevice360.port_type_nav_to_summary_page_and_save()

            # Save the config in Multi Edit tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_save_multi_edit_button()

            # Save the config and close the Port configuration tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration_all_switches()

            time.sleep(5)
            # Check if the successful message is displayed correctly after the config is saved
            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                       "Stack Port Configuration Saved":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
            elif node.cli_type.lower() == 'exos':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                       "Switch Port Configuration Saved":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
            elif node.cli_type == 'voss':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss() == \
                       "Interface settings were updated successfully.":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss()}")
            else:
                logger.info("The success message was not generated")

            xiq_library_at_class_level.xflowsmanageDevice360.d360_cancel_port_configuration_all_switches()

            if not xiq_library_at_class_level.xflowsmanageDevice360.exit_d360_Page() == 1:
                pytest.fail("Fail to exit from D360 page")

            # Check the config in Delta view
            for port in voss_or_exos_port:
                if node.cli_type == 'voss':
                    commands_into_delta = [
                        'interface gigabitEthernet ' + '1/' + str(port),
                        'no auto-sense enable',
                        'exit',
                        'interface gigabitEthernet ' + '1/' + str(port),
                        'name "A new port profile was created"',
                        'encapsulation dot1q',
                        'default-vlan-id 29',
                        'vlan members add 29 ' + '1/' + str(port) + ' portmember'
                    ]
                elif node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                    commands_into_delta = [
                        'configure vlan 1 delete port ' + str(slot) + ":" + str(port),
                        'configure vlan 29 add port ' + str(slot) + ":" + str(port) + ' untagged #y',
                        'configure ports ' + str(slot) + ":" + str(
                            port) + ' description-string "A new port profile was created"',
                    ]
                elif node.cli_type == 'exos':
                    commands_into_delta = [
                        'configure vlan 1 delete port ' + str(port),
                        'configure vlan 29 add port ' + str(port) + ' untagged #y',
                        'configure ports ' + str(port) + ' description-string "A new port profile was created"',
                    ]
                else:
                    pytest.fail("Configuration is not displayed into Delta View")

            xiq_library_at_class_level.xflowsmanageDevice360.check_delta_config_local(node.mac, commands_into_delta)

            if not xiq_library_at_class_level.xflowsmanageDevices.select_device(node.mac):
                pytest.fail("Failed to select")

            # Update configuration on device and check if the process is completed without error
            if not xiq_library_at_class_level.xflowsmanageDevices.update_switch_complete(node.mac) == 1:
                pytest.fail("Failed to update policy ")

            # Check device update status
            if not xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(
                    device_mac=node.mac) == 1:
                pytest.fail("The update was not finished successfully")

        finally:

            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac) == 1:
                pytest.fail("Fail on navigating to D360 view with MAC")
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)
            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360() == 1:
                pytest.fail("Fail on navigating to Port Config")

            # Revert all setings to default settings
            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                stack_ports = []
                for port in voss_or_exos_port:
                    stack_ports.append(str(slot) + ':' + str(port))
                logger.info(stack_ports)
                for port in stack_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
            elif node.cli_type == 'voss':
                logger.info("VOSS device")
                voss_port_name = "eth"
                voss_ports = []
                for port in voss_or_exos_port:
                    voss_ports.append(voss_port_name + str(port))
                logger.info(voss_ports)
                for port in voss_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)
            else:
                for port in voss_or_exos_port:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_ports_d360_port_config(port)

            # Open the Multi Edit tab
            xiq_library_at_class_level.xflowsmanageDevice360.multi_edit_d360_port_config()

            # Check the fields in Multi Edit tab to revert all setings
            xiq_library_at_class_level.xflowsmanageDevice360.check_fileds_from_multi_edit_tab()

            # Save the config in Multi Edit tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_save_multi_edit_button()

            # Save the config and close the Port configuration tab
            xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration_all_switches()

            # Check if the successful message is displayed correctly after the config is saved
            if node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                       "Stack Port Configuration Saved":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
            elif node.cli_type.lower() == 'exos':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos() == \
                       "Switch Port Configuration Saved":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_exos()}")
            elif node.cli_type == 'voss':
                if not xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss() == \
                       "Interface settings were updated successfully.":
                    pytest.fail(f"Unable to display the success message: \
                        {xiq_library_at_class_level.xflowsmanageDevice360.succesful_message_multi_edit_voss()}")
            else:
                logger.info("The success message was not generated")

            xiq_library_at_class_level.xflowsmanageDevice360.d360_cancel_port_configuration_all_switches()

            if not xiq_library_at_class_level.xflowsmanageDevice360.exit_d360_Page() == 1:
                pytest.fail("Fail to exit from D360 page")

            # Check the config in Delta view
            for port in voss_or_exos_port:
                if node.cli_type.lower() == 'voss':
                    commands_into_delta = [
                        'interface gigabitEthernet ' + '1/' + str(port),
                        f'name "Default settings for auto-sense port"',
                    ]
                elif node.cli_type.lower() == 'exos' and node.platform.lower() == 'stack':
                    commands_into_delta = [
                        'configure ports ' + str(slot) + ":" + str(
                            port) + f' description-string "Default settings for the access port"',
                    ]
                elif node.cli_type.lower() == 'exos':
                    commands_into_delta = [
                        'configure ports ' + str(port) + f' description-string "Default settings for the access port"',
                    ]
                else:
                    pytest.fail("Configuration is not displayed into Delta View")

            xiq_library_at_class_level.xflowsmanageDevice360.check_delta_config_local(node.mac, commands_into_delta)

            if not xiq_library_at_class_level.xflowsmanageDevices.select_device(node.mac):
                pytest.fail("Failed to select")

            # Update configuration on device and check if the process is completed without error
            if not xiq_library_at_class_level.xflowsmanageDevices.update_switch_complete(node.mac) == 1:
                pytest.fail("Failed to update policy ")

            # Check device update status
            if not xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(
                    device_mac=node.mac) == 1:
                pytest.fail("The update was not finished successfully")

    @pytest.mark.tcxm_25566
    @pytest.mark.dependson("tcxm_25573")
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    def test_tcxm_25566(self, node, logger, xiq_library_at_class_level):
        """ TCXM-25573 - Select at least 2 ports that are configured on "Access Port" Port Type,
        enter on "Multi-Edit" window, create a new Port Type profile, save the configuration
        and check if the updates are successfully."""
        """ TCXM-25566 - Check the display of correct fields when Port Type is configured to an existing 
        Port Type Profile"""

        logger.info("The test TCXM_25566 was run in the test TCXM_25573")

    @pytest.mark.tcxm_25577
    @pytest.mark.dependson("tcxm_25562")
    @pytest.mark.dependson("tcxm_25563")
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p2
    def test_tcxm_25577(self, node, logger, xiq_library_at_class_level):
        """ TCXM-25562 - Check availability of "VLAN" field when Port Type is "Access Port"
        configure all fields and verify if the settings are saved successfully and update the device without error."""
        """ TCXM-25563 - Check availability of "VLAN" fields (native VLAN and allowed VLAN) 
        when Port Type is "Trunk Port", configure all fields and verify if the settings are saved 
        and upload on the device without errors."""
        """ TCXM-25577 - Select at least 2 ports, and edit all available fields in the Multi Edit window."""

        logger.info("The test TCXM_25577 was run in the test TCXM_25562 and also in the test TCXM_25563")

    @pytest.mark.tcxm_25579
    @pytest.mark.dependson("tcxm_25562")
    @pytest.mark.dependson("tcxm_25563")
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    def test_tcxm_25579(self, node, logger, xiq_library_at_class_level):
        """ TCXM-25562 - Check availability of "VLAN" field when Port Type is "Access Port"
        configure all fields and verify if the settings are saved successfully and update the device without error."""
        """ TCXM-25563 - Check availability of "VLAN" fields (native VLAN and allowed VLAN) 
        when Port Type is "Trunk Port", configure all fields and verify if the settings are saved 
        and upload on the device without errors."""
        """ TCXM-25579 - Validate successful multi-edit configuration."""

        logger.info("The test TCXM_25579 was run in the test TCXM_25562 and also in the test TCXM_25563")
