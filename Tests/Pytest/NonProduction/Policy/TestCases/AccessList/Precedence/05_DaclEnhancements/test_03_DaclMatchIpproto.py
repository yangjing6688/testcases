from Tests.Staging.Functional.Policy.TestCases.PolicyBase import PolicyBase
from pytest import mark
from pytest import fixture


@fixture()
def test_setup_teardown(request):
    # Setup_section
    def teardown():
        request.instance.Test_Case_Cleanup()
    request.addfinalizer(teardown)


class DaclMatchIpprotoTypeTests(PolicyBase):

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

        print('  (Class setup Step_4) Create Policy Profiles specify ACL name as same as profile name')
        cls.localPolicyUdks.Create_Policy_Profile_with_Name_PVID_and_ACL(cls.tb.config.netelem1.name,
                                                                         cls.tb.config.policyId_dac1,
                                                                         cls.tb.config.policyName_dac1,
                                                                         cls.tb.config.policyName_dac1,
                                                                         cls.tb.config.pvid_dac1)
        cls.localPolicyUdks.Create_Policy_Profile_with_Name_PVID_and_ACL(cls.tb.config.netelem1.name,
                                                                         cls.tb.config.policyId_dac2,
                                                                         cls.tb.config.policyName_dac2,
                                                                         cls.tb.config.policyName_dac2,
                                                                         cls.tb.config.pvid_dac2)

    def teardown_class(cls):
        print('  (Class teardown Step_1) Delete Policy Profiles')
        cls.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(cls.tb.config.netelem1.name,
                                                                                       cls.tb.config.policyId_dac1)
        cls.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(cls.tb.config.netelem1.name,
                                                                                       cls.tb.config.policyId_dac2)

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
    def test_01_Dyn_Access_List_Ipproto_Decimal(self):
        '''[Documentation]  Test_Objective: Verify_Dynamic_Access-List_Created_With_Matching_On_Decimal_Ipproto_Type'''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_2) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC21.name,
                                                         self.tb.config.packetDAC21.dst_mac,
                                                         self.tb.config.packetDAC21.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC22.name,
                                                         self.tb.config.packetDAC22.dst_mac,
                                                         self.tb.config.packetDAC22.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_3) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC21.name,
                                                                             self.tb.config.packetDAC22.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC21.name,
                                                                                     self.tb.config.packetDAC22.name,
                                                                                     self.tb.config.packetDAC22.name,
                                                                                     self.tb.config.packetDAC21.name,
                                                                                     self.tb.config.packetDAC21.src_mac,
                                                                                     self.tb.config.packetDAC22.src_mac,
                                                                                     tx_count=25)

        print('  (Step_4) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC21.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC22.src_mac,
                                                                                  self.tb.config.pvid_dac2,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_5) Verify DACLs created with expected match clauses')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          profile_id=self.tb.config.
                                                                                          policyId_dac1)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          profile_id=self.tb.config.
                                                                                          policyId_dac2)
        print('  (Step_6) Verify DACLs created with expected ipproto type')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipproto(self.tb.config.netelem1.
                                                                                            name,
                                                                                            profile_id=self.tb.config.
                                                                                            policyId_dac1,
                                                                                            ipproto=self.tb.config.
                                                                                            ipproto_max,
                                                                                            mask="8")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipproto(self.tb.config.netelem1.
                                                                                            name,
                                                                                            profile_id=self.tb.config.
                                                                                            policyId_dac2,
                                                                                            ipproto=self.tb.config.
                                                                                            ipproto_max,
                                                                                            mask="8")
        print('  (Step_7) Calling test case cleanup function')
        self.Cleanup_01()

    def Cleanup_01(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC21.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac1,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC22.src_mac,
                                                                                          self.tb.config.pvid_dac2,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_b.ifname)

        print('  (Test Case cleanup Step_3) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_02_Dyn_Access_List_Ipproto_Hex(self):
        '''[Documentation]  Test_Objective: Verify_Dynamic_Access-List_Created_With_Matching_On_Hex_Ipproto_Type '''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_2) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC23.name,
                                                         self.tb.config.packetDAC23.dst_mac,
                                                         self.tb.config.packetDAC23.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC24.name,
                                                         self.tb.config.packetDAC24.dst_mac,
                                                         self.tb.config.packetDAC24.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_3) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC23.name,
                                                                             self.tb.config.packetDAC24.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC23.name,
                                                                                     self.tb.config.packetDAC24.name,
                                                                                     self.tb.config.packetDAC24.name,
                                                                                     self.tb.config.packetDAC23.name,
                                                                                     self.tb.config.packetDAC23.src_mac,
                                                                                     self.tb.config.packetDAC24.src_mac,
                                                                                     tx_count=25)

        print('  (Step_4) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC23.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC24.src_mac,
                                                                                  self.tb.config.pvid_dac2,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_5) Verify DACLs created with expected match clauses')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          profile_id=self.tb.config.
                                                                                          policyId_dac1)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          profile_id=self.tb.config.
                                                                                          policyId_dac2)

        print('  (Step_6) Verify DACLs created with expected ipproto type')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipproto(self.tb.config.netelem1.
                                                                                           name,
                                                                                           profile_id=self.tb.config.
                                                                                           policyId_dac1,
                                                                                           ipproto=self.tb.config.
                                                                                           ipproto_max,
                                                                                           mask="8")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipproto(self.tb.config.netelem1.
                                                                                           name,
                                                                                           profile_id=self.tb.config.
                                                                                           policyId_dac2,
                                                                                           ipproto=self.tb.config.
                                                                                           ipproto_max,
                                                                                           mask="8")

        print('  (Step_7) Calling test case cleanup function')
        self.Cleanup_02()

    def Cleanup_02(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC23.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac1,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC24.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac2,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_b.ifname)

        print('  (Test Case cleanup Step_3) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_03_Dyn_Access_List_Ipproto_Type_Zero(self):
        '''[Documentation]  Test_Objective: Verify DACL matching on minimum ipproto type of 0, with and without a mask'''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_2) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC25.name,
                                                         self.tb.config.packetDAC25.dst_mac,
                                                         self.tb.config.packetDAC25.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC26.name,
                                                         self.tb.config.packetDAC26.dst_mac,
                                                         self.tb.config.packetDAC26.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_3) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC25.name,
                                                                             self.tb.config.packetDAC26.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC25.name,
                                                                                     self.tb.config.packetDAC26.name,
                                                                                     self.tb.config.packetDAC26.name,
                                                                                     self.tb.config.packetDAC25.name,
                                                                                     self.tb.config.packetDAC25.src_mac,
                                                                                     self.tb.config.packetDAC26.src_mac,
                                                                                     tx_count=25)

        print('  (Step_4) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC25.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC26.src_mac,
                                                                                  self.tb.config.pvid_dac2,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_5) Verify DACLs created with specified profile pvid')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          self.tb.config.policyId_dac1)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          self.tb.config.policyId_dac2)

        print('  (Step_6) Verify DACLs created with expected ipproto type')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipproto(self.tb.config.netelem1.
                                                                                           name,
                                                                                           profile_id=self.tb.config.
                                                                                           policyId_dac1,
                                                                                           ipproto=self.tb.config.
                                                                                           ipproto_min,
                                                                                           mask="8")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipproto(self.tb.config.netelem1.
                                                                                           name,
                                                                                           profile_id=self.tb.config.
                                                                                           policyId_dac2,
                                                                                           ipproto=self.tb.config.
                                                                                           ipproto_min,
                                                                                           mask="8")

        print('  (Step_7) Calling test case cleanup function')
        self.Cleanup_03()

    def Cleanup_03(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_04_Dyn_Access_List_ipproto_icmp(self):
        '''[Documentation]  Test_Objective: Verify DACL is created if ipproto type set to icmp with and w/out r flag'''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_2) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC27.name,
                                                         self.tb.config.packetDAC27.dst_mac,
                                                         self.tb.config.packetDAC27.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC28.name,
                                                         self.tb.config.packetDAC28.dst_mac,
                                                         self.tb.config.packetDAC28.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_3) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC27.name,
                                                                             self.tb.config.packetDAC28.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC27.name,
                                                                                     self.tb.config.packetDAC28.name,
                                                                                     self.tb.config.packetDAC28.name,
                                                                                     self.tb.config.packetDAC27.name,
                                                                                     self.tb.config.packetDAC27.src_mac,
                                                                                     self.tb.config.packetDAC28.src_mac,
                                                                                     tx_count=25)

        print('  (Step_4) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC27.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC28.src_mac,
                                                                                  self.tb.config.pvid_dac2,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_5) Verify DACLs created with specified profile pvid')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          self.tb.config.policyId_dac1)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          self.tb.config.policyId_dac2)

        print('  (Step_6) Verify DACLs created with expected ipproto type')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipproto(self.tb.config.netelem1.
                                                                                           name,
                                                                                           profile_id=self.tb.config.
                                                                                           policyId_dac1,
                                                                                           ipproto=self.tb.config.
                                                                                           ipproto_icmp,
                                                                                           mask="8")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipproto(self.tb.config.netelem1.
                                                                                           name,
                                                                                           profile_id=self.tb.config.
                                                                                           policyId_dac2,
                                                                                           ipproto=self.tb.config.
                                                                                           ipproto_icmp,
                                                                                           mask="8")

        print('  (Step_7) Calling test case cleanup function')
        self.Cleanup_04()

    def Cleanup_04(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name,'configure netlogin del mac-list default',ignore_cli_feedback=True)

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_05_Dyn_Access_List_Ipproto_Exceed_Max(self):
        '''[Documentation]  Test_Objective: Verify DACL not created as the IP protocol type exceeds the maximum '''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name,'configure netlogin add mac-list default {}'.format(self.tb.config.default_password))

        print('  (Step_2) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC29.name,
                                                         self.tb.config.packetDAC29.dst_mac,
                                                         self.tb.config.packetDAC29.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC30.name,
                                                         self.tb.config.packetDAC30.dst_mac,
                                                         self.tb.config.packetDAC30.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_3) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC29.name,
                                                                             self.tb.config.packetDAC30.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC29.name,
                                                                                     self.tb.config.packetDAC30.name,
                                                                                     self.tb.config.packetDAC30.name,
                                                                                     self.tb.config.packetDAC29.name,
                                                                                     self.tb.config.packetDAC29.src_mac,
                                                                                     self.tb.config.packetDAC30.src_mac,
                                                                                     tx_count=25)

        print('  (Step_4) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC29.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC30.src_mac,
                                                                                  self.tb.config.pvid_dac2,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_5) Verify DACLs not created as ipproto type exceeds maximum')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  self.tb.config.
                                                                                                  policyId_dac1)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  self.tb.config.
                                                                                                  policyId_dac2)
        print('  (Step_6) Calling test case cleanup function')
        self.Cleanup_05()

    def Cleanup_05(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_06_Dyn_Access_List_Ipproto_Hex_Exceed_Max(self):
        '''[Documentation]  Test_Objective: Verify DACL not created as IP protocol type in Hex exceeds the maximum '''

        print('  (Step_3) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_5) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC31.name,
                                                         self.tb.config.packetDAC31.dst_mac,
                                                         self.tb.config.packetDAC31.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC32.name,
                                                         self.tb.config.packetDAC32.dst_mac,
                                                         self.tb.config.packetDAC32.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_6) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC31.name,
                                                                             self.tb.config.packetDAC32.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC31.name,
                                                                                     self.tb.config.packetDAC32.name,
                                                                                     self.tb.config.packetDAC32.name,
                                                                                     self.tb.config.packetDAC31.name,
                                                                                     self.tb.config.packetDAC31.src_mac,
                                                                                     self.tb.config.packetDAC32.src_mac,
                                                                                     tx_count=25)

        print('  (Step_7) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC31.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC32.src_mac,
                                                                                  self.tb.config.pvid_dac2,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_8) Verify DACLs not created as ipproto type exceeds maximum')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  self.tb.config.
                                                                                                  policyId_dac1)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  self.tb.config.
                                                                                                  policyId_dac2)
        print('  (Step_9) Calling test case cleanup function')
        self.Cleanup_06()

    def Cleanup_06(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_07_Dyn_Access_List_Ipproto_Invalid_Mask(self):
        '''[Documentation]  Test_Objective: Verify DACL not created as IP protocol type has invalid mask '''

        print('  (Step_3) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_5) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC33.name,
                                                         self.tb.config.packetDAC33.dst_mac,
                                                         self.tb.config.packetDAC33.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC34.name,
                                                         self.tb.config.packetDAC34.dst_mac,
                                                         self.tb.config.packetDAC34.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_6) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC33.name,
                                                                             self.tb.config.packetDAC34.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC33.name,
                                                                                     self.tb.config.packetDAC34.name,
                                                                                     self.tb.config.packetDAC34.name,
                                                                                     self.tb.config.packetDAC33.name,
                                                                                     self.tb.config.packetDAC33.src_mac,
                                                                                     self.tb.config.packetDAC34.src_mac,
                                                                                     tx_count=25)

        print('  (Step_7) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC33.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC34.src_mac,
                                                                                  self.tb.config.pvid_dac2,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_8) Verify DACLs not created as ipproto type exceeds maximum')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  self.tb.config.
                                                                                                  policyId_dac1)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  self.tb.config.
                                                                                                  policyId_dac2)
        print('  (Step_9) Calling test case cleanup function')
        self.Cleanup_07()

    def Cleanup_07(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)