import pytest


@pytest.mark.p1
@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.testbed_1_node
@pytest.mark.development
class Xiq9301neNodeTests:
    """
    Contains all testcases for story XIQ-9301 that require only one node to run. The description for each test is under the test definition.
    Testcases covered by the script:
        TCXM-25646 - covered by tcxm_25646
        TCXM-25654 - covered by tcxm_25654
        TCXM-25649 - covered by tcxm_25649
        TCXM-25656 - covered by tcxm_25656
        TCXM-25650 - covered by tcxm_25656, tcxm_25677_1, tcxm_25677_2 and tcxm_25677_3.
        TCXM-25673 - covered by test_tcxm_25646
        TCXM-25676 - covered by test_tcxm_25649
        TCXM-25680 - covered by test_tcxm_25649
        TCXM-25682 - covered by test test_tcxm_25656 and also by tests tcxm_25677_1, tcxm_25677_2 and tcxm_25677_3
        TCXM-25683 - covered in test tcxm_25677_1, tcxm_25677_2 and tcxm_25677_3, one test for each button under Actions .
        Couldn't implement the test for the Enable Port for ELRP disabled ports because of automation framework limitation,
        specific traffic is required to simulate ELRP.
    """

    @pytest.mark.p1
    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.testbed_1_node
    @pytest.mark.development
    @pytest.mark.tcxm_25646
    def test_tcxm_25646(self, logger, node_1, cli, xiq_library_at_class_level, test_data, test_bed):
        """
        Test verifies the Port Details button is present.

         Step       Step Description
         1          Onboard the device
         2          Navigate to Device360, Monitor, Diagnostics
         3          Verify Port Details button is present
         """
        try:
            logger.info("Step 2: Navigate to Device360, Monitor, Diagnostics")
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()

            logger.info("Step 3: Verify Port Details button is present")
            port_details_button = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_port_details_button()
            assert port_details_button, "Did not find the Port Details button"

            xiq_library_at_class_level.xflowsmanageDevice360.select_monitor_diagnostics_port_details()

        finally:
            logger.info("Cleanup: Closing Device360 Window")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

    @pytest.mark.p1
    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.testbed_1_node
    @pytest.mark.development
    @pytest.mark.tcxm_25654
    def test_tcxm_25654(self, logger, node_1, cli, xiq_library_at_class_level, test_data, test_bed, utils):
        """
        Verifies ports can be selected and deselected using Select All and Deselect All buttons.

        Step        Step Description
        1           Verify Port Details table contains all ports
        2           Deselect all ports
        3           Verify Port Details table is empty
        4           Select all ports using the "Select all ports" button
        5           Verify all ports present in the table
        """

        try:
            logger.info("Step 1: Verify Port Details table contains all ports")
            utils.wait_till(delay=5)
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
            xiq_library_at_class_level.xflowsmanageDevice360.select_monitor_diagnostics_port_details()
            port_details_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_monitor_diagnostics_port_details_table()
            assert port_details_table, "Did not find port details table"

            # Get Port Details table rows , one row per each switch port
            xiq_library_at_class_level.xflowscommonAutoActions.scroll_by_horizontal(port_details_table)
            utils.wait_till(delay=10)
            port_details_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
            assert port_details_rows, "Did not find port details table"
            logger.info(f"Number of rows: {len(port_details_rows)}")

            logger.info("Step 2: Deselect all ports and verify table is empty")
            number_of_ports = len(port_details_rows)
            xiq_library_at_class_level.xflowsmanageDevice360.click_device360_diagnostics_deselect_all_button(1)
            utils.wait_till(delay=5)

            logger.info("Step 3: Verify Port Details table is empty")
            empty_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
            assert empty_table is None, "Table is not empty"

            logger.info('Step 4: Select all ports with "Select all" button')
            xiq_library_at_class_level.xflowsmanageDevice360.click_device360_diagnostics_select_all_button(1)

            logger.info('Step 5: Verify all ports present in the table')
            xiq_library_at_class_level.xflowsmanageDevice360.select_diagnostics_port_details_table()
            xiq_library_at_class_level.xflowscommonAutoActions.scroll_by_horizontal(port_details_table)
            utils.wait_till(delay=10)
            port_details_rows_2 = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
            assert port_details_rows_2, "Did not find port details table"
            logger.info(f"Number of rows after Select All: {len(port_details_rows_2)}")

            assert number_of_ports == len(port_details_rows_2), "Not all ports selected"

        finally:
            logger.info("Cleanup: Closing Device360 Window")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

    @pytest.mark.p1
    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.testbed_1_node
    @pytest.mark.development
    @pytest.mark.tcxm_25649
    def test_tcxm_25649(self, logger, node_1, cli, xiq_library_at_class_level, test_data, test_bed, utils):
        """
        Verifies ports can be selected and deselected by clicking on the port icons in the switch wireframe

        Step        Step Description
        1           Deselect all ports
        2           Verify Port Details table is empty
        3           Select ports from the switch wireframe
        4           Verify selected ports appear in the Ports Details table
        5           Deselect ports selected at step 3 - also from the wireframe
        6           Verify Ports Details table is empty
        """

        try:
            logger.info("Opening Device360 window and navigating to Monitor -> Diagnostics page")
            utils.wait_till(delay=5)
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
            xiq_library_at_class_level.xflowsmanageDevice360.select_monitor_diagnostics_port_details()
            port_details_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_monitor_diagnostics_port_details_table()
            xiq_library_at_class_level.xflowscommonAutoActions.scroll_by_horizontal(port_details_table)
            utils.wait_till(delay=10)
            port_details_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
            no_of_ports = len(port_details_rows)

            logger.info("Step 1 : Deselect ports")
            xiq_library_at_class_level.xflowsmanageDevice360.click_device360_diagnostics_deselect_all_button(1)
            utils.wait_till(delay=5)

            logger.info("Step 2: Verify Port Details table is empty")
            empty_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
            assert empty_table is None, "Table is not empty"

            logger.info("Step 3: Select ports from the switch wireframe")
            for i in range(1, no_of_ports + 5):
                port_icon_present = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_ah_icon(
                    i)
                if port_icon_present:
                    xiq_library_at_class_level.xflowsmanageDevice360.device360_diagnostics_click_on_port_icon(i)

            logger.info("Step 4: Verify selected ports appear in the Port Details table")
            utils.wait_till(delay=3)
            xiq_library_at_class_level.xflowsmanageDevice360.select_diagnostics_port_details_table()
            xiq_library_at_class_level.xflowscommonAutoActions.scroll_by_horizontal(port_details_table)
            utils.wait_till(delay=10)
            port_details_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
            assert port_details_rows, "Did not find port details table"
            logger.info(f"Number of rows after select from wireframe: {len(port_details_rows)}")

            assert no_of_ports == len(
                port_details_rows), "Not all selected ports are present in the Ports Details table"

            logger.info("Step 5: Deselect selected ports - also from the wireframe")
            for i in range(1, no_of_ports + 5):
                port_icon_present = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_ah_icon(
                    i)
                if port_icon_present:
                    xiq_library_at_class_level.xflowsmanageDevice360.device360_diagnostics_click_on_port_icon(i)

            logger.info("Step 6: Verify Port Details table is empty")
            utils.wait_till(delay=2)
            empty_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
            assert empty_table is None, "Table is not empty"

        finally:
            logger.info("Cleanup: Closing Device360 Window")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

    @pytest.mark.p1
    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.testbed_1_node
    @pytest.mark.development
    @pytest.mark.tcxm_25656
    def test_tcxm_25656(self, logger, node_1, cli, xiq_library_at_class_level, test_data, test_bed, utils):
        """
        Verifies Actions button is present only when ports are selected in the Port Details table.

		Step        Step Description
		1           Go to Port Details table under Monitor -> Diagnostics
		2           Select ports in the Port Details table
		3           Verify Actions button is present
		4           Deselect ports
		5           Verify Actions button no longer available
		"""

        try:
            logger.info("Step 1: Opening Device360 window and navigating to Monitor -> Diagnostics page")
            utils.wait_till(delay=5)
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
            xiq_library_at_class_level.xflowsmanageDevice360.select_monitor_diagnostics_port_details()
            port_details_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_monitor_diagnostics_port_details_table()

            logger.info("Step 2: Select ports in the Port Details table")
            xiq_library_at_class_level.xflowscommonAutoActions.scroll_by_horizontal(port_details_table)
            utils.wait_till(delay=10)
            port_details_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
            nr_of_ports = len(port_details_rows)
            logger.info(f"Number of rows is {len(port_details_rows)}")

            logger.info(
                "Step 3: Select all ports from the checkbox in the table header and verify Actions button exist")
            selected = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_table_select_checkbox(
                1)
            if selected.is_selected() is False:
                xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(1)

            for i in range(2, nr_of_ports + 1):
                selected = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_table_select_checkbox(
                    i)
                port_name = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_port_name(
                    i - 1)
                assert selected.is_selected(), f"Checkbox for port {port_name} was not selected."

            # Step 3: Verify Actions button is present
            actions_btn = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_actions_button()
            assert actions_btn, "Can't find actions button."

            logger.info("Step 4: Deselect ports")
            xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(1)
            for i in range(2, nr_of_ports + 1):
                selected = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_table_select_checkbox(
                    i)
                port_name = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_port_name(
                    i - 1)
                assert selected.is_selected() is False, f"Checkbox for port {port_name} is still selected."

            logger.info("Step 5: Verify Actions button no longer available")
            utils.wait_till(delay=3)
            actions_btn_disabled = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_actions_button_disabled()
            assert actions_btn_disabled, "Actions button is still available, should be grayed out."

        finally:
            logger.info("Cleanup: Closing Device360 Window")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

    @pytest.mark.p1
    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.testbed_1_node
    @pytest.mark.development
    @pytest.mark.tcxm_25677_1
    def test_tcxm_25677_1(self, logger, node_1, cli, xiq_library_at_class_level, test_data, test_bed, utils):
        """
        Verifies ports can be bounced using the Bounce Port button under Actions

		Step        Step Description
		1           Go to Port Details table under Monitor -> Diagnostics
		2           Select multiple ports from the table
		3           Click Actions button and verify Bounce port button is present
		4           Click on the Bounce port button and verify action was successful
		5           Verify error message when action tried on Disconnected ports
		"""
        tested_ports = []
        connected_ports = []
        port_names = []
        port_nr = 1
        verify_button = True
        verify_error = True
        connected_port_status = "Connected"
        disconnected_port_status = "Disconnected"
        mgmt_port_name = "mgmt"

        try:
            logger.info("Step 1: Opening Device360 window and navigating to Monitor -> Diagnostics page")
            utils.wait_till(delay=5)
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
            xiq_library_at_class_level.xflowsmanageDevice360.select_monitor_diagnostics_port_details()
            port_details_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_monitor_diagnostics_port_details_table()

            logger.info("Step 2: Select multiple ports from the table")
            xiq_library_at_class_level.xflowscommonAutoActions.scroll_by_horizontal(port_details_table)
            utils.wait_till(delay=10)
            port_details_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
            logger.info(f"Number of rows is {len(port_details_rows)}")

            for row in port_details_rows:
                port_nr += 1
                tested_ports.append(port_nr)
                port_name = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_port_name(
                    port_nr - 1).text
                port_status = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_port_status(
                    port_nr - 1).text
                selected = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_table_select_checkbox(
                    port_nr)
                if selected.is_selected() is True:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                        port_nr)
                if port_status == connected_port_status and port_name != mgmt_port_name:
                    xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                        port_nr)
                    connected_ports.append(port_nr)
                    port_names.append(port_name)
                    logger.info(f"Added port {port_name} to connected ports")
                if len(tested_ports) == 7:
                    logger.info(f"Tested ports are : {tested_ports} ")
                    if len(connected_ports) != 0:
                        logger.info(f"Connected ports in tested_ports are : {port_names} on rows {connected_ports}")
                        xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_actions_button()

                        logger.info("Step 3: Click Actions button and verify Bounce port button is present")
                        if verify_button:
                            port_button = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_actions_bounce_port_button()
                            assert port_button, "Can't find Bounce Port button."
                            verify_button = False

                        logger.info("Step 4: Click on the Bounce port button and verify action was successful")
                        xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_bounce_port_button()
                        message = xiq_library_at_class_level.xflowsmanageDevice360.wait_for_device360_diagnostics_actions_message()
                        assert message, "Message was not generated"
                        all_ports_used = ", ".join(port_names)
                        logger.info(f"Ports expected to be found in successful message: {all_ports_used}")
                        logger.info(f'Message is: {message.get_attribute("innerHTML")}')
                        assert f"Bounce Port {all_ports_used} successful" in message.get_attribute("innerHTML")
                        for port, port_name in zip(connected_ports, port_names):
                            logger.info(f"Deselecting port {port_name} on row {port}.")
                            xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                                port)
                    tested_ports = []
                    connected_ports = []
                    port_names = []

            logger.info("Step 5: Verify error message when action tried on Disconnected ports")
            port_nr = 1
            for row in port_details_rows:
                port_nr += 1
                if disconnected_port_status in row.text and verify_error:
                    selected = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_table_select_checkbox(
                        port_nr)
                    if selected.is_selected() is False:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                            port_nr)
                        xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_actions_button()
                        xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_bounce_port_button()
                        utils.wait_till(delay=2)
                        message = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_bounce_port_error_message()
                        assert message, "Message was not generated"
                        verify_error = False
                        break

        finally:
            logger.info("Cleanup: Closing Device360 Window")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

    @pytest.mark.p1
    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.testbed_1_node
    @pytest.mark.development
    @pytest.mark.tcxm_25677_2
    def test_tcxm_25677_2(self, logger, node_1, cli, xiq_library_at_class_level, test_data, test_bed, utils, dev_cmd,
                          default_library, network_manager):
        """
        Verifies PoE on a bundle of ports can be bounced by using the Bounce PoE button under Actions

		Step        Step Description
		1           Go to Port Details table under Monitor -> Diagnostics
		2           Select multiple ports from the table
		3           Click Actions button and verify Bounce Poe button is present
		4           Click on the Bounce Poe button and verify action was successful
		5           Verify no error message is displayed when action tried on Disconnected ports
		"""

        supports_poe = False
        tested_ports = []
        connected_ports = []
        port_names = []
        port_nr = 1
        connected_port_status = "Connected"
        disconnected_port_status = "Disconnected"
        mgmt_port_name = "mgmt"
        verify_button = True
        verify_error = True
        device360_opened = False

        try:
            logger.info("Verifying if device supports PoE!")
            try:
                network_manager.connect_to_network_element_name(node_1.name)
                ports_power_cli = []
                if node_1.cli_type.upper() == "EXOS":
                    try:
                        output = \
                        dev_cmd.send_cmd(node_1.name, "show inline-power configuration ports", max_wait=5, interval=2)[
                            0].return_text
                    except:
                        pytest.skip("The device '{}' does not supported the PoE feature!".format(node_1.name))

                    logger.info(f"The result of the command is {output}")
                    if "None of the specified ports are inline-power capable" in output:
                        pytest.skip("The device '{}' does not supported the PoE feature!".format(node_1.name))
                    else:
                        supports_poe = True

                elif node_1.cli_type.upper() == "VOSS":

                    dev_cmd.send_cmd(node_1.name, "enable", max_wait=5, interval=2)
                    dev_cmd.send_cmd(node_1.name, "configure terminal", max_wait=5, interval=2)
                    output = dev_cmd.send_cmd(node_1.name, "show poe-power-measurement",
                                              max_wait=5, interval=2, ignore_cli_feedback=True)[0].return_text
                    utils.wait_till(delay=1)
                    if "Device is not a POE device" in output:
                        logger.info(output)
                        pytest.skip("The device '{}' does not supported the PoE feature!".format(node_1.name))
                    else:
                        supports_poe = True
            finally:
                network_manager.close_connection_to_network_element(node_1.name)

            if supports_poe:
                logger.info("Step 1: Opening Device360 window and navigating to Monitor -> Diagnostics page")
                xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac)
                xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
                xiq_library_at_class_level.xflowsmanageDevice360.select_monitor_diagnostics_port_details()
                port_details_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_monitor_diagnostics_port_details_table()
                device360_opened = True
                xiq_library_at_class_level.xflowscommonAutoActions.scroll_by_horizontal(port_details_table)
                utils.wait_till(delay=10)
                port_details_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
                logger.info(f"Number of rows is {len(port_details_rows)}")

                logger.info("Step 2: Select multiple ports from the table")
                for row in port_details_rows:
                    port_nr += 1
                    tested_ports.append(port_nr)
                    port_name = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_port_name(
                        port_nr - 1).text
                    port_status = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_port_status(
                        port_nr - 1).text
                    selected = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_table_select_checkbox(
                        port_nr)
                    if selected.is_selected() is True:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                            port_nr)
                    if port_status == connected_port_status and port_name != mgmt_port_name:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                            port_nr)
                        connected_ports.append(port_nr)
                        port_names.append(port_name)
                        logger.info(f"Added port {port_name} to connected ports")
                    if len(tested_ports) == 7:
                        logger.info(f"Tested ports are : {tested_ports} ")

                        if len(connected_ports) != 0:
                            # Step 3: Click Actions button and verify Bounce PoE port button is present
                            logger.info(f"Connected ports in tested_ports are : {port_names} on rows {connected_ports}")
                            xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_actions_button()

                            logger.info("Step 3: Click Actions button and verify Bounce Poe button is present")
                            if verify_button:
                                port_button = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_actions_bounce_poe_button()
                                assert port_button, "Can't find Bounce PoE button."
                                verify_button = False

                            logger.info("Step 4: Click on the Bounce port button and verify action was successful")
                            xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_bounce_poe_button()
                            message = xiq_library_at_class_level.xflowsmanageDevice360.wait_for_device360_diagnostics_actions_message()
                            assert message, "Success Message was not generated"
                            all_ports_used = ", ".join(port_names)
                            logger.info(f"Ports expected to be found in successful message: {all_ports_used}")
                            logger.info(f'Message is: {message.get_attribute("innerHTML")}')
                            assert f"Bounce PoE Port {all_ports_used} successful" in message.get_attribute("innerHTML")
                            for port, port_name in zip(connected_ports, port_names):
                                logger.info(f"Deselecting port {port_name} on row {port}")
                                xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                                    port)
                        tested_ports = []
                        connected_ports = []
                        port_names = []

                logger.info("Step 5: Verify no error message is displayed when action tried on Disconnected ports")
                port_nr = 1
                for row in port_details_rows:
                    port_nr += 1
                    if disconnected_port_status in row.text and verify_error:
                        selected = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_table_select_checkbox(
                            port_nr)
                        if selected.is_selected() is False:
                            xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                                port_nr)
                            xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_actions_button()
                            xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_bounce_poe_button()
                            utils.wait_till(delay=2)
                            message = xiq_library_at_class_level.xflowsmanageDevice360.wait_for_device360_diagnostics_actions_message()
                            logger.info(f'Message is: {message.get_attribute("innerHTML")}')
                            assert f"Bounce PoE Port {port_nr} successful" in message.get_attribute("innerHTML")
                            verify_error = False
                            break

        finally:
            if device360_opened:
                logger.info("Cleanup: Closing Device360 Window")
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

    @pytest.mark.p1
    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.testbed_1_node
    @pytest.mark.development
    @pytest.mark.tcxm_25677_3
    def test_tcxm_25677_3(self, logger, node_1, cli, xiq_library_at_class_level, test_data, test_bed, utils, udks,
                          dev_cmd, default_library, network_manager,
                          config_helper):
        """
        Verifies that a port blocked by Mac Locking can be enabled by using the Clear Mac Locking button under Actions

		Step        Step Description
		1           Go to Port Details table under Monitor -> Diagnostics
		2           Enable Mac Locking on the network device
		3           Send traffic so that port is disabled by Mac Locking
		4           Select the disabled port in the Port Details table
		5           Click Actions button and verify Clear Mac Locking button is present
		6           Click on the Clear Mac Locking button and verify action was successful
		"""

        device360_opened = False
        connected_port_status = "Connected"

        def send_source_macs_on_port_from_traffic_generator(mac_add_list):
            packet_a = 'packetA'
            tgen_port_a = config_helper.createTgenPort(config_helper.tgen1_name, config_helper.tgen_dut1_port_a.ifname)
            for i in range(0, len(mac_add_list)):
                udks.trafficGenerationUdks.Create_Ethernet2_Packet(packet_a, dmac=destmac, smac=mac_add_list[i],
                                                                   packet_len=105)
                udks.trafficGenerationUdks.send_stream_with_incrementing_smac(tgen_port_a,
                                                                              packet_a, stream_number=1, count=2,
                                                                              rate=100, unit='pps', sa_count=1,
                                                                              max_wait=120)

        mac_add_list = ['00:00:00:00:00:01', '00:00:00:00:00:02', '00:00:00:00:00:03']
        destmac = "00:00:00:00:00:0a"
        port_status_to_be_checked = "Disabled by MAC Locking"
        maclock_state_to_be_checked = "Enabled"

        logger.info("Test if device is EXOS; if Voss skip test")
        logger.info(f"CLI Type for this device is {node_1.cli_type.upper()}")
        if node_1.cli_type.upper() == "VOSS":
            pytest.skip("The device '{}' does not support the MAC Locking feature!".format(node_1.name))

        try:
            logger.info("Call jets setup")
            udks.setupTeardownUdks.Base_Test_Suite_Setup()
            try:
                udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(config_helper.dut1_name,
                                                                       config_helper.dut1_tgen_port_a.ifname)
                device360_opened = True
            except:
                pytest.skip("The device '{}' does not have a traffic generator connected!".format(node_1.name))

            logger.info("Step 2: Enable Mac Locking on the network device")
            network_manager.connect_to_network_element_name(node_1.name)
            dev_cmd.send_cmd(node_1.name, f"configure vlan Default add ports {node_1.tgen.port_a.ifname}", max_wait=5,
                             interval=2)
            dev_cmd.send_cmd(node_1.name, "enable mac-locking", max_wait=5, interval=2)
            dev_cmd.send_cmd(node_1.name, f"enable mac-locking ports {node_1.tgen.port_a.ifname}", max_wait=5,
                             interval=2)

            dev_cmd.send_cmd(node_1.name,
                             f"configure mac-locking ports {node_1.tgen.port_a.ifname} first-arrival limit-learning 1",
                             max_wait=5, interval=2)
            dev_cmd.send_cmd(node_1.name,
                             f"configure mac-locking ports {node_1.tgen.port_a.ifname} learn-limit-action disable-port",
                             max_wait=5, interval=2)
            utils.wait_till(delay=1)

            network_manager.close_connection_to_network_element(node_1.name)

            logger.info("Step 3: Send traffic so that port is disabled by Mac Locking")
            send_source_macs_on_port_from_traffic_generator(mac_add_list)

            utils.wait_till(delay=5)

            logger.info("Opening Device360 window and navigating to Monitor -> Diagnostics page")
            xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
            xiq_library_at_class_level.xflowsmanageDevice360.select_monitor_diagnostics_port_details()

            logger.info("Step 4: Select the disabled port in the Port Details table")
            tested_port = int(node_1.tgen.port_a.ifname)
            logger.info(f"Tested ports are : {tested_port}")

            logger.info("Step 5: Click Actions button and verify Clear Mac Locking button is present")
            selected = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_table_select_checkbox(
                tested_port + 1)
            if selected.is_selected() is False and "Disabled by MAC Locking" \
                    in xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_port_status(
                tested_port).text:
                xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                    tested_port + 1)
                xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_actions_button()
                clear_mac_locking_btn = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_actions_clear_mac_locking()
                assert clear_mac_locking_btn, "Clear MAC Locking button not found"

                logger.info("Step 6: Click on the Clear Mac Locking button and verify action was successful")
                xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_actions_clear_mac_locking()
                message = xiq_library_at_class_level.xflowsmanageDevice360.wait_for_device360_diagnostics_actions_message()
                assert message, "Message was not generated"
                assert f"Clear MAC lock for port {tested_port} successful" in message.get_attribute("innerHTML")
                utils.wait_till(delay=100)
                xiq_library_at_class_level.xflowsmanageDevice360.click_device360_diagnostics_actions_refresh_button()
                utils.wait_till(delay=10)
                new_port_status = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_port_status(
                    tested_port).text
                assert connected_port_status in new_port_status, "Port status is not correct."


        finally:
            if device360_opened:
                logger.info("Cleanup: Closing Device360 Window and reverting mac-locking settings")
                network_manager.connect_to_network_element_name(node_1.name)
                dev_cmd.send_cmd(node_1.name,
                                 f"configure mac-locking ports {node_1.tgen.port_a.ifname},{node_1.tgen.port_b.ifname} first-arrival limit-learning 600",
                                 max_wait=5, interval=2)
                dev_cmd.send_cmd(node_1.name,
                                 f"configure mac-locking ports {node_1.tgen.port_a.ifname},{node_1.tgen.port_b.ifname} learn-limit-action remain-enabled",
                                 max_wait=5, interval=2)
                dev_cmd.send_cmd(node_1.name,
                                 f"disable mac-locking ports {node_1.tgen.port_a.ifname}, {node_1.tgen.port_b.ifname}",
                                 max_wait=5, interval=2)
                dev_cmd.send_cmd(node_1.name, "disable mac-locking", max_wait=5, interval=2)
                dev_cmd.send_cmd(node_1.name, f"enable ports {node_1.tgen.port_a.ifname}", max_wait=5, interval=2)
                network_manager.close_connection_to_network_element(node_1.name)
                udks.setupTeardownUdks.Base_Test_Suite_Cleanup()
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

    @pytest.mark.p1
    @pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.testbed_stack
    @pytest.mark.development
    class Xiq9301StackTests:
        """
        Contains all stack testcases for story XIQ-9301. The description for each test is under the test definition.
        Testcases covered by the script:
            TCXM-25659 - covered by tcxm_25659
            TCXM-25668 - covered by tcxm_25668
            TCXM-25663 - covered by tcxm_25663
            TCXM-25670 - covered by tcxm_25670
            TCXM-25664 - covered by tcxm_25664_1 and tcxm_25664_2. Mac Locking not supported on stack and
                the ELRP test not implemented because of traffic generator limitation
        """

        @pytest.mark.dependson("tcxm_xiq_onboarding")
        @pytest.mark.testbed_stack
        @pytest.mark.development
        @pytest.mark.tcxm_25659
        @pytest.mark.p1
        def test_tcxm_25659(self, node_stack, logger, test_data, xiq_library_at_class_level, test_bed, config_helper):
            """
            Test verifies the Port Details button is present.

            Step	    Step Description
            1	        Onboard the device
            2	        Navigate to Device360, Monitor, Diagnostics
            3	        Verify Port Details button is present
            """

            try:
                logger.info("Step 2: Navigate to Device360, Monitor, Diagnostics")
                xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_stack.mac)
                xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()

                logger.info("Step 3: Verify Port Details button is present")
                port_details_button = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_port_details_button()
                assert port_details_button, "Did not find the Port Details button"

                xiq_library_at_class_level.xflowsmanageDevice360.select_monitor_diagnostics_port_details()

            finally:
                logger.info("Cleanup: Closing Device360 Window")
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

        @pytest.mark.p1
        @pytest.mark.dependson("tcxm_xiq_onboarding")
        @pytest.mark.testbed_stack
        @pytest.mark.development
        @pytest.mark.tcxm_25668
        def test_tcxm_25668(self, logger, node_stack, cli, test_data, test_bed, get_stack_slots,
                            xiq_library_at_class_level, utils, config_helper):
            """
            Verifies ports can be selected and deselected using Select All and Deselect All buttons.

            Step        Step Description
            1           Verify Port Details table contains all ports
            2           Deselect all ports
            3           Verify Port Details table is empty
            4           Select all ports using the "Select all ports" button
            5           Verify all ports present in the table
            """

            stack_nr = len(get_stack_slots(config_helper.dut1))

            try:
                logger.info("Opening Device360 window and navigating to Monitor -> Diagnostics page")
                xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_stack.mac)
                xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
                xiq_library_at_class_level.xflowsmanageDevice360.select_monitor_diagnostics_port_details()

                for i in range(1, stack_nr + 1):
                    logger.info("Step 1: Verify Port Details table contains all ports")
                    port_details_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_monitor_diagnostics_port_details_table()
                    assert port_details_table, "Did not find port details table"
                    xiq_library_at_class_level.xflowscommonAutoActions.scroll_by_horizontal(port_details_table)
                    utils.wait_till(delay=30)
                    port_details_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()

                    assert port_details_rows, "Did not find port details table"
                    logger.info(f"Number of rows: {len(port_details_rows)}")

                    logger.info("Step 2: Deselect all ports and verify table is empty")
                    number_of_ports = len(port_details_rows)
                    xiq_library_at_class_level.xflowsmanageDevice360.click_device360_diagnostics_deselect_all_button(i)
                    utils.wait_till(delay=5)

                    logger.info("Step 3: Verify Port Details table is empty")
                    empty_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
                    assert empty_table is None, "Table is not empty"

                    logger.info('Step 4: Select all ports with "Select all" button')
                    xiq_library_at_class_level.xflowsmanageDevice360.click_device360_diagnostics_select_all_button(i)
                    xiq_library_at_class_level.xflowsmanageDevice360.select_diagnostics_port_details_table()
                    xiq_library_at_class_level.xflowscommonAutoActions.scroll_by_horizontal(port_details_table)
                    utils.wait_till(delay=30)

                    logger.info('Step 5: Verify all ports present in the table')
                    port_details_rows_2 = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
                    assert port_details_rows_2, "Did not find port details table"
                    logger.info(f"Number of rows after Select All: {len(port_details_rows_2)}")
                    assert number_of_ports == len(port_details_rows_2), "Not all ports selected"

                    # Select Backup unit and repeat test
                    if i < stack_nr:
                        logger.info("Changing stack unit")
                        xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_stack_unit(i + 1)


            finally:
                logger.info("Cleanup: Closing Device360 Window")
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

        @pytest.mark.p1
        @pytest.mark.dependson("tcxm_xiq_onboarding")
        @pytest.mark.testbed_stack
        @pytest.mark.development
        @pytest.mark.tcxm_25663
        def test_tcxm_25663(self, logger, node_stack, cli, test_data, test_bed, get_stack_slots,
                            xiq_library_at_class_level, utils, config_helper):
            """
            Verifies ports can be selected and deselected by clicking on the port icons in the switch wireframe

    		Step        Step Description
    		1           Deselect all ports
    		2           Verify Port Details table is empty
    		3           Select ports from the switch wireframe
    		4           Verify selected ports appear in the Ports Details table
    		5           Deselect ports selected at step 3 - also from the wireframe
    		6           Verify Ports Details table is empty
    		"""

            stack_nr = len(get_stack_slots(config_helper.dut1))

            try:

                logger.info("Opening Device360 window and navigating to Monitor -> Diagnostics page")
                xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_stack.mac)
                xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
                xiq_library_at_class_level.xflowsmanageDevice360.select_monitor_diagnostics_port_details()

                port_details_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_monitor_diagnostics_port_details_table()
                xiq_library_at_class_level.xflowscommonAutoActions.scroll_by_horizontal(port_details_table)
                utils.wait_till(delay=20)
                port_details_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
                no_of_ports = len(port_details_rows)

                for i in range(1, stack_nr + 1):
                    logger.info("Step 1 : Deselect ports")
                    xiq_library_at_class_level.xflowsmanageDevice360.click_device360_diagnostics_deselect_all_button(i)

                    logger.info("Step 2: Verify Port Details table is empty")
                    for i in range(6):
                        empty_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
                        if empty_table is None:
                            break
                        else:
                            utils.wait_till(delay=10)
                    assert empty_table is None, "Table is not empty"

                    logger.info("Step 3: Select ports from the switch wireframe")
                    for i in range(1, no_of_ports + 5):
                        port_icon_present = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_ah_icon(
                            i)
                        if port_icon_present:
                            xiq_library_at_class_level.xflowsmanageDevice360.device360_diagnostics_click_on_port_icon(i)

                    logger.info("Step 4: Verify selected ports appear in the Port Details table")
                    xiq_library_at_class_level.xflowsmanageDevice360.select_diagnostics_port_details_table()
                    xiq_library_at_class_level.xflowscommonAutoActions.scroll_by_horizontal(port_details_table)
                    utils.wait_till(delay=30)
                    port_details_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
                    assert port_details_rows, "Did not find port details table"
                    logger.info(f"Number of rows after select from wireframe: {len(port_details_rows)}")

                    assert no_of_ports == len(
                        port_details_rows), "Not all selected ports are present in the Ports Details table"

                    logger.info("Step 5: Deselect selected ports - also from the wireframe")
                    for i in range(1, no_of_ports + 5):
                        port_icon_present = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_ah_icon(
                            i)
                        if port_icon_present:
                            xiq_library_at_class_level.xflowsmanageDevice360.device360_diagnostics_click_on_port_icon(i)

                    logger.info("Step 6: Verify Port Details table is empty")
                    utils.wait_till(delay=30)
                    empty_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
                    assert empty_table is None, "Table is not empty"

                    logger.info("Select Backup unit and repeat test")
                    if i < stack_nr:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_stack_unit(i + 1)

            finally:
                logger.info("Cleanup: Closing Device360 Window")
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

        @pytest.mark.p1
        @pytest.mark.dependson("tcxm_xiq_onboarding")
        @pytest.mark.testbed_stack
        @pytest.mark.development
        @pytest.mark.tcxm_25670
        def test_tcxm_25670(self, logger, node_stack, cli, xiq_library_at_class_level, test_data, get_stack_slots,
                            test_bed, utils, config_helper):
            """
            Verifies Actions button is present only when ports are selected in the Port Details table.

    		Step        Step Description
    		1           Go to Port Details table under Monitor -> Diagnostics
    		2           Select ports in the Port Details table
    		3           Verify Actions button is present
    		4           Deselect ports
    		5           Verify Actions button no longer available
    		"""
            stack_nr = len(get_stack_slots(config_helper.dut1))

            try:
                logger.info("Step 1: Opening Device360 window and navigating to Monitor -> Diagnostics page")
                xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_stack.mac)
                xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
                xiq_library_at_class_level.xflowsmanageDevice360.select_monitor_diagnostics_port_details()

                # Step 2: Select ports in the Port Details table
                for i in range(1, stack_nr + 1):
                    logger.info("Step 2: Select ports in the Port Details table")
                    port_details_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_monitor_diagnostics_port_details_table()
                    xiq_library_at_class_level.xflowscommonAutoActions.scroll_by_horizontal(port_details_table)
                    utils.wait_till(delay=20)
                    port_details_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
                    nr_of_ports = len(port_details_rows)

                    logger.info(
                        "Step 3: Select all ports from the checkbox in the table header and verify Actions button exist")
                    selected = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_table_select_checkbox(
                        1)
                    if selected.is_selected() is False:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                            1)

                    for j in range(2, nr_of_ports + 1):
                        selected = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_table_select_checkbox(
                            j)
                        port_name = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_port_name(
                            j - 1).text
                        assert selected.is_selected(), f"Checkbox for port {port_name} was not selected."

                    # Step 3: Verify Actions button is present
                    actions_btn = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_actions_button()
                    assert actions_btn, "Can't find actions button."

                    logger.info("Step 4: Deselect ports")
                    xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(1)
                    for j in range(2, nr_of_ports + 1):
                        selected = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_table_select_checkbox(
                            j)
                        port_name = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_port_name(
                            j - 1).text
                        assert selected.is_selected() is False, f"Checkbox for port {port_name} is still selected."

                    logger.info("Step 5: Verify Actions button no longer available")
                    utils.wait_till(delay=10)
                    actions_btn_disabled = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_actions_button_disabled()
                    assert actions_btn_disabled, "Actions button is still available, should be grayed out."

                    logger.info("Select Backup unit and repeat test")
                    if i < stack_nr:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_stack_unit(i + 1)
            finally:
                logger.info("Cleanup: Closing Device360 Window")
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

        @pytest.mark.p1
        @pytest.mark.dependson("tcxm_xiq_onboarding")
        @pytest.mark.testbed_stack
        @pytest.mark.development
        @pytest.mark.tcxm_25664_1
        def test_tcxm_25664_1(self, logger, node_stack, cli, xiq_library_at_class_level, test_data, get_stack_slots,
                              test_bed, utils, config_helper):
            """
            Verifies PoE on a bundle of ports can be bounced by using the Bounce PoE button under Actions

            Step        Step Description
            1           Go to Port Details table under Monitor -> Diagnostics
            2           Select multiple ports from the table
            3           Click Actions button and verify Bounce port button is present
            4           Click on the Bounce port button and verify action was successful
            """
            stack_nr = len(get_stack_slots(config_helper.dut1))
            connected_port_status = "Connected"
            mgmt_port_name = "mgmt"
            stacking_port_name = "Stacking"

            try:
                logger.info("Step 1: Opening Device360 window and navigating to Monitor -> Diagnostics page")
                xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_stack.mac)
                xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
                xiq_library_at_class_level.xflowsmanageDevice360.select_monitor_diagnostics_port_details()
                port_details_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_monitor_diagnostics_port_details_table()

                for i in range(1, stack_nr + 1):
                    tested_ports = []
                    connected_ports = []
                    selected_ports = []
                    verify_button = True
                    verify_error = True
                    port_nr = 1
                    port_details_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_monitor_diagnostics_port_details_table()
                    xiq_library_at_class_level.xflowscommonAutoActions.scroll_by_horizontal(port_details_table)
                    utils.wait_till(delay=20)
                    port_details_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
                    nr_of_ports = len(port_details_rows)

                    logger.info("Step 2: Select multiple ports from the table")
                    for row in port_details_rows:
                        port_nr += 1
                        tested_ports.append(port_nr)
                        # Only connected ports must be bounced otherwise the success message can't be seen because of the eror message
                        selected = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_table_select_checkbox(
                            port_nr)
                        if selected.is_selected():
                            xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                                port_nr)
                        if connected_port_status in row.text and stacking_port_name not in row.text and mgmt_port_name not in row.text:
                            connected_ports.append(port_nr)
                            selected_ports.append(
                                xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_port_name(
                                    port_nr - 1).text)

                        if len(tested_ports) == 7:
                            # Step 4: Click on the Bounce port button and verify action was successful
                            if len(connected_ports) != 0:
                                logger.info(f"Selected ports are : {selected_ports}")
                                logger.info(f"Selected rows are : {connected_ports}")
                                for port in connected_ports:
                                    xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                                        port)
                                xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_actions_button()

                                logger.info("Step 3: Click Actions button and verify Bounce port button is present")
                                if verify_button:
                                    port_button = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_actions_bounce_port_button()
                                    assert port_button, "Can't find Bounce Port button."
                                    verify_button = False

                                logger.info("Step 4: Click on the Bounce port button and verify action was successful")
                                xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_bounce_port_button()
                                message = xiq_library_at_class_level.xflowsmanageDevice360.wait_for_device360_diagnostics_actions_message()
                                assert message, "Success Message was not generated"
                                for port, port2 in zip(selected_ports, connected_ports):
                                    assert f"Bounce Port {port} successful" in message.get_attribute("innerHTML")
                                    logger.info(f"Deselecting port {port}")
                                    xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                                        port2)
                            tested_ports = []
                            connected_ports = []
                            is_connected = False
                            selected_ports = []
                    if i < stack_nr:
                        xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_stack_unit(i + 1)
            finally:
                logger.info("Cleanup: Closing Device360 Window")
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

        @pytest.mark.p1
        @pytest.mark.dependson("tcxm_xiq_onboarding")
        @pytest.mark.testbed_stack
        @pytest.mark.development
        @pytest.mark.tcxm_25664_2
        def test_tcxm_25664_2(self, logger, node_stack, cli, xiq_library_at_class_level, test_data, test_bed,
                              get_stack_slots, utils,
                              dev_cmd, default_library, network_manager, config_helper):
            """
            Verifies ports can be bounced using the Bounce Port button under Actions

    		Step        Step Description
    		1           Go to Port Details table under Monitor -> Diagnostics
    		2           Select multiple ports from the table
    		3           Click Actions button and verify Bounce Poe button is present
    		4           Click on the Bounce Poe button and verify action was successful
    		"""

            stack_nr = len(get_stack_slots(config_helper.dut1))

            connected_port_status = "Connected"
            mgmt_port_name = "mgmt"
            stacking_port_name = "Stacking"
            verify_button = True
            verify_error = True

            try:

                logger.info("Step 1: Opening Device360 window and navigating to Monitor -> Diagnostics page")
                xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_stack.mac)
                xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
                xiq_library_at_class_level.xflowsmanageDevice360.select_monitor_diagnostics_port_details()
                port_details_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_monitor_diagnostics_port_details_table()

                for i in range(1, stack_nr + 1):
                    logger.info("Verifying if device supports PoE!")
                    supports_poe = False
                    port_nr = 1
                    tested_ports = []
                    connected_ports = []
                    selected_ports = []
                    verify_button = True
                    verify_error = True
                    # Verify if Poe is supported and based on the results verify Bounce Poe button is present or not
                    logger.info("Verifying in device supports PoE!")
                    try:
                        network_manager.connect_to_network_element_name(node_stack.name)
                        ports_power_cli = []
                        if node_stack.cli_type.upper() == "EXOS":
                            output = dev_cmd.send_cmd(node_stack.name, f"show inline-power slot {i}",
                                                      max_wait=5, interval=2)[0].return_text
                            utils.wait_till(delay=10)
                            if "Inline-power card not present in slot" in output:
                                pytest.skip(
                                    "The device '{}' does not supported the PoE feature!".format(node_stack.name))
                            else:
                                supports_poe = True

                        elif node_stack.cli_type.upper() == "VOSS":

                            dev_cmd.send_cmd(node_stack.name, "enable", max_wait=5, interval=2)
                            dev_cmd.send_cmd(node_stack.name, "configure terminal", max_wait=5, interval=2)
                            output = dev_cmd.send_cmd(node_stack.name, "show poe-power-measurement | begin 1",
                                                      max_wait=5, interval=2, ignore_cli_feedback=True)[0].return_text
                            utils.wait_till(delay=2)
                            if "Device is not a POE device" in output:
                                logger.info(output)
                                pytest.skip(
                                    "The device '{}' does not supported the PoE feature!".format(node_stack.name))
                            else:
                                supports_poe = True
                    finally:
                        network_manager.close_connection_to_network_element(node_stack.name)

                    if supports_poe == True:
                        port_details_table = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_monitor_diagnostics_port_details_table()

                        # Step 2: Select multiple ports from the table
                        port_details_rows = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_all_port_table_rows()
                        logger.info(f"Number of rows is {len(port_details_rows)}")

                        logger.info("Step 2: Select multiple ports from the table")
                        for row in port_details_rows:
                            port_nr += 1
                            tested_ports.append(port_nr)
                            # Only connected ports must be bounced otherwise the success message can't be seen because of the error message
                            selected = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_table_select_checkbox(
                                port_nr)
                            if selected.is_selected():
                                xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                                    port_nr)
                            if stacking_port_name in row.text and stacking_port_name not in row.text and mgmt_port_name not in row.text:
                                connected_ports.append(port_nr)
                                selected_ports.append(
                                    xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_port_details_port_name(
                                        port_nr - 1).text)

                            if len(tested_ports) == 7:
                                # Step 4: Click on the Bounce port button and verify action was successful
                                if len(connected_ports) != 0:
                                    logger.info(f"Selected ports are : {selected_ports}")
                                    logger.info(f"Selected rows are : {connected_ports}")
                                    for port in connected_ports:
                                        xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                                            port)
                                    xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_actions_button()

                                    logger.info("Step 3: Click Actions button and verify Bounce Poe button is present")
                                    if verify_button:
                                        port_button = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_diagnostics_actions_bounce_poe_button()
                                        assert port_button, "Can't find Bounce PoE button."
                                        verify_button = False

                                    logger.info(
                                        "Step 4: Click on the Bounce port button and verify action was successful")
                                    xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_bounce_poe_button()
                                    message = xiq_library_at_class_level.xflowsmanageDevice360.wait_for_device360_diagnostics_actions_message()
                                    assert message, "Success Message was not generated"
                                    for port, port2 in zip(selected_ports, connected_ports):
                                        assert f"Bounce PoE Port {port} successful" in message.get_attribute(
                                            "innerHTML")
                                        logger.info(f"Deselecting port {port}")
                                        xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_port_select_button(
                                            port2)
                                tested_ports = []
                                connected_ports = []
                                is_connected = False
                                selected_ports = []

                        logger.info("Select Backup unit and repeat test")
                        if i < stack_nr:
                            logger.info(f"Selecting stack member : {i + 1}")
                            xiq_library_at_class_level.xflowsmanageDevice360.click_device360_diagnostics_actions_refresh_button()
                            xiq_library_at_class_level.xflowsmanageDevice360.select_device360_diagnostics_stack_unit(
                                i + 1)

            finally:
                logger.info("Cleanup: Closing Device360 Window")
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
