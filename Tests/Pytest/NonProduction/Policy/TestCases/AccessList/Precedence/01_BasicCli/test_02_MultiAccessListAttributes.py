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

class MultiAccessListAttributesTests(PolicyBase):
    @mark.F_1000_0102
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_02_Create_Policy_Access_List_Multi_Match_CLI_Validation(self,):
        '''[Documentation]  Test_Objective: Verify_Policy_Access_Lists_with_multiple_match_conditions_can_be_programmed_properly.'''
        
        print('(Step_1) Basic_Test_Case_Setup. (N/A)')
        self.localPolicyUdks.networkElementConnectionManager.change_netelem_connection_agent(self.tb.config.netelem1.name,  'telnet')
    
        print('(Step_2) Create_policy_profile, rules, and_admin_port_rule.')
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(self.tb.config.netelem1.name,  self.tb.config.profile_a
                        ,self.tb.config.vlan_a)
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Access-List')
    
        print('(Step_3) Run_Test_in_CLI_Mode')
        self.TestCaseBody()
        '''print('(Step_4) Switch_to_Rest')
        self.localPolicyUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name,  self.tb.config.netelem1.ip,  self.tb.config.netelem1.username,  self.tb.config.netelem1.password,  'rest',
                                                                                          self.tb.config.netelem1.os,self.tb.config.netelem1.os,exos_auth_mode='basic')
    
        print('(Step_5) Run_Test_in_REST_Mode')
        self.Test_Case_Body()
    
        print('(Step_6) Return_to_telnet')
        self.localPolicyUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name,  self.tb.config.netelem1.ip,  self.tb.config.netelem1.username,  self.tb.config.netelem1.password,  'telnet',
                                 self.tb.config.netelem1.os,exos_auth_mode='basic')'''    
        #self.TestCaseCleanup()
  
    def TestCaseBody(self,):
        #
        #  Create_and_verify_a "standard" set_of_rules.
        #
        self.localPolicyUdks.Configure_Basic_Multiple_Match_Access_List_Entries()
    
        print('(Test_Step_1) Delete_a_rule_and_verify_it_doesn\'t_exist.')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_rule(self.tb.config.netelem1.name,'AclTwo','FivePart')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_rule_does_not_exist(self.tb.config.netelem1.name,'AclTwo','FivePart')
        #
        #  Recreate_a_deleted_entry_and_verify_it_can_be_recreated, then_delete_again_and_verify.
        #
        print('(Test_Step_2) Recreate_a_deleted_entry_and_verify_it_can_be_recreated, then_delete_again_and_verify.')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name,'AclTwo','FivePart',
         'tcpdestportip ' + self.tb.config.l4_port_c + ':' + self.tb.config.dst_ip_a + ' mask 16'+' tcpsourceportip '+ self.tb.config.l4_port_b + ':' +self.tb.config.dst_ip_b + ' mask 16 iptos 128 '+' ipttl 128' +
        ' ether 0x0800 mask 8','drop syslog cos ' + self.tb.config.cos_5 + ' mirror-destination 2')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_tcpdestportip(self.tb.config.netelem1.name,'AclTwo','FivePart',self.tb.config.l4_port_c, '16')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_tcpsourceportip(self.tb.config.netelem1.name,'AclTwo','FivePart',self.tb.config.l4_port_b,'16')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_ether(self.tb.config.netelem1.name,'AclTwo','FivePart','0x800','8')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_iptos(self.tb.config.netelem1.name,'AclTwo','FivePart','128')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_ipttl(self.tb.config.netelem1.name,'AclTwo','FivePart','128')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.tb.config.netelem1.name,'AclTwo','FivePart','NV','S','drop', self.tb.config.cos_5,'2')
        #
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_rule(self.tb.config.netelem1.name,'AclTwo','FivePart')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_rule_does_not_exist(self.tb.config.netelem1.name, 'AclTwo','FivePart')
    
        #
        #   Delete_the_rest_of_the_rules/access_lists_and_check_a_couple_of_things_that_were_present_that_should_have_been_deleted.
        #
        print('(Test_Step_3) Delete_a_complete_access_list_and_verify_it_does_not_exist.')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list(self.tb.config.netelem1.name,    'AclOne')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_does_not_exist(self.tb.config.netelem1.name,'AclOne')
        #
        #   Delete_the_rest_of_the_rules/access_lists_and_check_a_couple_of_things_that_were_present_that_should_have_been_deleted.
        #
        print('(Test_Step_4) Delete_all_access_lists_and_spot_verify_entries_do_not_exist.')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_rule_does_not_exist(self.tb.config.netelem1.name,'AclTwo','FourPart')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_rule_does_not_exist( self.tb.config.netelem1.name, 'AclOne','ThreeFull')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_does_not_exist(self.tb.config.netelem1.name, 'AclTwo')
    
    def Test_Case_Cleanup(self,):
        #
        #  In_case_REST_tests_fail, set_back_to_'telnet',_mode.
        # 
        #no need until rest is supported       
        '''self.localPolicyUdks.networkElementConnectionManager.close_connection_to_network_element(self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name,  self.tb.config.netelem1.ip,  
                                                                                        self.tb.config.netelem1.username,  self.tb.config.netelem1.password,'telnet',
                                                                                        self.tb.config.netelem1.os,exos_auth_mode='basic')'''
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(self.tb.config.netelem1.name)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_a)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Hierarchical')