from Tests.Pytest.Functional.nonprod.Policy.Resources.PolicyBase import PolicyBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.Functional.nonprod.Policy.Resources.Policy_Test_Suite_Udks import Policy_Test_Suite_Udks

@fixture()
def test_setup_teardown(request):
    # Setup_section
    def teardown():
        request.instance.Test_Case_Cleanup()
    request.addfinalizer(teardown)


class TrapActionTests(PolicyBase): 
    @mark.F_1000_0302    
    @mark.Precedence_ACL_Trap    
    
    def test_02_Trap_Action_for_Policy_Access_Lists(self):
        #[Documentation]  Test_Objective: Verify_An_Access-List_with_full_masks_drops_properly (policy_profile_defaulted_to_forward).
        
    
        print('  (Step_1) Configure_ports, QoS, and_FDB_for_Policy_traffic_tests.')
        self.localPolicyUdks.Policy_Test_Case_Setup_Precedence()
    
        self.localPolicyUdks.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.tb.config.netelem1.name,  self.tb.config.vlan_b)
    
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name,
                                    self.tb.config.vlan_b, self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name, self.tb.config.vlan_b,
                                                                          self.tb.config.netelem1.tgen.port_a.ifname)
    
        print('  (Step_2) Create_A_conduit_for_the_Trap_message_to_egress')
    #
    #   Put_an_IP_address_on_the_default_Vlan.
    #   Assign_a_FDB_entry_to_a_port_and_then_an_ARP_entry_to_the_FDB_entry
    #   Configure_and_enable_the_syslog_messages_to_be_setn_to_the_IP_address_in_the_ARP_entry.
    #
        self.localPolicyUdks.interfaceUdks.Configure_Primary_IPv4_Address_Enable_Interface_and_Validate(self.tb.config.netelem1.name,
               self.tb.config.vlan_default,   self.tb.config.vlan_default_ip,   '255.255.255.0')
        self.localPolicyUdks.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.tb.config.netelem1.name,  self.tb.config.dst_mac_c,
                                                                                 self.tb.config.vlan_default , '1')
        self.localPolicyUdks.arpUdks.Add_ARP_Entry_and_Verify_it_was_Added(self.tb.config.netelem1.name,  self.tb.config.dst_ip_c,  self.tb.config.dst_mac_c)
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name, 'configure_snmp_add_trapreceiver ' + self.tb.config.dst_ip_c + ' community_public')
        
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name, 'enable_snmp_traps')
    
        print('  (Step_3) Set_the_policy_rule-model_to_Access-List')
            
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Access-List')
    
        print('  (Step_4) Create_policy_profile_TCI-Overwrite_Enabled_with_a_default_Drop_Rule')
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(
                                                         self.tb.config.netelem1.name,  self.tb.config.profile_a,  '0')
        self.localPolicyUdks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                         self.tb.config.profile_a)
    
        print('  (Step_5) Create_default_access_list_rules_with_forward_and_syslog_action.')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name,'AclWithTrap','ether','ether 0x0800','forward_trap')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_ether(self.tb.config.netelem1.name,'AclWithTrap','ether',
                                                                                     '0x800','16')
        self.localPolicyUdks.networkElementPolicyGenKeywords.verify_policy_acl_action_all(self.tb.config.netelem1.name,'AclWithTrap','ether','NV','T',
                                                                                          'fwrd','EMPTY','EMPTY')
    #
    
        print('  (Step_6) Assign_ethertype (0x0800) Forward_access_list_rule_to_the_policy_profile. No_Cos_override (cos_3)')
        self.localPolicyUdks.change_policy_access_list_profile_index(self.tb.config.netelem1.name,   self.tb.config.profile_a,   'AclWithTrap')
    #
        print('  (Verification_6a) Verify_100_ethertype_0x0800_frames_were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a, self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a, self.tb.config.dst_ip_a, self.tb.config.l4_port_a,    self.tb.config.l4_port_c)
    
        print('  (Verification_6b) Verify_100_ethertype (0x0800) frames_were_sent_and_NOT_received.')
        self.localPolicyUdks.Transmit_100_Untagged_Frames_with_ethertype_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a, self.tb.config.tgen_ports.netelem1.port_b, self.tb.config.src_mac_a, self.tb.config.dst_mac_a,
              self.tb.config.vlan_a,   self.tb.config.type_ipx)
        
        #self.TestCaseCleanup()
            #
    def Test_Case_Cleanup(self):
    #    Remove_All_Policy_Rules                          self.tb.config.netelem1.name,
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(self.tb.config.netelem1.name)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_a)
        self.localPolicyUdks.policyUdks.Remove_Port_Admin_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                     self.tb.config.profile_a)
    
        self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(
                self.tb.config.netelem1.name,  self.tb.config.dst_mac_a,  self.tb.config.vlan_a,  
                                    self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name, 'configure_snmp_del_trapreceiver ' +self.tb.config.dst_ip_c)
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name, 'disable_snmp_traps')
        self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(
                                    self.tb.config.netelem1.name,self.tb.config.dst_mac_c, self.tb.config.vlan_default,'1')
        self.localPolicyUdks.arpUdks.Remove_ARP_Entry_and_verify_it_was_Removed(
                                    self.tb.config.netelem1.name,  self.tb.config.dst_ip_c,  self.tb.config.dst_mac_c)
        self.localPolicyUdks.interfaceUdks.Remove_Primary_IPv4_Address_Interface_and_Validate_Interface_Removed(self.tb.config.netelem1.name,  self.tb.config.vlan_default)
    #
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,  self.tb.config.vlan_a)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,  self.tb.config.vlan_b)
        self.localPolicyUdks.Clear_all_Dot1p_QOS_Profiles(self.tb.config.netelem1.name)
        self.localPolicyUdks.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,  
                                                                             self.tb.config.qos_none)
        self.localPolicyUdks.cosUdks.Remove_QOS_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name, self.tb.config.qos_profile_all)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name,'Hierarchical')



