# Author:         abolojan
# Description:    To verify if the port speed is shown correctly in the D360 table
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9570
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import re
import time

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9570Tests(xiqBase):

    @pytest.mark.tcxm_9570
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.run(order=1)
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_9570_check_speed_all_ports(self, logger, onboarded_switch):
        """
        Step          Step Description
        1             Onboard the device
        2             Navigate to Device360
        3             Get the speed values for all the ports from the device CLI
        4             Get the speed values for all the ports from XIQ Device360
        5             Check that the speed values from steps 3 and 4 are the same
        6             Setup clean up
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9570'

        try:
            self.network_manager.connect_to_network_element_name(onboarded_switch.name)
            # retrieve the port speed values from the device
            device_ports_speed = self.suite_udk.get_device_ports_speed(devCmd=self.devCmd, dut=onboarded_switch)
        finally:
            self.network_manager.close_connection_to_network_element(onboarded_switch.name)

        if device_ports_speed is None:
            pytest.fail('device_ports_speed is None')

        # get the list of the ports of the device
        match_port = device_ports_speed.keys()

        # retrieve the port speed values from XIQ
        logger.info("****************** Getting XIQ ports speed: ******************")
        try:
            
            self.suite_udk.go_to_device360(onboarded_switch)

            self.suite_udk.select_max_pagination_size()

            time.sleep(5)
            
            xiq_port_table_info = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()
            
        finally:
            
            paginations = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()
            if paginations:
                [pg_10] = [pg for pg in paginations if pg.text == "10"]
                self.auto_actions.click(pg_10)
            self.xiq.xflowsmanageDevice360.close_device360_window()

        logger.info("****************** XIQ ports speed dictionary: ******************")
        logger.info(xiq_port_table_info)

        # device - XIQ speed values comparison
        logger.info("****************** Ports speed info ******************")
        for port in match_port:
            
            table_entry = [e for e in xiq_port_table_info if e['PORT NAME'] == port]
            if table_entry:
                table_entry = table_entry[0]
                # compare the values only if the port is shown in XIQ D360
                xiq_port_speed = table_entry["PORT SPEED"]
                device_port_speed = device_ports_speed[port]

                # remove the Mbps string from the XIQ D360 speed value
                if xiq_port_speed != "Auto":
                    xiq_port_speed = re.search(r'\d+', xiq_port_speed).group(0)

                logger.info(f'port: {port}, xid_port_speed: {xiq_port_speed}, device_port_speed: {device_port_speed}')

                if device_port_speed != xiq_port_speed:
                    if not (device_port_speed == "0" and xiq_port_speed == "Auto"):
                        pytest.fail('Device port speed "{}" and XIQ port speed "{}" differ'.format(
                            device_port_speed, xiq_port_speed))
