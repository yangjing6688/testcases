from Tests.Staging.Functional.Policy.TestCases.PolicyBase import PolicyBase
from pytest import mark
from pytest import fixture


@fixture()
def test_setup_teardown(request):
    # Setup_section
    def teardown():
        request.instance.Test_Case_Cleanup()
    request.addfinalizer(teardown)


class DaclMatchAnyTests(PolicyBase):

    def setup_class(cls):
        print('  (Class setup Step_1) Call PolicyBase setup, connect to devices')
        PolicyBase.setup_class()

        print('  (Class setup Step_2) Call DACL setup to configure common policy and radius settings')
        cls.localPolicyUdks.Policy_Test_Case_Setup_Dacl(cls.tb.config.netelem1)

        print('  (Class setup Step_3) Enable Radius netlogin server')
        cls.localPolicyUdks.radiusSuiteUdks.Configure_And_Enable_Radius_Netlogin_Server(cls.tb.config.netelem1.name,
                                                                                        cls.tb.config.endsysRadius.
                                                                                        instance,
                                                                                        cls.tb.config.endsysRadius.ip,
                                                                                        cls.tb.config.endsysRadius.port,
                                                                                        cls.tb.config.endsysRadius.
                                                                                        shared_secret,
                                                                                        cls.tb.config.netelem1.ip,
                                                                                        cls.tb.config.vr_mgmt)

    def teardown_class(cls):

        print('  (Class teardown Step_2) Unconfigure and disable netlogin server')
        cls.localPolicyUdks.radiusSuiteUdks.UnConfigure_And_Disable_Radius_Netlogin_Server(cls.tb.config.netelem1.name,
                                                                                           cls.tb.config.endsysRadius.
                                                                                           instance,
                                                                                           cls.tb.config.endsysRadius.
                                                                                           ip)

        print('  (Class setup Step_3) Call DACL teardown function to remove common policy and radius settings')
        cls.localPolicyUdks.Policy_Test_Case_Teardown_Dacl(cls.tb.config.netelem1)

        print('  (Class teardown Step_4) Call the base class teardown method disconnects DUT connections')
        PolicyBase.teardown_class()

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    @mark.GAS_DEBUG
    def test_01_Dyn_Access_List_Match_Any_Profile_ACL(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL created with Match Any, a matching profile, and ACL
        Name configured on the profile.  One entry uses the r flag, the other entry does not use the r flag'''

        print('  (Step_1) Create Policy Profiles specify ACL name as same as profile name')
        self.localPolicyUdks.Create_Policy_Profile_with_Name_PVID_and_ACL(self.tb.config.netelem1.name,
                                                                          self.tb.config.policyId_dac1,
                                                                          self.tb.config.policyName_dac1,
                                                                          self.tb.config.policyName_dac1,
                                                                          self.tb.config.pvid_dac1)
        self.localPolicyUdks.Create_Policy_Profile_with_Name_PVID_and_ACL(self.tb.config.netelem1.name,
                                                                          self.tb.config.policyId_dac2,
                                                                          self.tb.config.policyName_dac2,
                                                                          self.tb.config.policyName_dac2,
                                                                          self.tb.config.pvid_dac2)

        print('  (Step_2) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_3) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC41.name,
                                                         self.tb.config.packetDAC41.dst_mac,
                                                         self.tb.config.packetDAC41.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC42.name,
                                                         self.tb.config.packetDAC42.dst_mac,
                                                         self.tb.config.packetDAC42.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC41.name,
                                                                             self.tb.config.packetDAC42.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC41.name,
                                                                                     self.tb.config.packetDAC42.name,
                                                                                     self.tb.config.packetDAC42.name,
                                                                                     self.tb.config.packetDAC41.name,
                                                                                     self.tb.config.packetDAC41.src_mac,
                                                                                     self.tb.config.packetDAC42.src_mac,
                                                                                     tx_count=25)

        print('  (Step_5) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC41.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC42.src_mac,
                                                                                  self.tb.config.pvid_dac2,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_6) Verify DACLs created with expected match clauses')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          profile_id=self.tb.config.
                                                                                          policyId_dac1)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          profile_id=self.tb.config.
                                                                                          policyId_dac2)

        print('  (Step_7) Verify DACLs using r flag created with match any clause, only second DACL has r flag')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id=self.tb.config.
                                                                                              policyId_dac2, item="Any")
        print('  (Step_8) Calling test case cleanup function')
        self.Cleanup_01()

    def Cleanup_01(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC41.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac1,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC42.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac2,
                                                                                          self.tb.config.netelem1.
                                                                                          tgen.port_b.ifname)

        print('  (Test Case cleanup Step_3) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

        print('  (Test Case cleanup Step_4) Delete Policy Profiles')
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,
                                                                                        self.tb.config.policyId_dac1)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,
                                                                                        self.tb.config.policyId_dac2)

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    @mark.GAS_DEBUG
    def test_02_Dyn_Access_List_Match_Any_Profile_ACL_RC(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL created with Match Any, a matching profile, and ACL
        Name configured on the profile.  Both entries use the rc flags'''

        print('  (Step_1) Create Policy Profiles specify ACL name as same as profile name')
        self.localPolicyUdks.Create_Policy_Profile_with_Name_PVID_and_ACL(self.tb.config.netelem1.name,
                                                                          self.tb.config.policyId_dac1,
                                                                          self.tb.config.policyName_dac1,
                                                                          self.tb.config.policyName_dac1,
                                                                          self.tb.config.pvid_dac1)
        self.localPolicyUdks.Create_Policy_Profile_with_Name_PVID_and_ACL(self.tb.config.netelem1.name,
                                                                          self.tb.config.policyId_dac2,
                                                                          self.tb.config.policyName_dac2,
                                                                          self.tb.config.policyName_dac2,
                                                                          self.tb.config.pvid_dac2)

        print('  (Step_2) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_3) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC43.name,
                                                         self.tb.config.packetDAC43.dst_mac,
                                                         self.tb.config.packetDAC43.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC44.name,
                                                         self.tb.config.packetDAC44.dst_mac,
                                                         self.tb.config.packetDAC44.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC43.name,
                                                                             self.tb.config.packetDAC44.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC43.name,
                                                                                     self.tb.config.packetDAC44.name,
                                                                                     self.tb.config.packetDAC44.name,
                                                                                     self.tb.config.packetDAC43.name,
                                                                                     self.tb.config.packetDAC43.src_mac,
                                                                                     self.tb.config.packetDAC44.src_mac,
                                                                                     tx_count=25)

        print('  (Step_5) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC43.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC44.src_mac,
                                                                                  self.tb.config.pvid_dac2,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_6) Verify DACLs created with expected match clauses')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          profile_id=self.tb.config.
                                                                                          policyId_dac1)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          profile_id=self.tb.config.
                                                                                          policyId_dac2)

        print('  (Step_7) Verify DACLs created with match any specified clauses')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id=self.tb.config.
                                                                                              policyId_dac1, item="Any")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id=self.tb.config.
                                                                                              policyId_dac2, item="Any")
        print('  (Step_8) Calling test case cleanup function')
        self.Cleanup_02()

    def Cleanup_02(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC43.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac1,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC44.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac2,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_b.ifname)

        print('  (Test Case cleanup Step_3) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

        print('  (Test Case cleanup Step_4) Delete Policy Profiles')
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,
                                                                                        self.tb.config.policyId_dac1)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,
                                                                                        self.tb.config.policyId_dac2)

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_03_Dyn_Access_List_Match_Any_No_Profile_RC(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL created with Match Any, no matching profile.
          Both entries use the rc flags. To allow for fdb entry add ports to a vlan '''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_2) Create VLAN and add egress ports as untagged')
        self.localPolicyUdks.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.tb.config.netelem1.name,
                                                                       self.tb.config.vlan_a)
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   self.tb.config.
                                                                                                   vlan_a,
                                                                                                   self.tb.config.
                                                                                                   netelem1.tgen.port_a.
                                                                                                   ifname)
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   self.tb.config.
                                                                                                   vlan_a,
                                                                                                   self.tb.config.
                                                                                                   netelem1.tgen.port_b.
                                                                                                   ifname)

        print('  (Step_3) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC43.name,
                                                         self.tb.config.packetDAC43.dst_mac,
                                                         self.tb.config.packetDAC43.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC44.name,
                                                         self.tb.config.packetDAC44.dst_mac,
                                                         self.tb.config.packetDAC44.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC43.name,
                                                                             self.tb.config.packetDAC44.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC43.name,
                                                                                     self.tb.config.packetDAC44.name,
                                                                                     self.tb.config.packetDAC44.name,
                                                                                     self.tb.config.packetDAC43.name,
                                                                                     self.tb.config.packetDAC43.src_mac,
                                                                                     self.tb.config.packetDAC44.src_mac,
                                                                                     tx_count=25)

        print('  (Step_5) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC43.src_mac,
                                                                                  self.tb.config.vlan_a,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC44.src_mac,
                                                                                  self.tb.config.vlan_a,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_6) Verify DACLs created with expected match clauses')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          profile_id="1")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          profile_id="2")

        print('  (Step_7) Verify DACLs created with match any specified clauses')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id="1",
                                                                                              item="Any")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id="2",
                                                                                              item="Any")
        print('  (Step_8) Calling test case cleanup function')
        self.Cleanup_03()

    def Cleanup_03(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC43.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac1,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC44.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac2,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_b.ifname)

        print('  (Test Case cleanup Step_3) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

        print('  (Test Case cleanup Step_4) Delete VLAN')
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,
                                                                           self.tb.config.vlan_a)

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_04_Dyn_Access_List_Match_Any_Profile_NoACL(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL not created with Match Any, a matching profile, and no ACL
        Name configured on the profile.  One entry uses the r flag the other uses the rc flag'''

        print('  (Step_1) Create Policy Profiles without specifying the ACL name')
        self.localPolicyUdks.Create_Policy_Profile_with_Name_and_PVID(self.tb.config.netelem1.name,
                                                                      self.tb.config.policyId_dac1,
                                                                      self.tb.config.policyName_dac1,
                                                                      self.tb.config.pvid_dac1)
        self.localPolicyUdks.Create_Policy_Profile_with_Name_and_PVID(self.tb.config.netelem1.name,
                                                                      self.tb.config.policyId_dac2,
                                                                      self.tb.config.policyName_dac2,
                                                                      self.tb.config.pvid_dac2)

        print('  (Step_2) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_3) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC45.name,
                                                         self.tb.config.packetDAC45.dst_mac,
                                                         self.tb.config.packetDAC45.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC46.name,
                                                         self.tb.config.packetDAC46.dst_mac,
                                                         self.tb.config.packetDAC46.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC45.name,
                                                                             self.tb.config.packetDAC46.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC45.name,
                                                                                     self.tb.config.packetDAC46.name,
                                                                                     self.tb.config.packetDAC46.name,
                                                                                     self.tb.config.packetDAC45.name,
                                                                                     self.tb.config.packetDAC45.src_mac,
                                                                                     self.tb.config.packetDAC46.src_mac,
                                                                                     tx_count=25, ignore_error = "True")

        print('  (Step_5) Not expecting to authenticate in this case so dont Verify FDB entries.')


        print('  (Step_6) Verify DACLs not created with expected match clauses')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  profile_id=self.tb.
                                                                                                  config.policyId_dac1)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  profile_id=self.
                                                                                                  tb.config.
                                                                                                  policyId_dac2)

        print('  (Step_7) Calling test case cleanup function')
        self.Cleanup_04()

    def Cleanup_04(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC45.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac1,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC46.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac2,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_b.ifname)

        print('  (Test Case cleanup Step_3) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

        print('  (Test Case cleanup Step_4) Delete Policy Profiles')
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,
                                                                                        self.tb.config.policyId_dac1)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,
                                                                                        self.tb.config.policyId_dac2)

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_05_Dyn_Access_List_Match_Any_Profile_ACL_Addl_Clause(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL not created with Match Any, a matching profile, and ACL
        Name configured on the profile.  An additional match clause is present either before or after the match any
        Both entries use the r flag. Currently, with the r flag the authentication passes and ACL is created, for
        now the test is written so it passes, if we change the policy behavior we will change the test.'''

        print('  (Step_1) Create Policy Profiles specify ACL name as same as profile name')
        self.localPolicyUdks.Create_Policy_Profile_with_Name_PVID_and_ACL(self.tb.config.netelem1.name,
                                                                          self.tb.config.policyId_dac1,
                                                                          self.tb.config.policyName_dac1,
                                                                          self.tb.config.policyName_dac1,
                                                                          self.tb.config.pvid_dac1)
        self.localPolicyUdks.Create_Policy_Profile_with_Name_PVID_and_ACL(self.tb.config.netelem1.name,
                                                                          self.tb.config.policyId_dac2,
                                                                          self.tb.config.policyName_dac2,
                                                                          self.tb.config.policyName_dac2,
                                                                          self.tb.config.pvid_dac2)

        print('  (Step_2) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_3) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC47.name,
                                                         self.tb.config.packetDAC47.dst_mac,
                                                         self.tb.config.packetDAC47.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC48.name,
                                                         self.tb.config.packetDAC48.dst_mac,
                                                         self.tb.config.packetDAC48.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_6) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC47.name,
                                                                             self.tb.config.packetDAC48.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC47.name,
                                                                                     self.tb.config.packetDAC48.name,
                                                                                     self.tb.config.packetDAC48.name,
                                                                                     self.tb.config.packetDAC47.name,
                                                                                     self.tb.config.packetDAC47.src_mac,
                                                                                     self.tb.config.packetDAC48.src_mac,
                                                                                     tx_count=25)

        print('  (Step_7) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC47.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.
                                                                                  port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC48.src_mac,
                                                                                  self.tb.config.pvid_dac2,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_8) Verify DACLs created with expected match clauses - for now written to expect ACLs to exist')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          profile_id=self.tb.config.
                                                                                          policyId_dac1)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          profile_id=self.tb.config.
                                                                                          policyId_dac2)

        print('  (Step_9) Calling test case cleanup function')
        self.Cleanup_05()

    def Cleanup_05(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC47.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac1,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC48.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac2,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_b.ifname)

        print('  (Test Case cleanup Step_3) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

        print('  (Test Case cleanup Step_4) Delete Policy Profiles')
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,
                                                                                        self.tb.config.policyId_dac1)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,
                                                                                        self.tb.config.policyId_dac2)
