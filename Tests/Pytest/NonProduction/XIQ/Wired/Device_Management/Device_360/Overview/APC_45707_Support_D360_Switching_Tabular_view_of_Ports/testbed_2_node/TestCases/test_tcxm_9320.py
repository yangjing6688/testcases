# Author:         sraescu
# Description:    To verify that LLDP column displays the sysname with hyperlink
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9320
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
#                 This test case needs a testbed yaml with two devices.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time


from Tests.Pytest.NonProduction.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_2_node.Resources.testcase_base import xiqBase


class TCXM9320Tests(xiqBase):

    @pytest.mark.xim_tcxm_9320
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.development
    @pytest.mark.p1
    @pytest.mark.testbed_2_node
    def test_9320_verify_LLDP_column_in_ports_table(self, logger, onboarded_2_switches, onboarding_location):
        """
        Step	        Step Description
        1	            Onboard two devices
        2	            For one device navigate to Device360, Monitor, Overview
        3	            Verify if LLDP NEIGHBOR column displays the sysname with hyperlink on all ports connected to
                        the onboarded neighbor device as configured in yaml file
        4	            Delete the onboarded neighbor device from XIQ
        5	            Verify if LLDP NEIGHBOR column displays the sysname without hyperlink on all ports connected to
                        the neighbor device as configured in yaml file
        6	            Exit Device360, delete the remaining device from XIQ and logout
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9320'

        dut1, dut2 = onboarded_2_switches
                   
        isl_ports = self.suite_udk.get_isl_ports(dut1.isl)
        
        if len(isl_ports) < 1:
            pytest.skip(
                "****This testcase doesn't run on single node testbed, it needs at least two nodes for execution. "
                "Hence skipping test****")

        logger.info("Wait for LLDP NEIGHBORS column to be updated before to start the test (bounce IQAgent)")
        self.suite_udk.bounce_device(self.xiq, dut1)
        self.suite_udk.bounce_device(self.xiq, dut2)
        time.sleep(5)

        try:
            self.suite_udk.go_to_device360(dut1)

            self.suite_udk.select_max_pagination_size()

            logger.info("Verify if LLDP NEIGHBOR column displays the sysname with hyperlink on all ports connected to "
                        "the onboarded neighbor device as configured in yaml file")
            self.suite_udk.check_device360_LLDP_neighbors_with_hyperlink(isl_ports)

        finally:
            self.suite_udk.select_pagination_size("10")
            self.xiq.xflowsmanageDevice360.close_device360_window()
            time.sleep(5)

        try:
            logger.info("Delete the onboarded neighbor device from XIQ")
            self.xiq.xflowscommonDevices.delete_device(device_serial=dut2.serial)
            time.sleep(5)

            self.suite_udk.go_to_device360(dut1)

            self.suite_udk.select_max_pagination_size()

            logger.info("Verify if LLDP NEIGHBOR column displays the sysname without hyperlink on all ports connected to "
                        "the neighbor device as configured in yaml file")
            self.suite_udk.check_device360_LLDP_neighbors_without_hyperlink(isl_ports)

        finally:
            self.suite_udk.select_pagination_size("10")
            self.xiq.xflowsmanageDevice360.close_device360_window()

            time.sleep(5)
            assert self.xiq.xflowsmanageSwitch.onboard_switch(
                dut2.serial, device_os=dut2.cli_type, location=onboarding_location) == 1, \
                    f"Failed to onboard this dut to XiQ: {dut2}"

            self.xiq.xflowscommonDevices.wait_until_device_online(dut2.serial)
            res = self.xiq.xflowscommonDevices.get_device_status(device_serial=dut2.serial)
            assert res == 'green', f"The device did not come up successfully in the XIQ; Device: {dut2}"
