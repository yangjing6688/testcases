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

class SingleMatchForwardingTests(PolicyBase): 
    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6 
    def test_02_Access_List_Single_Match_Full_Mask_Forwarding_Tests(self):
        '''[Documentation]  Test_Objective: Verify_An_Access-List_with_full_masks_Forwards_properly (policy_profile_defaulted_to_drop)'''
        
        print('  (Step_1) Configure_ports, QoS, and_FDB_for_Policy_traffic_tests.')
        self.localPolicyUdks.Policy_Test_Case_Setup_Precedence()
    
        self.localPolicyUdks.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.tb.config.netelem1.name,  self.tb.config.vlan_b)
    
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name,    self.tb.config.vlan_b,
                                                                          self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(    self.tb.config.netelem1.name,    self.tb.config.vlan_b,
                                                                          self.tb.config.netelem1.tgen.port_a.ifname)
    
        self.localPolicyUdks.change_policy_rule_model(   self.tb.config.netelem1.name,    'Access-List')
    
        print('  (Step_2) Create_policy_profile_TCI-Overwrite_Enabled_with_a_default_Drop_Rule')
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(
                                                         self.tb.config.netelem1.name,  self.tb.config.profile_a,  '0')
        self.localPolicyUdks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(  self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                         self.tb.config.profile_a)
    
        print('  (Step_3) Create_default_access_list_rules_with_forward_action.')
        self.localPolicyUdks.Create_And_Verify_Separate_List_Single_Match_Access_List_Entries('true','forward','fwrd')
    
    #
    #
        print('  (Step_4) Assign_icmp_Forward_access_list_rule_to_the_policy_profile. override:(cos_5)')
        self.localPolicyUdks.change_policy_access_list_profile_index(  self.tb.config.netelem1.name,   self.tb.config.profile_a,    'fwrdicmptype')
        time.sleep(int(self.tb.config.policy_delay))# Delay_for_EXOS_policy_hardware_config_batching.
    
        print('  (Verification_4a) Verify_ICMP_100 (type_8_code_0) frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_IPv4_ICMP_Frames_and_Verify_Priority_Changed(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_b,
              self.tb.config.priority_5,    self.tb.config.src_ip_a,  self.tb.config.dst_ip_a,   None,   None,   None,  None,   '8','0')
    
        print('  (Verification_4b) Verify_ICMP_100 (type_3_code_0) frames_were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_IPv4_ICMP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_b,
              self.tb.config.src_ip_a,  self.tb.config.dst_ip_a,   None,   None,   None,  None,   '3','0')
    
        print('  (Verification_4c) Verify_100_TCP_frames_were_sent_and_NOT_received. (default_policy_rule_is_to_drop)')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    #
    #
    #
        print('  (Step_5) Assign_ethertype (0x0800) Forward_access_list_rule_to_the_policy_profile. No_Cos_override (cos_3)')
        self.localPolicyUdks.change_policy_access_list_profile_index(   self.tb.config.netelem1.name,   self.tb.config.profile_a,   'fwrdether')
    
        print('  (Verification_5a) Verify_100_ethertype_0x0800_frames_were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Priority_Changed(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.priority_3,   self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_5b) Verify_100_ethertype (non_0x0800) frames_were_sent_and_NOT_received.')
        self.localPolicyUdks.Transmit_100_Untagged_Frames_with_ethertype_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,
              self.tb.config.vlan_b,   self.tb.config.type_ipx)
    #
    #
    #
        print('  (Step_6) !!!SKIPPING!!! Assign_icmp6type_Forward_access_list_rule_to_the_policy_profile_override:(cos_5).')
    #       self.localPolicyUdks.change_policy_access_list_profile_index(   self.tb.config.netelem1.name,   self.tb.config.profile_a,   fwrdicmp6type
    #
    #   print('  (Verification_6a) Verify_100_IPV6_ICMP_frames (type_222_code_173) were_sent_and_received
    #        self.localPolicyUdks.Transmit_100_Untagged_IPv6_ICMP_Frames_and_Verify_Priority_Changed
    #          self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
    #          self.tb.config.priority_5,  self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,   icmp_type=222_code=173
    #
    #   print('  (Verification_6a) Verify_100_IPV6_ICMP_frames_non_matching_type/code_were_sent_and_NOT_received
    #       self.localPolicyUdks.Transmit_100_Untagged_IPv6_ICMP_Frames_and_Verify_NOT_Received
    #          self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
    #          self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,   icmp_type=22_code=73
    #
    #   print('  (Verification_6c) Verify_100_Non_IPv6_ICMP_frames_were_sent_and_NOT_received.
    #        self.localPolicyUdks.Transmit_100_Untagged_IPv6_Frames_and_Verify_NOT_Received
    #          self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
    #          self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,
    #
    #
    #
        print('  (Step_7) Assign_IP_Dest_Socket_Forward (dst_ip_a:l4_port_c) access_list_rule_to_the_policy_profile.')
        self.localPolicyUdks.change_policy_access_list_profile_index(   self.tb.config.netelem1.name,   self.tb.config.profile_a,   'fwrdipdestsocket')
    
        print('  (Verification_7a) Verify_100_TCP_frames_with_matching_dst_ip_a:l4_port_c_were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_7b) Verify_100_TCP_frames_with_non-matching_dst_ip_a:l4_port_b_were_sent_and_NOT_received.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
    #
        '''
        print('  (Step_8) Assign_IP_Fragment_Forward_access_list_rule_to_the_policy_profile.')
        self.localPolicyUdks.change_policy_access_list_profile_index(   self.tb.config.netelem1.name,   self.tb.config.profile_a,   'fwrdipfrag')
    
        print('  (Verification_8a) Verify_100_fragmented_frames_were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_IP_Frag_Frames_and_Verify_Received(
                  self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_b,  self.tb.config.dst_mac_a,  self.tb.config.vlan_b,
                  self.tb.config.src_ip_a,   self.tb.config.dst_ip_a,  self.tb.config.pkt_id,   self.tb.config.mf_flag,  self.tb.config.no_offset)
    
        print('  (Verification_8b) Verify_100_non_fragmented_frames_frames_were_sent_but_NOT_received.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
        '''
    #
        print('  (Step_9) Assign_IP_ipproto_17 (UDP) Forward_access_list_rule_to_the_policy_profile.')
        self.localPolicyUdks.change_policy_access_list_profile_index(   self.tb.config.netelem1.name,   self.tb.config.profile_a,   'fwrdipproto')
    
        print('  (Verification_9a) Verify_100_ipproto_UDP (17) frames_were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Priority_Changed(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.priority_5,  self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
    
        print('  (Verification_9b) Verify_100_ipproto_TCP (6) frames_were_sent_but_NOT_received.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
    #
    #
    #
        print('  (Step_10) Assign_IP_ip_source_socket_Forward_access_list_rule_to_the_policy_profile.')
        self.localPolicyUdks.change_policy_access_list_profile_index(   self.tb.config.netelem1.name,   self.tb.config.profile_a,   'fwrdipSsock')
    
        print('  (Verification_10a) Verify_100_ip_Source_Socket_frames (src_ip_a:l4_port_a) were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Priority_Changed(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.priority_5,  self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_10b) Verify_100_ip_Source_Socket_frames (src_ip_a:l4_port_a) were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Priority_Changed(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.priority_5,  self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_10a) Verify_100_TCP_Source_Socket_frames (src_ip_a:l4_port_b) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_c)
    
        print('  (Verification_10a) Verify_100_UDP_Source_Socket_frames (src_ip_a:l4_port_b) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_c)
    
    #
    #
    #
        print('  (Step_11) Assign_IP_iptos_Forward_access_list_rule_to_the_policy_profile.')
        self.localPolicyUdks.change_policy_access_list_profile_index(   self.tb.config.netelem1.name,   self.tb.config.profile_a,   'fwrdiptos')
    
        print('  (Verification_11a) Verify_100_frames_iptos_of_31_were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c,  tos='31')
    
        print('  (Verification_11b) Verify_100_frames_iptos_of_15_were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c,  tos='15')
    
    #
    #
    #
        print('  (Step_12) Assign_IP_ipttl_Forward_access_list_rule_to_the_policy_profile.')
        self.localPolicyUdks.change_policy_access_list_profile_index(   self.tb.config.netelem1.name,   self.tb.config.profile_a,   'fwrdipttl')
    
        print('  (Verification_12a) Verify_100_frames_ipttl_of_10_were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c,  ttl='10')
    
        print('  (Verification_12b) Verify_100_frames_ipttl_of_5_were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c,  ttl='5')
    
    #
    #
    #
        print('  (Step_13) Assign_IP_tcpdestportip_Forward_access_list_rule_to_the_policy_profile.')
        self.localPolicyUdks.change_policy_access_list_profile_index(   self.tb.config.netelem1.name,   self.tb.config.profile_a,   'fwrdtcpDportIP')
    
        print('  (Verification_13a) Verify_100_TCP_frames_dest:(l4_port_c:dst_ip_a) were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_13b) Verify_100_UDP_frames_dest:(l4_port_c:dst_ip_a) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_13c) Verify_100_TCP_frames_dest:(l4_port_a:dst_ip_a) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_a)
    
        print('  (Verification_13d) Verify_100_UDP_frames_dest:(l4_port_b:src_ip_a) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_b)
    #
    #
    #
        print('  (Step_14) Assign_IP_tcpsourceportip_Forward_access_list_rule_to_the_policy_profile.')
        self.localPolicyUdks.change_policy_access_list_profile_index(   self.tb.config.netelem1.name,   self.tb.config.profile_a,   'fwrdtcpSportIP')
    
        print('  (Verification_14a) Verify_100_TCP_frames_src:(l4_port_a:dst_ip_a) were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Priority_Changed(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.priority_5,  self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_14b) Verify_100_UDP_frames_src:(l4_port_c:dst_ip_a) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,     self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_14c) Verify_100_TCP_frames_src:(l4_port_a:dst_ip_a) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_a)
    
        print('  (Verification_14d) Verify_100_UDP_frames_src:(l4_port_b:src_ip_a) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_b)
    
    #
    #
    #
        print('  (Step_15) Assign_IP_udpdestportip_Forward_access_list_rule_to_the_policy_profile.')
        self.localPolicyUdks.change_policy_access_list_profile_index(   self.tb.config.netelem1.name,   self.tb.config.profile_a,   'fwrdudpDportIP')
    
        print('  (Verification_15a) Verify_100_UDP_frames_dest:(l4_port_c:dst_ip_a) were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Priority_Changed(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.priority_5,  self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_15b) Verify_100_TCP_frames_dest:(l4_port_c:dst_ip_a) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_15c) Verify_100_UDP_frames_dest:(l4_port_a:dst_ip_a) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_a)
    
        print('  (Verification_15d) Verify_100_TCP_frames_dest:(l4_port_a:src_ip_a) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_a)
    
    #
    #
    #
        print('  (Step_16) Assign_IP_udpdestportip_Forward_access_list_rule_to_the_policy_profile.')
        self.localPolicyUdks.change_policy_access_list_profile_index(   self.tb.config.netelem1.name,   self.tb.config.profile_a,   'fwrdudpSportIP')
    
        print('  (Verification_16a) Verify_100_UDP_frames_dest:(l4_port_a:src_ip_a) were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_16b) Verify_100_TCP_frames_dest:(l4_port_a:src_ip_a) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_16c) Verify_100_UDP_frames_dest:(l4_port_b:src_ip_a) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_a)
    
        print('  (Verification_16d) Verify_100_TCP_frames_dest:(l4_port_b:src_ip_a) were_sent_and_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_a)    
    
        #self.TestCaseCleanup()#
    
    def Test_Case_Cleanup(self):
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Access-List')
        #self.localPolicyUdks.TestCaseCleanupTrafficValidation()
    #    Remove_All_Policy_Rules                          self.tb.config.netelem1.name,
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(  self.tb.config.netelem1.name)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(  self.tb.config.netelem1.name,  self.tb.config.profile_a)
        self.localPolicyUdks.policyUdks.Remove_Port_Admin_Profile_and_Verify_it_was_Removed(    self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                     self.tb.config.profile_a)    
        self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(
                                    self.tb.config.netelem1.name,  self.tb.config.dst_mac_a,      self.tb.config.vlan_a,  self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,  self.tb.config.vlan_a)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,  self.tb.config.vlan_b)
        self.localPolicyUdks.Clear_all_Dot1p_QOS_Profiles(self.tb.config.netelem1.name)
        self.localPolicyUdks.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,  self.tb.config.qos_none)
        #self.localPolicyUdks.cosUdks.Remove_QOS_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.qos_profile_all)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_b.ifname)
        #self.localPolicyUdks.change_policy_rule_model(   self.tb.config.netelem1.name,    'Hierarchical')
        self.localPolicyUdks.networkElementCosGenKeywords.cos_set_port_qos_profile(self.tb.config.netelem1.name,  self.tb.dut1_tgen_port_a.ifname, 'none')
        self.localPolicyUdks.networkElementCosGenKeywords.cos_delete_qos_profile(self.tb.config.netelem1.name, self.tb.config.qos_profile_all)
     