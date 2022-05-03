from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementPolicyGenKeywords import NetworkElementPolicyGenKeywords


class PolicySuiteUdks():
    def __init__(self) -> None:
        self.networkElementPolicyGenKeywords = NetworkElementPolicyGenKeywords()

    # EXOS DEFINED
    def Cleanup_any_policy_that_might_be_present_where_we_are_going_to_create_them(self, netelem_name, policyId_a, policyId_b, policyId_c, vlan_100, vlan_200, vlan_300, policyName_a, policyName_b, policyName_c):
        self.networkElementPolicyGenKeywords.policy_clear_profile(netelem_name, policyId_a)
        self.networkElementPolicyGenKeywords.policy_clear_profile(netelem_name, policyId_a)
        self.networkElementPolicyGenKeywords.policy_clear_profile(netelem_name, policyId_a)
        # Create the policies that we are going to use..
        self.networkElementPolicyGenKeywords.Create_Policy_Profile_With_PVID_and_PVID_Status_Enabled(netelem_name, policyId_a, vlan_100)
        self.networkElementPolicyGenKeywords.Create_Policy_Profile_With_PVID_and_PVID_Status_Enabled(netelem_name, policyId_b, vlan_200)
        self.networkElementPolicyGenKeywords.Create_Policy_Profile_With_PVID_and_PVID_Status_Enabled(netelem_name, policyId_c, vlan_300)
        self.networkElementPolicyGenKeywords.Create_Policy_Profile_and_Verify_it_Exists(netelem_name, policyId_a, policyName_a)
        self.networkElementPolicyGenKeywords.Create_Policy_Profile_and_Verify_it_Exists(netelem_name, policyId_b, policyName_b)
        self.networkElementPolicyGenKeywords.Create_Policy_Profile_and_Verify_it_Exists(netelem_name, policyId_c, policyName_c)
        # Create Port Admin Profile and Verify it Exists  ${netelem1.name}  ${netelem1.tgen.port_a.ifname}  ${policyId_a}
        self.networkElementPolicyGenKeywords.policy_set_maptable_response(netelem_name, 'policy')
        
    def Basic_Policy_Cleanup(self, netelem_name, policyId_a, policyId_b, policyId_c):
        self.Remove_Policy_Profile_and_Verify_it_was_Removed(netelem_name, policyId_a)
        self.Remove_Policy_Profile_and_Verify_it_was_Removed(netelem_name, policyId_b)
        self.Remove_Policy_Profile_and_Verify_it_was_Removed(netelem_name, policyId_c)
        # Remove Port Admin Profile and Verify it was Removed  ${netelem1.name}  ${netelem1.tgen.port_a.ifname}  ${policyId_a}
        self.networkElementPolicyGenKeywords.policy_set_maptable_response(netelem_name, 'policy')
