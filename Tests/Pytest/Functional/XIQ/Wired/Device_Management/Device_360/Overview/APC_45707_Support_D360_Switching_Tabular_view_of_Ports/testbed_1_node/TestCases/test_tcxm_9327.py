# Author:         vstefan
# Description:    To verify if table includes mgmt port details
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9327
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time
import re

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9327Tests(xiqBase):

    @pytest.mark.tcxm_9327
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_9327_verify_mgmt_port_details(self, logger, onboarded_switch):
        """
        Step	Step Description
        1	    Onboard the device
        2	    Navigate to Device360, Monitor, Overview
        3	    Skip the test case if the onboarded device has platform  EXOS X435 or  5320 UHW
        4	    Go to the ports table and get its columns
        5	    Set the pagination size to 10
        6	    Go through all the pages til the entry of the management port is visible
        7	    Set the pagination size to 20
        8	    Go through all the pages til the entry of the management port is visible
        9	    Set the pagination size to 50
        10	    Go through all the pages til the entry of the management port is visible
        11	    Set the pagination size to 100
        12	    Go through all the pages til the entry of the management port is visible
        13	    Delete the onboarded device and logout from XIQ
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9327'

        unsupported_platforms = ["X435", "5320 UHW"]
        dut_platform = onboarded_switch.get("platform", "")

        if any(re.search(dut_platform, platform) for platform in unsupported_platforms):
            pytest.skip(f"The switch platform is {onboarded_switch['platform']} and it is not supported; skipping the test case;\nunsupported platforms: {unsupported_platforms}")

        try:
            self.suite_udk.go_to_device360(onboarded_switch)
            
            paginations_size = [
                pg.text for pg in self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()]
            
            for pg_size_number in paginations_size:
                
                logger.info(f"Current pagination size is {pg_size_number}")
            
                self.suite_udk.select_pagination_size(pg_size_number)

                for i in range(1, 99):

                    try:
                        rows = self.suite_udk.get_device360_port_table_rows()
                        if any(
                            re.search("mgmt.*Management", row.text) for row in rows):
                            logger.info(f"Successfully found the management port in current page {i}")
                            time.sleep(3)
                            break
                        else:
                            logger.info(f"Did not find the management port in the current page: {i}")
                        
                        next_page_button = self.xiq.xflowsmanageDevice360.dev360.get_device360_pagination_next_button()
                        assert next_page_button, f"Did not find the next page button (current page is {i})"
                        self.auto_actions.click(next_page_button)
                        time.sleep(3)

                    except AssertionError as exc:
                        assert False, f"No page left to check: {repr(exc)}"
        finally:
            self.suite_udk.select_pagination_size("10")
            self.xiq.xflowsmanageDevice360.close_device360_window()
