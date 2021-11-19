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

class MirrorActionTests(PolicyBase): 
    @mark.F_1000_0303
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6 
    @mark.WEEKLY
    def test_03_Mirror_Action_for_Policy_Access_Lists(self):
        #[Documentation]  Test_Objective: Verify_An_Access-List_mirror_action_properly_mirrors_frames
        
        print('  (Step_1) Configure_ports, QoS, and_FDB_for_Policy_traffic_tests.)')
        self.tb.config.Policy_Test_Case_Setup_Precedence()
    
        self.localPolicyUdks.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.tb.config.netelem1.name,self.tb.config.vlan_b)
    
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name,    self.tb.config.vlan_b,
                                                                          self.tb.config.netelem1.tgen.port_b.ifname)
                                                                          
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name,    self.tb.config.vlan_b,
                                                                          self.tb.config.netelem1.tgen.port_a.ifname)
    
        print('  (Step_2) Create_A_conduit_for_the_Mirrored_Frames_to_egress')
    #
    #   Put_an_IP_address_on_the_default_Vlan.
    #   Assign_a_FDB_entry_to_a_port_and_then_an_ARP_entry_to_the_FDB_entry
    #   Configure_and_enable_the_syslog_messages_to_be_setn_to_the_IP_address_in_the_ARP_entry.
    #
        self.localPolicyUdks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_c.ifname)
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,'create_mirror_AclTest_to_port ' + self.tb.config.netelem1.tgen.port_c.ifname)
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,'enable_mirror_AclTest_wait_for_prompt=False')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,'y_check_initial_prompt=False_ignore_error=detected_at \'^\' marker')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,'create_mirror_1')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name, 'configure_mirror_1_add_AclTest')
    
        print('  (Step_3) Set_the_policy_rule-model_to_Access-List')
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name,'Access-List')
    
        print('  (Step_4) Create_policy_profile_TCI-Overwrite_Enabled_with_a_default_Drop_Rule')
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(
                                                         self.tb.config.netelem1.name,self.tb.config.profile_a,'0')
        self.localPolicyUdks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                         self.tb.config.profile_a)
    
        print('  (Step_5) Create_default_access_list_rules_with_forward_and_syslog_action.')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name,'AclWithMirror','ether','ether_0x0800',
                                                                                    'mirror-destination_1_forward')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_ether(self.tb.config.netelem1.name, 'AclWithMirror','ether 0x800','16')
        self.localPolicyUdks.networkElementPolicyGenKeywords.verify_policy_acl_action_all(self.tb.config.netelem1.name,
                                             'AclWithMirror','ether','NV','EMPTY','fwrd','EMPTY','1')
    #
    
        print('(Step_6) Assign_ethertype (0x0800) Forward_access_list_rule_to_the_policy_profile. No_Cos_override (cos_3)')
        self.localPolicyUdks.change_policy_access_list_profile_index(self.tb.config.netelem1.name,self.tb.config.profile_a,'AclWithMirror')
    #
    #       Wait_extra_time_for_the_mirror_to_get_programmed
        time.sleep(int(self.tb.config.policy_delay))
    
        print('  (Verification_6a) Verify_100_frames_ethertype_0x0800_were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received_And_Mirrored(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,   self.tb.config.tgen_ports.netelem1.port_c,
              self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,    self.tb.config.vlan_b,
              self.tb.config.src_ip_a,    self.tb.config.dst_ip_a,self.tb.config.l4_port_a,self.tb.config.l4_port_c,)
    
        print('  (Verification_6b) Verify_100_ipx_frames_ethertype (0x8137) were_sent_and_NOT_received.')
        self.localPolicyUdks.Transmit_100_Untagged_Frames_with_ethertype_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,    self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,
              self.tb.config.vlan_a,   self.tb.config.type_ipx)
    #
    #  Reboot_and_make_sure_Mirror_information_is_propery_transferred_to_policy (packets_are_mirrored)..
    #
        print('  (Step_7) Save_config_and_reboot.')
        self.localPolicyUdks.networkElementFileManagementUtilsKeywords.save_current_config(self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementResetDeviceUtilsKeywords.reboot_network_element_now_and_wait(
            self.tb.config.netelem1.name, '180','60','60')
        time.sleep(int(self.tb.config.policy_delay))
        print('(Verification_7a) Verify_100_frames_ethertype_0x0800_were_sent_and_received')
        self.localPolicyUdks.Transmit_100_Untagged_TCP_Frames_and_Verify_Received_And_Mirrored(
              self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.tgen_ports.netelem1.port_c,
              self.tb.config.src_mac_a,self.tb.config.dst_mac_a,self.tb.config.vlan_b,self.tb.config.src_ip_a,self.tb.config.dst_ip_a,self.tb.config.l4_port_a,
              self.tb.config.l4_port_c)
    
        print('  (Verification_7b) Verify_100_ipx_frames_ethertype (0x8137) were_sent_and_NOT_received.')
        self.localPolicyUdks.Transmit_100_Untagged_Frames_with_ethertype_and_Verify_NOT_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,    self.tb.config.dst_mac_a,
              self.tb.config.vlan_a,   self.tb.config.type_ipx)
    
        #self.TestCaseCleanup()
    #
    #
    
    def Test_Case_Cleanup(self):
    #    Remove_All_Policy_Rules                          self.tb.config.netelem1.name,
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(self.tb.config.netelem1.name)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_a)
        
        self.localPolicyUdks.policyUdks.Remove_Port_Admin_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  
                        self.tb.config.netelem1.tgen.port_a.ifname,self.tb.config.profile_a)
    
        self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(
                                    self.tb.config.netelem1.name,self.tb.config.dst_mac_a,self.tb.config.vlan_a,
                                    self.tb.config.netelem1.tgen.port_b.ifname)
    
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,   'disable_mirror_AclTest')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,   'delete_mirror_AclTest')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,'delete_mirror 1')
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,  self.tb.config.vlan_a)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,  self.tb.config.vlan_b)
        self.localPolicyUdks.Clear_all_Dot1p_QOS_Profiles(self.tb.config.netelem1.name)
        self.localPolicyUdks.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,  
                                                                             self.tb.config.qos_none)
        self.localPolicyUdks.cosUdks.Remove_QOS_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name, self.tb.config.qos_profile_all)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_c.ifname)
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name,'Hierarchical')
        
        
        
    #
    #   Save_the "unconfig" here_since_we_did_a_save_and_reboot_test_before - this_should_result_in_a "clean" config
    #
        self.localPolicyUdks.networkElementFileManagementUtilsKeywords.save_current_config(self.tb.config.netelem1.name)



