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

class ConfigRestoreAfterRebootTests(PolicyBase):
    @mark.F_1000_0103
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_03_Create_Policy_Access_List_Config_Restore_Validation(self):
        '''[Documentation]  Test_Objective: Verify_Policy_Access_Lists_are_restored_properly_after_a_reboot.'''
        print('(Step_1) Basic_Test_Case_Setup. (N/A)')
    
        print('(Step_2) Configure_rule_model_to_access-list')
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name,'Access-List')
    
         #
         #  Create_basic_single_and_multi_match_access_list_rules.
         #
        self.localPolicyUdks.Configure_Basic_Single_Match_Access_List_Entries()
        self.localPolicyUdks.Configure_Basic_Multiple_Match_Access_List_Entries()
    
        print('(Step_3) Save_config_and_reboot.')
             
        self.localPolicyUdks.networkElementFileManagementUtilsKeywords.save_current_config(self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementResetDeviceUtilsKeywords.reboot_network_element_now_and_wait(self.tb.config.netelem1.name, '180',
                                                                                                        '60','60')
    
        print('(Step_4) Verify_the_entries_are_correct_after_a_reboot.')
        self.localPolicyUdks.Verify_Basic_Single_Match_Access_List_Entries()
        self.localPolicyUdks.Verify_Basic_Multiple_Match_Access_List_Entries()
    
    
    #        Delete_the_rest_of_the_rules/access_lists_and_check_a_couple_of_things_that_were_present_that_should_have_been_deleted.
         #
        # there is no keyword for the below will use the clear command for now 
        #delete_policy_access_list_all  self.tb.config.netelem1.name,
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(self.tb.config.netelem1.name)
    
        #self.TestCaseCleanup()
    #
    
    def Test_Case_Cleanup(self):
        #delete_policy_access_list_all  self.tb.config.netelem1.name,
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(self.tb.config.netelem1.name)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_a)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Hierarchical')