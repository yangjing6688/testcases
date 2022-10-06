# Author:         vstefan
# Description:    To verify if table is having Port Name, Type, LLDP Neighbor,
#                 LACP status, Port Status, Transmission mode, Port Mode, Access VLAN, 
#                 Tagged VLAN,Traffic Received (Rx), Traffic Transmitted (Rx), 
#                 Power Used, Port Speed as default column
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9311
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9311Tests(xiqBase):

    @pytest.mark.tcxm_9311
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_9311_verify_default_columns_in_ports_table(self, logger, onboarded_switch):
        """ 
       Step	    Step Description
        1	    Onboard the device
        2	    Navigate to Device360, Monitor, Overview
        3	    Go to the ports table
        4	    Verify that only the expected columns are selected in the column picker
        5	    Get the columns from the ports table
        6	    Verify the found columns are the ones specified in the title of the test case
        7	    Refresh the page
        8	    Verify that only the expected columns are selected in the column picker
        9	    Get the columns from the ports table
        10	    Verify the found columns are the ones specified in the title of the test case
        11	    Delete the onboarded device and logout from XIQ
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9311'

        self.suite_udk.go_to_device360(onboarded_switch)

        try:

            expected_default_columns = [
                'Port Name', 'LLDP Neighbor', 'Port Status', 'Transmission Mode', 'Port Mode',
                'Access VLAN', 'Tagged VLAN(s)', 'Traffic Received (Rx)', 'Traffic Transmitted (Tx)', 
                'Power Used', 'Port Speed'
            ]
            
            if onboarded_switch.cli_type.upper() == "EXOS":
                expected_default_columns.extend(
                    [
                        'ELRP Enabled VLAN(s)',
                        'MAC Locking'
                    ]
                )

            for _ in range(2):
                checkbox_button = self.xiq.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()
                checkbox_button.location_once_scrolled_into_view
                self.auto_actions.click(checkbox_button)
                time.sleep(3)

                all_checkboxes = self.xiq.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
                columns_found_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
                logger.info(f"These columns are currently found enabled: {columns_found_enabled}")
                
                assert sorted(expected_default_columns) == sorted(columns_found_enabled), \
                    "Did not find all the expected columns enabled"
                logger.info(f"Successfully found all the expected columns enabled: {expected_default_columns}")

                found_headers = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_description_table_header()
                logger.info(f"The table has these columns viewable: {found_headers}")
                
                assert len(found_headers) == len(expected_default_columns), \
                    "Failed! More columns visible than checkbox enabled"

                for column_name in expected_default_columns:
                    assert any(column_name.upper() == header.upper() for header in found_headers), \
                        f"Did not find this column in the table header: {column_name.upper()}"
                    logger.info(f"Successfully verified this column is visible in table: {column_name}")
                
                self.auto_actions.click(self.xiq.xflowsmanageDevice360.dev360.get_device360_refresh_page_button())
                time.sleep(5)

        finally:
            self.xiq.xflowsmanageDevice360.close_device360_window()
