from Tests.Pytest.Functional.nonprod.AAA.Resources.AAASuiteUdks import AAASuiteUdks
from Tests.Pytest.Functional.nonprod.AAA.Resources.AAABase import AAABase
from pytest import fixture, mark
from time import sleep

#*** Keywords ***
class AAA_UPM_Vlan_AuthenticationTests(AAABase):
    """Test Objective: Verify UPM Vlan for Policy Profile Enabled Vlan"""
     
    @mark.F_A000_0101
    @mark.release_30_4
    @mark.BUILD
    def test_101_UpmVlan_Verify_UPM_with_VLAN_ID(self): 
       self.upm_vlan_policy_vid_method(self.tb.config.packetA, self.tb.config.packetB,'Verify UPM Vlan for Policy Profile Enabled Vlan Using VLAN ID')
       
    @mark.F_A000_0102
    @mark.release_30_4
    @mark.BUILD
    def test_102_UpmVlan_Verify_UPM_with_VLAN_STRING(self):
        self.upm_vlan_policy_vid_method(self.tb.config.packetC, self.tb.config.packetD,'Verify UPM Vlan for Policy Profile Enabled Vlan Using VLAN String')
       
        #${packetC}   ${packetD}
        #Verify UPM Vlan for Policy Profile Enabled Vlan Using VLAN String
       #[Tags]   F-A000-0102  30.5  NIGHTLY


# Setup here will run the "Test Suite Setup" in the Resources -> SuiteUdks.robot
#  change this along the lines of "[Setup]  Test Case Setup" if you have a setup specific to a subset of test cases.
#   [Setup]  AAA UPM VID Test Case Setup
#
#   Auth with mode "policy" (using filterId in RADIUS response)
#   Policy config should auth to port Vlan (V500) since we are going to remove the policy name.
#      in the authed filterID (Policy100)...
#
    def upm_vlan_policy_vid_method(self, packet1, packet2,  TestDescription="Start Test"):
    
        #configure packets        
        self.aaaSuiteUdks.tgenUdks.Create_Ethernet2_Packet(packet1.name, 
                                              packet1.dst_mac, 
                                              packet1.src_mac, 
                                              packet_len=64)
        # Setup Packet Streams    
        self.aaaSuiteUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.tgen_dut1_port_a,
                                                                          self.tb.tgen_dut1_port_b,
                                                                          packet1.name,
                                                                          packet2.name)
        
        self.aaaSuiteUdks.create_log_message("(Step 1a) Remove Policy Profile in Radius Filter ID attribute.")
        
        self.aaaSuiteUdks.policyUDKs.Remove_Policy_Profile_and_Verify_it_was_Removed(self.tb.config.netelem1.name,
                                                                        self.tb.config.policyId_a)
        
        #Clear Netlogin Port States
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_b.ifname)
        
        #Clear Syslog
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)
        
        self.aaaSuiteUdks.create_log_message("Log  (Verification 1) Remove Authed Policy (created during setup) Re-Auth should be to port pvid.")
    
        # Send Packets Verify Received        
        self.aaaSuiteUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.tgen_dut1_port_a,
                                                            self.tb.tgen_dut1_port_b,
                                                            packet1.name,
                                                            packet2.name,
                                                            packet2.name,
                                                            packet1.name,
                                                            packet1.src_mac,
                                                            packet2.src_mac)
    #  Expect VLAN V500 -> 500
       # Verify UPM config is correct  ${vlan_500}  ${vlanName_500}   ${Packet1}  ${Packet2}
        self.aaaSuiteUdks.Verify_UPM_config_is_correct(self.tb.config.vlan_500, self.tb.config.vlanName_500, self.tb.config.packet1, self.tb.config.packet2)
            
        self.aaaSuiteUdks.create_log_message("Log  (Step 2) Bounce ports to clear authed user. Remove Port Vlan")
        
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_b.ifname)
                  
        #Clear Syslog  ${netelem1.name}
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)    
    #   Remove the port VLAN (V500) ... Now there is no policy to auth to or
    #      any other VLAN to assign so NO vlan should be assigned.
    #
        #remove port/s from untagged egress for vlan and verify it is removed  ${netelem1.name}  ${vlan_500}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.aaaSuiteUdks.vlanUDKs.Remove_Ports_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name, self.tb.config.vlan_default, 
                self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.vlanUDKs.Remove_Ports_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name, self.tb.config.vlan_default, 
                self.tb.config.netelem1.tgen.port_b.ifname)     
        
        #Log  (Verification 2) Remove Port Vlan - No VLAN should be able to be determined..
        self.aaaSuiteUdks.create_log_message("Log  (Verification 2) Remove Port Vlan - No VLAN should be able to be determined..")
        
        #verify packets are not recieved
        self.aaaSuiteUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Not_Received(self.tb.config.tgen_ports.netelem1.port_a, self.tb.config.tgen_ports.netelem1.port_b, 
                                                                    packet2.name, packet1.name,
                                                                    packet1.src_mac, packet2.src_mac)   
       
        self.aaaSuiteUdks.Verify_UPM_config_is_correct(self.tb.config.vlan_500, 'unknown', self.tb.config.packet1, self.tb.config.packet2,'none',False)
                
        #Log  (Step 3) Bounce ports to clear authed user. Reconfigure Port Vlan and Policy
        self.aaaSuiteUdks.create_log_message("(Step 3) Bounce ports to clear authed user. Reconfigure Port Vlan and Policy")
        
        #Clear Netlogin Port State  ${netelem1.name}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_b.ifname)
              
        #Clear_Syslog  ${netelem1.name}
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)
         
        self.aaaSuiteUdks.vlanUDKs.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name, self.tb.config.vlan_default, 
                self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.vlanUDKs.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name, self.tb.config.vlan_default, 
                self.tb.config.netelem1.tgen.port_b.ifname)
                
        self.aaaSuiteUdks.policyUDKs.Create_Policy_Profile_With_PVID_and_PVID_Status_Enabled(self.tb.config.netelem1.name, self.tb.config.policyId_a, 
                                                                                                                self.tb.config.vlan_100)
        
        self.aaaSuiteUdks.policyUDKs.Create_Policy_Profile_and_Verify_it_Exists(self.tb.config.netelem1.name, self.tb.config.policyId_a)
     
        self.aaaSuiteUdks.create_log_message("Log  (Verification 3) Auth to the VLAN (100) in the policy profile ID returned in the RADIUS Response.")
                
        self.aaaSuiteUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.tgen_dut1_port_a,
                                                            self.tb.tgen_dut1_port_b,
                                                            packet1.name,
                                                            packet2.name,
                                                            packet2.name,
                                                            packet1.name,
                                                            packet1.src_mac,
                                                            packet2.src_mac)
        self.aaaSuiteUdks.Verify_UPM_config_is_correct(self.tb.config.vlan_100, self.tb.config.vlanName_100, self.tb.config.packet1, self.tb.config.packet2)
            
        #Log  (Step 4) Bounce ports to clear authed user. Enable vlanauth and set maptable response to tunnel.
        self.aaaSuiteUdks.create_log_message(" Log  (Step 4) Bounce ports to clear authed user. Enable vlanauth and set maptable response to tunnel.")
    
        #Clear_Netlogin Port State  ${netelem1.name}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_b.ifname)
       
        #Clear Syslog  ${netelem1.name}
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)
    #
    #   Configure policy to use vlan authorization/RFC3580 vlan in the RADIUS response
    #
        #policy set vlanauthorization state  ${netelem1.name}  enable    
        self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_vlanauthorization_state(self.tb.config.netelem1.name, 'enable')
        
        #policy set maptable response        ${netelem1.name}  tunnel
        self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name, 'tunnel')
    #   set policy maptable response and verify  ${netelem1.name}  tunnel
    
        #Log  (Verification 4) Auth to the VLAN in the RFC 3580 VLAN Id in the RADIUS Response.
        self.aaaSuiteUdks.create_log_message("Log  (Verification 4) Auth to the VLAN in the RFC 3580 VLAN Id in the RADIUS Response.")
           
        
        self.aaaSuiteUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.tgen_dut1_port_a,
                                                            self.tb.tgen_dut1_port_b,
                                                            packet1.name,
                                                            packet2.name,
                                                            packet2.name,
                                                            packet1.name,
                                                            packet1.src_mac,
                                                            packet2.src_mac)
    
        #Verify UPM config is correct  ${vlan_200}  ${vlanName_200}  ${Packet1}  ${Packet2}
        self.aaaSuiteUdks.Verify_UPM_config_is_correct(self.tb.config.vlan_200, self.tb.config.vlanName_200, self.tb.config.packet1, self.tb.config.packet2)
         
        self.aaaSuiteUdks.create_log_message("Log  (Step 5) Switch to a hyphenated mac auth. Bounce ports and configure maptable response to policy")
        #configure netlogin mac username format  hyphenated
        self.aaaSuiteUdks.radiusSuiteUdks.configure_netlogin_mac_username_format( self.tb.config.netelem1.name, 'hyphenated')
    
        #Clear Netlogin Port State  ${netelem1.name}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}        
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Netlogin_Port_State(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_b.ifname)
       
        #Clear Syslog  ${netelem1.name}
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)
    #
    #   Set policy maptable response back to "policy" and disable vlan authorization.
    #
       #policy set_vlanauthorization state  ${netelem1.name}  disable
        self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_vlanauthorization_state(self.tb.config.netelem1.name, 'disable')
            
        #policy set maptable response  ${netelem1.name}  policy
        self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name, 'policy')
    #
        #Log  (Verification 5) Auth to the VLAN in the policy profile ID returned in the RADIUS Response.
        self.aaaSuiteUdks.create_log_message("Log  (Verification 5) Auth to the VLAN in the policy profile ID returned in the RADIUS Response.")
              
        self.aaaSuiteUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(self.tb.tgen_dut1_port_a,
                                                            self.tb.tgen_dut1_port_b,
                                                            packet1.name,
                                                            packet2.name,
                                                            packet2.name,
                                                            packet1.name,
                                                            packet1.src_mac,
                                                            packet2.src_mac)
    #
    #
    #  Expect VLAN 300 -> V300
    #
        #Verify UPM config is correct  ${vlan_300}  ${vlanName_300}  ${Packet1}  ${Packet2}  hyphen        
        self.aaaSuiteUdks.Verify_UPM_config_is_correct(self.tb.config.vlan_300, self.tb.config.vlanName_300, self.tb.config.packet1, self.tb.config.packet2)
        #Clear Syslog  ${netelem1.name}
        self.aaaSuiteUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)
    #
    #  A Re-Auth (no port link bounce) to a new VLAN should be reported from Policy to Netlogin.
    #
        #Log  (Step 6) configure vlan authorization and set the response to tunnel. Then sleep and wait for a re-auth.
        self.aaaSuiteUdks.create_log_message("Log  (Step 6) configure vlan authorization and set the response to tunnel. Then sleep and wait for a re-auth.")
       
        #policy set vlanauthorization state  ${netelem1.name}  enable
        self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_vlanauthorization_state(self.tb.config.netelem1.name, 'enable')
        
        #policy set maptable response  ${netelem1.name}  tunnel
        self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name, 'tunnel')
       
    #   Wait 30 sec for a re-auth to the tunnel VLAN
        #Log  (Verification 6) Auth to the VLAN in the policy profile ID returned in the RADIUS Response.
        self.aaaSuiteUdks.create_log_message("Log  (Verification 6) Auth to the VLAN in the policy profile ID returned in the RADIUS Response.")
       
        ##Sleep  ${policy_reauth_timer}  # Delay to allow for a reauth to take place
        sleep(int(self.tb.config.policy_reauth_timer))
    #
    #  Expect VLAN 400 -> V400
    #
    #  -- here don't check for the FDB entry, in stacked systems sometimes the FDB
    #  --  entry does not get programmed on the backup system due to a timing issue with vlan manager
    #  --  we are not sending traffic in for this test, if we did the FDB would get programmed.
    #    Verify UPM config is correct  ${vlan_400}  ${vlanName_400}    ${Packet1}  ${Packet2}  hyphen
        #Verify Syslog ClientAuthenticated Message Vlan  ${vlanName_400}  ${Packet1}  ${Packet2}  hyphen    
        #self.aaaSuiteUdks.Verify_Syslog_ClientAuthenticated_Message_Vlan(vid_name, packet1, packet2, mac_address_separator)
        self.aaaSuiteUdks.Verify_Syslog_ClientAuthenticated_Message_Vlan(self.tb.config.vlanName_400, self.tb.config.packet1, self.tb.config.packet2)
    #

def AAA_UPM_VID_Test_Case_Setup(self):
    self.aaaSuiteUdks.AAA_Common_Test_Case_Setup()

#    Enable UPM VLAN FEATURE
def Enable_UPM_VLAN_FEATURE(self):
  #Configure_UPM_Vlan Script macAuthenticate
  self.aaaSuiteUdks.Configure_UPM_Vlan_Script_macAuthenticate()
  #Configure UPM Vlan Script macUnAuthenticate
  self.aaaSuiteUdks.Configure_UPM_Vlan_Script_macUnAuthenticate()
  #enable UPM macAuthenticate and macUnauthenticate
  self.aaaSuiteUdks.enable_UPM_macAuthenticate_and_macUnauthenticate()


# This section is used to create a user-defined keyword to clean up configuration made by this test case.
def AAA_UPM_VLAN_Test_Case_Cleanup(self):
    #AAA Common Failure Info Dump
    self.aaaSuiteUdks.AAA_Common_Failure_Info_Dump()
    #AAA UPM Failure Info Dump
    self.aaaSuiteUdks.AAA_UPM_Failure_Info_Dump()

#  Put these back in case the test fails above when they were removed...
    #Add Port/s to Untagged Egress for VLAN and Verify it is Added  ${netelem1.name}  ${vlan_500}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}    
    self.aaaSuiteUdks.vlanUDKs.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name, self.tb.config.vlan_default, 
                self.tb.config.netelem1.tgen.port_a.ifname)
    self.aaaSuiteUdks.vlanUDKs.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.config.netelem1.name, self.tb.config.vlan_default, 
                self.tb.config.netelem1.tgen.port_b.ifname)   
    #Create Policy Profile With PVID and PVID Status Enabled  ${netelem1.name}  ${policyId_a}  ${vlan_100}
    self.aaaSuiteUdks.policyUDKs.Create_Policy_Profile_With_PVID_and_PVID_Status_Enabled(self.tb.config.netelem1.name, self.tb.config.policyId_a, 
                                                                                                                self.tb.config.vlan_100)
        
    #Create Policy Profile with Name and Verify it Exists  ${netelem1.name}  ${policyId_a}  ${policyName_a}
    self.aaaSuiteUdks.policyUDKs.Create_Policy_Profile_with_Name_and_Verify_it_Exists(self.tb.config.netelem1.name,self.tb.config.policyId_a, 
                                                                         self.tb.config.policyName_a)
#
    #configure netlogin mac username format  none
    self.aaaSuiteUdks.radiusSuiteUdk.configure_netlogin_mac_username_format( self.tb.config.tgen_ports.netelem1, 'none')
    
    #policy set vlanauthorization state  ${netelem1.name}  disable
    self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_vlanauthorization_state(self.tb.config.netelem1.name, 'disable')
       
    #policy set maptable response  ${netelem1.name}  policy
    self.aaaSuiteUdks.networkElementPolicyGenKeywords.policy_set_maptable_response(self.tb.config.netelem1.name, 'policy')
#   

#    Disable UPM VLAN FEATURE
    #disable UPM macAuthenticate and macUnauthenticate
    self.aaaSuiteUdks.disable_UPM_macAuthenticate_and_macUnauthenticate()
    #upm clear profile  ${netelem1.name}  macAuthenticate
    self.aaaSuiteUdks.policy.remove_policy_profile(self.tb.config.netelem1.name, 'macAuthenticate')
    
       