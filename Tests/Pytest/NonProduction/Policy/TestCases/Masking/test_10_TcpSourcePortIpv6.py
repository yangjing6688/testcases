from Tests.Pytest.NonProduction.Policy.Resources.PolicyBase import PolicyBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.NonProduction.Policy.Resources.Policy_Test_Suite_Udks import Policy_Test_Suite_Udks
import time

@fixture()
def test_setup_teardown(request):
    # Setup_section
    def teardown():
        request.instance.Test_Case_Cleanup()
    request.addfinalizer(teardown)

class TcpSourcePortIpv6Tests(PolicyBase):
    @mark.F_129413
    @mark.EXOS
    @mark.P2
    @mark.Policy_Masking
    @mark.NIGHTLY
    def test_10_Masking_Precedence_IPv6_TCPSourcePortIP(self):
        '''[Documentation]  Test_Objective: Verify_tcpsourceportip_policy_rules_drop_or_forward_traffic_correctly_when_using
                      masks.'''        
    
        self.localPolicyUdks.change_policy_rule_model(   self.tb.config.netelem1.name, 'Hierarchical')
        print('  (Step_1) Configure_ports, QoS, and_FDB_for_Policy_traffic_tests.')
        self.localPolicyUdks.Policy_Test_Case_Setup_B()
    
        print('  (Step_2) Create_policy_profile, rules, and_admin_port_rule.')
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_TCI_Overwrite_Enabled_and_Verify(self.tb.config.netelem1.name,  self.tb.config.profile_a)
        self.localPolicyUdks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(self.tb.config.netelem1.name,
                                                                          self.tb.config.netelem1.tgen.port_a.ifname,  self.tb.config.profile_a)
        self.localPolicyUdks.policy_set_rule_tcpsourceportip(self.tb.config.netelem1.name,  self.tb.config.profile_a,    self.tb.config.mask_l4ip_b,  mask='8',
                                                        drop=True)
        self.localPolicyUdks.policy_verify_rule_tcpdestportip_exists(   self.tb.config.netelem1.name,  self.tb.config.profile_a,    self.tb.config.mask_l4ip_a,  mask='8')
    
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    
        print('  (Verification_1) Verify_100_unlearned_frames_were_sent_and_NOT_received.')
        self.localPolicyUdks.Transmit_100_Untagged_IPv6_TCP_Frames_and_Verify_NOT_Received(
                  self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_a,
                  self.tb.config.src_ip6_a,     self.tb.config.dst_ip6_a,  src_port=self.tb.config.l4_port_a,          dst_port=self.tb.config.l4_port_c)
    
        print('  (Verification_2) Verify_100_unlearned_frames_were_sent_and_NOT_received.')
        self.localPolicyUdks.Transmit_100_Tagged_IPv6_TCP_Frames_and_Verify_NOT_Received(
                  self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_a,
                  self.tb.config.src_ip6_a,     self.tb.config.dst_ip6_a,  src_port=self.tb.config.l4_port_a,          dst_port=self.tb.config.l4_port_c)
    
        print('  (Step_3) Create_additional_Policy_Rules.')
        self.localPolicyUdks.policy_set_rule_tcpsourceportip(self.tb.config.netelem1.name,  self.tb.config.profile_a,  self.tb.config.mask_l4ip_b,  mask='16',
                                                       forward=True)
        self.localPolicyUdks.policy_verify_rule_tcpdestportip_exists(  self.tb.config.netelem1.name,  self.tb.config.profile_a,  self.tb.config.mask_l4ip_b,  mask='16')
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    
        print('  (Verification_3) Verify_100_unlearned_frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_IPv6_TCP_Frames_and_Verify_Received(
                  self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_a,
                  self.tb.config.src_ip6_a,     self.tb.config.dst_ip6_a,  src_port=self.tb.config.l4_port_a,          dst_port=self.tb.config.l4_port_c)
    
        print('  (Verification_4) Verify_100_unlearned_frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Tagged_IPv6_TCP_Frames_and_Verify_Received(
                  self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_a,
                  self.tb.config.src_ip6_a,     self.tb.config.dst_ip6_a,  src_port=self.tb.config.l4_port_a,          dst_port=self.tb.config.l4_port_c)
    
        #self.Test_Case_Cleanup()
    
    
    
    def Test_Case_Cleanup(self):
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_all_rules(self.tb.config.netelem1.name)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(  self.tb.config.netelem1.name,  self.tb.config.profile_a)
        self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(
                                    self.tb.config.netelem1.name,  self.tb.config.dst_mac_a,      self.tb.config.vlan_a, self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(             self.tb.config.netelem1.name,  self.tb.config.vlan_a)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(       self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(       self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_b.ifname)
