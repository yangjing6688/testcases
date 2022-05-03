from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper

from Tests.Pytest.NonProduction.LLDP_Sync_on_Failover_Feature_Unit_Tests.Resources.SuiteVariables import SuiteVariable


# Test Suite User-Defined Keyword functions
class SuiteUdk:

    def __init__(self):
        self.defaultLibrary = DefaultLibrary()
        self.tb = PytestConfigHelper(config)
        self.var = SuiteVariable()
        self.defaultLibrary = DefaultLibrary()
        self.netElement = self.defaultLibrary.deviceNetworkElement
        self.lowApis = self.defaultLibrary.apiLowLevelApis
        self.udks = self.defaultLibrary.apiUdks

    def Test_suite_setup(self):
        print("Unit Test Suite Setup:")
        self.verify_backup_sync_in_dut()
        self.enable_required_ports()
        self.configure_fa_server(self.tb.dut3_name)
        self.create_fa_client_vlan_and_nsi(self.tb.dut2_name)
        self.verify_fa_element_state(self.tb.dut3_name, self.var.fa_mode_server)
        self.verify_fa_element_state(self.tb.dut1_name, self.var.fa_mode_proxy)
        self.verify_fa_element_state(self.tb.dut2_name, self.var.fa_mode_client)

    def Test_suite_cleanup(self):
        print("Unit Test Suite Cleanup:")
        self.unconfigure_fa_server(self.tb.dut3_name)
        self.delete_fa_client_vlan(self.tb.dut2_name)

    def verify_backup_sync_in_dut(self):
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP.*(In.*Sync)',
                                                                           max_wait=60)

    def wait_for_backup_sync(self):
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP.*(In.*Sync)',
                                                                           max_wait=360, interval=20)

    def enable_required_ports(self):
        print("Enabled required ports in all switches:")
        self.netElement.networkElementCliSend.send_cmd(self.tb.dut1_name, "disable ports all")
        self.netElement.networkElementCliSend.send_cmd(self.tb.dut2_name, "disable ports all")
        self.netElement.networkElementCliSend.send_cmd(self.tb.dut3_name, "disable ports all")
        self.netElement.networkElementCliSend.send_cmd(self.tb.dut4_name, "disable ports all")
        self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut3_name,
                                                                    self.tb.dut3_isl_dut1_port_b.ifname)
        self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut1_name,
                                                                    self.tb.dut1_isl_dut3_port_b.ifname)
        self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut1_name,
                                                                    self.tb.dut1_isl_dut2_port_c.ifname)
        self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut2_name,
                                                                    self.tb.dut2_isl_dut1_port_c.ifname)

    def configure_fa_server(self, dut_name):
        print("Configure FA Server:")
        self.lowApis.vlan.vlan_create_vlan(dut_name, self.var.server_loopback_vlan_name)
        self.lowApis.vlan.vlan_verify_enabled(dut_name, self.var.server_loopback_vlan_name)
        self.lowApis.interface.interface_enable_loopback(dut_name, self.var.server_loopback_vlan_name)

    def unconfigure_fa_server(self, dut_name):
        print("Un-configure FA Server:")
        self.lowApis.vlan.vlan_delete_vlan(dut_name, self.var.server_loopback_vlan_name)
        self.lowApis.vlan.vlan_verify_does_not_exist(dut_name, self.var.server_loopback_vlan_name)

    def create_fa_client_vlan_and_nsi(self, dut_name):
        print("Configure FA Client:")
        self.udks.vlanUdks.Create_VLAN_and_Verify_it_Exists(dut_name, self.var.fa_client_vlan_id)
        self.udks.vlanUdks.Configure_Vlan_Nsi_and_Verify_it_is_Set(dut_name, self.var.fa_client_vlan_id,
                                                                   self.var.fa_client_vlan_nsi)

    def delete_fa_client_vlan(self, dut_name):
        print("Un-configure FA Client:")
        self.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(dut_name, self.var.fa_client_vlan_id,
                                                                ignore_error="Error")

    def verify_fa_element_state(self, dut_name, state):
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(dut_name,
                                                                           'show fabric attach agent',
                                                                           'Element.*' + state)

    def verify_neighbors_and_assignments(self, wait_time):
        double_wait_time = wait_time * 2
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show lldp port ' +
                                                                           self.tb.dut1_isl_dut3_port_b.ifname +
                                                                           ' neighbors',
                                                                           self.tb.dut1_isl_dut3_port_b.ifname +
                                                                           '.*' + self.tb.dut3_isl_dut1_port_b.ifname,
                                                                           max_wait=wait_time)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show lldp port ' +
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           ' neighbors',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*' + self.tb.dut2_isl_dut1_port_c.ifname,
                                                                           max_wait=wait_time)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach elements',
                                                                           self.tb.dut1_isl_dut3_port_b.ifname +
                                                                           '.*Server', max_wait=wait_time)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach elements',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*Switch', max_wait=wait_time)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*' + self.var.fa_client_vlan_id +
                                                                           '.*' + self.var.fa_client_vlan_nsi +
                                                                           '.*Active',
                                                                           max_wait=double_wait_time)

    def enable_required_mlag_setup_ports(self):
        print("Enable required MLAG setup ports:")
        self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut4_name,
                                                                    self.tb.dut4_isl_dut1_port_c.ifname)
        self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut1_name,
                                                                    self.tb.dut1_isl_dut4_port_c.ifname)
        self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut4_name,
                                                                    self.tb.dut4_isl_dut1_port_d.ifname)
        self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut1_name,
                                                                    self.tb.dut1_isl_dut4_port_d.ifname)
        self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut4_name,
                                                                    self.tb.dut4_isl_dut3_port_a.ifname)
        self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut3_name,
                                                                    self.tb.dut3_isl_dut4_port_a.ifname)
        self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut4_name,
                                                                    self.tb.dut4_isl_dut2_port_a.ifname)
        self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut2_name,
                                                                    self.tb.dut2_isl_dut4_port_a.ifname)

    def configure_lag(self, dut_name, master_port, member_port):
        self.lowApis.lacp.lacp_create_lag(dut_name, master_port, master_port)
        if master_port != member_port:
            self.lowApis.lacp.lacp_set_lag_port(dut_name, master_port, member_port)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(dut_name, "show config vlan | grep sharing",
                                                                           "sharing.*" + master_port +
                                                                           ".*grouping.*" + member_port)

    def unconfigure_lag(self, dut_name, master_port):
        self.lowApis.lacp.lacp_delete_lag(dut_name, master_port)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(dut_name, "show config vlan | grep sharing",
                                                                           "sharing.*" + master_port, exists=False)

    def configure_lag_on_required_ports_in_all_duts(self):
        print("Configure LAG on all required ports:")
        # FA server to FA proxy 1 and 2 ports config
        self.configure_lag(self.tb.dut3_name, self.tb.dut3_isl_dut4_port_a.ifname,
                           self.tb.dut3_isl_dut1_port_b.ifname)
        # FA proxy 1 to FA server port config
        self.configure_lag(self.tb.dut4_name, self.tb.dut4_isl_dut3_port_a.ifname,
                           self.tb.dut4_isl_dut3_port_a.ifname)
        # FA proxy 2 to FA server port config
        self.configure_lag(self.tb.dut1_name, self.tb.dut1_isl_dut3_port_b.ifname,
                           self.tb.dut1_isl_dut3_port_b.ifname)

        # FA proxy 1 to FA proxy 2 ISC ports config
        self.configure_lag(self.tb.dut4_name, self.tb.dut4_isl_dut1_port_d.ifname,
                           self.tb.dut4_isl_dut1_port_c.ifname)
        # FA proxy 2 to FA proxy 1 ISC ports config
        self.configure_lag(self.tb.dut1_name, self.tb.dut1_isl_dut4_port_d.ifname,
                           self.tb.dut1_isl_dut4_port_c.ifname)

        # FA proxy 1 to FA client port config
        self.configure_lag(self.tb.dut4_name, self.tb.dut4_isl_dut2_port_a.ifname,
                           self.tb.dut4_isl_dut2_port_a.ifname)
        # FA proxy 2 to FA client port config
        self.configure_lag(self.tb.dut1_name, self.tb.dut1_isl_dut2_port_c.ifname,
                           self.tb.dut1_isl_dut2_port_c.ifname)
        # FA client to FA proxy 1 and 2 ports config
        self.configure_lag(self.tb.dut2_name, self.tb.dut2_isl_dut4_port_a.ifname,
                           self.tb.dut2_isl_dut1_port_c.ifname)

    def unconfigure_lag_on_required_ports_in_all_duts(self):
        print("Un-Configure LAG on all required ports:")
        # FA server to FA proxy 1 and 2 ports config
        self.unconfigure_lag(self.tb.dut3_name, self.tb.dut3_isl_dut4_port_a.ifname)
        # FA proxy 1 to FA server port config
        self.unconfigure_lag(self.tb.dut4_name, self.tb.dut4_isl_dut3_port_a.ifname)
        # FA proxy 2 to FA server port config
        self.unconfigure_lag(self.tb.dut1_name, self.tb.dut1_isl_dut3_port_b.ifname)

        # FA proxy 1 to FA proxy 2 ISC ports config
        self.unconfigure_lag(self.tb.dut4_name, self.tb.dut4_isl_dut1_port_d.ifname)
        # FA proxy 2 to FA proxy 1 ISC ports config
        self.unconfigure_lag(self.tb.dut1_name, self.tb.dut1_isl_dut4_port_d.ifname)

        # FA proxy 1 to FA client port config
        self.unconfigure_lag(self.tb.dut4_name, self.tb.dut4_isl_dut2_port_a.ifname)
        # FA proxy 2 to FA client port config
        self.unconfigure_lag(self.tb.dut1_name, self.tb.dut1_isl_dut2_port_c.ifname)
        # FA client to FA proxy 1 and 2 ports config
        self.unconfigure_lag(self.tb.dut2_name, self.tb.dut2_isl_dut4_port_a.ifname)

    def configure_mlag_on_peer_a(self):
        print("Configure MLAG on Peer A:")
        self.udks.vlanUdks.Create_VLAN_with_Name_and_Add_Ports_Tagged_then_Verify(self.tb.dut4_name,
                                                                                  self.var.isc_vlan,
                                                                                  self.var.isc_vlan_id,
                                                                                  self.tb.dut4_isl_dut1_port_d.ifname)
        self.lowApis.interface.interface_set_ipv4_primary_addr_netmask(self.tb.dut4_name, self.var.isc_vlan,
                                                                       self.var.isc_vlan_ipaddr_a,
                                                                       self.var.isc_vlan_ipaddr_mask)
        self.lowApis.mlag.mlag_create_peer(self.tb.dut4_name, self.var.mlag_peer_name_b)
        self.lowApis.mlag.mlag_set_peer_ipaddress_vr(self.tb.dut4_name, self.var.mlag_peer_name_b,
                                                     self.var.isc_vlan_ipaddr_b,
                                                     'VR-Default')
        self.lowApis.mlag.mlag_enable_port_peer_id(self.tb.dut4_name, self.tb.dut4_isl_dut2_port_a.ifname,
                                                   self.var.mlag_peer_name_b, self.var.mlag_peer_id)
        self.lowApis.mlag.mlag_verify_peer_exists(self.tb.dut4_name, self.var.mlag_peer_name_b, ignore_error="Error")

    def configure_mlag_on_peer_b(self):
        print("Configure MLAG on Peer B:")
        self.udks.vlanUdks.Create_VLAN_with_Name_and_Add_Ports_Tagged_then_Verify(self.tb.dut1_name,
                                                                                  self.var.isc_vlan,
                                                                                  self.var.isc_vlan_id,
                                                                                  self.tb.dut1_isl_dut4_port_d.ifname)
        self.lowApis.interface.interface_set_ipv4_primary_addr_netmask(self.tb.dut1_name, self.var.isc_vlan,
                                                                       self.var.isc_vlan_ipaddr_b,
                                                                       self.var.isc_vlan_ipaddr_mask)
        self.lowApis.mlag.mlag_create_peer(self.tb.dut1_name, self.var.mlag_peer_name_a)
        self.lowApis.mlag.mlag_set_peer_ipaddress_vr(self.tb.dut1_name, self.var.mlag_peer_name_a,
                                                     self.var.isc_vlan_ipaddr_a,
                                                     'VR-Default')
        self.lowApis.mlag.mlag_enable_port_peer_id(self.tb.dut1_name, self.tb.dut1_isl_dut2_port_c.ifname,
                                                   self.var.mlag_peer_name_a, self.var.mlag_peer_id)
        self.lowApis.mlag.mlag_verify_peer_exists(self.tb.dut1_name, self.var.mlag_peer_name_a, ignore_error="Error")

    def unconfigure_mlag_on_peer_a(self):
        print("Un-Configure MLAG on Peer A:")
        self.lowApis.mlag.mlag_disable_port(self.tb.dut4_name, self.tb.dut4_isl_dut2_port_a.ifname)
        self.lowApis.mlag.mlag_delete_peer(self.tb.dut4_name, self.var.mlag_peer_name_b)
        self.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.dut4_name, self.var.isc_vlan)

    def unconfigure_mlag_on_peer_b(self):
        print("Un-Configure MLAG on Peer B:")
        self.lowApis.mlag.mlag_disable_port(self.tb.dut1_name, self.tb.dut1_isl_dut2_port_c.ifname)
        self.lowApis.mlag.mlag_delete_peer(self.tb.dut1_name, self.var.mlag_peer_name_a)
        self.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.dut1_name, self.var.isc_vlan)
