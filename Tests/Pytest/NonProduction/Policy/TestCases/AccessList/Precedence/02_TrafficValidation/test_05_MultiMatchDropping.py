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

class MultiMatchDroppingTests(PolicyBase): 
    @mark.F_1000_0205
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
        
    
    def test_05_Access_List_Multiple_Match_Mixed_Mask_Dropping_Tests(self):
        #[Documentation]  Test_Objective: Verify_Access-List_with_more_than_one_match_condition_drops_properly. (policy_profile_defaulted_to_forward)
        print('  (Step_1) Configure_ports, QoS, and_FDB_for_Policy_traffic_tests.')
        self.localPolicyUdks.Policy_Test_Case_Setup_Precedence()
        self.localPolicyUdks.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.tb.config.netelem1.name,  self.tb.config.vlan_b)
    
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(      self.tb.config.netelem1.name,    self.tb.config.vlan_b,
                                                                          self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(    self.tb.config.netelem1.name,    self.tb.config.vlan_b,
                                                                          self.tb.config.netelem1.tgen.port_a.ifname)
    
        print('  (Step_2) Create_policy_profile, rules, and_admin_port_rule.')
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(
                                                         self.tb.config.netelem1.name,  self.tb.config.profile_a,  self.tb.config.vlan_a)
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_With_PVID_and_PVID_Status_Enabled(
                                                         self.tb.config.netelem1.name,  self.tb.config.profile_b,  self.tb.config.vlan_a)
    
        self.localPolicyUdks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                         self.tb.config.profile_a)
    
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Access-List')
    #       Assign_the_access-list_to_the_policy_profile_entry.
    #
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_profile_index(  self.tb.config.netelem1.name,   self.tb.config.profile_a,  'pV4Sock')
    
    #
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name,'pV4Sock','ipV4SockDrop',
               'ipdestsocket '+ self.tb.config.dst_ip_a + ':' + self.tb.config.l4_port_a + ' mask 48 ' + ' ipsourcesocket ' +  self.tb.config.src_ip_b +':'+self.tb.config.l4_port_b +
                ' mask 48 ','drop')
        
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_ipdestsocket(self.tb.config.netelem1.name,   'pV4Sock', 'ipV4SockDrop', self.tb.config.dst_ip_a+':'+self.tb.config.l4_port_a, 
                                                                                                '48')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_ipsourcesocket(self.tb.config.netelem1.name, 'pV4Sock', 'ipV4SockDrop', self.tb.config.src_ip_b +':'+self.tb.config.l4_port_b, 
                                                                                                    '48')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_drop( self.tb.config.netelem1.name, 'pV4Sock', 'ipV4SockDrop')
    
        time.sleep(int(self.tb.config.policy_delay))# Delay_for_EXOS_policy_hardware_config_batching.
    #
    #      Should_hit_drop_if_src_ip "B" and_port "B" and_dst_ip "A" and_port "A" match.
    #
        print('  (Step_3) Validate_TCP_and_UDP_Traffic_with_configured_Access-List_to_DROP_IpV4_specified_TCP_and_UDP_Frames')
    #
    #      Source_and_dest_IP/Port_match_TCP_frame_should_be_dropped.
    #
        print('  (Verification_3a) Verify_100_TCP_frames_were_sent_and_dropped.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_a)
    #
    #      Source_Dest_port "C" does_not_match_should_forward_by_default.
    #
        print('  (Verification_3b) Verify_100_TCP_frames_were_sent_and_forwarded.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_c)
    #
    #      Source_Port "C" does_not_match_should_forward_by_default.
    
    #
        # level to defaults
        confidenceLevel = 10
        highConfidenceLevel = 8
        #now check to see if they have be changed in yaml
        try:
            newconfidence = self.tb.config.ConfidenceLevel
            confidenceLevel = int(newconfidence)
        except:
            pass
        try:
            newconfidence = self.tb.config.HighConfidence
            highConfidenceLevel = int(newconfidence)
        except:
            pass
        
            
        if  confidenceLevel >= highConfidenceLevel:
             self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
             self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a, self.tb.config.dst_mac_a,    
             self.tb.config.vlan_a, self.tb.config.src_ip_b, self.tb.config.dst_ip_a, self.tb.config.l4_port_c,    self.tb.config.l4_port_a)
    #
    #      Dest_IP "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
             self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
             self.tb.config.tgen_ports.netelem1.port_a, self.tb.config.tgen_ports.netelem1.port_b, self.tb.config.src_mac_a, self.tb.config.dst_mac_a, 
             self.tb.config.vlan_a, self.tb.config.src_ip_b,  self.tb.config.dst_ip_c,  self.tb.config.l4_port_a,    self.tb.config.l4_port_a)
    #
    #      Source_IP "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
            self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
            self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
            self.tb.config.src_ip_c,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_a)
    #
    #      Source_and_dest_IP/Port_match_UDP_frame_should_be_dropped.
    #
        if  confidenceLevel >= highConfidenceLevel:
            self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_NOT_Received(
            self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
            self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_a)
    #
    #      Source_Dest_port "C" does_not_match_should_forward_by_default.
    #
            print('  (Verification_3c) Verify_100_UDP_frames_were_sent_and_forwarded.')
            self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_c)
    #
    #      Source_Port "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_c,    self.tb.config.l4_port_a)
    #
    #      Dest_IP "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_c,    self.tb.config.l4_port_a,    self.tb.config.l4_port_a)
    #
    #      Source_IP "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_c,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_a)
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_profile_index(  self.tb.config.netelem1.name,   self.tb.config.profile_a,    'IpV4Sock')
    #
        print('   (Step_4) Create_a_multi-match_rule_for_tcp_source_and_dest, remove_ip(tcp&udp)Socket')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name, 'IpV4Sock', 'tcpV4SockDrop',
               'tcpdestportip ' + self.tb.config.l4_port_a + ':' + self.tb.config.dst_ip_a + ' mask 48 '+ ' tcpsourceportip ' + self.tb.config.l4_port_b +':' + self.tb.config.src_ip_b + ' mask 48 ',' drop')
            
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_tcpdestportip(    self.tb.config.netelem1.name,     'IpV4Sock','tcpV4SockDrop', self.tb.config.l4_port_a +':' + self.tb.config.dst_ip_a,'48')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_tcpsourceportip(  self.tb.config.netelem1.name,     'IpV4Sock','tcpV4SockDrop' ,  self.tb.config.l4_port_b +':' + self.tb.config.src_ip_b,'48')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_drop(     self.tb.config.netelem1.name,      'IpV4Sock','tcpV4SockDrop')
    
        print('   (Step_5) Remove_prior_rule_IpV4SockDrop_from_access_list')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_rule(   self.tb.config.netelem1.name,'IpV4Sock','tcpV4SockDrop')
        time.sleep(int(self.tb.config.policy_delay)) # Delay_for_EXOS_policy_hardware_config_batching.
    #
    #      Should_hit_drop_if_src_ip "B" and_port "B" and_dst_ip "A" and_port "A" match.
    #
    #
    #      Source_and_dest_IP/Port_match_TCP_frame_should_be_dropped.
    #
        print('  (Step_6) Validate_TCP_and_UDP_Traffic_with_configured_Access-List_to_DROP_IpV4_specified_TCP_Frames')
    #
        print('  (Verification_6a) Verify_100_TCP_frames_were_sent_and_dropped.')
        '''self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_a)'''
    #
    #      Source_Dest_port "C" does_not_match_should_forward_by_default.
    #
        print('  (Verification_6b) Verify_100_TCP_frames_were_sent_and_forwarded.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_c)
    #
    #      Source_Port "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
            self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
            self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
            self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_c,    self.tb.config.l4_port_a)
    #
    #      Dest_IP "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_c,    self.tb.config.l4_port_a,    self.tb.config.l4_port_a)
    #
    #      Source_IP "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
            self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_c,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_a)
    #
    #      Source_and_dest_IP/Port_match_UDP_frame_should_be_dropped.
    #
            print('  (Verification_6c) Verify_100_UDP_frames_were_sent_and_forwarded (match_is_for_TCP_only).')
            self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_a)
    #
    #      Source_Dest_port "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_c)
    #
    #      Source_Port "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_c,    self.tb.config.l4_port_a)
    #
    #      Dest_IP "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_c,    self.tb.config.l4_port_a,    self.tb.config.l4_port_a)
    #
    #      Source_IP "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_c,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_a)
    #
    #
    #
        print('   (Step_7) Create_a_multi-match_rule_for_UDP_source_and_dest, remove_ip(tcp)Socket')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name, 'IpV4Sock','udpV4SockDrop' ,
               'udpdestportip ' + self.tb.config.l4_port_a + ':' + self.tb.config.dst_ip_a +' mask 48 ' + 'udpsourceportip ' + self.tb.config.l4_port_b + ':' +self.tb.config.src_ip_b + ' mask 48', 'drop')
        
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_udpdestportip(self.tb.config.netelem1.name,'IpV4Sock','udpV4SockDrop', self.tb.config.l4_port_a+':'+self.tb.config.dst_ip_a,'48')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_udpsourceportip(self.tb.config.netelem1.name,'IpV4Sock','udpV4SockDrop',  self.tb.config.l4_port_b+':'+self.tb.config.src_ip_b,'48')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_drop(self.tb.config.netelem1.name,'IpV4Sock','udpV4SockDrop')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_rule(   self.tb.config.netelem1.name,'IpV4Sock','udpV4SockDrop')
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    #
    #      Should_hit_drop_if_src_ip "B" and_port "B" and_dst_ip "A" and_port "A" match.
    #
    #
    #      Source_and_dest_IP/Port_match_UDP_frame_should_be_dropped.
    #
        print('  (Step_8) Validate_TCP_and_UDP_Traffic_with_configured_Access-List_to_DROP_IpV4_specified_UDP_Frames')
    #
        print('  (Verification_8a) Verify_100_TCP_frames_were_sent_and_forwarded (match_is_for_UDP_only).')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_a)
    #
    #      Source_Dest_port "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_c)
    #
    #      Source_Port "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_c,    self.tb.config.l4_port_a)
    #
    #      Dest_IP "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_c,    self.tb.config.l4_port_a,    self.tb.config.l4_port_a)
    #
    #      Source_IP "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_c,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_a)
    #
    #      Source_and_dest_IP/Port_match_UDP_frame_should_be_dropped.
    #
        print('  (Verification_8b) Verify_100_UDP_frames_were_sent_and_dropped.')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_a)
    #
    #      Source_Dest_port "C" does_not_match_should_forward_by_default.
    #
        print('  (Verification_8c) Verify_100_UDP_frames_were_sent_and_forwarded.')
        self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_b,    self.tb.config.l4_port_c)
    #
    #      Source_Port "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_c,    self.tb.config.l4_port_a)
    #
    #      Dest_IP "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_b,    self.tb.config.dst_ip_c,    self.tb.config.l4_port_a,    self.tb.config.l4_port_a)
    #
    #      Source_IP "C" does_not_match_should_forward_by_default.
    #
        if  confidenceLevel >= highConfidenceLevel:
              self.localPolicyUdks.Transmit_100_Untagged_UDP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_c,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_a)
    #
    #
        #self.TestCaseCleanup()
    #
    #
    def Test_Case_Cleanup (self):
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Access-List')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_all_rules(self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(  self.tb.config.netelem1.name)
        self.localPolicyUdks.policyUdks.Remove_Port_Admin_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                     self.tb.config.profile_a)
        #Remove_Port_Admin_Profile   self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_port_admin_profile(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        #self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(, Ignore_CLI_Feedback    self.tb.config.netelem1.name,    self.tb.config.vlan_b,
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_a)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_b)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(  self.tb.config.netelem1.name)
        self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(
                                    self.tb.config.netelem1.name,  self.tb.config.dst_mac_a,      self.tb.config.vlan_a,  self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,  self.tb.config.vlan_a)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,  self.tb.config.vlan_b)
        self.localPolicyUdks.Clear_all_Dot1p_QOS_Profiles(self.tb.config.netelem1.name)
        self.localPolicyUdks.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,  self.tb.config.qos_none)
        #self.localPolicyUdks.cosUdks.Remove_QOS_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.qos_profile_all)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.networkElementCosGenKeywords.cos_set_port_qos_profile(self.tb.config.netelem1.name,  self.tb.dut1_tgen_port_a.ifname, 'none')
        self.localPolicyUdks.networkElementCosGenKeywords.cos_delete_qos_profile(self.tb.config.netelem1.name, self.tb.config.qos_profile_all)
        #
        #self.localPolicyUdks.change_policy_rule_model(   self.tb.config.netelem1.name, 'Hierarchical')