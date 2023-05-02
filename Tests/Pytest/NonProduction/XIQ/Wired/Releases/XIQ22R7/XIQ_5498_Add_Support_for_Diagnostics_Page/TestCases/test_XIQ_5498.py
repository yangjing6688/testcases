import pytest


@pytest.fixture
def make_sure_windows_are_closed(xiq_library_at_class_level):
    """ This fixture makes sure that the device360 window is closed at the TEARDOWN of the test case.
    """
    try:
        yield
    finally:
        try:
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
        except:
            # device360 window is not opened
            pass


@pytest.mark.development
@pytest.mark.p1
@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.testbed_1_node
class Xiq5498OneNodeTests:
    
    @pytest.mark.tcxm_22209
    def test_tcxm_22209(self, test_data, node_1, logger, xiq_library_at_class_level, make_sure_windows_are_closed):
        """
        TCXM - 22209 - Verify that the Diagnostics option is available under the Monitor Tab
        Step    Description
        1       Onboard the EXOS device
        2       Navigate to Device360
        3       In Monitor Tab check that the Diagnostics option is present in Monitoring Menu
        4       Click on the Diagnostics TAB
        --------------
        5       Verify if the slot selector dropdown isn't present
        """
        D360Flag = 0

        try:
            res = xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac)
            assert res, "Unable to go to device360 window"
            D360Flag = 1
            res = xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
            assert res, "Unable to navigate to Diagnostics TAB"

            logger.step("Verify that the slot dropdown selector is not present")
            stack_dropdown = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_monitor_diagnostics_stack_drop_down()
            assert stack_dropdown == -1, "The stack selector dropdown is present for standalone"

        finally:
            if D360Flag == 1:
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

    @pytest.mark.tcxm_22211
    @pytest.mark.dependson("tcxm_22209")
    def test_tcxm_22211(self, test_data, logger):
        """
        TCXM - 22211 - Verify that the slot dropdown selector is not present for standalone.
        """
        logger.info("This test case is covered by tcxm_22209.")


@pytest.mark.p1
@pytest.mark.testbed_stack
@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.development
class Xiq5498StackTests:
    
    @pytest.fixture(scope="class", autouse=True)
    def connect_to_node_stack(self, node_stack, network_manager, close_connection):
        try:
            close_connection(node_stack)
            network_manager.connect_to_network_element_name(node_stack.name)
            yield
        finally:
            close_connection(node_stack)

    @pytest.mark.tcxm_22213
    def test_tcxm_22213(self, test_data, node_stack, cli, logger, xiq_library_at_class_level, make_sure_windows_are_closed):
        """
        TCXM - 22213 - Verify that the Diagnostics option is available under the Monitor Tab for a stack (Step 1-4)
        Step    Description
        1       Onboard the EXOS device
        2       Navigate to Device360
        3       In Monitor Tab check that the Diagnostics option is present in Monitoring Menu
        4       Click on the Diagnostics TAB
        --------------
        5       For each value displayed in the header part(device information), verify if it coincides with the cli value
        """
        D360Flag = 0

        try:
            res = xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_stack.mac)
            assert res != -1, "Unable to go to device360 window"
            D360Flag = 1
            res = xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
            assert res != -1, "Unable to navigate to Diagnostics TAB"

            logger.step("Navigate to master unit")
            stacking_info_cli = cli.get_stacking_details_cli(node_stack)
            logger.info(f"Print a list with mac add, number of slot and role for each stack unit: {stacking_info_cli}")

            res = xiq_library_at_class_level.xflowsmanageDevice360.navigate_to_unit_options_from_xiq_diagnostics_page(
                stacking_info_cli[0][0][1], stacking_info_cli[0][0][2].upper())

            logger.step("Verify if the device information from the header side is displayed correctly according to the CLI - Master Unit")
            res = xiq_library_at_class_level.xflowsmanageDevice360.match_info_stack_cli_with_xiq(
                node_stack, cli.get_info_from_stack(node_stack), stacking_info_cli[0][0][1])
            assert res != -1, "Unable to verify if the device information from the header side is displayed correctly according to the CLI"

        finally:
            if D360Flag == 1:
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

    @pytest.mark.tcxm_22221
    @pytest.mark.dependson("tcxm_22213")
    def test_tcxm_22221(self, test_data, logger):
        """
        TCXM - 22221 - Verify if the device information(ip, mac address, software version, model, serial, make, iqagent version) 
        from the header side is displayed correctly according to the cli (Master Unit) (Step 1-5)
        """
        logger.info("This test case is covered by tcxm_22213")

    @pytest.mark.tcxm_22215
    def test_tcxm_22215(self, test_data, node_stack, logger, cli, xiq_library_at_class_level, make_sure_windows_are_closed):
        """
        TCXM - 22215 - Verify that the slot dropdown selector is present and contains all the individual
        Step    Description
        1	Onboard the EXOS stack.
        2	Navigate to Device360.
        3	Navigate to the Monitor Tab --> Diagnostics TAB.
        --------------
        4	Check if the dropdown at the top of the page is present and correctly displays all the devices in the stack
        5   Click on each item in the dropdown in order to verify that it redirects the user to the correct option
        --------------
        6	Verify if the select all ports button is present.
        7	Click on the select all ports button.
        --------------
        8	Verify if the DeSelect all ports button is present.
        9	Click on the DeSelect all ports button.
        """
        D360Flag = 0

        try:
            res = xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_stack.mac)
            assert res != -1, "Unable to go to device360 window"
            D360Flag = 1
            res = xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
            assert res != -1, "Unable to navigate to Diagnostics TAB"

            logger.step("Check if the dropdown at the top of the page is present")
            stack_dropdown = xiq_library_at_class_level.xflowsmanageDevice360.get_device360_monitor_diagnostics_stack_drop_down()
            assert stack_dropdown != -1, "The stack selector dropdown isn't present"

            stacking_info_cli = cli.get_stacking_details_cli(node_stack)
                
            logger.step("Check each item in the dropdown in order to verify that it redirects the user to the correct option")
            res = xiq_library_at_class_level.xflowsmanageDevice360.check_all_the_individual_devices_in_the_stack_monitor_diagnostics(
                node_stack, stacking_info_cli)
            assert res != -1, "Unable to check each item in the dropdown"

            logger.step("Verify if the select all ports button is present and click on it")
            select = xiq_library_at_class_level.xflowsmanageDevice360.device360_port_diagnostics_select_all_ports()
            assert select != -1, "unable to verify if the select all ports button is present and click on it"

            logger.step("Verify if the dselect all ports button is present and click on it")
            deselect = xiq_library_at_class_level.xflowsmanageDevice360.device360_port_diagnostics_deselect_all_ports()
            assert deselect != -1, "Unable to verify if the dselect all ports button is present and click on it"

        finally:
            if D360Flag == 1:
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

    @pytest.mark.tcxm_22217
    @pytest.mark.dependson("tcxm_22215")
    def test_tcxm_22217(self, test_data, logger):
        """ TCXM - 22217 - Verify if the Select All Ports button is present and clickable
        """
        logger.info("This test case is covered by tcxm_22215.")
        
    @pytest.mark.tcxm_22219
    @pytest.mark.dependson("tcxm_22215")
    def test_tcxm_22219(self, test_data, logger):
        """ TCXM - 22219 - Verify if the DeSelect All Ports button is present and clickable
        """
        logger.info("This test case is covered by tcxm_22215.")

    @pytest.mark.tcxm_22223
    def test_tcxm_22223(self, test_data, node_stack, cli, logger, xiq_library_at_class_level, make_sure_windows_are_closed):
        """
        TCXM - 22223 - Verify if it's possible to hover over the first 7 icons
                       in the port diagnostics section(CPU Usage, Memory, Temperature etc)
                       and the opened box displays correctly the information(Master Unit).
        Step    Description
        1	Onboard the EXOS stack.
        2	Navigate to Device360.
        3	Navigate to the Monitor Tab --> Diagnostics TAB.
        4	Hover over each item from the seven icons in the port diagnostics section.
        """
        D360Flag = 0

        try:
            res = xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_stack.mac)
            assert res != -1, "Unable to go to device360 window"
            D360Flag = 1
            res = xiq_library_at_class_level.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
            assert res != -1, "Unable to navigate to Diagnostics TAB"

            logger.step("Navigate to master unit")
            stacking_info_cli = cli.get_stacking_details_cli(node_stack)
            logger.info(f"Print a list with mac add, number of slot and role for each stack unit: {stacking_info_cli}")

            res = xiq_library_at_class_level.xflowsmanageDevice360.navigate_to_unit_options_from_xiq_diagnostics_page(
                stacking_info_cli[0][0][1], stacking_info_cli[0][0][2].upper())

            logger.step("Verify the first seven icons from the top bar (Master Unit)")
            xiq_library_at_class_level.xflowsmanageDevice360.device360_get_top_bar_information_stack()
            logger.info("Verify the first seven icons from the top bar for each other unit")

            stacking_info_cli = cli.get_stacking_details_cli(node_stack)

            xiq_library_at_class_level.xflowsmanageDevice360.navigate_to_unit_1_n_and_hover_over_top_bar_information_stack(
                node_stack, stacking_info_cli)

        finally:
            if D360Flag == 1:
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
