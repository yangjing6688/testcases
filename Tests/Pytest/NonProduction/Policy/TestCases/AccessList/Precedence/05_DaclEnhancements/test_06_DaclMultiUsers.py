from Tests.Staging.Functional.Policy.TestCases.PolicyBase import PolicyBase
from pytest import mark
from pytest import fixture


@fixture()
def test_setup_teardown(request):
    # Setup_section
    def teardown():
        request.instance.Test_Case_Cleanup()
    request.addfinalizer(teardown)


class DaclMultiUsersTests(PolicyBase):

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

        print('  (Class teardown Step_1) Unconfigure and disable netlogin server')
        cls.localPolicyUdks.radiusSuiteUdks.UnConfigure_And_Disable_Radius_Netlogin_Server(cls.tb.config.netelem1.name,
                                                                                           cls.tb.config.endsysRadius.
                                                                                           instance,
                                                                                           cls.tb.config.endsysRadius.
                                                                                           ip)

        print('  (Class setup Step_2) Call DACL teardown function to remove common policy and radius settings')
        cls.localPolicyUdks.Policy_Test_Case_Teardown_Dacl(cls.tb.config.netelem1)

        print('  (Class teardown Step_3) Call the base class teardown method disconnects DUT connections')
        PolicyBase.teardown_class()

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_01_Dyn_Access_List_Multi_Users_Create(self):
        '''[Documentation]  Test_Objective: Verify when 2 users authenticate to the same profile,
         a DACL is created with the match conditions associated with the first users radius entry.
         Verify traffic source from either user, matching the DACL is forwarded and traffic not matching
         the DACL is not forwarded.  Verify the DACL is maintained if the first users auth is cleared,
         and verify the DACL is deleted if then the second users auth is cleared.  In this test the profile is not
         pre existing and the user entries have the rc flag set'''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_2) Create VLAN and add egress ports as untagged')
        self.localPolicyUdks.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.tb.config.netelem1.name, self.tb.config.
                                                                       vlan_a)
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   self.tb.config.
                                                                                                   vlan_a,
                                                                                                   self.tb.config.
                                                                                                   netelem1.tgen.
                                                                                                   port_a.ifname)
        self.localPolicyUdks.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   self.tb.config.
                                                                                                   vlan_a,
                                                                                                   self.tb.config.
                                                                                                   netelem1.tgen.port_b.
                                                                                                   ifname)

        print('  (Step_3) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_UDP_Packet(self.tb.config.packetDAC63.name,
                                                             self.tb.config.packetDAC63.dst_mac,
                                                             self.tb.config.packetDAC63.src_mac,
                                                             sip=self.tb.config.src_ip_a,
                                                             dip=self.tb.config.dst_ip_a,
                                                             src_port=self.tb.config.udp_src_port,
                                                             dst_port=self.tb.config.udp_dst_port)
        self.localPolicyUdks.tgenUdks.Create_IPv4_UDP_Packet(self.tb.config.packetDAC64.name,
                                                             self.tb.config.packetDAC64.dst_mac,
                                                             self.tb.config.packetDAC64.src_mac,
                                                             sip=self.tb.config.src_ip_a,
                                                             dip=self.tb.config.dst_ip_a,
                                                             src_port=self.tb.config.udp_src_port,
                                                             dst_port=self.tb.config.udp_dst_port)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC63.name,
                                                                             self.tb.config.packetDAC64.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1
                                                                                     .port_b,
                                                                                     self.tb.config.packetDAC63.name,
                                                                                     self.tb.config.packetDAC64.name,
                                                                                     self.tb.config.packetDAC64.name,
                                                                                     self.tb.config.packetDAC63.name,
                                                                                     self.tb.config.packetDAC63.src_mac,
                                                                                     self.tb.config.packetDAC64.src_mac,
                                                                                     tx_count=25)

        print('  (Step_5) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC63.src_mac,
                                                                                  self.tb.config.vlan_a,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC64.src_mac,
                                                                                  self.tb.config.vlan_a,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_6) Verify DACL contains L4 port ranges associated with first users radius entry - udp')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id="1",
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id="1",
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32")

        print('  (Step_6a) Verify policy profile is created')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_profile_exists(self.tb.config.netelem1.name,
                                                                                          profile_ids="1")
        print('  (Step_7) Clear the authentication for the first user')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name, 'clear netlogin state port {}'.format(self.tb.config.netelem1.tgen.port_a.
                                                                                ifname))

        print('  (Step_8) Verify DACL still contains L4 port ranges associated with first users radius entry - udp')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id="1",
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id="1",
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32")
        print('  (Step_8a) Verify policy profile still exists')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_profile_exists(self.tb.config.netelem1.name,
                                                                                          profile_ids="1")
        print('  (Step_9) Clear the authentication for the second user')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name, 'clear netlogin state port {}'.format(self.tb.config.netelem1.tgen.port_b.
                                                                               ifname))

        print('  (Step_10) Verify the DACL is deleted')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  profile_id="1")
        print('  (Step_10a) Verify policy profile is deleted')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_profile_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  profile_ids="1")
        print('  (Step_11) Calling test case cleanup function')
        self.Cleanup_01()

    def Cleanup_01(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name, 'clear netlogin state port {},{}'.format(self.tb.config.netelem1.tgen.port_a.
                                                                                   ifname,
                                                                                   self.tb.config.netelem1.tgen.port_b.
                                                                                   ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC63.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac1,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC64.
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
    def test_02_Dyn_Access_List_Multi_Users_Existing(self):
        '''[Documentation]  Test_Objective: Verify when 2 users authenticate to the same profile,
         a DACL is created with the match conditions associated with the first users radius entry.
         Verify traffic source from either user, matching the DACL is forwarded and traffic not matching
         the DACL is not forwarded.  Verify the DACL is maintained if the first users auth is cleared,
         and verify the DACL is deleted if then the second users auth is cleared.  In this test the profile is
         pre existing with an ACL name and the user entries have the rc flag set'''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_2) Create a single Policy Profile specify ACL name as same as profile name')
        self.localPolicyUdks.Create_Policy_Profile_with_Name_PVID_and_ACL(
            self.tb.config.netelem1.name, self.tb.config.policyId_dac1, self.tb.config.policyName_dac1,
            self.tb.config.policyName_dac1, self.tb.config.pvid_dac1)

        print('  (Step_3) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_UDP_Packet(self.tb.config.packetDAC63.name,
                                                             self.tb.config.packetDAC63.dst_mac,
                                                             self.tb.config.packetDAC63.src_mac,
                                                             sip=self.tb.config.src_ip_a,
                                                             dip=self.tb.config.dst_ip_a,
                                                             src_port=self.tb.config.udp_src_port,
                                                             dst_port=self.tb.config.udp_dst_port)
        self.localPolicyUdks.tgenUdks.Create_IPv4_UDP_Packet(self.tb.config.packetDAC64.name,
                                                             self.tb.config.packetDAC64.dst_mac,
                                                             self.tb.config.packetDAC64.src_mac,
                                                             sip=self.tb.config.src_ip_a,
                                                             dip=self.tb.config.dst_ip_a,
                                                             src_port=self.tb.config.udp_src_port,
                                                             dst_port=self.tb.config.udp_dst_port)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC63.name,
                                                                             self.tb.config.packetDAC64.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1
                                                                                     .port_b,
                                                                                     self.tb.config.packetDAC63.name,
                                                                                     self.tb.config.packetDAC64.name,
                                                                                     self.tb.config.packetDAC64.name,
                                                                                     self.tb.config.packetDAC63.name,
                                                                                     self.tb.config.packetDAC63.src_mac,
                                                                                     self.tb.config.packetDAC64.src_mac,
                                                                                     tx_count=25)

        print('  (Step_5) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC63.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC64.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_6) Verify DACL contains L4 port ranges associated with first users radius entry - udp')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id=self.tb.
                                                                                                    config.
                                                                                                    policyId_dac1,
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id=self.tb.
                                                                                                   config.
                                                                                                   policyId_dac1,
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32")

        print('  (Step_7) Clear the authentication for the first user')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name, 'clear netlogin state port {}'.format(self.tb.config.netelem1.tgen.port_a.
                                                                                ifname))

        print('  (Step_8) Verify DACL still contains L4 port ranges associated with first users radius entry - udp')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id=self.tb.
                                                                                                    config.
                                                                                                    policyId_dac1,
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id=self.tb.
                                                                                                   config.
                                                                                                   policyId_dac1,
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32")

        print('  (Step_9) Clear the authentication for the second user')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name, 'clear netlogin state port {}'.format(self.tb.config.netelem1.tgen.port_b.
                                                                                ifname))

        print('  (Step_10) Verify the DACL is deleted')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  profile_id=self.tb.
                                                                                                  config.
                                                                                                  policyId_dac1)
        print('  (Step_11) Calling test case cleanup function')
        self.Cleanup_02()

    def Cleanup_02(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name, 'clear netlogin state port {},{}'.format(self.tb.config.netelem1.tgen.port_a.
                                                                                   ifname,
                                                                                   self.tb.config.netelem1.tgen.port_b.
                                                                                   ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC63.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac1,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC64.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac2,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_b.ifname)

        print('  (Test Case cleanup Step_3) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

        print('  (Test Case cleanup Step_4) Delete the policy profile')
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,
                                                                                        self.tb.config.policyId_dac1)

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_03_Dyn_Access_List_multi_tunnel(self):
        '''[Documentation]  Test_Objective: Verify when 2 users authenticate to the same profile,
         a DACL is created with the match conditions associated with the first users radius entry.
         Verify traffic source from either user, matching the DACL is forwarded and traffic not matching
         the DACL is not forwarded.  Verify the DACL is maintained if the first users auth is cleared,
         and verify the DACL is deleted if then the second users auth is cleared.  In this test the profile is not
         pre existing, the user entries have the rc flag set, and the vlan is obtained from the tunnel attribute
         (maptable response is set to both) '''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_2) Enable policy vlan authorization')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure policy vlanauthorization enable')

        print('  (Step_3) Set maptable response to both')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name,
                                                                                          'both')

        print('  (Step_4) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_UDP_Packet(self.tb.config.packetDAC65.name,
                                                             self.tb.config.packetDAC65.dst_mac,
                                                             self.tb.config.packetDAC65.src_mac,
                                                             sip=self.tb.config.src_ip_a,
                                                             dip=self.tb.config.dst_ip_a,
                                                             src_port=self.tb.config.udp_src_port,
                                                             dst_port=self.tb.config.udp_dst_port)
        self.localPolicyUdks.tgenUdks.Create_IPv4_UDP_Packet(self.tb.config.packetDAC66.name,
                                                             self.tb.config.packetDAC66.dst_mac,
                                                             self.tb.config.packetDAC66.src_mac,
                                                             sip=self.tb.config.src_ip_a,
                                                             dip=self.tb.config.dst_ip_a,
                                                             src_port=self.tb.config.udp_src_port,
                                                             dst_port=self.tb.config.udp_dst_port)

        print('  (Step_5) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC65.name,
                                                                             self.tb.config.packetDAC66.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1
                                                                                     .port_b,
                                                                                     self.tb.config.packetDAC65.name,
                                                                                     self.tb.config.packetDAC66.name,
                                                                                     self.tb.config.packetDAC66.name,
                                                                                     self.tb.config.packetDAC65.name,
                                                                                     self.tb.config.packetDAC65.src_mac,
                                                                                     self.tb.config.packetDAC66.src_mac,
                                                                                     tx_count=25)

        print('  (Step_6) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC65.src_mac,
                                                                                  self.tb.config.vlan_tunnel,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC66.src_mac,
                                                                                  self.tb.config.vlan_tunnel,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_7) Verify DACL contains L4 port ranges associated with first users radius entry - udp')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id="1",
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id="1",
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32")

        print('  (Step_7a) Verify policy profile is created')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_profile_exists(self.tb.config.netelem1.name,
                                                                                          profile_ids="1")

        print('  (Step_7b) Verify vlan is created from user entry tunnel attribute')
        self.localPolicyUdks.networkElementVlanGenKeywords.vlan_verify_exists(self.tb.config.netelem1.name,
                                                                              self.tb.config.vlan_tunnel)

        print('  (Step_8) Clear the authentication for the first user')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name, 'clear netlogin state port {}'.format(self.tb.config.netelem1.tgen.port_a.
                                                                                ifname))

        print('  (Step_9) Verify DACL still contains L4 port ranges associated with first users radius entry - udp')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id="1",
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id="1",
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32")
        print('  (Step_10) Verify policy profile still exists')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_profile_exists(self.tb.config.netelem1.name,
                                                                                          profile_ids="1")
        print('  (Step_11) Clear the authentication for the second user')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name, 'clear netlogin state port {}'.format(self.tb.config.netelem1.tgen.port_b.
                                                                                ifname))

        print('  (Step_12) Verify the DACL is deleted')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  profile_id="1")
        print('  (Step_12a) Verify policy profile is deleted')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_profile_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  profile_ids="1")
        print('  (Step_13) Calling test case cleanup function')
        self.Cleanup_03()

    def Cleanup_03(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name, 'clear netlogin state port {},{}'.format(self.tb.config.netelem1.tgen.port_a.
                                                                                   ifname,
                                                                                   self.tb.config.netelem1.tgen.port_b.
                                                                                   ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC65.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_tunnel,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC66.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_tunnel,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_b.ifname)

        print('  (Test Case cleanup Step_3) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

        print('  (Test Case cleanup Step_4) Disable policy vlan authorization')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure policy vlanauthorization disable')

        print('  (Test Case cleanup Step_5) Set maptable response to policy')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name,
                                                                                          'policy')

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_04_Dyn_Access_List_Multi_Existing_tunnel(self):
        '''[Documentation]  Test_Objective: Verify when 2 users authenticate to the same profile,
         a DACL is created with the match conditions associated with the first users radius entry.
         Verify traffic source from either user, matching the DACL is forwarded and traffic not matching
         the DACL is not forwarded.  Verify the DACL is maintained if the first users auth is cleared,
         and verify the DACL is deleted if then the second users auth is cleared.  In this test the profile is
         pre existing with an ACL name and no PVID .  The vlan is obtained from the tunnel attribute, maptable response
         is set to both and the user entries have the rc flag set'''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_2) Enable policy vlan authorization')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure policy vlanauthorization enable')

        print('  (Step_3) Set maptable response to both')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name,
                                                                                          'both')

        print('  (Step_4) Create a single Policy Profile specify ACL name as same as profile name no PVID')
        self.localPolicyUdks.Create_Policy_Profile_with_Name_and_ACL(
            self.tb.config.netelem1.name, self.tb.config.policyId_dac1, self.tb.config.policyName_dac1,
            self.tb.config.policyName_dac1)

        print('  (Step_5) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_UDP_Packet(self.tb.config.packetDAC65.name,
                                                             self.tb.config.packetDAC65.dst_mac,
                                                             self.tb.config.packetDAC65.src_mac,
                                                             sip=self.tb.config.src_ip_a,
                                                             dip=self.tb.config.dst_ip_a,
                                                             src_port=self.tb.config.udp_src_port,
                                                             dst_port=self.tb.config.udp_dst_port)
        self.localPolicyUdks.tgenUdks.Create_IPv4_UDP_Packet(self.tb.config.packetDAC66.name,
                                                             self.tb.config.packetDAC66.dst_mac,
                                                             self.tb.config.packetDAC66.src_mac,
                                                             sip=self.tb.config.src_ip_a,
                                                             dip=self.tb.config.dst_ip_a,
                                                             src_port=self.tb.config.udp_src_port,
                                                             dst_port=self.tb.config.udp_dst_port)

        print('  (Step_6) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC65.name,
                                                                             self.tb.config.packetDAC66.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1
                                                                                     .port_b,
                                                                                     self.tb.config.packetDAC65.name,
                                                                                     self.tb.config.packetDAC66.name,
                                                                                     self.tb.config.packetDAC66.name,
                                                                                     self.tb.config.packetDAC65.name,
                                                                                     self.tb.config.packetDAC65.src_mac,
                                                                                     self.tb.config.packetDAC66.src_mac,
                                                                                     tx_count=25)

        print('  (Step_7) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC65.src_mac,
                                                                                  self.tb.config.vlan_tunnel,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC66.src_mac,
                                                                                  self.tb.config.vlan_tunnel,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_8) Verify DACL contains L4 port ranges associated with first users radius entry - udp')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id=self.tb.
                                                                                                    config.
                                                                                                    policyId_dac1,
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id=self.tb.
                                                                                                   config.
                                                                                                   policyId_dac1,
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32")

        print('  (Step_8a) Verify policy profile is created')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_profile_exists(self.tb.config.netelem1.name,
                                                                                          profile_ids=self.tb.
                                                                                          config.
                                                                                          policyId_dac1)

        print('  (Step_8b) Verify vlan is created from user entry tunnel attribute')
        self.localPolicyUdks.networkElementVlanGenKeywords.vlan_verify_exists(self.tb.config.netelem1.name,
                                                                              self.tb.config.vlan_tunnel)

        print('  (Step_9) Clear the authentication for the first user')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name, 'clear netlogin state port {}'.format(self.tb.config.netelem1.tgen.port_a.
                                                                                ifname))

        print('  (Step_10) Verify DACL still contains L4 port ranges associated with first users radius entry - udp')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id=self.tb.
                                                                                                    config.
                                                                                                    policyId_dac1,
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id=self.tb.
                                                                                                   config.
                                                                                                   policyId_dac1,
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32")

        print('  (Step_11) Clear the authentication for the second user')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name, 'clear netlogin state port {}'.format(self.tb.config.netelem1.tgen.port_b.
                                                                                ifname))

        print('  (Step_12) Verify the DACL is deleted')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  profile_id=self.tb.
                                                                                                  config.
                                                                                                  policyId_dac1)
        print('  (Step_13) Calling test case cleanup function')
        self.Cleanup_04()

    def Cleanup_04(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name, 'clear netlogin state port {},{}'.format(self.tb.config.netelem1.tgen.port_a.
                                                                                   ifname,
                                                                                   self.tb.config.netelem1.tgen.port_b.
                                                                                   ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC65.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_tunnel,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC66.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_tunnel,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_b.ifname)

        print('  (Test Case cleanup Step_3) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

        print('  (Test Case cleanup Step_4) Delete the policy profile')
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,
                                                                                        self.tb.config.policyId_dac1)

        print('  (Test Case cleanup Step_5) Disable policy vlan authorization')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure policy vlanauthorization disable')

        print('  (Test Case cleanup Step_6) Set maptable response to policy')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name,
                                                                                          'policy')

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_05_Dyn_Access_List_Multi_Acl_Tunnel(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL created with multiple ACL entries within a user entry,
         no matching profile on the device. Both entries use the rc flags. The VLAN is obtained from the tunnel
           attribute '''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))


        print('  (Step_2) Enable policy vlan authorization')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure policy vlanauthorization enable')

        print('  (Step_3) Set maptable response to both')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name,
                                                                                          'both')
        print('  (Step_4) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_UDP_Packet(self.tb.config.packetDAC67.name,
                                                             self.tb.config.packetDAC67.dst_mac,
                                                             self.tb.config.packetDAC67.src_mac,
                                                             sip=self.tb.config.src_ip_a,
                                                             dip=self.tb.config.dst_ip_a,
                                                             src_port=self.tb.config.udp_src_port,
                                                             dst_port=self.tb.config.udp_dst_port)

        self.localPolicyUdks.tgenUdks.Create_IPv4_TCP_Packet(self.tb.config.packetDAC68.name,
                                                             self.tb.config.packetDAC68.dst_mac,
                                                             self.tb.config.packetDAC68.src_mac,
                                                             sip=self.tb.config.dst_ip_a,
                                                             dip=self.tb.config.src_ip_a,
                                                             src_port=self.tb.config.tcp_src_port,
                                                             dst_port=self.tb.config.tcp_dst_port)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC67.name,
                                                                             self.tb.config.packetDAC68.name,
                                                                             tx_count=100)

        print('  (Step_5) Send the traffic to verify forwarding')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC67.name,
                                                                                     self.tb.config.packetDAC68.name,
                                                                                     self.tb.config.packetDAC68.name,
                                                                                     self.tb.config.packetDAC67.name,
                                                                                     self.tb.config.packetDAC67.src_mac,
                                                                                     self.tb.config.packetDAC68.src_mac,
                                                                                     tx_count=100)

        print('  (Step_6) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC67.src_mac,
                                                                                  self.tb.config.vlan_tunnel,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC68.src_mac,
                                                                                  self.tb.config.vlan_tunnel,
                                                                                  self.tb.config.netelem1.tgen.
                                                                                  port_b.ifname)

        print('  (Step_7) Verify DACLs for user 1 contain expected L4 port ranges - both tcp and udp used')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id="1",
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id="1",
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32")

        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id="1",
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac2_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id="1",
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac2_src_range,
                                                                                                   mask="32")

        print('  (Step_7a) Verify DACLs for user 2 contain expected L4 port ranges - both tcp and udp used')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id="2",
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id="2",
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32")

        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id="2",
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac2_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id="2",
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac2_src_range,
                                                                                                   mask="32")

        print('  (Step_8) Verify DACLs contain ipproto type of icmp')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipproto(self.tb.config.netelem1.
                                                                                           name,
                                                                                           profile_id="1",
                                                                                           ipproto=self.tb.config.
                                                                                           ipproto_icmp,
                                                                                           mask="8")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipproto(self.tb.config.netelem1.
                                                                                           name,
                                                                                           profile_id="2",
                                                                                           ipproto=self.tb.config.
                                                                                           ipproto_icmp,
                                                                                           mask="8")

        print('  (Step_9) Verify DACLs contain fall through match any with action of drop')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id="1", item="Any",
                                                                                              action="drop")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id="2", item="Any",
                                                                                              action="drop")
        print('  (Step_10) Calling test case cleanup function')
        self.Cleanup_05()

    def Cleanup_05(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                                   self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC67.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_tunnel,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC68.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_tunnel,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_b.ifname)

        print('  (Test Case cleanup Step_3) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

        print('  (Test Case cleanup Step_4) Disable policy vlan authorization')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure policy vlanauthorization disable')

        print('  (Test Case cleanup Step_5) Set maptable response to policy')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name,
                                                                                          'policy')

    @mark.F_1000_0202
    @mark.EXOS
    @mark.P3
    @mark.Precedence_ACL
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6
    def test_06_Dyn_Access_List_Multi_Acl_Tunnel_Existing(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL created with multiple ACL entries within a user entry,
         matching profile with ACL name but no PVID on the device. Both entries use the rc flags.
         The VLAN is obtained from the tunnel attribute '''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))


        print('  (Step_2) Enable policy vlan authorization')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure policy vlanauthorization enable')

        print('  (Step_3) Set maptable response to both')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name,
                                                                                          'both')

        print('  (Step_4) Create Policy Profiles, specify ACL name as same as profile name no PVID')
        self.localPolicyUdks.Create_Policy_Profile_with_Name_and_ACL(
            self.tb.config.netelem1.name, self.tb.config.policyId_dac1, self.tb.config.policyName_dac1,
            self.tb.config.policyName_dac1)
        self.localPolicyUdks.Create_Policy_Profile_with_Name_and_ACL(
            self.tb.config.netelem1.name, self.tb.config.policyId_dac2, self.tb.config.policyName_dac2,
            self.tb.config.policyName_dac2)

        print('  (Step_4) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_UDP_Packet(self.tb.config.packetDAC67.name,
                                                             self.tb.config.packetDAC67.dst_mac,
                                                             self.tb.config.packetDAC67.src_mac,
                                                             sip=self.tb.config.src_ip_a,
                                                             dip=self.tb.config.dst_ip_a,
                                                             src_port=self.tb.config.udp_src_port,
                                                             dst_port=self.tb.config.udp_dst_port)

        self.localPolicyUdks.tgenUdks.Create_IPv4_TCP_Packet(self.tb.config.packetDAC68.name,
                                                             self.tb.config.packetDAC68.dst_mac,
                                                             self.tb.config.packetDAC68.src_mac,
                                                             sip=self.tb.config.dst_ip_a,
                                                             dip=self.tb.config.src_ip_a,
                                                             src_port=self.tb.config.tcp_src_port,
                                                             dst_port=self.tb.config.tcp_dst_port)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC67.name,
                                                                             self.tb.config.packetDAC68.name,
                                                                             tx_count=100)

        print('  (Step_5) Send the traffic to verify forwarding')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC67.name,
                                                                                     self.tb.config.packetDAC68.name,
                                                                                     self.tb.config.packetDAC68.name,
                                                                                     self.tb.config.packetDAC67.name,
                                                                                     self.tb.config.packetDAC67.src_mac,
                                                                                     self.tb.config.packetDAC68.src_mac,
                                                                                     tx_count=100)

        print('  (Step_6) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC67.src_mac,
                                                                                  self.tb.config.vlan_tunnel,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC68.src_mac,
                                                                                  self.tb.config.vlan_tunnel,
                                                                                  self.tb.config.netelem1.tgen.
                                                                                  port_b.ifname)

        print('  (Step_7) Verify DACLs for user 1 contain expected L4 port ranges - both tcp and udp used')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id=self.tb.
                                                                                                    config.policyId_dac1,
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id=self.tb.
                                                                                                   config.policyId_dac1,
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32")

        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id=self.tb.
                                                                                                    config.policyId_dac1,
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac2_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id=self.tb.
                                                                                                   config.policyId_dac1,
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac2_src_range,
                                                                                                   mask="32")

        print('  (Step_7a) Verify DACLs for user 2 contain expected L4 port ranges - both tcp and udp used')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id=self.tb.
                                                                                                    config.policyId_dac2,
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id=self.tb.
                                                                                                   config.policyId_dac2,
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32")

        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id=self.tb.
                                                                                                    config.policyId_dac2,
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac2_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id=self.tb.
                                                                                                   config.policyId_dac2,
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac2_src_range,
                                                                                                   mask="32")

        print('  (Step_8) Verify DACLs contain ipproto type of icmp')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipproto(self.tb.config.netelem1.
                                                                                           name,
                                                                                           profile_id=self.tb.
                                                                                           config.policyId_dac1,
                                                                                           ipproto=self.tb.config.
                                                                                           ipproto_icmp,
                                                                                           mask="8")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipproto(self.tb.config.netelem1.
                                                                                           name,
                                                                                           profile_id=self.tb.
                                                                                           config.policyId_dac2,
                                                                                           ipproto=self.tb.config.
                                                                                           ipproto_icmp,
                                                                                           mask="8")

        print('  (Step_9) Verify DACLs contain fall through match any with action of drop')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id=self.tb.
                                                                                              config.policyId_dac1,
                                                                                              item="Any", action="drop")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id=self.tb.
                                                                                              config.policyId_dac2,
                                                                                              item="Any", action="drop")
        print('  (Step_10) Calling test case cleanup function')
        self.Cleanup_06()

    def Cleanup_06(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                                   self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC67.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_tunnel,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC68.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_tunnel,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_b.ifname)

        print('  (Test Case cleanup Step_3) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

        print('  (Test Case cleanup Step_4) Disable policy vlan authorization')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure policy vlanauthorization disable')

        print('  (Test Case cleanup Step_5) Set maptable response to policy')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name,
                                                                                          'policy')

        print('  (Test Case cleanup Step_6) Delete the policy profile')
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
    @mark.GAS_NEW
    def test_07_Dyn_Access_List_Multi_Acl_Mismatch(self):
        '''[Documentation]  Test_Objective: Multiple ACL entries exist within a user entry but mismatching setting of
         r or rc type flag.  Verify DACL's created up to the point where the first mismatch occurs but none are created
         at the point of the mismatch and after. First user has tcp ranges only.  Second user has tcp and udp ranges,
         and ipproto=icmp.  Neither user has the match any drop since this is after the r flag mismatch.'''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))


        print('  (Step_2) Enable policy vlan authorization')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure policy vlanauthorization enable')

        print('  (Step_3) Set maptable response to both')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name,
                                                                                          'both')

        print('  (Step_4) Create Policy Profiles, specify ACL name as same as profile name no PVID')
        self.localPolicyUdks.Create_Policy_Profile_with_Name_and_ACL(
            self.tb.config.netelem1.name, self.tb.config.policyId_dac1, self.tb.config.policyName_dac1,
            self.tb.config.policyName_dac1)
        self.localPolicyUdks.Create_Policy_Profile_with_Name_and_ACL(
            self.tb.config.netelem1.name, self.tb.config.policyId_dac2, self.tb.config.policyName_dac2,
            self.tb.config.policyName_dac2)

        print('  (Step_4) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_UDP_Packet(self.tb.config.packetDAC69.name,
                                                             self.tb.config.packetDAC69.dst_mac,
                                                             self.tb.config.packetDAC69.src_mac,
                                                             sip=self.tb.config.src_ip_a,
                                                             dip=self.tb.config.dst_ip_a,
                                                             src_port=self.tb.config.udp_src_port,
                                                             dst_port=self.tb.config.udp_dst_port)

        self.localPolicyUdks.tgenUdks.Create_IPv4_TCP_Packet(self.tb.config.packetDAC6a.name,
                                                             self.tb.config.packetDAC6a.dst_mac,
                                                             self.tb.config.packetDAC6a.src_mac,
                                                             sip=self.tb.config.dst_ip_a,
                                                             dip=self.tb.config.src_ip_a,
                                                             src_port=self.tb.config.tcp_src_port,
                                                             dst_port=self.tb.config.tcp_dst_port)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC69.name,
                                                                             self.tb.config.packetDAC6a.name,
                                                                             tx_count=100)

        print('  (Step_5) Send the traffic to verify forwarding')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC69.name,
                                                                                     self.tb.config.packetDAC6a.name,
                                                                                     self.tb.config.packetDAC6a.name,
                                                                                     self.tb.config.packetDAC69.name,
                                                                                     self.tb.config.packetDAC69.src_mac,
                                                                                     self.tb.config.packetDAC6a.src_mac,
                                                                                     tx_count=100)

        print('  (Step_6) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC69.src_mac,
                                                                                  self.tb.config.vlan_tunnel,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC6a.src_mac,
                                                                                  self.tb.config.vlan_tunnel,
                                                                                  self.tb.config.netelem1.tgen.
                                                                                  port_b.ifname)

        print('  (Step_7) Verify DACL for user 1 contains tcp ranges src: 1100-1200 dst: 1200-1300 ')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id=self.tb.
                                                                                                    config.policyId_dac1,
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac2_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id=self.tb.
                                                                                                   config.policyId_dac1,
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac2_src_range,
                                                                                                   mask="32")

        print('  (Step_7a) Verify DACLs for user 2 contain tcp ranges, udp ranges, and ipproto=icmp ')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id=self.tb.
                                                                                                    config.policyId_dac2,
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id=self.tb.
                                                                                                   config.policyId_dac2,
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32")

        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id=self.tb.
                                                                                                    config.policyId_dac2,
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac2_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id=self.tb.
                                                                                                   config.policyId_dac2,
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac2_src_range,
                                                                                                   mask="32")

        print('  (Step_8) Verify user 2 DACLs contain ipproto type of icmp')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipproto(self.tb.config.netelem1.
                                                                                           name,
                                                                                           profile_id=self.tb.
                                                                                           config.policyId_dac2,
                                                                                           ipproto=self.tb.config.
                                                                                           ipproto_icmp,
                                                                                           mask="8")

        print('  (Step_9) Verify DACLs for user 1 doesnt contain udp ranges, ipproto=icmp, and match any ')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id=self.tb.
                                                                                                    config.policyId_dac1,
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32",
                                                                                                    expected_result=False)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_udpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id=self.tb.
                                                                                                   config.policyId_dac1,
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32",
                                                                                                   expected_result=False)

        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipproto(self.tb.config.netelem1.
                                                                                           name,
                                                                                           profile_id=self.tb.
                                                                                           config.policyId_dac1,
                                                                                           ipproto=self.tb.config.
                                                                                           ipproto_icmp,
                                                                                           mask="8",
                                                                                           expected_result=False)

        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id=self.tb.config.
                                                                                              policyId_dac1, item="Any",
                                                                                              expected_result=False)
        print('  (Step_9a) Verify DACLs for user 2 doent contain  match any ')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id=self.tb.config.
                                                                                              policyId_dac2, item="Any",
                                                                                              expected_result=False)
        print('  (Step_10) Calling test case cleanup function')
        self.Cleanup_07()

    def Cleanup_07(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                                   self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC69.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_tunnel,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC6a.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_tunnel,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_b.ifname)

        print('  (Test Case cleanup Step_3) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin del mac-list default',
                                                            ignore_cli_feedback=True)

        print('  (Test Case cleanup Step_4) Disable policy vlan authorization')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure policy vlanauthorization disable')

        print('  (Test Case cleanup Step_5) Set maptable response to policy')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name,
                                                                                          'policy')

        print('  (Test Case cleanup Step_6) Delete the policy profile')
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,
                                                                                        self.tb.config.policyId_dac1)
        self.localPolicyUdks.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,
                                                                                        self.tb.config.policyId_dac2)

