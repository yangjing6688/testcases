import pytest
import random
import string
import time


# Function to generate random word of 12 characters
def random_word(x=12):
    randword = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(x))
    return randword


# Global Vars


class XIQ1059Tests:
    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_19955
    @pytest.mark.p1
    def test_tcxm_19955(self, node, logger, node_policy_name, node_template_name, cli,
                        xiq_library_at_class_level, loaded_config, utils, config_helper, network_manager,
                        default_library):
        """
        Description   : Configure mac locking on a port type in Template configuration
        Step            Step Description
         1              Onboard one EXOS device
         2              Configure a policy-template with mac-locking on and click save
         3              Create a port type with mac-locking on
         4              Configure following Mac-locking properties:
                        "Maximum first arrival" as "10"
         5              Configure policy-template to device and push config
         6              Send 11 source MACs on port from traffic generator
         7              Check in Monitor - > Overview page
         8              Delete the onboarded device and logout from XIQ(Teardown)
        """

        loaded_config['${TEST_NAME}'] = 'test_tcxm_19955'
        D360Flag = 0
        tgen_port = config_helper.createTgenPort(config_helper.tgen1_name, config_helper.tgen_dut1_port_a.ifname)
        assert  tgen_port, "Tgen port not generated"
        logger.info(f"tgen ports are: {tgen_port}")
        isl_ports_dut = config_helper.create_ports_list(node.tgen)
        logger.info(f'isl ports are: {isl_ports_dut}')
        mac_add_list = ['00:00:00:00:00:01', '00:00:00:00:00:02', '00:00:00:00:00:03', '00:00:00:00:00:04',
                        '00:00:00:00:00:05', '00:00:00:00:00:06', '00:00:00:00:00:07', '00:00:00:00:00:08',
                        '00:00:00:00:00:09', '00:00:00:00:01:01', '00:00:00:00:01:02', ]

        port_status_to_be_checked = "Disabled by MAC Locking"
        maclock_state_to_be_checked = "Enabled"

        template_mac = {'name': ["MLport_type_mac", "MLport_type_mac"],
                        'description': [None, None],
                        'status': [None, 'on'],
                        'page2 accessVlanPage': ['next_page', None],
                        'page3 transmissionSettings': ["next_page", None],
                        'page4 stp': ["next_page", None],
                        'page5 stormControlSettings': ["next_page", None],
                        'page6 MACLOCKINGSettingsPage': ["next_page", None],
                        'mac locking': ["click", "On"],
                        'max first arrival': ["10", "10"],
                        'disable port': ["click", "Enabled"],
                        'page 7 ELRP': ["next_page", None],
                        'page8 pseSettings': ["next_page", None],
                        'page9 summary': ["next_page", None]
                        }

        # randomize port template name:
        nr = random.randint(0, 1000)
        port_type_name = template_mac['name'][0] + "_" + str(nr)
        template_mac['name'][0] = port_type_name
        template_mac['name'][1] = port_type_name

        is_configured = False

        try:
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                pytest.fail("This test should run only on an EXOS standalone device")
            elif node.cli_type.upper() == "EXOS":

                assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                    node_policy_name, node_template_name, status="ON")
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                            node_template_name,
                                                                                            node.cli_type)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                create_port = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_mac,
                                                                                                    isl_ports_dut[0],
                                                                                                    d360=False)
                if create_port:
                    logger.info("Port type was created")
                else:
                    pytest.fail("Could not create the required port type")
                is_configured = True

                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

                assert xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(
                    node_policy_name, node.mac)

                res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(serial=node.serial,
                                                                            policy_name=node_policy_name, IRV=False)
                if res == -1:
                    logger.step("Update failed, trying to do a Delta Update")
                    xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node.serial)
                    xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)
                assert res == 1, f"Failed to update network policy to the device"

                loaded_config['${TEST_NAME}'] = 'test_tcxm_19955 : Traffic'
                default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()
                default_library.apiUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                                                                                          config_helper.dut1_tgen_port_a.ifname)
                # default_library.apiUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                #                                                                           config_helper.dut1_tgen_port_a.ifname)
                default_library.apiUdks.trafficGenerationUdks.send_source_macs_on_port_from_traffic_generator(
                    mac_add_list, tgen_port)
                default_library.apiUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(config_helper.dut1_name, "10")
                default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()
                logger.step("Check in Monitor - > Overview page -> Port status")
                loaded_config['${TEST_NAME}'] = 'test_tcxm_19955 - Checking'

                logger.step("Check in Monitor - > Overview page")
                loaded_config['${TEST_NAME}'] = 'test_tcxm_19955 - Checking'
                network_manager.connect_to_network_element_name(node.name)
                enabled_mac_loc_on_ports_cli = cli.show_maclocking_on_the_ports_in_cli(node)
                network_manager.close_connection_to_network_element(node.name)
                found = False
                for i in enabled_mac_loc_on_ports_cli:
                    if i[0] == isl_ports_dut[0] and i[1] == 'ena':
                        logger.info(f"Port {isl_ports_dut[0]} is configured for MAC locking in CLI.")
                        found = True
                        break
                    else:
                        continue
                assert found, f"MAC locking was not enabled on CLI on port {isl_ports_dut[0]}"
                D360Flag = xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac)

                logger.info("******Checking Port Status******")

                check_status = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                    isl_ports_dut[0], column_name="PORT STATUS")
                max_wait = 10
                count = 0
                while check_status != port_status_to_be_checked and count < max_wait:
                    time.sleep(2)
                    count += 1
                    check_status = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                        isl_ports_dut[0], column_name="PORT STATUS")
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_status == port_status_to_be_checked:
                    logger.info("Port status is - Disabled by MAC Locking")
                else:
                    pytest.fail(f"Port status is - {check_status}")

                logger.info("******Checking Port State******")
                check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                    isl_ports_dut[0], column_name="MAC LOCKING")
                logger.step("Check in Monitor - > Overview page ->Mac Locking state")
                max_wait = 10
                count = 0
                while check_state != maclock_state_to_be_checked and count < max_wait:
                    time.sleep(2)
                    count += 1
                    check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                        isl_ports_dut[0], column_name="MAC LOCKING")
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_state == maclock_state_to_be_checked:
                    logger.info("MAC Locking state is - Enabled")
                else:
                    pytest.fail(f"MAC Locking state is {check_state}")
                D360Flag = -(xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window())

        finally:

            loaded_config['${TEST_NAME}'] = 'test_tcxm_19955 : Cleanup'
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                logger.info("Test case works only in EXOS")
            elif node.cli_type.upper() == "EXOS":
                if is_configured:

                    if D360Flag == 1:
                        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

                    assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                        node_policy_name, node_template_name, status="OFF")
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                                node_template_name,
                                                                                                node.cli_type)
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.revert_port_configuration_template_level("Access Port")

                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                    res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name)
                    assert res == 1, f"Failed to update network policy to the device"

                    # Delete the port type created
                    xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(
                        template_mac["name"][0])

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_19956
    @pytest.mark.p1
    def test_tcxm_19956(self, node, logger, node_policy_name, node_template_name, cli, network_manager,
                        xiq_library_at_class_level, loaded_config, utils, config_helper, default_library):
        """
        Author        : icosmineanu
        Description   : Configure mac locking on a port in device level configuration
        Step                Step Description
         1              Onboard one EXOS device
         2              Configure a policy-template with mac-locking on and click save, Configure policy-template to device.
         3              Configure following Mac-locking properties for a port in D360:
                        "Mac-Locking" as "on"
                        "Maximum first arrival" as "10"
                        "Disable port" as "on"
                        "Link down action" as "Clear first arrival MACs when port link goes down"
                        "Remove aged MACs" as "on"
         4              Click on "Save port configuration" and Push config on device
         5              Send 11 source MACs on port from traffic generator
         6              Check in Monitor - > Overview page
         7              Check in Monitor - > Events page
         8              Delete the onboarded device and logout from XIQ(Teardown)
        """

        loaded_config['${TEST_NAME}'] = 'test_tcxm_19956'
        isl_ports_dut = config_helper.create_ports_list(node.tgen)
        D360Flag = 0
        tgen_port = config_helper.createTgenPort(config_helper.tgen1_name, config_helper.tgen_dut1_port_a.ifname)
        assert tgen_port, "Tgen port not generated"
        logger.info("tgen_port", tgen_port)
        mac_add_list = ['00:00:00:00:00:01', '00:00:00:00:00:02', '00:00:00:00:00:03', '00:00:00:00:00:04',
                        '00:00:00:00:00:05', '00:00:00:00:00:06', '00:00:00:00:00:07', '00:00:00:00:00:08',
                        '00:00:00:00:00:09', '00:00:00:00:01:01', '00:00:00:00:01:02']

        port_status_to_be_checked = "Disabled by MAC Locking"
        maclock_state_to_be_checked = "Enabled"
        event_str = 'MAC address learning limit has been exceeded'

        template_mac = {'name': ["MLport_type_mac", "MLport_type_mac"],
                        'description': [None, None],
                        'status': [None, 'on'],
                        'page2 accessVlanPage': ['next_page', None],
                        'page3 transmissionSettings': ["next_page", None],
                        'page4 stp': ["next_page", None],
                        'page5 stormControlSettings': ["next_page", None],
                        'page6 MACLOCKINGSettingsPage': ["next_page", None],
                        'mac locking': ["click", "On"],
                        'max first arrival': ["10", "10"],
                        'disable port': ["click", "Enabled"],
                        'link down clear': ["click", "Clear"],
                        'remove aged MACs': ["click", "Enabled"],
                        'page7 ELRP': ["next_page", None],
                        'page8 pseSettings': ["next_page", None],
                        'page9 summary': ["next_page", None]
                        }

        # randomize port template name:
        nr = random.randint(0, 1000)
        port_type_name = template_mac['name'][0] + "_" + str(nr)
        template_mac['name'][0] = port_type_name
        template_mac['name'][1] = port_type_name

        is_configured = False

        try:
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                pytest.skip("This test should run on an EXOS device")
            elif node.cli_type.upper() == "EXOS":
                # Configure Mac-locking properties
                assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                    node_policy_name, node_template_name, status="ON")
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

                loaded_config['${TEST_NAME}'] = 'test_tcxm_19956 - Configure'
                res = xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(
                    node_policy_name, node.mac)
                if res != 1:
                    pytest.fail(f"No policy was assigned'{node_policy_name}'")
                else:
                    logger.info("Policy was assigned")

                res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name, IRV=False)
                if res == -1:
                    logger.step("Update failed, trying to do a Delta Update")
                    xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node.serial)
                    xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)
                assert res == 1, f"Failed to update network policy to the device"

                xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac)

                utils.wait_till(
                    xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration, delay=2)
                assert xiq_library_at_class_level.xflowsmanageDevice360.unlock_device360_port_config() == 1
                loaded_config['${TEST_NAME}'] = 'test_tcxm_19956 - Configure D360PortTypes'
                create_port = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_mac,
                                                                                                    isl_ports_dut[0],
                                                                                                    d360=True)
                if create_port:
                    logger.info("Port type was created")
                else:
                    pytest.fail("Could not create the required port type")
                is_configured = True

                xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration()
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
                is_configured = True

                xiq_library_at_class_level.xflowscommonDevices._goto_devices()
                res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name, IRV=False)
                if res == -1:
                    logger.step("Update failed, trying to do a Delta Update")
                    xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node.serial)
                    xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)
                assert res == 1, f"Failed to update network policy to the device"

                loaded_config['${TEST_NAME}'] = 'test_tcxm_19956 - Traffic'
                default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()
                default_library.apiUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                                                                                          config_helper.dut1_tgen_port_a.ifname)
                default_library.apiUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                                                                                          config_helper.dut1_tgen_port_a.ifname)
                default_library.apiUdks.trafficGenerationUdks.send_source_macs_on_port_from_traffic_generator(
                    mac_add_list, tgen_port)
                default_library.apiUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(config_helper.dut1_name, "10")
                default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()

                logger.step("Check in Monitor - > Overview page -> Port status")
                loaded_config['${TEST_NAME}'] = 'test_tcxm_19956 - Checking'
                network_manager.connect_to_network_element_name(node.name)
                enabled_mac_loc_on_ports_cli = cli.show_maclocking_on_the_ports_in_cli(node)
                network_manager.close_connection_to_network_element(node.name)
                found = False
                for i in enabled_mac_loc_on_ports_cli:
                    if i[0] == isl_ports_dut[0] and i[1] == 'ena':
                        logger.info(f"Port {isl_ports_dut[0]} is configured for MAC locking in CLI.")
                        found = True
                        break
                    else:
                        continue
                assert found, f"MAC locking was not enabled on CLI on port {isl_ports_dut[0]}"
                D360Flag = xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac)

                logger.info("******Checking Port Status******")

                check_status = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                    isl_ports_dut[0], column_name="PORT STATUS")
                max_wait = 10
                count = 0
                while check_status != port_status_to_be_checked and count < max_wait:
                    time.sleep(2)
                    count += 1
                    check_status = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                        isl_ports_dut[0], column_name="PORT STATUS")
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_status == port_status_to_be_checked:
                    logger.info("Port status is - Disabled by MAC Locking")
                else:
                    pytest.fail(f"Port status is - {check_status}")

                logger.info("******Checking Port State******")
                check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                    isl_ports_dut[0], column_name="MAC LOCKING")
                logger.step("Check in Monitor - > Overview page ->Mac Locking state")
                max_wait = 10
                count = 0
                while check_state != maclock_state_to_be_checked and count < max_wait:
                    time.sleep(2)
                    count += 1
                    check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                        isl_ports_dut[0], column_name="MAC LOCKING")
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_state == maclock_state_to_be_checked:
                    logger.info("Mac Locking state is - Enabled")
                else:
                    pytest.fail(f"Mac Locking state is {check_state}")

                logger.step("Check in Events page")
                utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_select_events_view, delay=2)
                utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                check_events = xiq_library_at_class_level.xflowsmanageDevice360.device360_search_event_and_confirm_event_description_contains(
                    event_str)
                max_wait = 180
                count = 0
                while not check_events and count < max_wait:
                    time.sleep(2)
                    count += 10
                    check_events = xiq_library_at_class_level.xflowsmanageDevice360.device360_search_event_and_confirm_event_description_contains(
                        event_str)
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_events:
                    logger.info("MAC address learning limit has been exceeded")
                else:
                    pytest.fail("MAC address learning limit has not been exceeded")

                D360Flag = -(xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window())

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_19956 - Cleanup'
            if is_configured:
                logger.info("In finally  - configured True")

                if D360Flag == 1:
                    xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
                assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                    node_policy_name, node_template_name, status="OFF")
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                xiq_library_at_class_level.xflowsmanageDevices.revert_device_to_template(node.serial)
                xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(
                    template_mac["name"][0])

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_19960
    @pytest.mark.p2
    def test_tcxm_19960(self, node, logger, node_policy_name, node_template_name, cli, network_manager,
                        xiq_library_at_class_level, loaded_config, utils, config_helper, default_library):
        """
        Description   : Configure mac locking on a port type in Template configuration
        Step            Step Description
         1              Onboard one EXOS device
         2              Configure a policy-template with mac-locking on and click save
         3              Create a port type with mac-locking on
         4              Configure following Mac-locking properties:
                        "Maximum first arrival" as "5"
         5              Configure policy-template to device
         6              Create another port in d360 for the same  port with max first
                        arrival as 10 and push config
         6              Send 11 source MACs on port from traffic generator
         7              Check in Monitor - > Overview page
         8              Delete the onboarded device and logout from XIQ(Teardown)
        """

        loaded_config['${TEST_NAME}'] = 'test_tcxm_19960'
        isl_ports_dut = config_helper.create_ports_list(node.tgen)

        mac_add_list = ['00:00:00:00:00:01', '00:00:00:00:00:02', '00:00:00:00:00:03', '00:00:00:00:00:04',
                        '00:00:00:00:00:05', '00:00:00:00:00:06', '00:00:00:00:00:07', '00:00:00:00:00:08',
                        '00:00:00:00:00:09', '00:00:00:00:01:01', '00:00:00:00:01:02']

        port_status_to_be_checked = "Disabled by MAC Locking"
        maclock_state_to_be_checked = "Enabled"

        template_mac = {'name': ["port_type_mac", "port_type_mac"],
                        'description': [None, None],
                        'status': [None, 'on'],
                        'page2 accessVlanPage': ['next_page', None],
                        'page3 transmissionSettings': ["next_page", None],
                        'page4 stp': ["next_page", None],
                        'page5 stormControlSettings': ["next_page", None],
                        'page6 MACLOCKINGSettingsPage': ["next_page", None],
                        'mac locking': ["click", "On"],
                        'max first arrival': ["5", "5"],
                        'disable port': ["click", "Enabled"],
                        'page 7 ELRP': ["next_page", None],
                        'page8 pseSettings': ["next_page", None],
                        'page9 summary': ["next_page", None]
                        }

        template_mac_d360 = {'name': ["port_type_mac_d360", "port_type_mac_d360"],
                             'description': [None, None],
                             'status': [None, 'on'],
                             'page2 accessVlanPage': ['next_page', None],
                             'page3 transmissionSettings': ["next_page", None],
                             'page4 stp': ["next_page", None],
                             'page5 stormControlSettings': ["next_page", None],
                             'page6 MACLOCKINGSettingsPage': ["next_page", None],
                             'mac locking': [None, "On"],
                             'max first arrival': ["10", "10"],
                             'page 7 ELRP': ["next_page", None],
                             'page8 pseSettings': ["next_page", None],
                             'page9 summary': ["next_page", None]
                             }

        # randomize port template name:
        nr = random.randint(0, 1000)
        nr1 = random.randint(0, 1000)
        port_type_name = template_mac['name'][0] + "_" + str(nr)
        port_type_name_d360 = template_mac_d360['name'][0] + "_" + str(nr1)
        template_mac['name'][0] = port_type_name
        template_mac['name'][1] = port_type_name
        tgen_port = config_helper.createTgenPort(config_helper.tgen1_name, config_helper.tgen_dut1_port_a.ifname)
        assert tgen_port, "Tgen port not generated"
        template_mac_d360['name'][0] = port_type_name_d360
        template_mac_d360['name'][1] = port_type_name_d360
        D360Flag = 0
        is_configured = False

        try:

            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                pytest.fail("This test should run only on an EXOS standalone device")
            elif node.cli_type.upper() == "EXOS":

                assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                    node_policy_name, node_template_name, status="ON")

                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                            node_template_name,
                                                                                            node.cli_type)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                loaded_config['${TEST_NAME}'] = 'test_tcxm_19960 - Configure'
                res = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_mac,
                                                                                            isl_ports_dut[0],
                                                                                            d360=False)
                assert res == 1, f"Could not create the required port type"

                is_configured = True

                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

                assert xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(
                    node_policy_name,
                    node.mac) == 1

                xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac)
                xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_port_configuration()
                assert xiq_library_at_class_level.xflowsmanageDevice360.unlock_device360_port_config() == 1

                create_port = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_mac_d360,
                                                                                                    isl_ports_dut[0],
                                                                                                    d360=True)
                if create_port == 1:
                    logger.info("Port type was created")
                else:
                    pytest.fail("Could not create the required port type")

                xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration()
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

                is_configured = True

                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name, IRV=False)
                if res == -1:
                    logger.step("Update failed, trying to do a Delta Update")
                    xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node.serial)
                    xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)

                loaded_config['${TEST_NAME}'] = 'test_tcxm_19960 - Traffic'
                default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()
                default_library.apiUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                                                                                          config_helper.dut1_tgen_port_a.ifname)
                default_library.apiUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                                                                                          config_helper.dut1_tgen_port_a.ifname)
                default_library.apiUdks.trafficGenerationUdks.send_source_macs_on_port_from_traffic_generator(
                    mac_add_list, tgen_port)
                default_library.apiUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(config_helper.dut1_name, "10")
                default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()

                logger.step("Check in Monitor - > Overview page")
                network_manager.connect_to_network_element_name(node.name)
                enabled_mac_loc_on_ports_cli = cli.show_maclocking_on_the_ports_in_cli(node)
                network_manager.close_connection_to_network_element(node.name)
                found = False
                for i in enabled_mac_loc_on_ports_cli:
                    if i[0] == isl_ports_dut[0] and i[1] == 'ena':
                        logger.info(f"Port {isl_ports_dut[0]} is configured for MAC locking in CLI.")
                        found = True
                        break
                    else:
                        continue
                assert found, f"MAC locking was not enabled on CLI on port {isl_ports_dut[0]}"
                D360Flag = xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac)

                logger.info("******Checking Port Status******")
                check_status = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                    isl_ports_dut[0], column_name="PORT STATUS")
                max_wait = 10
                count = 0
                while check_status != port_status_to_be_checked and count < max_wait:
                    time.sleep(2)
                    count += 1
                    check_status = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                        isl_ports_dut[0], column_name="PORT STATUS")
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_status == port_status_to_be_checked:
                    logger.info("Port status is - Disabled by MAC Locking")
                else:
                    pytest.fail(f"Port status is - {check_status}")

                logger.info("******Checking Port State******")
                check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                    isl_ports_dut[0], column_name="MAC LOCKING")
                logger.step("Check in Monitor - > Overview page ->Mac Locking state")
                max_wait = 10
                count = 0
                while check_state != maclock_state_to_be_checked and count < max_wait:
                    time.sleep(2)
                    count += 1
                    check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                        isl_ports_dut[0], column_name="MAC LOCKING")
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_state == maclock_state_to_be_checked:
                    logger.info("Mac Locking state is - Enabled")
                else:
                    pytest.fail(f"Mac Locking state is {check_state}")
                D360Flag = -(xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window())

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_19960 - Cleanup'
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                time.sleep(2)
            elif node.cli_type.upper() == "EXOS":

                if D360Flag == 1:
                    xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
                if is_configured:
                    assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                        node_policy_name, node_template_name, status="OFF")
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                                node_template_name,
                                                                                                node.cli_type)
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.revert_port_configuration_template_level(
                        "Access Port")
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

                    res = xiq_library_at_class_level.xflowsmanageDevices.revert_device_to_template(node.serial)
                    assert res == 1, f"Failed to revert network policy to default"

                    xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(
                        template_mac["name"][0])
                    xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(
                        template_mac_d360["name"][0])

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_19961
    @pytest.mark.p1
    def test_tcxm_19961(self, node, logger, node_policy_name, node_template_name, cli, network_manager,
                        xiq_library_at_class_level, loaded_config, utils, config_helper, default_library):
        """
        Description   : Configure different "Maximum first arrival" values on a port type in Template configuration
        Step            Step Description
         1              Onboard one EXOS device
         2              Configure a policy-template with mac-locking on and click save
         3              Create a port type with mac-locking on
         4              Configure following Mac-locking properties:
                        "Maximum first arrival" as "300"
         5              Configure policy-template to device
         6              Configure max first arrival as 100
         7              Configure policy-template to device
         8              Configure following Mac-locking properties:
                        "Maximum first arrival" as "50"
         9              Configure policy-template to device
         10             Configure max first arrival as 10
         11             Configure policy-template to device

         6              Send 11 source MACs on port from traffic generator
         7              Check in Monitor - > Overview page
         8              Delete the onboarded device and logout from XIQ(Teardown)
        """

        loaded_config['${TEST_NAME}'] = 'test_tcxm_19961'
        isl_ports_dut = config_helper.create_ports_list(node.tgen)
        D360Flag = 0
        tgen_port = config_helper.createTgenPort(config_helper.tgen1_name, config_helper.tgen_dut1_port_a.ifname)
        assert tgen_port, "Tgen port not generated"
        mac_add_list = ['00:00:00:00:00:01', '00:00:00:00:00:02', '00:00:00:00:00:03', '00:00:00:00:00:04',
                        '00:00:00:00:00:05', '00:00:00:00:00:06', '00:00:00:00:00:07', '00:00:00:00:00:08',
                        '00:00:00:00:00:09', '00:00:00:00:01:01', '00:00:00:00:01:02']

        port_status_to_be_checked = "Disabled by MAC Locking"
        maclock_state_to_be_checked = "Enabled"

        template_mac = {'name': ["port_type_mac", "port_type_mac"],
                        'description': [None, None],
                        'status': [None, 'on'],
                        'page2 accessVlanPage': ['next_page', None],
                        'page3 transmissionSettings': ["next_page", None],
                        'page4 stp': ["next_page", None],
                        'page5 stormControlSettings': ["next_page", None],
                        'page6 MACLOCKINGSettingsPage': ["next_page", None],
                        'mac locking': ["click", "On"],
                        'disable port': ["click", "Enabled"],
                        'max first arrival': ["10", "10"],
                        'page 7 ELRP': ["next_page", None],
                        'page8 pseSettings': ["next_page", None],
                        'page9 summary': ["next_page", None]
                        }

        template_mac_new = {
            'MACLOCKINGSettingsPage': ['click', None],
            'max first arrival': ["200", "200"],
            'page9 summaryPage': ['next_page', None]
        }

        # randomize port template name:
        nr = random.randint(0, 1000)
        port_type_name = template_mac['name'][0] + "_" + str(nr)
        template_mac['name'][0] = port_type_name
        template_mac['name'][1] = port_type_name
        is_created = False
        is_added = False
        is_configured = False

        try:
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                pytest.fail("This test should run only on an EXOS standalone device")
            elif node.cli_type.upper() == "EXOS":
                logger.step("Configure Mac-locking properties")
                assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                    node_policy_name, node_template_name, status="ON")
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                            node_template_name,
                                                                                            node.cli_type)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                create_port = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_mac,
                                                                                                    isl_ports_dut[0],
                                                                                                    d360=False)
                if create_port:
                    logger.info("Port type was created")
                else:
                    pytest.fail("Could not create the required port type")
                is_configured = True

                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

                loaded_config['${TEST_NAME}'] = 'test_tcxm_19961 - Configure'

                assert xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(
                    node_policy_name, node.mac) == 1
                logger.step("Change 'max first arrival' to 100.")
                xiq_library_at_class_level.xflowscommonNavigator.navigate_configure_network_policies()
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                            node_template_name,
                                                                                            node.cli_type)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                template_mac_new['max first arrival'][0] = "100"
                template_mac_new['max first arrival'][1] = "100"
                res = xiq_library_at_class_level.xflowsmanageDevice360.edit_port_type(template_mac_new,
                                                                                      isl_ports_dut[0])
                if res == -1:
                    pytest.fail("summary verification failed in configuration of port attribute ")

                logger.step("Change 'max first arrival' to 10")
                template_mac_new['max first arrival'][0] = "10"
                template_mac_new['max first arrival'][1] = "10"
                res = xiq_library_at_class_level.xflowsmanageDevice360.edit_port_type(template_mac_new,
                                                                                      isl_ports_dut[0])
                if res == -1:
                    pytest.fail("summary verification failed in configuration of port attribute ")
                is_configured = True
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name, IRV=False)
                if res == -1:
                    logger.step("Update failed, trying to do a Delta Update")
                    xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node.serial)
                    xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)
                is_configured = True
                loaded_config['${TEST_NAME}'] = 'test_tcxm_19961 - Traffic'
                default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()
                default_library.apiUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                                                                                          config_helper.dut1_tgen_port_a.ifname)
                default_library.apiUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                                                                                          config_helper.dut1_tgen_port_a.ifname)
                default_library.apiUdks.trafficGenerationUdks.send_source_macs_on_port_from_traffic_generator(
                    mac_add_list, tgen_port)
                default_library.apiUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(config_helper.dut1_name, "10")
                default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()

                logger.step("Check in Monitor - > Overview page -> Port status")
                loaded_config['${TEST_NAME}'] = 'test_tcxm_19961 - Checking'
                network_manager.connect_to_network_element_name(node.name)
                enabled_mac_loc_on_ports_cli = cli.show_maclocking_on_the_ports_in_cli(node)
                network_manager.close_connection_to_network_element(node.name)
                found = False
                for i in enabled_mac_loc_on_ports_cli:
                    if i[0] == isl_ports_dut[0] and i[1] == 'ena':
                        logger.info(f"Port {isl_ports_dut[0]} is configured for MAC locking in CLI.")
                        found = True
                        break
                    else:
                        continue
                assert found, f"MAC locking was not enabled on CLI on port {isl_ports_dut[0]}"
                D360Flag = xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac)

                logger.info("******Checking Port Status******")

                check_status = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                    isl_ports_dut[0], column_name="PORT STATUS")
                max_wait = 10
                count = 0
                while check_status != port_status_to_be_checked and count < max_wait:
                    time.sleep(2)
                    count += 1
                    check_status = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                        isl_ports_dut[0], column_name="PORT STATUS")
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_status == port_status_to_be_checked:
                    logger.info("Port status is - Disabled by MAC Locking")
                else:
                    pytest.fail(f"Port status is - {check_status}")

                logger.info("******Checking Port State******")
                check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                    isl_ports_dut[0], column_name="MAC LOCKING")
                max_wait = 10
                count = 0
                while check_state != maclock_state_to_be_checked and count < max_wait:
                    time.sleep(2)
                    count += 1
                    check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                        isl_ports_dut[0], column_name="MAC LOCKING")
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_state == maclock_state_to_be_checked:
                    logger.info("Mac Locking state is - Enabled")
                else:
                    pytest.fail(f"Mac Locking state is {check_state}")
                D360Flag = -(xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window())

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_19961 - Cleanup'
            if is_configured:
                if D360Flag == 1:
                    xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

                assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                    node_policy_name, node_template_name, status="OFF")
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                            node_template_name,
                                                                                            node.cli_type)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.revert_port_configuration_template_level(
                    "Access Port")
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()

                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name, IRV=False)
                if res == -1:
                    logger.step("Update failed, trying to do a Delta Update")
                    xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node.serial)
                    xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)
                assert res == 1, f"Failed to update network policy to the device"

                xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(
                    template_mac["name"][0])

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_19963
    @pytest.mark.p1
    def test_tcxm_19963(self, node, logger, node_policy_name, node_template_name, cli, network_manager,
                        xiq_library_at_class_level, loaded_config, utils, config_helper, default_library):
        """
        Author        : icosmineanu
        Description   : Configure mac locking on a port type and verify in Client360
        Step                Step Description
         1              Onboard one EXOS device
         2              Configure a policy-template with mac-locking on and click save
         3              Create a port type with mac-locking on
         4              Configure following Mac-locking properties:
                        "Maximum first arrival" as "10"
                        "Disable port" as "off"
                        "Link down action" as "Clear first arrival MACs when port link goes down"
                        "Remove aged MACs" as "on"
         5              Configure policy-template to device and push config
         6              Send 11 source MACs on port from traffic generator
         7              Check in Monitor - > Overview page
         8              Delete the onboarded device and logout from XIQ(Teardown)
        """

        loaded_config['${TEST_NAME}'] = 'test_tcxm_19963'
        isl_ports_dut = config_helper.create_ports_list(node.tgen)
        D360Flag = 0
        mac_add_list = ['00:00:00:00:00:01', '00:00:00:00:00:02', '00:00:00:00:00:03', '00:00:00:00:00:04',
                        '00:00:00:00:00:05', '00:00:00:00:00:06', '00:00:00:00:00:07', '00:00:00:00:00:08',
                        '00:00:00:00:00:09', '00:00:00:00:01:01', '00:00:00:00:01:02']

        maclock_state_to_be_checked = "Enabled"
        tgen_port = config_helper.createTgenPort(config_helper.tgen1_name, config_helper.tgen_dut1_port_a.ifname)
        assert tgen_port, "Tgen port not generated"
        template_mac = {'name': ["port_type_mac", "port_type_mac"],
                        'description': [None, None],
                        'status': [None, 'on'],
                        'page2 accessVlanPage': ['next_page', None],
                        'page3 transmissionSettings': ["next_page", None],
                        'page4 stp': ["next_page", None],
                        'page5 stormControlSettings': ["next_page", None],
                        'page6 MACLOCKINGSettingsPage': ["next_page", None],
                        'mac locking': ["click", "On"],
                        'max first arrival': ["10", "10"],
                        'link down clear': ["click", "Clear"],
                        'remove aged MACs': ["click", "Enabled"],
                        'page 7 ELRP': ["next_page", None],
                        'page8 pseSettings': ["next_page", None],
                        'page9 summary': ["next_page", None]
                        }

        # randomize port template name:
        nr = random.randint(0, 1000)
        port_type_name = template_mac['name'][0] + "_" + str(nr)
        template_mac['name'][0] = port_type_name
        template_mac['name'][1] = port_type_name
        is_configured = False

        try:
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                pytest.skip("This test should run on an EXOS device")
            elif node.cli_type.upper() == "EXOS":
                assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                    node_policy_name, node_template_name, status="ON")
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                            node_template_name,
                                                                                            node.cli_type)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                create_port = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_mac,
                                                                                                    isl_ports_dut[0],
                                                                                                    d360=False)
                if create_port:
                    logger.info("Port type was created")
                else:
                    pytest.fail("Could not create the required port type")
                is_configured = True

                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

                assert xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(
                    node_policy_name, node.mac)

                res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name, IRV=False)
                if res == -1:
                    logger.step("Update failed, trying to do a Delta Update")
                    xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node.serial)
                    xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)
                assert res == 1, f"Failed to update network policy to the device"

                loaded_config['${TEST_NAME}'] = 'test_tcxm_19963- Traffic'
                default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()
                default_library.apiUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                                                                                          config_helper.dut1_tgen_port_a.ifname)
                default_library.apiUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                                                                                          config_helper.dut1_tgen_port_a.ifname)
                default_library.apiUdks.trafficGenerationUdks.send_source_macs_on_port_from_traffic_generator(
                    mac_add_list, tgen_port)
                default_library.apiUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(config_helper.dut1_name, "10")
                default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()

                logger.step("Check in Monitor - > Overview page -> Mac Locking state")
                logger.info("******Checking Port State******")
                network_manager.connect_to_network_element_name(node.name)
                enabled_mac_loc_on_ports_cli = cli.show_maclocking_on_the_ports_in_cli(node)
                network_manager.close_connection_to_network_element(node.name)
                found = False
                for i in enabled_mac_loc_on_ports_cli:
                    if i[0] == isl_ports_dut[0] and i[1] == 'ena':
                        logger.info(f"Port {isl_ports_dut[0]} is configured for MAC locking in CLI.")
                        found = True
                        break
                    else:
                        continue
                assert found, f"MAC locking was not enabled on CLI on port {isl_ports_dut[0]}"
                D360Flag = xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac)
                check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                    isl_ports_dut[0], column_name="MAC LOCKING")
                max_wait = 10
                count = 0
                while check_state != maclock_state_to_be_checked and count < max_wait:
                    time.sleep(2)
                    count += 1
                    check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                        isl_ports_dut[0], column_name="MAC LOCKING")
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_state == maclock_state_to_be_checked:
                    logger.info("Mac Locking state is - Enabled")
                else:
                    pytest.fail(f"Mac Locking state is {check_state}")
                D360Flag = -(xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window())

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_19963- Cleanup'
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                logger.info("This test should run on an EXOS device")
            elif node.cli_type.upper() == "EXOS":
                if is_configured:
                    if D360Flag == 1:
                        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

                    assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                        node_policy_name, node_template_name, status="OFF")
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                                node_template_name,
                                                                                                node.cli_type)
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.revert_port_configuration_template_level(
                        "Access Port")

                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                    res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name, IRV=False)
                    if res == -1:
                        logger.step("Update failed, trying to do a Delta Update")
                        xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node.serial)
                        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)
                    assert res == 1, f"Failed to update network policy to the device"

                    xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(
                        template_mac["name"][0])

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_19965
    @pytest.mark.p1
    def test_tcxm_19965(self, node, logger, node_policy_name, node_template_name, cli,
                        xiq_library_at_class_level, loaded_config, network_manager, utils, config_helper,
                        default_library):
        """
        Author        : icosmineanu
        Description   : Configure "link down action" as "retain macs" for a port type in Template configuration
        Step                Step Description
         1              Onboard one EXOS device
         2              Configure a policy-template with mac-locking on and click save
         3              Create a port type with mac-locking on
         4              Configure following Mac-locking properties:
                        "Maximum first arrival" as "10"
                        "Disable port" as "on"
                        "Link down action" as "Retain first arrival MACs when port link goes down"
                        "Remove aged MACs" as "off"
         5              Configure policy-template to device and push config
         6              Send 11 source MACs on port from traffic generator
         7              Check in Monitor - > Overview page
         8              Delete the onboarded device and logout from XIQ(Teardown)
        """

        loaded_config['${TEST_NAME}'] = 'test_tcxm_19965'
        isl_ports_dut = config_helper.create_ports_list(node.tgen)
        D360Flag = 0
        tgen_port = config_helper.createTgenPort(config_helper.tgen1_name, config_helper.tgen_dut1_port_a.ifname)
        assert tgen_port, "Tgen port not generated"
        mac_add_list = ['00:00:00:00:00:01', '00:00:00:00:00:02', '00:00:00:00:00:03', '00:00:00:00:00:04',
                        '00:00:00:00:00:05', '00:00:00:00:00:06', '00:00:00:00:00:07', '00:00:00:00:00:08',
                        '00:00:00:00:00:09', '00:00:00:00:01:01', '00:00:00:00:01:02']

        port_status_to_be_checked = "Disabled by MAC Locking"
        maclock_state_to_be_checked = "Enabled"

        template_mac = {'name': ["port_type_mac", "port_type_mac"],
                        'description': [None, None],
                        'status': [None, 'on'],
                        'page2 accessVlanPage': ['next_page', None],
                        'page3 transmissionSettings': ["next_page", None],
                        'page4 stp': ["next_page", None],
                        'page5 stormControlSettings': ["next_page", None],
                        'page6 MACLOCKINGSettingsPage': ["next_page", None],
                        'mac locking': ["click", "On"],
                        'max first arrival': ["10", "10"],
                        'disable port': ["click", "Enabled"],
                        'link down retain': ["click", "Retain"],
                        'remove aged MACs': ["click", "Enabled"],
                        'page 7 ELRP': ["next_page", None],
                        'page8 pseSettings': ["next_page", None],
                        'page9 summary': ["next_page", None]
                        }

        # randomize port template name:
        nr = random.randint(0, 1000)
        port_type_name = template_mac['name'][0] + "_" + str(nr)
        template_mac['name'][0] = port_type_name
        template_mac['name'][1] = port_type_name
        is_created = False
        is_added = False
        is_configured = False

        try:
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                pytest.skip("This test should run on an EXOS device")
            elif node.cli_type.upper() == "EXOS":
                assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                    node_policy_name, node_template_name, status="ON")
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                            node_template_name,
                                                                                            node.cli_type)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                create_port = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_mac,
                                                                                                    isl_ports_dut[0],
                                                                                                    d360=False)
                if create_port:
                    logger.info("Port type was created")
                else:
                    pytest.fail("Could not create the required port type")
                is_configured = True

                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

                assert xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(
                    node_policy_name, node.mac)

                res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name, IRV=False)
                if res == -1:
                    logger.step("Update failed, trying to do a Delta Update")
                    xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node.serial)
                    xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)
                assert res == 1, f"Failed to update network policy to the device"

                loaded_config['${TEST_NAME}'] = 'test_tcxm_19965 : Traffic'
                default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()
                default_library.apiUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                                                                                          config_helper.dut1_tgen_port_a.ifname)
                default_library.apiUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                                                                                          config_helper.dut1_tgen_port_a.ifname)
                default_library.apiUdks.trafficGenerationUdks.send_source_macs_on_port_from_traffic_generator(
                    mac_add_list, tgen_port)
                default_library.apiUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(config_helper.dut1_name, "10")
                default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()
                logger.step("Check in Monitor - > Overview page -> Port status")
                loaded_config['${TEST_NAME}'] = 'test_tcxm_19965 - Checking'

                logger.step("Check in Monitor - > Overview page")
                loaded_config['${TEST_NAME}'] = 'test_tcxm_19965 - Checking'
                network_manager.connect_to_network_element_name(node.name)
                enabled_mac_loc_on_ports_cli = cli.show_maclocking_on_the_ports_in_cli(node)
                network_manager.close_connection_to_network_element(node.name)
                found = False
                for i in enabled_mac_loc_on_ports_cli:
                    if i[0] == isl_ports_dut[0] and i[1] == 'ena':
                        logger.info(f"Port {isl_ports_dut[0]} is configured for MAC locking in CLI.")
                        found = True
                        break
                    else:
                        continue
                assert found, f"MAC locking was not enabled on CLI on port {isl_ports_dut[0]}"
                D360Flag = xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac)

                logger.info("******Checking Port Status******")

                check_status = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                    isl_ports_dut[0], column_name="PORT STATUS")
                max_wait = 10
                count = 0
                while check_status != port_status_to_be_checked and count < max_wait:
                    time.sleep(2)
                    count += 1
                    check_status = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                        isl_ports_dut[0], column_name="PORT STATUS")
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_status == port_status_to_be_checked:
                    logger.info("Port status is - Disabled by MAC Locking")
                else:
                    pytest.fail(f"Port status is - {check_status}")

                logger.info("******Checking Port State******")
                check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                    isl_ports_dut[0], column_name="MAC LOCKING")
                logger.step("Check in Monitor - > Overview page ->Mac Locking state")
                max_wait = 10
                count = 0
                while check_state != maclock_state_to_be_checked and count < max_wait:
                    time.sleep(2)
                    count += 1
                    check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                        isl_ports_dut[0], column_name="MAC LOCKING")
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_state == maclock_state_to_be_checked:
                    logger.info("Mac Locking state is - Enabled")
                else:
                    pytest.fail(f"Mac Locking state is {check_state}")
                D360Flag = -(xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window())
        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_19965- Cleanup'
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                logger.info("This test should run on an EXOS device")
            elif node.cli_type.upper() == "EXOS":
                if is_configured:
                    if D360Flag == 1:
                        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

                    assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                        node_policy_name, node_template_name, status="OFF")
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                                node_template_name,
                                                                                                node.cli_type)
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.revert_port_configuration_template_level(
                        "Access Port")

                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                    res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name, IRV=False)
                    if res == -1:
                        logger.step("Update failed, trying to do a Delta Update")
                        xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node.serial)
                        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)
                    assert res == 1, f"Failed to update network policy to the device"

                    xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(
                        template_mac["name"][0])

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_19972
    @pytest.mark.p1
    def test_tcxm_19972(self, node, logger, node_policy_name, node_template_name, cli, network_manager,
                        xiq_library_at_class_level, loaded_config, utils, config_helper, default_library):
        """
        Author        : icosmineanu
        Description   : Configure "on" and "off" for "Remove aged MACs" on a port type in Template configuration
        Step                Step Description
         1              Onboard one EXOS device
         2              Configure a policy-template with mac-locking on and click save
         3              Create a port type with mac-locking on
         4              Configure following Mac-locking properties:
                        "Maximum first arrival" as "10"
                        "Disable port" as "on"
                        "Link down action" as "Clear first arrival MACs when port link goes down"
                        "Remove aged MACs" as "on"
         5              Configure policy-template to device and push config
         6              Send 11 source MACs on port from traffic generator
         7              Check in Monitor - > Overview page
         8              Delete the onboarded device and logout from XIQ(Teardown)
        """

        loaded_config['${TEST_NAME}'] = 'test_tcxm_19972'
        isl_ports_dut = config_helper.create_ports_list(node.tgen)
        D360Flag = 0
        tgen_port = config_helper.createTgenPort(config_helper.tgen1_name, config_helper.tgen_dut1_port_a.ifname)
        assert tgen_port, "Tgen port not generated"
        mac_add_list = ['00:00:00:00:00:01', '00:00:00:00:00:02', '00:00:00:00:00:03', '00:00:00:00:00:04',
                        '00:00:00:00:00:05', '00:00:00:00:00:06', '00:00:00:00:00:07', '00:00:00:00:00:08',
                        '00:00:00:00:00:09', '00:00:00:00:01:01', '00:00:00:00:01:02']

        port_status_to_be_checked = "Disabled by MAC Locking"
        maclock_state_to_be_checked = "Enabled"

        template_mac = {'name': ["port_type_mac", "port_type_mac"],
                        'description': [None, None],
                        'status': [None, 'on'],
                        'page2 accessVlanPage': ['next_page', None],
                        'page3 transmissionSettings': ["next_page", None],
                        'page4 stp': ["next_page", None],
                        'page5 stormControlSettings': ["next_page", None],
                        'page6 MACLOCKINGSettingsPage': ["next_page", None],
                        'mac locking': ["click", "On"],
                        'max first arrival': ["10", "10"],
                        'disable port': ["click", "Enabled"],
                        'link down clear': ["click", "Clear"],
                        'remove aged MACs': ["click", "Enabled"],
                        'page 7 ELRP': ["next_page", None],
                        'page8 pseSettings': ["next_page", None],
                        'page9 summary': ["next_page", None]
                        }

        # randomize port template name:
        nr = random.randint(0, 1000)
        port_type_name = template_mac['name'][0] + "_" + str(nr)
        template_mac['name'][0] = port_type_name
        template_mac['name'][1] = port_type_name
        is_configured = False

        try:
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                pytest.skip("This test should run on an EXOS device")
            elif node.cli_type.upper() == "EXOS":

                assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                    node_policy_name, node_template_name, status="ON")
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                            node_template_name,
                                                                                            node.cli_type)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                create_port = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_mac,
                                                                                                    isl_ports_dut[0],
                                                                                                    d360=False)
                if create_port:
                    logger.info("Port type was created")
                else:
                    pytest.fail("Could not create the required port type")
                is_configured = True

                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

                assert xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(
                    node_policy_name, node.mac)

                res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name, IRV=False)
                if res == -1:
                    logger.step("Update failed, trying to do a Delta Update")
                    xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node.serial)
                    xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)
                assert res == 1, f"Failed to update network policy to the device"

                loaded_config['${TEST_NAME}'] = 'test_tcxm_19972 : Traffic'
                default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()
                default_library.apiUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                                                                                          config_helper.dut1_tgen_port_a.ifname)
                default_library.apiUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                                                                                          config_helper.dut1_tgen_port_a.ifname)
                default_library.apiUdks.trafficGenerationUdks.send_source_macs_on_port_from_traffic_generator(
                    mac_add_list, tgen_port)
                default_library.apiUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(config_helper.dut1_name, "10")
                default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()

                logger.step("Check in Monitor - > Overview page")
                loaded_config['${TEST_NAME}'] = 'test_tcxm_19972 - Checking'
                network_manager.connect_to_network_element_name(node.name)
                enabled_mac_loc_on_ports_cli = cli.show_maclocking_on_the_ports_in_cli(node)
                network_manager.close_connection_to_network_element(node.name)
                found = False
                for i in enabled_mac_loc_on_ports_cli:
                    if i[0] == isl_ports_dut[0] and i[1] == 'ena':
                        logger.info(f"Port {isl_ports_dut[0]} is configured for MAC locking in CLI.")
                        found = True
                        break
                    else:
                        continue
                assert found, f"MAC locking was not enabled on CLI on port {isl_ports_dut[0]}"
                D360Flag = xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac)

                logger.info("******Checking Port Status******")

                check_status = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                    isl_ports_dut[0], column_name="PORT STATUS")
                max_wait = 10
                count = 0
                while check_status != port_status_to_be_checked and count < max_wait:
                    time.sleep(2)
                    count += 1
                    check_status = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                        isl_ports_dut[0], column_name="PORT STATUS")
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_status == port_status_to_be_checked:
                    logger.info("Port status is - Disabled by MAC Locking")
                else:
                    pytest.fail(f"Port status is - {check_status}")

                logger.info("******Checking Port State******")
                check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                    isl_ports_dut[0], column_name="MAC LOCKING")
                logger.step("Check in Monitor - > Overview page ->Mac Locking state")
                max_wait = 10
                count = 0
                while check_state != maclock_state_to_be_checked and count < max_wait:
                    time.sleep(2)
                    count += 1
                    check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                        isl_ports_dut[0], column_name="MAC LOCKING")
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_state == maclock_state_to_be_checked:
                    logger.info("Mac Locking state is - Enabled")
                else:
                    pytest.fail(f"Mac Locking state is {check_state}")
                D360Flag = -(xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window())

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_19972- Cleanup'
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                logger.info("Test case works only in EXOS")
            elif node.cli_type.upper() == "EXOS":
                if is_configured:
                    if D360Flag == 1:
                        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

                    assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                        node_policy_name, node_template_name, status="OFF")
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                                node_template_name,
                                                                                                node.cli_type)
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.revert_port_configuration_template_level(
                        "Access Port")

                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                    res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name, IRV=False)
                    if res == -1:
                        logger.step("Update failed, trying to do a Delta Update")
                        xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node.serial)
                        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)
                    assert res == 1, f"Failed to update network policy to the device"

                    xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(
                        template_mac["name"][0])

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_19978
    @pytest.mark.p1
    def test_tcxm_19978(self, node, logger, node_policy_name, node_template_name, cli, network_manager,
                        xiq_library_at_class_level, loaded_config, enter_switch_cli, utils, config_helper):
        """
        Author        : icosmineanu
        Description   : Disable mac-locking on a port in Device level config, enable mac locking on the same port in CLI,
                        Check in Monitor->Overview page after 10 mins
        Step                Step Description
         1              Onboard one EXOS device
         2              Disable mac-locking on a port in Device level config
         3              Enable mac locking on the same port in CLI
         4              Check in Monitor->Overview page
         5              Delete the onboarded device and logout from XIQ(Teardown)
        """

        loaded_config['${TEST_NAME}'] = 'test_tcxm_19978'
        isl_ports_dut = config_helper.create_ports_list(node.tgen)
        D360Flag = 0
        tgen_port = config_helper.createTgenPort(config_helper.tgen1_name, config_helper.tgen_dut1_port_a.ifname)
        assert tgen_port, "Tgen port not generated"
        maclock_state_to_be_checked = "Enabled"

        template_mac = {'name': ["port_type_mac", "port_type_mac"],
                        'description': [None, None],
                        'status': [None, 'on'],
                        'page2 accessVlanPage': ['next_page', None],
                        'page3 transmissionSettings': ["next_page", None],
                        'page4 stp': ["next_page", None],
                        'page5 stormControlSettings': ["next_page", None],
                        'page6 MACLOCKINGSettingsPage': ["next_page", None],
                        'mac locking': ["click", "On"],
                        'page 7 ELRP': ["next_page", None],
                        'page8 pseSettings': ["next_page", None],
                        'page9 summary': ["next_page", None]
                        }

        # randomize port template name:
        nr = random.randint(0, 100)
        port_type_name = template_mac['name'][0] + "_" + str(nr)
        template_mac['name'][0] = port_type_name
        template_mac['name'][1] = port_type_name
        is_configured = False

        try:
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                pytest.skip("This test should run on an EXOS device")
            elif node.cli_type.upper() == "EXOS":
                assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                    node_policy_name, node_template_name, status="ON")
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                            node_template_name,
                                                                                            node.cli_type)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                create_port = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_mac,
                                                                                                    isl_ports_dut[0],
                                                                                                    d360=False)
                if create_port:
                    logger.info("Port type was created")
                else:
                    pytest.fail("Could not create the required port type")
                is_configured = True

                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

                assert xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(
                    node_policy_name, node.mac)

                res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name, IRV=False)
                if res == -1:
                    logger.step("Update failed, trying to do a Delta Update")
                    xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node.serial)
                    xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)
                assert res == 1, f"Failed to update network policy to the device"

                logger.step("Disable mac-locking on a port in Device level config")
                D360Flag = xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac)
                xiq_library_at_class_level.xflowsmanageDevice360.configure_mac_locking_from_port_config(
                    isl_ports_dut[0],
                    mac_lock="OFF")
                xiq_library_at_class_level.xflowsmanageDevice360.d360_save_port_configuration()
                D360Flag = -(xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window())
                res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name, IRV=False)
                if res == -1:
                    logger.step("Update failed, trying to do a Delta Update")
                    xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node.serial)
                    xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node.mac)
                assert res == 1, f"Failed to update network policy to the device"

                logger.step("Enable mac locking on the same port in CLI")
                with enter_switch_cli(node) as dev_cmd:
                    dev_cmd.send_cmd(node.name, 'enable mac-locking', max_wait=10, interval=2)
                    dev_cmd.send_cmd(node.name, f'enable mac-locking ports {isl_ports_dut[0]}',
                                     max_wait=10, interval=2)
                    dev_cmd.send_cmd(node.name, 'restart process iqagent', confirmation_phrases="(y or n)",
                                     confirmation_args="Yes")
                logger.step("Check in cli and in Monitor - > Overview page ->Mac Locking state")
                network_manager.connect_to_network_element_name(node.name)
                enabled_mac_loc_on_ports_cli = cli.show_maclocking_on_the_ports_in_cli(node)
                network_manager.close_connection_to_network_element(node.name)
                found = False
                for i in enabled_mac_loc_on_ports_cli:
                    if i[0] == isl_ports_dut[0] and i[1] == 'ena':
                        logger.info(f"Port {isl_ports_dut[0]} is configured for MAC locking in CLI.")
                        found = True
                        break
                    else:
                        continue
                assert found, f"MAC locking was not enabled on CLI on port {isl_ports_dut[0]}"

                logger.info("******Checking Port State******")
                xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node.serial)
                D360Flag = xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac)
                check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                    isl_ports_dut[0], column_name="MAC LOCKING")
                max_wait = 10
                count = 0
                while check_state != maclock_state_to_be_checked and count < max_wait:
                    time.sleep(2)
                    count += 1
                    check_state = xiq_library_at_class_level.xflowsmanageDevice360.check_overview_row_table_by_port(
                        isl_ports_dut[0], column_name="MAC LOCKING")
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
                if check_state == maclock_state_to_be_checked:
                    logger.info("Mac Locking state is - Enabled")
                else:
                    pytest.fail(f"Mac Locking state is {check_state}")

                D360Flag = -(xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window())

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_19978- Cleanup'
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                logger.info("This test should run on an EXOS device")
            elif node.cli_type.upper() == "EXOS":
                if is_configured:
                    if is_configured:
                        if D360Flag == 1:
                            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

                        assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                            node_policy_name, node_template_name, status="OFF")
                        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                                    node_template_name,
                                                                                                    node.cli_type)
                        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.revert_port_configuration_template_level(
                            "Access Port")

                        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                        res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        serial=node.serial, policy_name=node_policy_name, IRV=False)
                        if res == -1:
                            logger.step("Update failed, trying to do a Delta Update")
                            xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(
                                node.serial)
                            xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(
                                node.mac)
                        assert res == 1, f"Failed to update network policy to the device"

                        # Delete the port type created
                        xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(
                            template_mac["name"][0])

    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_19983
    @pytest.mark.p1
    def test_tcxm_19983(self, node, logger, node_policy_name, node_template_name, xiq_library_at_class_level,
                        loaded_config, config_helper):
        """
        Author        : icosmineanu
        Description   : Configure invalid values for maximum first arrival
        Step                Step Description
         1              Onboard one EXOS device
         2              Navigate to Device360, Monitor, Overview
         3              Configure Maximum first arrival as 601
         4              Delete the onboarded device and logout from XIQ(Teardown)
        """

        loaded_config['${TEST_NAME}'] = 'test_tcxm_19983'
        isl_ports_dut = config_helper.create_ports_list(node.tgen)
        expected_limit_exceed_msg = "Must be an integer that is between 0 and 600"
        D360Flag = 0
        try:
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                pytest.skip("This test should run on an EXOS device")
            elif node.cli_type.upper() == "EXOS":
                assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                    node_policy_name, node_template_name, status="ON")
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                assert xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(
                    node_policy_name, node.mac)
                D360Flag = xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac)
                error_msg = xiq_library_at_class_level.xflowsmanageDevice360.configure_mac_locking_from_port_config(
                    isl_ports_dut[0], max_first_limit="601")
                assert expected_limit_exceed_msg == error_msg, "No error message was shown when exceeding 600 MAC limit!"
                D360Flag = -(xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window())

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_19983 - CLEANUP'
            if node.cli_type.upper() == "VOSS" or node.platform.upper() == "STACK":
                logger.info("This test should run on an EXOS device")
            elif node.cli_type.upper() == "EXOS":
                if D360Flag == 1:
                    xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
                assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.global_mac_locking_status_change(
                    node_policy_name, node_template_name, status="OFF")
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
