from Tests.Staging.Functional.Policy.TestCases.PolicyBase import PolicyBase
from pytest import mark
from pytest import fixture
import time


@fixture()
def test_setup_teardown(request):
    # Setup_section
    def teardown():
        request.instance.Test_Case_Cleanup()
    request.addfinalizer(teardown)


class DaclMatchComboTests(PolicyBase):

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
    def test_01_Dyn_Access_List_Match_Combo_Profile_ACL(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL created with Match on 5 parameters,
         a matching profile, and ACL Name configured on the profile.  Match requires r flag since L4 port range given.
         One entry uses the rc flag, the other entry uses the r flag'''

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
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC51.name,
                                                         self.tb.config.packetDAC51.dst_mac,
                                                         self.tb.config.packetDAC51.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC52.name,
                                                         self.tb.config.packetDAC52.dst_mac,
                                                         self.tb.config.packetDAC52.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC51.name,
                                                                             self.tb.config.packetDAC52.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1
                                                                                     .port_b,
                                                                                     self.tb.config.packetDAC51.name,
                                                                                     self.tb.config.packetDAC52.name,
                                                                                     self.tb.config.packetDAC52.name,
                                                                                     self.tb.config.packetDAC51.name,
                                                                                     self.tb.config.packetDAC51.src_mac,
                                                                                     self.tb.config.packetDAC52.src_mac,
                                                                                     tx_count=25)

        print('  (Step_5) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC51.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC52.src_mac,
                                                                                  self.tb.config.pvid_dac2,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_6) Verify DACLs contain expected L4 port ranges')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id=self.tb.
                                                                                                    config.
                                                                                                    policyId_dac2,
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac2_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id=self.tb.
                                                                                                   config.
                                                                                                   policyId_dac2,
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac2_src_range,
                                                                                                   mask="32")
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

        print('  (Step_7) Verify DACLs contain expected source and destination IP addresses and mask')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipsource(self.tb.config.netelem1.
                                                                                            name,
                                                                                            profile_id=self.tb.config.
                                                                                            policyId_dac1,
                                                                                            ipsource=self.tb.
                                                                                            config.src_ip_dac1,
                                                                                            mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipdest(self.tb.config.netelem1.
                                                                                            name,
                                                                                            profile_id=self.tb.config.
                                                                                            policyId_dac1,
                                                                                            ipdest=self.tb.
                                                                                            config.dst_ip_dac1,
                                                                                            mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipsource(self.tb.config.netelem1.
                                                                                            name,
                                                                                            profile_id=self.tb.config.
                                                                                            policyId_dac2,
                                                                                            ipsource=self.tb.
                                                                                            config.src_ip_dac2,
                                                                                            mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipdest(self.tb.config.netelem1.
                                                                                          name,
                                                                                          profile_id=self.tb.config.
                                                                                          policyId_dac2,
                                                                                          ipdest=self.tb.
                                                                                          config.dst_ip_dac2,
                                                                                          mask="32")

        print('  (Step_8) Calling test case cleanup function')
        self.Cleanup_01()

    def Cleanup_01(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name,'clear netlogin state port {},{}'.format(self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname))

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
    def test_02_Dyn_Access_List_Match_Combo_No_Profile_RC(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL created with 5 Match clauses, no matching profile.
          on the device. Both entries use the rc flags.  Also verify match any with action of drop created. '''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_2) Create VLAN and add egress ports as untagged')
        self.localPolicyUdks.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.tb.config.netelem1.name,self.tb.config.
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
        self.localPolicyUdks.tgenUdks.Create_IPv4_UDP_Packet(self.tb.config.packetDAC53.name,
                                                             self.tb.config.packetDAC53.dst_mac,
                                                             self.tb.config.packetDAC53.src_mac,
                                                             sip=self.tb.config.src_ip_a,
                                                             dip=self.tb.config.dst_ip_a,
                                                             src_port=self.tb.config.udp_src_port,
                                                             dst_port=self.tb.config.udp_dst_port)

        self.localPolicyUdks.tgenUdks.Create_IPv4_TCP_Packet(self.tb.config.packetDAC54.name,
                                                             self.tb.config.packetDAC54.dst_mac,
                                                             self.tb.config.packetDAC54.src_mac,
                                                             sip=self.tb.config.dst_ip_a,
                                                             dip=self.tb.config.src_ip_a,
                                                             src_port=self.tb.config.tcp_src_port,
                                                             dst_port=self.tb.config.tcp_dst_port)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC53.name,
                                                                             self.tb.config.packetDAC54.name,
                                                                             tx_count=100)

        print('  (Step_5) Send the traffic to verify forwarding')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC53.name,
                                                                                     self.tb.config.packetDAC54.name,
                                                                                     self.tb.config.packetDAC54.name,
                                                                                     self.tb.config.packetDAC53.name,
                                                                                     self.tb.config.packetDAC53.src_mac,
                                                                                     self.tb.config.packetDAC54.src_mac,
                                                                                     tx_count=100)

        print('  (Step_6) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC53.src_mac,
                                                                                  self.tb.config.vlan_a,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC54.src_mac,
                                                                                  self.tb.config.vlan_a,
                                                                                  self.tb.config.netelem1.tgen.
                                                                                  port_b.ifname)

        print('  (Step_7) Verify DACLs contain expected L4 port ranges')
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

        print('  (Step_8) Verify DACLs contain expected source and destination IP addresses and mask')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipsource(self.tb.config.netelem1.
                                                                                            name,
                                                                                            profile_id="1",
                                                                                            ipsource=self.tb.
                                                                                            config.src_ip_p1,
                                                                                            mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipdest(self.tb.config.netelem1.
                                                                                          name,
                                                                                          profile_id="1",
                                                                                          ipdest=self.tb.
                                                                                          config.dst_ip_p1,
                                                                                          mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipsource(self.tb.config.netelem1.
                                                                                            name,
                                                                                            profile_id="2",
                                                                                            ipsource=self.tb.
                                                                                            config.src_ip_p2,
                                                                                            mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_ipdest(self.tb.config.netelem1.
                                                                                          name,
                                                                                          profile_id="2",
                                                                                          ipdest=self.tb.
                                                                                          config.dst_ip_p2,
                                                                                          mask="32")

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
        self.Cleanup_02()

    def Cleanup_02(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC53.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_a,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC54.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_a,
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
    def test_03_Dyn_Access_List_Match_Ether_L4PortRange_Profile(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL created with Match on Ether type (ipv4) and
          tcp/upd port ranges.  Profiles and ACL names exist on the device '''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_2) Create Policy Profiles specify ACL name as same as profile name')
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

        print('  (Step_3) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC55.name,
                                                         self.tb.config.packetDAC55.dst_mac,
                                                         self.tb.config.packetDAC55.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC56.name,
                                                         self.tb.config.packetDAC56.dst_mac,
                                                         self.tb.config.packetDAC56.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC55.name,
                                                                             self.tb.config.packetDAC56.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.
                                                                                     netelem1.port_b,
                                                                                     self.tb.config.packetDAC55.name,
                                                                                     self.tb.config.packetDAC56.name,
                                                                                     self.tb.config.packetDAC56.name,
                                                                                     self.tb.config.packetDAC55.name,
                                                                                     self.tb.config.packetDAC55.src_mac,
                                                                                     self.tb.config.packetDAC56.src_mac,
                                                                                     tx_count=25)

        print('  (Step_5) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC55.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC56.src_mac,
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

        print('  (Step_7) Verify DACLs contain expected L4 port ranges')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id=self.tb.
                                                                                                    config.
                                                                                                    policyId_dac2,
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac2_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id=self.tb.
                                                                                                   config.
                                                                                                   policyId_dac2,
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac2_src_range,
                                                                                                   mask="32")
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

        print('  (Step_7) Calling test case cleanup function')
        self.Cleanup_03()

    def Cleanup_03(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC55.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac1,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC56.
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
    def test_04_Dyn_Access_List_Match_Ether_L4PortRange_No_Profile(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL created with Match Ether type (ipv4), ipproto tcp/udp in hex,
        L4 port range, and no matching profile exists on the device .  Each entry uses the rc flag'''

        print('  (Step_1) Create VLAN and add egress ports as untagged')
        self.localPolicyUdks.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.tb.config.netelem1.name,self.tb.config.
                                                                       vlan_a)
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
                                                                                                   netelem1.tgen.
                                                                                                   port_b.ifname)

        print('  (Step_2) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_3) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_UDP_Packet(self.tb.config.packetDAC57.name,
                                                             self.tb.config.packetDAC57.dst_mac,
                                                             self.tb.config.packetDAC57.src_mac,
                                                             sip=self.tb.config.src_ip_a,
                                                             dip=self.tb.config.dst_ip_a,
                                                             src_port=self.tb.config.udp_src_port,
                                                             dst_port=self.tb.config.udp_dst_port)

        self.localPolicyUdks.tgenUdks.Create_IPv4_TCP_Packet(self.tb.config.packetDAC58.name,
                                                             self.tb.config.packetDAC58.dst_mac,
                                                             self.tb.config.packetDAC58.src_mac,
                                                             sip=self.tb.config.dst_ip_a,
                                                             dip=self.tb.config.src_ip_a,
                                                             src_port=self.tb.config.tcp_src_port,
                                                             dst_port=self.tb.config.tcp_dst_port)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC57.name,
                                                                             self.tb.config.packetDAC58.name,
                                                                             tx_count=100)

        time.sleep(int(self.tb.config.dacl_delay))

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC57.name,
                                                                                     self.tb.config.packetDAC58.name,
                                                                                     self.tb.config.packetDAC58.name,
                                                                                     self.tb.config.packetDAC57.name,
                                                                                     self.tb.config.packetDAC57.src_mac,
                                                                                     self.tb.config.packetDAC58.src_mac,
                                                                                     tx_count=100)

        print('  (Step_5) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC57.src_mac,
                                                                                  self.tb.config.vlan_a,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC58.src_mac,
                                                                                  self.tb.config.vlan_a,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_6) Verify DACLs contain expected L4 port ranges')
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

        print('  (Step_7) Verify DACLs contain fall through match any with action of drop')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id="1", item="Any",
                                                                                              action="drop")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id="2", item="Any",
                                                                                              action="drop")

        print('  (Step_8) Calling test case cleanup function')
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
    def test_05_Dyn_Access_List_Match_Ether_Ipv6_Profile(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL created with Match on Ether type (ipv6) and
          in one case udp with l4 port ranges, in the case ipproto of icmpv6 (58).
           Profiles and ACL names exist on the device '''

        print('  (Step_1) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_2) Create Policy Profiles specify ACL name as same as profile name')
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

        print('  (Step_3) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC59.name,
                                                         self.tb.config.packetDAC59.dst_mac,
                                                         self.tb.config.packetDAC59.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC5a.name,
                                                         self.tb.config.packetDAC5a.dst_mac,
                                                         self.tb.config.packetDAC5a.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC59.name,
                                                                             self.tb.config.packetDAC5a.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC59.name,
                                                                                     self.tb.config.packetDAC5a.name,
                                                                                     self.tb.config.packetDAC5a.name,
                                                                                     self.tb.config.packetDAC59.name,
                                                                                     self.tb.config.packetDAC59.src_mac,
                                                                                     self.tb.config.packetDAC5a.src_mac,
                                                                                     tx_count=25)

        print('  (Step_5) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC59.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC5a.src_mac,
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

        print('  (Step_7) Verify DACL created with expected UDP port ranges')
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
        print('  (Step_7) Calling test case cleanup function')
        self.Cleanup_05()

    def Cleanup_05(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC59.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac1,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC5a.
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
    def test_06_Dyn_Access_List_Match_Ether_Ipv6_No_Profile(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL created with Match Ether type (ipv6), ipproto tcp/icmpv6 in hex,
        L4 port range for tcp case, and no matching profile exists on the device .  Each entry uses the rc flag'''

        print('  (Step_1) Create VLAN and add egress ports as untagged')
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

        print('  (Step_2) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_3) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv6_TCP_Packet(self.tb.config.packetDAC5b.name,
                                                             self.tb.config.packetDAC5b.dst_mac,
                                                             self.tb.config.packetDAC5b.src_mac,
                                                             sip=self.tb.config.src_ip6_a,
                                                             dip=self.tb.config.dst_ip6_a,
                                                             src_port=self.tb.config.udp_src_port,
                                                             dst_port=self.tb.config.udp_dst_port)

        self.localPolicyUdks.tgenUdks.Create_IPv6_ICMP_Packet(self.tb.config.packetDAC5c.name,
                                                             self.tb.config.packetDAC5c.dst_mac,
                                                             self.tb.config.packetDAC5c.src_mac,
                                                             sip=self.tb.config.dst_ip6_a,
                                                             dip=self.tb.config.src_ip6_a)

        print('  (Step_4) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC5b.name,
                                                                             self.tb.config.packetDAC5c.name,
                                                                             tx_count=100)

        time.sleep(int(self.tb.config.dacl_delay))

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC5b.name,
                                                                                     self.tb.config.packetDAC5c.name,
                                                                                     self.tb.config.packetDAC5c.name,
                                                                                     self.tb.config.packetDAC5b.name,
                                                                                     self.tb.config.packetDAC5b.src_mac,
                                                                                     self.tb.config.packetDAC5c.src_mac,
                                                                                     tx_count=100)

        print('  (Step_5) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC5b.src_mac,
                                                                                  self.tb.config.vlan_a,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC5c.src_mac,
                                                                                  self.tb.config.vlan_a,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_6) Verify DACLs created with expected match clauses')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          profile_id="1")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_exists(self.tb.config.netelem1.name,
                                                                                          profile_id="2")

        print('  (Step_7) Verify DACLs contain expected L4 port ranges')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpdestportrange(self.tb.config.
                                                                                                    netelem1.name,
                                                                                                    profile_id="1",
                                                                                                    port_range=self.tb.
                                                                                                    config.
                                                                                                    dac1_dst_range,
                                                                                                    mask="32")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_tcpsrcportrange(self.tb.config.
                                                                                                   netelem1.name,
                                                                                                   profile_id="1",
                                                                                                   port_range=self.tb.
                                                                                                   config.
                                                                                                   dac1_src_range,
                                                                                                   mask="32")

        print('  (Step_8) Verify DACLs contain fall through match any with action of drop')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id="1", item="Any",
                                                                                              action="drop")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_match_item(self.tb.config.netelem1.
                                                                                              name,
                                                                                              profile_id="2", item="Any",
                                                                                              action="drop")
        print('  (Step_9) Calling test case cleanup function')
        self.Cleanup_06()

    def Cleanup_06(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC5b.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_a,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist (self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC5c.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_a,
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
    def test_07_Dyn_Access_List_Match_Icmp_L4Range_Profile_ACL(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL not created with Match Ether (ipv4), ipproto (icmp),
        and an L4 port range which is inconsistent with icmp as ipproto type.
        Matching profiles and ACL name are configured on the device, one entry uses the r flag the other uses the
        rc flag. '''

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
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC5d.name,
                                                         self.tb.config.packetDAC5d.dst_mac,
                                                         self.tb.config.packetDAC5d.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC5e.name,
                                                         self.tb.config.packetDAC5e.dst_mac,
                                                         self.tb.config.packetDAC5e.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_6) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC5d.name,
                                                                             self.tb.config.packetDAC5e.name,
                                                                             tx_count=25)

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC5d.name,
                                                                                     self.tb.config.packetDAC5e.name,
                                                                                     self.tb.config.packetDAC5e.name,
                                                                                     self.tb.config.packetDAC5d.name,
                                                                                     self.tb.config.packetDAC5d.src_mac,
                                                                                     self.tb.config.packetDAC5e.src_mac,
                                                                                     tx_count=25)

        print('  (Step_7) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC5d.src_mac,
                                                                                  self.tb.config.pvid_dac1,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC5e.src_mac,
                                                                                  self.tb.config.pvid_dac2,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_8) Verify DACLs not created ')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  profile_id=self.tb.
                                                                                                  config.policyId_dac1)
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  profile_id=self.tb.
                                                                                                  config.policyId_dac2)

        print('  (Step_9) Calling test case cleanup function')
        self.Cleanup_07()

    def Cleanup_07(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC5d.
                                                                                          src_mac,
                                                                                          self.tb.config.pvid_dac1,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC5e.
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
    def test_08_Dyn_Access_List_Match_Icmp_Arp_L4Range_No_Profile(self):
        '''[Documentation]  Test_Objective: Verify Dynamic ACL not created with Match Ether (ipv4), ipproto (icmp or arp),
        and an L4 port range which is inconsistent with ipproto types.
        Matching profile do not exist on the device, both entries uses the rc flag. '''

        print('  (Step_1) Create VLAN and add egress ports as untagged')
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

        print('  (Step_2) Create Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'configure netlogin add mac-list default {}'.
                                                            format(self.tb.config.default_password))

        print('  (Step_3) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC61.name,
                                                         self.tb.config.packetDAC61.dst_mac,
                                                         self.tb.config.packetDAC61.src_mac,
                                                         sip=self.tb.config.src_ip_a,
                                                         dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(self.tb.config.packetDAC62.name,
                                                         self.tb.config.packetDAC62.dst_mac,
                                                         self.tb.config.packetDAC62.src_mac,
                                                         sip=self.tb.config.dst_ip_a,
                                                         dip=self.tb.config.src_ip_a)

        print('  (Step_6) Send the traffic to create initial authentication.')
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.config.tgen_ports.netelem1.port_a,
                                                                             self.tb.config.tgen_ports.netelem1.port_b,
                                                                             self.tb.config.packetDAC61.name,
                                                                             self.tb.config.packetDAC62.name,
                                                                             tx_count=25)

        time.sleep(int(self.tb.config.dacl_delay))

        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.config.tgen_ports.netelem1.
                                                                                     port_a,
                                                                                     self.tb.config.tgen_ports.netelem1.
                                                                                     port_b,
                                                                                     self.tb.config.packetDAC61.name,
                                                                                     self.tb.config.packetDAC62.name,
                                                                                     self.tb.config.packetDAC62.name,
                                                                                     self.tb.config.packetDAC61.name,
                                                                                     self.tb.config.packetDAC61.src_mac,
                                                                                     self.tb.config.packetDAC62.src_mac,
                                                                                     tx_count=25)

        print('  (Step_7) Verify FDB entries created for SRC Mac address on VLAN specified by profile PVID.')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC61.src_mac,
                                                                                  self.tb.config.vlan_a,
                                                                                  self.tb.config.netelem1.tgen.port_a.
                                                                                  ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,
                                                                                  self.tb.config.packetDAC62.src_mac,
                                                                                  self.tb.config.vlan_a,
                                                                                  self.tb.config.netelem1.tgen.port_b.
                                                                                  ifname)

        print('  (Step_8) Verify DACLs not created ')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  profile_id="1")
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_pid_does_not_exist(self.tb.config.
                                                                                                  netelem1.name,
                                                                                                  profile_id="2")

        print('  (Step_9) Calling test case cleanup function')
        self.Cleanup_08()

    def Cleanup_08(self):
        print('  (Test Case cleanup Step_1) Clear netlogin sessions')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,
                                                            'clear netlogin state port {},{}'.
                                                            format(self.tb.config.netelem1.tgen.port_a.ifname,
                                                            self.tb.config.netelem1.tgen.port_b.ifname))

        print('  (Test Case cleanup Step_2) Verify FDB entries are not present')
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC61.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_a,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_a.ifname)
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_does_not_exist(self.tb.config.netelem1.name,
                                                                                          self.tb.config.packetDAC62.
                                                                                          src_mac,
                                                                                          self.tb.config.vlan_a,
                                                                                          self.tb.config.netelem1.tgen.
                                                                                          port_b.ifname)

        print('  (Test Case cleanup Step_3) Delete Netlogin mac-list entries.')
        self.localPolicyUdks.networkElementCliSend.send_cmd(
            self.tb.config.netelem1.name,'configure netlogin del mac-list default',ignore_cli_feedback=True)

        print('  (Test Case cleanup Step_4) Delete VLAN')
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,self.tb.config.
                                                                           vlan_a)
