from ExtremeAutomation.Apis.NetworkElement.GeneratedApis.CommandApis.Constants.PolicyConstants import \
    PolicyConstants as CommandConstants
from ExtremeAutomation.Apis.NetworkElement.GeneratedApis.ParseApis.Constants.PolicyConstants import \
    PolicyConstants as ParseConstants
from ExtremeAutomation.Keywords.BaseClasses.NetworkElementKeywordBaseClass import NetworkElementKeywordBaseClass
from ExtremeAutomation.Library.Utils.ListUtils import ListUtils
from ExtremeAutomation.Library.Utils.StringUtils import StringUtils
from ast import literal_eval
from pytest import fixture, mark
import time
from Tests.Pytest.NonProduction.AAA.Resources.AAABase import AAABase

class AAA_COA_RF3580_Vlan_AuthenticationTests(AAABase):
      
    @mark.F_A000_0601    
    @mark.release_30_4
    @mark.BUILD
    def test_601_AAA_COA_RFC3580_Vlan_Change_VlanId_Client_and_NasPort(self):       
       self.aaa_coa_rf3580_vlan_authenticationTests(self.tb.config.policyName_b, self.tb.config.vlan_400, self.tb.config.vlan_400,    
                                          "macAuthClient", '65536', "Include All Attributes. Should find session and change session to RFC3580 vlan 400")
            
    @mark.F_A000_0602    
    @mark.release_30_4
    @mark.BUILD
    def test_602_AAA_COA_RFC3580_Vlan_Change_VlanId_Client_No_NasPort(self):       
       self.aaa_coa_rf3580_vlan_authenticationTests(self.tb.config.policyName_b, self.tb.config.vlan_400, self.tb.config.vlan_400, 
                                          "macAuthClient", '0', "Exclude NAS-Port. Should find sesssion and change session to to RFC3580 vlan 400")
    
    @mark.F_A000_0603    
    @mark.release_30_4
    @mark.BUILD
    def test_603_AAA_COA_RFC3580_Vlan_Change_VlanId_No_Client_No_NasPort(self):       
       self.aaa_coa_rf3580_vlan_authenticationTests(self.tb.config.policyName_b, self.tb.config.vlan_400, self.tb.config.vlan_400, 
                                          "NoAuthClient", '0', "Exclude client and NAS-Port. Should find sesssion and change session to RFC3580 vlan 400")
       
    @mark.F_A000_0604    
    @mark.release_30_4
    @mark.BUILD
    def test_604_AAA_COA_RFC3580_Vlan_Change_VlanId_No_Client_Bad_NasPort(self):       
       self.aaa_coa_rf3580_vlan_authenticationTests(self.tb.config.policyName_b, self.tb.config.vlan_400, self.tb.config.vlan_200, 
                                          "NoAuthClient", '65536', "Use incorrect NAS PORT. Should result in no change from original vlan of 200")
    
    @mark.F_A000_0605    
    @mark.release_30_4
    @mark.BUILD
    def test_605_AAA_COA_RFC3580_Vlan_Change_VlanId_Wrong_Client_with_NasPort(self):       
       self.aaa_coa_rf3580_vlan_authenticationTests(self.tb.config.policyName_b, self.tb.config.vlan_400, self.tb.config.vlan_200, 
                                          "dot1xAuthClient", '65536', "Use wrong Client. Should result in no change from original vlan of 200")
       
    @mark.F_A000_0606    
    @mark.release_30_4
    @mark.BUILD
    def test_606_AAA_COA_RFC3580_Vlan_Change_VlanId_Bad_Policy_Profile_Client_with_NasPort(self):       
       self.aaa_coa_rf3580_vlan_authenticationTests(self.tb.config.policyName_b, self.tb.config.vlan_400, self.tb.config.vlan_400, 
                                          "macAuthClient", '0', "Use Invalid Policy Name. Result should be Vlan 400 as policy name should not be used when maptable is set to Tunnel")
        
    @mark.F_A000_0651    
    @mark.release_30_5
    @mark.BUILD
    def test_651_AAA_COA_RFC3580_Vlan_Change_VlanId_Client_and_NasPort(self):       
       self.aaa_coa_rf3580_vlan_authenticationTests(self.tb.config.policyName_b, self.tb.config.vlanName_400, self.tb.config.vlan_400, 
                                          "macAuthClient", '65536', "Include All Attributes. Should find session and change session to RFC3580 vlan 400")
       
    @mark.F_A000_0652    
    @mark.release_30_5
    @mark.BUILD
    def test_652_AAA_COA_RFC3580_Vlan_Change_VlanId_Client_No_NasPort(self):       
       self.aaa_coa_rf3580_vlan_authenticationTests(self.tb.config.policyName_b, self.tb.config.vlanName_400, self.tb.config.vlan_400, 
                                          "macAuthClient", '0', "Exclude NAS-Port. Should find sesssion and change session to to RFC3580 vlan 400")
    
    @mark.F_A000_0653    
    @mark.release_30_5
    @mark.BUILD
    def test_653_AAA_COA_RFC3580_Vlan_Change_VlanId_No_Client_No_NasPort(self):       
       self.aaa_coa_rf3580_vlan_authenticationTests(self.tb.config.policyName_b, self.tb.config.vlanName_400, self.tb.config.vlan_400, 
                                          "NoAuthClient", '0', "Exclude client and NAS-Port. Should find sesssion and change session to RFC3580 vlan 400")
       
    @mark.F_A000_0654    
    @mark.release_30_5
    @mark.BUILD
    def test_654_AAA_COA_RFC3580_Vlan_Change_VlanId_No_Client_Bad_NasPort(self):       
       self.aaa_coa_rf3580_vlan_authenticationTests(self.tb.config.policyName_b, self.tb.config.vlanName_400, self.tb.config.vlan_200, 
                                          "NoAuthClient", 'BadNasPort', "Use incorrect NAS PORT. Should result in no change from original vlan of 200")
    
    @mark.F_A000_0655    
    @mark.release_30_5
    @mark.BUILD
    def test_655_AAA_COA_RFC3580_Vlan_Change_VlanId_Wrong_Client_with_NasPort(self):       
       self.aaa_coa_rf3580_vlan_authenticationTests(self.tb.config.policyName_b, self.tb.config.vlanName_400, self.tb.config.vlan_200, 
                                          "dot1xAuthClient", '65536', "Use wrong Client. Should result in no change from original vlan of 200")
       
    @mark.F_A000_0656    
    @mark.release_30_5
    @mark.BUILD
    def test_656_AAA_COA_RFC3580_Vlan_Change_VlanId_Bad_Policy_Profile_Client_with_NasPort(self):       
       self.aaa_coa_rf3580_vlan_authenticationTests(self.tb.config.policyName_b, self.tb.config.vlanName_400, self.tb.config.vlan_400, 
                                          "macAuthClient", '0', "Use Invalid Policy Name. Result should be Vlan 400 as policy name should not be used when maptable is set to Tunnel")
        
    def aaa_coa_rf3580_vlan_authenticationTests(self, coa_policy,  coa_vlan_in, coa_expected_vlan, client_type, if_num_offset, test_description ="Start Test"):
        '''[Documentation]  Test Objective: Change of Authentication attributes.'''
        self.aaaSuiteUdks.create_log_message("Setup test case...")
        self.AAA_COA_RFC3580_Vlan_Setup()
              
        self.aaaSuiteUdks.create_log_message("=======================================================================================================")        
        self.aaaSuiteUdks.create_log_message("(Init Interface) compute the COA interface nbr from the slot and port nbr.")    
        #log  IfIndex = port + slot*0x10000, (0x10000 = 65536) - (port is formatted as port or slot:port)        
        self.aaaSuiteUdks.create_log_message("=======================================================================================================") 
        
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
        coaIfNum = portNum + slotNum * if_num_offsetIntValue
                      
        #Clear Syslog  ${netelem1.name}
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)
        #Log  (Step 2) COA: Issue a Change of Auth with input attributes and check for desired change.
        self.aaaSuiteUdks.create_log_message("(Step 2) COA: Issue a Change of Auth with input attributes and check for desired change.")
       
        #def Send_COA_Auth_Request(self, device_name, EndSysName, Ip, HyphenatedMac):
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
        #Start Transmit on Port     ${tgen_ports.netelem1.port_a}
        self.aaaSuiteUdks.trafficTransmitKeywords.start_transmit_on_port(self.tb.tgen_dut1_port_a)    
        #Start Transmit on Port     ${tgen_ports.netelem1.port_b}
        self.aaaSuiteUdks.trafficTransmitKeywords.start_transmit_on_port(self.tb.tgen_dut1_port_b)
        #sleep  1
        time.sleep(1)
        #Stop Transmit on Port     ${tgen_ports.netelem1.port_a}
        self.aaaSuiteUdks.trafficTransmitKeywords.stop_transmit_on_port(self.tb.tgen_dut1_port_a)
        #Stop Transmit on Port     ${tgen_ports.netelem1.port_b}
        self.aaaSuiteUdks.trafficTransmitKeywords.stop_transmit_on_port(self.tb.tgen_dut1_port_b)
    
        #fdb entry should exist  ${netelem1.name}  ${packetA.src_mac}  ${coaExpectedVlan}  ${netelem1.tgen.port_a.ifname}  wait_for=True  max_wait=5
        self.aaaSuiteUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name, self.tb.config.packetA.src_mac, 
                                                                         coa_expected_vlan, self.tb.config.netelem1.tgen.port_a.ifname)
        
        self.aaaSuiteUdks.create_log_message("Cleanup test case...")
        self.AAA_COA_RFC3580_Vlan_Cleanup()
    
    def AAA_COA_RFC3580_Vlan_Setup(self):
        self.aaaSuiteUdks.AAA_Common_Test_Case_Setup()
    
       # Set non default vlanAuth and maptable response for each of these tests.
    #   configure netlogin mac username format  none
        #configure policy global vlan authorization state  ${netelem1.name}  enable
        self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_vlanauthorization_state(self.tb.config.netelem1.name, state='enable')   
        #policy set maptable response  ${netelem1.name}  tunnel
        self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name, 'tunnel')
        #Log  (Step 1) Clear Netlogin sessions and Send in packets and Auth to base settings: Vlan 100 (Policy100)
        self.aaaSuiteUdks.create_log_message("Log  (Verification 1) Remove Authed Policy (created during setup) Re-Auth should be to port pvid.")
        #Clear Netlogin Port State  ${netelem1.name}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}    
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_b.ifname)
        #Clear Syslog  ${netelem1.name}
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)
        #configure packets        
        self.aaaSuiteUdks.tgenUdks.Create_Ethernet2_Packet(self.tb.config.packetA.name, 
                                              self.tb.config.packetA.dst_mac, 
                                              self.tb.config.packetA.src_mac, 
                                              packet_len=64)
        self.aaaSuiteUdks.tgenUdks.Create_Ethernet2_Packet(self.tb.config.packetB.name, 
                                              self.tb.config.packetB.dst_mac, 
                                              self.tb.config.packetB.src_mac, 
                                              packet_len=64)
        #setup packets         
        self.aaaSuiteUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.tgen_dut1_port_a,
                                                                          self.tb.tgen_dut1_port_b,
                                                                          self.tb.config.packetA.name,
                                                                          self.tb.config.packetB.name) 
                   
        self.aaaSuiteUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.tgen_dut1_port_a,
                                                                self.tb.tgen_dut1_port_b,
                                                                self.tb.config.packetA.name,
                                                                self.tb.config.packetB.name,
                                                                self.tb.config.packetB.name,
                                                                self.tb.config.packetA.name,
                                                                self.tb.config.packetA.src_mac,
                                                                self.tb.config.packetB.src_mac)
        
        #fdb entry should exist  ${netelem1.name}  ${packetA.src_mac}  ${vlan_200}   ${netelem1.tgen.port_a.ifname}    wait_for=True  max_wait=5    
        self.aaaSuiteUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name, self.tb.config.packetA.src_mac, 
                                                                         self.tb.config.vlan_200, self.tb.config.netelem1.tgen.port_a.ifname)
    
    def AAA_COA_RFC3580_Vlan_Cleanup(self):
        # Will Dump Syslogs and Traces on a Test Failure
        self.aaaSuiteUdks.AAA_Common_Failure_Info_Dump()
       # Reset entries we set to non-defaults after each test here (ideally if we could just do it
       #   once for each of the tests for all cases in the template it would be nice.
    #   configure netlogin mac username format  none
        #configure policy global vlan authorization state  ${netelem1.name}  disable
        self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_vlanauthorization_state(self.tb.config.netelem1.name, state='disable')    
        #policy set maptable response  ${netelem1.name}  policy    
        self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name, 'policy')