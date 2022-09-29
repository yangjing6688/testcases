# Author:         arebega
# Description:    To verify if table is displayed in D360 > monitor > Overview
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9310
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9311Tests(xiqBase):

    @pytest.mark.tcxm_9310
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_9310_verify_default_columns_in_ports_table(self, onboarded_switch):
        """
        Step	    Step Description
        1	        Onboard the device
        2	        Navigate to Device360, Monitor, Overview
        3	        Go to the ports table
        4           Verify the rows of the table can be retrieved
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9310'

        try:
            self.suite_udk.go_to_device360(onboarded_switch)

            table_rows = self.xiq.xflowsmanageDevice360.get_device360_port_table_rows()
            assert table_rows, "Did not find the rows of the ports table"

        finally:
            self.xiq.xflowsmanageDevice360.close_device360_window()
