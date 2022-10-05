# Author:         gonoleata
# Description:    To verify if the port status is shown correctly in the D360 table
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9565
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9565Tests(xiqBase):

    @pytest.mark.tcxm_9565
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_9565_check_ports_status(self, logger, onboarded_switch):
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9565'

        self.suite_udk.bounce_IQAgent(onboarded_switch)

        try:
            self.network_manager.connect_to_network_element_name(onboarded_switch.name)
            cli_ports_status = self.suite_udk.get_device_port_status(devCmd=self.devCmd, dut=onboarded_switch)
        finally:
            self.network_manager.close_connection_to_network_element(onboarded_switch.name)

        if cli_ports_status is None:
            pytest.fail('cli_ports_status=None')

        # get the list of the ports of the device
        match_port = cli_ports_status.keys()

        # retrieve the port status values from XIQ
        logger.info("****************** Getting XIQ ports status: ******************")
        try:
            
            self.suite_udk.go_to_device360(onboarded_switch)

            self.suite_udk.select_max_pagination_size()

            time.sleep(5)
            
            xiq_port_table_info = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()
            
        finally:
            
            self.suite_udk.select_pagination_size("10")
            self.xiq.xflowsmanageDevice360.close_device360_window()

        logger.info(xiq_port_table_info)

        # CLI - XIQ speed values comparison
        logger.info("****************** Ports status info ******************")
        for port in match_port:
            # compare the values only if the port is shown in XIQ D360
            table_entry = [e for e in xiq_port_table_info if e['PORT NAME'] == port]
            if table_entry:
                table_entry = table_entry[0]
            
                xiq_port_status = table_entry["PORT STATUS"]
                if xiq_port_status == "Connected":
                    xiq_port_status_mapped = "up"
                else:
                    xiq_port_status_mapped = "down"
                    # if the admin status is "down", the operate status cannot be
                    # "up", so "Port Disabled by Admin" will be mapped as "down"
                    
                cli_port_status= cli_ports_status[port]
                logger.info(f'port: {port}, xid_port_status: {xiq_port_status}, device_port_status: {cli_port_status},'
                            f' xiq_port_status_mapped: {xiq_port_status_mapped}')

                print("comparing cli - xiq port status")
                assert xiq_port_status_mapped == cli_port_status, \
                    f"for port: {port} found xiq_port_status: {xiq_port_status} " \
                    f"different than cli_port_status: {cli_port_status}"
