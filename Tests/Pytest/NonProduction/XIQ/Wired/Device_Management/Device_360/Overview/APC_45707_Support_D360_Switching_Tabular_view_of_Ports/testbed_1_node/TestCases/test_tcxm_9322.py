# Author:         Marius Chelu
# Description:    Tests if left clicking on each port icon in the graphical representation from Device
#                 360 window have the correct port details.
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9322
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.NonProduction.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9322Tests(xiqBase):

    @pytest.mark.xim_tcxm_9322
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.development
    @pytest.mark.testbed_1_node
    def test_tcxm_9322(self, onboarded_switch):
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9322'

        try:
            self.network_manager.connect_to_network_element_name(onboarded_switch.name)
            no_of_ports = len(self.suite_udk.get_port_list_from_dut(onboarded_switch))
        finally:
            self.network_manager.close_connection_to_network_element(onboarded_switch.name)
                
        print(f'Number of ports for this switch is {no_of_ports}')
        
        self.suite_udk.go_to_device360(onboarded_switch)

        try:
            for i in range(1, no_of_ports):
                
                for _ in range(4):
                    try:
                        port_icon_present = self.xiq.xflowsmanageDevice360.dev360.get_device360_ah_icon(i)
                        if port_icon_present:
                            
                            if port_icon_present.get_attribute("data-automation-tag") == "automation-port-console":
                                break

                            self.xiq.xflowsmanageDevice360.device360_left_click_on_port_icon(i)
                            port_no = self.suite_udk.list_port_element(self.xiq, i)
                            assert port_no == 1, 'Port details missing'
                        else:
                            print(f'Port {i} is not displayed on the graphical representation of the DUT!')
                    except Exception as exc:
                        print(exc)
                        time.sleep(5)
                    else:
                        break
                else:
                    assert False, "Failed: Port details missing"
        finally:
            self.xiq.xflowsmanageDevice360.close_device360_window()
