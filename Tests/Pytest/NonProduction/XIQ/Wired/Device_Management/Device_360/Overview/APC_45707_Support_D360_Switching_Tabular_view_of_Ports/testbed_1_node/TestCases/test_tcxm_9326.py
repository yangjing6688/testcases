# Author:         scostache
# Description:    Configure and check Trunk Vlan Ports are displayed in Device360 Tabular View.
#                 Then change to default Access Type and then back to Auto-Sense
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9326
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.NonProduction.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9326Tests(xiqBase):
    
    @pytest.mark.xim_tcxm_9326
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.development
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_tcxm_9326(self, request, onboarded_switch, onboarding_location, logger, setup_lldp):
        """ 
        Step	Step Description
        1	    Onboard the device
        2	    Create Network Policy
        3	    Add Switch Template to Network Policy
        4	    Assign Network Policy to DUT
        5	    Update DUT
        6	    Go to Device360, Configure, Port Configuration
        7	    Select at least 10 ports from tabular view, no mgmt. Save ports in a list
        8	    Change port type to tagging and allowed VLANs from format "vlanid-vlanid,vlanid"
        9	    Update DUT
        10	    Navigate to Device360
        11	    Check ports from initial port list for same vlans and port type
        12	    Change port type to access for all ports in list
        13	    Update DUT
        14	    Navigate to Device360
        15	    Check ports from initial port list for same vlans and port type
        16	    Revert ports to default AutoSense
        17	    Setup CleanUp
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9326'

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

        trunk_ports = ports[:10]
        logger.info(f"Trunk ports: {trunk_ports}")

        access_ports = ports[10:12]
        logger.info(f"Access ports: {access_ports}")
        
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
                    
                for port in trunk_ports + access_ports:
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
            self.suite_udk.go_to_device_360_port_config(onboarded_switch)

            for port in access_ports:
                temp_vlan = self.suite_udk.generate_vlan_id()
                logger.info(f"Set {temp_vlan} vlan for {port} port")
                self.suite_udk.enter_port_type_and_vlan_id(
                    port=port, port_type="Access Port", access_vlan_id=temp_vlan)
            
        finally:
            self.suite_udk.save_device_360_port_config()
            logger.info("Saved the device360 port configuration.")

            self.xiq.xflowsmanageDevice360.close_device360_window()
            logger.info("Closed the device360 window")

        self.suite_udk.update_and_wait_switch(policy_name=policy_name, dut=onboarded_switch)
        
        for _ in range(7):
            try:
                self.suite_udk.go_to_device360(onboarded_switch)
                
                self.suite_udk.select_max_pagination_size()
            
                ports_table = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()

                for row in ports_table:
            
                    port_name = row["PORT NAME"]
                    port_mode = row[column_name.upper()]
                    
                    if port_name in trunk_ports:
                        assert port_mode == "Trunk", f"Expected port_mode='Trunk' but found '{port_mode}' for port_name='{port_name}'"
                        logger.info(f"Successfully verified {port_name} port is in Trunk port mode")
            
            except Exception as exc:
                logger.warning(repr(exc))
                time.sleep(60)
            else:
                break
            finally:
                self.suite_udk.select_pagination_size("10")
                self.xiq.xflowsmanageDevice360.close_device360_window()
        else:
            assert False, "Failed to very the port configuration"
