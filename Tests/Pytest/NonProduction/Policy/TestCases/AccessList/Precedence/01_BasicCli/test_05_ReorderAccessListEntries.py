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

class ReorderAccessListEntriesTests(PolicyBase):
        
    @mark.F_1000_0105
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_05_Reorder_Policy_Access_List_Entries(self):
        #[Documentation]  Test_Objective: Verify_Access_Lists_Entries_Can_Be_Reordered.
        print('(Step_1) Basic_Test_Case_Setup. (N/A)')
    
        print('  (Step_2) Create_policy_profile, rules, and_admin_port_rule.')
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(
                                                      self.tb.config.netelem1.name,  self.tb.config.profile_a,  self.tb.config.vlan_a)
    
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(
                                                      self.tb.config.netelem1.name,  self.tb.config.profile_b,  self.tb.config.vlan_a)
    
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name,'Access-List')
    
    #    Configure_Basic_Single_Match_Access_List_Entries
        self.localPolicyUdks.Configure_Basic_Multiple_Match_Access_List_Entries()
    
        print('(Step_2) Move_things_around_using_each_of_After_Before_First_Last')
         # AclOne_TwoFull_ThreeFull_TwoPart_ThreePart
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
         '[\\s\\S]*AclOne[\\s\\S]*TwoFull[\\s\\S]*ThreeFull[\\s\\S]*TwoPart[\\s\\S]*ThreePart')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_after(self.tb.config.netelem1.name, 
                                                                                                          'AclOne','TwoFull','AclOne','ThreeFull')
         # AclOne_ThreeFull_TwoFull_TwoPart_ThreePart
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
         '[\\s\\S]*AclOne[\\s\\S]*ThreeFull[\\s\\S]*TwoFull[\\s\\S]*TwoPart[\\s\\S]*ThreePart')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_before(self.tb.config.netelem1.name,   
                                                                                                           'AclOne','ThreePart','AclOne','TwoPart')
         # AclOne_ThreeFull_TwoFull_ThreePart_TwoPart
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
                            '[\\s\\S]*AclOne[\\s\\S]*ThreeFull[\\s\\S]*TwoFull[\\s\\S]*ThreePart[\\s\\S]*TwoPart')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_first(self.tb.config.netelem1.name,   
                                                                                                          'AclOne','ThreePart')
         # AclOne_ThreePart_ThreeFull_TwoFull_TwoPart
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show policy access-list',
         '[\\s\\S]*AclOne[\\s\\S]*ThreePart[\\s\\S]*ThreeFull[\\s\\S]*TwoFull[\\s\\S]*TwoPart')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_last(self.tb.config.netelem1.name,
                                                                                                         'AclOne','ThreeFull')
         # AclOne_ThreePart_TwoFull_TwoPart_ThreeFull
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
         '[\\s\\S]*AclOne[\\s\\S]*ThreePart[\\s\\S]*TwoFull[\\s\\S]*TwoPart[\\s\\S]*ThreeFull')
    
        print('(Step_3) Issue_the_same_commands_but_in_a_way_such_as_they_don\'t_actually_move_anything')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_after(self.tb.config.netelem1.name,
                                                                                                          'AclOne','ThreeFull','AclOne','ThreeFull')
         # AclOne_ThreePart_TwoFull_TwoPart_ThreeFull
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
         '[\\s\\S]*AclOne[\\s\\S]*ThreePart[\\s\\S]*TwoFull[\\s\\S]*TwoPart[\\s\\S]*ThreeFull')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_after(self.tb.config.netelem1.name,   
                                                                                                          'AclOne','ThreeFull', 'AclOne','TwoPart')
         # AclOne_ThreePart_TwoFull_TwoPart_ThreeFull
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
         '[\\s\\S]*AclOne[\\s\\S]*ThreePart[\\s\\S]*TwoFull[\\s\\S]*TwoPart[\\s\\S]*ThreeFull')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_before(self.tb.config.netelem1.name,
                                                                                                           'AclOne','TwoFull','AclOne','TwoFull')
         # AclOne_ThreePart_TwoFull_TwoPart_ThreeFull
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,'show policy access-list',
                                                                                '[\\s\\S]*AclOne[\\s\\S]*ThreePart[\\s\\S]*TwoFull[\\s\\S]*TwoPart[\\s\\S]*ThreeFull')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_before(self.tb.config.netelem1.name, 'AclOne',
                                                                                                           'TwoFull','AclOne','TwoPart')
        
         # AclOne_ThreePart_TwoFull_TwoPart_ThreeFull
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,'show policy access-list',
                                                                                '[\\s\\S]*AclOne[\\s\\S]*ThreePart[\\s\\S]*TwoFull[\\s\\S]*TwoPart[\\s\\S]*ThreeFull')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_first(self.tb.config.netelem1.name, 'AclOne','ThreePart')
         #  AclOne_ThreePart_TwoFull_TwoPart_ThreeFull
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
                                                                                '[\\s\\S]*AclOne[\\s\\S]*ThreePart[\\s\\S]*TwoFull[\\s\\S]*TwoPart[\\s\\S]*ThreeFull')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_last(self.tb.config.netelem1.name,'AclOne','ThreeFull')
         # AclOne_ThreePart_TwoFull_TwoPart_ThreeFull
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
                                                                                '[\\s\\S]*AclOne[\\s\\S]*ThreePart[\\s\\S]*TwoFull[\\s\\S]*TwoPart[\\s\\S]*ThreeFull')    
         #
        print('(Step_4) Issue_First_command_for_each_element_starting_with_the_last_finishing_with_the_second')
         #
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_first(self.tb.config.netelem1.name, 'AclOne','ThreeFull')
         # AclOne_ThreeFull_ThreePart_TwoFull_TwoPart
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
                                                                                '[\\s\\S]*AclOne[\\s\\S]*ThreeFull[\\s\\S]*ThreePart[\\s\\S]*TwoFull[\\s\\S]*TwoPart')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_first(self.tb.config.netelem1.name, 'AclOne', 'TwoFull')
         # AclOne_TwoFull_ThreeFull_ThreePart_TwoPart
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
        '[\\s\\S]*AclOne[\\s\\S]*TwoFull[\\s\\S]*ThreeFull[\\s\\S]*ThreePart[\\s\\S]*TwoPart')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_first(self.tb.config.netelem1.name, 'AclOne','ThreeFull')
         # AclOne_ThreeFull_TwoFull_ThreePart_TwoPart
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,'show policy access-list',
         '[\\s\\S]*AclOne[\\s\\S]*ThreeFull[\\s\\S]*TwoFull[\\s\\S]*ThreePart[\\s\\S]*TwoPart')
        #
        print('(Step_4) Issue_Last_command_for_each_element_starting_with_the_First_finishing_with_the_next_to_last')
         #
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_last(self.tb.config.netelem1.name,'AclOne','ThreeFull')
         # AclOne_TwoFull_ThreePart_TwoPart_ThreeFull
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,'show policy access-list',
                                                                                '[\\s\\S]*AclOne[\\s\\S]*TwoFull[\\s\\S]*ThreePart[\\s\\S]*TwoPart[\\s\\S]*ThreeFull')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_last(self.tb.config.netelem1.name,'AclOne','ThreePart')
         # AclOne_TwoFull_TwoPart_ThreeFull_ThreePart
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
                                                                                '[\\s\\S]*AclOne[\\s\\S]*TwoFull[\\s\\S]*TwoPart[\\s\\S]*ThreeFull[\\s\\S]*ThreePart')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_last(self.tb.config.netelem1.name,'AclOne','ThreeFull')
         # AclOne_TwoFull_TwoPart_ThreePart_ThreeFull
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
                                                                                '[\\s\\S]*AclOne[\\s\\S]*TwoFull[\\s\\S]*TwoPart[\\s\\S]*ThreePart[\\s\\S]*ThreeFull')
        
        print('  (Step_5) Issue_Before_command_for_each_element_starting_with_the_Last_finishing_with_the_Second')
         #
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_before(self.tb.config.netelem1.name, 'AclOne','ThreeFull',
                                                                                                           'AclOne','ThreePart')
         # AclOne_TwoFull_TwoPart_ThreeFull_ThreePart
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,'show policy access-list',
                                                                                '[\\s\\S]*AclOne[\\s\\S]*TwoFull[\\s\\S]*TwoPart[\\s\\S]*ThreeFull[\\s\\S]*ThreePart')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_before(self.tb.config.netelem1.name, 'AclOne',
                                                                                                           'ThreeFull','AclOne','TwoPart')
         #  AclOne_TwoFull_ThreeFull_TwoPart_ThreePart
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,'show policy access-list',
                                                                                '[\\s\\S]*AclOne[\\s\\S]*TwoFull[\\s\\S]*ThreeFull[\\s\\S]*TwoPart[\\s\\S]*ThreePart')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_before(self.tb.config.netelem1.name,'AclOne',
                                                                                                           'ThreeFull','AclOne','TwoFull')
         # AclOne_ThreeFull_TwoFull_TwoPart_ThreePart
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,'show policy access-list',
                                                                                '[\\s\\S]*AclOne[\\s\\S]*ThreeFull[\\s\\S]*TwoFull[\\s\\S]*TwoPart[\\s\\S]*ThreePart')
        #
        print('(Step_6) Issue_After_command_for_each_element_starting_with_the_First_finishing_with_the_next_to_last')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_after(self.tb.config.netelem1.name, 
                                                                                                          'AclOne','ThreeFull','AclOne','TwoFull')
         # AclOne_TwoFull_ThreeFull_TwoPart_ThreePart
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
                                                                                 '[\\s\\S]*AclOne[\\s\\S]*TwoFull[\\s\\S]*ThreeFull[\\s\\S]*TwoPart[\\s\\S]*ThreePart')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_after(self.tb.config.netelem1.name,'AclOne',
                                                                                                          'ThreeFull','AclOne','TwoPart')
         # AclOne_TwoFull_TwoPart_ThreeFull_ThreePart
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
                                                                                '[\\s\\S]*AclOne[\\s\\S]*TwoFull[\\s\\S]*TwoPart[\\s\\S]*ThreeFull[\\s\\S]*ThreePart')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_rule_precedence_after(self.tb.config.netelem1.name,
                                                                                                          'AclOne','ThreeFull','AclOne','ThreePart')
        
         # AclOne_TwoFull_TwoPart_ThreePart_ThreeFull
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,'show policy access-list',
                                                                                '[\\s\\S]*AclOne[\\s\\S]*TwoFull[\\s\\S]*TwoPart[\\s\\S]*ThreePart[\\s\\S]*ThreeFull')
        
        #self.TestCaseCleanup()
    #
    #
    def Test_Case_Cleanup (self):
    #    Remove_All_Policy_Rules                          self.tb.config.netelem1.name,
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_all(self.tb.config.netelem1.name)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_a)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_b)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Hierarchical')