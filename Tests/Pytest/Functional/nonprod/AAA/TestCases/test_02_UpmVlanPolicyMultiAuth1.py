from Tests.Pytest.Functional.nonprod.AAA.Resources.AAASuiteUdks import AAASuiteUdks
from Tests.Pytest.Functional.nonprod.AAA.Resources.AAABase import AAABase
from pytest import fixture,mark

#*** Test Cases ***
#201 UpmVlan MultiAuth
class UpmVlan_MultiAuth_201Tests(AAABase):
    
    @mark.F_A000_0002    
    @mark.NotFinished
    def test_02_01_upm_vlan_multi_auth(self):
    
        """[Documentation]  Test Objective: Verify UPM Vlan for Policy Profile Enabled Vlan"""
        #[Tags]  F-A000-0002  NotFinished
    # Setup here will run the "Test Suite Setup" in the Resources -> SuiteUdks.robot
    #  change this along the lines of "[Setup]  Test Case Setup" if you have a setup specific to a subset of test cases.
       #[Setup]
        #self.aaaSuiteUdks.setup_class()
    #   This library allows us to pause execution with the "pause execution" keyword.
    #    import library dialogs
        #Log  (Step 1) Base Setup Enable Policy, MacAuth and UPM on selected ports.
        self.aaaSuiteUdks.create_log_message('(Step 1) Base Setup Enable Policy, MacAuth and UPM on selected ports.')    
           
        #Pass Execution   Bypassing, this test has not been written.
    
        #Enable Policy and Verify it is Enabled  ${netelem1.name}
        self.aaaSuiteUdks.policyUDKs.Enable_Policy_and_Verify_it_is_Enabled(self.tb.config.netelem1.name)    
        
    #    Enable Macauth and Verify it is Enabled  ${netelem1.name}   -- Currently Broken for EXOS
        #Enable Macauth  ${netelem1.name}
        self.aaaSuiteUdks.macAuthUdks.Enable_Macauth_and_Verify_it_is_Enabled(self.tb.config.netelem1.name)
            
    #    enable macauth port and verify it is enabled  ${netelem1.name}  ${port_a},${port_b} -- Currently Broken for EXOS
        #enable macauth port  ${netelem1.name}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.aaaSuiteUdks.macAuthUdks.Enable_Macauth_Port_and_Verify_it_is_Enabled(self.tb.config.netelem1.name,
                                                                        self.tb.config.netelem1.tgen.port_a.ifname)                                                                        
        self.aaaSuiteUdks.macAuthUdks.Enable_Macauth_Port_and_Verify_it_is_Enabled(self.tb.config.netelem1.name,
                                                                        self.tb.config.netelem1.tgen.port_b.ifname)
                                                                        
    #
    
        #Create Ethernet2 Packet  ${packetA.name}  ${packetA.dst_mac}  ${packetA.src_mac}
        self.aaaSuiteUdks.tgenUdks.Create_Ethernet2_Packet(self.tb.config.packetA.name, 
                                                  self.tb.config.packetA.dst_mac, 
                                                  self.tb.config.packetA.src_mac)
        
        
        #Create Ethernet2 Packet  ${packetB.name}  ${packetB.dst_mac}  ${packetB.src_mac}
        self.aaaSuiteUdks.tgenUdks.Create_Ethernet2_Packet(self.tb.config.packetB.name, 
                                                  self.tb.config.packetB.dst_mac, 
                                                  self.tb.config.packetB.src_mac)
                
        self.aaaSuiteUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(self.tb.tgen_dut1_port_a,self.tb.tgen_dut1_port_b,
                                                        self.tb.config.packetA.name,self.tb.config.packetB.name)       
    
        #disable macauth  ${netelem1.name}
        self.aaaSuiteUdks.macAuthUdks.Disable_Macauth_and_Verify_it_is_Disabled(self.tb.config.netelem1.name)
        
        #disable macauth port  ${netelem1.name}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.aaaSuiteUdks.macAuthUdks.Disable_Macauth_Port_and_Verify_it_is_Disabled(self.tb.config.netelem1.name,
                                                self.tb.config.netelem1.tgen.port_a.ifname)
        self.aaaSuiteUdks.macAuthUdks.Disable_Macauth_Port_and_Verify_it_is_Disabled(self.tb.config.netelem1.name,
                                                self.tb.config.netelem1.tgen.port_b.ifname)
        
        #disable policy and verify it is disabled  ${netelem1.name}
        self.aaaSuiteUdks.policyUDKs.Disable_Policy_and_Verify_it_is_Disabled(self.tb.config.netelem1.name)
    
       #[Teardown]  #<Cleanup Keyword>
        #self.aaaSuiteUdks.teardown_class()


#*** Keywords ***
# This section is used to create a user-defined keyword to clean up configuration made by this test case.
#<Cleanup User-Defined Keyword Name>
    #<Keywords>