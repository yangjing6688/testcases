from pytest import fixture, mark
import time
from Tests.Pytest.NonProduction.AAA.Resources.AAASuiteUdks import AAASuiteUdks
from Tests.Pytest.NonProduction.AAA.Resources.AAABase import AAABase


class AAA_COA_Policy_AuthenticationTests(AAABase):
    
    @mark.F_A000_0501    
    @mark.release_30_4
    @mark.BUILD
    def test_501_AAA_COA_Policy_Profile_Change_Client_and_NasPort(self):       
       self.aaa_coa_policy_authentication(self.tb.config.policyName_b, self.tb.config.vlan_400, self.tb.config.vlan_200, 
                                          "macAuthClient", '65536', "Include All Attributes. Should find session and change session to policy B vlan of 200")
    
    @mark.F_A000_0502    
    @mark.release_30_4
    @mark.BUILD   
    def test_502_AAA_COA_Policy_Profile_Change_Client_No_NasPort(self):       
       self.aaa_coa_policy_authentication(self.tb.config.policyName_b, self.tb.config.vlan_400, self.tb.config.vlan_200, 
                                          "macAuthClient", '0', "Exclude NAS-Port. Should find sesssion and change session to policy B vlan of 200")
    
    @mark.F_A000_0503    
    @mark.release_30_4
    @mark.BUILD
    def test_503_AAA_COA_Policy_Profile_Change_No_Client_No_NasPort(self):       
       self.aaa_coa_policy_authentication(self.tb.config.policyName_a, self.tb.config.vlan_400, self.tb.config.vlan_200, 
                                          "NoAuthClient", '0', "Exclude client and NAS-Port. Should find sesssion and change session to policy B vlan of 200")
    
    
    @mark.F_A000_0504    
    @mark.release_30_4
    @mark.BUILD
    def test_504_AAA_COA_Policy_Profile_Change_No_Client_Bad_NasPort(self):       
       self.aaa_coa_policy_authentication(self.tb.config.policyName_a, self.tb.config.vlan_400, self.tb.config.vlan_100, 
                                          "NoAuthClient", '65536', "Use incorrect NAS PORT. Should result in no change from original vlan of 100")
    
    @mark.F_A000_0505    
    @mark.release_30_4
    @mark.BUILD
    def test_505_AAA_COA_Policy_Profile_Change_Wrong_Client_with_NasPort(self):       
       self.aaa_coa_policy_authentication(self.tb.config.policyName_a, self.tb.config.vlan_400, self.tb.config.vlan_100, 
                                          "dot1xAuthClient", '65536', "Use wrong Client. Should result in no change from original vlan of 100")
        
    @mark.F_A000_0506    
    @mark.release_30_4
    @mark.BUILD
    def test_506_AAA_COA_Policy_Profile_Change_Bad_Policy_Profile_Client_with_NasPort(self):       
       self.aaa_coa_policy_authentication(self.tb.config.policyName_a, self.tb.config.vlan_400, self.tb.config.vlan_500, 
                                          "macAuthClient", '0', "Use Invalid Policy Name. Result should be Vlan 500 (port vlan) due to invalid policy action")
        
    def aaa_coa_policy_authentication(self, coa_policy,  coa_vlan_in, coa_expected_vlan, client_type, if_num_offset, test_description ="Start Test"):
        '''
        [Documentation]  Test Objective: Change of Authentication attributes.''' 
        self.aaaSuiteUdks.create_log_message("Setup test case...")
        self.AAA_COA_Policy_Setup()
              
        self.aaaSuiteUdks.create_log_message("=======================================================================================================")        
        self.aaaSuiteUdks.create_log_message("(Init Interface) compute the COA interface nbr from the slot and port nbr.")       
        self.aaaSuiteUdks.create_log_message("IfIndex = port + slot*0x10000, (0x10000 = 65536) - (port is formatted as port or slot:port)")        
        self.aaaSuiteUdks.create_log_message("Log  =======================================================================================================")
        
        #set defaults
        slotNum = 0
        portNum = 0
        coaIfNum = 0
        if_num_offsetIntValue = 0
        
        #use raw value of port to get slot and port info        
        rawPortString = self.tb.config.netelem1.tgen.port_a.ifname
        
        try:
            if_num_offsetIntValue = int(if_num_offset)
        except:
            if_num_offsetIntValue = 0
        
        if "." in rawPortString:        
            rawPortStringList = rawPortString.splilt(".")
            lengthOfPortStringList = len(rawPortStringList)
            
            if lengthOfPortStringList == 1:
                portNum = rawPortStringList[0]
            if lengthOfPortStringList > 1:
                slotNum = rawPortStringList[0]
                portNum = rawPortStringList[1]
        else:
            portNum = int(rawPortString)
        
        #set coaIfNum
        coaIfNum = portNum + slotNum * int(if_num_offset)
               
        #Clear Syslog        
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)
        
        self.aaaSuiteUdks.create_log_message("(Step 2) COA: Issue a Change of Auth with input attributes and check for desired change.")
        
        if if_num_offset != '0':
            self.aaaSuiteUdks.radiusSuiteUdks.Send_COA_Auth_Request(self.tb.config.netelem1.name, self.tb.config.endsysRadius.name,
                                                                    self.tb.config.netelem1.ip,self.tb.config.packetA.hyphenated_mac,
                                                                    coa_policy,coa_vlan_in,coaIfNum,client_type)  
        if if_num_offset == '0':
            self.aaaSuiteUdks.radiusSuiteUdks.Send_COA_Auth_Request(self.tb.config.netelem1.name, self.tb.config.endsysRadius.name,
                                                                    self.tb.config.netelem1.ip,self.tb.config.packetA.hyphenated_mac,
                                                                    coa_policy,coa_vlan_in,'0',client_type)
       
    #
        
    #  Stacked systems don't seem to program the FDB consistently so we need to send some frames in to kick off the
    #    FDB programming after the COA message is processed.
    #
        #Start Transmit on Port    ${tgen_ports.netelem1.port_a}
        self.aaaSuiteUdks.trafficTransmitKeywords.start_transmit_on_port(self.tb.tgen_dut1_port_a)
        
        #Start Transmit on Port    ${tgen_ports.netelem1.port_b}
        self.aaaSuiteUdks.trafficTransmitKeywords.start_transmit_on_port(self.tb.tgen_dut1_port_b)
            
        #sleep  1
        time.sleep(1)
        #Stop Transmit on Port     ${tgen_ports.netelem1.port_a}
        self.aaaSuiteUdks.trafficTransmitKeywords.stop_transmit_on_port(self.tb.tgen_dut1_port_a)    
        #Stop Transmit on Port     ${tgen_ports.netelem1.port_b}
        self.aaaSuiteUdks.trafficTransmitKeywords.stop_transmit_on_port(self.tb.tgen_dut1_port_b)
        #fdb entry should exist  ${netelem1.name}  ${packetA.src_mac}  ${coaExpectedVlan}  ${netelem1.tgen.port_a.ifname}        
        self.aaaSuiteUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name, self.aaaSuiteUdks.pytestConfigHelper.config.packetA.src_mac, 
                                                                         coa_expected_vlan, self.tb.config.netelem1.tgen.port_a.ifname)
        
        self.aaaSuiteUdks.create_log_message("Cleanup test case...")
        self.AAA_COA_Policy_Cleanup()

    def AAA_COA_Policy_Setup(self):
    
        # These Are the Defaults For this test Suite So no need to set/reset them.
    #    configure netlogin mac username format  none
    #    configure policy global vlan authorization state  ${netelem1.name}  disable
    #    policy set maptable response  ${netelem1.name}  policy
    
        #Log  (Step 1) Clear Netlogin sessions and Send in packets and Auth to base settings: Vlan 100 (Policy100)
        self.aaaSuiteUdks.create_log_message ("(Step 1) Clear Netlogin sessions and Send in packets and Auth to base settings: Vlan 100 (Policy100)")
        #Clear Netlogin Port State  ${netelem1.name}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_b.ifname)
        #Clear Syslog  ${netelem1.name}
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)        
        
        self.aaaSuiteUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.tgen_dut1_port_a, self.tb.tgen_dut1_port_b,
                                                             self.tb.config.packetA.name, self.tb.config.packetB.name)
        
        self.aaaSuiteUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.tgen_dut1_port_a,
                                                                self.tb.tgen_dut1_port_b,
                                                                self.tb.config.packetA.name,
                                                                self.tb.config.packetB.name,
                                                                self.tb.config.packetB.name,
                                                                self.tb.config.packetA.name,
                                                                self.tb.config.packetA.src_mac,
                                                                self.tb.config.packetB.src_mac)
       
        #fdb entry should exist  ${netelem1.name}  ${packetA.src_mac}  ${vlan_100}   ${netelem1.tgen.port_a.ifname}        
        
        self.aaaSuiteUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name, self.tb.config.packetA.src_mac, 
                                                                         self.tb.config.vlan_100, self.tb.config.netelem1.tgen.port_a.ifname)
    
    def AAA_COA_Policy_Cleanup(self):
        # Will Dump Syslogs and Traces on a Test Failure
        self.aaaSuiteUdks.AAA_Common_Failure_Info_Dump()
    
        # These Are the Defaults For this test Suite So no need to set/reset them.
    #    configure netlogin mac username format  none
    #    configure policy global vlan authorization state  ${netelem1.name}  disable
    #    policy set maptable response  ${netelem1.name}  policy
