from Tests.Pytest.NonProduction.Policy.Resources.PolicyBase import PolicyBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.NonProduction.Policy.Resources.Policy_Test_Suite_Udks import Policy_Test_Suite_Udks

@fixture()
def test_setup_teardown(request):
    # Setup_section
    def teardown():
        request.instance.Test_Case_Cleanup()
    request.addfinalizer(teardown)

class DiagnoseTest(PolicyBase): 
    @mark.F_1000_0299    

    def test_01_Verify_Precedence_of_Access_List_Match_Entries(self):
        '''[Documentation]  Test_Objective: Verify_Access-List_for_ipdestination_socket_forward/drop_precedence_is_correct.
           for_UnTagged_Frames'''
        
    
        print('  (Step_1) Configure_ports, QoS, and_FDB_for_Policy_traffic_tests.')
        self.localPolicyUdks.Policy_Test_Case_Setup_Precedence()
    
        self.localPolicyUdks.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.tb.config.netelem1.name,self.tb.config.vlan_b)
    
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.nameself.tb.config.vlan_b,
                                                                          self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name,    self.tb.config.vlan_b,
                                                                          self.tb.config.netelem1.tgen.port_a.ifname)
    
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name,'Access-List')
    
        print('  (Step_2) Create_policy_profile_TCI-Overwrite_Enabled_with_a_default_Forward_Rule')
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(
                                                         self.tb.config.netelem1.name,  self.tb.config.profile_a,  self.tb.config.vlan_a)
    #        Create_Port_Admin_Profile  self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,
    #                                                     self.tb.config.profile_a,
    #BGC_BUG_self.localPolicyUdks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(  self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,
    #BGC_BUG                                                     self.tb.config.profile_a,
        self.localPolicyUdks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(  self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_a.ifname,
                                                        self.tb.config.profile_a)
    
        print('  (Step_3) Create_default_access_list_rules_with_forward_action.')
        self.localPolicyUdks.Create_And_Verify_Separate_List_Single_Match_Access_List_Entries('true','drop','drop')
    
    #
    #
    
    #
    #
    #
        print('  (Step_6) Assign_icmp6type_Forward_access_list_rule_to_the_policy_profile_override:(cos_5).')
        self.localPolicyUdks.change_policy_access_list_profile_index(self.tb.config.netelem1.name, self.tb.config.profile_a,'dropicmp6type')
    
        print('  (Verification_6a) Verify_100_IPV6_ICMP_frames (type_222_code_173) were_sent_but_NOT_received')
        self.localPolicyUdks.Transmit_100_Untagged_IPv6_ICMP_Frames_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,   icmp_type='222',_code='173')
    
        print('  (Verification_6b) Verify_100_IPV6_ICMP_frames_non_matching_type/code_were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_IPv6_ICMP_Frames_and_Verify_Priority_Changed(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.priority_3,   self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,   icmp_type='22',code='73')
    
        print('  (Verification_6c) Verify_100_Non_IPv6_ICMP_frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_IPv6_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_a,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a)
    
        #self.Test_Case_Cleanup()
    #
    def Test_Case_Cleanup(self):
    #    Remove_All_Policy_Rules                          self.tb.config.netelem1.name,
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all( self.tb.config.netelem1.name)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_a)
        self.localPolicyUdks.policyUdks.Remove_Port_Admin_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                     self.tb.config.profile_a)
    
        self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(
                                    self.tb.config.netelem1.name,  self.tb.config.dst_mac_a,      self.tb.config.vlan_a,  self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,  self.tb.config.vlan_a)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,  self.tb.config.vlan_b)
        self.localPolicyUdks.Clear_all_Dot1p_QOS_Profiles(self.tb.config.netelem1.name)
        self.localPolicyUdks.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname,self.tb.config.qos_none)
        #self.localPolicyUdks.cosUdks.Remove_QOS_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.qos_profile_all)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_b.ifname)
        #self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name,'Hierarchical',reEnablePolicy='false')
        self.localPolicyUdks.networkElementCosGenKeywords.cos_set_port_qos_profile(self.tb.config.netelem1.name,  self.tb.dut1_tgen_port_a.ifname, 'none')
        self.localPolicyUdks.networkElementCosGenKeywords.cos_delete_qos_profile(self.tb.config.netelem1.name, self.tb.config.qos_profile_all)