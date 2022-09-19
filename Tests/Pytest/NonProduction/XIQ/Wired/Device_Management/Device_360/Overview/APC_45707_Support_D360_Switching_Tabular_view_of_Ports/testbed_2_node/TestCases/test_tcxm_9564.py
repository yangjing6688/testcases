# Author:         gburlacu
# Description:    To verify if LACP Status is shown correctly in D360 table
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9564
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
#                 This test case needs a testbed yaml with two devices.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.NonProduction.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_2_node.Resources.testcase_base import xiqBase


class TCXM9564Tests(xiqBase):

    @pytest.mark.xim_tcxm_9564
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.development
    @pytest.mark.p2
    @pytest.mark.testbed_2_node
    def test_9564_lacp_status(self, logger, onboarded_2_switches):
        """
        Step	Step Description
        1	    Onboard 2 devices
        2	    Navigate to Device360, Monitor, Overview for the first device
        3	    Verify if LACP Status for isl.port_a is false
        4	    Exit Device360
        5	    CLI: Modify LACP Status for both devices for each isl.port_a
        6	    CLI: Bounce both devices
        7	    Navigate to Device360, Monitor, Overview for the first device
        8	    Verify if LACP Status for isl.port_a is true
        9	    CLI: Cleanup for both devices regarding LACP configuration made at step 5
        10	    Exit Device360 and Logout
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9564'

        dut1, dut2 = onboarded_2_switches
        port_device_1 = dut1.isl.port_a.ifname
        port_device_2 = dut2.isl.port_a.ifname
        mlt = 70
        key = 7
   
        self.suite_udk.bounce_device(self.xiq, dut1)
        self.suite_udk.bounce_device(self.xiq, dut2)
        
        self.suite_udk.verify_lacp_status_for_port_device_in_360_table(
            self.xiq, dut1, logger, port_device_1, 'false')
        
        try:
            
            logger.info(f"Modify lacp for device 1 port {port_device_1}")
            self.suite_udk.set_lacp(dut1, mlt, key, port_device_1)
            time.sleep(2)

            logger.info(f"Modify lacp for device 2 port {port_device_2}")
            self.suite_udk.set_lacp(dut2, mlt, key, port_device_2)
            time.sleep(20)

            logger.info("Bounce device 2")
            self.suite_udk.bounce_device(self.xiq, dut2)

            logger.info("Bounce device 1")
            self.suite_udk.bounce_device(self.xiq, dut1)
            time.sleep(5)

            self.suite_udk.verify_lacp_status_for_port_device_in_360_table(
                self.xiq, dut1, logger, port_device_1, 'true')
        
        finally:
            
            logger.info("Cleanup")
            self.suite_udk.cleanup_lacp(dut1, mlt, port_device_1)
            time.sleep(3)
            self.suite_udk.cleanup_lacp(dut2, mlt, port_device_2)
