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
class ClearRuleUntaggedTests(PolicyBase):
     @mark.F_1000043123
     @mark.EXOS
     @mark.P3
     @mark.Policy_Rules
     @mark.Policy_IpProto_Rules
     def test_11_IpProto_Policy_Clear_Drop_Rule_Untagged_Packet(self):
         '''[Documentation]  Test_Objective: Verify_traffic_passes_again_after_removing_an_ipttl_policy_drop_rule.'''
         print('  (Step_1) Configure_ports, QoS, and_FDB_for_Policy_traffic_tests.')
         self.localPolicyUdks.Policy_Test_Case_Setup_B()
         print('  (Step_2) Create_policy_profile, rules, and_admin_port_rule.')
         self.localPolicyUdks.Create_Policy_Profile_and_Verify_it_Exists(self.tb.config.netelem1.name,self.tb.config.profile_a)
         self.localPolicyUdks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname,self.tb.config.profile_a)
         self.localPolicyUdks.policy_set_rule_ipproto(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp,drop=True)
         self.localPolicyUdks.policy_verify_rule_ipproto_exists(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp,drop=True)
         time.sleep(int(self.tb.config.policy_delay))
         print('  (Verification_1) Verify_100_unlearned_frames_were_sent_and_NOT_received.')
         self.localPolicyUdks.Transmit_100_Untagged_IP_TTL_Frames_and_Verify_NOT_Received(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,self.tb.config.dst_mac_a,self.tb.config.vlan_a,self.tb.config.src_ip_a,self.tb.config.dst_ip_a,self.tb.config.proto_tcp)
         print('  (Step_3) Clear_policy_drop_rule.')
         self.localPolicyUdks.Remove_Policy_Rule_IpProto(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp)
         self.localPolicyUdks.policy_verify_rule_ipproto_exists(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp,drop=True)
         time.sleep(int(self.tb.config.policy_delay))
         print('  (Verification_2) Verify_100_unlearned_frames_were_sent_and_received.')
         self.localPolicyUdks.Transmit_100_Untagged_IP_TTL_Frames_and_Verify_Received(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,self.tb.config.dst_mac_a,self.tb.config.vlan_a,self.tb.config.src_ip_a,self.tb.config.dst_ip_a,self.tb.config.proto_tcp)
         print('  (Step_4) Bounce_traffic_ports_to_clear_FDB_entries, re-create_policy_drop_rule, and_prime_FDB_with_traffic.')
         self.localPolicyUdks.policyUdks.Bounce_Netelem_Port(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname)
         self.localPolicyUdks.policyUdks.Bounce_Netelem_Port(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_b.ifname)
         self.localPolicyUdks.policy_set_rule_ipproto(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp,drop=True)
         self.localPolicyUdks.policy_verify_rule_ipproto_exists(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp,drop=True)
         time.sleep(int(self.tb.config.policy_delay))
         self.localPolicyUdks.Transmit_10_Frames_and_Verify_FDB_Entry_is_Learned(self.tb.config.netelem1.name,self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.packet_name_a,self.tb.config.src_mac_a,self.tb.config.dst_mac_a,self.tb.config.vlan_a,self.tb.config.netelem1.tgen.port_a.ifname)
         print('  (Verification_3) Verify_100_learned_frames_were_sent_and_NOT_received.')
         self.localPolicyUdks.Transmit_100_Untagged_IP_TTL_Frames_and_Verify_NOT_Received(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,self.tb.config.dst_mac_a,self.tb.config.vlan_a,self.tb.config.src_ip_a,self.tb.config.dst_ip_a,self.tb.config.proto_tcp)
         print('  (Step_5) Clear_policy_drop_rule.')
         self.localPolicyUdks.Remove_Policy_Rule_IpProto(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp)
         self.localPolicyUdks.policy_verify_rule_ipproto_exists(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp,drop=True)
         time.sleep(int(self.tb.config.policy_delay))
         print('  (Verification_4) Verify_100_learned_frames_were_sent_and_received.')
         self.localPolicyUdks.Transmit_100_Untagged_IP_TTL_Frames_and_Verify_Received(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,self.tb.config.dst_mac_a,self.tb.config.vlan_a,self.tb.config.src_ip_a,self.tb.config.dst_ip_a,self.tb.config.proto_tcp)
         print('  (Step_6) Re-create_policy_drop_rule.')
         self.localPolicyUdks.policy_set_rule_ipproto(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp,drop=True)
         self.localPolicyUdks.policy_verify_rule_ipproto_exists(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp,drop=True)
         time.sleep(int(self.tb.config.policy_delay))
         print('  (Verification_5) Verify_100_broadcast_frames_were_sent_and_NOT_received.')
         self.localPolicyUdks.Transmit_100_Untagged_IP_TTL_Frames_and_Verify_NOT_Received(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,self.tb.config.bcast_mac,self.tb.config.vlan_a,self.tb.config.src_ip_a,self.tb.config.dst_ip_a,self.tb.config.proto_tcp)
         print('  (Step_7) Clear_policy_drop_rule.')
         self.localPolicyUdks.Remove_Policy_Rule_IpProto(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp)
         self.localPolicyUdks.policy_verify_rule_ipproto_exists(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp,drop=True)
         time.sleep(int(self.tb.config.policy_delay))
         print('  (Verification_6) Verify_100_broadcast_frames_were_sent_and_received.')
         self.localPolicyUdks.Transmit_100_Untagged_IP_TTL_Frames_and_Verify_Received(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,self.tb.config.bcast_mac,self.tb.config.vlan_a,self.tb.config.src_ip_a,self.tb.config.dst_ip_a,self.tb.config.proto_tcp)
         print('  (Step_80) Re-create_policy_drop_rule.')
         self.localPolicyUdks.policy_set_rule_ipproto(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp,drop=True)
         self.localPolicyUdks.policy_verify_rule_ipproto_exists(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp,drop=True)
         time.sleep(int(self.tb.config.policy_delay))
         print('  (Verification_7) Verify_100_multicast_frames_were_sent_and_NOT_received.')
         self.localPolicyUdks.Transmit_100_Untagged_IP_TTL_Frames_and_Verify_NOT_Received(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,self.tb.config.mcast_mac,self.tb.config.vlan_a,self.tb.config.src_ip_a,self.tb.config.dst_ip_a,self.tb.config.proto_tcp)
         print('  (Step_91) Clear_policy_drop_rule.')
         self.localPolicyUdks.Remove_Policy_Rule_IpProto(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp)
         self.localPolicyUdks.policy_verify_rule_ipproto_exists(self.tb.config.netelem1.name,self.tb.config.profile_a,self.tb.config.proto_tcp,drop=True)
         time.sleep(int(self.tb.config.policy_delay))
         print('  (Verification_8) Verify_100_multicast_frames_were_sent_and_received.')
         self.localPolicyUdks.Transmit_100_Untagged_IP_TTL_Frames_and_Verify_Received(self.tb.config.tgen_ports.netelem1.port_a,self.tb.config.tgen_ports.netelem1.port_b,self.tb.config.src_mac_a,self.tb.config.mcast_mac,self.tb.config.vlan_a,self.tb.config.src_ip_a,self.tb.config.dst_ip_a,self.tb.config.proto_tcp)
         #self.Test_Case_Cleanup()
     def Test_Case_Cleanup(self):
         self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_all_rules(self.tb.config.netelem1.name)
         self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,self.tb.config.profile_a)
         self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(self.tb.config.netelem1.name,self.tb.config.dst_mac_a,self.tb.config.vlan_a,self.tb.config.netelem1.tgen.port_b.ifname)
         self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,self.tb.config.vlan_a)
         self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname)
         self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_b.ifname)
         self.localPolicyUdks.networkElementCosGenKeywords.cos_set_port_qos_profile(self.tb.config.netelem1.name,  self.tb.dut1_tgen_port_a.ifname, 'none')
         self.localPolicyUdks.networkElementCosGenKeywords.cos_delete_qos_profile(self.tb.config.netelem1.name, self.tb.config.qos_profile_all)
