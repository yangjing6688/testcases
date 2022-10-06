# Author:         icosmineanu
# Description:    To verify if the port type is shown correctly in the D360 table
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9563
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9563Tests(xiqBase):

    @pytest.mark.tcxm_9563
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_tcxm_9563(self, onboarded_switch):
        """
        Author        : icosmineanu
        Description   : To verify if the port type is shown correctly in the D360 table

        Step            Step Description
         1              Onboard the device
         2              Navigate to Device360, Monitor, Overview
         3              Validate that 'port type' column is not shown in D360 table
         4              Go to column picker, validate that the 'port type' checkbox is not selected and select 'port type' column
         5              Go to D360 table and validate that 'port type' column is shown in D360 table
         6              Get all the entries of the ports table
         7              Verify that each entry has a value set for the 'port type' column('RJ45,'SFP+','SFP-DD')
         8              Check if the port type from XIQ is the same as the one from CLI
         9              Delete the onboarded device and logout from XIQ(Teardown)
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9563'

        dut = onboarded_switch
        is_selected = False
        
        try:
            self.suite_udk.go_to_device360(onboarded_switch)

            self.suite_udk.select_max_pagination_size()

            table_rows = self.suite_udk.get_device360_port_table_rows()
            assert table_rows, "Did not find the rows of the ports table"

            expected_port_type_column = ['Type']

            time.sleep(3)
            found_headers = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_description_table_header()
            print(f"The table has these columns viewable: {found_headers}")

            for column_name in found_headers:
                assert column_name != expected_port_type_column[0].upper(), "Found port type column in the table header"

            checkbox_button = self.xiq.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()
            self.auto_actions.click(checkbox_button)
            time.sleep(3)

            all_checkboxes = self.xiq.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
            columns_found_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
            print(f"These columns are currently found enabled: {columns_found_enabled}")

            for selected_column_name in columns_found_enabled:
                assert selected_column_name != expected_port_type_column, f"Port type checkbox is selected"

            port_type_checkbox = all_checkboxes['Type']['element']
            self.auto_actions.click(port_type_checkbox)

            found_headers = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_description_table_header()
            print(f"The table has these columns viewable: {found_headers}")

            if expected_port_type_column[0].upper() in found_headers:
                print("Successfully found port type column in the table header")
                is_selected = True

            try:
                self.network_manager.connect_to_network_element_name(dut.name)
                self.suite_udk.check_port_type(dut)
            finally:
                self.network_manager.close_connection_to_network_element(dut.name)
            
            time.sleep(3)

        finally:
            
            expected_port_type_column = ['Type']
            
            if is_selected:
                
                checkbox_button = self.xiq.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()
                if not checkbox_button.is_selected():
                    self.auto_actions.click(checkbox_button)
                    time.sleep(3)
            
                all_checkboxes = self.xiq.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
                columns_found_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
                print(f"These columns are currently found enabled: {columns_found_enabled}")

                port_type_checkbox = all_checkboxes['Type']['element']
                self.auto_actions.click(port_type_checkbox)

                for selected_column_name in columns_found_enabled:
                    assert selected_column_name != expected_port_type_column, f"Port type checkbox is selected"

                found_headers = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_description_table_header()
                print(f"The table has these columns viewable: {found_headers}")
                time.sleep(5)
                if expected_port_type_column[0].upper() not in found_headers:
                    print("Port type column is not in the table header")

            else:
                checkbox_button = self.xiq.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()
                if not checkbox_button.is_selected():
                    self.auto_actions.click(checkbox_button)
                    time.sleep(3)
                    
                all_checkboxes = self.xiq.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
                columns_found_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
                print(f"These columns are currently found enabled: {columns_found_enabled}")

                for selected_column_name in columns_found_enabled:
                    assert selected_column_name != expected_port_type_column, f"Port type checkbox is selected"

                found_headers = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_description_table_header()
                print(f"The table has these columns viewable: {found_headers}")
                time.sleep(5)
                if expected_port_type_column[0].upper() not in found_headers:
                    print("Port type column is not in the table header")

            self.suite_udk.select_pagination_size("10")
            
            self.xiq.xflowsmanageDevice360.close_device360_window()
