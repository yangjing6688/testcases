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

class NegativeTestingTests(PolicyBase):
    
    @mark.F_1000_0106
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6    
    def test_06_Negative_Policy_Access_List_Testing(self):
        #[Documentation]  Test_Objective: Check_that_tests_that_should_fail_actually_fail.
        
        print('(Step_1) Basic_Test_Case_Setup. (N/A)')
        self.localPolicyUdks.networkElementConnectionManager.change_netelem_connection_agent(self.tb.config.netelem1.name,'telnet')
    
        print('(Step_2) Create_policy_profile, rules, and_admin_port_rule.')
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(
                                                         self.tb.config.netelem1.name,  self.tb.config.profile_a,  self.tb.config.vlan_a)
    
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(
                                                         self.tb.config.netelem1.name,  self.tb.config.profile_b, self.tb.config.vlan_a)
    
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name,'Access-List')
    
        print('(Step_3) Run_Test_in_CLI_Mode')
        self.TestCaseBody()
    
        '''
        REST NOT SUPPORTED AT THIS TIME
        print('(Step_4) Switch_to_REST')
        self.localPolicyUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name,  self.tb.config.netelem1.ip,  self.tb.config.netelem1.username,  
                                                                                        self.tb.config.netelem1.password, 'rest',self.tb.config.netelem1.os, exos_auth_mode='basic')
    
        print('Step_5) Run_Test_in_REST_Mode')
        self.Test_Case_Body()
    
        print('(Step_6) Return_to_Telnet')
        self.localPolicyUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name, self.tb.config.netelem1.ip, self.tb.config.netelem1.username,  
                                                                                        self.tb.config.netelem1.password,  'telnet',self.tb.config.netelem1.os , exos_auth_mode='basic')
        '''
         #
         #  Test_each_individual_rule_type_with_varying_actions....
         #
    
        #self.TestCaseCleanup()
    
    
    #
    
    def TestCaseBody(self):
        print('(Test) Do_some_stuff_we_don\'t_expect_to_work.')
    
        print('(Test_Step_1) AccessList.Name_more_that_31_chars_each.')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(  self.tb.config.netelem1.name,
           'WickedLong-AccessList-OverLength1.WickedLong-AccessList-OverLength2', 'icmptype','icmptype 4.4','cos ' + self.tb.config.cos_5 + ' ' + 'mirror-destination 1',
           expect_error=True)
    
        print('(Test_Step_2) AccessList.Name_more_that_31_chars_total.')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name,'WickedLong.AccessList-OverLength1',
                                                                                    'icmptype','icmptype 4.4','cos ' + self.tb.config.cos_5 + ' mirror-destination 1',
                                                                                    expect_error=True)
    
        print('(Test_Step_3) AccessList_missing_match_criteria')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(self.tb.config.netelem1.name,'Legit_Matches','EMPTY', 
                                                                                      'cos ' + self.tb.config.cos_5 + ' ' + 'mirror-destination 1',
                                                                                      expect_error=True)
    
        print('(Test_Step_4) AccessList.Name_Missing_action_criteria')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list(  self.tb.config.netelem1.name,'Legit_Actions','icmptype 4.4','EMPTY',
                                                                                      expect_error=True)
    
        self.localPolicyUdks.networkElementConnectionManager.change_netelem_connection_agent(self.tb.config.netelem1.name,  'telnet')
    
        print('(Test_Step_5) AccessList.Name_more_that_31_chars_each_in_policy_assignment.')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_profile_index(self.tb.config.netelem1.name,self.tb.config.profile_a,
                                                                                                  'WickedLong-AccessList-OverLength1',expect_error=True)
    
    def Test_Case_Cleanup(self):
        #        
        '''self.localPolicyUdks.networkElementConnectionManager.close_connection_to_network_element(self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name,self.tb.config.netelem1.ip,self.tb.config.netelem1.username,
                                                                                           self.tb.config.netelem1.password,'telnet',self.tb.config.netelem1.os,exos_auth_mode='basic')'''
       
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(self.tb.config.netelem1.name)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_a)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_b)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name,'Hierarchical')