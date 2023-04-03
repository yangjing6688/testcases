# Author:         Marius Chelu
# Description:    This suite tests if the Access Vlan column from Device 360 view page is populated with
#                 the correct vlan id value
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9566
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


@pytest.mark.testbed_1_node
class TCXM9566Tests(xiqBase):

    @pytest.mark.tcxm_9566
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.testbed_1_node
    def test_tcxm_9566(self, onboarded_switch, onboarding_location, request, setup_lldp):
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9566'

        vlan_id = self.suite_udk.generate_vlan_id()
        policy_name = self.suite_udk.generate_policy_name()
 
        self.suite_udk.change_device_management_settings(option="disable")

        ports = sorted(
            self.suite_udk.get_ports_from_dut(onboarded_switch),
            key=int if onboarded_switch.cli_type.upper() == "EXOS" else (lambda x: int(x.split("/")[1]))
        )[:4]
        
        self.suite_udk.create_network_policy(policy_name)

        def finalizer():
            try:
                self.suite_udk.go_to_device_360_port_config(onboarded_switch)
            
                access_vlan_id = "1" if onboarded_switch.cli_type.upper() == "EXOS" else None
                port_type = "Access Port" if onboarded_switch.cli_type.upper() == "EXOS" else "Auto-sense Port"
                
                for port in ports:
                    self.suite_udk.enter_port_type_and_vlan_id(
                        port=port, port_type=port_type, access_vlan_id=access_vlan_id)
        
            finally:
                self.suite_udk.save_device_360_port_config()
                self.xiq.xflowsmanageDevice360.close_device360_window()
                
            self.suite_udk.update_and_wait_switch(policy_name, onboarded_switch)
            
            self.suite_udk.do_onboarding(onboarded_switch, location=onboarding_location)
            
            try:
                self.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(policy_name)
            except Exception as exc:
                print(repr(exc))
                
        request.addfinalizer(finalizer)

        try:
            self.suite_udk.go_to_device_360_port_config(onboarded_switch)
        
            for port in ports:
                self.suite_udk.enter_port_type_and_vlan_id(port=port, port_type="Access Port", access_vlan_id=vlan_id)
        
        finally:
            self.suite_udk.save_device_360_port_config()
            self.xiq.xflowsmanageDevice360.close_device360_window()
                
        self.suite_udk.assign_policy(policy_name, onboarded_switch)
        self.suite_udk.update_and_wait_switch(policy_name, onboarded_switch)
        
        try:
            self.suite_udk.go_to_device360(onboarded_switch)
            
            self.suite_udk.select_max_pagination_size()
                
            table_rows = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()
            for row in table_rows:
                access_vlan = row["ACCESS VLAN"]
                if row["PORT NAME"] in ports:
                    if access_vlan == vlan_id:
                        print(f'Port {row["PORT NAME"]} has assign VLAN ID {vlan_id}')
                    else:
                        pytest.fail(f'Port {row["PORT NAME"]} does not have assigned the VLAN ID {vlan_id}.None was found!')
        
        finally:
            
            self.suite_udk.select_pagination_size("10")
            self.xiq.xflowsmanageDevice360.close_device360_window()
