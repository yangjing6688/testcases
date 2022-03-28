from Tests.Pytest.NonProduction.Policy.Resources.PolicyBase import PolicyBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.NonProduction.Policy.Resources.Policy_Test_Suite_Udks import Policy_Test_Suite_Udks
import time
@fixture()
def test_setup_teardown(request):
     def teardown():
         request.instance.Test_Case_Cleanup()
     request.addfinalizer(teardown)
class ForbiddenVlansTests(PolicyBase):
     @mark.F_127925
     @mark.EXOS
     @mark.P3
     @mark.Policy_Profile
     def test_12_Policy_Profile_Forbidden_VLANs(self):
         '''[Documentation]  Test_Objective: Verify_a_policy_profile_configured_with_forbidden_egress_that_traffic_is_not egressed_out_the_vlan_configured.'''
         print('  (Step_1) Configure_ports, QoS, and_FDB_for_Policy_traffic_tests.')
         self.localPolicyUdks.Policy_Test_Case_Setup_Egress_VLANs()
         print('  (Step_2) Create_policy_profile, rules, and_admin_port_rule.')
         self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.vlan_b)
         self.localPolicyUdks.Configure_Policy_Profile_Forbidden_VLANs(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.vlan_b)
         self.localPolicyUdks.Policy_Profile_Forbidden_VLAN_Should_Contain(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.vlan_b)
         self.localPolicyUdks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname,self.tb.config.profile_a)
         self.localPolicyUdks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_b.ifname,self.tb.config.profile_a)
         time.sleep(int(self.tb.config.policy_delay))
         print('  (Verification_1) Verify_100_untagged_frames_were_sent_and_received_untagged.')
         self.localPolicyUdks.Transmit_100_Untagged_Frames_and_Verify_NOT_Received(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,self.tb.config.dst_mac_a,self.tb.config.vlan_b)
         print('  (Verification_2) Verify_100_untagged_frames_were_sent_and_received_untagged.')
         self.localPolicyUdks.Transmit_100_Untagged_Frames_and_Verify_NOT_Received(self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.dst_mac_a,self.tb.config.src_mac_a,self.tb.config.vlan_b)
         print('  (Verification_3) Verify_Policy_added_the_ports_to_the_forbidden_egress_list_for_vlan_b.')
         self.localPolicyUdks.Port_Should_be_on_Forbidden_Egress(self.tb.config.netelem1.name,self.tb.config.vlan_b,self.tb.config.netelem1.tgen.port_b.ifname)
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
