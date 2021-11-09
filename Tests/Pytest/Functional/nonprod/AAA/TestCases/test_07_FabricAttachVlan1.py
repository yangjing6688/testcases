from pytest import fixture, mark

from Tests.Pytest.Functional.nonprod.AAA.Resources.AAASuiteUdks import AAASuiteUdks
from Tests.Pytest.Functional.nonprod.AAA.Resources.AAABase import AAABase


#AAA Fabric Attach ISID Validation
class AAA_Fabric_Attach_ISID_ValidationTests(AAABase):
        
    @mark.F_A000_0701    
    @mark.release_30_4
    @mark.BUILD
    @mark.FA
    def test_701_AAA_Fabric_Attach_Extreme_VSA(self):       
       self.aaa_fabric_attach_isid_validation('hyphenated', self.tb.config.vlanName_400, 'nsi1', "Check with Extreme NSI ISID mapping to RFC3580 VLAN")
       
    @mark.F_A000_0702    
    @mark.release_30_4
    @mark.BUILD
    @mark.FA
    def test_702_AAA_Fabric_Attach_Avaya_VSA(self):       
       self.aaa_fabric_attach_isid_validation('none', self.tb.config.vlanName_200, 'nsi2', "Check with Nortel Avaya Fabric Attach VLAN ISID Pair")
      
    def aaa_fabric_attach_isid_validation(self, expected_format,  expected_vlan, nsi_val, test_description ="Start Test"):        
       '''[Documentation]  Test Objective: Validate Fabric Attach VNI/ISID pairs are received'''
        
       self.aaaSuiteUdks.create_log_message("Setup test case...")
       self.AAA_Fabric_Attach_ISID_Test_Setup()
    
      # configure netlogin mac username format  ${format}
       self.aaaSuiteUdks.radiusSuiteUdks.configure_netlogin_mac_username_format(self.tb.config.netelem1.name, expected_format)
       
       self.aaaSuiteUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.tgen_dut1_port_a,
                                                            self.tb.tgen_dut1_port_b,
                                                            self.tb.config.packetA.name,
                                                            self.tb.config.packetB.name,
                                                            self.tb.config.packetB.name,
                                                            self.tb.config.packetA.name,
                                                            self.tb.config.packetA.src_mac,
                                                            self.tb.config.packetB.src_mac)
             
        # fdb entry should exist  ${netelem1.name}  ${packetFA1.src_mac}  ${expectedVlan}   ${netelem1.tgen.port_a.ifname}
       self.aaaSuiteUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name, self.tb.config.packetA.src_mac, 
                                                                         expected_vlan, self.tb.config.netelem1.tgen.port_a.ifname)
       
        # entry should exist  ${netelem1.name}  ${packetFA2.src_mac}  ${expectedVlan}   ${netelem1.tgen.port_b.ifname}
       self.aaaSuiteUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name, self.tb.config.packetB.src_mac, 
                                                                         expected_vlan, self.tb.config.netelem1.tgen.port_b.ifname)        
               
         #send cmd verify output regex   ${netelem1.name}  show fabric attach assignments  .*${expectedVlan}.*Dynamic.*${nsiVal}.*Pending  
       self.aaaSuiteUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, "show fabric attach assignments", '.*${' + expected_vlan + '}.*Dynamic.*${' + nsi_val + '}.*Pending')
       
       self.aaaSuiteUdks.create_log_message("Cleanup test case...")
       self.AAA_Fabric_Attach_ISID_Test_Cleanup()
     
    def AAA_Fabric_Attach_ISID_Test_Setup(self):
        #AAA Common Test Case Setup
        self.aaaSuiteUdks.AAA_Common_Test_Case_Setup()
    
    # Set non default vlanAuth and maptable response for each of these tests.
    #   configure netlogin mac username format  none
        #configure policy global vlan authorization state  ${netelem1.name}  enable
        self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_vlanauthorization_state(self.tb.config.netelem1.name, state='enable')
        #policy set maptable response  ${netelem1.name}  tunnel
        self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name, 'tunnel')
        #Log  (Step 1) Clear Netlogin sessions and Send in packets and Auth to base settings: Vlan 100 (Policy100)
        self.aaaSuiteUdks.create_log_message("(Step 1) Clear Netlogin sessions and Send in packets and Auth to base settings: Vlan 100 (Policy100)")
        #Clear Netlogin Port State  ${netelem1.name}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_b.ifname)
        #Clear Syslog  ${netelem1.name}
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)
        
        self.aaaSuiteUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.tgen_dut1_port_a, self.tb.tgen_dut1_port_b,
                                                             self.tb.config.packetA.name, self.tb.config.packetB.name)     
        
    
    def AAA_Fabric_Attach_ISID_Test_Cleanup(self):
        # Will Dump Syslogs and Traces on a Test Failure
        #AAA Common Failure Info Dump
        self.aaaSuiteUdks.AAA_Common_Failure_Info_Dump()
       # Reset entries we set to non-defaults after each test here (ideally if we could just do it
       #   once for each of the tests for all cases in the template it would be nice.
    
    #   configure netlogin mac username format  none
        #configure policy global vlan authorization state  ${netelem1.name}  disable
        self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_vlanauthorization_state(self.tb.config.netelem1.name, state='disable')
        #policy set maptable response  ${netelem1.name}  policy
        self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name, 'policy')