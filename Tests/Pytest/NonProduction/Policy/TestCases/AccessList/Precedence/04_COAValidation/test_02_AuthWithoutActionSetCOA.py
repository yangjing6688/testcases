from Tests.Pytest.NonProduction.Policy.Resources.PolicyBase import PolicyBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.NonProduction.Policy.Resources.Policy_Test_Suite_Udks import Policy_Test_Suite_Udks
import time

@fixture()
def test_setup_teardown(request):
    # Setup_section
    def teardown():
        request.instance.Test_Case_Cleanup()
    request.addfinalizer(teardown)

class AuthWithoutActionSetCOATests(PolicyBase): 
    @mark.F_1000_0402
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6 
    
    def test_01_Access_List_COA_Single_Match_Full_Mask_Dropping_Tests(self):
        #[Documentation]  Test_Objective: Verify_An_Access-List_with_full_masks_drops_properly (policy_profile_defaulted_to_forward).
        
        print('  (Step_1) Configure_ports, QoS, and_FDB_for_Policy_traffic_tests.')
        self.localPolicyUdks.Basic_Policy_Setup()
    
    #        Create_VLAN_and_Verify_it_Exists                                self.tb.config.netelem1.name,  ${vlan_b}
    #
        self.localPolicyUdks.vlanUdks.Create_VLAN_with_Name_and_Verify_it_Exists( self.tb.config.netelem1.name,  self.tb.config.vlanName_100,  
                                                                                   self.tb.config.vlan_100)
        self.localPolicyUdks.vlanUdks.Create_VLAN_with_Name_and_Verify_it_Exists( self.tb.config.netelem1.name,  self.tb.config.vlanName_200,
                                                                                     self.tb.config.vlan_200)
        self.localPolicyUdks.vlanUdks.Create_VLAN_with_Name_and_Verify_it_Exists( self.tb.config.netelem1.name,  self.tb.config.vlanName_300,
                                                                                     self.tb.config.vlan_300)
        self.localPolicyUdks.vlanUdks.Create_VLAN_with_Name_and_Verify_it_Exists( self.tb.config.netelem1.name,  self.tb.config.vlanName_400,
                                                                                     self.tb.config.vlan_400)
        self.localPolicyUdks.vlanUdks.Create_VLAN_with_Name_and_Verify_it_Exists( self.tb.config.netelem1.name,  self.tb.config.vlanName_500,
                                                                                     self.tb.config.vlan_500)
    
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name,    self.tb.config.vlan_100,
                                                                       self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name,    self.tb.config.vlan_100,
                                                                       self.tb.config.netelem1.tgen.port_a.ifname)
    
        self.localPolicyUdks.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.tb.config.netelem1.name,  self.tb.config.packetA.dst_mac,  self.tb.config.vlanName_100,
                                                  self.tb.config.netelem1.tgen.port_b.ifname)
    
        self.localPolicyUdks.policyUdks.Disable_Policy_and_Verify_it_is_Disabled(self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementCliSend.send_cmd( self.tb.config.netelem1.name,  'configure policy slices tci-overwrite 1')
        self.localPolicyUdks.networkElementCliSend.send_cmd( self.tb.config.netelem1.name,  'configure policy slices shared 1')
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Access-List')
        self.localPolicyUdks.networkElementCliSend.send_cmd( self.tb.config.netelem1.name,  "disable clipaging")
        self.localPolicyUdks.networkElementPortGenKeywords.port_enable_state( self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.networkElementPortGenKeywords.port_enable_state( self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_b.ifname)
    
        print(' (Step_2) Test_Setup_Create_and_enable_Radius_Netlogin_and_radius_DynAuth_Server')
        
        self.localPolicyUdks.radiusSuiteUdks.Configure_And_Enable_Radius_Netlogin_Server( self.tb.dut1.name, self.tb.config.endsysRadius.instance, self.tb.config.endsysRadius.ip, self.tb.config.endsysRadius.port , 
                                                                                          self.tb.config.endsysRadius.shared_secret, self.tb.dut1.ip,"VR-Mgmt")
        self.localPolicyUdks.radiusSuiteUdks.Configure_And_Enable_Radius_DynAuth_Server( self.tb.dut1.name, self.tb.config.endsysRadius.instance, self.tb.config.endsysRadius.ip, 
                                                                                         self.tb.config.endsysRadius.shared_secret, self.tb.dut1.ip, "VR-Mgmt")
        
        self.localPolicyUdks.policyUdks.Enable_Policy_and_Verify_it_is_Enabled(self.tb.config.netelem1.name)
        self.localPolicyUdks.macAuthUdks.Enable_Macauth_and_Verify_it_is_Enabled( self.tb.config.netelem1.name)
    #    Enable_Macauth self.tb.config.netelem1.name,
        self.localPolicyUdks.macAuthUdks.Enable_Macauth_Port_and_Verify_it_is_Enabled( self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.macAuthUdks.Enable_Macauth_Port_and_Verify_it_is_Enabled( self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_b.ifname)
    #    enable_macauth_port self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,,self.tb.config.netelem1.tgen.port_b.ifname,
    #
        self.localPolicyUdks.networkElementCliSend.send_cmd( self.tb.config.netelem1.name,  'configure netlogin add mac-list ff:ff:ff:ff:ff:ff 48')
        self.localPolicyUdks.networkElementCliSend.send_cmd( self.tb.config.netelem1.name,  'configure netlogin mac username format none')
    
        print('  (Step_3) setup_connection_to_the_RADIUS_server_to_transmit_COA_requests')
        self.localPolicyUdks.endsystemConnectionMan.connect_to_endsystem_element(self.tb.config.endsysRadius.name,  self.tb.config.endsysRadius.ip,  self.tb.config.endsysRadius.username,
                                                                                         self.tb.config.endsysRadius.password,self.tb.config.endsysRadius.connection_method,self.tb.config.endsysRadius.os)
    
        print('  =======================================================================================================')
        print('  (Init_Interface) compute_the_COA_interface_nbr_from_the_slot_and_port_nbr.')
        print('  IfIndex = port + slot*0x10000, (0x10000 = 65536) - (port_is_formatted_as_port_or_slot:port)')
        print('  =======================================================================================================')
        #${slotNum} =  get_slot_from_port_string   self.tb.config.netelem1.tgen.port_a.ifname,
        #${portNum} =  fetch_from_right   self.tb.config.netelem1.tgen.port_a.ifname,   :
        #coaIfNum  Evaluate  ${portNum} + ${slotNum} * 65536
        # coaIfNum = 0
        coaIfNum = self.tb.config.Port_A_MIB2_IfIndex
        macAuthClient = 3
     
        print( ' (Step_5) Send_Traffic_to_get_Initial_Authentication.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.packetA.src_mac, self.tb.config.packetA.dst_mac, self.tb.config.vlan_100,
             self.tb.config.src_ip_a, self.tb.config.dst_ip_a, self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
    #
        print('  (Step_6) Assign_IP_ipproto_17 (UDP) Forward_access_list_rule_to_the_policy_profile.')
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
             self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_a,  self.tb.config.vlan_400,  coaIfNum,  
             macAuthClient,'\"v:1 t:a m:ipproto=udp a:drop\"')
        time.sleep(int(self.tb.config.policy_delay))
    
        print('  (Verification_6a) Verify_100_ipproto_UDP (17) frames_were_sent_and_Not_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_NOT_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,
             self.tb.config.vlan_100, self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
    
        print('  (Verification_6b) Verify_100_ipproto_TCP (6) frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,     self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,     self.tb.config.vlan_100,
             self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
             self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_a,  self.tb.config.vlan_400,  coaIfNum,  
             macAuthClient,'"v:1 t:d m:ipproto=udp a:drop"')
    #
        print('  (Step_7) Assign_IP_ipproto_6 (TCP) Forward_access_list_rule_to_the_policy_profile.')
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
            self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_a,  self.tb.config.vlan_400,  
            coaIfNum,  macAuthClient, '\"v:1 t:a m:ipproto=tcp a:drop\"')
        time.sleep(int(self.tb.config.policy_delay))
    
        print('  (Verification_7a) Verify_100_ipproto_TCP (6) frames_were_sent_and_Not_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,
             self.tb.config.vlan_100, self.tb.config.src_ip_a, self.tb.config.dst_ip_a, self.tb.config.l4_port_a, self.tb.config.l4_port_b)
    
        print('  (Verification_7b) Verify_100_ipproto_UDP (17) frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,     self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,     self.tb.config.vlan_100,
             self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
             self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_a,  
             self.tb.config.vlan_400,  coaIfNum,  macAuthClient, '\"v:1 t:d m:ipproto=tcp a:drop\"')
    #
        print('  (Step_8) COA: Issue_a_Change_of_Auth_connect_to_deny_TCP_frames_dst_ip_a:l4_port_c')
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
             self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_a,  self.tb.config.vlan_400,
             coaIfNum,  macAuthClient, 
             '\"v:1 t:a m:ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp a:drop\"')
        time.sleep(int(self.tb.config.policy_delay))
    
        print('  (Verification_8a) Verify_100_TCP_frames_with_dst_ip_a:l4_port_c_were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,      self.tb.config.vlan_100,
             self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_8b) Verify_100_TCP_frames_with_non-dst_ip_a:l4_port_b_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,     self.tb.config.vlan_100,
             self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
    
        print('  (Verification_8c) Verify_100_UDP_frames_with_dst_ip_a:l4_port_c_were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,     self.tb.config.vlan_100,
             self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
             self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_a,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
             '\"v:1 t:d m:ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp a:drop\"')
    #
        print('  (Step_9) Assign_IP_ip_source /l4Srcport_access_list_drop_rule_to_the_policy_profile.')
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
             self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_a,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
             '\"v:1 t:a m:ipv4src=' + self.tb.config.src_ip_a + '/32,l4srcport=' + self.tb.config.l4_port_a + '/16,ipproto=tcp a:drop\"')
        time.sleep(int(self.tb.config.policy_delay))
    
        print('  (Verification_9a) Verify_100_TCP_Source_Socket_frames (src_ip_a:l4_port_a) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,      self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,      self.tb.config.vlan_100,
             self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_9b) Verify_100_UDP_Source_Socket_frames (src_ip_a:l4_port_a) were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,     self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,       self.tb.config.vlan_100,
             self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_9c) Verify_100_TCP_Source_Socket_frames (src_ip_a:l4_port_b) were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,      self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,       self.tb.config.vlan_100,
             self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_c)
    
        print('  (Verification_9d) Verify_100_UDP_Source_Socket_frames (src_ip_a:l4_port_b) were_sent_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,      self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,        self.tb.config.vlan_100,
             self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_c)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
             self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip, self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_a,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
             '\"v:1 t:d m:ipv4src=' + self.tb.config.src_ip_a + '/32,l4srcport=' + self.tb.config.l4_port_a + '/16,ipproto=tcp a:drop\"')
    #
        print('  (Step_10) Assign_All_5-tuple_rule_to_the_policy_profile_and_check.')
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
             self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_a,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
             '\"v:1 t:a m:ipv4src=' + self.tb.config.src_ip_a + '/32,l4srcport=' + self.tb.config.l4_port_a + '/16,ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_b + '/16,ipproto=' + 'tcp a:drop\"')
        time.sleep(int(self.tb.config.policy_delay))
    
        print('  (Verification_10a) Verify_100_TCP_Source_Socket_frames (src_ip_a:l4_port_a_dst_ip_b:l4_port_b) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,     self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,       self.tb.config.vlan_100,
             self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
    
        print('  (Verification_10b) Verify_100_UDP_Source_Socket_frames (src_ip_a:l4_port_a_dst_ip_b:l4_port_b) were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,     self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,      self.tb.config.vlan_100,
             self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
    
        print('  (Verification_10c) Verify_100_TCP_Source_Socket_frames (src_ip_a:l4_port_a_dst_ip_b:l4_port_c) were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,     self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,        self.tb.config.vlan_100,
             self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_c)
    
        print('  (Verification_10d) Verify_100_UDP_Source_Socket_frames (src_ip_a:l4_port_a_dst_ip_b:l4_port_c) were_sent_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
             self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,     self.tb.config.packetA.src_mac,    self.tb.config.packetA.dst_mac,        self.tb.config.vlan_100,
             self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_c)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
             self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_a,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
             '\"v:1 t:d m:ipv4src=' + self.tb.config.src_ip_a + '/32,l4srcport=' + self.tb.config.l4_port_a + '/16,ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_b + '/16,ipproto=tcp a:drop\"')
    #self.Test_Case_Cleanup()
    
    def Test_Case_Cleanup(self):
    #    Remove_All_Policy_Rules                         self.tb.config.netelem1.name,
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(self.tb.config.netelem1.name)
        self.localPolicyUdks.Basic_Policy_Cleanup()
        self.localPolicyUdks.policyUdks.Remove_Port_Admin_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                     self.tb.config.profile_a)
    
        self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(
                                               self.tb.config.netelem1.name,  self.tb.config.packetA.dst_mac,   self.tb.config.vlanName_100,  self.tb.config.netelem1.tgen.port_b.ifname)
    
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed( self.tb.config.netelem1.name,  self.tb.config.vlan_100)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed( self.tb.config.netelem1.name,  self.tb.config.vlan_200)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed( self.tb.config.netelem1.name,  self.tb.config.vlan_300)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed( self.tb.config.netelem1.name,  self.tb.config.vlan_400)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed( self.tb.config.netelem1.name,  self.tb.config.vlan_500)
    #    Clear_all_Dot1p_QOS_Profiles                    self.tb.config.netelem1.name,
    #    Configure_Port_Queue_Profile_and_Verify         self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,  ${qos_none}
    #    Remove_QOS_Profile_and_Verify_it_was_Removed    self.tb.config.netelem1.name,  ${qos_profile_all}
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_b.ifname)
    #    Remove_the_RADIUS_configuration
        self.localPolicyUdks.radiusSuiteUdks.UnConfigure_And_Disable_Radius_Netlogin_Server( self.tb.config.netelem1.name,  self.tb.config.endsysRadius.instance)
        self.localPolicyUdks.radiusSuiteUdks.UnConfigure_And_Disable_Radius_DynAuth_Server(  self.tb.config.netelem1.name,  self.tb.config.endsysRadius.instance)
        self.localPolicyUdks.networkElementCliSend.send_cmd( self.tb.config.netelem1.name,  'configure netlogin del mac-list ff:ff:ff:ff:ff:ff 48')
        self.localPolicyUdks.macAuthUdks.Disable_Macauth_and_Verify_it_is_Disabled(self.tb.config.netelem1.name, "")
        self.localPolicyUdks.macAuthUdks.Disable_Macauth_and_Verify_it_is_Disabled(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.macAuthUdks.Disable_Macauth_and_Verify_it_is_Disabled(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.policyUdks.Disable_Policy_and_Verify_it_is_Disabled(  self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementCliSend.send_cmd( self.tb.config.netelem1.name,  'configure policy slices shared 0')
        self.localPolicyUdks.networkElementCliSend.send_cmd( self.tb.config.netelem1.name,  'configure policy slices tci-overwrite 4')
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name,    'Hierarchical')
