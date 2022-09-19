# Author:         dbadea
# Description:    To verify if you can go to 360 page and check LLDP neighbours hyperlinks
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9323
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
#                 This test case needs a testbed yaml with two devices.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.NonProduction.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_2_node.Resources.testcase_base import xiqBase


class TCXM9323Tests(xiqBase):

    @pytest.mark.xim_tcxm_9323
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.development
    @pytest.mark.p2
    @pytest.mark.testbed_2_node
    def test_9323_check_lldp_neighbour_hyperlink_and_value(self, logger, onboarded_2_switches):
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9323_p2'

        dut1, dut2 = onboarded_2_switches
        
        ports_isl = self.suite_udk.create_ports_list(dut1.isl)
        logger.info('ISL ports = {} for dut = {}'.format(ports_isl, dut1.name))

        start_time = time.time()
        
        self.suite_udk.bounce_device(self.xiq, dut1)
        self.suite_udk.bounce_device(self.xiq, dut2)

        while time.time() - start_time < 600:
            try:
                logger.info('Refresh page')
                self.auto_actions.click(self.client_web_elements.get_client_page_refresh_button())
                time.sleep(5)

                logger.info('Go to 360 page of dut = {}'.format(dut1.name))
                self.suite_udk.go_to_device360(dut1)

                real_ports = self.device_360_web_elements.get_ports_from_device360_up()
                logger.info("REAL PORTS =  {}".format(real_ports))
                time.sleep(10)

                success = self.suite_udk.check_lld_neighbour_field_with_value_and_with_hyperlink(
                    ports_isl, real_ports, logger)
                
                assert success == 1
            
            except Exception as exc:
                
                logger.error("Test is a failure and LLDP neighbours does not exist with Hyperlinks")
                logger.error(repr(exc))
                time.sleep(30)
                
            else:
                
                logger.info("Test is a success and LLDP neighbours exist with Hyperlinks")
                break
            
            finally:
                
                self.xiq.xflowsmanageDevice360.close_device360_window()
        else:
            pytest.fail("Test is a failure and LLDP neighbours does not exist with Hyperlinks")

    # @pytest.mark.skip
    # @pytest.mark.development
    # @pytest.mark.testbed_2_node
    # @pytest.mark.xim_tcxm_9323
    # @pytest.mark.p3
    # def test_check_lldp_neighbour_without_hyperlink_and_with_value(self, logger, onboarded_2_switches, onboarding_location):
    #     self.executionHelper.testSkipCheck()
    #     self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9323_p3'

    #     dut1, dut2 = onboarded_2_switches

    #     ports_isl = self.suite_udk.create_ports_list(dut1.isl)
    #     logger.info('ISL ports = {} for dut = {}'.format(ports_isl, dut1.name))

    #     try:
    #         self.xiq.xflowscommonDevices.delete_device(device_serial=dut2.serial)
    #         time.sleep(10)

    #         logger.info('Refresh page')
    #         self.auto_actions.click(self.client_web_elements.get_client_page_refresh_button())
    #         time.sleep(5)

    #         self.suite_udk.go_to_device360(dut1)

    #         real_ports = self.device_360_web_elements.get_ports_from_device360_up()
    #         logger.info("REAL PORTS =  {}".format(real_ports))
    #         time.sleep(10)

    #         success = self.suite_udk.check_lld_neighbour_field_with_value_and_without_hyperlink(ports_isl, real_ports,
    #                                                                                             logger)

    #         if success == 1:
    #             logger.info("Test is a success and LLDP neighbours exist without Hyperlinks")
    #         else:
    #             logger.error("Test is a failure and LLDP neighbours does not exist with Hyperlinks")
    #             pytest.fail("Test is a failure and LLDP neighbours does not exist with Hyperlinks")
    #     finally:
    #         self.xiq.xflowsmanageDevice360.close_device360_window()
    #         time.sleep(5)

    #         self.suite_udk.do_onboarding(dut2, location=onboarding_location)

    # @pytest.mark.skip
    # @pytest.mark.development
    # @pytest.mark.testbed_2_node
    # @pytest.mark.xim_tcxm_9323
    # @pytest.mark.p4
    # def test_check_lldp_neighbour_without_hyperlink_and_value(self, logger, onboarded_2_switches):
    #     self.executionHelper.testSkipCheck()
    #     self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9323_p4'

    #     dut1, dut2 = onboarded_2_switches

    #     ports_isl = self.suite_udk.create_ports_list(dut1.isl)
    #     logger.info('ISL ports = {} for dut = {}'.format(ports_isl, dut1.name))

    #     time.sleep(660)
    #     try:
    #         time.sleep(10)
    #         logger.info('Go to 360 page of dut = {}'.format(dut1.name))
    #         self.suite_udk.go_to_device360(dut1)

    #         self.network_manager.connect_to_network_element_name(dut2.name)
            
    #         if dut2.cli_type.upper() == "EXOS":
    #             try:
    #                 logger.info("EXOS case to disable ports")
    #                 for port in ports_isl:
    #                     self.devCmd.send_cmd(dut2.name, f'disable port {port}', max_wait=10, interval=2)

    #                 logger.info('Refresh 360 page')
    #                 self.auto_actions.click(self.device_360_web_elements.get_device360_refresh_page_button())
    #                 time.sleep(660)

    #                 logger.info('Close 360 page')
    #                 self.xiq.xflowsmanageDevice360.close_device360_window()
    #                 time.sleep(5)

    #                 logger.info('Go to 360 page of dut = {}'.format(dut1.name))
    #                 self.suite_udk.go_to_device360(dut1)

    #                 logger.info('Refresh 360 page')
    #                 self.auto_actions.click(self.device_360_web_elements.get_device360_refresh_page_button())
    #                 time.sleep(5)

    #                 real_ports = self.device_360_web_elements.get_ports_from_device360_up()
    #                 logger.info("REAL PORTS =  {}".format(real_ports))
    #                 time.sleep(10)

    #                 success = self.suite_udk.check_lld_neighbour_field_without_value_and_without_hyperlink(ports_isl, real_ports, logger)

    #                 if success == 1:
    #                     logger.info("Test is a success and LLDP neighbours exist without Hyperlinks and values")
    #                 else:
    #                     logger.error("Test is a failure and LLDP neighbours exist with Hyperlinks and values")
    #                     pytest.fail("Test is a failure and LLDP neighbours exist with Hyperlinks and values")
    #                 time.sleep(10)

    #             finally:
                    
    #                 for port in ports_isl:
    #                     self.devCmd.send_cmd(dut2.name, f'enable port {port}', max_wait=10, interval=2)

    #         elif dut2.cli_type.upper() == "VOSS":
    #             logger.info("VOSS case to disable ports")

    #             for cmd in [
    #                 "enable",
    #                 "configure terminal",
    #                 "application",
    #             ]:
    #                 print(f"Send this command to VOSS dut: '{cmd}'")
    #                 self.devCmd.send_cmd(dut2.name, cmd, max_wait=10, interval=2)
    #                 time.sleep(1)
                
    #             try:
                    
    #                 for port in ports_isl:
    #                     logger.info("PORT =  {}".format(port))
    #                     self.devCmd.send_cmd(dut2.name, f'interface gigabitEthernet 1/{port}', max_wait=10, interval=2)
    #                     self.devCmd.send_cmd(dut2.name, "shutdown", max_wait=10, interval=2)
    #                     self.devCmd.send_cmd(dut2.name, "exit", max_wait=10, interval=2)

    #                 time.sleep(660)
    #                 logger.info('Refresh 360 page')
    #                 self.auto_actions.click(self.device_360_web_elements.get_device360_refresh_page_button())
    #                 time.sleep(5)

    #                 logger.info('Close 360 page')
    #                 self.xiq.xflowsmanageDevice360.close_device360_window()
    #                 time.sleep(5)

    #                 logger.info('Go to 360 page of dut = {}'.format(dut1.name))
    #                 self.suite_udk.go_to_device360(dut1)

    #                 logger.info('Refresh 360 page')
    #                 self.auto_actions.click(self.device_360_web_elements.get_device360_refresh_page_button())
    #                 time.sleep(5)

    #                 real_ports = self.device_360_web_elements.get_ports_from_device360_up()
    #                 logger.info("REAL PORTS =  {}".format(real_ports))
    #                 time.sleep(10)

    #                 success = self.suite_udk.check_lld_neighbour_field_without_value_and_without_hyperlink(ports_isl,
    #                                                                                                     real_ports,
    #                                                                                                     logger)

    #                 if success == 1:
    #                     logger.info("Test is a success and LLDP neighbours exist without Hyperlinks and values")
    #                 else:
    #                     logger.error("Test is a failure and LLDP neighbours exist with Hyperlinks and values")
    #                     for port in ports_isl:
    #                         self.devCmd.send_cmd(dut2.name, f'interface gigabitEthernet 1/{port}', max_wait=10, interval=2)
    #                         self.devCmd.send_cmd(dut2.name, "no shutdown", max_wait=10, interval=2)
    #                         self.devCmd.send_cmd(dut2.name, "exit", max_wait=10, interval=2)
    #                     pytest.fail("Test is a failure and LLDP neighbours exist with Hyperlinks and values")
    #                 time.sleep(10)

    #             finally:
                    
    #                 for port in ports_isl:
    #                     logger.info("PORT =  {}".format(port))
    #                     self.devCmd.send_cmd(dut2.name, f'interface gigabitEthernet 1/{port}', max_wait=10, interval=2)
    #                     self.devCmd.send_cmd(dut2.name, "no shutdown", max_wait=10, interval=2)
    #                     self.devCmd.send_cmd(dut2.name, "exit", max_wait=10, interval=2)

    #     finally:
    #         self.xiq.xflowsmanageDevice360.close_device360_window()
    #         self.suite_udk.close_connection_with_error_handling(dut2)
