from Tests.Pytest.NonProduction.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark
from pytest import fixture
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementCliSend import NetworkElementCliSend
from ExtremeAutomation.Library.Utils.DotDict import DotDict
import time

@fixture()
def test_setup_teardown(request):
    request.instance.Configure_DUTs_for_Traffic()
  
    def teardown():
        request.instance.Unconfigure_DUTs_for_Traffic()
    request.addfinalizer(teardown)
    
@fixture()
def test_setup_teardown_unconfigure_all(request):
    def teardown():
        request.instance.Unconfigure_All()
    request.addfinalizer(teardown)


class EXOS27585Tests(MACsecBase):

    def test_05_10_Ping_over_Mgmt_VLAN_with_MACsec_Disabled(self, test_setup_teardown):
        """ Verify_DUT1_can_ping_the_Host_IP_of_DUT2, and_vice_versa
        ...              Communication_is_on_VR-Mgmt, so_the_management_ports (not 
        ...              the_front_panel_ports) are_not_being_tested.
        ...              This_test_is_not_mandatory_to_detect_EXOS-27585, it_is
        ...              just_a_ping_sanity_test. """
    
        self.Verify_Mgmt_Port_Connectivity()
    
    
    def test_05_11_Ping_over_Port_VLAN_with_MACsec_Disabled(self, test_setup_teardown):
        """Verify_DUT1_can_ping_a_VLAN_IP_on_DUT2, and_vice_versa.
        ...              Communication_is_on_VR-Default.  This_tests_connectivity
        ...              of_the_front_panel_ports_which_are_assigned_to_the
        ...              TEST_VLAN_during_Test_Setup.
        ...              This_test_is_not_mandatory_to_detect_EXOS-27585, it_is
        ...              just_a_ping_sanity_test. """
    
        self.Verify_Front_Panel_Port_Connectivity()
    
    @mark.NIGHTLY
    def test_05_12_EXOS_27585_Bounce_MACsec_on_PortA_and_Verify_Connectivity_on_PortB(self, test_setup_teardown, test_setup_teardown_unconfigure_all):
        """This_test_detects_defect_EXOS-27585.  When_MACsec_is_enabled_between
        ...              DUT1:port_a_and_DUT2:port_a_and_DUT1:port_b_and_DUT2:port_b, disabling
        ...              MACsec_on_DUT1:port_a_breaks_DUT2:port_b_to_DUT1:port_a_connection.
        ...              Problem_may_be_limited_s_MIURA_PHYs (i.e., X465, VIM-4XE, etc.)
        ...
        ...              Test_Flow:
        ...                  o_Reboot_DUT1
        ...                  o_Enable_MACsec_between_DUT1:port_a & DUT2:port_a, and_DUT1:port_b & DUT2:port_b
        ...                  o_Verify_connectivity_on_port_b (by_pinging_over_port_b's_TEST_VLAN)
        ...                  o_Disable_MACsec_on_DUT1:port_a
        ...                  o_Verify_connectivity_on_port_b
        ...                  o_Enable_MACsec_on_DUT1:port_a
        ...                  o_Verify_connectivity_on_port_b """
    
        # The_bug_stops_happening_after_a_port_is_bounced_a_few_times.
        # Ensure_the_port_under_test_is_in_a_known_state_by_resetting_DUT1.
        self.suiteUdks.Reboot_DUT(self.tb.dut1)
    
        # Enable_MACsec_on_ports_A_and_B, then_verify_connectivity_on_port_B
        self.suiteUdks.Create_and_Verify_Macsec_Connection(self.tb.dut1.name, self.tb.dut1.port_a, self.tb.dut2.name, self.tb.dut2.port_a, self.tb.config.ca256_a)
        self.suiteUdks.Create_and_Verify_Macsec_Connection(self.tb.dut1.name, self.tb.dut1.port_b, self.tb.dut2.name, self.tb.dut2.port_b, self.tb.config.ca256_b)
        self.Verify_Front_Panel_Port_Connectivity()
    
        # Disable_MACsec_on_port_A, then_verify_connectivity_on_port_B
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_disable_ca_port(self.tb.dut1.name, self.tb.config.ca256_a.name, self.tb.dut1.port_a)
        self.suiteUdks.Macsec_Verify_Port_Connect_Pending(self.tb.dut2.name, self.tb.dut2.port_a)
        self.Verify_Front_Panel_Port_Connectivity()
    
        # Enable_MACsec_on_port_A, then_verify_connectivity_on_port_B
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_enable_ca_port(self.tb.dut1.name, self.tb.config.ca256_a.name, self.tb.dut1.port_a)
        self.suiteUdks.Macsec_Verify_Port_Connect_Secure(self.tb.dut2.name, self.tb.dut2.port_a)
        print("Next_test_expected_to_fail_if_EXOS-27585_is_present")
        self.Verify_Front_Panel_Port_Connectivity()
    
    def test_05_20_Host_Ping_over_Front_Panel_Port_with_MACsec_Enabled(self, test_setup_teardown):
        """Verify_Host-to-Host_packets (i.e., host_ping) are_transported
        ...              over_a_MACsec_connection.  When_executed_on_an_interop_testbed,
        ...              such_as_5420_to_5520, this_test_will_ensure_both_sides_are
        ...              encrypting/decrypting_host-generated_packets. """
        # Enable_MACsec_on_port_B, then_verify_connectivity_on_port_B (via_host_ping)
        self.suiteUdks.Create_and_Verify_Macsec_Connection(self.tb.dut1.name, self.tb.dut1.port_b, self.tb.dut2.name, self.tb.dut2.port_b, self.tb.config.ca256_b)
        self.Clear_Macsec_Counters(self.tb.dut1, self.tb.dut2)
        self.Verify_Front_Panel_Port_Connectivity()
        self.Verify_No_Macsec_Errors()
        self.suiteUdks.Disable_and_Verify_Macsec_Connection(self.tb.dut1.name, self.tb.dut1.port_b, self.tb.dut2.name, self.tb.dut2.port_b, self.tb.config.ca256_b)
    
    
    # *** keywords ***
    def Clear_Macsec_Counters(self, dut1, dut2):
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_clear_counters_on_port(dut1.name, dut1.port)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_clear_counters_on_port(dut2.name, dut2.port)
        time.sleep(1)

    def Configure_DUTs_for_Traffic(self):
        """Enable_host-to-host_ping_by_adding_the_ports_we_want_to
        ...              test_to_Tagged_VLANs_and_add_unique_IPs_to_these_VLANs.
        ...              We_will_test_connectivity_by_having_DUT1's_host_ping 
        ...              DUT2's_VLAN_IP. """
    
        self.HOST_VLAN = {}
        self.HOST_VLAN['name'] = 'VLAN_HOST_PING'
        self.HOST_VLAN['vid'] = '2000'
        self.HOST_VLAN['ip_dut1'] = '10.0.1.1'
        self.HOST_VLAN['ip_dut2'] = '10.0.1.2'
        self.HOST_VLAN['mask'] = '255.255.255.0'
        self.HOST_VLAN = DotDict(self.HOST_VLAN)
    
        self.defaultLibrary.apiLowLevelApis.port.port_enable_state(self.tb.dut2.name, self.tb.dut2.port_b)
        self.defaultLibrary.apiLowLevelApis.port.port_enable_state(self.tb.dut1.name, self.tb.dut1.port_b)
    
        self.Create_VLAN_with_Name_and_IP_on_Port(self.tb.dut1.name, self.HOST_VLAN.name, self.HOST_VLAN.vid, self.HOST_VLAN.ip_dut1, self.tb.dut1.port_b)
        self.Create_VLAN_with_Name_and_IP_on_Port(self.tb.dut2.name, self.HOST_VLAN.name, self.HOST_VLAN.vid, self.HOST_VLAN.ip_dut2, self.tb.dut2.port_b)
    
    def Unconfigure_All(self):
        self.suiteUdks.Disable_and_Verify_Macsec_Connection(self.tb.dut1.name, self.tb.dut1.port_a, self.tb.dut2.name, self.tb.dut2.port_a, self.tb.config.ca256_a)
        self.suiteUdks.Disable_and_Verify_Macsec_Connection(self.tb.dut1.name, self.tb.dut1.port_b, self.tb.dut2.name, self.tb.dut2.port_b, self.tb.config.ca256_b)
        self.Unconfigure_DUTs_for_Traffic()
    
    def Unconfigure_DUTs_for_Traffic(self):
        self.defaultLibrary.apiLowLevelApis.port.port_disable_state(self.tb.dut2.name, self.tb.dut2.port_b)
        self.defaultLibrary.apiLowLevelApis.port.port_disable_state(self.tb.dut1.name, self.tb.dut1.port_b)
    
        self.Remove_VLAN(self.tb.dut1.name, self.HOST_VLAN.name)
        self.Remove_VLAN(self.tb.dut2.name, self.HOST_VLAN.name)
    
    def Verify_Mgmt_Port_Connectivity(self):
        self.Host_Ping(self.tb.dut1.name, self.tb.dut2.ip, self.tb.dut1.mgmt_vlan)
        self.Host_Ping(self.tb.dut2.name, self.tb.dut1.ip, self.tb.dut2.mgmt_vlan)
    
    def Verify_Front_Panel_Port_Connectivity(self):
        self.Host_Ping(self.tb.dut1.name, self.HOST_VLAN.ip_dut2)
        self.Host_Ping(self.tb.dut2.name, self.HOST_VLAN.ip_dut1)
    
    def Host_Ping(self, dut_name, ip, vr='VR-Default'):
       """Execute_Host_Ping_test_but_retry_if_failure_dected. """
       # Wait_Until_Keyword_Succeeds_2x_200ms
       self.Host_Ping_Strict(dut_name, ip, vr)
    
    def Host_Ping_Strict(self, dut_name, ip, vr='VR-Default'):
        """Ping_specified_address_with_4_packets_and_verify_none_are_lost. """
        self.suiteUdks.networkElementCliSend.send_cmd_verify_output(dut_name, 'ping vr ' + vr + " " + ip, "4 packets transmitted, 4 packets received, 0% loss")
    
    def Create_VLAN_with_Name_and_IP_on_Port(self, dut_name, vlan_name, vlan_id, ip, port):
        self.defaultLibrary.apiUdks.vlanUdks.Create_VLAN_with_Name_and_Add_Ports_Tagged_then_Verify(dut_name, vlan_name, vlan_id, port)
        self.suiteUdks.networkElementCliSend.send_cmd_verify_output(dut_name, 'configure vlan ' + vlan_name + ' ipaddress ' + ip + ' ' + self.HOST_VLAN.mask, "IP interface for vlan " + vlan_name + " has been created.")
    
    def Remove_VLAN(self, dut_name, vlan_name):
        self.defaultLibrary.apiUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(dut_name, vlan_name,ignore_error="Error", ignore_cli_feedback=True)
    
    def Clear_Macsec_Counter(self):
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_clear_counters_on_port(self.tb.dut1.name, self.tb.dut1.port_b)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_clear_counters_on_port(self.tb.dut2.name, self.tb.dut2.port_b)
    
    def Verify_No_Macsec_Errors(self):
        self.suiteUdks.Verify_No_Macsec_Errors_on_Port(self.tb.dut1.name, self.tb.dut1.port_b)
        self.suiteUdks.Verify_No_Macsec_Errors_on_Port(self.tb.dut2.name, self.tb.dut2.port_b)