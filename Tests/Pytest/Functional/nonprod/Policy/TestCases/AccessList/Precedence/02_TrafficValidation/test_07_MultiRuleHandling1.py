from Tests.Pytest.Functional.nonprod.Policy.Resources.PolicyBase import PolicyBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.Functional.nonprod.Policy.Resources.Policy_Test_Suite_Udks import Policy_Test_Suite_Udks
import time
@fixture()
def test_setup_teardown(request):
    # Setup_section
    def teardown():
        request.instance.Test_Case_Cleanup()
    request.addfinalizer(teardown)
    
class MultiRuleHandlingTests(PolicyBase): 
    @mark.F_1000_0207
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_05_Access_List_Multiple_Match_Mixed_Mask_Dropping_Tests(self):
        '''[Documentation]  Test_Objective: Verify_Access-List_for_ipdestination_socket_forward/drop_precedence_is_correct.
           for_UnTagged_Frames'''
            
        print('  (Step_1) Configure_ports, QoS, and_FDB_for_Policy_traffic_tests.')
        self.localPolicyUdks.Policy_Test_Case_Setup_Precedence()
        self.localPolicyUdks.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.tb.config.netelem1.name, self.tb.config.vlan_b)
    
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name, self.tb.config.vlan_b,
                                                                          self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name,    self.tb.config.vlan_b,
                                                                          self.tb.config.netelem1.tgen.port_a.ifname)
    
        print('  (Step_2) Create_policy_profile, rules, and_admin_port_rule.')
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(
                                                         self.tb.config.netelem1.name,  self.tb.config.profile_a,  self.tb.config.vlan_a)
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_With_PVID_and_PVID_Status_Enabled(
                                                         self.tb.config.netelem1.name,self.tb.config.profile_b, self.tb.config.vlan_a)
    
        self.localPolicyUdks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                         self.tb.config.profile_a)
    
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Access-List')
    
    #       Assign_the_access-list_to_the_policy_profile_entry.
    #
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_profile_index(self.tb.config.netelem1.name,   
                                                                                                  self.tb.config.profile_a,    'IpV4DstSock')
    
         #  Create_an_access_list_as_follows:
         #        drop_IP_frames_with_ip_Address self.tb.config.dst_ip_a,: TCPdestPort self.tb.config.l4_port_c,
         #        forward_IP_frames_with_ip_address self.tb.config.dst_ip_a, (all_other_l4_ports_for_example)
         #        drop_ip_frames (ethertype_0x0800)
         #   Vlan_will_be_picked_up_based_on_policy_profile_settings
         #
         # Access-List_entries_First_In_is_Highest_precedence_wise
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name, 'IpV4DstSock', 'ipdestsocketDropPort', 'ipdestsocket ' + self.tb.config.dst_ip_a + ':' +
                                                                                    self.tb.config.l4_port_c + ' mask 48','drop')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_ipdestsocket(self.tb.config.netelem1.name,'IpV4DstSock', 'ipdestsocketDropPort', self.tb.config.dst_ip_a + ':' + self.tb.config.l4_port_c, '48')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_drop(self.tb.config.netelem1.name,'IpV4DstSock','ipdestsocketDropPort')
            #
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name,'IpV4DstSock','ipdestsocketFwd','ipdestsocket ' + self.tb.config.dst_ip_a + ' mask 32', 'forward')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_ipdestsocket(self.tb.config.netelem1.name,'IpV4DstSock','ipdestsocketFwd',   self.tb.config.dst_ip_a, '32')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_forward(self.tb.config.netelem1.name,'IpV4DstSock','ipdestsocketFwd')    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name,'IpV4DstSock','ether', 'ether  0x0800','drop')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_ether(self.tb.config.netelem1.name,'IpV4DstSock','ether', '0x800', '16')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_drop(self.tb.config.netelem1.name,'IpV4DstSock','ether')
    
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    #
    #      Should_hit_ipdestsocketDropPort
    #
        print('  (Step_3) Validate_Traffic_with_configured_Access-List_using_profile_a (TCI_overrwrite_enabled).')
        print('  (Verification_3a) Verify_100_frames_were_sent_and_dropped_with_IP/l4_dest_that_should_drop.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    #
    #      Should_hit_Forward_rule_ipDestsocketFwd, as_dst_port_does_not_match_ipdestsocketDropPort
    #
        print('  (Verification_3b) Verify_100_frames_were_sent_and_received_with_IP/l4_dest_that_should_forward.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
    #
    #      Should_hit_ether_0x0800_drop_as_the_IP_addres_does_not_match_the_ipdestsocket_access-list_entries.
    #
        print('  (Verification_3c) Verify_100_frames_were_sent_and_dropped_due_to_ether_rule_when_other_rules_are_not_hit')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_b,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    #
    #       Should_not_hit_any_Access-list_entry, should_forward_based_on_default_forwarding_rules..
    #
        print('  (Verification_3d) Verify_100_frames_were_sent_Should_not_hit_any_Access-list_entry, should_forward_based_on_default_forwarding_rules..')
        self.localPolicyUdks.Transmit_100_Untagged_IPv6_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_b)
    
        print('  (Step_4) Move_Ether_Drop_Rule_Above_ipv4destsocket_forward_rule_and_verify_traffic_is_handled_correctly.')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_before(self.tb.config.netelem1.name,'IpV4DstSock','ether','IpV4DstSock','ipdestsocketFwd')
    
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.g
        print('  (Verification_4a) Verify_100_frames_were_sent_and_dropped_with_IP/l4_dest_that_should_drop.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    #
    #      Should_hit_Forward_rule_ipDestsocketFwd, as_dst_port_does_not_match_ipdestsocketDropPort
    #
        print('  (Verification_4b) Verify_100_frames_were_sent_and_received_with_IP/l4_dest_that_should_drop (due_to_moved_EtherRule).')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
    #
    #      Should_hit_ether_0x0800_drop_as_the_IP_addres_does_not_match_the_ipdestsocket_access-list_entries.
    #
        print('  (Verification_4c) Verify_100_frames_were_sent_and_dropped_due_to_ether_rule_when_other_rules_are_not_hit')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_b,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    #
    #       Should_not_hit_any_Access-list_entry, should_forward_based_on_default_forwarding_rules..
    #
        print('  (Verification_4d) Verify_100_frames_were_sent_Should_not_hit_any_Access-list_entry, should_forward_based_on_default_forwarding_rules..')
        self.localPolicyUdks.Transmit_100_Untagged_IPv6_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_b)
    #
    #
    #
        print('  (Step_5) Repeat_Tests_With_TCI_Overrwrite_Disabled (profile_b)')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(  self.tb.config.netelem1.name)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name, self.tb.config.profile_a)
    
        self.localPolicyUdks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname,
                                                         self.tb.config.profile_b)
         # Access-List_entries_First_In_is_Highest_precedence_wise
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name,'IpV4DstSock','ipdestsocketDropPort',
                                                                                    'ipdestsocket ' + self.tb.config.dst_ip_a + ':' + self.tb.config.l4_port_c + ' mask 48', 'drop')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_ipdestsocket(self.tb.config.netelem1.name,'IpV4DstSock', 'ipdestsocketDropPort',  self.tb.config.dst_ip_a + ':' + self.tb.config.l4_port_c, '48')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_drop(self.tb.config.netelem1.name,'IpV4DstSock', 'ipdestsocketDropPort')
            #
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name,'IpV4DstSock','ipdestsocketFwd', 'ipdestsocket ' + self.tb.config.dst_ip_a + ' mask 32','forward')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_ipdestsocket(self.tb.config.netelem1.name,'IpV4DstSock', 'ipdestsocketFwd', self.tb.config.dst_ip_a,'32')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_forward(self.tb.config.netelem1.name,'IpV4DstSock','ipdestsocketFwd')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name,'IpV4DstSock','ether', 'ether 0x0800','drop')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_ether(self.tb.config.netelem1.name,'IpV4DstSock','ether','0x800','16')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_drop(self.tb.config.netelem1.name,'IpV4DstSock','ether')
    
    
    #       Assign_the_access-list_to_the_policy_profile_entry.
    #
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_profile_index(self.tb.config.netelem1.name,self.tb.config.profile_b,'IpV4DstSock')
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    #
    #      Should_hit_ipdestsocketDropPort
    #
        print('  (Step_6) Validate_Traffic_with_configured_Access-List')
        print('  (Verification_6a) Verify_100_frames_were_sent_and_dropped_with_IP/l4_dest_that_should_drop.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    #
    #      Should_hit_Forward_rule_ipDestsocketFwd, as_dst_port_does_not_match_ipdestsocketDropPort
    #
        print('  (Verification_6b) Verify_100_frames_were_sent_and_received_with_IP/l4_dest_that_should_forward.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
    #
    #      Should_hit_ether_0x0800_drop_as_the_IP_addres_does_not_match_the_ipdestsocket_access-list_entries.
    #
    
        print('  (Verification_6c) Verify_100_frames_were_sent_and_dropped_due_to_ether_rule_when_other_rules_are_not_hit')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_b,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    #
    #       Should_not_hit_any_Access-list_entry, should_forward_based_on_default_forwarding_rules..
    #
        print('  (Verification_6d) Verify_100_frames_were_sent_Should_not_hit_any_Access-list_entry, should_forward_based_on_default_forwarding_rules..')
        self.localPolicyUdks.Transmit_100_Untagged_IPv6_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_b)
    
        print('  (Step_7) Move_Ether_Drop_Rule_Above_ipv4destsocket_forward_rule_and_verify_traffic_is_handled_correctly.')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_before( self.tb.config.netelem1.name,'IpV4DstSock','ether','IpV4DstSock','ipdestsocketFwd')
    
        time.sleep(int(self.tb.config.policy_delay))# Delay_for_EXOS_policy_hardware_config_batching.g
        print('  (Verification_7a) Verify_100_frames_were_sent_and_dropped_with_IP/l4_dest_that_should_drop.')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    #
    #      Should_hit_Forward_rule_ipDestsocketFwd, as_dst_port_does_not_match_ipdestsocketDropPort
    #
        print('  (Verification_7b) Verify_100_frames_were_sent_and_received_with_IP/l4_dest_that_should_drop (due_to_moved_EtherRule).')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,    self.tb.config.l4_port_a,    self.tb.config.l4_port_b)
    #
    #      Should_hit_ether_0x0800_drop_as_the_IP_addres_does_not_match_the_ipdestsocket_access-list_entries.
    #
        print('  (Verification_7c) Verify_100_frames_were_sent_and_dropped_due_to_ether_rule_when_other_rules_are_not_hit')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_b,    self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    #
    #       Should_not_hit_any_Access-list_entry, should_forward_based_on_default_forwarding_rules..
    #
        print('  (Verification_7d) Verify_100_frames_were_sent_Should_not_hit_any_Access-list_entry, should_forward_based_on_default_forwarding_rules..')
        self.localPolicyUdks.Transmit_100_Untagged_IPv6_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,    self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_b)
        # 
        #self.Test_Case_Cleanup()
        
    def Test_Case_Cleanup(self):
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Access-List')
    #BGC_BUG_Remove_All_Policy_Rules                          self.tb.config.netelem1.name,
    #BGC_BUG_self.localPolicyUdks.policyUdks.Remove_Port_Admin_Profile_and_Verify_it_was_Removed(   self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,
    #BGC_BUG                                                 self.tb.config.profile_a,
        
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_port_admin_profile( self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed_Ignore_CLI_Feedback(self.tb.config.netelem1.name,    self.tb.config.vlan_b)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_a)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_b)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(  self.tb.config.netelem1.name)
        self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(
                                    self.tb.config.netelem1.name,  self.tb.config.dst_mac_a,      self.tb.config.vlan_a,  self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed( self.tb.config.netelem1.name,  self.tb.config.vlan_a)
        self.localPolicyUdks.Clear_all_Dot1p_QOS_Profiles(self.tb.config.netelem1.name)
        self.localPolicyUdks.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname,self.tb.config.qos_none)
        #self.localPolicyUdks.cosUdks.Remove_QOS_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,self.tb.config.qos_profile_all)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled( self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_b.ifname)
        #self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name,    'Hierarchical')
        self.localPolicyUdks.networkElementCosGenKeywords.cos_set_port_qos_profile(self.tb.config.netelem1.name,  self.tb.dut1_tgen_port_a.ifname, 'none')
        self.localPolicyUdks.networkElementCosGenKeywords.cos_delete_qos_profile(self.tb.config.netelem1.name, self.tb.config.qos_profile_all)