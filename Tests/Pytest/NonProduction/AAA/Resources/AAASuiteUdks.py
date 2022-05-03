from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementCliSend import NetworkElementCliSend
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from Tests.Pytest.NonProduction.Resources.RadiusSuiteUdks import RadiusSuiteUdks
from Tests.Pytest.NonProduction.Resources.PolicySuiteUdks import PolicySuiteUdks
from Tests.Pytest.NonProduction.Resources.PlatformGenericSuiteUdks import PlatformGenericSuiteUdks
from ExtremeAutomation.Keywords.EndsystemKeywords.EndsystemConnectionManager import EndsystemConnectionManager
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementPortGenKeywords import NetworkElementPortGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementVlanGenKeywords import NetworkElementVlanGenKeywords
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.Security.PolicyUdks import PolicyUdks
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementMacauthGenKeywords import NetworkElementMacauthGenKeywords
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.Security.MacAuthUdks import MacAuthUdks
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.L2.VlanUdks import VlanUdks
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.SetupTeardown.SetupTeardownUdks import SetupTeardownUdks
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementLoggingGenKeywords import NetworkElementLoggingGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementFdbGenKeywords import NetworkElementFdbGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementIpsecurityGenKeywords import NetworkElementIpsecurityGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementUpmGenKeywords import NetworkElementUpmGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementPolicyGenKeywords import NetworkElementPolicyGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementLoginconfigGenKeywords import NetworkElementLoginconfigGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.StaticKeywords.NetworkElementHostUtilsKeywords import NetworkElementHostUtilsKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementConnectionVerification import NetworkElementConnectionVerification
from ExtremeAutomation.Keywords.TrafficKeywords.TrafficTransmitKeywords import TrafficTransmitKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementListUtils import NetworkElementListUtils
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementVlanGenKeywords import NetworkElementVlanGenKeywords
from Tests.Pytest.NonProduction.Resources.TrafficSuiteUdks import TrafficGenerationSuiteUdks
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.Security.RadiusUdks import RadiusUdks

class AAASuiteUdks():
    
    def __init__(self, pytestConfigHelper):
        self.pytestConfigHelper = pytestConfigHelper        
        self.defaultLibrary = DefaultLibrary()
        self.networkElementCliSend = NetworkElementCliSend()
        self.radiusSuiteUdks = RadiusSuiteUdks()
        self.endsystemConnectionMan = EndsystemConnectionManager()
        self.tgenUdks = self.defaultLibrary.apiUdks.trafficGenerationUdks
        self.networkElementPortGenKeywords = NetworkElementPortGenKeywords()        
        self.networkElementVlanGenKeywords = NetworkElementVlanGenKeywords()
        self.policyUDKs = PolicyUdks()
        self.networkElementMacAuth = NetworkElementMacauthGenKeywords()
        self.macAuthUdks = MacAuthUdks()
        self.vlanUDKs =  VlanUdks()
        self.policySuiteUdks =   PolicySuiteUdks()
        self.setupTeardownUdks =  SetupTeardownUdks()
        self.networkElementLoggingGenKeywords =NetworkElementLoggingGenKeywords()
        self.networkElementFdbGenKeywords = NetworkElementFdbGenKeywords()
        self.networkElementIpsecurityGenKeywords = NetworkElementIpsecurityGenKeywords()
        self.networkElementUpmGenKeywords = NetworkElementUpmGenKeywords()
        self.networkElementPolicyGenKeywords = NetworkElementPolicyGenKeywords()
        self.networkElementLoginconfigGenKeywords = NetworkElementLoginconfigGenKeywords()
        self.networkElementHostUtilsKeywords = NetworkElementHostUtilsKeywords()
        self.networkElementConnectionVerification = NetworkElementConnectionVerification()
        self.trafficTransmitKeywords = TrafficTransmitKeywords()
        self.vlan = NetworkElementVlanGenKeywords()
        self.trafficGenerationSuiteUdks = TrafficGenerationSuiteUdks()
        self.tgenUdks = self.defaultLibrary.apiUdks.trafficGenerationUdks
        self.radiusUdks =   RadiusUdks()
             
    #This Is A Suite User-Defined Keyword
    #    This is a low level keyword        ${a variable}
    #    This is another low level keyword  ${another variable}
    def Dump_AAA_Diagnostics(self):
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'disable clipaging')
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'show config')
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'show log \| exclude ConvEndPoint')
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'debug ems show trace aaa all')
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'debug ems show trace policy all')
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'debug ems show trace netlogin all')

    def Clear_AAA_Diagnostics(self):
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'clear log static')        
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'debug ems clear trace aaa all')
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'debug ems clear trace policy all')
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'debug ems clear trace netlogin all')
        
    def AAA_Common_Test_Case_Setup(self):
        self.Clear_AAA_Diagnostics()
    
    def AAA_Common_Failure_Info_Dump(self, shouldDump=False):
        if shouldDump:
            self.Dump_AAA_Diagnostics()       
    
    def AAA_UPM_Failure_Info_Dump(self, testFailed=False):
        if testFailed:
            self.Dump_AAA_Diagnostics()
        #note used Dump_AAA_Diagnostics() did not set a Debug Dump UPM Failure Info method
        #Run Keyword If Test Failed  Debug Dump UPM Failure Info
            
    def Initialize_AAA_EMS_Config(self):
        # NOTE: If debug mode is not enabled on the device, the following "jerry" command not execute.
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'jerry aaa set debuglevel 10  ignore_cli_feedback=true')
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'enable log debug-mode')
        #  - can't use this easily as the "default" logs can at times contain the word "Error" which makes the
        #    system think there was an error in the test
        #    send cmd   ${netelem1.name}  configure log filter DefaultFilter add events Nl severity debug-data  ignore_cli_feedback=TRUE
        #    send cmd   ${netelem1.name}  configure log filter DefaultFilter add events Policy severity debug-data  ignore_cli_feedback=TRUE
        #    send cmd   ${netelem1.name}  configure log filter DefaultFilter add events AAA severity debug-data  ignore_cli_feedback=TRUE
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'configure log target memory-buffer number-of-messages 20000')
        
    def Clear_AAA_EMS_Config(self):
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'disable log debug-mode')
        
        #    send cmd   ${netelem1.name}  configure log filter DefaultFilter delete events Policy severity debug-data  ignore_cli_feedback=TRUE
        #    send cmd   ${netelem1.name}  configure log filter DefaultFilter delete events Nl severity debug-data  ignore_cli_feedback=TRUE
                          
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'configure log filter DefaultFilter delete events AAA severity debug-data  ignore_cli_feedback=TRUE')
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'configure log target memory-buffer number-of-messages 1000   wait_for_prompt=${FALSE}')
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, ' y                   check_initial_prompt=${FALSE}')
    
    def Test_Suite_Setup(self):
        #  "Base Test Suite Setup" must come first... It initializes stuff we don't need to know about.
        
        
        #Base_Test_Suite_Setup()
        self.setupTeardownUdks.Base_Test_Suite_Setup()
        # Run Keyword If  "${netelem1.upgrade_firmware}" == "True"  Upgrade Netelem to Latest Firmware  ${netelem1.name}  ${tftp_server.ip}  ${netelem1.build_directory}  ${netelem1.build}  ${netelem1.mgmt_vlan}  ${netelem1.ip}
#
        # Initialize AAA EMS Config
        # AaaLogin Validation seems to lose this setting somehow (at least on the 30.7 branch)
        #  After a failure the log/trace dumps were paginating until I explicitly put in another disable clipaging command in.
    
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'disable clipaging')
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'show config')
       
        # Configure the RADIUS servers and connect to the server to send COA frames.
        #     ${netelem1.mgmt_vlan} is actually the MGMT VR that is used to communicate to the device.
        #          it can be VR-MGMT (common) or VR-Default (not as common), The RADIUS server should use the same VR.
        #   
        
        radius_server = self.pytestConfigHelper.config.endsysRadius.name
        radius_instance = self.pytestConfigHelper.config.endsysRadius.instance
        radius_ip_address = self.pytestConfigHelper.config.endsysRadius.ip
        radius_port = self.pytestConfigHelper.config.endsysRadius.port
        radius_secret = self.pytestConfigHelper.config.endsysRadius.shared_secret
        radius_vr = "VR-Mgmt"
        radius_username = self.pytestConfigHelper.config.endsysRadius.username
        radius_password = self.pytestConfigHelper.config.endsysRadius.password
        radius_connection_method = self.pytestConfigHelper.config.endsysRadius.connection_method
        radius_os = self.pytestConfigHelper.config.endsysRadius.os        
                
        #self.radiusSuiteUdks.Configure_And_Enable_Radius_Netlogin_Server( self.pytestConfigHelper.dut1.name, radius_instance, radius_ip_address, radius_port , radius_secret,  self.pytestConfigHelper.dut1.ip,radius_vr)
                
        #self.radiusSuiteUdks.Configure_And_Enable_Radius_DynAuth_Server( self.pytestConfigHelper.dut1.name, radius_instance, radius_server, radius_secret, radius_ip_address, radius_vr)
                  
        #self.endsystemConnectionMan.connect_to_endsystem_element( radius_server, radius_ip_address, radius_username, radius_password,radius_connection_method,  radius_os)

        #  Create A packets to use for the various tests.

        #Create Ethernet2 Packet  ${packetA.name}  ${packetA.dst_mac}  ${packetA.src_mac}
        self.tgenUdks.Create_Ethernet2_Packet(self.pytestConfigHelper.config.packetA.name, 
                                                  self.pytestConfigHelper.config.packetA.dst_mac, 
                                                  self.pytestConfigHelper.config.packetA.src_mac)        
        #Create Ethernet2 Packet  ${packetB.name}  ${packetB.dst_mac}  ${packetB.src_mac}
        self.tgenUdks.Create_Ethernet2_Packet(self.pytestConfigHelper.config.packetB.name, 
                                                  self.pytestConfigHelper.config.packetB.dst_mac, 
                                                  self.pytestConfigHelper.config.packetB.src_mac)
        #Create Ethernet2 Packet  ${PacketC.name}  ${PacketC.dst_mac}  ${PacketC.src_mac}
        self.tgenUdks.Create_Ethernet2_Packet(self.pytestConfigHelper.config.packetC.name, 
                                                  self.pytestConfigHelper.config.packetC.dst_mac, 
                                                  self.pytestConfigHelper.config.packetC.src_mac)    
        #Create Ethernet2 Packet  ${PacketD.name}  ${PacketD.dst_mac}  ${PacketD.src_mac}
        self.tgenUdks.Create_Ethernet2_Packet(self.pytestConfigHelper.config.packetD.name, 
                                                  self.pytestConfigHelper.config.packetD.dst_mac, 
                                                  self.pytestConfigHelper.config.packetD.src_mac)
        #Create Ethernet2 Packet  ${PacketFA1.name}  ${PacketFA1.dst_mac}  ${PacketFA1.src_mac}
        self.tgenUdks.Create_Ethernet2_Packet(self.pytestConfigHelper.config.packetFA1.name, 
                                                  self.pytestConfigHelper.config.packetFA1.dst_mac, 
                                                  self.pytestConfigHelper.config.packetFA1.src_mac)
        #Create Ethernet2 Packet  ${PacketFA2.name}  ${PacketFA2.dst_mac}  ${PacketFA2.src_mac}
        self.tgenUdks.Create_Ethernet2_Packet(self.pytestConfigHelper.config.packetFA2.name, 
                                                  self.pytestConfigHelper.config.packetFA2.dst_mac, 
                                                  self.pytestConfigHelper.config.packetFA2.src_mac)
        #  Netlogin Config
        #configure port enable  ${netelem1.name}    ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}        
        self.networkElementPortGenKeywords.port_enable_state(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)    
        
        # Enable Policy and Verify it is Enabled  ${netelem1.name}              
        self.policyUDKs.Enable_Policy_and_Verify_it_is_Enabled(self.pytestConfigHelper.dut1.name)
            
        # macauth enable  ${netelem1.name}    
        self.networkElementMacAuth.macauth_enable(self.pytestConfigHelper.dut1.name)
        
        #enable macauth port  ${netelem1.name}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.macAuthUdks.Enable_Macauth_Port_and_Verify_it_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.macAuthUdks.Enable_Macauth_Port_and_Verify_it_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
            
        #send cmd  ${netelem1.name}  configure netlogin add mac-list ff:ff:ff:ff:ff:ff 48
        #send cmd  ${netelem1.name}  configure netlogin mac username format none
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'configure netlogin add mac-list ff:ff:ff:ff:ff:ff 48')
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'configure netlogin mac username format none')

        #  VLAN config
        #Create VLAN with Name and Verify it Exists  ${netelem1.name}  ${vlanName_100}  ${vlan_100}
        #Create VLAN with Name and Verify it Exists  ${netelem1.name}  ${vlanName_200}  ${vlan_200}
        #Create VLAN with Name and Verify it Exists  ${netelem1.name}  ${vlanName_300}  ${vlan_300}
        #Create VLAN with Name and Verify it Exists  ${netelem1.name}  ${vlanName_400}  ${vlan_400}
        #Create VLAN with Name and Verify it Exists  ${netelem1.name}  ${vlanName_500}  ${vlan_500}
                
        self.vlanUDKs.Create_VLAN_with_Name_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlanName_100,self.pytestConfigHelper.config.vlan_100)
        self.vlanUDKs.Create_VLAN_with_Name_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlanName_200,self.pytestConfigHelper.config.vlan_200)
        self.vlanUDKs.Create_VLAN_with_Name_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlanName_300,self.pytestConfigHelper.config.vlan_300)
        self.vlanUDKs.Create_VLAN_with_Name_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlanName_400,self.pytestConfigHelper.config.vlan_400)
        self.vlanUDKs.Create_VLAN_with_Name_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlanName_500,self.pytestConfigHelper.config.vlan_500)
       
        #  Deafault port VLAN Assignment.
        #Remove Port/s from Untagged Egress for VLAN and Verify it is Removed  ${netelem1.name}  ${Vlan_Default}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.vlanUDKs.Remove_Ports_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_default, 
            self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.vlanUDKs.Remove_Ports_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_default, 
            self.pytestConfigHelper.dut1_tgen_port_b.ifname)
              
        #Add Port/s to Untagged Egress for VLAN and Verify it is Added  ${netelem1.name}  ${vlan_500}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.vlanUDKs.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_default, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.vlanUDKs.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_default, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        
    def Cleanup_DUT(self):
        print("Cleaning up DUT " + self.pytestConfigHelper.dut1.name)
        self.vlanUDKs.Remove_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_100)
        self.vlanUDKs.Remove_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_200)
        self.vlanUDKs.Remove_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_300)
        self.vlanUDKs.Remove_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_400)
        self.vlanUDKs.Remove_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_500)
       
    #  Standard Policy Profile Configuration
    #Basic Policy Setup
    def Test_Suite_Cleanup(self):
        #    Log  (Cleanup Step 1) Test Cleanup Unconfigure stuff we configured earlier.
        #Clear AAA EMS Config
        self.Clear_AAA_EMS_Config()
    #    Remove the policy profiles that we created
        # Basic Policy Cleanup
        self.policySuiteUdks.Basic_Policy_Cleanup( self.pytestConfigHelper.config.netelem_name, self.pytestConfigHelper.config.policyId_a, self.pytestConfigHelper.config.policyId_b, 
                                                   self.pytestConfigHelper.config.policyId_c)
    
    #    Remove the vlans that were created.configure port pvid
        # Remove Port/s from Untagged Egress for VLAN and Verify it is Removed  ${netelem1.name}  ${vlan_500}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.vlanUDKs.Remove_Ports_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.conf.vlan_500,
            self.pytestConfigHelper.conf.port_a.ifname)
        self.vlanUDKs.Remove_Ports_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.conf.vlan_500, 
            self.pytestConfigHelper.conf.port_b.ifname)
                
        '''Remove VLAN and Verify it is Removed  ${netelem1.name}  ${vlan_100}
        Remove VLAN and Verify it is Removed  ${netelem1.name}  ${vlan_200}
        Remove VLAN and Verify it is Removed  ${netelem1.name}  ${vlan_300}
        Remove VLAN and Verify it is Removed  ${netelem1.name}  ${vlan_400}
        Remove VLAN and Verify it is Removed  ${netelem1.name}  ${vlan_500}'''
        
        self.vlanUDKs.Remove_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_100)
        self.vlanUDKs.Remove_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_200)
        self.vlanUDKs.Remove_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_300)
        self.vlanUDKs.Remove_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_400)
        self.vlanUDKs.Remove_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_500)
               
        #    Put the port(s) back on the default vlan.
        # Add Port/s to Untagged Egress for VLAN and Verify it is Added  ${netelem1.name}  ${Vlan_Default}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.vlanUDKs.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.conf.Vlan_Default, self.pytestConfigHelper.conf.port_a.ifname)
        self.vlanUDKs.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.conf.Vlan_Default, self.pytestConfigHelper.conf.port_b.ifname)
            
        #    Remove the RADIUS configuration
        #UnConfigure And Disable Radius Netlogin Server  ${netelem1.name}  ${endsysRadius.instance}
        self.radiusSuiteUdk.UnConfigure_And_Disable_Radius_Netlogin_Server(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.conf.radius.instance)
        #UnConfigure And Disable Radius DynAuth Server   ${netelem1.name}  ${endsysRadius.instance}
        self.radiusSuiteUdk.UnConfigure_And_Disable_Radius_DynAuth_Server(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.conf.radius.instance)
    
        # macauth disable  ${netelem1.name}
        self.macAuthUdks.Disable_Macauth_and_Verify_it_is_Disabled(self.pytestConfigHelper.dut1.name)
                
        #disable macauth port  ${netelem1.name}  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.macAuthUdks.Disable_Macauth_Port_and_Verify_it_is_Disabled(self.pytestConfigHelper.dut1.name,  self.pytestConfigHelper.conf.port_a.ifname)
        self.macAuthUdks.Disable_Macauth_Port_and_Verify_it_is_Disabled(self.pytestConfigHelper.dut1.name,  self.pytestConfigHelper.conf.port_b.ifname)
                
        #disable policy and verify it is disabled  ${netelem1.name}
        self.policyUDK.Disable_Policy_and_Verify_it_is_Disabled(self.pytestConfigHelper.dut1.name)
                
        #send cmd  ${netelem1.name}  configure netlogin mac username format none
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'configure netlogin mac username format none') 
        
        #send cmd  ${netelem1.name}  configure netlogin del mac-list ff:ff:ff:ff:ff:ff 48
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'configure netlogin del mac-list ff:ff:ff:ff:ff:ff 48')
    
        #"Base Test Suite Cleanup" must come last... It de-initializes stuff we don't need to know about.
        self.setupTeardownUdks.Base_Test_Suite_Cleanup()
#----------------------------------------------------------------------------------------------------------
#Upgrade Netelem to Latest Firmware
#    [Documentation]  Upgrades the provided netelem to the latest firmware on the TFTP server provided.
#    [Arguments]                          ${netelem_name}  ${tftp_server_ip}  ${build_location}  ${build}  ${mgmt_vlan}  ${netelem_ip}
#    Wait Until Keyword Succeeds  3x  200ms  load_firmware_on_network_element     ${netelem_name}  ${tftp_server_ip}  ${build_location}  vr=${mgmt_vlan}
#    reboot_network_element_now_and_wait  ${netelem_name}  300  20  60
#    send cmd  ${netelem_name}  unconfigure switch  wait_for_prompt=${FALSE}
#    send cmd  ${netelem_name}  y                   check_initial_prompt=${FALSE}
#    wait for pingable  ${netelem_ip}  300  20  20
#    firmware_version_should_be_equal     ${netelem_name}  ${build}

#
#  Check to make sure the expected vlan is in the ClientAuthenticated syslog response for the mac authed users:
#    - checks for MAC address user with no separators between the MAC address Bytes.
#
    def Verify_Syslog_ClientAuthenticated_Message_Vlan(self, authed_vlan, packet1, packet2, mac_address_separator='none'):

            #    String to match must be full words, no partial word matches allowed, punctuation must be included, only space/linefeeds
            #      are acceptable delimiters. (had to have the "," in the original string match now using regex match as policy name was added in 30.7
        if mac_address_separator == 'none' :
          self.networkElementLoggingGenKeywords.logging_verify_regex_in_log(self.pytestConfigHelper.dut1.name)
          network_message = 'Network Login Mac user ' + packet1.noseparator_mac + ' logged in MAC ' + packet1.uppercase_mac + ' port ' + str(self.pytestConfigHelper.dut1_tgen_port_a.ifname) + ' VLAN ' + str(authed_vlan)
          self.create_log_message(network_message)    
        if mac_address_separator == 'none' :            
          self.networkElementLoggingGenKeywords.logging_verify_regex_in_log(self.pytestConfigHelper.dut1.name)          
          network_message = 'Network Login Mac user ' + packet1.noseparator_mac + ' logged in MAC ' + packet1.uppercase_mac + ' port ' + str(self.pytestConfigHelper.dut1_tgen_port_b.ifname) + ' VLAN ' + str(authed_vlan)
          self.create_log_message(network_message)    
        if mac_address_separator == 'hyphen' :            
          self.networkElementLoggingGenKeywords.logging_verify_regex_in_log(self.pytestConfigHelper.dut1.name)                   
          network_message = 'Network Login Mac user ' + packet1.noseparator_mac + ' logged in MAC ' + packet1.uppercase_mac + ' port ' + str(self.pytestConfigHelper.dut1_tgen_port_a.ifname) + ' VLAN ' + str(authed_vlan)
          self.create_log_message(network_message)    
        if mac_address_separator == 'hyphen' :            
          self.networkElementLoggingGenKeywords.logging_verify_regex_in_log(self.pytestConfigHelper.dut1.name)                    
          network_message = 'Network Login Mac user ' + packet1.noseparator_mac + ' logged in MAC ' + packet1.uppercase_mac + ' port ' + str(self.pytestConfigHelper.dut1_tgen_port_b.ifname) + ' VLAN ' + str(authed_vlan)
          self.create_log_message(network_message)  
            


    def Verify_UPM_config_is_correct (self, vid, vid_name, packet1, packet2, mac_address_separator='none', fdb_entry_expected=True):
        #[Arguments]  ${vid}  ${vid_name}  ${packet1}  ${packet2}  ${mac_address_separator}=none  ${fdb_entry_expected}=true
        if  fdb_entry_expected  == 'true':
            #fdb verify entry exists  ${netelem1.name}  ${packet1.src_mac}  ${vid}  ${netelem1.tgen.port_a.ifname}
            self.networkElementFdbGenKeyword(self.pytestConfigHelper.dut1.name,packet1.src_mac,vid,self.pytestConfigHelper.conf.port_a.ifname)
        if fdb_entry_expected == 'true':
            #fdb verify entry exists  ${netelem1.name}  ${packet2.src_mac}  ${vid}  ${netelem1.tgen.port_b.ifname}
            self.networkElementFdbGenKeyword(self.pytestConfigHelper.dut1.name,packet2.src_mac,vid,self.pytestConfigHelper.conf.port_b.ifname)            
        if  fdb_entry_expected == 'false':
            #fdb verify entry does not exist  ${netelem1.name}  ${packet1.src_mac}  ${vid}  ${netelem1.tgen.port_a.ifname}
            self.networkElementFdbGenKeyword(self.pytestConfigHelper.dut1.name,packet1.src_mac,vid,self.pytestConfigHelper.conf.port_a.ifname)
        if  fdb_entry_expected == 'false':
            #fdb verify entry does not exist  ${netelem1.name}  ${packet2.src_mac}  ${vid}  ${netelem1.tgen.port_b.ifname}
            self.networkElementFdbGenKeyword(self.pytestConfigHelper.dut1.name,packet2.src_mac,vid,self.pytestConfigHelper.conf.port_b.ifname) 
        # Verify Syslog ClientAuthenticated Message Vlan  ${vid_name}  ${packet1}  ${packet2}  ${mac_address_separator}
        self.Verify_Syslog_ClientAuthenticated_Message_Vlan(vid_name, packet1, packet2, mac_address_separator)
        
    def Create_List(self):
        pass
    
    def create_log_message(self, mes):
        print(mes)
        #pass
        
#
#  These work...
#
    '''def Configure_UPM_Vlan_Script_dot1xAuthenticate(self):
        UPM_DOT1X_AUTH_SCRIPT =  self.Create_List()
        # create log message "UPM-Auth-Dot1X - Port: \'$(EVENT.USER_PORT)\' Vlan: \'$(EVENT.USER_VLAN)\'"
        self.create_log_message ("UPM-Auth-Dot1X - Port: {}  Vlan: {}" + format(EVENT.USER_PORT,EVENT.USER_VLAN))        
        #enable ip-security dhcp-snooping $(EVENT.USER_VLAN) ports $(EVENT.USER_PORT) violation-action none
        self.networkElementIpsecurityGenKeywords.ipsecurity_enable_dhcp_snooping(self.pytestConfigHelper.dut1.name,EVENT.USER_VLAN, EVENT.USER_PORT) 
        #upm set profile  ${netelem1.name}  dot1xAuthenticate  ${UPM_DOT1X_AUTH_SCRIPT}
        self.networkElementUpmGenKeywords.upm_set_profile(self.pytestConfigHelper.dut1.name)'''

    def Configure_UPM_Vlan_Script_macAuthenticate(self):
        UPM_MAC_AUTH_SCRIPT =  self.Create_List()
        #create log message "UPM-Auth-MAC - Port: \'$(EVENT.USER_PORT)\' Vlan: \'$(EVENT.USER_VLAN)\'"
        # self.create_log_message ("UPM-Auth-Dot1X - Port: {}  Vlan: {}" + format(EVENT.USER_PORT,EVENT.USER_VLAN)) 
        #enable ip-security dhcp-snooping $(EVENT.USER_VLAN) ports $(EVENT.USER_PORT) violation-action none
        # self.networkElementIpsecurityGenKeywords.ipsecurity_enable_dhcp_snooping(self.pytestConfigHelper.dut1.name,EVENT.USER_VLAN, EVENT.USER_PORT) 
        #upm set profile   ${netelem1.name}  macAuthenticate  ${UPM_MAC_AUTH_SCRIPT}
        self.networkElementUpmGenKeywords.upm_set_profile(self.pytestConfigHelper.dut1.name)

    '''def Configure_UPM_Vlan_Script_dot1xUnAuthenticate(self):
        UPM_DOT1X_UNAUTH_SCRIPT =  Create_List
        #create log message "UPM-UnAuth-Dot1X - Port: \'$(EVENT.USER_PORT)\' Vlan: \'$(EVENT.USER_VLAN)\'"
        create_log_message ("UPM-Auth-Dot1X - Port: {}  Vlan: {}" + format(EVENT.USER_PORT,EVENT.USER_VLAN)) 
        #disable ip-security dhcp-snooping $(EVENT.USER_VLAN) ports $(EVENT.USER_PORT) violation-action none
        self.networkElementIpsecurityGenKeywords.ipsecurity_disable_dhcp_snooping(self.pytestConfigHelper.dut1.name,EVENT.USER_VLAN, EVENT.USER_PORT) 
        #upm set profile e  ${netelem1.name}  dot1xUnAuthenticate  ${UPM_DOT1X_UNAUTH_SCRIPT}
        self.networkElementUpmGenKeywords.upm_set_profile(self.pytestConfigHelper.dut1.name)'''

    def Configure_UPM_Vlan_Script_macUnAuthenticate(self):
        UPM_MAC_UNAUTH_SCRIPT =  self.Create_List()
        #create log message "UPM-UnAuth-Mac - Port: \'$(EVENT.USER_PORT)\' Vlan: \'$(EVENT.USER_VLAN)\'"
        # create_log_message ("UPM-Auth-Dot1X - Port: {}  Vlan: {}" + format(EVENT.USER_PORT,EVENT.USER_VLAN)) 
        #disable ip-security dhcp-snooping $(EVENT.USER_VLAN) ports $(EVENT.USER_PORT) violation-action none
        # self.networkElementIpsecurityGenKeywords.ipsecurity_disable_dhcp_snooping(self.pytestConfigHelper.dut1.name,EVENT.USER_VLAN, EVENT.USER_PORT) 
        #upm set profile   ${netelem1.name}  macUnAuthenticate  ${UPM_MAC_UNAUTH_SCRIPT}
        self.networkElementUpmGenKeywords.upm_set_profile(self.pytestConfigHelper.dut1.name)

#  These work...

    def Debug_Dump_UPM_Failure_Info(self):
        #send cmd  ${netelem1.name}  show fdb
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'show fdb')    
        #send cmd  ${netelem1.name}  show netlogin session
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'show netlogin session')
        #send cmd  ${netelem1.name}  show config ipSecurity
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, 'show config ipSecurity')    
        #send cmd  ${netelem1.name}  show port ${netelem1.tgen.port_a.ifname}-${netelem1.tgen.port_b.ifname} vlan
        self.networkElementCliSend.send_cmd(self.pytestConfigHelper.dut1.name, "show port {}-{}".format(self.pytestConfigHelper.conf.port_a.ifname,self.pytestConfigHelper.conf.port_b.ifname))

    def enable_UPM_macAuthenticate_and_macUnauthenticate(self):
        #upm set auth  ${netelem1.name}  macAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.networkElementUpmGenKeywords.upm_set_auth(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.conf.macAuthenticate,self.pytestConfigHelper.conf.port_a.ifname )
        self.networkElementUpmGenKeywords.upm_set_auth(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.conf.macAuthenticate,self.pytestConfigHelper.conf.port_b.ifname )
    
        # upm set unauth  ${netelem1.name}  macUnAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.networkElementUpmGenKeywords.upm_set_auth(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.conf.macUnAuthenticate,self.pytestConfigHelper.conf.port_a.ifname )
        self.networkElementUpmGenKeywords.upm_set_auth(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.conf.macUnAuthenticate,self.pytestConfigHelper.conf.port_b.ifname )
        # upm authenticate event should exist  ${netelem1.name}  macAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        # upm unauthenticated event should exist  ${netelem1.name}  macUnAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}

    def disable_UPM_macAuthenticate_and_macUnauthenticate(self):
        #upm set auth  ${netelem1.name}  macAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.networkElementUpmGenKeywords.upm_set_auth(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.conf.macAuthenticate,self.pytestConfigHelper.conf.port_a.ifname )
        self.networkElementUpmGenKeywords.upm_set_auth(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.conf.macAuthenticate,self.pytestConfigHelper.conf.port_b.ifname )
            
        #upm set unauth  ${netelem1.name}  macUnAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.networkElementUpmGenKeywords.upm_set_unauth(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.conf.macUnAuthenticate,self.pytestConfigHelper.conf.port_a.ifname )
        self.networkElementUpmGenKeywords.upm_set_unauth(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.conf.macUnAuthenticate,self.pytestConfigHelper.conf.port_b.ifname )
            
        #    upm authenticate event should not exist  ${netelem1.name}  macAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        #    upm unauthenticated event should not exist  ${netelem1.name}  macUnAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}

    '''def enable_UPM_dot1XAuthenticate_and_dot1xUnauthenticate(self):
        #upm set auth  ${netelem1.name}  dot1XAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.networkElementUpmGenKeywords.upm_set_auth(self.pytestConfigHelper.dut1.name, dot1XAuthenticate,self.pytestConfigHelper.conf.port_a.ifname )
        self.networkElementUpmGenKeywords.upm_set_auth(self.pytestConfigHelper.dut1.name, dot1XAuthenticate,self.pytestConfigHelper.conf.port_b.ifname )
                
        #upm set unauth  ${netelem1.name}  dot1XUnAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.networkElementUpmGenKeywords.upm_set_unauth(self.pytestConfigHelper.dut1.name, dot1XUnAuthenticate,self.pytestConfigHelper.conf.port_a.ifname )
        self.networkElementUpmGenKeywords.upm_set_unauth(self.pytestConfigHelper.dut1.name, dot1XUnAuthenticate,self.pytestConfigHelper.conf.port_b.ifname )
       
        #    upm authenticate event should exist  ${netelem1.name}  dot1XAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        #    upm unauthenticated event should exist  ${netelem1.name}  dot1XUnAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}'''

    '''def disable_UPM_dot1XAuthenticate_and_dot1xUnauthenticate(self):
        #upm set auth  ${netelem1.name}  dot1XAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.networkElementUpmGenKeywords.upm_set_auth(self.pytestConfigHelper.dut1.name, dot1XAuthenticate,self.pytestConfigHelper.conf.port_a.ifname )
        self.networkElementUpmGenKeywords.upm_set_auth(self.pytestConfigHelper.dut1.name, dot1XAuthenticate,self.pytestConfigHelper.conf.port_b.ifname )
       
        #upm set unauth  ${netelem1.name}  dot1XUnAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        self.networkElementUpmGenKeywords.upm_set_unauth(self.pytestConfigHelper.dut1.name, dot1XUnAuthenticate,self.pytestConfigHelper.conf.port_a.ifname )
        self.networkElementUpmGenKeywords.upm_set_unauth(self.pytestConfigHelper.dut1.name, dot1XUnAuthenticate,self.pytestConfigHelper.conf.port_b.ifname )
               
        #    upm authenticate event should not exist  ${netelem1.name}  dot1XAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}
        #    upm unauthenticated event should not exist  ${netelem1.name}  dot1XUnAuthenticate  ${netelem1.tgen.port_a.ifname},${netelem1.tgen.port_b.ifname}'''