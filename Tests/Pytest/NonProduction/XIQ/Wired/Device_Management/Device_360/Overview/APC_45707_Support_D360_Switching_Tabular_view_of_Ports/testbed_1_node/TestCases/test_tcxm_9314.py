# Author:         vstefan
# Description:    To verify if column size can be resized
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9314
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.NonProduction.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase
from selenium.webdriver.common.action_chains import ActionChains


class TCXM9314Tests(xiqBase):

    @pytest.mark.xim_tcxm_9314
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.development       
    @pytest.mark.p2
    @pytest.mark.testbed_1_node
    def test_9314_verify_column_can_be_resized(self, logger, onboarded_switch):
        """  
        Step	Step Description
        1	    Onboard the device
        2	    Navigate to Device360, Monitor, Overview
        3	    Go to the ports table and get its columns
        4	    Get the width of the first column
        5	    Increase the width of the first column with 10px
        6	    Verify the width of the first column is the initial width plus 10px
        7	    Delete the onboarded device and logout from XIQ
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9314'

        for _ in range(3):
            try:
                self.suite_udk.go_to_device360(onboarded_switch)

                ths = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()
                first_column = ths[list(ths)[0]]
                column_name = first_column.text
                initial_width = first_column.size["width"]
                logger.info(f"The width of {column_name} column before resize is {initial_width}px")

                logger.info(f"Increase width of {column_name} column with 10px")
                action = ActionChains(self.cloud_driver)
                action.move_to_element(first_column).move_by_offset(initial_width/2 -1, 0).click_and_hold().move_by_offset(
                    10, 0).release().perform()
                time.sleep(5)

                ths = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()
                first_column = ths[list(ths)[0]]
                final_width = first_column.size["width"]
                logger.info(f"The width of {column_name} column after resize is {final_width}px")
            
                assert initial_width + 10 == final_width
                logger.info("Successfully verified the size of the column increased with 10px")
                
                self.auto_actions.click(self.xiq.xflowsmanageDevice360.dev360.get_device360_refresh_page_button())
                time.sleep(5)
                
                ths = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()
                first_column = ths[list(ths)[0]]
                width_after_refresh = first_column.size["width"]
                
                assert width_after_refresh == initial_width, f"Failed! The width after refreshing Device 360 is " \
                                                            f"{width_after_refresh}px but expected {initial_width}px"
            except Exception as exc:
                logger.info(exc)
            else:
                logger.info(f"Successfully verified the size of the column after refreshing the Device 360 window")
                break
            finally:
                self.xiq.xflowsmanageDevice360.close_device360_window()
        else:
            assert False, "Failed to resize the column"
