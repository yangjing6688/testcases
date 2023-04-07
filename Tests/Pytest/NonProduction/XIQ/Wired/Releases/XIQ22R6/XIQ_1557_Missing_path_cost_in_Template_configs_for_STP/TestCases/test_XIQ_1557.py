import pytest
import random
import string
import re

from collections import defaultdict
from ExtremeAutomation.Keywords.NetworkElementKeywords.StaticKeywords.NetworkElementResetDeviceUtilsKeywords import NetworkElementResetDeviceUtilsKeywords


@pytest.fixture
def make_sure_windows_are_closed(xiq_library_at_class_level, auto_actions):
    """ This fixture makes sure that the honeycomb/device360 windows are closed at the TEARDOWN of the test case.
    This way the next test case won't be affected if the current test failed and did not close all the windows during its call.
    """
    try:
        yield
    finally:
        try:
            if btn := xiq_library_at_class_level.xflowsmanageDevice360.get_cancel_port_type_box():
                auto_actions.click(btn)
        except:
            # close button not found
            pass
        
        try:
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
        except:
            # device360 window is not opened
            pass


@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.development
@pytest.mark.testbed_1_node
@pytest.mark.testbed_stack
class XIQ1557Tests:

    @pytest.mark.tcxm_22138
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p2
    def test_22138_verify_path_cost_column_is_present(
        self, test_data, logger, xiq_library_at_class_level,
        node_policy_name, node_template_name, utils, node):
        """
        TCXM-22138: Verify that Path Cost column is present under the STP tab in Switch Template Port Configuration.
        Author: vstefan
        """

        logger.info(
            f"Go to the port configuration of '{node_template_name}' template")
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(
            node_policy_name, node_template_name, node.cli_type)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.click_on_stp_tab()
        rows = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.get_stp_port_configuration_rows()

        for slot_index in range(1, (len(node.stack) if node.platform.upper() == "STACK" else 1) + 1):
            
            if node.platform.upper() == "STACK":
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.navigate_to_slot_template(f'{node_template_name}-{slot_index}')
            
            utils.wait_till(timeout=2)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.click_on_stp_tab()
            rows = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.get_stp_port_configuration_rows()
                    
            for index, row in enumerate(rows):
                
                path_cost_element, _ = utils.wait_till(
                    func=lambda:
                    xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_path_cost_row(row),
                    silent_failure=True,
                    exp_func_resp=True, 
                    delay=1
                )
                
                assert path_cost_element, \
                    f"Did not find the path cost element for this row:" \
                    f" '{row.text}' (row index: {index})"
                logger.info(
                    f"Successfully found the path cost element (it has "
                    f"value='{path_cost_element.get_attribute('value')}') "
                    f"for the row with index: {index}")

            logger.info(
                "Successfully verified that the path cost element is contained"
                " in every row of the STP port configuration table"
            )

    @pytest.mark.tcxm_22139
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p1
    def test_22139_verify_default_values_of_path_cost_at_template_level(
        self, test_data, logger, xiq_library_at_class_level, node_policy_name,
        node_template_name, utils, node):
        """
        TCXM-22139 - Verify that Path Cost for every port is set initially to default value (empty field).
        Author: vstefan
        """
        logger.info(
            f"Go to the port configuration of '{node_template_name}' template")
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(
            node_policy_name, node_template_name, node.cli_type)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        for slot_index in range(1, (len(node.stack) if node.platform.upper() == "STACK" else 1) + 1):
            
            if node.platform.upper() == "STACK":
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.navigate_to_slot_template(f'{node_template_name}-{slot_index}')
            
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.click_on_stp_tab()
            rows = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.get_stp_port_configuration_rows()
            assert rows, "Failed to get the STP port configuration rows"
            
            results = defaultdict(lambda: {"msg": "", "status": False})
            
            for row in rows:
                
                if text := row.text:
                    port_match = re.search(r"^(.*)\n", text)
                    assert port_match, f"Failed to get the port from '{text}'"
                    port = port_match.group(1)
                    
                    path_cost_element, _ = utils.wait_till(
                        func=lambda:
                        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_path_cost_row(row),
                        exp_func_resp=True,
                        delay=1
                    )
                    
                    path_cost_value = path_cost_element.get_attribute("value")
                    results[port]["status"] = path_cost_value == ""
                    results[port]["msg"] = f"Expected the path cost value to be '' but found '{path_cost_value}'" \
                                        f" for row with port='{port}'" if path_cost_value != "" else \
                        f"Successfully verified the default value of path cost for row with port={port}"
            
            for port, data in {port: data for port, data in results.items() if data["status"] is True}.items():
                logger.info(data["msg"])
            
            failed_verifications = {port: data for port, data in results.items() if data["status"] is False}
            
            if failed_verifications:
                for port, data in failed_verifications.items():
                    logger.error(data["msg"])
                pytest.fail("\n".join(list(data["msg"] for data in failed_verifications.values())))
            
            logger.info("Successfully verified that the default path cost values are '' at template level")


@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.development
@pytest.mark.testbed_1_node
class TestbedOneNodeXIQ1557Tests:
    
    @pytest.mark.tcxm_22140
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p1
    def test_22140_verify_path_cost_field_is_editable_template_level(
        self, test_data, logger, xiq_library_at_class_level, node_1, 
        node_1_policy_name, node_1_template_name, make_sure_windows_are_closed, auto_actions):
        """
        TCXM-22140 - Verify that Path Cost field is present under the STP tab when creating Port Type for the
         second port on each ASIC and has an editable field.
        Author: vstefan
        """
        
        ports = xiq_library_at_class_level.xflowsmanageDevice360.get_one_port_from_each_asic_flow(dut=node_1, order=2)
        port_config = defaultdict(lambda: {})
        
        for port in ports:
            port_config[port]["port_type_name"] = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"
            port_config[port]["path_cost"] = str(random.choice(range(1, 200000000)))
        logger.info(f"Port Type Configuration: {port_config}")

        logger.info(f"Go to the port configuration of '{node_1_template_name}' template")
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name, node_1_template_name, node_1.cli_type)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.click_on_port_details_tab()

        for port, port_info in port_config.items():
            
            logger.info(f"Configuring port '{port}' with {port_info}")
            
            port_type_name = port_info["port_type_name"]
            path_cost = port_info["path_cost"]
            
            try:
                xiq_library_at_class_level.xflowsmanageDevice360.open_new_port_type_editor(port=port)
                xiq_library_at_class_level.xflowsmanageDevice360.configure_port_name_usage_tab(port_type_name=port_type_name, port_type="access")
                xiq_library_at_class_level.xflowsmanageDevice360.go_to_stp_settings_tab_in_honeycomb()
                xiq_library_at_class_level.xflowsmanageDevice360.verify_path_cost_field_is_editable()
                xiq_library_at_class_level.xflowsmanageDevice360.configure_stp_settings_tab_in_honeycomb(
                    stp_enabled=True,
                    edge_port=True,
                    bpdu_protection="Disabled",
                    path_cost=path_cost
                )
                xiq_library_at_class_level.xflowsmanageDevice360.go_to_last_page()

                expected_summary = {
                    'STP': 'Enabled', 
                    'Edge Port': 'Enabled', 
                    'BPDU Protection': 'Disabled', 
                    'Path Cost': path_cost
                    }
                logger.info(f"Expected summary: {expected_summary}")
                
                summary = xiq_library_at_class_level.xflowsmanageDevice360.get_stp_settings_summary()
                logger.info(f"Found summary: {summary}")

                logger.info("Verify that the configured fields appear correctly in the summary tab")
                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"
                logger.info("Successfully verified the summary")
            
            finally:
                btn = xiq_library_at_class_level.xflowsmanageDevice360.get_cancel_port_type_box()
                auto_actions.click(btn)

    @pytest.mark.tcxm_22141
    @pytest.mark.tcxm_22142
    @pytest.mark.tcxm_22143
    @pytest.mark.tcxm_22144
    @pytest.mark.tcxm_22145
    @pytest.mark.tcxm_22201
    @pytest.mark.tcxm_22268
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p2
    def test_verify_path_cost(
        self, test_data, xiq_library_at_class_level, node_1, node_1_policy_name,
        node_1_template_name, make_sure_windows_are_closed):
        """
        TCXM-22141 - Verify that value 1 can be set for Path Cost for the 7th port on each ASIC.
        TCXM-22142 - Verify that value 200000000 can be set for Path Cost for the second port on each ASIC.
        TCXM-22143 - Verify that a random value between 1 and 200000000 can be set for Path Cost for the third port on each ASIC.
        TCXM-22144 - Verify that port Path Cost can be set to default for the4th port on each ASIC.
        TCXM-22145 - Verify that Configuration Audit reflects the changes when modifying Path Cost for the second port on each ASIC.
        TCXM-22201 - Verify that Path Cost can be modified for the 8th port from each ASIC when Port Usage is Trunk Port (802.1Q VLAN Tagging).
        TCXM-22268 - Verify that Path Cost can be modified for the 9th port from each ASIC when STP MODE is RSTP.
        Author: vstefan
        """
        
        if (test_data["tc"] == "tcxm_22268") and (node_1.cli_type.upper() != "EXOS"):
            pytest.skip("This test case must run on an EXOS device.")

        xiq_library_at_class_level.xflowsmanageXiqVerifications.verify_path_cost_at_template_level(
            onboarded_switch=node_1,
            path_cost=test_data.get("path_cost", "random"),
            port_order_in_asic=test_data.get("port_order_in_asic", "1"),
            template_switch=node_1_template_name,
            network_policy=node_1_policy_name,
            port_type=test_data.get("port_type", "access"),
            verify_delta_cli=test_data.get("verify_delta_cli", False),
            stp_mode=test_data.get("stp_mode", "mstp"),
            revert_mode=test_data.get("revert_mode", "revert_template"),
            revert_configuration=test_data.get("revert_configuration", True),
            cli_type=node_1.cli_type
        )

    @pytest.mark.tcxm_22147
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p1
    def test_22147_verify_path_cost_value_in_create_port_type_window(
            self, logger, test_data, xiq_library_at_class_level, node_1, auto_actions,
            node_1_policy_name, node_1_template_name, make_sure_windows_are_closed):
        """
        TCXM-22147 - Verify that the Path Cost Value is present and correct in Create Port Type window, Summary tab.
        Author: vstefan
        """
        ports = xiq_library_at_class_level.xflowsmanageDevice360.get_one_port_from_each_asic_flow(dut=node_1, order=4)

        logger.info(f"Go to the port configuration of '{node_1_template_name}' template")
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name, node_1_template_name, node_1.cli_type)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.click_on_port_details_tab()
        
        for port in ports:
        
            port_type_name = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"
            path_cost = str(random.choice(range(1, 200000000)))
            logger.info(
                f"Create a new port type '{port_type_name}' with path cost '{path_cost}' for port '{port}'")
            
            try:
                expected_summary = {
                    'STP': 'Enabled', 
                    'Edge Port': 'Enabled', 
                    'BPDU Protection': 'Disabled',
                    'Path Cost': path_cost
                    }
                logger.info(f"Expected summary: {expected_summary}")
                
                _, summary = xiq_library_at_class_level.xflowsmanageDevice360.create_port_type_with_stp_settings(
                    port, port_type_name=port_type_name, path_cost=path_cost, description="description", status=True, 
                    port_usage="access", bpdu_protection="Disabled", stp_enabled=True, edge_port=True,
                    save=False)
                logger.info(f"Found summary: {summary}")

                logger.info("Verify that the configured fields appear correctly in the summary tab")
                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"
                logger.info(
                    f"Successfully verified the summary for port type '{port_type_name}' "
                    f"with path cost '{path_cost}' for port '{port}'"
                )
                
            finally:
                btn = xiq_library_at_class_level.xflowsmanageDevice360.get_cancel_port_type_box()
                auto_actions.click(btn)

    @pytest.mark.tcxm_22148
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p2
    def test_22148_verify_path_cost_value_in_edit_port_type_window(
            self, test_data, logger, xiq_library_at_class_level, make_sure_windows_are_closed,
            node_1, node_1_policy_name, node_1_template_name, utils):
        """
        TCXM-22148 - Verify that the Path Cost Value is present and correct in Edit Port Type window, Summary tab.
        Author: vstefan
        """
        ports = xiq_library_at_class_level.xflowsmanageDevice360.get_one_port_from_each_asic_flow(dut=node_1, order=5)
        port_config = defaultdict(lambda: {})
        
        for port in ports:
            port_config[port]["port_type_name"] = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"
            port_config[port]["path_cost"] = str(random.choice(range(1, 200000000)))
        logger.info(f"Port Type Configuration: {port_config}")

        logger.info(f"Go to the port configuration of '{node_1_template_name}' template")
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name, node_1_template_name, node_1.cli_type)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.click_on_port_details_tab()

        try:
            for port, port_info in port_config.items():
                
                port_type_name = port_info["port_type_name"]
                path_cost = port_info["path_cost"]
                logger.info(
                    f"Create a new port type '{port_type_name}' with path cost '{path_cost}' for port '{port}'")
                
                expected_summary = {
                    'STP': 'Enabled', 
                    'Edge Port': 'Enabled', 
                    'BPDU Protection': 'Disabled',
                    'Path Cost': path_cost
                    }
                logger.info(f"Expected summary: {expected_summary}")
                
                _, create_port_type_summary = xiq_library_at_class_level.xflowsmanageDevice360.create_port_type_with_stp_settings(
                    port, port_type_name=port_type_name, path_cost=path_cost, description="description", status=True, 
                    port_usage="access", bpdu_protection="Disabled", stp_enabled=True, edge_port=True)
                logger.info(
                    f"Summary from create port type in honeycom (port {port}): {create_port_type_summary}")

                logger.info(
                    f"Verify that the configured fields appear correctly in the summary tab (port {port})")
                assert all(expected_summary[k] == create_port_type_summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones (port {port}). " \
                    f"Expected summary: {expected_summary}\nFound summary: {create_port_type_summary}"
                logger.info(
                    f"Successfully verified the summary at port type creation in honeycomb (port {port})")
                
                utils.wait_till(timeout=10)
                _, edit_port_type_summary = xiq_library_at_class_level.xflowsmanageDevice360.edit_stp_settings_in_honeycomb_port_editor(
                    port, port_type_name)
                logger.info(
                    f"Summary from edit port type in honeycomb (port {port}): {create_port_type_summary}")
        
                logger.info(
                    f"Verify that the configured fields appear correctly in the summary tab (port {port})")
                assert all(expected_summary[k] == edit_port_type_summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones (port {port}). " \
                    f"Expected summary: {expected_summary}\nFound summary: {edit_port_type_summary}"
                logger.info(
                    f"Successfully verified the summary at port type edit in honeycomb (port {port})")

        finally:
            
            logger.info(f"Go to the port configuration of '{node_1_template_name}' template")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(
                node_1_policy_name, node_1_template_name, node_1.cli_type)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                    
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.revert_port_configuration_template_level(
                "Auto-sense Port" if node_1.cli_type.upper() == "VOSS" else "Access Port")
            utils.wait_till(timeout=5)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
            utils.wait_till(timeout=10)

    @pytest.mark.tcxm_22151
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p1
    def test_22151_verify_not_valid_path_cost_values_in_honeycomb(
            self, logger, xiq_library_at_class_level, node_1, auto_actions,
            node_1_policy_name, node_1_template_name, make_sure_windows_are_closed, utils):
        """
        TCXM-22151 - Verify you cannot set a negative value, 0, 200000001 or a character for Path Cost for the second port on each ASIC.
        Author: vstefan
        """
        wrong_values = ["-1", "200000001", "#", "b"]
        ports = xiq_library_at_class_level.xflowsmanageDevice360.get_one_port_from_each_asic_flow(
            dut=node_1, order=2)
        port_type_name = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"
        
        logger.info(
            f"Go to the port configuration of '{node_1_template_name}' template")
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(
            node_1_policy_name, node_1_template_name, node_1.cli_type)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.click_on_port_details_tab()

        for port in ports:
            logger.info(
                f"Verifying that the wrong values ('{wrong_values}') cannot be"
                f"set as path cost in honeycomb port editor for port '{port}'"
            )
            
            try:
                xiq_library_at_class_level.xflowsmanageDevice360.open_new_port_type_editor(port=port)
                xiq_library_at_class_level.xflowsmanageDevice360.configure_port_name_usage_tab(
                    port_type_name=port_type_name,
                    port_type="access"
                )
                xiq_library_at_class_level.xflowsmanageDevice360.go_to_stp_settings_tab_in_honeycomb()
                
                for value in wrong_values:
                    
                    logger.info(
                        f"Try to set '{value}' as path_cost for port '{port}'")
                    xiq_library_at_class_level.xflowsmanageDevice360.set_path_cost_in_honeycomb(value)
                    
                    utils.wait_till(timeout=5)
                    path_cost_value = xiq_library_at_class_level.xflowsmanageDevice360.get_select_element_port_type("path cost").get_attribute("value")
                    if path_cost_value != value:
                        logger.info(f"Path cost input element did not update to the wrong given value '{value}'.")
                        continue
                    
                    xiq_library_at_class_level.xflowsmanageDevice360.go_to_next_editor_tab()
                    
                    try:
                        xiq_library_at_class_level.xflowsmanageDevice360.verify_port_type_editor_still_in_stp_tab()
                    
                    except AssertionError as err:
                        msg = f"Failed! Expected the honeycomb editor to " \
                              f"still be in the STP tab after " \
                              f"clicking NEXT TAB when path_cost='{value}'"
                        logger.info(msg)
                        logger.info(repr(err))
                        pytest.fail(msg)
                    else:
                        logger.info(f"Path cost input element did not update to the wrong given value '{value}'.")
                        
                logger.info(
                    f"Successfully verified that these values cannot be set"
                    f" (port '{port}'): '{wrong_values}'"
                )
            
            finally:
                btn = xiq_library_at_class_level.xflowsmanageDevice360.get_cancel_port_type_box()
                auto_actions.click(btn)

    @pytest.mark.tcxm_22152
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p2
    def test_22152_verify_path_cost_value_after_reboot_of_device(
        self, test_data, logger, test_bed, xiq_library_at_class_level, make_sure_windows_are_closed,
        node_1, node_1_policy_name, node_1_template_name, cli, utils):
        """
        TCXM-22152 - Verify that rebooting the device doesn't affect the configured Path Cost values
        Author: vstefan
        """
        ports = xiq_library_at_class_level.xflowsmanageDevice360.get_one_port_from_each_asic_flow(
            node_1, order=1)
        path_cost = str(random.choice(range(1, 200000000)))
        
        reboot_utils = NetworkElementResetDeviceUtilsKeywords()

        try:
            xiq_library_at_class_level.xflowsmanageXiqVerifications.verify_path_cost_at_template_level(
                onboarded_switch=node_1,
                path_cost=path_cost,
                template_switch=node_1_template_name,
                network_policy=node_1_policy_name,
                revert_configuration=False,
                ports=ports,
                cli_type=node_1.cli_type
            )

            with test_bed.enter_switch_cli(node_1):
                reboot_utils.reboot_network_element_now_and_wait(node_1.name, max_wait=600)

            xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(
                node_1.serial)
            res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(
                device_serial=node_1.serial)
            assert res == 'green', \
                f"The device did not come up successfully in the XIQ;" \
                f"Device: {node_1}"
            logger.info("Device come up successfully in the XIQ")

            for port in ports:
                
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.verify_path_cost_in_port_configuration_stp_tab(
                    node_1.cli_type, node_1_template_name, node_1_policy_name, port, path_cost)
                cli.verify_path_cost_on_device(
                    node_1,
                    port=port, 
                    expected_path_cost=path_cost
                )

        finally:
            
            try:
                logger.info(
                    f"Go to the port configuration of" 
                    f" '{node_1_template_name}' template"
                )
                
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(
                    node_1_policy_name, node_1_template_name, node_1.cli_type)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.click_on_port_details_tab()
                        
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.revert_port_configuration_template_level(
                    "Auto-sense Port" if node_1.cli_type.upper() == "VOSS" else "Access Port")
                    
            finally:
                
                utils.wait_till(timeout=5)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                utils.wait_till(timeout=10)
                
                logger.info(
                    "Saved the port type configuration,"
                    "now push the changes to the dut"
                )
                xiq_library_at_class_level.xflowscommonDevices.update_and_wait_device(
                    policy_name=node_1_policy_name, dut=node_1)


@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.development
@pytest.mark.testbed_stack
class TestbedStackXIQ1557Tests:

    @pytest.mark.tcxm_22161
    @pytest.mark.EXOS
    @pytest.mark.p2
    def test_22161_verify_random_value_as_path_cost(
        self, test_data, logger, node_stack_policy_name, make_sure_windows_are_closed,
        node_stack_template_name, node_stack, xiq_library_at_class_level):
        """
        TCXM-22161 - Verify that a random value between 1 and 200000000 can be set for Path Cost the third port on each ASIC on stack slot 2
        Author: sstaut
        """
        xiq_library_at_class_level.xflowsmanageXiqVerifications.verify_path_cost_at_template_level(
            onboarded_switch=node_stack,
            path_cost="random",
            port_order_in_asic=3,
            template_switch=node_stack_template_name,
            network_policy=node_stack_policy_name,
            slot="2",
            cli_type=node_stack.cli_type
        )

    @pytest.mark.tcxm_22164
    @pytest.mark.EXOS
    @pytest.mark.p2
    def test_22164_verify_random_value_as_path_cost(
        self, test_data, logger, node_stack_policy_name, node_stack_template_name,
        node_stack, xiq_library_at_class_level, make_sure_windows_are_closed):
        """
        TCXM-22164 - Verify that a random value between 1 and 200000000 can be set for Path Cost the last port on each ASIC on both stack slots.
        Author: rvisterineanu
        """
        xiq_library_at_class_level.xflowsmanageXiqVerifications.verify_path_cost_at_template_level(
            onboarded_switch=node_stack,
            path_cost="random",
            port_order_in_asic=20,
            template_switch=node_stack_template_name,
            network_policy=node_stack_policy_name,
            slot="1",
            cli_type=node_stack.cli_type
        )

        xiq_library_at_class_level.xflowsmanageXiqVerifications.verify_path_cost_at_template_level(
            onboarded_switch=node_stack,
            path_cost="random",
            port_order_in_asic=20,
            template_switch=node_stack_template_name,
            network_policy=node_stack_policy_name,
            slot="2",
            cli_type=node_stack.cli_type
        )

    @pytest.mark.tcxm_22167
    @pytest.mark.EXOS
    @pytest.mark.p2
    def test_22167_verify_random_value_as_path_cost(
        self, test_data, logger, node_stack_policy_name, node_stack_template_name,
        node_stack, xiq_library_at_class_level, utils, make_sure_windows_are_closed):
        """
        TCXM-22167 - Verify that the Path Cost Value is present and correct in Edit Port Type window Summary tab for the second port on each ASIC on both stack slots.
        Author: rvisterineanu
        """
        try:
            
            for slot in range(1, len(node_stack.stack) + 1):
                
                slot = str(slot)
                ports = xiq_library_at_class_level.xflowsmanageDevice360.get_one_port_from_each_asic_flow(dut=node_stack, order=2, slot=slot)
                
                port_config = defaultdict(lambda: {})
                for port in ports:
                    port_config[port]["port_type_name"] = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"
                    port_config[port]["path_cost"] = str(random.choice(range(1, 200000000)))
                logger.info(f"Port Type Configuration: {port_config}")

                logger.info(f"Go to the port configuration of '{node_stack_template_name}' template")
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_stack_policy_name, node_stack_template_name, node_stack.cli_type)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                required_slot = node_stack_template_name + "-" + slot
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.navigate_to_slot_template(required_slot)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.click_on_port_details_tab()

                for port, port_info in port_config.items():
                    port_type_name = port_info["port_type_name"]
                    path_cost = port_info["path_cost"]
                    logger.info(
                        f"Create a new port type '{port_type_name}' with path cost '{path_cost}' for port '{port}'")

                    expected_summary = {
                        'STP': 'Enabled',
                        'Edge Port': 'Enabled',
                        'BPDU Protection': 'Disabled',
                        'Path Cost': path_cost
                    }
                    logger.info(f"Expected summary: {expected_summary}")

                    _, create_port_type_summary = xiq_library_at_class_level.xflowsmanageDevice360.create_port_type_with_stp_settings(
                        port, port_type_name=port_type_name, path_cost=path_cost, description="description", status=True,
                        port_usage="access", bpdu_protection="Disabled", stp_enabled=True, edge_port=True)
                    logger.info(
                        f"Summary from create port type in honeycom (port {port}): {create_port_type_summary}")

                    logger.info(
                        f"Verify that the configured fields appear correctly in the summary tab (port {port})")
                    assert all(expected_summary[k] == create_port_type_summary[k] for k in expected_summary), \
                        f"Not all the values of the summary are the expected ones (port {port}). " \
                        f"Expected summary: {expected_summary}\nFound summary: {create_port_type_summary}"
                    logger.info(
                        f"Successfully verified the summary at port type creation in honeycomb (port {port})")

                    utils.wait_till(timeout=10)
                    _, edit_port_type_summary = xiq_library_at_class_level.xflowsmanageDevice360.edit_stp_settings_in_honeycomb_port_editor(
                            port, port_type_name)
                    logger.info(
                        f"Summary from edit port type in honeycomb (port {port}): {create_port_type_summary}")

                    logger.info(
                        f"Verify that the configured fields appear correctly in the summary tab (port {port})")
                    assert all(expected_summary[k] == edit_port_type_summary[k] for k in expected_summary), \
                        f"Not all the values of the summary are the expected ones (port {port}). " \
                        f"Expected summary: {expected_summary}\nFound summary: {edit_port_type_summary}"
                    logger.info(
                        f"Successfully verified the summary at port type edit in honeycomb (port {port})")

        finally:

            logger.info(f"Go to the port configuration of '{node_stack_template_name}' template")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(
                node_stack_policy_name, node_stack_template_name, node_stack.cli_type)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.revert_port_configuration_template_level("Access Port")
            utils.wait_till(timeout=5)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
            utils.wait_till(timeout=10)

    @pytest.mark.tcxm_22171
    @pytest.mark.EXOS
    @pytest.mark.p2
    def test_22171_verify_path_cost_value_after_reboot_of_device(
        self, test_data, logger, test_bed, node_stack_policy_name, node_stack_template_name,
        node_stack, xiq_library_at_class_level, utils, cli, make_sure_windows_are_closed):
        """
        TCXM-22171 - Verify that rebooting the stack doesn't affect the configured Path Cost values
        Author: rvisterineanu
        """
        
        ports_slot1 = xiq_library_at_class_level.xflowsmanageDevice360.get_one_port_from_each_asic_flow(
            node_stack, order=8, slot="1")
        ports_slot2 = xiq_library_at_class_level.xflowsmanageDevice360.get_one_port_from_each_asic_flow(
            node_stack, order=8, slot="2")
        path_cost = str(random.choice(range(1, 200000000)))

        try:
            xiq_library_at_class_level.xflowsmanageXiqVerifications.verify_path_cost_at_template_level(
                onboarded_switch=node_stack,
                path_cost=path_cost,
                template_switch=node_stack_template_name,
                network_policy=node_stack_policy_name,
                revert_configuration=False,
                ports=ports_slot1,
                slot="1",
                cli_type=node_stack.cli_type
            )

            xiq_library_at_class_level.xflowsmanageXiqVerifications.verify_path_cost_at_template_level(
                onboarded_switch=node_stack,
                path_cost=path_cost,
                template_switch=node_stack_template_name,
                network_policy=node_stack_policy_name,
                revert_configuration=False,
                ports=ports_slot2,
                slot="2",
                cli_type=node_stack.cli_type
            )

            reboot_utils = NetworkElementResetDeviceUtilsKeywords()
            
            with test_bed.enter_switch_cli(node_stack):
                reboot_utils.reboot_network_element_now_and_wait(node_stack.name, max_wait=600)

            xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(
                node_stack.mac)
            res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(
                device_serial=node_stack.mac)
            assert res == 'green', \
                f"The device did not come up successfully in the XIQ;" \
                f"Device: {node_stack}"
            logger.info("Device come up successfully in the XIQ")

            for port in ports_slot1:
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.verify_path_cost_in_port_configuration_stp_tab(
                    node_stack.cli_type, node_stack_template_name, node_stack_policy_name, port, path_cost, slot="1")
                cli.verify_path_cost_on_device(
                    node_stack,
                    port=port,
                    expected_path_cost=path_cost
                )

            for port in ports_slot2:
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.verify_path_cost_in_port_configuration_stp_tab(
                    node_stack.cli_type, node_stack_template_name, node_stack_policy_name, port, path_cost, slot="2")
                cli.verify_path_cost_on_device(
                    node_stack,
                    port=port,
                    expected_path_cost=path_cost
                )

        finally:

            try:
                logger.info(
                    f"Go to the port configuration of"
                    f" '{node_stack_template_name}' template"
                )

                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(
                    node_stack_policy_name, node_stack_template_name, node_stack.cli_type)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.click_on_port_details_tab()

                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.revert_port_configuration_template_level("Access Port")

            finally:
                
                utils.wait_till(timeout=5)
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
                utils.wait_till(timeout=10)
                
                logger.info(
                    "Saved the port type configuration,"
                    "now push the changes to the dut"
                )
                xiq_library_at_class_level.xflowscommonDevices.update_and_wait_device(
                    policy_name=node_stack_policy_name, dut=node_stack)

    @pytest.mark.tcxm_22190
    @pytest.mark.EXOS
    @pytest.mark.p2
    def test_22190_verify_not_valid_path_cost_values_in_honeycomb(
            self, test_data, logger, node_stack_policy_name, node_stack_template_name,
            node_stack, xiq_library_at_class_level, make_sure_windows_are_closed, auto_actions, utils):
        """
        TCXM-22190 - Verify you cannot set a negative value, 0, 200000001 or a character for Path Cost for the 3rd port on each ASIC on both stack slots.
        Author: rvisterineanu
        """
        wrong_values = ["-1", "200000001", "#", "b"]

        for slot in range(1, len(node_stack.stack) + 1):
            slot = str(slot)
            ports = xiq_library_at_class_level.xflowsmanageDevice360.get_one_port_from_each_asic_flow(dut=node_stack, order=3, slot=slot)
            port_type_name = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"

            logger.info(
                f"Go to the port configuration of '{node_stack_template_name}' template")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(
                node_stack_policy_name, node_stack_template_name, node_stack.cli_type)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            required_slot = node_stack_template_name + "-" + slot
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.navigate_to_slot_template(required_slot)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.click_on_port_details_tab()

            for port in ports:
                logger.info(
                    f"Verifying that the wrong values ('{wrong_values}') cannot be"
                    f"set as path cost in honeycomb port editor for port '{port}'"
                )

                try:
                    xiq_library_at_class_level.xflowsmanageDevice360.open_new_port_type_editor(port=port)
                    xiq_library_at_class_level.xflowsmanageDevice360.configure_port_name_usage_tab(
                        port_type_name=port_type_name,
                        port_type="access"
                    )
                    xiq_library_at_class_level.xflowsmanageDevice360.go_to_stp_settings_tab_in_honeycomb()

                    for value in wrong_values:
                        
                        logger.info(
                            f"Try to set '{value}' as path_cost for port '{port}'")
                        xiq_library_at_class_level.xflowsmanageDevice360.set_path_cost_in_honeycomb(value)
                        
                        utils.wait_till(timeout=5)
                        path_cost_value = xiq_library_at_class_level.xflowsmanageDevice360.get_select_element_port_type("path cost").get_attribute("value")
                        if path_cost_value != value:
                            logger.info(f"Path cost input element did not update to the wrong given value '{value}'.")
                            continue
                        
                        xiq_library_at_class_level.xflowsmanageDevice360.go_to_next_editor_tab()
                        
                        try:
                            xiq_library_at_class_level.xflowsmanageDevice360.verify_port_type_editor_still_in_stp_tab()
                        
                        except AssertionError as err:
                            msg = f"Failed! Expected the honeycomb editor to " \
                                f"still be in the STP tab after " \
                                f"clicking NEXT TAB when path_cost='{value}'"
                            logger.info(msg)
                            logger.info(repr(err))
                            pytest.fail(msg)
                        else:
                            logger.info(f"Path cost input element did not update to the wrong given value '{value}'.")
                        
                    logger.info(
                        f"Successfully verified that these values cannot be set"
                        f" (port '{port}'): '{wrong_values}'"
                    )
                finally:
                    btn = xiq_library_at_class_level.xflowsmanageDevice360.get_cancel_port_type_box()
                    auto_actions.click(btn)
