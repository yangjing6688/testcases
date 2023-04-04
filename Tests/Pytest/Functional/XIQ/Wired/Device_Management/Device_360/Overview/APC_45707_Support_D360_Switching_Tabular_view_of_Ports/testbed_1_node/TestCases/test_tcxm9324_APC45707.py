# Author:         vstefan
# Description:    To verify if tabular view displays transmission mode column
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9324
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase
from typing import List


class TCXM9324Tests(xiqBase):

    @pytest.mark.tcxm_9324
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_9324_verify_transmission_mode_column(self, logger, onboarded_switch, request, setup_lldp, onboarding_location):
        """ 
        Step	Step Description
        1	    Onboard the device
        2	    Navigate to Device360, Monitor, Overview
        3	    Go to the ports table and get its columns
        4	    Verify the 'transmission mode' column is selected in the column picker
        5	    Get all the entries of the ports table
        6	    Verify the transmission mode is set to “Full-Duplex” for active ports (by default value) and 'N/A' for inactive ports
        7	    CLI - Change the value of the  'transmission mode' field to 'Half-Duplex' for all the ports
        8	    Verify that the ports updated to 'Half-Duplex' in Device360
        9	    CLI - Verify that the ports updated to 'Half-Duplex' directly on the EXOS/VOSS dut
        10	    Revert the changes to the chosen ports
        11	    Delete the onboarded device and logout from XIQ
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9324'

        column_name = "Transmission Mode"
        connected_ports: List[str] = []
        
        try:
            self.suite_udk.go_to_device360(onboarded_switch)

            self.suite_udk.select_max_pagination_size()

            checkbox_button = self.xiq.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()
            checkbox_button.location_once_scrolled_into_view
            self.auto_actions.click(checkbox_button)
            time.sleep(3)

            all_checkboxes = self.xiq.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
            columns_found_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
            logger.info(f"These columns are currently found enabled: {columns_found_enabled}")

            assert column_name in columns_found_enabled, f"Failed! {column_name} column is not visible by default"
            logger.info(f"{column_name} column is visible by default")

            ports_table = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()

            for entry in ports_table:
                
                assert column_name.upper() in entry, f"Failed to find {column_name} column in table row: {entry}"
                
                transmission_mode = entry[column_name.upper()]
                port_name = entry['PORT NAME']
                logger.info(f"Row with 'Port Name'='{port_name}' has '{column_name}'='{transmission_mode}'")
                
                if entry["PORT STATUS"] == "Connected":
                    assert transmission_mode == "Full-Duplex", \
                        f"{port_name} port is connected but transmission mode={transmission_mode} (expected 'Full-Duplex')"
                    logger.info(f"Successfully found transmission_mode='Full-Duplex' for port_name={port_name}")
                    if port_name != "mgmt":
                        connected_ports.append(port_name)

                elif entry["PORT STATUS"] == "Disconnected" and onboarded_switch.cli_type.upper() == "VOSS":
                    assert entry[column_name.upper()] == "N/A", \
                        f"{port_name} port is disconnected but transmission mode={transmission_mode} (expected 'N/A')"
                    logger.info(f"Successfully found transmission_mode='N/A' for port_name={port_name}")

        finally:
            self.suite_udk.select_pagination_size("10")
            self.xiq.xflowsmanageDevice360.close_device360_window()

        unsupported_models = ["FabricEngine5520_48SE", "SwitchEngine5520_48SE"]
        switch_model = onboarded_switch.get("model", "")

        if not connected_ports:
            pytest.skip("There are no ports in connected state on the onboarded switch; will skip this test case")
        elif switch_model in unsupported_models:
            pytest.skip(f'Can\'t set half duplex speed on {switch_model} model')
        else:
            connected_ports = connected_ports[:4]
            logger.info(f"Will verify these connected ports: {connected_ports}")
        
            policy_name = self.suite_udk.generate_policy_name()
            self.suite_udk.create_network_policy(policy_name=policy_name)
            
            self.suite_udk.assign_policy(policy_name=policy_name, dut=onboarded_switch)
        
            def func():
                if onboarded_switch.cli_type.upper() == "VOSS":
                    try:
                        self.suite_udk.go_to_device_360_port_config(onboarded_switch)
                    
                        for port in connected_ports:
                            self.suite_udk.enter_port_type_and_vlan_id(port=port, port_type="Auto-sense Port")

                    finally:
                        self.suite_udk.save_device_360_port_config()
                        logger.info("Saved the device360 port configuration.")

                        self.xiq.xflowsmanageDevice360.close_device360_window()
                        logger.info("Closed the device360 window")

                try:
                    self.suite_udk.go_to_device_360_port_config(onboarded_switch)
                    
                    for port in connected_ports:
                        self.suite_udk.enter_port_transmission_mode(port, transmission_mode="Auto")
            
                finally:
                    
                    self.suite_udk.save_device_360_port_config()
                    logger.info("Saved the device360 port configuration.")

                    self.xiq.xflowsmanageDevice360.close_device360_window()
                    logger.info("Closed the device360 window")
                    self.suite_udk.update_and_wait_switch(policy_name=policy_name, dut=onboarded_switch)

                    self.suite_udk.do_onboarding(onboarded_switch, location=onboarding_location)
                    
                    try:
                        self.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(policy=policy_name)
                    except Exception as exc:
                        logger.warning(repr(exc))

            request.addfinalizer(func)

            self.suite_udk.change_device_management_settings(option="disable")

            if onboarded_switch.cli_type.upper() == "VOSS":
                
                logger.info(f"Change {connected_ports} ports from auto-sense to access port")
                try:
                    self.suite_udk.go_to_device_360_port_config(onboarded_switch)
                    
                    for port in connected_ports:
                        logger.info(f"Set vlan 1 for {port} port")
                        self.suite_udk.enter_port_type_and_vlan_id(port=port, port_type="Access Port", access_vlan_id="1")
            
                finally:
                    self.suite_udk.save_device_360_port_config()
                    logger.info("Saved the device360 port configuration.")

                    self.xiq.xflowsmanageDevice360.close_device360_window()
                    logger.info("Closed the device360 window")

            try:
                self.suite_udk.go_to_device_360_port_config(onboarded_switch)
                
                for port in connected_ports:
                    self.suite_udk.enter_port_transmission_mode(port, transmission_mode="Half-Duplex")
        
            finally:
                
                self.suite_udk.save_device_360_port_config()
                logger.info("Saved the device360 port configuration.")

                self.xiq.xflowsmanageDevice360.close_device360_window()
                logger.info("Closed the device360 window")
            
            self.suite_udk.update_and_wait_switch(policy_name=policy_name, dut=onboarded_switch)
            
            try:
                self.suite_udk.go_to_device360(onboarded_switch)

                self.suite_udk.select_max_pagination_size()
            
                ports_table = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()
                for row in ports_table:
                    
                    port_name = row["PORT NAME"]
                    transmission_mode = row["TRANSMISSION MODE"]
                    logger.info(f"Row with 'Port Name'='{port_name}' has '{column_name}'='{transmission_mode}'")
                    
                    if port_name in connected_ports:
                        assert transmission_mode == "Half-Duplex", \
                            f"Expected the transmission mode to be Half-Duplex for '{port_name}' port but found '{transmission_mode}'"
                        logger.info(f"Successfully found transmission_mode='Half-Duplex' for port_name='{port_name}'")
            finally:
                self.suite_udk.select_pagination_size("10")
                self.xiq.xflowsmanageDevice360.close_device360_window()
