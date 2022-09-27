# Author:         vstefan
# Description:    To verify if columns can be moved in the table
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9316
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9316Tests(xiqBase):

    @pytest.mark.tcxm_9316
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p2
    @pytest.mark.testbed_1_node
    def test_9316_verify_columns_can_be_moved(self, logger, onboarded_switch):
        """
        Step	Step Description
        1	    Onboard the device
        2	    Navigate to Device360, Monitor, Overview
        3	    Go to the ports table
        4	    Get the first two columns of the table
        5	    Switch the order of the first two column
        6	    Verify that the order of the frst two column switched
        7	    Refresh Device360
        8	    Verify that the order of the frst two column switched back to the initial state
        9	    Delete the onboarded device and logout from XIQ
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9316'

        try:
            
            self.suite_udk.go_to_device360(onboarded_switch)
                
            for _ in range(3):
                try:

                    ths = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()

                    first_column, second_column = ths[list(ths)[0]], ths[list(ths)[1]]
                    first_column_width = first_column.size.get("width")
                    first_column_name_before_moving = first_column.text
                    logger.info(f"The first column before moving: {first_column_name_before_moving}")

                    second_column_name_before_moving = second_column.text
                    logger.info(f"The second column before moving: {second_column_name_before_moving}")

                    second_column_width = second_column.size.get('width')
                    offset_x = first_column_width + second_column_width - 20
                    logger.info(f"Move first column {first_column_name_before_moving} with {offset_x}px")
                    self.auto_actions.click_and_hold_element(first_column, offset_value=offset_x)
                    
                    time.sleep(5)

                    ths = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()

                    first_column, second_column = ths[list(ths)[0]], ths[list(ths)[1]]
                    first_column_name_after_moving = first_column.text
                    logger.info(f"The first column after moving: {first_column_name_after_moving}")

                    second_column_name_after_moving = second_column.text
                    logger.info(f"The second column after moving: {second_column_name_after_moving}")

                    assert first_column_name_before_moving == second_column_name_after_moving, \
                        "First column before moving is not equal with the second column after moving"
                    assert second_column_name_before_moving == first_column_name_after_moving, \
                        "Second column before moving is not equal with the first column after moving"
                    logger.info("Succesfully verified that the columns changed their positions")
                except AssertionError as exc:
                    logger.info(exc)
                else:
                    break
            else:
                assert False, f"Failed to move the {first_column_name_before_moving} column"

            self.auto_actions.click(self.xiq.xflowsmanageDevice360.dev360.get_device360_refresh_page_button())
            time.sleep(5)
            
            ths = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()

            first_column, second_column = ths[list(ths)[0]], ths[list(ths)[1]]
            first_column_name_after_refresh = first_column.text
            logger.info(f"The first column after refresh: {first_column_name_after_refresh}")

            second_column_name_after_refresh = second_column.text
            logger.info(f"The second column after refresh: {second_column_name_after_refresh}")
            
            assert first_column_name_after_refresh == first_column_name_before_moving, \
                "The first column after refresh is not equal with the first one before moving"
            assert second_column_name_after_refresh == second_column_name_before_moving, \
                "The seconds column after refresh is not equal with the second one before moving"

        finally:
            self.xiq.xflowsmanageDevice360.close_device360_window()
