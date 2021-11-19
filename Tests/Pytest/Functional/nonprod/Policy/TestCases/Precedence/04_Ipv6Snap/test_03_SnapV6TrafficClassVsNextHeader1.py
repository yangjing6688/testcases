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
class TrafficClassVsNextHeaderTests(PolicyBase):
     @mark.F_1000043263
     @mark.EXOS
     @mark.P2
     @mark.Precedence
     @mark.Precedence_IpV6Snap
     @mark.NIGHTLY
     def test_03_IPv6_SNAP_Precedence_Traffic_Class_vs_Next_Header(self):
         '''[Documentation]  Test_Objective: Verify_macsource_policy_rules_associate_traffic_correctly_for_unlearned/learned unicast, broadcast_and_multicast_frames_when_TCI-Overwrite_is_disabled.'''
         print('  (Step_1) Configure_ports, QoS, and_FDB_for_Policy_traffic_tests.')
         self.localPolicyUdks.Policy_Test_Case_Setup_Precedence()
         print('  (Step_2) Create_policy_profile, rules, and_admin_port_rule.')
         self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled_and_TCI_Overwrite_Enabled(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.vlan_a)
         self.localPolicyUdks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname,self.tb.config.profile_a)
         self.localPolicyUdks.policy_set_rule_ipproto(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_none6,forward=True,cos=self.tb.config.cos_5)
         self.localPolicyUdks.policy_verify_rule_ipproto_exists(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_none6,cos=self.tb.config.cos_5)
         time.sleep(int(self.tb.config.policy_delay))
         print('  (Verification_1) Verify_100_frames_were_sent_and_received, with_a_priority_value_of_5.')
         self.localPolicyUdks.Transmit_100_Untagged_IPv6_SNAP_Frames_and_Verify_Priority_Changed(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,self.tb.config.dst_mac_a,self.tb.config.vlan_a,self.tb.config.priority_5,self.tb.config.src_ip6_a,self.tb.config.dst_ip6_a,traffic_class=self.tb.config.tos_a)
         print('  (Step_3) Create_policy_profile, rules, and_admin_port_rule.')
         self.localPolicyUdks.policy_set_rule_iptos(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.tos_a,drop=True)
         self.localPolicyUdks.policy_verify_rule_iptos_exist(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.tos_a)
         time.sleep(int(self.tb.config.policy_delay))
         print('  (Verification_2) Verify_100_frames_were_sent_and_NOT_received.')
         self.localPolicyUdks.Transmit_100_Untagged_IPv6_SNAP_Frames_and_Verify_NOT_Received(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,self.tb.config.dst_mac_a,self.tb.config.vlan_a,self.tb.config.src_ip6_a,self.tb.config.dst_ip6_a,traffic_class=self.tb.config.tos_a)
         print('  (Step_4) Create_policy_profile, rules, and_admin_port_rule.')
         self.localPolicyUdks.policy_set_rule_iptos(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.tos_a,forward=True,cos=self.tb.config.cos_4)
         self.localPolicyUdks.policy_verify_rule_iptos_exist(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.tos_a,cos=self.tb.config.cos_4)
         time.sleep(int(self.tb.config.policy_delay))
         print('  (Verification_2) Verify_100_frames_were_sent_and_NOT_received.')
         self.localPolicyUdks.Transmit_100_Untagged_IPv6_SNAP_Frames_and_Verify_Priority_Changed(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,self.tb.config.dst_mac_a,self.tb.config.vlan_a,self.tb.config.priority_4,self.tb.config.src_ip6_a,self.tb.config.dst_ip6_a,traffic_class=self.tb.config.tos_a)
         #self.Test_Case_Cleanup()
     def Test_Case_Cleanup(self):
         self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_all_rules(self.tb.config.netelem1.name)
         self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,self.tb.config.profile_a)
         self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(self.tb.config.netelem1.name,self.tb.config.dst_mac_a,self.tb.config.vlan_a,self.tb.config.netelem1.tgen.port_b.ifname)
         self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,self.tb.config.vlan_a)
         self.localPolicyUdks.Clear_all_Dot1p_QOS_Profiles(self.tb.config.netelem1.name)
         self.localPolicyUdks.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname,self.tb.config.qos_none)
         #self.localPolicyUdks.cosUdks.Remove_QOS_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,self.tb.config.qos_profile_all)
         self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname)
         self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_b.ifname)
         self.localPolicyUdks.networkElementCosGenKeywords.cos_set_port_qos_profile(self.tb.config.netelem1.name,  self.tb.dut1_tgen_port_a.ifname, 'none')
         self.localPolicyUdks.networkElementCosGenKeywords.cos_delete_qos_profile(self.tb.config.netelem1.name, self.tb.config.qos_profile_all)
