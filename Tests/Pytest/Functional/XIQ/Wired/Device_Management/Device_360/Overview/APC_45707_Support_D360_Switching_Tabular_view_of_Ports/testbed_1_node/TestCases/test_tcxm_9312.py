# Author:         vstefan
# Description:    To verify if columns can be shown or hided by selecting in column picker
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9312
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9312Tests(xiqBase):

    @pytest.mark.tcxm_9312
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p2
    @pytest.mark.testbed_1_node
    def test_9312_verify_column_picker_usage(self, request, logger, onboarded_switch):
        """ 
        Step	Step Description
        1	    Onboard the device
        2	    Navigate to Device360, Monitor, Overview
        3	    Go to the ports table
        4	    Verify that the columns coresponding to the checkboxes that are selected in the column picker are visible in the header of the table
        5	    Click on each checkbox of the column picker
        6	    Verify that the columns coresponding to the checkboxes that are selected in the column picker are visible in the header of the table
        7	    Delete the onboarded device and logout from XIQ
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9312'

        self.suite_udk.go_to_device360(onboarded_switch)

        checkbox_button = self.xiq.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()
        checkbox_button.location_once_scrolled_into_view
        self.auto_actions.click(checkbox_button)
        time.sleep(3)

        all_checkboxes = self.xiq.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
        default_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
        logger.info(f"These columns are enabled by default: {default_enabled}")
        
        default_disabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is False]
        logger.info(f"These columns are disabled by default: {default_disabled}")

        found_headers = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_description_table_header()
        logger.info(f"The table has these columns viewable: {found_headers}")

        for checkbox_name, stats in all_checkboxes.items():
            is_selected = stats["is_selected"]

            if is_selected:
                assert any(checkbox_name.upper() == header.upper() for header in found_headers), \
                    f"Did not find this column in the table header: {checkbox_name}"
            else:
                assert not any(checkbox_name.upper() == header.upper() for header in found_headers), \
                    f"Found this column in the table header which is not expected: {checkbox_name}"
        
        def func():
            
            all_checkboxes = self.xiq.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
            
            for checkbox_name, stats in all_checkboxes.items():
                if any([
                    (checkbox_name in default_enabled) and (stats["is_selected"] is False),
                    (checkbox_name in default_disabled) and (stats["is_selected"] is True)
                ]):
                    self.auto_actions.click(stats["element"])

            self.auto_actions.click(self.xiq.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button())
            self.xiq.xflowsmanageDevice360.close_device360_window()
            time.sleep(3)
        request.addfinalizer(func)

        logger.info("Press each checkbox")
        for stats in all_checkboxes.values():
            self.auto_actions.click(stats["element"])
        time.sleep(3)

        all_checkboxes = self.xiq.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
        found_headers = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_description_table_header()
        logger.info(f"The table has these columns viewable: {found_headers}")

        for checkbox_name, stats in all_checkboxes.items():
            is_selected = stats["is_selected"]
            
            if checkbox_name in default_enabled:
                assert is_selected is False, f"{checkbox_name} checkbox should be disabled"
                assert not any(checkbox_name.upper() == header.upper() for header in found_headers), \
                    f"Found this column in the table header which is not expected: {checkbox_name}"
            elif checkbox_name in default_disabled:
                assert is_selected is True, f"{checkbox_name} checkbox should be enabled"
                assert any(checkbox_name.upper() == header.upper() for header in found_headers),  \
                    f"Did not find this column in the table header: {checkbox_name}"
