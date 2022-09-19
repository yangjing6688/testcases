# Author:         vstefan
# Description:    To verify if columns can be sorted on clicking on the column name
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9313
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.NonProduction.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9313Tests(xiqBase):
    
    @pytest.mark.xim_tcxm_9313
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.development       
    @pytest.mark.p2
    @pytest.mark.testbed_1_node
    def test_9313_verify_columns_can_be_sorted_by_name(
            self, logger, onboarded_switch, request, setup_lldp, onboarding_location):
        """ 
        Step	Step Description
        1	    Onboard the device
        2	    Navigate to Device360, Monitor, Overview
        3	    Go to the ports table
        4	    Verify that the ports available in this table are the ports also available on the onboarded EXOS/VOSS dut
        5	    Choose the first column (which contains the name of the port)
        6	    Verify that the entries are sorted ascending by default
        7	    Click on the name column
        8	    Verify that the entries are now sorted descending
        9	    Change the 'access vlan' value of some entries of the table
        10	    Choose the 'access vlan' column
        11	    Click on the 'access vlan' column
        12	    Verify that the entries are sorted ascending by default
        13	    Click on the 'access vlan' column
        14	    Verify that the entries are now sorted descending
        15	    Revert the changes for the modified ports
        16	    Delete the onboarded device and logout from XIQ
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9313'

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
        
        port_vlan_mapping = {p: str(int(p) * 25) if onboarded_switch.cli_type.upper() == "EXOS" else str(
            int(p.split("/")[1]) * 25) for p in ports[:4]}
        logger.info(f"port-vlanid mapping {port_vlan_mapping}")

        def func():
            port_type = "Access Port" if onboarded_switch.cli_type.upper() == "EXOS" else "Auto-sense Port"
            access_vlan_id = "1" if onboarded_switch.cli_type.upper() == "EXOS" else None
            
            try:
                self.suite_udk.go_to_device_360_port_config(onboarded_switch)
                
                for port in port_vlan_mapping:
                    self.suite_udk.enter_port_type_and_vlan_id(port=port, port_type=port_type, access_vlan_id=access_vlan_id)

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

        try:
            self.suite_udk.go_to_device_360_port_config(onboarded_switch)
            
            for port, vlan in port_vlan_mapping.items():
                logger.info(f"Set {vlan} vlan for {port} port")
                self.suite_udk.enter_port_type_and_vlan_id(port=port, port_type="Access Port", access_vlan_id=vlan)
            
        finally:
            self.suite_udk.save_device_360_port_config()
            logger.info("Saved the device360 port configuration.")

            self.xiq.xflowsmanageDevice360.close_device360_window()
            logger.info("Closed the device360 window")
        
        self.suite_udk.update_and_wait_switch(policy_name=policy_name, dut=onboarded_switch)
        
        self.suite_udk.verify_vlan_config_on_switch(onboarded_switch, port_vlan_mapping, logger)

        try:
            self.suite_udk.go_to_device360(onboarded_switch)

            self.suite_udk.select_max_pagination_size()

            time.sleep(5)
            
            logger.info("The port names rows should be now in ascending order")
            first_order_rows = [r.text for r in self.suite_udk.get_device360_port_table_rows()]
            first_port_names = [r.split(" ")[0] for r in first_order_rows]
            logger.info(f"Found these port names in the table: {first_port_names}")

            # pop the mgmt port got from xiq d360 because it does not appear in
            # the output of the exos/voss command that shows the available ports
            first_port_names.pop(first_port_names.index("mgmt"))

            assert first_port_names == sorted(first_port_names,
                                              key=lambda x: int(x)
                                              if onboarded_switch.cli_type.upper() == "EXOS" else int(x.split("/")[1])), \
                f"port names are not in ascending order: {first_port_names}"
            logger.info(f"Successfully found the port names in ascending order")

            # the first verification is done for the 'PORT NAME' column of the table
            logger.info(f"Click on the th element with text='PORT NAME' in order to see the ports in descending order")
            self.auto_actions.click(
                self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()['PORT NAME'])

            time.sleep(5)

            logger.info("The port names rows should be now in descending order")
            second_order_rows = [r.text for r in self.suite_udk.get_device360_port_table_rows()]
            second_port_names = [r.split(" ")[0] for r in second_order_rows]
            logger.info(f"Found these port names in the table: {second_port_names}")

            second_port_names.pop(second_port_names.index("mgmt"))
            assert second_port_names == sorted(second_port_names,
                                               key=lambda x: int(x)
                                               if onboarded_switch.cli_type.upper() == "EXOS" else int(x.split("/")[1]),
                                               reverse=True), \
                f"port names are not in descending order: {second_port_names}"
                
            logger.info("Check that the port name entries are completely reversed")
            assert [r.split(" ")[0] for r in second_order_rows] == [r.split(" ")[0] for r in first_order_rows][::-1],\
                "port names are not in ascending order"

        finally:
            self.suite_udk.select_pagination_size("10")
            self.xiq.xflowsmanageDevice360.close_device360_window()

        try:
            
            # the second verification is done for the 'ACCESS VLAN' column of the table
            # voss: auto-sense is enabled by default (ACCESS VLAN on all the ports is set to 'None')
            
            self.suite_udk.go_to_device360(onboarded_switch)
            
            self.suite_udk.select_max_pagination_size()

            table = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()
            initial_order = [int(row["ACCESS VLAN"]) for row in table] if onboarded_switch.cli_type.upper() == "EXOS" else \
                [int(row["ACCESS VLAN"]) for row in table if row["ACCESS VLAN"] != "None"]
            logger.info(f"vlan ids order before clicking on the 'ACCESS VLAN' column: {initial_order}")

            logger.info(f"Verify the vlan is set correctly for each port: {port_vlan_mapping}")
            for port, vlan in port_vlan_mapping.items():
                assert any((row["PORT NAME"] == port) and (row["ACCESS VLAN"] == vlan) for row in table), \
                    f"Did not find an entry in the ports table for vlanid={vlan} and port name={port}"
            
            self.auto_actions.click(
                self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()['ACCESS VLAN'])
            logger.info("The entries in the tabular view should be in ascending order now")
            
            table = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()
            ascending_order = [int(row["ACCESS VLAN"]) for row in table] if onboarded_switch.cli_type.upper() == "EXOS" else\
                [int(row["ACCESS VLAN"]) for row in table if row["ACCESS VLAN"] != "None"]
            assert sorted(initial_order) == ascending_order, \
                f"The entries should be in ascending order but found: {ascending_order}"
            logger.info("Successfully verified the ascending order after pressing once on the 'ACCESS VLAN' column")

            self.auto_actions.click(
                self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()['ACCESS VLAN'])
            logger.info("The entries in the tabular view should be in descending order now")
            
            table = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()
            descending_order = [int(row["ACCESS VLAN"]) for row in table] if onboarded_switch.cli_type.upper() == "EXOS" else\
                [int(row["ACCESS VLAN"]) for row in table if row["ACCESS VLAN"] != "None"]
            assert sorted(initial_order, reverse=True) == descending_order, \
                f"The entries should be in descending order but found: {descending_order}"
            logger.info(
                "Successfully verified the descending order after presedonce again on the 'ACCESS VLAN' column")
            
        finally:
            self.suite_udk.select_pagination_size("10")
            self.xiq.xflowsmanageDevice360.close_device360_window()
