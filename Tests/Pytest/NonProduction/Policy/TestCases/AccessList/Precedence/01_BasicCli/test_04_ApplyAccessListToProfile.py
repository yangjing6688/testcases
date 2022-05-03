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

class ApplyAccessListToProfileTests(PolicyBase):
    
    @mark.F_1000_0104
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_04_Assign_Policy_Access_List_to_Policy_Profile_Entries(self):
        '''[Documentation]  Test_Objective: Verify_Access_Lists_can_be_assigned_to_policy_profile_entries.'''
        
    
        print('(Step_1) Basic_Test_Case_Setup. (N/A)')
    
        print('(Step_2) Create_policy_profile, rules, and_admin_port_rule.')
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_a)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_b)
         
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(
                                                     self.tb.config.netelem1.name,  self.tb.config.profile_a ,self.tb.config.vlan_a)
        
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(
                                                     self.tb.config.netelem1.name,self.tb.config.profile_b,  self.tb.config.vlan_a,)
    
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name,'Access-List')
    
        self.localPolicyUdks.Configure_Basic_Single_Match_Access_List_Entries()
        self.localPolicyUdks.Configure_Basic_Multiple_Match_Access_List_Entries()
    
        print('(Step_3) Assign_Access_lists_to_policy_profile_entries')
        
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_profile_name(self.tb.config.netelem1.name, self.tb.config.profile_a, 'AclOne')
        
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_profile_name(self.tb.config.netelem1.name, self.tb.config.profile_b, 'AclTwo')
    
        '''
        CHECKING BY INDEX DOES NOT WORK
        
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_profile_index(self.tb.config.netelem1.name,
                                                                                             'AclOne',self.tb.config.profile_a)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_profile_index(self.tb.config.netelem1.name,'AclTwo',
                                                                                             self.tb.config.profile_b)'''
        
        
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_profile_name(self.tb.config.netelem1.name,
                                                                                             self.tb.config.profile_a,'AclOne')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_profile_name(self.tb.config.netelem1.name,
                                                                                             self.tb.config.profile_b,'AclTwo')
       
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_profile_none(self.tb.config.netelem1.name,
        self.tb.config.profile_a)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_profile_none(self.tb.config.netelem1.name,
                                                                                                 self.tb.config.profile_a)
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_profile_index_none(self.tb.config.netelem1.name,'AclOne')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_profile_index_none(self.tb.config.netelem1.name,'AclTwo')
    
        print('(Step_4) Assign_Non_Existent_Access_lists_to_policy_profile_entries')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_profile_index(self.tb.config.netelem1.name,
                                                                                                  self.tb.config.profile_a,   'AclDoesNotExistYet')
        #verify_policy_acl_profile_index   self.tb.config.netelem1.name,    AclDoesNotExistYet    self.tb.config.profile_a,
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_profile_index(self.tb.config.netelem1.name,
                                                                                             'AclDoesNotExistYet',self.tb.config.profile_a)
        
        #delete_policy_access_list   self.tb.config.netelem1.name,   AclDoesNotExistYet_expect_error=true
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list(self.tb.config.netelem1.name, 'AclDoesNotExistYet',expect_error=True)
        #self.TestCaseCleanup()
    #    
    def Test_Case_Cleanup(self):
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_all_rules(self.tb.config.netelem1.name)
        #delete_policy_access_list_all                    self.tb.config.netelem1.name,
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(self.tb.config.netelem1.name)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_a)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_b)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Hierarchical')