from Tests.Pytest.Functional.nonprod.AAA.Resources.AAASuiteUdks import AAASuiteUdks
from Tests.Pytest.Functional.nonprod.AAA.Resources.AAABase import  AAABase
from pytest import fixture, mark
from time import sleep

class Debug_AAATests(AAABase):
    
    def test_99_UPMVlan_Issue_Debug(self):
        '''[Documentation]  Test_Objective: Verify_UPM_Vlan_for_Policy_Profile_Enabled_Vlan
        [Tags]  UpmVlan'''
    
        self.aaaSuiteUdks.Test_Case_Setup()
    
        #Pass_Execution_Test_only_used_when_debugging_a_specific_issue.
    
        print('  (Step_1) Base_Setup_Enable_Policy, MacAuth_and_UPM_on_selected_ports.')
    
        self.aaaSuiteUdks.policyUDKs.Enable_Policy_and_Verify_it_is_Enabled(self.tb.config.netelem1.name)    
   
        #Enable_Macauth
        self.aaaSuiteUdks.macAuthUdks.Enable_Macauth_and_Verify_it_is_Enabled(self.tb.config.netelem1.name)
    #    enable_macauth_port_and_verify_it_is_enabled
        self.aaaSuiteUdks.macAuthUdks.Enable_Macauth_Port_and_Verify_it_is_Enabled(self.tb.config.netelem1.name,
                                                                        self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.macAuthUdks.Enable_Macauth_Port_and_Verify_it_is_Enabled(self.tb.config.netelem1.name,
                                                                        self.tb.config.netelem1.tgen.port_b.ifname)
        
        self.aaaSuiteUdks.tgenUdks.Create_Ethernet2_Packet(self.tb.config.packetA.name,self.tb.config.packetA.dst_mac, 
                                             self.tb.config.packetA.src_mac,packet_len=64)
        self.aaaSuiteUdks.tgenUdks.Create_Ethernet2_Packet(self.tb.config.packetB.name,self.tb.config.packetB.dst_mac, 
                                             self.tb.config.packetB.src_mac,packet_len=64)
        self.aaaSuiteUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.tgen_dut1_port_a, self.tb.tgen_dut1_port_b,
                                             self.tb.config.packetA.name, self.tb.config.packetB.name)
        
        print('  (Step_1a) Remove_Policy_Profile_in_Radius_Filter_ID_attribute.')
        self.aaaSuiteUdks.policyUDKs.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,
                                                                        self.tb.config.policyId_a)
        
        self.aaaSuiteUdks.policyUdks.Bounce_Netelem_Port(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.policyUdks.Bounce_Netelem_Port(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_b.ifname)
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)
        
        print('  (Verification_1) Remove_Authed_Policy (created_during_setup) Re-Auth_should_be_to_port_pvid.')
        
        # Prime the pump
        self.udks.trafficGenerationUdks.Prime_Traffic_Bidirectionally(self.tb.config.tgen_ports.netelem1.port_a, 
                    self.tb.config.tgen_ports.netelem1.port_b, self.tb.config.packetA.name, self.tb.config.packetB.name)
        # send the bidirectional packets
        self.udks.trafficGenerationUdks.Transmit_Traffic_Bidirectionally_and_Verify_it_was_Received(self.tb.config.tgen_ports.netelem1.port_a,
                    self.tb.config.tgen_ports.netelem1.tgen_port_b, self.tb.config.packetA.name, self.tb.config.packetB.name,
                    self.tb.config.packetB.name, self.tb.config.packetA.name, tx_count=10)
        
        self.cliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, "show fdb", ".*aa:aa:aa.*V500.*bb:bb:bb.*V500.*",max_wait=65)
        
        self.aaaSuiteUdks.Debug_Dump_UPM_Failure_Info()
        
        print('  (Step_2) Bounce_ports_to_clear_authed_user. Remove_Port_Vlan')
        
        self.aaaSuiteUdks.policyUdks.Bounce_Netelem_Port(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.policyUdks.Bounce_Netelem_Port(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_b.ifname)
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)
        
        self.defaultLibrary.aaaSuiteUdks.vlanUdks.Remove_Ports_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.tb.dut1.name, self.tb.config.vlan_500, self.tb.netelem1.tgen.port_a.ifname)
        self.defaultLibrary.aaaSuiteUdks.vlanUdks.Remove_Ports_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.tb.dut1.name, self.tb.config.vlan_500, self.tb.netelem1.tgen.port_b.ifname)
        
        print("  (Verification_2) Remove_Port_Vlan - No_VLAN_should_be_able_to_be_determined..")
        
        # Prime the pump
        self.udks.trafficGenerationUdks.Prime_Traffic_Bidirectionally(self.tb.config.tgen_ports.netelem1.port_a, 
                    self.tb.config.tgen_ports.netelem1.port_b, self.tb.config.packetA.name, self.tb.config.packetB.name)
        # send the bidirectional packets
        self.udks.trafficGenerationUdks.Transmit_Traffic_Bidirectionally_and_Verify_it_was_Received(self.tb.config.tgen_ports.netelem1.port_a,
                    self.tb.config.tgen_ports.netelem1.tgen_port_b, self.tb.config.packetA.name, self.tb.config.packetB.name,
                    self.tb.config.packetB.name, self.tb.config.packetA.name, tx_count=0)
        
        print('  (Verification - 1_THIS_works) any_5_characters_for_port_string_any_4_characters_for "(s) " following_VLAN')
        
        self.cliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, "show log", "..*00:00:00:BB:BB:BB_port .{1,5} VLAN....<unknown>.*00:00:00:AA:AA:AA_port .{1,5} VLAN....<unknown>.*",
                                                  max_wait=65)
        print('  (Verification - 2_FAILS_Escaping_parenthesis_does_not_seem_to_work.')
    
        self.cliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, "show log", 
                                                  "*00:00:00:BB:BB:BB_port .{1,5} VLAN\(s\) <unknown>.*00:00:00:AA:AA:AA_port .{1,5} VLAN\(s\) <unknown>.*")
    
        print('  (Verification - 3_FAILS_Attribute_substition_is_not_expanded_as_I_would_hope.')
    
        self.cliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  "show log",
              ".*00:00:00:BB:BB:BB_port ${netelem1.tgen.port_a.ifname} VLAN....<unknown> .*00:00:00:AA:AA:AA_port ${netelem1.tgen.port_a.ifname} VLAN....<unknown> .*")
        
        self.aaaSuiteUdks.Debug_Dump_UPM_Failure_Info()
    
        print('  (Step_3) Bounce_ports_to_clear_authed_user. Reconfigure_Port_Vlan_and_Policy')
        self.aaaSuiteUdks.policyUdks.Bounce_Netelem_Port(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.policyUdks.Bounce_Netelem_Port(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_b.ifname)
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)
        
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name, self.tb.config.vlan_500,self.tb.config.netelem1.tgen.port_a.ifname)
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name, self.tb.config.vlan_500,self.tb.config.netelem1.tgen.port_b.ifname)
        self.aaaSuiteUdks.policyUdks.Create_Policy_Profile_with_PVID_and_PVID_Status_Enabled(self.tb.config.netelem1.name, self.tb.config.policyId_a,
                                                                    self.tb.config.vlan_100)
        
        self.aaaSuiteUdks.policyUDKs.Create_Policy_Profile_with_Name_and_Verify_it_Exists(self.tb.config.netelem1.name,self.tb.config.policyId_a, 
                                                                         self.tb.config.policyName_a)
        
        print('  (Verification_3) Auth_to_the_VLAN (100) in_the_policy_profile_ID_returned_in_the_RADIUS_Response.')
        # Prime the pump
        self.udks.trafficGenerationUdks.Prime_Traffic_Bidirectionally(self.tb.config.tgen_ports.netelem1.port_a, 
                    self.tb.config.tgen_ports.netelem1.port_b, self.tb.config.packetA.name, self.tb.config.packetB.name)
        # send the bidirectional packets
        self.udks.trafficGenerationUdks.Transmit_Traffic_Bidirectionally_and_Verify_it_was_Received(self.tb.config.tgen_ports.netelem1.port_a,
                    self.tb.config.tgen_ports.netelem1.tgen_port_b, self.tb.config.packetA.name, self.tb.config.packetB.name,
                    self.tb.config.packetB.name, self.tb.config.packetA.name, tx_count=10)
        
        self.cliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  "show fdb", ".*aa:aa:aa.*V100.*bb:bb:bb.*V100.*")
        
        self.aaaSuiteUdks.Debug_Dump_UPM_Failure_Info()
        
        self.aaaSuiteUdks.policyUDKs.Disable_Policy_and_Verify_it_is_Disabled(self.tb.config.netelem1.name)
        
        #Disable_Macauth
        self.aaaSuiteUdks.macAuthUdks.Disable_Macauth_and_Verify_it_is_Enabled(self.tb.config.netelem1.name)
    #    disable_macauth_port_and_verify_it_is_enabled
        self.aaaSuiteUdks.macAuthUdks.Disable_Macauth_Port_and_Verify_it_is_Enabled(self.tb.config.netelem1.name,
                                                                        self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.macAuthUdks.Disable_Macauth_Port_and_Verify_it_is_Enabled(self.tb.config.netelem1.name,
                                                                        self.tb.config.netelem1.tgen.port_b.ifname)
    
        self.aaaSuiteUdks.Test_Suite_Cleanup()