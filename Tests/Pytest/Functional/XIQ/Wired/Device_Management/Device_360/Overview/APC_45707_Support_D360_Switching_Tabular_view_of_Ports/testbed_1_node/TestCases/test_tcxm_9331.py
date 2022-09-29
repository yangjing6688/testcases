# Author:         dciupitu
# Description:    To verify the channelized ports in tabular view
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9331
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the VOSS devices that are supported by XIQ.

import pytest
import time
import re

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9331Tests(xiqBase):

    @pytest.mark.tcxm_9331
    @pytest.mark.voss
    @pytest.mark.run(order=-1)
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_9331_verify_channelized_ports(self, logger, onboarded_switch):
        """
        Step    Step Description
            1	Onboard the device
            2	Navigate into the Device Monitoring->Overview Tab
            3	CLI - Verify that there are channelizable ports
            4	CLI - Enable channelization on all ports
            5	Verify that the Port Mode from Port Info View that is changed to Channelized
            6	CLI - Disable channelization on all ports
            7	Verify that the Port Mode from Port Info View that is the same as before
            8	Revert all the additional configuration that have been done on the switch
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9331'

        if onboarded_switch.cli_type.upper() == "EXOS":
            pytest.skip("EXOS platform not supported")
            
        elif not onboarded_switch.get("console_ip") or not onboarded_switch.get("console_port"):
            pytest.skip("This test case needs a testbed yaml with console ip and port")

        try:

            self.suite_udk.go_to_device360(onboarded_switch)

            self.network_manager.connect_to_network_element_name(onboarded_switch.name)
            
            self.devCmd.send_cmd(onboarded_switch.name, 'enable',
                                    max_wait=10,
                                    interval=2)
            self.devCmd.send_cmd(onboarded_switch.name, 'configure terminal',
                                    max_wait=10,
                                    interval=2)
            output = self.devCmd.send_cmd(onboarded_switch.name, 'show interfaces GigabitEthernet channelize',
                                            max_wait=10,
                                            interval=2)[0].return_text
            match_port = re.findall(r"(\d+)\/(\d+)\s+(false|true)\s+[a-zA-Z0-9]+", output)

            if len(match_port) == 0:
                output = self.devCmd.send_cmd(onboarded_switch.name, 'show boot config flags',
                                                max_wait=10,
                                                interval=2)[0].return_text
                advanced_flag = re.findall(r"flags\sadvanced-feature-bandwidth-reservation\s([a-zA-Z]+)", output)
                spbm_flag = re.findall(r"flags\sspbm-config-mode\s([a-zA-Z]+)", output)

                if advanced_flag != "disable":
                    if spbm_flag == "false":
                        self.devCmd.send_cmd(onboarded_switch.name, 'boot config flags spbm-config-mode',
                                                max_wait=10,
                                                interval=2)
                        self.devCmd.send_cmd(onboarded_switch.name, 'save config',
                                                max_wait=10,
                                                interval=2)
                        self.devCmd.send_cmd(onboarded_switch.name, 'reset -y',
                                                max_wait=10,
                                                interval=2)

                        self.network_manager.close_connection_to_network_element(onboarded_switch.name)
                        time.sleep(240)
                        self.network_manager.connect_to_network_element_name(onboarded_switch.name)

                        logger.info("spbm-config-mode flag has been disabled")

                        self.devCmd.send_cmd(onboarded_switch.name, f'enable',
                                                max_wait=10,
                                                interval=2)
                        self.devCmd.send_cmd(onboarded_switch.name, f'configure terminal',
                                                max_wait=10,
                                                interval=2)

                    output = self.devCmd.send_cmd(onboarded_switch.name, 'no spbm',
                                                    max_wait=10,
                                                    interval=2,
                                                    ignore_cli_feedback=True)[0].return_text
                    error_msg = re.findall("Error: Delete i-sid from Vlan before setting SPBM global flag", output)
                    if error_msg:
                        output = self.devCmd.send_cmd(onboarded_switch.name, f'show interfaces GigabitEthernet state',
                                                        max_wait=10,
                                                        interval=2)[0].return_text
                        ports = re.findall(r"(\d+)\/(\d+)\s+(up|down)\s+(up|down)\s+--\s+(\d+)\/(\d+)\/(\d+)\s(\d+):(\d+):(\d+)", output)

                        slots = []
                        num_ports = {}
                        for port in ports:
                            if port[0] not in slots:
                                slots.append(port[0])
                            if port[0] not in num_ports.keys():
                                num_ports[port[0]] = 1
                            else:
                                num_ports[port[0]] += 1

                        for slot in slots:
                            command = "interface GigabitEthernet " + str(slot) + "/1-" + str(slot) + "/" + str(num_ports[slot])
                            self.devCmd.send_cmd(onboarded_switch.name, command,
                                                    max_wait=10,
                                                    interval=2)
                            self.devCmd.send_cmd(onboarded_switch.name, 'no auto-sense enable',
                                                    max_wait=10,
                                                    interval=2)
                            self.devCmd.send_cmd(onboarded_switch.name, 'exit',
                                                    max_wait=10,
                                                    interval=2)
                            logger.info("auto-sense has been disabled on all ports")

                        self.devCmd.send_cmd(onboarded_switch.name, 'no auto-sense onboarding i-sid',
                                                max_wait=10,
                                                interval=2)
                        logger.info("auto-sense onboarding i-sid has been deleted")
                        self.devCmd.send_cmd(onboarded_switch.name, 'no vlan i-sid 4048',
                                                max_wait=10,
                                                interval=2)
                        logger.info("vlan onboarding i-sid has been deleted")
                        self.devCmd.send_cmd(onboarded_switch.name, 'no router isis enable',
                                            confirmation_phrases='Do you want to continue (y/n) ?',
                                            confirmation_args='y')
                        logger.info("router isis has been disabled")

                    self.devCmd.send_cmd(onboarded_switch.name, 'no spbm',
                                            max_wait=10,
                                            interval=2,
                                            ignore_cli_feedback=True)
                    logger.info("spbm has been disabled")
                    self.devCmd.send_cmd(onboarded_switch.name, 'no boot config flags advanced-feature-bandwidth-reservation',
                                            max_wait=10,
                                            interval=2)
                    self.devCmd.send_cmd(onboarded_switch.name, 'save config',
                                            max_wait=10,
                                            interval=2)
                    self.devCmd.send_cmd(onboarded_switch.name, 'reset -y',
                                            max_wait=10,
                                            interval=2)

                    self.network_manager.close_connection_to_network_element(onboarded_switch.name)
                    time.sleep(240)
                    self.network_manager.connect_to_network_element_name(onboarded_switch.name)

                    logger.info("advanced-feature-bandwidth-reservation flag has been disabled")

                    self.devCmd.send_cmd(onboarded_switch.name, f'enable',
                                            max_wait=10,
                                            interval=2)
                    self.devCmd.send_cmd(onboarded_switch.name, f'configure terminal',
                                            max_wait=10,
                                            interval=2)

                    output = self.devCmd.send_cmd(onboarded_switch.name, 'show interfaces GigabitEthernet channelize',
                                                    max_wait=10,
                                                    interval=2)[0].return_text
                    match_port = re.findall(r"(\d+)\/(\d+)\s+(false|true)\s+[a-zA-Z0-9]+", output)

            if len(match_port) > 0:

                    already_channelized = []
                    for port in match_port:
                        if port[2] == "false":
                            command = "interface GigabitEthernet " + port[0] + "/" + port[1]

                            self.devCmd.send_cmd(onboarded_switch.name, command)
                            self.devCmd.send_cmd(onboarded_switch.name, 'channelize enable',
                                                 confirmation_phrases='Do you wish to continue (y/n) ?',
                                                 confirmation_args='y')
                        else:
                            already_channelized.append(port[0] + "/" + port[1])
                    logger.info("Channelization enabled on all ports")

                    time.sleep(200)
                    for port in match_port:
                        ok = 0
                        start_time = time.time()
                        while time.time() - start_time < 500:
                            self.xiq.xflowsmanageDevice360.device360_refresh_page()
                            device_info = self.xiq.xflowsmanageDevice360.device360_get_automation_port_info(port[0] + "/" + port[1])

                            device_port_mode = device_info["port_mode"].split()[2]
                            if device_port_mode != "Channelized":
                                time.sleep(20)
                            else:
                                ok = 1
                                break

                        if ok == 0:
                            self.suite_udk.no_channel_enable_on_all_ports(onboarded_switch)
                            assert ok, f"Failed to change Port Mode {port[1]} to Channelized"

                    for port in match_port:
                        command = "interface GigabitEthernet " + port[0] + "/" + port[1] + "/1"
                        self.devCmd.send_cmd(onboarded_switch.name, command)
                        output = self.devCmd.send_cmd(onboarded_switch.name, 'no channelize enable',
                                             confirmation_phrases='Do you wish to continue (y/n) ?',
                                             confirmation_args='y',
                                             ignore_cli_feedback=True)[0].return_text

                    logger.info("Channelization disabled on all ports")

                    time.sleep(200)
                    for port in match_port:
                        str_port = port[0] + "/" + port[1]
                        if str_port in already_channelized:
                            continue

                        ok = 0
                        start_time = time.time()
                        while time.time() - start_time < 500:
                            self.xiq.xflowsmanageDevice360.device360_refresh_page()
                            device_info = self.xiq.xflowsmanageDevice360.device360_get_automation_port_info(port[0] + "/" + port[1])
                            device_port_mode = device_info["port_mode"].split()[2]
                            if device_port_mode == "Channelized":
                                time.sleep(20)
                            else:
                                ok = 1
                                break
                        if ok == 0:
                            self.suite_udk.no_channel_enable_on_all_ports(onboarded_switch)
                            assert ok, f"Failed to change Port Mode {port[1]} back"
        
        finally:
            
            self.xiq.xflowsmanageDevice360.close_device360_window()
            
            try:
                self.network_manager.connect_to_network_element_name(onboarded_switch.name)
            except Exception as exc:
                logger.info(repr(exc))

            output = self.devCmd.send_cmd(onboarded_switch.name, 'show boot config choice',
                                          max_wait=10,
                                          interval=2)[0].return_text
            config_file = re.findall(r"choice primary config-file \"(.*)\"", output)[0]
            self.devCmd.send_cmd(onboarded_switch.name, 'remove ' + config_file,
                                 confirmation_phrases='Are you sure (y/n) ?',
                                 confirmation_args='y')
            self.devCmd.send_cmd(onboarded_switch.name, 'reset -y',
                                 max_wait=10,
                                 interval=2)
            self.network_manager.close_connection_to_network_element(onboarded_switch.name)
            time.sleep(240)
            logger.info("Primary choice config file has been deleted")

            self.network_manager.connect_to_network_element_name(onboarded_switch.name)

            self.devCmd.send_cmd(onboarded_switch.name, 'enable', max_wait=10, interval=2)
            self.devCmd.send_cmd(onboarded_switch.name, 'configure terminal', max_wait=10, interval=2)
            self.devCmd.send_cmd(onboarded_switch.name, 'boot config flags sshd', max_wait=10, interval=2)
            self.devCmd.send_cmd(onboarded_switch.name, 'boot config flags telnet', max_wait=10, interval=2)
            self.devCmd.send_cmd(onboarded_switch.name, 'application', max_wait=10, interval=2)
            self.devCmd.send_cmd(onboarded_switch.name, 'no iqagent enable', max_wait=10, interval=2)
            self.devCmd.send_cmd(onboarded_switch.name, f'iqagent server {self.cfg["sw_connection_host"]}', max_wait=10, interval=2)
            self.devCmd.send_cmd(onboarded_switch.name, 'iqagent enable', max_wait=10, interval=2)
            
            self.xiq.xflowscommonDevices.wait_until_device_online(onboarded_switch.serial)
            res = self.xiq.xflowscommonDevices.get_device_status(device_serial=onboarded_switch.serial)
            assert res == 'green', f"The device did not come up successfully in the XIQ; Device: {onboarded_switch}"

            logger.info("Device come up successfully in the XIQ")
