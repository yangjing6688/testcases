# Author:         asterian
# Description:    To verify that port details of slot 1 is displayed by default
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9329
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS stack should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable only for the EXOS stack devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_stack.Resources.testcase_base import xiqBase


class TCXM9329Tests(xiqBase):

    @pytest.mark.tcxm_9329
    @pytest.mark.stack
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_9329_verify_default_port_details(self, logger, onboarded_stack):
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9329'
        
        try:
            self.suite_udk.go_to_device360(onboarded_stack)
            self.suite_udk.verify_port_names(logger)

            try:
                self.network_manager.connect_to_network_element_name(onboarded_stack.name)
                master_slot = self.suite_udk.get_master_slot(onboarded_stack)
                self.devCmd.send_cmd(onboarded_stack.name, 'reboot slot '+str(master_slot), max_wait=10, interval=2,
                                    confirmation_phrases='(y - save and reboot, n - reboot without save, <cr> - cancel command)',
                                    confirmation_args='y')
            finally:
                self.network_manager.close_connection_to_network_element(onboarded_stack.name)

            time.sleep(10)
            self.xiq.xflowsmanageDevice360.close_device360_window()
            time.sleep(5)

            self.suite_udk.go_to_device360(onboarded_stack)
            self.suite_udk.verify_port_names(logger)

        finally:
            self.xiq.xflowsmanageDevice360.close_device360_window()
