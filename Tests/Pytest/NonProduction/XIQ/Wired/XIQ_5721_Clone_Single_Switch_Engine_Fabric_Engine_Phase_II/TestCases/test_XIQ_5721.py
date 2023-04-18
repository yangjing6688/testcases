import pytest


@pytest.mark.p1
@pytest.mark.development
@pytest.mark.testbed_2_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class XIQ5721Tests:

    auditlog = None
    original_device_os = None
    
    @pytest.fixture(scope="class", autouse=True)
    def make_sure_node_2_is_onboarded(self, revert_node, node_2, xiq_library_at_class_level):
        try:
            yield
        finally:
            revert_node(node_2, xiq_library_at_class_level, assign_network_policy=False, push_network_policy=False)
        
    @pytest.mark.tcxm_precondition
    def test_tcxm_precondition(self, xiq_library_at_class_level, node_1, node_1_policy_name,
                               node_1_template_name, node_2, network_manager, get_random_word, logger, cli, utils):
        """
            Author        : rioanbobi@extremenetworks.com
            Preconditions : Original device have Policy Template assigned and Device Level Config present.
                            Replacement and original device have the same or the latest NOS version.
            Platform supported: EXOS/SwitchEngine, VOSS/FabricEngine standalone
        """

        port_type_exos_access = f"Port_type_exos_access_{get_random_word()}"
        port_type_voss_access = f"Port_type_voss_access_{get_random_word()}"
        port_numbers = '11,12,13,14,15'

        template_exos_access = {'name': [port_type_exos_access, port_type_exos_access],
                                'description': [None, None],
                                'status': [None, 'on'],
                                'port usage': ['access port', 'access'],
                                'page2 accessVlanPage': ['next_page', None],
                                'vlan': ['2', '2'],
                                'page3 transmissionSettings': ["next_page", None],
                                'page4 stp': ["next_page", None],
                                'page5 stormControlSettings': ["next_page", None],
                                'page6 MACLOCKINGSettingsPage': ["next_page", None],
                                'mac locking': ["click", "On"],
                                'max first arrival': ["20", "20"],
                                'page7 ELRPSettingsPage': ["next_page", None],
                                'elrp status': ["click", "enabled"],
                                'page8 pseSettings': ["next_page", None],
                                'page9 summary': ["next_page", None]
                                }

        template_voss_access = {'name': [port_type_voss_access, port_type_voss_access],
                                'description': [None, None],
                                'status': [None, 'on'],
                                'auto-sense': ['click', None],
                                'port usage': ['access port', 'access'],
                                'page2 accessVlanPage': ['next_page', None],
                                'vlan': ['2', '2'],
                                'page3 transmissionSettings': ["next_page", None],
                                'page4 stp': ["next_page", None],
                                'page5 stormControlSettings': ["next_page", None],
                                'page6 pseSettings': ["next_page", None],
                                'page7 summary': ["next_page", None]
                                }

        port_type_exos_trunk = f"Port_type_exos_trunk_{get_random_word()}"
        port_type_voss_trunk = f"Port_type_voss_trunk_{get_random_word()}"
        port_numbers_d360 = '5,6,7,8,9'
        port_numbers_d360_voss = '1/5,1/6,1/7,1/8,1/9'

        template_exos_trunk = {'name': [port_type_exos_trunk, port_type_exos_trunk],
                               'description': [None, None],
                               'status': [None, 'on'],
                               'port usage': ['trunk port', 'TRUNK'],
                               'page2 trunkVlanPage': ['next_page', None],
                               'native vlan': ['3', '3'],
                               'page3 transmissionSettings': ["next_page", None],
                               'page4 stp': ["next_page", None],
                               'page5 stormControlSettings': ["next_page", None],
                               'page6 MACLOCKINGSettingsPage': ["next_page", None],
                               'mac locking': [None, "On"],
                               'max first arrival': ["30", "30"],
                               'page7 ELRPSettingsPage': ["next_page", None],
                               'elrp status': [None, "enabled"],
                               'page8 pseSettings': ["next_page", None],
                               'page9 summary': ["next_page", None]
                               }

        template_voss_trunk = {'name': [port_type_voss_trunk, port_type_voss_trunk],
                               'description': [None, None],
                               'status': [None, 'on'],
                               'auto-sense': ['click', None],
                               'port usage': ['trunk port', 'TRUNK'],
                               'page2 trunkVlanPage': ['next_page', None],
                               'native vlan': ['3', '3'],
                               'page3 transmissionSettings': ["next_page", None],
                               'page4 stp': ["next_page", None],
                               'page5 stormControlSettings': ["next_page", None],
                               'page6 pseSettings': ["next_page", None],
                               'page7 summary': ["next_page", None]
                               }

        XIQ5721Tests.original_device_os = xiq_library_at_class_level.xflowscommonDevices. \
            update_network_device_firmware(device_mac=node_1.mac, forceDownloadImage="false")

        network_manager.connect_to_network_element_name(node_1.name)
        network_manager.connect_to_network_element_name(node_2.name)

        logger.step("Check if the devices are the same model")
        sku1 = cli.get_device_model_name(node_2, node_2.cli_type)
        sku2 = cli.get_device_model_name(node_1, node_1.cli_type)

        if sku1 != sku2:
            pytest.fail(f"Devices should be the same SKU; {sku1=}, {sku2=}")

        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name, node_1_template_name, node_1.cli_type)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        logger.step("Create port type and assign it to ports in template")
        if node_1.cli_type == 'exos':
            xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(
                template_exos_access, port_numbers.split(',')[0], verify_summary=False)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(
                port_numbers, port_type_exos_access)
        elif node_1.cli_type == 'voss':
            xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_voss_access, port_numbers.split(',')[0],
                                                           verify_summary=False)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                             port_type_voss_access)

        logger.step("Create port type and assign it to ports in D360")
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node_1.mac)
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360()
        if node_1.cli_type == 'exos':
            xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_exos_trunk, port_numbers_d360.split(',')[0],
                                                           d360=True, verify_summary=False)
            xiq_library_at_class_level.xflowsmanageDevice360.d360_assign_port_type(port_type_exos_trunk, port_numbers_d360)
        elif node_1.cli_type == 'voss':
            xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_voss_trunk, port_numbers_d360_voss.split(',')[0],
                                                           d360=True, verify_summary=False)
            xiq_library_at_class_level.xflowsmanageDevice360.d360_assign_port_type(port_type_voss_trunk, port_numbers_d360_voss)

        xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration_all_switches()
        utils.wait_till(timeout=5)

        xiq_library_at_class_level.xflowsmanageDeviceConfig.close_D360_configuration_page()

        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

        XIQ5721Tests.auditlog = xiq_library_at_class_level.xflowsmanageDeviceConfig.get_device_config_audit_delta(node_1.mac)

        network_manager.close_connection_to_all_network_elements()

    @pytest.mark.tcxm_24842
    @pytest.mark.dependson("tcxm_precondition")
    def test_tcxm_24842(self, xiq_library_at_class_level, logger, node_1, node_2, network_manager, cli, utils):
        """
        Author        : rioanbobi@extremenetworks.com
        Description   : Check Clone Device function is available if the original device is connected to the xiq_library_at_class_level.
                        Select "quick onboard", enter a replacement serial number and initiate the Clonining Operation.
                        Ensure the config clone is successful to the replacement device with original device policy
                        template and device level configs
        Preconditions : Original device have Policy Template assigned and Device Level Config present.
                        Replacement and original device have the same or the latest NOS version.
        Platform supported: EXOS/SwitchEngine, VOSS/FabricEngine standalone
        """
        network_manager.connect_to_network_element_name(node_1.name)
        network_manager.connect_to_network_element_name(node_2.name)

        os_versions = cli.check_os_versions(node_1, node_2)
        logger.info(f"os versions are: {os_versions}")

        device_1 = XIQ5721Tests.original_device_os
        device_2 = None
        
        logger.step("Check if devices have same or different os versions")
        if os_versions == 'different':
            logger.info("OS versions are different. Upgrading device 2...")
            replacement = xiq_library_at_class_level.xflowscommonDevices.search_device(
                device_serial=node_2.serial, select_device=True, ignore_failure=True)
            if replacement != -1:
                logger.info("Replacement device already onboarded. Upgrading it to the latest OS.")
                try:
                    device_2 = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(device_mac=node_2.mac)
                except:
                    pytest.fail("Problem in updating the firmware")

                if device_1 == device_2:
                    logger.info("Devices have the same OS versions")
                else:
                    pytest.fail("Devices still don't have the same versions")
            else:
                logger.info("Trying to onboard replacement device to upgrade it to the latest OS version")
                try:
                    xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_2)
                    xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_2.serial)
                    xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_2.serial)
                    res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(device_serial=node_2.serial)
                    assert res == 'green', f"The device did not come up successfully in the XIQ; Device: {node_2}"

                    device_2 = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(device_mac=node_2.mac)
                except:
                    pytest.fail("Problem in updating the firmware")

                if device_1 == device_2:
                    logger.info("Devices have the same OS versions")
                else:
                    pytest.fail("Devices still don't have the same versions")

        elif os_versions == 'same':
            logger.info("Devices have the same OS versions")

        logger.step("Delete replacement device if it is already onboarded")
        xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_2.serial)
        utils.wait_till()
        
        logger.step("Clone the replacement device")
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
        xiq_library_at_class_level.xflowsmanageDevices.clone_device_quick_onboard(device_serial=node_1.serial,
                                                           replacement_device_type="Quick Onboard",
                                                           replacement_serial=node_2.serial,
                                                           continue_if_replacement_disconnected=True)
        xiq_library_at_class_level.xflowsmanageDevices.wait_until_device_online(node_2.serial)

        audit_dut1 = XIQ5721Tests.auditlog

        logger.step("Get the audit delta config from replacement device")
        audit_dut2 = xiq_library_at_class_level.xflowsmanageDeviceConfig.get_device_config_audit_delta(node_2.mac)

        network_manager.close_connection_to_all_network_elements()
        logger.info("It compares the audit result from the original device with the audit result from the replacement to see if they match")
        audit_dut1 = xiq_library_at_class_level.xflowsmanageDeviceConfig.clear_audit_commands(audit_dut1)
        audit_dut2 = xiq_library_at_class_level.xflowsmanageDeviceConfig.clear_audit_commands(audit_dut2)

        set_audit_dut1 = set(audit_dut1)
        set_audit_dut2 = set(audit_dut2)

        assert set_audit_dut1 == set_audit_dut2, "commands are not the same"
        logger.info("Commands are the same")

        xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_2.serial)
        utils.wait_till()

    @pytest.mark.tcxm_24843
    @pytest.mark.dependson("tcxm_precondition")
    def test_tcxm_24843(self, xiq_library_at_class_level, logger, node_1, node_2, network_manager, cli, utils, request):
        """
        Author        : rioanbobi@extremenetworks.com
        Description   : Check Clone Device function is available even if the original device
                        is onboarded but not connected to the xiq_library_at_class_level.
                        Select "quick onboard", enter a replacement serial number and initiate the Clonining Operation.
                        Ensure the config clone is successful to the replacement device with original device policy
                        template and device level configs
        Preconditions : Original device have Policy Template assigned and Device Level Config present.
                        Replacement and original device have the same or the latest NOS version.
        Platform supported: EXOS/SwitchEngine, VOSS/FabricEngine standalone
        """
        network_manager.connect_to_network_element_name(node_1.name)
        network_manager.connect_to_network_element_name(node_2.name)

        os_versions = cli.check_os_versions(node_1, node_2)
        logger.info(f"os versions are: {os_versions}")

        device_1 = XIQ5721Tests.original_device_os
        device_2 = None
        
        def func():
            network_manager.connect_to_network_element_name(node_1.name)
            logger.step("Connect back the cloning device to XIQ")
            cli.disable_enable_iqagent_clone_device(device=node_1, iqagent_option='enable')
            xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_1.serial)

            network_manager.close_connection_to_all_network_elements()

            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_2.serial)
            utils.wait_till()
        request.addfinalizer(func)
        
        logger.step("Check if devices have same or different os versions")
        if os_versions == 'different':
            logger.info("OS versions are different. Upgrading device 2...")
            replacement = xiq_library_at_class_level.xflowscommonDevices.search_device(device_serial=node_2.serial, select_device=True,
                                                                ignore_failure=True)
            if replacement != -1:
                logger.info("Replacement device already onboarded. Upgrading it to the latest OS.")
                try:
                    device_2 = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(device_mac=node_2.mac)
                except:
                    pytest.fail("Problem in updating the firmware")

                if device_1 == device_2:
                    logger.info("Devices have the same OS versions")
                else:
                    pytest.fail("Devices still don't have the same versions")
            else:
                logger.info("Trying to onboard replacement device to upgrade it to the latest OS version")
                try:
                    xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_2)
                    xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_2.serial)
                    xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_2.serial)
                    res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(device_serial=node_2.serial)
                    assert res == 'green', f"The device did not come up successfully in the XIQ; Device: {node_2}"

                    device_2 = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(device_mac=node_2.mac)
                except:
                    pytest.fail("Problem in updating the firmware")

                if device_1 == device_2:
                    logger.info("Devices have the same OS versions")
                else:
                    pytest.fail("Devices still don't have the same versions")

        elif os_versions == 'same':
            logger.info("Devices have the same OS versions")

        logger.step("Delete replacement device if it is already onboarded")
        xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_2.serial)
        utils.wait_till()
        
        logger.step("disable iqagent for original device to be not connected to the cloud")
        cli.disable_enable_iqagent_clone_device(device=node_1, iqagent_option='disable')

        logger.step("Clone the replacement device")
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
        xiq_library_at_class_level.xflowsmanageDevices.clone_device_quick_onboard(device_serial=node_1.serial,
                                                           replacement_device_type="Quick Onboard",
                                                           replacement_serial=node_2.serial,
                                                           continue_if_replacement_disconnected=True)
        xiq_library_at_class_level.xflowsmanageDevices.wait_until_device_online(node_2.serial)
        audit_dut1 = XIQ5721Tests.auditlog
        
        logger.step("Get the audit delta config from replacement device")
        audit_dut2 = xiq_library_at_class_level.xflowsmanageDeviceConfig.get_device_config_audit_delta(node_2.mac)
        xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()

        logger.step("It compares the audit result from the original device with the audit result from the replacement to see if they match")
        audit_dut1 = xiq_library_at_class_level.xflowsmanageDeviceConfig.clear_audit_commands(audit_dut1)
        audit_dut2 = xiq_library_at_class_level.xflowsmanageDeviceConfig.clear_audit_commands(audit_dut2)

        set_audit_dut1 = set(audit_dut1)
        set_audit_dut2 = set(audit_dut2)

        if set_audit_dut1 == set_audit_dut2:
            logger.info("Commands are the same")
        else:
            pytest.fail("commands are not the same")

    @pytest.mark.tcxm_24844
    @pytest.mark.dependson("tcxm_precondition")
    def test_tcxm_24844(self, xiq_library_at_class_level, logger, node_1, node_2, network_manager, cli, utils, request):
        """
        Author        : rioanbobi@extremenetworks.com
        Description   : Check Clone Device function is available even if the original device
                        is onboarded but unmanaged in xiq_library_at_class_level.
                        Select "quick onboard", enter a replacement serial number and initiate the Clonining Operation.
                        Ensure the config clone is successful to the replacement device with original device policy
                        template and device level configs
        Preconditions : Original device have Policy Template assigned and Device Level Config present.
                        Replacement and original device have the same or the latest NOS version.
        Platform supported: EXOS/SwitchEngine, VOSS/FabricEngine standalone
        """
        network_manager.connect_to_network_element_name(node_1.name)
        network_manager.connect_to_network_element_name(node_2.name)

        os_versions = cli.check_os_versions(node_1, node_2)
        logger.info(f"os versions are: {os_versions}")

        device_1 = XIQ5721Tests.original_device_os
        device_2 = None
        
        def func():
            logger.step("Put back the original device in managed state")
            xiq_library_at_class_level.xflowsmanageDevices.change_manage_device_status(device_mac=node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevices.wait_until_device_online(node_1.serial)
            xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_1.serial)

            network_manager.close_connection_to_all_network_elements()
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_2.serial)
            utils.wait_till()
        
        request.addfinalizer(func)
        
        logger.step("Check if devices have same or different os versions")
        if os_versions == 'different':
            logger.info("OS versions are different. Upgrading device 2...")
            replacement = xiq_library_at_class_level.xflowscommonDevices.search_device(device_serial=node_2.serial, select_device=True,
                                                                ignore_failure=True)
            if replacement != -1:
                logger.info("Replacement device already onboarded. Upgrading it to the latest OS.")
                try:
                    device_2 = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(device_mac=node_2.mac)
                except:
                    pytest.fail("Problem in updating the firmware")

                if device_1 == device_2:
                    logger.info("Devices have the same OS versions")
                else:
                    pytest.fail("Devices still don't have the same versions")
            else:
                logger.info("Trying to onboard replacement device to upgrade it to the latest OS version")
                try:
                    xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_2)
                    xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_2.serial)
                    xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_2.serial)
                    res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(device_serial=node_2.serial)
                    assert res == 'green', f"The device did not come up successfully in the XIQ; Device: {node_2}"

                    device_2 = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(device_mac=node_2.mac)
                except:
                    pytest.fail("Problem in updating the firmware")

                if device_1 == device_2:
                    logger.info("Devices have the same OS versions")
                else:
                    pytest.fail("Devices still don't have the same versions")

        elif os_versions == 'same':
            logger.info("Devices have the same OS versions")

        logger.step("Delete replacement device if it is already onboarded")
        xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_2.serial)
        utils.wait_till()
        
        logger.step("Put the original device in unmanaged state")
        xiq_library_at_class_level.xflowsmanageDevices.change_manage_device_status(manage_type='UNMANAGE', device_mac=node_1.mac)

        logger.step("Clone the replacement device")
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
        xiq_library_at_class_level.xflowsmanageDevices.clone_device_quick_onboard(device_serial=node_1.serial,
                                                           replacement_device_type="Quick Onboard",
                                                           replacement_serial=node_2.serial,
                                                           continue_if_replacement_disconnected=True)
        xiq_library_at_class_level.xflowsmanageDevices.wait_until_device_online(node_2.serial)
        audit_dut1 = XIQ5721Tests.auditlog
        
        logger.step("Get the audit delta config from replacement device")
        audit_dut2 = xiq_library_at_class_level.xflowsmanageDeviceConfig.get_device_config_audit_delta(node_2.mac)
        xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()

        logger.step("It compares the audit result from the original device with the audit result from the replacement to see if they match")
        audit_dut1 = xiq_library_at_class_level.xflowsmanageDeviceConfig.clear_audit_commands(audit_dut1)
        audit_dut2 = xiq_library_at_class_level.xflowsmanageDeviceConfig.clear_audit_commands(audit_dut2)

        set_audit_dut1 = set(audit_dut1)
        set_audit_dut2 = set(audit_dut2)

        if set_audit_dut1 == set_audit_dut2:
            logger.info("Commands are the same")
        else:
            pytest.fail("commands are not the same")

    @pytest.mark.tcxm_24845
    @pytest.mark.dependson("tcxm_precondition")
    def test_tcxm_24845(self, xiq_library_at_class_level, logger, node_1, node_2, network_manager, cli, utils):
        """
        Author        : rioanbobi@extremenetworks.com
        Description   : Check Clone Device function is available if the original device is connected to the xiq_library_at_class_level.
                        Select "quick onboard", enter a replacement serial number and initiate the Clonining Operation.
                        Ensure the config clone is successful to the replacement device with original device policy
                        template and device level configs
        Preconditions : Original device have Policy Template assigned and Device Level Config present.
                        Replacement and original device have different NOS version.
        Platform supported: EXOS/SwitchEngine, VOSS/FabricEngine standalone
        """
        network_manager.connect_to_network_element_name(node_1.name)
        network_manager.connect_to_network_element_name(node_2.name)

        os_versions = cli.check_os_versions(node_1, node_2)
        logger.info(f"os versions are: {os_versions}")

        device_1 = XIQ5721Tests.original_device_os
        device_2 = None
        
        logger.step("Check if devices have same or different os versions")
        if os_versions == 'same':
            logger.info("OS versions are the same. Upgrading device 2...")
            replacement = xiq_library_at_class_level.xflowscommonDevices.search_device(device_serial=node_2.serial, select_device=True,
                                                                ignore_failure=True)
            if replacement != -1:
                logger.info("Replacement device already onboarded. Upgrading it to a different OS.")
                try:
                    if node_2.cli_type.lower() == 'voss':
                        device_2 = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(
                            device_mac=node_2.mac,
                            version='noncurrent',
                            updateTo="noncurrent",
                            forceDownloadImage="false")
                        logger.info(f"Clone device has {device_2} version")

                    elif node_2.cli_type.lower() == 'exos':
                        device_2 = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(
                            device_mac=node_2.mac,
                            version='noncurrent',
                            updateTo='noncurrent',
                            forceDownloadImage="false")
                        logger.info(f"Clone device has {device_2} version")
                    else:
                        pytest.fail("No cli type found")
                except:
                    pytest.fail("Problem in updating the firmware")

                if device_1 != device_2:
                    logger.info("Devices have different OS versions")
                else:
                    pytest.fail("Devices still have the same OS versions")
            else:
                logger.info("Trying to onboard replacement device to upgrade it to a different OS version")
                try:
                    xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_2)
                    xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_2.serial)
                    xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_2.serial)
                    res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(device_serial=node_2.serial)
                    assert res == 'green', f"The device did not come up successfully in the XIQ; Device: {node_2}"

                    if node_2.cli_type.lower() == 'voss':
                        device = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(
                            device_mac=node_2.mac,
                            version='noncurrent',
                            updateTo="noncurrent")
                        logger.info(f"Clone device has {device} version")

                    elif node_2.cli_type.lower() == 'exos':
                        device = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(
                            device_mac=node_2.mac,
                            version='noncurrent',
                            updateTo='noncurrent')
                        logger.info(f"Clone device has {device} version")
                    else:
                        pytest.fail("No cli type found")
                except:
                    pytest.fail("Problem in updating the firmware")

                if device_1 != device_2:
                    logger.info("Devices have different OS versions")
                else:
                    pytest.fail("Devices still have the same OS versions")

        elif os_versions == 'different':
            logger.info("Devices have different OS versions")

        logger.step("Delete replacement device if it is already onboarded")
        xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_2.serial)
        utils.wait_till()
        
        logger.step("Clone the replacement device")
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
        xiq_library_at_class_level.xflowsmanageDevices.clone_device_quick_onboard(device_serial=node_1.serial,
                                                           replacement_device_type="Quick Onboard",
                                                           replacement_serial=node_2.serial,
                                                           continue_if_replacement_disconnected=True)
        xiq_library_at_class_level.xflowsmanageDevices.wait_until_device_online(node_2.serial)
        audit_dut1 = XIQ5721Tests.auditlog

        logger.step("Get the audit delta config from replacement device")
        audit_dut2 = xiq_library_at_class_level.xflowsmanageDeviceConfig.get_device_config_audit_delta(node_2.mac)
        network_manager.close_connection_to_all_network_elements()

        logger.step("It compares the audit result from the original device with the audit result from the replacement to see if they match")
        audit_dut1 = xiq_library_at_class_level.xflowsmanageDeviceConfig.clear_audit_commands(audit_dut1)
        audit_dut2 = xiq_library_at_class_level.xflowsmanageDeviceConfig.clear_audit_commands(audit_dut2)

        set_audit_dut1 = set(audit_dut1)
        set_audit_dut2 = set(audit_dut2)

        if set_audit_dut1 == set_audit_dut2:
            logger.info("Commands are the same")
        else:
            pytest.fail("commands are not the same")

        xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_2.serial)
        utils.wait_till()

    @pytest.mark.tcxm_24846
    @pytest.mark.dependson("tcxm_precondition")
    def test_tcxm_24846(self, xiq_library_at_class_level, logger, node_1, node_2, network_manager, cli, utils, request):
        """
        Author        : rioanbobi@extremenetworks.com
        Description   : Check Clone Device function is available even if the original device
                        is onboarded but not connected to the xiq_library_at_class_level.
                        Select "quick onboard", enter a replacement serial number and initiate the Clonining Operation.
                        Ensure the config clone is successful to the replacement device with original device policy
                        template and device level configs
        Preconditions : Original device have Policy Template assigned and Device Level Config present.
                        Replacement and original device have different NOS version.
        Platform supported: EXOS/SwitchEngine, VOSS/FabricEngine standalone
        """
        network_manager.connect_to_network_element_name(node_1.name)
        network_manager.connect_to_network_element_name(node_2.name)

        os_versions = cli.check_os_versions(node_1, node_2)
        logger.info(f"os versions are: {os_versions}")

        device_1 = XIQ5721Tests.original_device_os
        device_2 = None
        
        def func():
            network_manager.connect_to_network_element_name(node_1.name)
            logger.step("Connect back the cloning device to XIQ")
            cli.disable_enable_iqagent_clone_device(device=node_1, iqagent_option='enable')
            xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_1.serial)

            network_manager.close_connection_to_all_network_elements()
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_2.serial)
            utils.wait_till()
            
        request.addfinalizer(func)
        
        logger.step("Check if devices have same or different os versions")
        
        if os_versions == 'same':
            logger.info("OS versions are the same. Upgrading device 2...")
            replacement = xiq_library_at_class_level.xflowscommonDevices.search_device(device_serial=node_2.serial, select_device=True,
                                                                ignore_failure=True)
            if replacement != -1:
                logger.info("Replacement device already onboarded. Upgrading it to a different OS.")
                try:
                    if node_2.cli_type.lower() == 'voss':
                        device_2 = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(
                            device_mac=node_2.mac,
                            version='noncurrent',
                            updateTo='noncurrent')
                        logger.info(f"Clone device has {device_2} version")

                    elif node_2.cli_type.lower() == 'exos':
                        device_2 = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(
                            device_mac=node_2.mac,
                            version='noncurrent',
                            updateTo='noncurrent')
                        logger.info(f"Clone device has {device_2} version")
                    else:
                        pytest.fail("No cli type found")
                except:
                    pytest.fail("Problem in updating the firmware")

                if device_1 != device_2:
                    logger.info("Devices have different OS versions")
                else:
                    pytest.fail("Devices still have the same OS versions")
            else:
                logger.info("Trying to onboard replacement device to upgrade it to a different OS version")
                try:
                    xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_2)
                    xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_2.serial)
                    xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_2.serial)
                    res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(device_serial=node_2.serial)
                    assert res == 'green', f"The device did not come up successfully in the XIQ; Device: {node_2}"

                    if node_2.cli_type.lower() == 'voss':
                        device = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(
                            device_mac=node_2.mac,
                            version='noncurrent',
                            updateTo="noncurrent",
                            forceDownloadImage='false')
                        logger.info(f"Clone device has {device} version")

                    elif node_2.cli_type.lower() == 'exos':
                        device = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(
                            device_mac=node_2.mac,
                            version='noncurrent',
                            updateTo='noncurrent',
                            forceDownloadImage='false')
                        logger.info(f"Clone device has {device} version")
                    else:
                        pytest.fail("No cli type found")
                except:
                    pytest.fail("Problem in updating the firmware")

                if device_1 != device_2:
                    logger.info("Devices have different OS versions")
                else:
                    pytest.fail("Devices still have the same OS versions")

        elif os_versions == 'different':
            logger.info("Devices have different OS versions")

        logger.step("Delete replacement device if it is already onboarded")
        
        xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_2.serial)
        utils.wait_till()
        
        logger.step("disable iqagent for original device to be not connected to the cloud")
        cli.disable_enable_iqagent_clone_device(device=node_1, iqagent_option='disable')

        logger.step("Clone the replacement device")
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
        xiq_library_at_class_level.xflowsmanageDevices.clone_device_quick_onboard(device_serial=node_1.serial,
                                                           replacement_device_type="Quick Onboard",
                                                           replacement_serial=node_2.serial,
                                                           continue_if_replacement_disconnected=True)
        xiq_library_at_class_level.xflowsmanageDevices.wait_until_device_online(node_2.serial)
        audit_dut1 = XIQ5721Tests.auditlog
        
        logger.step("Get the audit delta config from replacement device")
        audit_dut2 = xiq_library_at_class_level.xflowsmanageDeviceConfig.get_device_config_audit_delta(node_2.mac)
        xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()

        logger.step("It compares the audit result from the original device with the audit result from the replacement to see if they match")
        audit_dut1 = xiq_library_at_class_level.xflowsmanageDeviceConfig.clear_audit_commands(audit_dut1)
        audit_dut2 = xiq_library_at_class_level.xflowsmanageDeviceConfig.clear_audit_commands(audit_dut2)

        set_audit_dut1 = set(audit_dut1)
        set_audit_dut2 = set(audit_dut2)

        if set_audit_dut1 == set_audit_dut2:
            logger.info("Commands are the same")
        else:
            pytest.fail("commands are not the same")

    @pytest.mark.tcxm_24847
    @pytest.mark.dependson("tcxm_precondition")
    def test_tcxm_24847(self, xiq_library_at_class_level, logger, node_1, node_2, network_manager, cli, utils, request):
        """
        Author        : rioanbobi@extremenetworks.com
        Description   : Check Clone Device function is available even if the original device
                        is onboarded but unmanaged in xiq_library_at_class_level.
                        Select "quick onboard", enter a replacement serial number and initiate the Clonining Operation.
                        Ensure the config clone is successful to the replacement device with original device policy
                        template and device level configs
        Preconditions : Original device have Policy Template assigned and Device Level Config present.
                        Replacement and original device have different NOS version.
        Platform supported: EXOS/SwitchEngine, VOSS/FabricEngine standalone
        """
        network_manager.connect_to_network_element_name(node_1.name)
        network_manager.connect_to_network_element_name(node_2.name)

        os_versions = cli.check_os_versions(node_1, node_2)
        logger.info(f"os versions are: {os_versions}")

        device_1 = XIQ5721Tests.original_device_os
        device_2 = None
        
        def func():
            logger.step("Put back the original device in managed state")
            xiq_library_at_class_level.xflowsmanageDevices.change_manage_device_status(device_mac=node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevices.wait_until_device_online(node_1.serial)
            xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_1.serial)

            network_manager.close_connection_to_all_network_elements()
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_2.serial)
            utils.wait_till()
            
        request.addfinalizer(func)
        
        logger.step("Check if devices have same or different os versions")
        
        if os_versions == 'same':
            logger.info("OS versions are the same. Upgrading device 2...")
            replacement = xiq_library_at_class_level.xflowscommonDevices.search_device(device_serial=node_2.serial, select_device=True,
                                                                ignore_failure=True)
            if replacement != -1:
                logger.info("Replacement device already onboarded. Upgrading it to a different OS.")
                try:
                    if node_2.cli_type.lower() == 'voss':
                        device_2 = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(
                            device_mac=node_2.mac,
                            version='noncurrent',
                            updateTo='noncurrent')
                        logger.info(f"Clone device has {device_2} version")

                    elif node_2.cli_type.lower() == 'exos':
                        device_2 = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(
                            device_mac=node_2.mac,
                            version='noncurrent',
                            updateTo='noncurrent')
                        logger.info(f"Clone device has {device_2} version")
                    else:
                        pytest.fail("No cli type found")
                except:
                    pytest.fail("Problem in updating the firmware")

                if device_1 != device_2:
                    logger.info("Devices have different OS versions")
                else:
                    pytest.fail("Devices still have the same OS versions")
            else:
                logger.info("Trying to onboard replacement device to upgrade it to a different OS version")
                try:
                    xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_2)
                    xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_2.serial)
                    xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_2.serial)
                    res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(device_serial=node_2.serial)
                    assert res == 'green', f"The device did not come up successfully in the XIQ; Device: {node_2}"

                    if node_2.cli_type.lower() == 'voss':
                        device = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(
                            device_mac=node_2.mac,
                            version='noncurrent',
                            updateTo='noncurrent',
                            forceDownloadImage='false')
                        logger.info(f"Clone device has {device} version")

                    elif node_2.cli_type.lower() == 'exos':
                        device = xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(
                            device_mac=node_2.mac,
                            version='noncurrent',
                            updateTo='noncurrent',
                            forceDownloadImage='false')
                        logger.info(f"Clone device has {device} version")
                    else:
                        pytest.fail("No cli type found")
                except:
                    pytest.fail("Problem in updating the firmware")

                if device_1 != device_2:
                    logger.info("Devices have different OS versions")
                else:
                    pytest.fail("Devices still have the same OS versions")

        elif os_versions == 'different':
            logger.info("Devices have different OS versions")

        logger.step("Delete replacement device if it is already onboarded")
        
        xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_2.serial)
        utils.wait_till()
        
        logger.step("Put the original device in unmanaged state")
        xiq_library_at_class_level.xflowsmanageDevices.change_manage_device_status(manage_type='UNMANAGE',
                                                            device_mac=node_1.mac)

        logger.step("Clone the replacement device")
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
        xiq_library_at_class_level.xflowsmanageDevices.clone_device_quick_onboard(device_serial=node_1.serial,
                                                           replacement_device_type="Quick Onboard",
                                                           replacement_serial=node_2.serial,
                                                           continue_if_replacement_disconnected=True)
        xiq_library_at_class_level.xflowsmanageDevices.wait_until_device_online(node_2.serial)
        audit_dut1 = XIQ5721Tests.auditlog
        
        logger.step("Get the audit delta config from replacement device")
        audit_dut2 = xiq_library_at_class_level.xflowsmanageDeviceConfig.get_device_config_audit_delta(node_2.mac)
        xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()

        logger.step("It compares the audit result from the original device with the audit result from the replacement to see if they match")
        audit_dut1 = xiq_library_at_class_level.xflowsmanageDeviceConfig.clear_audit_commands(audit_dut1)
        audit_dut2 = xiq_library_at_class_level.xflowsmanageDeviceConfig.clear_audit_commands(audit_dut2)

        set_audit_dut1 = set(audit_dut1)
        set_audit_dut2 = set(audit_dut2)

        if set_audit_dut1 == set_audit_dut2:
            logger.info("Commands are the same")
        else:
            pytest.fail("commands are not the same")
