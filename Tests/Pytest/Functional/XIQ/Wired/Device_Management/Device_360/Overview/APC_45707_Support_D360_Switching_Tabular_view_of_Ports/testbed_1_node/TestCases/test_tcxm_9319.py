# Author:         bmureseanu
# Description:    To verify if LLDP Neighbor column is present in D360 overview table
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9319
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9319Tests(xiqBase):

    @pytest.mark.tcxm_9319
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_9319_verify_lldp_neighbor_column(self, onboarded_switch):
        """
        Step	Step Description
        1	    Onboard the device
        2	    Navigate to Device360, Monitor, Overview
        3	    Verify if LLDP Neighbor column is present
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9319'

        self.suite_udk.go_to_device360(onboarded_switch)

        if self.xiq.xflowsmanageDevice360.dev360.get_d360_monitor_lldp_neighbor_header() is None:
            self.xiq.xflowsmanageDevice360.close_device360_window()
            pytest.fail("Missing LLDP Neighbor column")

        self.xiq.xflowsmanageDevice360.close_device360_window()
