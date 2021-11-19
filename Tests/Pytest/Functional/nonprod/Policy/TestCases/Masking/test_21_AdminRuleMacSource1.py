from Tests.Pytest.Functional.nonprod.Policy.Resources.PolicyBase import PolicyBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.Functional.nonprod.Policy.Resources.Policy_Test_Suite_Udks import Policy_Test_Suite_Udks
import time

@fixture()
def test_setup_teardown(request):
    # Setup_section
    def teardown():
        request.instance.Test_Case_Cleanup()
    request.addfinalizer(teardown)
    
class AdminRuleMacSourceTests(PolicyBase):    
    @mark.F_1000043232
    @mark.EXOS
    @mark.P3
    @mark.Policy_Masking
    @mark.NIGHTLY
    def test_21_Masking_Precedence_Admin_Rule_MacSource(self):
        '''[Documentation]  Test_Objective: Verify_macsource_policy_rules_drop_or_forward_traffic_correctly_when_using_masks.'''
        
        self.localPolicyUdks.change_policy_rule_model(   self.tb.config.netelem1.name, 'Hierarchical')
        print('  (Step_1) Configure_ports, QoS, and_FDB_for_Policy_traffic_tests.')
        self.localPolicyUdks.Policy_Test_Case_Setup_Admin_Rules()
    
        print('  (Step_2) Create_policy_profile, rules, and_admin_port_rule.')
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled(self.tb.config.netelem1.name,  self.tb.config.profile_a,  self.tb.config.vlan_a)
        self.localPolicyUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled(self.tb.config.netelem1.name,  self.tb.config.profile_b,  self.tb.config.vlan_b)
        self.localPolicyUdks.policyUdks.Create_Mac_Source_Admin_Profile_and_Verify_it_was_Created(self.tb.config.netelem1.name,  self.tb.config.src_mac_a,   self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_a,      mask='8')
        '''self.localPolicyUdks.networkElementPolicyGenKeywords.policy_mac_source_admin_profile_should_exist(  self.tb.config.netelem1.name,  self.tb.config.mask_mac_a,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_a,      mask=8)'''
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    
        print('  (Verification_1) Verify_100_unlearned_frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_a)
    
        print('  (Step_3) Create_additional_Policy_Rules.')
        self.localPolicyUdks.policyUdks.Create_Mac_Source_Admin_Profile_and_Verify_it_was_Created(self.tb.config.netelem1.name,  self.tb.config.src_mac_a,   self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_b,      mask='16')
        '''self.localPolicyUdks.networkElementPolicyGenKeywords.policy_mac_source_admin_profile_should_exist(  self.tb.config.netelem1.name,  self.tb.config.mask_mac_b,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_b,      mask=16)'''
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    
        print('  (Verification_2) Verify_100_unlearned_frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_b)
    
        print('  (Step_4) Create_additional_Policy_Rules.')
        self.localPolicyUdks.policyUdks.Create_Mac_Source_Admin_Profile_and_Verify_it_was_Created(self.tb.config.netelem1.name,  self.tb.config.src_mac_a,   self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_a,      mask='20')
        '''self.localPolicyUdks.networkElementPolicyGenKeywords.policy_mac_source_admin_profile_should_exist(  self.tb.config.netelem1.name,  self.tb.config.mask_mac_c,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_a,      mask=20)'''
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    
        print('  (Verification_3) Verify_100_unlearned_frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_a)
    
        print('  (Step_5) Create_additional_Policy_Rules.')
        self.localPolicyUdks.policyUdks.Create_Mac_Source_Admin_Profile_and_Verify_it_was_Created(self.tb.config.netelem1.name,  self.tb.config.src_mac_a,   self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_b,      mask='24')
        '''self.localPolicyUdks.networkElementPolicyGenKeywords.policy_mac_source_admin_profile_should_exist(  self.tb.config.netelem1.name,  self.tb.config.mask_mac_d,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_b,      mask=24)'''
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    
        print('  (Verification_4) Verify_100_unlearned_frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_b)
    
        print('  (Step_6) Create_additional_Policy_Rules.')
        self.localPolicyUdks.policyUdks.Create_Mac_Source_Admin_Profile_and_Verify_it_was_Created(self.tb.config.netelem1.name,  self.tb.config.src_mac_a,   self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_a,      mask='28')
        '''self.localPolicyUdks.networkElementPolicyGenKeywords.policy_mac_source_admin_profile_should_exist(  self.tb.config.netelem1.name,  self.tb.config.mask_mac_e,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_a,      mask=28)'''
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    
        print('  (Verification_5) Verify_100_unlearned_frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_a)
    
        print('  (Step_7) Create_additional_Policy_Rules.')
        self.localPolicyUdks.policyUdks.Create_Mac_Source_Admin_Profile_and_Verify_it_was_Created(self.tb.config.netelem1.name,  self.tb.config.src_mac_a,   self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_b,      mask='32')
        '''self.localPolicyUdks.networkElementPolicyGenKeywords.policy_mac_source_admin_profile_should_exist(  self.tb.config.netelem1.name,  self.tb.config.mask_mac_f,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_b,      mask=32)'''
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    
        print('  (Verification_6) Verify_100_unlearned_frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_b)
    
        print('  (Step_8) Create_additional_Policy_Rules.')
        self.localPolicyUdks.policyUdks.Create_Mac_Source_Admin_Profile_and_Verify_it_was_Created(self.tb.config.netelem1.name,  self.tb.config.src_mac_a,   self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_a,      mask='36')
        '''self.localPolicyUdks.networkElementPolicyGenKeywords.policy_mac_source_admin_profile_should_exist(  self.tb.config.netelem1.name,  self.tb.config.mask_mac_g,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_a,      mask=36)'''
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    
        print('  (Verification_7) Verify_100_unlearned_frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_a)
    
        print('  (Step_9) Create_additional_Policy_Rules.')
        self.localPolicyUdks.policyUdks.Create_Mac_Source_Admin_Profile_and_Verify_it_was_Created(self.tb.config.netelem1.name,  self.tb.config.src_mac_a,   self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_b,      mask='40')
        '''self.localPolicyUdks.networkElementPolicyGenKeywords.policy_mac_source_admin_profile_should_exist(self.tb.config.netelem1.name,  self.tb.config.mask_mac_h,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_b,      mask=40)'''
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    
        print('  (Verification_8) Verify_100_unlearned_frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_b)
    
        print('  (Step_10) Create_additional_Policy_Rules.')
        self.localPolicyUdks.policyUdks.Create_Mac_Source_Admin_Profile_and_Verify_it_was_Created(self.tb.config.netelem1.name,  self.tb.config.src_mac_a,   self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_a,      mask='44')
        '''self.localPolicyUdks.networkElementPolicyGenKeywords.policy_mac_source_admin_profile_should_exist(  self.tb.config.netelem1.name,  self.tb.config.mask_mac_i,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_a,      mask=44)'''
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    
        print('  (Verification_9) Verify_100_unlearned_frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_a)
    
        print('  (Step_11) Create_additional_Policy_Rules.')
        self.localPolicyUdks.policyUdks.Create_Mac_Source_Admin_Profile_and_Verify_it_was_Created(self.tb.config.netelem1.name,  self.tb.config.src_mac_a,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_b,      mask='48')
        '''self.localPolicyUdks.networkElementPolicyGenKeywords.policy_mac_source_admin_profile_should_exist(  self.tb.config.netelem1.name,  self.tb.config.src_mac_a,  self.tb.config.netelem1.tgen.port_a.ifname,
                                                       self.tb.config.profile_b,      mask=48)'''
        time.sleep(int(self.tb.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    
        print('  (Verification_10) Verify_100_unlearned_frames_were_sent_and_received.')
        self.localPolicyUdks.Transmit_100_Untagged_Frames_and_Verify_Received(
              self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,  self.tb.config.src_mac_a,  self.tb.config.dst_mac_a,  self.tb.config.vlan_b)
    
        #self.Test_Case_Cleanup()
    
    def Test_Case_Cleanup(self):
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_all_rules(self.tb.config.netelem1.name)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_a)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.profile_b)
        self.localPolicyUdks.Clear_all_Dot1p_QOS_Profiles(self.tb.config.netelem1.name)
        self.localPolicyUdks.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,  self.tb.config.qos_none)
        self.localPolicyUdks.cosUdks.Remove_QOS_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,  self.tb.config.qos_profile_all)
        self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(
                                    self.tb.config.netelem1.name,  self.tb.config.dst_mac_a, self.tb.config.vlan_a, self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(
                                    self.tb.config.netelem1.name,  self.tb.config.dst_mac_a, self.tb.config.vlan_b, self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,  self.tb.config.vlan_a)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,  self.tb.config.vlan_b)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_b.ifname)
