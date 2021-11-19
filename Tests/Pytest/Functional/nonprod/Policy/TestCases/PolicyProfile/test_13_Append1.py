from Tests.Pytest.Functional.nonprod.Policy.Resources.PolicyBase import PolicyBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.Functional.nonprod.Policy.Resources.Policy_Test_Suite_Udks import Policy_Test_Suite_Udks
import time
@fixture()
def test_setup_teardown(request):
     def teardown():
         request.instance.Test_Case_Cleanup()
     request.addfinalizer(teardown)
class AppendTests(PolicyBase):
     @mark.F_1000043389
     @mark.EXOS
     @mark.P3
     @mark.Policy_Profile
     def test_13_Policy_Profile_Append(self):
         '''[Documentation]  Test_Objective: Verify_the_append_command_adds_the_vlans_to_the_new_egress_lists_without_clearing the_current_egress_configuration.'''
         print('  (Step_1) Configure_ports, QoS, and_FDB_for_Policy_traffic_tests.')
         self.localPolicyUdks.Policy_Test_Case_Setup_Egress_VLANs()
         print('  (Step_2) Create_policy_profile, rules, and_admin_port_rule.')
         self.localPolicyUdks.Create_Policy_Profile_and_Verify_it_Exists(self.tb.config.netelem1.name,self.tb.config.profile_a)
         self.localPolicyUdks.Configure_Policy_Profile_Untagged_VLANs(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.vlan_a)
         self.localPolicyUdks.Policy_Profile_Untagged_VLAN_Should_Contain(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.vlan_a)
         time.sleep(int(self.tb.config.policy_delay))
         print('  (Verification_1) Verify_policy_profile_can_be_modified_with_the \'append\' option.')
         self.localPolicyUdks.Configure_Policy_Profile_Egress_VLANs(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.vlan_b,append=True)
         self.localPolicyUdks.Policy_Profile_Untagged_VLAN_Should_Contain(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.vlan_a)
         self.localPolicyUdks.Policy_Profile_Egress_VLAN_Should_Contain(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.vlan_b)
         #self.Test_Case_Cleanup()
     def Test_Case_Cleanup(self):
         self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_all_rules(self.tb.config.netelem1.name)
         self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,self.tb.config.profile_a)
         self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,self.tb.config.vlan_a)
         self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,self.tb.config.vlan_b)
         self.localPolicyUdks.Clear_all_Dot1p_QOS_Profiles(self.tb.config.netelem1.name)
         self.localPolicyUdks.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname,self.tb.config.qos_none)
         #self.localPolicyUdks.cosUdks.Remove_QOS_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,self.tb.config.qos_profile_all)
         self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname)
         self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_b.ifname)
         self.localPolicyUdks.networkElementCosGenKeywords.cos_set_port_qos_profile(self.tb.config.netelem1.name,  self.tb.dut1_tgen_port_a.ifname, 'none')
         self.localPolicyUdks.networkElementCosGenKeywords.cos_delete_qos_profile(self.tb.config.netelem1.name, self.tb.config.qos_profile_all)
