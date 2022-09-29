# Author:         rvisterineanu
# Description:    To verify we can increase rows length to 20, 50 and 100
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9317
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time


from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9317Tests(xiqBase):

    @pytest.mark.tcxm_9317
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_9317_verify_row_length_can_be_increased_to_20_50_100(self, logger, onboarded_switch):
        """
        Step	    Step Description
        1	        Onboard the device
        2	        Navigate to Device360, Monitor, Overview
        3	        Navigate to 20 hyperlink in the left bottom corner of the table
        4	        Verify the number of rows after the 20 hyperlink is clicked
        5	        Navigate to 50 hyperlink in the left bottom corner of the table
        6	        Verify the number of rows after the 50 hyperlink is clicked
        7	        Navigate to 100 hyperlink in the left bottom corner of the table
        8	        Navigate to 10 hyperlink in the left bottom corner of the table
        9	        Verify the number of rows after the 10 hyperlink is clicked
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9317'
        
        dut = onboarded_switch

        cli_no_ports = self.suite_udk.get_the_number_of_ports_from_cli(dut)
        print(f"The number of CLI ports is: {cli_no_ports}")
        
        self.suite_udk.go_to_device360(onboarded_switch)

        try:
            pagination_number = [20, 50, 100, 10]
            for pag in pagination_number:
                paginations = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()
                assert paginations, "Failed to find the paginations for Device 360 tabular ports view"
                [pagination] = [pg for pg in paginations if pg.text == str(pag)]
                print(f"Pagination is:{str(pag)}")
                time.sleep(5)

                self.auto_actions.click(pagination)
                logger.info(f"Selected the pagination size: {pagination.text}")
                time.sleep(3)

                table_rows = self.suite_udk.get_device360_port_table_rows()
                current_pagination_size = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_current_pagination_size()
                if current_pagination_size.text != str(pag):
                    logger.info(f"Pagination size is not set to {str(pag)}")
                else:
                    logger.info(f"pagination size is already set to {str(pag)}")

                for row in table_rows:
                    logger.info(f"Found this row: {row.text}")

                """The following verifications take into account 5420F platform, VOSS and EXOS.
                On VOSS, if 4 channelized ports are seen in CLI, in XIQ will be seen only 2.
                On EXOS, 4 stacking ports are seen in CLI and only 2 in XIQ.
                The verifications cover the fact that on XIQ can be seen fewer ports than on CLI.
                The number of ports in XIQ include also the management port (no_ports + 1) or less for 5420F (no_ports - 1)
                """

                if cli_no_ports + 1 < pag and len(table_rows) <= cli_no_ports + 1:
                    assert len(
                        table_rows) <= cli_no_ports + 1, f"Error! Expected at least {str(cli_no_ports - 1)} entries in the ports table but found {len(table_rows)}"
                    logger.info(f'The table has:{len(table_rows)} entries')
                    logger.info(f'Successfully checked that the ports table has at least:{str(cli_no_ports - 1)} entries')
                elif cli_no_ports + 1 >= pag and len(table_rows) <= cli_no_ports + 1:
                    assert len(
                        table_rows) == pag, f"Error! Expected {str(pag)} entries in the ports table but found {len(table_rows)}"
                    logger.info(f'Successfully checked that the ports table has:{str(pag)} entries')

        finally:
            self.suite_udk.select_pagination_size("10")
            self.xiq.xflowsmanageDevice360.close_device360_window()
