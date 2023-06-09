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
class PvidStatusTciOverwriteEnabledTests(PolicyBase):
     @mark.F_1000043378
     @mark.EXOS
     @mark.P3
     @mark.Policy_Profile
     def test_03_Policy_Profile_PVID_Status_and_TCI_Overwrite_Enabled(self):
         '''[Documentation]  Test_Objective: Verify_when_TCI_overwrite_is_enabled_and_pvid-status_is_enabled_the_tagged_packet is_associated_to_the_policy_pvid'''
         print('  (Step_1) Configure_ports, QoS, and_FDB_for_Policy_traffic_tests.')
         self.localPolicyUdks.Policy_Test_Case_Setup_Admin_Rules()
         self.localPolicyUdks.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname,self.tb.config.qos_none)
         print('  (Step_2) Create_policy_profile, rules, and_admin_port_rule.')
         self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.vlan_b)
         self.localPolicyUdks.Configure_Policy_Profile_CoS(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.cos_5)
         self.localPolicyUdks.Configure_Policy_Profile_CoS_Status_Disabled(self.tb.config.netelem1.name,self.tb.config.profile_a)
         self.localPolicyUdks.Policy_Profile_CoS_Should_be_Equal(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.cos_5)
         self.localPolicyUdks.Policy_Profile_CoS_Status_Should_be_Disabled(self.tb.config.netelem1.name,self.tb.config.profile_a)
         self.localPolicyUdks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname,self.tb.config.profile_a)
         time.sleep(int(self.tb.config.policy_delay))
         print('  (Verification_1) Verify_100_untagged_frames_were_sent_and_received, with_a_priority_value_of_5.')
         self.localPolicyUdks.Transmit_100_Untagged_Frames_and_Verify_Priority_Changed(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,self.tb.config.dst_mac_a,self.tb.config.vlan_b,self.tb.config.priority_5)
         print('  (Verification_2) Verify_100_priority_tagged_frames_were_sent_and_received, with_a_priority_value_of_0.')
         self.localPolicyUdks.Transmit_100_Priority_Tagged_Frames_and_Verify_Priority_has_NOT_Changed(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,self.tb.config.dst_mac_a,self.tb.config.vlan_b,self.tb.config.priority_2)
         print('  (Verification_3) Verify_100_tagged_frames_were_sent_and_received, with_a_priority_value_of_3.')
         self.localPolicyUdks.Transmit_100_Tagged_Frames_and_Verify_Priority_has_NOT_Changed(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_b,self.tb.config.dst_mac_a,self.tb.config.vlan_a,self.tb.config.priority_6)
         #self.Test_Case_Cleanup()
     def Test_Case_Cleanup(self):
         self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_all_rules(self.tb.config.netelem1.name)
         self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,self.tb.config.profile_a)
         self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(self.tb.config.netelem1.name,self.tb.config.dst_mac_a,self.tb.config.vlan_a,self.tb.config.netelem1.tgen.port_b.ifname)
         self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(self.tb.config.netelem1.name,self.tb.config.dst_mac_a,self.tb.config.vlan_b,self.tb.config.netelem1.tgen.port_b.ifname)
         self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,self.tb.config.vlan_a)
         self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,self.tb.config.vlan_b)
         self.localPolicyUdks.Clear_all_Dot1p_QOS_Profiles(self.tb.config.netelem1.name)
         self.localPolicyUdks.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname,self.tb.config.qos_none)
         #self.localPolicyUdks.cosUdks.Remove_QOS_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,self.tb.config.qos_profile_all)
         self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname)
         self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_b.ifname)
         self.localPolicyUdks.networkElementCosGenKeywords.cos_set_port_qos_profile(self.tb.config.netelem1.name,  self.tb.dut1_tgen_port_a.ifname, 'none')
         self.localPolicyUdks.networkElementCosGenKeywords.cos_delete_qos_profile(self.tb.config.netelem1.name, self.tb.config.qos_profile_all)
