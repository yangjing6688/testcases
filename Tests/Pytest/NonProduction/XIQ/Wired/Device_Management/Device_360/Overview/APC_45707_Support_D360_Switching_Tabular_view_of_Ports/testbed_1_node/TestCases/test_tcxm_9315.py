# Author:         vstefan
# Description:    To verify by default 10 rows are displayed
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9315
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.NonProduction.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9315Tests(xiqBase):
    
    @pytest.mark.xim_tcxm_9315
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.development       
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_9315_verify_10_rows_are_displayed_by_default(self, logger, onboarded_switch):
        """
        Step	Step Description
        1	    Onboard the device
        2	    Navigate to Device360, Monitor, Overview
        3	    Go to the ports table and get its columns
        4	    Verify the default pagination size is 10
        5	    Verify that in the table there are only 10 entries
        6	    Close Device360
        7	    Verify that in the table there are only 10 entries
        8	    Delete the onboarded device and logout from XIQ
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9315'

        try:
            self.suite_udk.go_to_device360(onboarded_switch)

            table_rows = self.suite_udk.get_device360_port_table_rows()
            assert table_rows, "Did not find the rows of the ports table"
            table_rows[0].location_once_scrolled_into_view

            for row in table_rows:
                logger.info(f"Found this row: {row.text}")

            assert len(table_rows) == 10, f"Error! Expected 10 entries in the ports table but found {len(table_rows)}"
            logger.info("Successfully checked that the ports table has 10 entries")

            paginations = [
                p.text for p in self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()]
            assert paginations, "Failed to find the paginations for Device 360 tabular ports view"
            logger.info(f"Found paginations: {paginations}")

            for pg in paginations:
                
                pg_elem = [p for p in self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()
                           if p.text == pg][0]
                self.auto_actions.click(pg_elem)
                time.sleep(5)
                
                current_pagination_size = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_current_pagination_size() # NOQA
                assert current_pagination_size.text == pg, \
                    f"pagination size is not set to 10; found pagination size: {current_pagination_size}"
            
            pg_size_default = [p for p in self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()
                               if p.text == "10"][0]
            self.auto_actions.click(pg_size_default)
            time.sleep(5)

            table_rows = self.suite_udk.get_device360_port_table_rows()
            assert table_rows, "Did not find the rows of the ports table"
            
            for row in table_rows:
                logger.info(f"Found this row: {row.text}")

            assert len(table_rows) == 10, f"Error! Expected 10 entries in the ports table but found {len(table_rows)}"
            logger.info("Successfully checked that the ports table has 10 entries")
            
            current_pagination_size = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_current_pagination_size() # NOQA
            assert current_pagination_size.text == '10', \
                f"pagination size is not set to 10;found pagination size: {current_pagination_size}"

        finally:
            self.suite_udk.select_pagination_size("10")
            self.xiq.xflowsmanageDevice360.close_device360_window()
