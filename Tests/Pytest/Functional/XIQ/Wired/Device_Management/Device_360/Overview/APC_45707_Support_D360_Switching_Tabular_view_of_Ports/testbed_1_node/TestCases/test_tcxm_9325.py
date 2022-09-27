# Author:         vstefan
# Description:    To verify if tabular view displays port mode column
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9325
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9325Tests(xiqBase):

    @pytest.mark.tcxm_9325
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_9325_verify_port_mode_column(self, logger, onboarded_switch, request, setup_lldp, onboarding_location):
        """ 
        Step	Step Description
        1	    Onboard the device
        2	    Navigate to Device360, Monitor, Overview
        3	    Go to the ports table and get its columns
        4	    Verify the 'port mode' column is selected in the column picker
        5	    Get all the entries of the ports table
        6	    Verify that default values of the 'port mode' field for all the ports
        7	    Add a few ports in different access and trunk VLANs
        8	    Verify that the changes done above are now updated in the tabular view
        9	    Revert the changes that were added at step 7
        10	    Delete the onboarded device and logout from XIQ
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9325'

        column_name = "Port Mode"

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

            assert column_name in columns_found_enabled, f"Failed! {column_name} column is not already visible"
            logger.info(f"{column_name} column is already visible")
                
            ports_table = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()

            for entry in ports_table:
                
                assert column_name.upper() in entry, f"Failed to find {column_name} column in table row: {entry}"

                port_mode = entry[column_name.upper()] 
                port_name = entry['PORT NAME']
                logger.info(
                    f"Row with 'Port Name'='{port_name}' has '{column_name}'='{entry[column_name.upper()]}'")
            
        finally:
            self.suite_udk.select_pagination_size("10")
            self.xiq.xflowsmanageDevice360.close_device360_window()

        ports = sorted(
        self.suite_udk.get_ports_from_dut(onboarded_switch),
            key=int if onboarded_switch.cli_type.upper() == "EXOS" else (lambda x: int(x.split("/")[1]))
        )
        logger.info(f"Found these ports available on switch: {ports}")
        
        self.suite_udk.change_device_management_settings(
            option="disable", platform=onboarded_switch.cli_type.upper())

        policy_name = self.suite_udk.generate_policy_name()
        self.suite_udk.create_network_policy(policy_name=policy_name)
        
        self.suite_udk.assign_policy(policy_name=policy_name, dut=onboarded_switch)

        trunk_ports = ports[:2]
        logger.info(f"Trunk ports: {trunk_ports}")
        
        port_vlan_mapping = {p: str(int(p) * 25) if onboarded_switch.cli_type.upper() == "EXOS" else str(
            int(p.split("/")[1]) * 25) for p in ports[2:6]}
        logger.info(f"port-vlanid mapping: {port_vlan_mapping}")
    
        def func():
            
            port_type = "Access Port" if onboarded_switch.cli_type.upper() == "EXOS" else "Auto-sense Port"
            access_vlan_id = "1" if onboarded_switch.cli_type.upper() == "EXOS" else None

            if onboarded_switch.cli_type.upper() == "VOSS":
                
                try:
                    self.suite_udk.go_to_device_360_port_config(onboarded_switch)
                    
                    for port in trunk_ports:
                        self.suite_udk.enter_port_type_and_vlan_id(port=port, port_type="Access Port")
                
                finally:
                    
                    self.suite_udk.save_device_360_port_config()
                    logger.info("Saved the device360 port configuration.")

                    self.xiq.xflowsmanageDevice360.close_device360_window()
                    logger.info("Closed the device360 window")
            
                self.suite_udk.update_and_wait_switch(policy_name=policy_name, dut=onboarded_switch)
            
            try:
                self.suite_udk.go_to_device_360_port_config(onboarded_switch)
                    
                for port in list(port_vlan_mapping) + trunk_ports:
                    self.suite_udk.enter_port_type_and_vlan_id(
                        port=port, port_type=port_type, access_vlan_id=access_vlan_id)
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
                print(repr(exc))

        request.addfinalizer(func)

        try:
            self.suite_udk.go_to_device_360_port_config(onboarded_switch)
            
            for port, vlan in port_vlan_mapping.items():
                logger.info(f"Set {vlan} vlan for {port} port")
                self.suite_udk.enter_port_type_and_vlan_id(port=port, port_type="Access Port", access_vlan_id=vlan)
            
            for port in trunk_ports:
                logger.info(f"Set {port} port as Trunk Port")
                self.suite_udk.enter_port_type_and_vlan_id(port=port, port_type="Trunk Port")

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
                port_mode = row[column_name.upper()]
                
                if port_name in port_vlan_mapping:
                    
                    assert port_mode == "Access", f"Expected port_mode='Access' but found '{port_mode}' for port_name='{port_name}'"
                    logger.info(f"Successfully verified {port_name} port is in Access port mode")
                    
                    assert row["ACCESS VLAN"] == port_vlan_mapping[port_name], \
                        f"Expected vlanid={port_vlan_mapping[port_name]} but found {row['ACCESS VLAN']} for {port_name} port"
                    logger.info(f"Successfully found vlanid='{port_vlan_mapping[port_name]}' for {port_name} port")
                
                elif port_name in trunk_ports:
                    assert port_mode == "Trunk", f"Expected port_mode='Trunk' but found '{port_mode}' for port_name='{port_name}'"
                    logger.info(f"Successfully verified {port_name} port is in Trunk port mode")
        
        finally:
            self.suite_udk.select_pagination_size("10")
            self.xiq.xflowsmanageDevice360.close_device360_window()
