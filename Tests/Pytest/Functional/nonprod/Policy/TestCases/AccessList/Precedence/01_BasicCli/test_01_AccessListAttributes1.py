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

class AccessListAttributesTests(PolicyBase):
    @mark.F_1000_0101
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_01_Create_Policy_Access_List_Single_Match_CLI_Validation (self):
       '''[Documentation]  Test_Objective: Verify_Policy_Access_Lists_with_single_match_conditions_can_be_programmed_properly.'''
        
    
       print('(Step_1) Basic_Test_Case_Setup. (N/A)')
       
       self.localPolicyUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name,self.tb.config.netelem1.ip,self.tb.config.netelem1.username,
                                                                                           self.tb.config.netelem1.password,'telnet',self.tb.config.netelem1.os,exos_auth_mode='basic')
       print('(Step_2) Switch_to_Access-List_Rule_Model')
       
           
       self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(self.tb.config.netelem1.name,  self.tb.config.profile_a
                                                                                                              ,self.tb.config.vlan_a)
       self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Access-List')
    
       print('(Step_3) Run_Test_in_CLI_Mode')
       self.TestCaseBody()
    
       
       '''
       REST NOT Supported at this time
       print('(Step_4) Switch_to_REST')
       self.localPolicyUdks.networkElementConnectionManager.close_connection_to_network_element(self.tb.config.netelem1.name)
       self.localPolicyUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name,self.tb.config.netelem1.ip,self.tb.config.netelem1.username,
                                                                                           self.tb.config.netelem1.password,'rest',self.tb.config.netelem1.os,exos_auth_mode='basic')
    
       print('(Step_5) Run_Test_in_REST_Mode')
       self.Test_Case_Body()
    
       print('(Step_6) Return_to_Telnet')
       self.localPolicyUdks.networkElementConnectionManager.close_connection_to_network_element(self.tb.config.netelem1.name)
       self.localPolicyUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name,self.tb.config.netelem1.ip,self.tb.config.netelem1.username,
                                                                                           self.tb.config.netelem1.password,'telnet',self.tb.config.netelem1.os,exos_auth_mode='basic')
       '''
       #self.TestCaseCleanup()
    #
    #
    def TestCaseBody (self,):
       print('  (Test_Step_1) Create_policy_profile, rules, and_admin_port_rule.')
       self.localPolicyUdks.Configure_Basic_Single_Match_Access_List_Entries()
         #
         #   Delete_a_couple_rules_and_verify_they_don't_exist.
         #
       print('(Test_Step_2) Delete_a_couple_rules_and_verify_they_don\'t_exist.')
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_rule(self.tb.config.netelem1.name,'IpV4a','tcpdestportIP')
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_rule_does_not_exist(self.tb.config.netelem1.name,'IpV4a','tcpdestportIP')
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_rule(self.tb.config.netelem1.name,'IpV4','ipttl')
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_rule_does_not_exist(self.tb.config.netelem1.name,'IpV4','ipttl')
         #
         #  Recreate_a_deleted_entry_and_verify_it_can_be_recreated, then_delete_again_and_verify.
         #
       print('(Test_Step_3) Recreate_a_deleted_entry_and_verify_it_can_be_recreated, then_delete_again_and_verify.')
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name,'IpV4a','tcpdestportIP','tcpdestportip '+ self.tb.config.l4_port_c+':'+self.tb.config.dst_ip_a + ' mask 16','drop mirror-destination 1')
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_tcpdestportip(self.tb.config.netelem1.name,'IpV4a','tcpdestportIP',self.tb.config.l4_port_c,'16')
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.tb.config.netelem1.name,'IpV4a','tcpdestportIP','NV','','drop','','1')
    
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_rule(self.tb.config.netelem1.name,'IpV4a','tcpdestportIP')
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_rule_does_not_exist(self.tb.config.netelem1.name,'IpV4a','tcpdestportIP')
    
       print('(Test_Step_4) Delete_a_complete_access_list_and_verify_it_does_not_exist.')
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list(self.tb.config.netelem1.name,'IpV4a')
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_rule_does_not_exist(self.tb.config.netelem1.name,'IpV4a')
         #   Delete_the_rest_of_the_rules/access_lists_and_check_a_couple_of_things_that_were_present_that_should_have_been_deleted.
         #
       print('(Test_Step_5) Delete_all_access_lists_and_spot_verify_entries_do_not_exist.')
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(self.tb.config.netelem1.name)
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_rule_does_not_exist(self.tb.config.netelem1.name,'IpV4a','iptos')
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_rule_does_not_exist(self.tb.config.netelem1.name,'IpV4a','udpsourceportIP')
       self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_does_not_exist(self.tb.config.netelem1.name,'IpV4')
    
    
    def Test_Case_Cleanup(self):
        #
        #  In_case_REST_tests_fail, set_back_to_telnet_mode.
        #
        '''self.localPolicyUdks.networkElementConnectionManager.close_connection_to_network_element(self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name,self.tb.config.netelem1.ip,self.tb.config.netelem1.username,
                                                                                           self.tb.config.netelem1.password,'telnet',self.tb.config.netelem1.os,exos_auth_mode='basic')'''
        
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(self.tb.config.netelem1.name)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name, self.tb.config.profile_a)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_b.ifname)
        #self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Hierarchical')