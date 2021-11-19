#*** Settings ***
#Documentation_Brief_description_of_where_these_keywords_are_used.
#Resource_AllResources.robot

#*** Keywords ***
# ---------------------------------------------------------------------------------------------------------------------
# Setup/Teardown_Keywords
# ---------------------------------------------------------------------------------------------------------------------
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Keywords.EndsystemKeywords.EndsystemConnectionManager import EndsystemConnectionManager
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementFdbGenKeywords import NetworkElementFdbGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementIpsecurityGenKeywords import NetworkElementIpsecurityGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementLoggingGenKeywords import NetworkElementLoggingGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementLoginconfigGenKeywords import NetworkElementLoginconfigGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementMacauthGenKeywords import NetworkElementMacauthGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementPolicyGenKeywords import NetworkElementPolicyGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementPolicyGenKeywords import NetworkElementPolicyGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementPortGenKeywords import NetworkElementPortGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementUpmGenKeywords import NetworkElementUpmGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementVlanGenKeywords import NetworkElementVlanGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementVlanGenKeywords import NetworkElementVlanGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.StaticKeywords.NetworkElementHostUtilsKeywords import NetworkElementHostUtilsKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementCliSend import NetworkElementCliSend
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementConnectionVerification import NetworkElementConnectionVerification
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementListUtils import NetworkElementListUtils
from ExtremeAutomation.Keywords.TrafficKeywords.TrafficCaptureKeywords import TrafficCaptureKeywords
from ExtremeAutomation.Keywords.TrafficKeywords.TrafficPacketCreationKeywords import TrafficPacketCreationKeywords
from ExtremeAutomation.Keywords.TrafficKeywords.TrafficPacketInspectionKeywords import TrafficPacketInspectionKeywords
from ExtremeAutomation.Keywords.TrafficKeywords.TrafficStatisticsKeywords import TrafficStatisticsKeywords
from ExtremeAutomation.Keywords.TrafficKeywords.TrafficTransmitKeywords import TrafficTransmitKeywords
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.L2.FdbUdks import FdbUdks
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.L2.VlanUdks import VlanUdks
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.QOS.CosUdks import CosUdks
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.Security.MacAuthUdks import MacAuthUdks
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.Security.PolicyUdks import PolicyUdks
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.SetupTeardown.SetupTeardownUdks import SetupTeardownUdks
import time
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.L1.PortUdks import PortUdks
from Tests.Pytest.Functional.nonprod.Resources.PlatformGenericSuiteUdks import PlatformGenericSuiteUdks
from Tests.Pytest.Functional.nonprod.Resources.PlatformGenericSuiteUdks import PlatformGenericSuiteUdks
from Tests.Pytest.Functional.nonprod.Resources.PolicySuiteUdks import PolicySuiteUdks
from Tests.Pytest.Functional.nonprod.Resources.RadiusSuiteUdks import RadiusSuiteUdks
from Tests.Pytest.Functional.nonprod.Resources.TrafficSuiteUdks import TrafficGenerationSuiteUdks
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import NetworkElementConnectionManager
from ExtremeAutomation.Keywords.NetworkElementKeywords.StaticKeywords.NetworkElementFileManagementUtilsKeywords import NetworkElementFileManagementUtilsKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.StaticKeywords.NetworkElementResetDeviceUtilsKeywords import NetworkElementResetDeviceUtilsKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementCosGenKeywords import NetworkElementCosGenKeywords
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.L3.InterfaceUdks import InterfaceUdks
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.L3.ArpUdks import ArpUdks
class Policy_Test_Suite_Udks():
    
    def __init__(self, pytestConfigHelper):
        self.pytestConfigHelper = pytestConfigHelper        
        self.defaultLibrary = DefaultLibrary()
        self.platformGenericSuiteUdks = PlatformGenericSuiteUdks()
        self.networkElementCliSend = NetworkElementCliSend()
        self.radiusSuiteUdks = RadiusSuiteUdks()
        self.endsystemConnectionMan = EndsystemConnectionManager()
        self.tgenUdks = self.defaultLibrary.apiUdks.trafficGenerationUdks
        self.networkElementPortGenKeywords = NetworkElementPortGenKeywords()
        self.networkElementVlanGenKeywords = NetworkElementVlanGenKeywords()
        self.policyUdks = PolicyUdks()
        self.networkElementMacAuth = NetworkElementMacauthGenKeywords()
        self.macAuthUdks = MacAuthUdks()
        self.vlanUdks =  VlanUdks()
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
        self.portUdks = PortUdks()
        self.cosUdks = CosUdks()
        self.trafficCaptureKeywords = TrafficCaptureKeywords()
        self.trafficStatisticsKeywords = TrafficStatisticsKeywords()
        self.trafficPacketInspectionKeywords = TrafficPacketInspectionKeywords()
        self.trafficPacketCreationKeywords = TrafficPacketCreationKeywords()
        self.networkElementConnectionManager = NetworkElementConnectionManager()
        self.networkElementFileManagementUtilsKeywords = NetworkElementFileManagementUtilsKeywords()
        self.networkElementResetDeviceUtilsKeywords = NetworkElementResetDeviceUtilsKeywords()
        self.fdbUdks = FdbUdks()
        self.networkElementCosGenKeywords = NetworkElementCosGenKeywords()
        self.interfaceUdks = InterfaceUdks()
        self.arpUdks = ArpUdks()
        #################
        self.netElem1Name = self.pytestConfigHelper.dut1.name
         

    def Dump_Policy_Diagnostics(self):
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'show config')
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'show log \| exclude ConvEndPoint')
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'debug ems show trace aaa all')
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'debug ems show trace policy all')
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'debug ems show trace netlogin all')
            
    def Initialize_Policy_Diagnostics(self):
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'clear log static')
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'debug ems clear trace aaa all')
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'debug ems clear trace policy all')
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'debug ems clear trace netlogin all')
            
    
    # Standard_Test_Case_setup_for_all_AAA_test_cases
    def Policy_Common_Test_Case_Setup(self):
        self.Initialize_Policy_Diagnostics()
    
    # Standard_Test_Case_Cleanup_for_AAA_All_Test_Cases(self,):
    def Policy_Common_Test_Case_Cleanup(self, runPolicyDiagnostics = False):
        if runPolicyDiagnostics == True:
            self.Dump_Policy_Diagnostics()
    
    
    # Test_Suite_Setup/Cleanup_once_per_the_entire_AAA_Test_Suite
    def Initialize_Policy_EMS_Config(self):
        #FIND OUT HOW TO DO THE BELOW!!
        #${ERROR_LIST}=  Create_List_Error_error        
        #use this until you fix the above
        ERROR_LIST = []
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'enable log debug-mode',  ignore_error='TRUE')
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'configure log filter DefaultFilter add events Policy severity debug-data',
                                            ignore_error = ERROR_LIST)
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'configure log filter DefaultFilter add events AAA severity debug-data',
                                            ignore_error = ERROR_LIST)
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'configure log target memory-buffer number-of-messages 20000',
                                            ignore_error = ERROR_LIST)        
    
    def Clear_Policy_EMS_Config(self,):
        #FIND OUT HOW TO DO THE BELOW!!
        #${ERROR_LIST}=  Create_List_Error_error_AttributeError_Traceback
        #use this until you fix the above
        ERROR_LIST = []
        
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'disable log debug-mode', ignore_error = ERROR_LIST)
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'configure log filter DefaultFilter delete events Policy severity debug-data',
                                             ignore_error = ERROR_LIST)
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'configure log filter DefaultFilter delete events AAA severity debug-data',
                                             ignore_error = ERROR_LIST)
        self.networkElementCliSend.send_cmd(self.netElem1Name, 'configure log target memory-buffer number-of-messages 1000',
                                             ignore_error = ERROR_LIST)
            
    def Test_Suite_Setup(self,):
        
        self.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()
        self.Initialize_Policy_EMS_Config()
        
        #NEED TO FIGURE THIS OUT
        #ConfidenceLevel =   Get_Variable_Value  ConfidenceLevel   defaultConfidenceLevel
        ConfidenceLevel = ''
        
        #NEED TO FIGURE THIS OUT
        #set_global_variable  ${ConfidenceLevel}
        
        if self.pytestConfigHelper.dut1.upgrade_firmware == 'True':
            self.platformGenericSuiteUdks.Upgrade_Netelem_to_Latest_Firmware(self.netElem1Name,  
                                                                             self.pytestConfigHelper.config.tftp_server.ip, 
                                                                             self.pytestConfigHelper.dut1.build_directory, 
                                                                             self.pytestConfigHelper.dut1.build, 
                                                                             self.pytestConfigHelper.dut1.mgmt_vlan, 
                                                                             self.pytestConfigHelper.dut1.ip)
        
        
        
        self.change_policy_rule_model( self.netElem1Name, 'Hierarchical_No-Verify')
        #Remove_Port/s_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed
        self.vlanUdks.Remove_Ports_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_default, 
            self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.vlanUdks.Remove_Ports_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_default, 
            self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.vlanUdks.Remove_Ports_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_default, 
            self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        
    
    def Test_Suite_Cleanup(self,):
        self.Clear_Policy_EMS_Config()
        #Add_Port/s_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_default, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_default, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_default, self.pytestConfigHelper.dut1_tgen_port_c.ifname)
        
        #policy disable
        #Policy_Disable  ${netelem1.name}
        self.networkElementPolicyGenKeywords.policy_disable(self.pytestConfigHelper.dut1.name)
        self.setupTeardownUdks.Base_Test_Suite_Cleanup()
    
    #Upgrade_Netelem_to_Latest_Firmware
    #    [Documentation]  Upgrades_the_provided_netelem_to_the_latest_firmware_on_the_TFTP_server_provided.
    #    [Arguments]                          ${netelem_name}  ${tftp_server_ip}  ${build_location}  ${build}  ${mgmt_vlan}
    #    Wait_Until_Keyword_Succeeds_3x_200ms_load_firmware_on_network_element     ${netelem_name}  ${tftp_server_ip}  ${build_location}  vr=${mgmt_vlan}
    #    reboot_network_element_now_and_wait  ${netelem_name}  300_20_60
    #    firmware_version_should_be_equal     ${netelem_name}  ${build}
    
    def Policy_Test_Case_Setup_A(self,):
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_b.ifname)        
        self.Create_and_Configure_all_QOS_Profiles(self.pytestConfigHelper.dut1.name)        
        self.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.dut1_tgen_port_a.ifname,
                                                               self.pytestConfigHelper.config.qos_profile_4)        
        self.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.vlan_a)        
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        
        self.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_b.ifname)        
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vlan_a,self.pytestConfigHelper.dut1_tgen_port_b.ifname)       
    
    def Policy_Test_Case_Setup_B(self,):
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.vlan_a)        
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vlan_a,self.pytestConfigHelper.dut1_tgen_port_b.ifname)        
    
    def Policy_Test_Case_Setup_C(self,):
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_c.ifname)
        self.Create_and_Configure_all_QOS_Profiles(self.pytestConfigHelper.dut1.name)
        self.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.vlan_a)         
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_a.ifname)        
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_c.ifname)        
        self.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vlan_a,self.pytestConfigHelper.dut1_tgen_port_b.ifname)        
    
    def Policy_Test_Case_Setup_D(self,):
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_c.ifname)
        self.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.vlan_a)        
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_a.ifname)        
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_c.ifname)        
        self.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vlan_a,self.pytestConfigHelper.dut1_tgen_port_b.ifname)       
            
    def Policy_Test_Case_Setup_QinQ_Tagged(self,):
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        '''self.Create_and_Configure_all_QOS_Profiles(self.pytestConfigHelper.dut1.name)        
        self.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.dut1_tgen_port_a.ifname,
                                                               self.pytestConfigHelper.config.qos_profile_4)       
        '''
        self.vlanUdks.Create_VMAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b)        
        self.vlanUdks.Add_Port_Tagged_for_VMAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b,
                                                                      self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.vlanUdks.Add_Port_Tagged_for_VMAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b,
                                                                      self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vman_b_name,self.pytestConfigHelper.dut1_tgen_port_b.ifname)       
    
    def Policy_Test_Case_Setup_QinQ_Untagged(self,):
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.Create_and_Configure_all_QOS_Profiles(self.pytestConfigHelper.dut1.name)        
        self.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.dut1_tgen_port_a.ifname,
                                                               self.pytestConfigHelper.config.qos_profile_4)      
        self.vlanUdks.Create_VMAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b)                
        self.vlanUdks.Add_Port_Tagged_for_VMAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b,
                                                                      self.pytestConfigHelper.dut1_tgen_port_a.ifname)        
        self.vlanUdks.Add_Port_Tagged_for_VMAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b,
                                                                      self.pytestConfigHelper.dut1_tgen_port_b.ifname)        
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vman_b_name,self.pytestConfigHelper.dut1_tgen_port_b.ifname) 
    
    def Policy_Test_Case_Setup_Port_Untagged(self,):
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_c.ifname)
        self.Create_and_Configure_all_QOS_Profiles(self.pytestConfigHelper.dut1.name)        
        self.vlanUdks.Create_VMAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b)        
        self.vlanUdks.Add_Port_Untagged_for_VMAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b,
                                                                      self.pytestConfigHelper.dut1_tgen_port_a.ifname)        
        self.vlanUdks.Add_Port_Untagged_for_VMAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b,
                                                                      self.pytestConfigHelper.dut1_tgen_port_c.ifname)
        self.vlanUdks.Add_Port_Tagged_for_VMAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b,
                                                                      self.pytestConfigHelper.dut1_tgen_port_b.ifname)               
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vman_b_name,self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        
    def Policy_Test_Case_Setup_Port_Tagged(self,):
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_c.ifname)
        self.Create_and_Configure_all_QOS_Profiles(self.pytestConfigHelper.dut1.name)      
        self.vlanUdks.Create_VMAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b)
        
        self.vlanUdks.Add_Port_Tagged_for_VMAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b,
                                                                      self.pytestConfigHelper.dut1_tgen_port_a.ifname)        
        self.vlanUdks.Add_Port_Tagged_for_VMAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b,
                                                                      self.pytestConfigHelper.dut1_tgen_port_c.ifname)
        self.vlanUdks.Add_Port_Tagged_for_VMAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b,
                                                                      self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vman_b_name,self.pytestConfigHelper.dut1_tgen_port_b.ifname)     
    
    def Policy_Test_Case_Setup_Admin_Rules(self,):
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.Create_and_Configure_all_QOS_Profiles(self.pytestConfigHelper.dut1.name)
        self.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.dut1_tgen_port_a.ifname,
                                                               self.pytestConfigHelper.config.qos_profile_4)       
        self.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.vlan_a)
        
        self.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.vlan_b)
        
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_b.ifname)        
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vlan_a,self.pytestConfigHelper.dut1_tgen_port_b.ifname)        
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vlan_b,self.pytestConfigHelper.dut1_tgen_port_b.ifname)        
    
    def Policy_Test_Case_Setup_Admin_Rules_Port(self,):
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_c.ifname)
        self.Create_and_Configure_all_QOS_Profiles(self.pytestConfigHelper.dut1.name)
        self.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.dut1_tgen_port_a.ifname, 
                                                             self.pytestConfigHelper.config.qos_profile_4)
        self.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.vlan_a)        
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_a.ifname)       
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_c.ifname)        
        self.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_b.ifname)      
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vlan_a,self.pytestConfigHelper.dut1_tgen_port_b.ifname)
    
    def Policy_Test_Case_Setup_Admin_Rules_Ports(self,):
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_c.ifname)
        self.Create_and_Configure_all_QOS_Profiles(self.pytestConfigHelper.dut1.name)
        self.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.dut1_tgen_port_a.ifname, self.pytestConfigHelper.config.qos_profile_4)
        self.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.vlan_a)
        self.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.vlan_b)        
        self.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.vlan_c)        
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_a.ifname)        
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_c,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_c.ifname)        
        self.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_b.ifname)        
        self.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_b,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_b.ifname)        
        self.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_c,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vlan_a,self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vlan_b,self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vlan_c,self.pytestConfigHelper.dut1_tgen_port_b.ifname)
            
    def Policy_Test_Case_Setup_Precedence(self,):
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.Create_and_Configure_all_QOS_Profiles(self.pytestConfigHelper.dut1.name)
        self.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.dut1_tgen_port_a.ifname, 
                                                             self.pytestConfigHelper.config.qos_profile_4)
        self.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.vlan_a)       
        self.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.config.vlan_a,
                                                                                     self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.dst_mac_a,
                                                                 self.pytestConfigHelper.config.vlan_a,self.pytestConfigHelper.dut1_tgen_port_b.ifname)       
           
    def Policy_Test_Case_Setup_Egress_VLANs(self,):
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_a.ifname)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.pytestConfigHelper.dut1.name, self.pytestConfigHelper.dut1_tgen_port_b.ifname)
        self.Create_and_Configure_all_QOS_Profiles(self.pytestConfigHelper.dut1.name)
        self.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.dut1_tgen_port_a.ifname, 
                                                             self.pytestConfigHelper.config.qos_profile_4)
        self.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.vlan_a)
        self.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.pytestConfigHelper.dut1.name,self.pytestConfigHelper.config.vlan_b)
    
    # ---------------------------------------------------------------------------------------------------------------------
    def Bounce_Netelem_Port(self, device_name,  port):
        self.portUdks.Disable_Port_and_Validate_Port_is_Disabled(device_name, port)
        self.portUdks.Enable_Port_and_Validate_Port_is_Enabled(device_name, port)
    
    # NOTE: Stacked_systems_do_not_allow_configuration_of_COS_Queue_6
    def Create_and_Configure_all_QOS_Profiles(self,network_element_name):        
        #Create_QOS_Profile_and_Verify_it_was_Created          ${netelem_name}  ${qos_profile_all}
        self.cosUdks.Create_QOS_Profile_and_Verify_it_was_Created(network_element_name, self.pytestConfigHelper.config.qos_profile_all)
        self.cosUdks.Configure_COS_Setting_Priority(network_element_name,'0','0','qp1')
        self.cosUdks.Configure_COS_Setting_Priority(network_element_name,'1','1','qp1')
        self.cosUdks.Configure_COS_Setting_Priority(network_element_name,'2','2','qp1')
        self.cosUdks.Configure_COS_Setting_Priority(network_element_name,'3','3','qp1')
        self.cosUdks.Configure_COS_Setting_Priority(network_element_name,'4','4','qp1')
        self.cosUdks.Configure_COS_Setting_Priority(network_element_name,'5','5','qp1')
        self.cosUdks.Configure_COS_Setting_Priority(network_element_name,'7','7','qp1')
    
    # NOTE: Stacked_systems_do_not_allow_configuration_of_COS_Queue_6
    def Clear_all_Dot1p_QOS_Profiles(self, network_element_name):
        self.cosUdks.Configure_COS_Setting_Priority(network_element_name,'0','0','qp1')
        self.cosUdks.Configure_COS_Setting_Priority(network_element_name,'1','0','qp1')
        self.cosUdks.Configure_COS_Setting_Priority(network_element_name,'2','0','qp1')
        self.cosUdks.Configure_COS_Setting_Priority(network_element_name,'3','0','qp1')
        self.cosUdks.Configure_COS_Setting_Priority(network_element_name,'4','0','qp1')
        self.cosUdks.Configure_COS_Setting_Priority(network_element_name,'5','0','qp1')
        self.cosUdks.Configure_COS_Setting_Priority(network_element_name,'7','7','qp1')
            
    def Configure_Policy_Profile_PVID_and_Enable_Override(self, netelem_name, profile_id, pvid):        
        self.networkElementPolicyGenKeywords.policy_set_profile_pvid(netelem_name,profile_id, pvid)
        self.networkElementPolicyGenKeywords.policy_set_profile_pvid_Status(netelem_name,profile_id, 'enable')
        self.networkElementPolicyGenKeywords.Policy_Verify_Profile_PVID_Status_Enabled(netelem_name, profile_id)        
            
    def Create_Policy_Profile_with_PVID_Status_and_CoS_Status_Disabled(self, netelem_name,  profile_id,  pvid, cos_value):               
        self.policyUdks.Create_Policy_Profile_and_Verify_it_Exists(netelem_name, profile_id)
        self.networkElementPolicyGenKeywords.policy_set_profile_pvid(netelem_name,profile_id, pvid)
        self.networkElementPolicyGenKeywords.policy_set_profile_pvid_status(netelem_name,profile_id, 'disable')        
        self.networkElementPolicyGenKeywords.policy_verify_profile_pvid(netelem_name, profile_id, pvid)        
        self.networkElementPolicyGenKeywords.policy_verify_profile_pvid_status_disabled(netelem_name, profile_id)
        self.networkElementPolicyGenKeywords.policy_set_profile_cos(netelem_name, profile_id, cos_value)        
        self.networkElementPolicyGenKeywords.policy_set_profile_cos_status(netelem_name, profile_id, 'disable')
        self.networkElementPolicyGenKeywords.policy_verify_profile_cos(netelem_name, profile_id, cos_value)        
        self.networkElementPolicyGenKeywords.policy_verify_profile_cos_status_should_be_disabled(netelem_name, profile_id) 
    
    def Transmit_10_Frames_and_Verify_FDB_Entry_is_Learned(self, netelem_name, tx_port, pkt_name_a,  src_mac,  dst_mac, vlan_id,  src_port):        
        #Create_Ethernet2_Packet    ${pkt_name_a}  dst_mac  src_mac     vlan_id
        self.tgenUdks.Create_Ethernet2_Packet(pkt_name_a, dst_mac, src_mac,vlan_id, packet_len='80')
        #config burst of 10       
        self.tgenUdks.Configure_Packet_on_Port_Single_Burst(tx_port, pkt_name_a, count='100')
        #start transmit
        self.trafficTransmitKeywords.start_transmit_on_port(tx_port)
        #wait 
        time.sleep(10)
        #stop transmit    
        self.trafficTransmitKeywords.stop_transmit_on_port(tx_port)
        #check fdb        
        #FDB_Verify_Entry_Exists  ${netelem_name}  src_mac  vlan_id     src_port
        self.networkElementFdbGenKeywords.fdb_verify_entry_exists(netelem_name, src_mac, vlan_id, src_port)
        
    def Transmit_10_QinQ_Frames_and_Verify_FDB_Entry_is_Learned(self, netelem_name, tx_port,  pkt_name_a, src_mac, dst_mac,  vlan_list,  tpid_list, vman_name,  src_port):        
        #Create_Ethernet2_VLAN_Stack_Packet     ${pkt_name_a}    dst_mac     src_mac
        #Set_VLAN_Stack_Tag                     ${pkt_name_a}    vlan_list   vlan_tpid_list=tpid_list
        self.tgenUdks.Create_Ethernet2_VLAN_Stack_Packet(pkt_name_a, dst_mac, src_mac, vlan_list,
                                           vlan_prio_list=None, vlan_tpid_list=tpid_list, ether_type=None,
                                           packet_len='112')
        #config burst of 10       
        self.tgenUdks.Configure_Packet_on_Port_Single_Burst(tx_port, pkt_name_a, count='10')
        #start transmit
        self.trafficTransmitKeywords.start_transmit_on_port(tx_port)
        #wait 
        time.sleep(2)
        #stop transmit    
        self.trafficTransmitKeywords.stop_transmit_on_port(tx_port)
        #check fdb       
        self.networkElementFdbGenKeywords.fdb_verify_entry_exists(netelem_name, src_mac, vman_name, src_port)     
    
    def Transmit_and_Verify_Frames_Received(self, tx_port, rx_port, sentdmac = None,  sentsmac = None):
        if sentdmac == None:
            sentdmac = self.pytestConfigHelper.config.dst_mac_a
        if sentsmac == None:
            sentsmac = self.pytestConfigHelper.config.src_mac_a
        #Clear_Port_Statistics                   tx_port
        self.trafficCaptureKeywords.clear_port_statistics(tx_port)               
        #Transmit_Packet_on_Port, Single_Burst   tx_port  tx_packet        
        #self.tgenUdks.Create_Ethernet2_Packet('genericTx', self.pytestConfigHelper.config.packetA.dst_mac, self.pytestConfigHelper.config.packetA.src_mac, packet_len='80')
        #config burst of 100       
        self.tgenUdks.Configure_Packet_on_Port_Single_Burst(tx_port, 'genericTx', count='100')
        #start capture
        #self.tgenUdks.Start_Capture_with_DMAC_and_SMAC_Filter(rx_port,self.pytestConfigHelper.config.packetA.dst_mac, self.pytestConfigHelper.config.packetA.src_mac)
        #self.tgenUdks.Start_Capture_with_DMAC_and_SMAC_Filter(rx_port,self.pytestConfigHelper.config.dst_mac_a, self.pytestConfigHelper.config.src_mac_a)
        self.tgenUdks.Start_Capture_with_DMAC_and_SMAC_Filter(rx_port, sentdmac, sentsmac)
        #start transmit
        self.trafficTransmitKeywords.start_transmit_on_port(tx_port)
        #wait 
        time.sleep(2)
        #stop transmit    
        self.trafficTransmitKeywords.stop_transmit_on_port(tx_port)               
        #stop_capture_on_port                    rx_port
        self.trafficCaptureKeywords.stop_capture_on_port(rx_port)        
        #Get_Captured_Count                      rx_port
        self.trafficStatisticsKeywords.get_captured_count(rx_port)                
        #Stat_Value_Should_be_Plus_or_Minus      rx_port  100_5
        self.trafficStatisticsKeywords.stat_value_should_be_plus_or_minus(rx_port, '100', '5')        
        #Get_Tx_Count                            tx_port
        self.trafficStatisticsKeywords.get_tx_count(tx_port) 
        # Stat_Value_Should_be_Equal              tx_port  100           
        self.trafficStatisticsKeywords.stat_value_should_be_equal(tx_port, '100')
        #capture_inspection_range                rx_port  rx_packet_50_54
        self.trafficPacketInspectionKeywords.capture_inspection_range(rx_port,'genericRx','50','54' )        
    #    Capture_Inspection_Random_List          rx_port  rx_packet_5
    
    def Transmit_and_Verify_Frames_Received_And_Mirrored(self, tx_port,  rx_port,  mirror_port ):       
        #Clear_Port_Statistics                   tx_port
        self.trafficCaptureKeywords.clear_port_statistics(tx_port)                
        #Transmit_Packet_on_Port, Single_Burst   tx_port  tx_packet        
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', self.pytestConfigHelper.config.packetA.dst_mac, self.pytestConfigHelper.config.packetA.src_mac, packet_len='80')
        #config burst of 100       
        self.tgenUdks.Configure_Packet_on_Port_Single_Burst(tx_port, 'genericTx', count='100')
        #start capture
        self.tgenUdks.Start_Capture_with_DMAC_and_SMAC_Filter(rx_port,self.pytestConfigHelper.config.packetA.dst_mac, self.pytestConfigHelper.config.packetA.src_mac)
        self.tgenUdks.Start_Capture_with_DMAC_and_SMAC_Filter(mirror_port,self.pytestConfigHelper.config.packetA.dst_mac, self.pytestConfigHelper.config.packetA.src_mac)
        #start transmit
        self.trafficTransmitKeywords.start_transmit_on_port(tx_port)
        #wait 
        time.sleep(2)
        #stop transmit    
        self.trafficTransmitKeywords.stop_transmit_on_port(tx_port)               
        #stop_capture_on_ports
        self.trafficCaptureKeywords.stop_capture_on_port(rx_port)
        self.trafficCaptureKeywords.stop_capture_on_port(mirror_port)
        #capture  
        self.trafficStatisticsKeywords.get_captured_count(rx_port)
        self.trafficStatisticsKeywords.get_captured_count(mirror_port)
        #check stats values
        self.trafficTransmitKeywords.stat_value_should_be_plus_or_minus(rx_port, '100', '5')
        self.trafficTransmitKeywords.stat_value_should_be_plus_or_minus(mirror_port, '100', '5')        
        #Get_Tx_Count                            tx_port
        self.trafficStatisticsKeywords.get_tx_count(tx_port) 
        # Stat_Value_Should_be_Equal              tx_port  100           
        self.trafficStatisticsKeywords.stat_value_should_be_equal(tx_port, '100')        
        # capture_inspection_range                rx_port  rx_packet_50_54
        self.trafficPacketInspectionKeywords.capture_inspection_range(rx_port,'rx_packet','50','54' )        
        # capture_inspection_range                rx_port  mirror_packet_50_54
        self.trafficPacketInspectionKeywords.capture_inspection_range(rx_port,'mirror_packet','50','54' )
            
    def Transmit_and_Verify_Frames_and_Trap_Received(self, tx_port,  rx_port, trap_port):        
        #Clear_Port_Statistics                   tx_port
        self.trafficCaptureKeywords.clear_port_statistics(tx_port)        
        #Transmit_Packet_on_Port, Single_Burst   tx_port  tx_packet        
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', self.pytestConfigHelper.config.packetA.dst_mac, self.pytestConfigHelper.config.packetA.src_mac, packet_len='80')
        #config burst of 100       
        self.tgenUdks.Configure_Packet_on_Port_Single_Burst(tx_port, 'genericTx', count='100')
        #start capture
        self.tgenUdks.Start_Capture_with_DMAC_and_SMAC_Filter(rx_port,self.pytestConfigHelper.config.packetA.dst_mac, self.pytestConfigHelper.config.packetA.src_mac)
        self.tgenUdks.Start_Capture_with_DMAC_and_SMAC_Filter(trap_port,self.pytestConfigHelper.config.packetA.dst_mac, self.pytestConfigHelper.config.packetA.src_mac)
        #start transmit
        self.trafficTransmitKeywords.start_transmit_on_port(tx_port)
        #wait 
        time.sleep(2)
        #stop transmit    
        self.trafficTransmitKeywords.stop_transmit_on_port(tx_port)               
        #stop_capture_on_ports
        self.trafficCaptureKeywords.stop_capture_on_port(rx_port)
        self.trafficCaptureKeywords.stop_capture_on_port(trap_port)
        #capture  
        self.trafficStatisticsKeywords.get_captured_count(rx_port)
        self.trafficStatisticsKeywords.get_captured_count(trap_port)
        #check stats values
        self.trafficTransmitKeywords.stat_value_should_be_plus_or_minus(rx_port, '100', '5')
        self.trafficTransmitKeywords.stat_value_should_be_plus_or_minus(trap_port, '2', '1')        
        #Get_Tx_Count                            tx_port
        self.trafficStatisticsKeywords.get_tx_count(tx_port) 
        # Stat_Value_Should_be_Equal              tx_port  100           
        self.trafficStatisticsKeywords.stat_value_should_be_equal(tx_port, '100')        
        # capture_inspection_range                rx_port  rx_packet_50_54
        self.trafficPacketInspectionKeywords.capture_inspection_range(rx_port,'rx_packet','50','54' )        
        # capture_inspection_range                rx_port  mirror_packet_50_54
        self.trafficPacketInspectionKeywords.capture_inspection_range(rx_port,'mirror_packet','50','54' )    
    #
    #  Notice_we_allow_up_to_2_frames_to_get_through_when_we_are "verifying_not_received"
    #    This_is_due_to_the_fact_that_policy_can "bleed" a_frame_or_two_through_in_certain
    #    cases_while_it_is_applying_the_policy_profile_rules.
    #
    #  This_will_occur_with_static_policy_profile_application_or_in_casees_where
    #    auth_optional_is_enabled.
    #
    def Transmit_and_Verify_Frames_NOT_Received(self, tx_port, rx_port, sentdmac = None,  sentsmac = None):
        if sentdmac == None:
            sentdmac = self.pytestConfigHelper.config.dst_mac_a
        if sentsmac == None:
            sentsmac = self.pytestConfigHelper.config.src_mac_a         
        #Clear_Port_Statistics                   tx_port
        self.trafficCaptureKeywords.clear_port_statistics(tx_port)               
        #Transmit_Packet_on_Port, Single_Burst   tx_port  tx_packet        
        #self.tgenUdks.Create_Ethernet2_Packet('genericTx', self.pytestConfigHelper.config.packetA.dst_mac, self.pytestConfigHelper.config.packetA.src_mac, packet_len='80')
        #config burst of 100       
        self.tgenUdks.Configure_Packet_on_Port_Single_Burst(tx_port, 'genericTx', count='100')
        #start capture
        #self.tgenUdks.Start_Capture_with_DMAC_and_SMAC_Filter(rx_port,self.pytestConfigHelper.config.packetA.dst_mac, self.pytestConfigHelper.config.packetA.src_mac)
        #self.tgenUdks.Start_Capture_with_DMAC_and_SMAC_Filter(rx_port,self.pytestConfigHelper.config.dst_mac_a, self.pytestConfigHelper.config.src_mac_a)
        self.tgenUdks.Start_Capture_with_DMAC_and_SMAC_Filter(rx_port, sentdmac, sentsmac)
        #start transmit
        self.trafficTransmitKeywords.start_transmit_on_port(tx_port)
        #wait 
        time.sleep(2)
        #stop transmit    
        self.trafficTransmitKeywords.stop_transmit_on_port(tx_port)               
        #stop_capture_on_port                    rx_port
        self.trafficCaptureKeywords.stop_capture_on_port(rx_port)        
        #Get_Captured_Count                      rx_port
        self.trafficStatisticsKeywords.get_captured_count(rx_port)                
        #Stat_Value_Should_be_Plus_or_Minus      rx_port  0 2
        self.trafficStatisticsKeywords.stat_value_should_be_plus_or_minus(rx_port, '0', '2')            
        #Get_Tx_Count                            tx_port
        self.trafficStatisticsKeywords.get_tx_count(tx_port) 
        # Stat_Value_Should_be_Equal              tx_port  100           
        self.trafficStatisticsKeywords.stat_value_should_be_equal(tx_port, '100')       
    
    # ---------------------------------------------------------------------------------------------------------------------
    # L2_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_Frames_and_Verify_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id):        
        #Create_Ethernet2_Packet_tx_packet  dst_mac  src_mac
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, packet_len='80')        
        #Create_Ethernet2_Packet_rx_packet  dst_mac  src_mac  vlan_id
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac,vlan_id, packet_len='80')       
        #self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)        
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_Frames_and_Verify_NOT_Received(self, tx_port,  rx_port, src_mac,  dst_mac,  vlan_id ):        
        #Create_Ethernet2_Packet_tx_packet  dst_mac  src_mac
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, packet_len='80')        
        #self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)        
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Untagged_Frames_and_Verify_Received_Untagged(self, tx_port, rx_port, src_mac, dst_mac):        
        #Create_Ethernet2_Packet_tx_packet  dst_mac  src_mac        
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, packet_len='80')        
        #Create_Ethernet2_Packet_rx_packet  dst_mac  src_mac
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, packet_len='80')               
        #self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)        
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_Frames_and_Verify_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id):       
        #Create_Ethernet2_Packet_tx_packet  dst_mac  src_mac  vlan_id
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, vlan_id, packet_len='80')        
        #Create_Ethernet2_Packet_rx_packet  dst_mac  src_mac  vlan_id
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, packet_len='80')               
        #self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)        
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_Frames_and_Verify_NOT_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id):        
        #Create_Ethernet2_Packet_tx_packet  dst_mac  src_mac  vlan_id
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, vlan_id, packet_len='80')                
        #self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)        
        #self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port, dst_mac, src_mac)
    
    def Transmit_100_Tagged_Frames_and_Verify_Priority_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, tx_priority, rx_priority):        
        #Create_Ethernet2_Packet_tx_packet  dst_mac  src_mac  vlan_id  tx_priority
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, vlan_id, tx_priority, packet_len='80')
        #Create_Ethernet2_Packet_rx_packet  dst_mac  src_mac  vlan_id  rx_priority
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, packet_len='80')
        #self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_Frames_and_Verify_Priority_Has_NOT_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, priority):        
        #Create_Ethernet2_Packet_tx_packet  dst_mac  src_mac  vlan_id  priority
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, vlan_id, priority, packet_len='80')
        #Create_Ethernet2_Packet_rx_packet  dst_mac  src_mac  vlan_id  priority
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, packet_len='80')
        #self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)        
    
    def Transmit_100_Untagged_Frames_and_Verify_Priority_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, rx_priority):        
        #Create_Ethernet2_Packet_tx_packet  dst_mac  src_mac
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, packet_len='80')
        #Create_Ethernet2_Packet_rx_packet  dst_mac  src_mac  vlan_id  rx_priority
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)       
    
    def Transmit_100_Untagged_Frames_and_Verify_Priority_Has_NOT_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id):        
        #Create_Ethernet2_Packet_tx_packet  dst_mac  src_mac
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, vlan_id, packet_len='80')
        #Create_Ethernet2_Packet_rx_packet  dst_mac  src_mac  vlan_id  0
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, '0', packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_Frames_and_Verify_Priority_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, tx_priority, rx_priority):
        
        #Create_Ethernet2_Packet_tx_packet  dst_mac  src_mac  0  tx_priority
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, '0', tx_priority, packet_len='80')        
        #Create_Ethernet2_Packet_rx_packet  dst_mac  src_mac  vlan_id  rx_priority
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, packet_len='80')        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_Frames_and_Verify_Priority_Has_NOT_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, priority):        
        #Create_Ethernet2_Packet_tx_packet  dst_mac  src_mac  0  priority
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, '0', priority, packet_len='80')        
        #Create_Ethernet2_Packet_rx_packet  dst_mac  src_mac  vlan_id  priority
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)        
    
    def Transmit_100_QinQ_Untagged_Frames_and_Verify_Priority(self, tx_port, rx_port, src_mac,  dst_mac,  vlan_id, priority, rx_vlan_list, rx_prio_list, rx_tpid_list):
        '''[Arguments]  tx_port  rx_port  src_mac  dst_mac  vlan_id  priority  rx_vlan_list
        ...          rx_prio_list         rx_tpid_list'''
        #Create_Ethernet2_Packet_tx_packet   dst_mac  src_mac  vlan_id  priority
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, vlan_id, priority, packet_len='80')                
        '''Create_Ethernet2_VLAN_Stack_Packet_rx_packet   dst_mac  src_mac  rx_vlan_list  rx_prio_list
        ...                                  rx_tpid_list'''
        self.tgenUdks.Create_Ethernet2_VLAN_Stack_Packet('genericRx', dst_mac, src_mac, rx_vlan_list, rx_prio_list, rx_tpid_list, ether_type=None, packet_len='112')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)       
    
    def Transmit_100_QinQ_Tagged_Frames_and_Verify_Priority(self, tx_port, rx_port, src_mac, dst_mac, tx_vlan_list, rx_vlan_list, tx_prio_list, rx_prio_list, tx_tpid_list, rx_tpid_list):
        
        '''Create_Ethernet2_VLAN_Stack_Packet_tx_packet   dst_mac  src_mac  tx_vlan_list  tx_prio_list
        ...                                  tx_tpid_list'''
        self.tgenUdks.Create_Ethernet2_VLAN_Stack_Packet('genericTx', dst_mac, src_mac, tx_vlan_list, tx_prio_list, tx_tpid_list, ether_type=None, packet_len='112')        
        '''Create_Ethernet2_VLAN_Stack_Packet_rx_packet   dst_mac  src_mac  rx_vlan_list  rx_prio_list
        ...                                  rx_tpid_list'''
        
        self.tgenUdks.Create_Ethernet2_VLAN_Stack_Packet('genericRx', dst_mac, src_mac, rx_vlan_list, rx_prio_list, rx_tpid_list, ether_type=None, packet_len='112')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)   
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IPv4_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_IPv4_Frames_and_Verify_Received(self, tx_port,  rx_port,  src_mac,  dst_mac, vlan_id, sip, dip):        
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, packet_len='80')        
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip, packet_len='80')        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv4_Frames_and_Verify_NOT_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, sip, dip):        
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)        
    
    def Transmit_100_Tagged_IPv4_Frames_and_Verify_Received(self, tx_port, rx_port, src_mac,  dst_mac, vlan_id,  sip, dip):       
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip, packet_len='80')        
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip, packet_len='80')        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv4_Frames_and_Verify_NOT_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, sip, dip):        
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IPv4_Frames_and_Verify_Priority_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, tx_priority, rx_priority, sip, dip):        
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, tx_priority, dip=dip,  sip=sip, packet_len='80')        
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip,  sip=sip, packet_len='80')        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)       
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv4_Frames_and_Verify_Priority_Has_NOT_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, priority, sip, dip):        
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip, packet_len='80')        
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip, packet_len='80')        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv4_Frames_and_Verify_Priority_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, rx_priority, sip, dip):        
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip,  sip=sip, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv4_Frames_and_Verify_Priority_Has_NOT_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, sip, dip):        
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, packet_len='80')        
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, '0', dip=dip, sip=sip, packet_len='80')        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv4_Frames_and_Verify_Priority_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, tx_priority, rx_priority, sip, dip):        
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, '0', tx_priority, dip=dip, sip=sip, packet_len='80')        
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip,  sip=sip, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv4_Frames_and_Verify_Priority_Has_NOT_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, priority, sip, dip):        
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, '0', priority, dip=dip,  sip=sip, packet_len='80')        
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IPv6_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_IPv6_Frames_and_Verify_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, sip, dip):        
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, packet_len='80')       
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Frames_and_Verify_NOT_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, sip, dip):        
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IPv6_Frames_and_Verify_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, sip, dip):        
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip, packet_len='80')        
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_Frames_and_Verify_NOT_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, sip, dip):        
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IPv6_Frames_and_Verify_Priority_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, tx_priority, rx_priority, sip, dip):       
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, tx_priority, dip=dip, sip=sip, packet_len='80')         
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip, sip=sip, packet_len='80')        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)        
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
            
    def Transmit_100_Tagged_IPv6_Frames_and_Verify_Priority_Has_NOT_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, priority, sip, dip):        
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, priority, dip=dip, sip=sip, packet_len='80')        
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip, sip=sip, packet_len='80')        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Frames_and_Verify_Priority_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, rx_priority, sip, dip):       
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip, sip=sip, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Frames_and_Verify_Priority_Has_NOT_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, sip, dip):       
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, packet_len='80')        
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, '0', dip=dip, sip=sip, packet_len='80')        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv6_Frames_and_Verify_Priority_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, tx_priority, rx_priority, sip, dip):               
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, '0', tx_priority, dip=dip, sip=sip, packet_len='80')        
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip, sip=sip, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv6_Frames_and_Verify_Priority_Has_NOT_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, priority, sip, dip):               
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, '0', priority, dip=dip, sip=sip, packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip, sip=sip, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IPX_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_IPX_Frames_and_Verify_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, ether_type):        
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, ether_type=ether_type, packet_len='80')        
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, ether_type=ether_type, packet_len='80')        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPX_Frames_and_Verify_NOT_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, ether_type):        
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, ether_type=ether_type, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IPX_Frames_and_Verify_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, ether_type):                                                                                   
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, vlan_id, ether_type=ether_type, packet_len='80')        
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, ether_type=ether_type, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPX_Frames_and_Verify_NOT_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, ether_type):        
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, vlan_id, ether_type=ether_type, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IPX_Frames_and_Verify_Priority_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, tx_priority,  rx_priority, ether_type):        
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, vlan_id, tx_priority, ether_type=ether_type, packet_len='80')        
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, ether_type=ether_type, packet_len='80')        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPX_Frames_and_Verify_Priority_Has_NOT_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, priority, ether_type ):                
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, vlan_id, priority, ether_type=ether_type, packet_len='80')        
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, ether_type=ether_type, packet_len='80')        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPX_Frames_and_Verify_Priority_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, rx_priority, ether_type):        
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, ether_type=ether_type, packet_len='80')
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, ether_type=ether_type, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPX_Frames_and_Verify_Priority_Has_NOT_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, ether_type):        
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, ether_type=ether_type, packet_len='80')        
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac,vlan_id, '0', ether_type=ether_type, packet_len='80')        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPX_Frames_and_Verify_Priority_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, tx_priority, rx_priority, ether_type):        
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, '0', ether_type=ether_type, packet_len='80')
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, ether_type=ether_type, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPX_Frames_and_Verify_Priority_Has_NOT_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, priority, ether_type):    
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, '0', priority, ether_type=ether_type, packet_len='80')
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, ether_type=ether_type, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IP_TCP_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_TCP_Frames_and_Verify_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, sip, dip, src_port, dst_port, 
                                                             ttl=None,  tos=None, flags=None, offset=None):          
        self.tgenUdks.Create_IPv4_TCP_Packet('genericTx',  dst_mac,  src_mac,  dip=dip,  sip=sip,  ttl=ttl,   tos=tos,
                                              flags=flags, frag_offset=offset, src_port=src_port, dst_port=dst_port, packet_len='80')
        
        self.tgenUdks.Create_IPv4_TCP_Packet('genericRx', dst_mac, src_mac,vlan_id, dip=dip,  sip=sip,  ttl=ttl, tos=tos,
                                      flags=flags,   frag_offset=offset,  src_port=src_port, dst_port=dst_port, packet_len='80') 
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    #
    #  Forwarded_frames_are_egress_tagged, mirrored_frames_egress_untagged (the_same_as_they_ingressed).
    #
    def Transmit_100_Untagged_TCP_Frames_and_Verify_Received_and_Mirrored(self,tx_port,rx_port,mirror_port,src_mac,dst_mac, vlan_id, sip, dip, src_port, dst_port,
                    ttl=None, tos=None,  flags=None,  offset=None):
       
        self.tgenUdks.Create_IPv4_TCP_Packet('genericTx', dst_mac, src_mac,  dip=dip,  sip=sip,  ttl=ttl,   tos=tos,
                                   flags=flags,   frag_offset=offset,  src_port=src_port,  dst_port=dst_port, packet_len='80')
        self.tgenUdks.Create_IPv4_TCP_Packet('genericRx',  dst_mac, src_mac,  vlan_id,  dip=dip,  sip=sip,  ttl=ttl,   tos=tos,
                                   flags=flags,   frag_offset=offset,  src_port=src_port,  dst_port=dst_port, packet_len='80')
        self.tgenUdks.Create_IPv4_TCP_Packet('genericMirror',  dst_mac, src_mac,  dip=dip,  sip=sip,  ttl=ttl,  tos=tos,
                                  flags=flags,   frag_offset=offset,  src_port=src_port,  dst_port=dst_port, packet_len='80')    
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)        
        self.tgenUdks.Start_Capture_with_DMAC_Filter(mirror_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received_and_Mirrored(tx_port, rx_port, mirror_port)
    
    def Transmit_100_Untagged_TCP_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac, vlan_id, sip, dip, src_port, dst_port,
                    ttl=None, tos=None,  flags=None,  offset=None):
        self.tgenUdks.Create_IPv4_TCP_Packet('genericTx', dst_mac, src_mac,  dip=dip,  sip=sip,  ttl=ttl,   tos=tos,
                                   flags=flags,   frag_offset=offset,  src_port=src_port,  dst_port=dst_port, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_TCP_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac, vlan_id, sip, dip, src_port, dst_port):
        self.tgenUdks.Create_IPv4_TCP_Packet('genericTx', dst_mac, src_mac, vlan_id,  dip=dip,  sip=sip,  src_port=src_port,  dst_port=dst_port, packet_len='80')
        self.tgenUdks.Create_IPv4_TCP_Packet('genericRx', dst_mac, src_mac, vlan_id,  dip=dip,  sip=sip,  src_port=src_port,  dst_port=dst_port, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_TCP_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac, vlan_id, sip, dip, src_port, dst_port):
        self.tgenUdks.Create_IPv4_TCP_Packet('genericTx', dst_mac, src_mac, vlan_id,  dip=dip,  sip=sip,  src_port=src_port,  dst_port=dst_port, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_TCP_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac, vlan_id, tx_priority, rx_priority, sip, dip, src_port, dst_port):
        self.tgenUdks.Create_IPv4_TCP_Packet('genericTx', dst_mac, src_mac, vlan_id, tx_priority, dip=dip,  sip=sip,  src_port=src_port,  dst_port=dst_port, packet_len='80')
        self.tgenUdks.Create_IPv4_TCP_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip,  sip=sip,  src_port=src_port,  dst_port=dst_port, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_TCP_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac, vlan_id, priority, sip, dip, src_port, dst_port):
        self.tgenUdks.Create_IPv4_TCP_Packet('genericTx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip,  src_port=src_port,  dst_port=dst_port, packet_len='80')
        self.tgenUdks.Create_IPv4_TCP_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip,  src_port=src_port,  dst_port=dst_port, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_TCP_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac, vlan_id, rx_priority, sip, dip, src_port, dst_port,ttl=None,tos=None,flags=None,offset=None):
        self.tgenUdks.Create_IPv4_TCP_Packet('genericTx',dst_mac, src_mac, dip=dip, sip=sip, ttl=ttl, tos=tos, flags=flags, frag_offset=offset, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Create_IPv4_TCP_Packet('genericRx',dst_mac, src_mac, vlan_id, rx_priority, dip=dip, sip=sip, ttl=ttl, tos=tos, flags=flags, frag_offset=offset, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_TCP_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac, vlan_id, sip, dip, src_port, dst_port):       
        self.tgenUdks.Create_IPv4_TCP_Packet('genericTx',dst_mac, src_mac, dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Create_IPv4_TCP_Packet('genericRx',dst_mac, src_mac, vlan_id, '0', dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_TCP_Frames_and_Verify_Priority_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, tx_priority, rx_priority, 
                                                                            sip, dip, src_port, dst_port):        
        self.tgenUdks.Create_IPv4_TCP_Packet('genericTx', dst_mac, src_mac, '0', tx_priority,dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Create_IPv4_TCP_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority,dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_TCP_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv4_TCP_Packet('genericTx', dst_mac, src_mac, '0', priority,dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Create_IPv4_TCP_Packet('genericRx', dst_mac, src_mac, vlan_id, priority,dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IP_UDP_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_UDP_Frames_and_Verify_Received(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, sip, dip,  src_port, dst_port):
        self.tgenUdks.Create_IPv4_UDP_Packet('genericTx', dst_mac, src_mac, dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Create_IPv4_UDP_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_UDP_Frames_and_Verify_NOT_Received(self,tx_port,rx_port, src_mac,dst_mac,vlan_id,sip,dip,src_port,dst_port,
                                                                 ttl=None,tos=None, flags=None,offset=None):
        self.tgenUdks.Create_IPv4_UDP_Packet('genericTx', dst_mac, src_mac, dip=dip, sip=sip, ttl=ttl, tos=tos,flags=flags, frag_offset=offset,
                                             src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_UDP_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id, sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv4_UDP_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Create_IPv4_UDP_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_UDP_Frames_and_Verify_NOT_Received(self,tx_port,rx_port, src_mac,dst_mac,vlan_id,sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv4_UDP_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_UDP_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,
                                                                   sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv4_UDP_Packet('genericTx', dst_mac, src_mac, vlan_id, tx_priority, dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Create_IPv4_UDP_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_UDP_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,
                                                                           src_port,dst_port):        
        self.tgenUdks.Create_IPv4_UDP_Packet('genericTx', dst_mac, src_mac, vlan_id, priority, dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Create_IPv4_UDP_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip, sip=sip, src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_UDP_Frames_and_Verify_Priority_Changed(self, tx_port, rx_port, src_mac, dst_mac, vlan_id, rx_priority, sip,  dip, src_port, dst_port,  
                                                                     ttl=None, tos=None, flags=None, offset=None):
        self.tgenUdks.Create_IPv4_UDP_Packet('genericTx', dst_mac, src_mac, dip=dip, sip=sip,ttl=ttl, tos=tos, flags=flags, frag_offset=offset,
                                             src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Create_IPv4_UDP_Packet('generiRx', dst_mac, src_mac,vlan_id,rx_priority,dip=dip, sip=sip,ttl=ttl, tos=tos, flags=flags, frag_offset=offset,
                                             src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_UDP_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv4_UDP_Packet('genericTx', dst_mac, src_mac, dip=dip, sip=sip,src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Create_IPv4_UDP_Packet('genericRx', dst_mac, src_mac,vlan_id,'0', dip=dip, sip=sip,src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac,dst_mac,src_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_UDP_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,
                                                                            sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv4_UDP_Packet('genericTx', dst_mac, src_mac,'0',tx_priority, dip=dip, sip=sip,src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Create_IPv4_UDP_Packet('genericRx', dst_mac, src_mac,vlan_id,rx_priority, dip=dip, sip=sip,src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_UDP_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,
                                                                                    src_port,dst_port):
        self.tgenUdks.Create_IPv4_UDP_Packet('genericTx', dst_mac, src_mac,'0',priority, dip=dip, sip=sip,src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Create_IPv4_UDP_Packet('genericRx', dst_mac, src_mac,vlan_id,priority, dip=dip, sip=sip,src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IPv4/IPv6_ICMP_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_IPv4_ICMP_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,ttl=None,tos=None,
                                                                       flags=None,offset=None,icmp_type=None, code=None):
        self.tgenUdks.Create_IPv4_ICMP_Packet('genericTx',dst_mac, src_mac,dip=dip,sip=sip,ttl=ttl,tos=tos,flags=flags,
                                             frag_offset=offset,icmp_type=icmp_type,code=code)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Untagged_IPv4_ICMP_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,ttl=None,tos=None,
                                                                       flags=None,offset=None,icmp_type=None, code=None):
        self.tgenUdks.Create_IPv4_ICMP_Packet('genericTx',dst_mac, src_mac,dip=dip,sip=sip,ttl=ttl,tos=tos,flags=flags,
                                             frag_offset=offset,icmp_type=icmp_type,code=code)
        self.tgenUdks.Create_IPv4_ICMP_Packet('genericRx',dst_mac, src_mac,vlan_id,rx_priority,dip=dip,sip=sip,ttl=ttl,tos=tos,flags=flags,
                                             frag_offset=offset,icmp_type=icmp_type,code=code)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv4_SNAP_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,ttl=None,
                                                                       tos=None,flags=None,offset=None):
        self.tgenUdks.Create_IPv4_SNAP_Packet('genericTx',dst_mac, src_mac,dip=dip,sip=sip,ttl=ttl,tos=tos,flags=flags,
                                             frag_offset=offset)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Untagged_IPv4_SNAP_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,
                                                                            ttl=None,tos=None,flags=None, offset=None):
        self.tgenUdks.Create_IPv4_SNAP_Packet('genericTx',dst_mac, src_mac,dip=dip,sip=sip,ttl=ttl,tos=tos,flags=flags,
                                             frag_offset=offset)
        self.tgenUdks.Create_IPv4_SNAP_Packet('genericRx',dst_mac, src_mac,dip=dip,sip=sip,ttl=ttl,tos=tos,flags=flags,
                                             frag_offset=offset)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_SNAP_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,hop_limit=None,
                                                                       traffic_class=None):
        self.tgenUdks.Create_IPv6_SNAP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,hop_limit=hop_limit,traffic_class=traffic_class)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Untagged_IPv6_SNAP_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,
                                                                           hop_limit=None,traffic_class=None):
        self.tgenUdks.Create_IPv6_SNAP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,hop_limit=hop_limit,traffic_class=traffic_class)
        self.tgenUdks.Create_IPv6_SNAP_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip,hop_limit=hop_limit,
                                              traffic_class=traffic_class)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_SNAP_Fragments_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,hop_limit=None,
                                                                          traffic_class=None):
        self.tgenUdks.Create_IPv6_SNAP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,hop_limit=hop_limit,traffic_class=traffic_class)        
        self.trafficPacketCreationKeywords.set_ipv6_fragment('genericTx')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Untagged_IPv6_SNAP_Fragments_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,
                                                                              hop_limit=None, traffic_class=None):
        self.tgenUdks.Create_IPv6_SNAP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,hop_limit=hop_limit,traffic_class=traffic_class)
        self.trafficPacketCreationKeywords.set_ipv6_fragment('genericTx')
        self.tgenUdks.Create_IPv6_SNAP_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip,hop_limit=hop_limit,
                                              traffic_class=traffic_class)
        self.trafficPacketCreationKeywords.set_ipv6_fragment('genericRx')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_ICMP_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,traffic_class=None,
                                                                       next_header=None, hop_limit=None,icmp_type=None,code=None):
        self.tgenUdks.Create_IPv6_ICMP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,traffic_class=traffic_class,next_header=next_header,
                                              hop_limit=hop_limit,icmp_type=icmp_type,code=code)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Untagged_IPv6_ICMP_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,
                                                                           traffic_class=None,next_header=None,hop_limit=None,
                                                                           icmp_type=None,code=None):
        self.tgenUdks.Create_IPv6_ICMP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,traffic_class=traffic_class,next_header=next_header,
                                              hop_limit=hop_limit,icmp_type=icmp_type,code=code)
        self.tgenUdks.Create_IPv6_ICMP_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip,traffic_class=traffic_class,next_header=next_header,
                                              hop_limit=hop_limit,icmp_type=icmp_type,code=code)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_ICMP_Fragments_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,traffic_class=None,
                                                                          next_header=None, hop_limit=None,icmp_type=None,code=None):        
        self.tgenUdks.Create_IPv6_ICMP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,traffic_class=traffic_class,next_header=next_header,
                                              hop_limit=hop_limit,icmp_type=icmp_type,code=code)
        self.trafficPacketCreationKeywords.set_ipv6_fragment('genericTx')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Untagged_IPv6_ICMP_Fragments_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,
                                                                              traffic_class=None, next_header=None,hop_limit=None,icmp_type=None,
                                                                              code=None):
        self.tgenUdks.Create_IPv6_ICMP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,traffic_class=traffic_class,next_header=next_header,
                                              hop_limit=hop_limit,icmp_type=icmp_type,code=code)
        self.trafficPacketCreationKeywords.set_ipv6_fragment('genericTx')
        self.tgenUdks.Create_IPv6_ICMP_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip,traffic_class=traffic_class,
                                              next_header=next_header,hop_limit=hop_limit,icmp_type=icmp_type,code=code)
        self.trafficPacketCreationKeywords.set_ipv6_fragment('genericRx')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IPv6_TCP_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_IPv6_TCP_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,
                                                                  sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv6_TCP_Packet('genericTx',dst_mac, src_mac,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_TCP_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,hop_limit=None,
                                                                      traffic_class=None,src_port=None,dst_port=None):
        self.tgenUdks.Create_IPv6_TCP_Packet('genericTx',dst_mac, src_mac,dip=dip,sip=sip,hop_limit=hop_limit,traffic_class=traffic_class,
                                             src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IPv6_TCP_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv6_TCP_Packet('genericTx',dst_mac, src_mac,vlan_id,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_TCP_Packet('genericRx',dst_mac, src_mac,vlan_id,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_TCP_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv6_TCP_Packet('genericTx',dst_mac, src_mac,vlan_id,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IPv6_TCP_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,
                                                                        sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv6_TCP_Packet('genericTx',dst_mac, src_mac,vlan_id,tx_priority,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_TCP_Packet('genericRx',dst_mac, src_mac,vlan_id,rx_priority,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_TCP_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,
                                                                                src_port,dst_port):
        self.tgenUdks.Create_IPv6_TCP_Packet('genericTx',dst_mac, src_mac,vlan_id,priority,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_TCP_Packet('genericRx',dst_mac, src_mac,vlan_id,priority,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_TCP_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,
                                                                          hop_limit=None,traffic_class=None, src_port=None,dst_port=None):
        self.tgenUdks.Create_IPv6_TCP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,hop_limit=hop_limit,
                                             traffic_class=traffic_class,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_TCP_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip,hop_limit=hop_limit,
                                             traffic_class=traffic_class,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_TCP_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,
                                                                                  src_port,dst_port):
        self.tgenUdks.Create_IPv6_TCP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_TCP_Packet('genericRx',dst_mac,src_mac,vlan_id,'0',dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv6_TCP_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,
                                                                                 sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv6_TCP_Packet('genericTx',dst_mac,src_mac,'0',tx_priority,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_TCP_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv6_TCP_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,
                                                                                         src_port,dst_port):
        self.tgenUdks.Create_IPv6_TCP_Packet('genericTx',dst_mac,src_mac,'0',priority,dip=dip,sip=sip,
                                             src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_TCP_Packet('genericRx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IPv6_UDP_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_IPv6_UDP_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,src_port,dst_port):
        
        self.tgenUdks.Create_IPv6_UDP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        
        self.tgenUdks.Create_IPv6_UDP_Packet('genericRx',dst_mac,src_mac,vlan_id,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_UDP_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,hop_limit=None,
                                                                      traffic_class=None,src_port=None,dst_port=None):
        self.tgenUdks.Create_IPv6_TCP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,hop_limit=hop_limit,traffic_class=traffic_class,
                                             src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IPv6_UDP_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv6_UDP_Packet('genericTx',dst_mac,src_mac,vlan_id,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_UDP_Packet('genericRx',dst_mac,src_mac,vlan_id,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_UDP_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv6_UDP_Packet('genericTx',dst_mac,src_mac,vlan_id,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IPv6_UDP_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,
                                                                        sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv6_UDP_Packet('genericTx',dst_mac,src_mac,vlan_id,tx_priority,dip=dip,sip=sip,src_port=src_port,
                                             dst_port=dst_port)
        self.tgenUdks.Create_IPv6_UDP_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip,src_port=src_port,
                                             dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_UDP_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,
                                                                                src_port, dst_port):
        self.tgenUdks.Create_IPv6_UDP_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,src_port=src_port,
                                             dst_port=dst_port)
        self.tgenUdks.Create_IPv6_UDP_Packet('genericRx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,src_port=src_port,
                                             dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_UDP_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,hop_limit=None,
                                                                          traffic_class=None,src_port=None,dst_port=None):
        self.tgenUdks.Create_IPv6_UDP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,hop_limit=hop_limit,traffic_class=traffic_class,
                                             src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_UDP_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip,hop_limit=hop_limit,
                                             traffic_class=traffic_class,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_UDP_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,
                                                                                  src_port,dst_port):
        self.tgenUdks.Create_IPv6_UDP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_UDP_Packet('genericRx',dst_mac,src_mac,vlan_id,'0',dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv6_UDP_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,
                                                                                 sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv6_UDP_Packet('genericTx',dst_mac,src_mac,'0',tx_priority,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_UDP_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv6_UDP_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,
                                                                                         sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv6_UDP_Packet('genericTx',dst_mac,src_mac,'0',priority,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_UDP_Packet('genericRx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IP_Fragment_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_IP_Frag_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,id,flags,offset): 
        self.tgenUdks.Create_IPv4_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,id=id,flags=flags,frag_offset=offset,packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx',dst_mac,src_mac,vlan_id,dip=dip,sip=sip,id=id,flags=flags,frag_offset=offset,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IP_Frag_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,id,flags,offset):
        self.tgenUdks.Create_IPv4_Packet('genericTx',dst_mac,src_mac,dip=dip,id=id,flags=flags,frag_offset=offset,sip=sip,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IP_Frag_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,id,flags,offset):
        self.tgenUdks.Create_IPv4_Packet('genericTx',dst_mac,src_mac,vlan_id,dip=dip,sip=sip,id=id,flags=flags,frag_offset=offset,packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx',dst_mac,src_mac,vlan_id,dip=dip,id=id,flags=flags,frag_offset=offset,sip=sip,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IP_Frag_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,id,flags,offset):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id,dip=dip,sip=sip,id=id,flags=flags,frag_offset=offset,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IP_Frag_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,sip,dip,id,flags,offset):
        self.tgenUdks.Create_IPv4_Packet('genericTx',dst_mac,src_mac,vlan_id,tx_priority,dip=dip,sip=sip, packet_len='80') 
        self.tgenUdks.Create_IPv4_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip, packet_len='80') 
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IP_Frag_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,
                                                                               dip,id,flags,offset): 
        self.tgenUdks.Create_IPv4_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,id=id,flags=flags,frag_offset=offset,packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,id=id,flags=flags,frag_offset=offset,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IP_Frag_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,id,
                                                                         flags,offset):
        self.tgenUdks.Create_IPv4_Packet('genericTx',dst_mac,src_mac,dip=dip,  sip=sip,id=id,flags=flags,frag_offset=offset, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip,id=id,flags=flags,frag_offset=offset,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IP_Frag_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,
                                                                                 id,flags,offset):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, '0', dip=dip, sip=sip, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IP_Frag_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,
                                                                                rx_priority,sip,dip,id,flags,offset):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, '0', tx_priority, dip=dip, sip=sip,id=id,flags=flags,frag_offset=offset, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip,  sip=sip,id=id,flags=flags,frag_offset=offset, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IP_Frag_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,id,flags,offset):
        
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, '0', priority, dip=dip,  sip=sip, id=id,flags=flags,frag_offset=offset,packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip,id=id,flags=flags,frag_offset=offset, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IPv6_Fragment_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_IPv6_Frag_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip):
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip)
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericRx',dst_mac,src_mac,vlan_id,dip=dip,sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Frag_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip):
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_Frag_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip):
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericTx',dst_mac,src_mac,vlan_id,dip=dip,sip=sip)
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericRx',dst_mac,src_mac,vlan_id,dip=dip,sip=sip) 
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_Frag_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip):
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericTx',dst_mac,src_mac,vlan_id,dip=dip,sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IPv6_Frag_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,
                                                                         sip,dip):
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericTx',dst_mac,src_mac,vlan_id,tx_priority,dip=dip,sip=sip)
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_Frag_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip):
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip)
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Frag_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip):
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip) 
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Frag_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip):
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip)
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericRx',dst_mac,src_mac,vlan_id,'0',dip=dip,sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv6_Frag_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,sip,dip):
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericTx',dst_mac,src_mac,'0',tx_priority,dip=dip,sip=sip)
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv6_Frag_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip):
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericTx',dst_mac,src_mac,'0',priority,dip=dip,sip=sip)
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericRx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_TCP_Fragments_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,hop_limit=None,
                                                                         traffic_class=None, src_port=None,dst_port=None):
        self.tgenUdks.Create_IPv6_TCP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,src_port=src_port, dst_port=dst_port)
        #Set_IPv6_Fragment_tx_packet
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Untagged_IPv6_TCP_Fragments_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,hop_limit=None,
                                                                             traffic_class=None,src_port=None,dst_port=None):
        self.tgenUdks.Create_IPv6_TCP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,hop_limit=hop_limit,traffic_class=traffic_class,src_port=src_port,
                                             dst_port=dst_port)
        self.trafficPacketCreationKeywords.set_ipv6_fragment('genericTx')
        self.tgenUdks.Create_IPv6_TCP_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip,hop_limit=hop_limit,traffic_class=traffic_class,src_port=src_port,
                                             dst_port=dst_port)
        self.trafficPacketCreationKeywords.set_ipv6_fragment('genericRx')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_UDP_Fragments_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,hop_limit=None,
                                                                         traffic_class=None, src_port=None,dst_port=None): 
        self.tgenUdks.Create_IPv6_UDP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,hop_limit=hop_limit,traffic_class=traffic_class,src_port=src_port,
                                             dst_port=dst_port)
        self.trafficPacketCreationKeywords.set_ipv6_fragment('genericTx')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_UDP_Fragments_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,
                                                                             hop_limit=None,traffic_class=None, src_port=None, dst_port=None):
        self.tgenUdks.Create_IPv6_UDP_Packet('genericTx',dst_mac,src_mac,dip=dip,sip=sip,hop_limit=hop_limit,traffic_class=traffic_class,src_port=src_port,
                                             dst_port=dst_port)
        self.trafficPacketCreationKeywords.set_ipv6_fragment('genericTx')
        self.tgenUdks.Create_IPv6_UDP_Packet('genericRx',dst_mac,src_mac,vlan_id,rx_priority,dip=dip,sip=sip,hop_limit=hop_limit,traffic_class=traffic_class,
                                             src_port=src_port,dst_port=dst_port)
        self.trafficPacketCreationKeywords.set_ipv6_fragment('genericRx')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IP_TTL_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_IP_TTL_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,ttl):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip,ttl=ttl, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip,ttl=ttl, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IP_TTL_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip, dip, ttl):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, ttl=ttl, packet_len='80') 
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IP_TTL_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,ttl):
        
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip,ttl=ttl, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip,ttl=ttl, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IP_TTL_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,ttl):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip,ttl=ttl, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IP_TTL_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac, dst_mac, vlan_id,tx_priority,rx_priority,
                                                                      sip,dip,ttl): 
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, tx_priority, dip=dip,  sip=sip, ttl=ttl,packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip,  sip=sip, ttl=ttl, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IP_TTL_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,ttl):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip,ttl=ttl, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip,ttl=ttl, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port)
        
    def Transmit_100_Untagged_IP_TTL_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,ttl):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, ttl=ttl,packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip,  sip=sip,ttl=ttl,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IP_TTL_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,ttl): 
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip,ttl=ttl, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, '0', dip=dip, sip=sip,ttl=ttl, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IP_TTL_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,
                                                                               sip,dip,ttl):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, '0', tx_priority, dip=dip, sip=sip,ttl=ttl, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip,  sip=sip, ttl=ttl,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac,dst_mac,src_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IP_TTL_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,ttl): 
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, '0', priority, dip=dip,  sip=sip,ttl=ttl, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip,ttl=ttl, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IPv6_TTL_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_IPv6_Hop_Limit_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,ttl): 
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip,hop_limit=ttl, packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip,hop_limit=ttl, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Hop_Limit_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,ttl):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, hop_limit=ttl,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_Hop_Limit_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,ttl):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip,hop_limit=ttl, packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip,hop_limit=ttl, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_Hop_Limit_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,ttl):
        
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip,hop_limit=ttl, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IPv6_Hop_Limit_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,
                                                                              rx_priority,sip,dip,ttl):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, tx_priority, dip=dip, sip=sip, hop_limit=ttl,packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip, sip=sip, hop_limit=ttl,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_Hop_Limit_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,ttl):
        
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, priority, dip=dip, sip=sip, hop_limit=ttl,packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip, sip=sip, hop_limit=ttl,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Hop_Limit_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,ttl):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, hop_limit=ttl,packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip, sip=sip, hop_limit=ttl,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Hop_Limit_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,ttl):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip,hop_limit=ttl, packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, '0', dip=dip, sip=sip,hop_limit=ttl, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv6_Hop_Limit_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,
                                                                                       sip,dip, ttl):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, '0', tx_priority, dip=dip, sip=sip, hop_limit=ttl,packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip, sip=sip, hop_limit=ttl,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv6_Hop_Limit_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,ttl):
        self.tgenUdks.Create_IPv6_Packet('genericTx',dst_mac,src_mac,'0',priority,  dip=dip,  sip=sip,hop_limit=ttl,packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip, sip=sip, hop_limit=ttl,packet_len='80') 
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IP_ToS_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_IP_ToS_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,tos): 
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip,tos=tos, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip, tos=tos, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IP_ToS_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,tos):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, tos=tos,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IP_ToS_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,tos): 
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip,   tos=tos,packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip,   tos=tos,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IP_ToS_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,tos):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip, tos=tos,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IP_ToS_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,
                                                                      rx_priority,sip,dip,tos):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, tx_priority, dip=dip,  sip=sip,  tos=tos,packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip,  sip=sip, tos=tos, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IP_ToS_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,tos):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip, tos=tos,packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip, tos=tos,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac) 
    
    def Transmit_100_Untagged_IP_ToS_Frames_and_Verify_Priority_Changed(self,tx_port, rx_port, src_mac,dst_mac, vlan_id, rx_priority, sip,  dip,  tos): 
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip,tos=tos, packet_len='80')  
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip,  sip=sip, tos=tos,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IP_ToS_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,tos): 
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, tos=tos,packet_len='80')  
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, '0', dip=dip, sip=sip,tos=tos, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IP_ToS_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,sip,dip,tos): 
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, '0', tx_priority, dip=dip, sip=sip,tos=tos, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip,  sip=sip, tos=tos,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IP_ToS_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,tos):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, '0', priority, dip=dip,  sip=sip, tos=tos,packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip, tos=tos,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IPv6_Traffic_Class_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_IPv6_Traffic_Class_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,traffic_class):
        
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip,traffic_class=traffic_class, packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip, traffic_class=traffic_class,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Traffic_Class_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,traffic_class):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, traffic_class=traffic_class,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_Traffic_Class_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,traffic_class):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip, traffic_class=traffic_class,packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip, traffic_class=traffic_class,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_Traffic_Class_Frames_and_Verify_NOT_Received(self,tx_port, rx_port, src_mac, dst_mac, vlan_id,  sip,  dip,  traffic_class):        
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip, traffic_class=traffic_class, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IPv6_Traffic_Class_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,
                                                                                  rx_priority,sip,dip,traffic_class):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, tx_priority, dip=dip, sip=sip, traffic_class=traffic_class, packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip, sip=sip,traffic_class=traffic_class, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_Traffic_Class_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,
                                                                                          traffic_class):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, priority, dip=dip, sip=sip, traffic_class=traffic_class,packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip, sip=sip, traffic_class=traffic_class,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Traffic_Class_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,
                                                                                    traffic_class):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, traffic_class=traffic_class,packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip, sip=sip, traffic_class=traffic_class,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Traffic_Class_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,traffic_class):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, traffic_class=traffic_class,packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, '0', dip=dip, sip=sip, traffic_class=traffic_class,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv6_Traffic_Class_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority ,rx_priority,
                                                                                           sip,dip,traffic_class):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, '0', tx_priority, dip=dip, sip=sip,traffic_class=traffic_class, packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip, sip=sip, traffic_class=traffic_class,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv6_Traffic_Class_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,
                                                                                                   traffic_class):
        self.tgenUdks.Create_IPv6_Packet('genericTx',dst_mac, src_mac,'0',priority, dip=dip, sip=sip, traffic_class=traffic_class, packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip, sip=sip, traffic_class=traffic_class, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IP_Proto_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_IP_Proto_Frames_and_Verify_Received(self,tx_port, rx_port, src_mac, dst_mac, vlan_id, sip, dip, proto):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip,proto=proto, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip, proto=proto,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IP_Proto_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,proto):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip,proto=proto, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IP_Proto_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,proto): 
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip,proto=proto, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip,proto=proto, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IP_Proto_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,proto):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip,  sip=sip,proto=proto, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IP_Proto_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,
                                                                        sip,dip,proto):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, tx_priority, dip=dip,  sip=sip,proto=proto, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip,  sip=sip, proto=proto,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IP_Proto_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,proto):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip, proto=proto, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip,proto=proto, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IP_Proto_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,proto):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, proto=proto, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip,  sip=sip,proto=proto, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IP_Proto_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,proto):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, proto=proto,packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, '0', dip=dip, sip=sip,proto=proto,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IP_Proto_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,
                                                                                 sip,dip,proto):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, '0', tx_priority, dip=dip, sip=sip,proto=proto, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip,  sip=sip, proto=proto, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IP_Proto_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,proto):
        self.tgenUdks.Create_IPv4_Packet('genericTx', dst_mac, src_mac, '0', priority, dip=dip,  sip=sip,proto=proto, packet_len='80')
        self.tgenUdks.Create_IPv4_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip, proto=proto,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # IPv6_Next_Header_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_Untagged_IPv6_Next_Header_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,next_header):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, next_header=next_header, packet_len='80')  
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip, next_header=next_header, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Next_Header_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,next_header):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, next_header=next_header, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    def Transmit_100_Tagged_IPv6_Next_Header_Frames_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,next_header):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip,next_header=next_header, packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip, next_header=next_header, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_Next_Header_Frames_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,sip,dip,next_header):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, dip=dip, sip=sip,next_header=next_header, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_Next_Header_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,
                                                                                sip,dip,next_header): 
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, tx_priority, dip=dip, sip=sip,next_header=next_header ,packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip, sip=sip, next_header=next_header,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Tagged_IPv6_Next_Header_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,
                                                                                        next_header):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, vlan_id, priority, dip=dip, sip=sip, next_header=next_header, packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip, sip=sip,next_header=next_header, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Next_Header_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,rx_priority,sip,dip,
                                                                                  next_header):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip,next_header=next_header, packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip, sip=sip, next_header=next_header,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_IPv6_Next_Header_Frames_and_Verify_Priority_Has_NOT_Changed(self, tx_port, rx_port, src_mac,  dst_mac, vlan_id, sip, dip, next_header): 
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, dip=dip,  sip=sip, next_header=next_header, packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, '0', dip=dip, sip=sip, next_header=next_header, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv6_Next_Header_Frames_and_Verify_Priority_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,tx_priority,rx_priority,
                                                                                         sip, dip, next_header):
        self.tgenUdks.Create_IPv6_Packet('genericTx', dst_mac, src_mac, '0', tx_priority, dip=dip, sip=sip,next_header=next_header, packet_len='80')
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, rx_priority, dip=dip, sip=sip,next_header=next_header, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Priority_Tagged_IPv6_Next_Header_Frames_and_Verify_Priority_Has_NOT_Changed(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,sip,dip,next_header):
        self.tgenUdks.Create_IPv6_Packet('genericTx',dst_mac,src_mac,'0', priority,dip=dip,sip=sip,next_header=next_header)
        self.tgenUdks.Create_IPv6_Packet('genericRx', dst_mac, src_mac, vlan_id, priority, dip=dip, sip=sip,next_header=next_header ,packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IPv4_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_IPv4_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,
                                                                 rx_prio_list,tx_tpid_list,rx_tpid_list,sip,dip):
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericTx',dst_mac, src_mac, tx_vlan_list, tx_prio_list, tx_tpid_list, dip=dip,  sip=sip)
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericRx',dst_mac, src_mac, rx_vlan_list, rx_prio_list, rx_tpid_list, dip=dip,  sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_QinQ_Untagged_IPv4_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,rx_vlan_list,rx_prio_list,
                                                                   rx_tpid_list,sip,dip):
        self.tgenUdks.Create_IPv4_Packet('genericTx',dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip)
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericRx',dst_mac, src_mac, rx_vlan_list, rx_prio_list, rx_tpid_list, dip=dip,  sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IPv6_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_IPv6_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,
                                                                 rx_prio_list,tx_tpid_list,rx_tpid_list,sip,dip):
        self.tgenUdks.Create_IPv4_Packet('genericTx',dst_mac, src_mac, tx_vlan_list, tx_prio_list, tx_tpid_list, dip=dip,  sip=sip)
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericRx',dst_mac, src_mac, rx_vlan_list, rx_prio_list, rx_tpid_list, dip=dip,  sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_QinQ_Untagged_IPv6_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,rx_vlan_list,rx_prio_list,
                                                                   rx_tpid_list,sip,dip):
        self.tgenUdks.Create_IPv6_Packet('genericTx',dst_mac, src_mac, vlan_id, priority, dip=dip,  sip=sip)
        self.tgenUdks.Create_IPv6_VLAN_Stack_Packet('genericRx',dst_mac, src_mac, rx_vlan_list, rx_prio_list, rx_tpid_list, dip=dip,  sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IPX_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_IPX_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,
                                                                rx_prio_list,tx_tpid_list,rx_tpid_list,  ether_type):
        self.tgenUdks.Create_Ethernet2_VLAN_Stack_Packet('genericTx',dst_mac, src_mac, tx_vlan_list, tx_prio_list, tx_tpid_list, ether_type=ether_type)
        self.tgenUdks.Create_Ethernet2_VLAN_Stack_Packet('genericRx',dst_mac, src_mac, tx_vlan_list, tx_prio_list, tx_tpid_list, ether_type=ether_type)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_QinQ_Untagged_IPX_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,vlan_list,prio_list,tpid_list,ether_type):
        self.tgenUdks.Create_Ethernet2_Packet('genericTx',dst_mac, src_mac, vlan_id, priority,  ether_type=ether_type)
        self.tgenUdks.Create_Ethernet2_VLAN_Stack_Packet('genericRx',dst_mac, src_mac, vlan_list, prio_list, tpid_list, ether_type=ether_type)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IP_TCP_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_TCP_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,
                                                                rx_prio_list,tx_tpid_list,rx_tpid_list,sip,dip,src_port,dst_port): 
        self.tgenUdks.IPv4_VLAN_Stack_TCP_Packet('genericTx',dst_mac,src_mac,tx_vlan_list,tx_prio_list,tx_tpid_list,dip=dip,sip=sip,src_port=src_port,
                                                 dst_port=dst_port)
        self.tgenUdks.IPv4_VLAN_Stack_TCP_Packet('genericRx',dst_mac,src_mac,rx_vlan_list,rx_prio_list,rx_tpid_list,dip=dip,sip=sip,src_port=src_port,
                                                 dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_QinQ_Untagged_TCP_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,vlan_list,prio_list,
                                                                  tpid_list,sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv4_TCP_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv4_VLAN_Stack_TCP_Packet('genericRx',dst_mac,src_mac,vlan_list,prio_list,tpid_list,dip=dip,sip=sip,src_port=src_port,
                                                        dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IP_UDP_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_UDP_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,
                                                                rx_prio_list,tx_tpid_list,rx_tpid_list,sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv4_VLAN_Stack_UDP_Packet('genericTx',dst_mac,src_mac,tx_vlan_list,tx_prio_list,tx_tpid_list,dip=dip,sip=sip,
                                                        src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Create_IPv4_VLAN_Stack_UDP_Packet('genericRx',dst_mac,src_mac,rx_vlan_list,rx_prio_list,rx_tpid_list,dip=dip,sip=sip,
                                                        src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_QinQ_Untagged_UDP_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,vlan_list,prio_list,
                                                                  tpid_list,sip,dip,src_port,dst_port):
        
        self.tgenUdks.Create_IPv4_UDP_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,src_port=src_port, dst_port=dst_port)
        self.tgenUdks.Create_IPv4_VLAN_Stack_UDP_Packet('genericRx',dst_mac,src_mac,vlan_list,prio_list,tpid_list,dip=dip,sip=sip,src_port=src_port,
                                                        dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IPv6_TCP_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_IPv6_TCP_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,
                                                                     rx_prio_list,tx_tpid_list,rx_tpid_list,sip,dip,src_port,dst_port):
        
        self.tgenUdks.Create_IPv6_VLAN_Stack_TCP_Packet('genericTx',dst_mac,src_mac,tx_vlan_list,tx_prio_list,tx_tpid_list,dip=dip,
                                                        sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_VLAN_Stack_TCP_Packet('genericRx',dst_mac,src_mac,rx_vlan_list,rx_prio_list,rx_tpid_list,dip=dip,
                                                        sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_QinQ_Untagged_IPv6_TCP_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,vlan_list,prio_list,
                                                                       tpid_list,sip,dip,src_port,dst_port): 
        self.tgenUdks.Create_IPv6_TCP_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,src_port=src_port,
                                             dst_port=dst_port)
        self.tgenUdks.Create_IPv6_VLAN_Stack_TCP_Packet('genericRx',dst_mac,src_mac,vlan_list,prio_list,tpid_list,dip=dip,sip=sip,
                                                        src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IPv6_UDP_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_IPv6_UDP_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,rx_prio_list,
                                                                     tx_tpid_list,rx_tpid_list,sip,dip,src_port,dst_port):
        
        self.tgenUdks.Create_IPv6_VLAN_Stack_UDP_Packet('genericTx',dst_mac,src_mac,tx_vlan_list,tx_prio_list,tx_tpid_list,dip=dip,sip=sip,
                                                        src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_VLAN_Stack_UDP_Packet('genericRx',dst_mac,src_mac,rx_vlan_list,rx_prio_list,rx_tpid_list,dip=dip,sip=sip,
                                                        src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_QinQ_Untagged_IPv6_UDP_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,vlan_list,prio_list,tpid_list,
                                                                       sip,dip,src_port,dst_port):
        self.tgenUdks.Create_IPv6_VLAN_Stack_UDP_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,src_port=src_port,dst_port=dst_port)
        self.tgenUdks.Create_IPv6_VLAN_Stack_UDP_Packet('genericRx',dst_mac,src_mac,vlan_list,prio_list,tpid_list,dip=dip,sip=sip,src_port=src_port,
                                                        dst_port=dst_port)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IP_Fragment_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_IP_Frag_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,
                                                                    rx_prio_list,tx_tpid_list,rx_tpid_list,sip,dip,id,flags,offset):
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericTx',dst_mac,src_mac,tx_vlan_list,tx_prio_list,tx_tpid_list,dip=dip,sip=sip,id=id,flags=flags,frag_offset=offset)
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericRx',dst_mac,src_mac,rx_vlan_list,rx_prio_list,rx_tpid_list,dip=dip,sip=sip,id=id,flags=flags,frag_offset=offset)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_QinQ_Untagged_IP_Frag_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,vlan_list,prio_list,tpid_list,sip,
                                                                      dip,id,flags,offset):
        self.tgenUdks.Create_IPv4_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,id=id,flags=flags,frag_offset=offset)
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericRx',dst_mac,src_mac,vlan_list,prio_list,tpid_list,dip=dip,sip=sip,id=id,flags=flags,frag_offset=offset)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IPv6_Fragment_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_IPv6_Frag_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,rx_prio_list,
                                                                      tx_tpid_list,rx_tpid_list,sip,dip):
        self.tgenUdks.Create_IPv6_VLAN_Stack_Fragment_Packet('genericTx',dst_mac,src_mac,tx_vlan_list,tx_prio_list,tx_tpid_list,dip=dip,sip=sip)
        self.tgenUdks.Create_IPv6_VLAN_Stack_Fragment_Packet('genericRx',dst_mac,src_mac,rx_vlan_list,rx_prio_list,rx_tpid_list,dip=dip,sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_QinQ_Untagged_IPv6_Frag_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,vlan_list,prio_list,tpid_list,sip,dip):
        self.tgenUdks.Create_IPv6_Fragment_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip)
        self.tgenUdks.Create_IPv6_VLAN_Stack_Fragment_Packet('genericRx',dst_mac,src_mac,vlan_list,prio_list,tpid_list,dip=dip,sip=sip)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IP_TTL_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_IP_TTL_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,rx_prio_list,
                                                                   tx_tpid_list,rx_tpid_list,sip,dip,ttl):
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericTx',dst_mac,src_mac,tx_vlan_list,tx_prio_list,tx_tpid_list,dip=dip,sip=sip,ttl=ttl)
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericRx',dst_mac,src_mac,rx_vlan_list,rx_prio_list,rx_tpid_list,dip=dip,sip=sip,ttl=ttl)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_QinQ_Untagged_IP_TTL_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,vlan_list,prio_list,tpid_list,
                                                                     sip,dip,ttl):
        self.tgenUdks.Create_IPv4_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,ttl=ttl)
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericRx',dst_mac,src_mac,vlan_list,prio_list,tpid_list,dip=dip,sip=sip,ttl=ttl)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IPv6_TTL_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_IPv6_Hop_Limit_Frames_and_Verify_Priority(self, tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,rx_prio_list,
                                                                           tx_tpid_list,rx_tpid_list,sip,dip,ttl):
        self.tgenUdks.Create_IPv6_VLAN_Stack_Packet('genericTx',dst_mac,src_mac,tx_vlan_list,tx_prio_list,tx_tpid_list,dip=dip,sip=sip,hop_limit=ttl)
        self.tgenUdks.Create_IPv6_VLAN_Stack_Packet('genericRx',dst_mac,src_mac,rx_vlan_list,rx_prio_list,rx_tpid_list,dip=dip,sip=sip,hop_limit=ttl)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_QinQ_Untagged_IPv6_Hop_Limit_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,vlan_list,prio_list,
                                                                             tpid_list,sip,dip,ttl):
        self.tgenUdks.Create_IPv6_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,hop_limit=ttl)
        self.tgenUdks.Create_IPv6_VLAN_Stack_Packet('genericRx',dst_mac,src_mac,vlan_list,prio_list,tpid_list,dip=dip,sip=sip,hop_limit=ttl)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IP_ToS_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_IP_ToS_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,rx_prio_list,
                                                                   tx_tpid_list,rx_tpid_list,sip,dip,tos):
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericTx',dst_mac,src_mac,tx_vlan_list,tx_prio_list,tx_tpid_list,dip=dip,sip=sip,tos=tos)
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericRx',dst_mac,src_mac,rx_vlan_list,rx_prio_list,rx_tpid_list,dip=dip,sip=sip,tos=tos)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_QinQ_Untagged_IP_ToS_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,vlan_list,prio_list,tpid_list,
                                                                     sip,dip,tos):
        self.tgenUdks.Create_IPv4_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,tos=tos)
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericRx',dst_mac,src_mac,vlan_list,prio_list,tpid_list,dip=dip,sip=sip,tos=tos)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IPv6_Traffic_Class_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_IPv6_Traffic_Class_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,
                                                                               rx_prio_list,tx_tpid_list,rx_tpid_list,sip,dip,traffic_class):
        self.tgenUdks.IPv6_VLAN_Stack_Packet('genericTx',dst_mac,src_mac,tx_vlan_list,tx_prio_list,tx_tpid_list,dip=dip,sip=sip,traffic_class=traffic_class)
        self.tgenUdks.IPv6_VLAN_Stack_Packet('genericRx',dst_mac,src_mac,rx_vlan_list,rx_prio_list,rx_tpid_list,dip=dip,sip=sip,traffic_class=traffic_class)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_QinQ_Untagged_IPv6_Traffic_Class_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,vlan_list,prio_list,
                                                                                 tpid_list,sip,dip,traffic_class):
        self.tgenUdks.Create_IPv6_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,traffic_class=traffic_class)
        self.tgenUdks.Create_IPv6_VLAN_Stack_Packet('genericRx',dst_mac,src_mac,vlan_list,prio_list,tpid_list,dip=dip,sip=sip,traffic_class=traffic_class)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IP_Proto_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_IP_Proto_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,rx_prio_list,tx_tpid_list,
                                                                     rx_tpid_list,sip,dip,proto):
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericTx',dst_mac,src_mac,tx_vlan_list,tx_prio_list,tx_tpid_list,dip=dip,sip=sip,proto=proto)
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericRx',dst_mac,src_mac,rx_vlan_list,rx_prio_list,rx_tpid_list,dip=dip,sip=sip,proto=proto)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_QinQ_Untagged_IP_Proto_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,vlan_list,prio_list,tpid_list,
                                                                       sip,dip,proto):
        self.tgenUdks.Create_IPv4_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,proto=proto)
        self.tgenUdks.Create_IPv4_VLAN_Stack_Packet('genericRx',dst_mac,src_mac,vlan_list,prio_list,tpid_list,dip=dip,sip=sip,proto=proto)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    # ---------------------------------------------------------------------------------------------------------------------
    # QinQ_IPv6_Next_Header_Traffic_UDKs
    # ---------------------------------------------------------------------------------------------------------------------
    
    def Transmit_100_QinQ_Tagged_IPv6_Next_Header_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,tx_vlan_list,rx_vlan_list,tx_prio_list,
                                                                             rx_prio_list,tx_tpid_list,rx_tpid_list,sip,dip,next_header):
        self.tgenUdks.Create_IPv6_VLAN_Stack_Packet('genericTx',dst_mac,src_mac,tx_vlan_list,tx_prio_list,tx_tpid_list,dip=dip,sip=sip,next_header=next_header)
        self.tgenUdks.Create_IPv6_VLAN_Stack_Packet('genericRx',dst_mac,src_mac,rx_vlan_list,rx_prio_list,rx_tpid_list,dip=dip,sip=sip,next_header=next_header)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port)
    
    def Transmit_100_QinQ_Untagged_IPv6_Next_Header_Frames_and_Verify_Priority(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,priority,vlan_list,prio_list,
                                                                               tpid_list,sip,dip,next_header):
        self.tgenUdks.Create_IPv6_VLAN_Stack_Packet('genericTx',dst_mac,src_mac,vlan_id,priority,dip=dip,sip=sip,next_header=next_header)
        self.tgenUdks.Create_IPv6_VLAN_Stack_Packet('genericRx',dst_mac,src_mac,vlan_list,prio_list,tpid_list,dip=dip,sip=sip,next_header=next_header)
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_Frames_with_ethertype_and_Verify_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,ether_type): 
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, ether_type=ether_type, packet_len='80')
        self.tgenUdks.Create_Ethernet2_Packet('genericRx', dst_mac, src_mac, vlan_id, ether_type=ether_type, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_Received(tx_port, rx_port,dst_mac,src_mac)
    
    def Transmit_100_Untagged_Frames_with_ethertype_and_Verify_NOT_Received(self,tx_port,rx_port,src_mac,dst_mac,vlan_id,ether_type):
        
        self.tgenUdks.Create_Ethernet2_Packet('genericTx', dst_mac, src_mac, ether_type=ether_type, packet_len='80')
        self.tgenUdks.Start_Capture_with_DMAC_Filter(rx_port, dst_mac)
        self.Transmit_and_Verify_Frames_NOT_Received(tx_port, rx_port)
    
    #
    #  Policy_Access-List_mode_UDK's
    #
    def Create_And_Verify_Basic_Single_Match_Access_List_Entries(self,createEntry='false'):
        #
        #  Test_each_individual_rule_type_with_varying_actions....  FULL_MASK_VALUES
        #
        print('Create and Check Fully masked single match Access-List entries.')
        
        if createEntry == 'true':
            cos_string = 'cos ' + self.pytestConfigHelper.config.cos_5 + ' mirror-destination 1 forward'
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,'IpV4','icmptype','icmptype 4.4',cos_string)
        self.networkElementPolicyGenKeywords.policy_verify_acl_icmptype(self.pytestConfigHelper.dut1.name,'IpV4','icmptype', '4.4','16')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4','icmptype','NV','', 'fwrd', self.pytestConfigHelper.config.cos_5,'1')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,'IpV4','ether','ether 0x0888','forward')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ether(self.pytestConfigHelper.dut1.name,'IpV4','ether','0x888', '16')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4','ether','NV', '', 'fwrd','','')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,'IpV4','icmp6type','icmp6type de-ad mask 16','drop')
        self.networkElementPolicyGenKeywords.policy_verify_acl_icmp6type(self.pytestConfigHelper.dut1.name,'IpV4', 'icmp6type', '222.173', '16')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, 'IpV4','icmp6type', 'NV', '', 'drop','','')
            
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,'IpV4', 'ipdestsocket', 'ipdestsocket ' + self.pytestConfigHelper.config.dst_ip_a+':' + self.pytestConfigHelper.config.l4_port_c + ' mask 48','forward syslog')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipdestsocket(self.pytestConfigHelper.dut1.name, 'IpV4','ipdestsocket', self.pytestConfigHelper.config.dst_ip_a+':' + self.pytestConfigHelper.config.l4_port_c, '48')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4','ipdestsocket','NV','S','fwrd','','')
            
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4', 'ipfrag', 'ipfrag', 'drop')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipfrag(self.pytestConfigHelper.dut1.name, 'IpV4','ipfrag')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, 'IpV4','ipfrag','NV','','drop', ''  '')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4', 'ipproto', 'ipproto 255', 'forward cos ' + self.pytestConfigHelper.config.cos_5)
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipproto(self.pytestConfigHelper.dut1.name,'IpV4','ipproto','255','8')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, 'IpV4','ipproto','NV','','fwrd',self.pytestConfigHelper.config.cos_5,'')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4','ipsourcesocket', 'ipsourcesocket ' + self.pytestConfigHelper.config.dst_ip_a+':' + self.pytestConfigHelper.config.l4_port_c, 'drop cos ' + self.pytestConfigHelper.config.cos_5)
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipsourcesocket(self.pytestConfigHelper.dut1.name, 'IpV4','ipsourcesocket', self.pytestConfigHelper.config.dst_ip_a+':' + self.pytestConfigHelper.config.l4_port_c,'48')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4','ipsourcesocket','NV','','drop',self.pytestConfigHelper.config.cos_5,'')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4','iptos', 'iptos 255','forward cos ' + self.pytestConfigHelper.config.cos_5 + ' mirror-destination 1')
        self.networkElementPolicyGenKeywords.policy_verify_acl_iptos(self.pytestConfigHelper.dut1.name, 'IpV4','iptos','255','8')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4','iptos','NV','','fwrd',self.pytestConfigHelper.config.cos_5,'1')
      
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4','ipttl', 'ipttl 255','forward cos ' + self.pytestConfigHelper.config.cos_5 + ' mirror-destination 1')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipttl(self.pytestConfigHelper.dut1.name, 'IpV4','ipttl','255','8')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4','ipttl','NV','','fwrd',self.pytestConfigHelper.config.cos_5,'1')
      
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4','tcpdestportIP', 
                                                                        'tcpdestportIP ' + self.pytestConfigHelper.config.l4_port_c + ':' + self.pytestConfigHelper.config.dst_ip_a,'drop  mirror-destination 1')
        self.networkElementPolicyGenKeywords.policy_verify_acl_tcpdestportip(self.pytestConfigHelper.dut1.name, 'IpV4','tcpdestportIP', self.pytestConfigHelper.config.l4_port_c + ':' + self.pytestConfigHelper.config.dst_ip_a,'48')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4','tcpdestportIP','NV','','drop','','1')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4','tcpsourceportIP', 
                                                                        'tcpsourceportIP ' + self.pytestConfigHelper.config.l4_port_a + ':' + self.pytestConfigHelper.config.dst_ip_b,'forward cos ' + self.pytestConfigHelper.config.cos_5)
        self.networkElementPolicyGenKeywords.policy_verify_acl_tcpsourceportip(self.pytestConfigHelper.dut1.name, 'IpV4','tcpsourceportIP', self.pytestConfigHelper.config.l4_port_a + ':' + self.pytestConfigHelper.config.dst_ip_b,'48')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4','tcpsourceportIP','NV','','fwrd',self.pytestConfigHelper.config.cos_5,'')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4','udpdestportIP', 
                                                                        'udpdestportIP ' + self.pytestConfigHelper.config.l4_port_c + ':' + self.pytestConfigHelper.config.dst_ip_a,'forward cos ' + self.pytestConfigHelper.config.cos_5)
        self.networkElementPolicyGenKeywords.policy_verify_acl_udpdestportip(self.pytestConfigHelper.dut1.name, 'IpV4','udpdestportIP', self.pytestConfigHelper.config.l4_port_c + ':' +self.pytestConfigHelper.config.dst_ip_a,'48')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4','udpdestportIP','NV','','fwrd',self.pytestConfigHelper.config.cos_5,'')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4','udpsourceportIP', 
                                                                        'udpsourceportIP ' + self.pytestConfigHelper.config.l4_port_b + ':' + self.pytestConfigHelper.config.dst_ip_c,'forward cos ' + self.pytestConfigHelper.config.cos_5)
        self.networkElementPolicyGenKeywords.policy_verify_acl_udpsourceportip(self.pytestConfigHelper.dut1.name, 'IpV4','udpsourceportIP', self.pytestConfigHelper.config.l4_port_b + ':' + self.pytestConfigHelper.config.dst_ip_c,'48')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4','udpsourceportIP','NV','','fwrd',self.pytestConfigHelper.config.cos_5,'')
        #
        #  PARTIAL_MASK_VALUES
        #
        #Log_Create_and_Check_Partial_mask_single_match_Access-List_entries.
        print(' Log_Create_and_Check_Partial_mask_single_match_Access-List_entries.')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,'IpV4a','icmptype','icmptype 6.1 mask 8','cos ' + self.pytestConfigHelper.config.cos_5 + ' mirror-destination 1 forward')
        self.networkElementPolicyGenKeywords.policy_verify_acl_icmptype(self.pytestConfigHelper.dut1.name,'IpV4a','icmptype', '6.0','8')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4a','icmptype','NV','', 'fwrd', self.pytestConfigHelper.config.cos_5,'1')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,'IpV4a','ether','ether 0x0888 mask 8','forward')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ether(self.pytestConfigHelper.dut1.name,'IpV4a','ether','0x800', '8')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4a','ether','NV', '', 'fwrd','','')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,'IpV4a','icmp6type','icmp6type de-ad mask 8','drop')
        self.networkElementPolicyGenKeywords.policy_verify_acl_icmp6type(self.pytestConfigHelper.dut1.name,'IpV4a', 'icmp6type', '222.0', '8')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, 'IpV4a','icmp6type', 'NV', '', 'drop','','')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,'IpV4a', 'ipdestsocket', 'ipdestsocket ' + self.pytestConfigHelper.config.dst_ip_a+':' + self.pytestConfigHelper.config.l4_port_c + ' mask 32','forward syslog')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipdestsocket(self.pytestConfigHelper.dut1.name, 'IpV4a','ipdestsocket', self.pytestConfigHelper.config.dst_ip_a,'32')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4a','ipdestsocket','NV','S', 'fwrd','','')
        #
        #
        #  Note: ipfrag_cannot_be_masked...
        #
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4a', 'ipproto', 'ipproto 0xAB mask 4', 'forward cos ' + self.pytestConfigHelper.config.cos_5)
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipproto(self.pytestConfigHelper.dut1.name,'IpV4a','ipproto','0xa0','4')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, 'IpV4a','ipproto','NV','','fwrd',self.pytestConfigHelper.config.cos_5,'')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4a','ipsourcesocket', 'ipsourcesocket ' + self.pytestConfigHelper.config.dst_ip_a+':' + self.pytestConfigHelper.config.l4_port_c +' mask 32', 'drop cos ' + self.pytestConfigHelper.config.cos_5)
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipsourcesocket(self.pytestConfigHelper.dut1.name, 'IpV4a','ipsourcesocket', self.pytestConfigHelper.config.dst_ip_a,'32')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4a','ipsourcesocket','NV','','drop',self.pytestConfigHelper.config.cos_5,'')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4a','iptos', 'iptos 0xFA mask 6', 'forward cos ' + self.pytestConfigHelper.config.cos_5 + ' mirror-destination 1')
        self.networkElementPolicyGenKeywords.policy_verify_acl_iptos(self.pytestConfigHelper.dut1.name, 'IpV4a','iptos','0xf8','6')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4a','iptos','NV','','fwrd',self.pytestConfigHelper.config.cos_5,'1')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4a','ipttl', 'ipttl 0xAA mask 6','forward cos ' + self.pytestConfigHelper.config.cos_5 + ' mirror-destination 1')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipttl(self.pytestConfigHelper.dut1.name, 'IpV4a','ipttl','0xa8','6')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4a','ipttl','NV','','fwrd',self.pytestConfigHelper.config.cos_5,'1')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4a','tcpdestportIP', 
                                                                        'tcpdestportIP ' + self.pytestConfigHelper.config.l4_port_c + ':' + self.pytestConfigHelper.config.dst_ip_a + ' mask 16','drop  mirror-destination 1')
        self.networkElementPolicyGenKeywords.policy_verify_acl_tcpdestportip(self.pytestConfigHelper.dut1.name, 'IpV4a','tcpdestportIP ', self.pytestConfigHelper.config.l4_port_c,'16')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4a','tcpdestportIP','NV','','drop','','1')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4a','tcpsourceportIP', 
                                                                        'tcpsourceportIP ' + self.pytestConfigHelper.config.l4_port_a + ':' + self.pytestConfigHelper.config.dst_ip_b + ' mask 16','forward cos ' + self.pytestConfigHelper.config.cos_5)
        self.networkElementPolicyGenKeywords.policy_verify_acl_tcpsourceportip(self.pytestConfigHelper.dut1.name, 'IpV4a','tcpsourceportIP ', self.pytestConfigHelper.config.l4_port_a,'16')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4a','tcpsourceportIP','NV','','fwrd',self.pytestConfigHelper.config.cos_5,'')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4a','udpdestportIP', 
                                                                        'udpdestportIP ' + self.pytestConfigHelper.config.l4_port_c + ':' + self.pytestConfigHelper.config.dst_ip_a + ' mask 16','forward cos ' + self.pytestConfigHelper.config.cos_5)
        self.networkElementPolicyGenKeywords.policy_verify_acl_udpdestportip(self.pytestConfigHelper.dut1.name, 'IpV4a','udpdestportIP ', self.pytestConfigHelper.config.l4_port_c, '16')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4a','udpdestportIP','NV','','fwrd',self.pytestConfigHelper.config.cos_5,'')
        
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'IpV4a','udpsourceportIP', 
                                                                        'udpsourceportIP ' + self.pytestConfigHelper.config.l4_port_b + ':' +self.pytestConfigHelper.config.dst_ip_c + ' mask 16','forward cos ' + self.pytestConfigHelper.config.cos_5)
        self.networkElementPolicyGenKeywords.policy_verify_acl_udpsourceportip(self.pytestConfigHelper.dut1.name, 'IpV4a','udpsourceportIP ', self.pytestConfigHelper.config.l4_port_b,'16')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'IpV4a','udpsourceportIP','NV','','fwrd',self.pytestConfigHelper.config.cos_5,'')
    #  Policy_Access-List_mode_UDK's
    #
    def Create_And_Verify_Separate_List_Single_Match_Access_List_Entries(self,createEntry='false', ForwardOrDrop='drop',   FwrdOrDrop='drop'):
         #
         #  Test_each_individual_rule_type_with_varying_actions....  FULL_MASK_VALUES
         #
         #  If_there_is_a "COS" action, we_cannot_add_drop_to_it_so_it_is_a_bit_convoluted_here...
         #
         #
        print('Log_Create_and_Check_Fully_masked_single_match_Access-List_entries.')
        print('Log_COS_values_are_NOT_checked_explicitly_as_they_are_not_present_in_drop_rules.')
        cos_5_string = self.pytestConfigHelper.config.cos_5
        dst_ip_a_string = self.pytestConfigHelper.config.dst_ip_a
        src_ip_a_string = self.pytestConfigHelper.config.src_ip_a
        str_l4_port_c = self.pytestConfigHelper.config.l4_port_c
        str_l4_port_a = self.pytestConfigHelper.config.l4_port_a
    #
    #  icmp
    #
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,  FwrdOrDrop + 'icmptype','icmptype','icmptype 8.0', 'cos ' + cos_5_string + ' mirror-destination 1')
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
             self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,  FwrdOrDrop + 'icmptype','icmptype','icmptype 8.0', ForwardOrDrop + ' mirror-destination 1')
        self.networkElementPolicyGenKeywords.policy_verify_acl_icmptype(self.pytestConfigHelper.dut1.name,  FwrdOrDrop + 'icmptype', 'icmptype','8.0', '16')
         
        if createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop + 'icmptype', 'icmptype', 'NV', '', '', cos_5_string, '1')
            
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
             self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop + 'icmptype', 'icmptype', 'NV', '', FwrdOrDrop, '', '1')
    #
    #  ethertype
    #
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop + 'ether', 'ether', 'ether 0x0800',  ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_ether(self.pytestConfigHelper.dut1.name, FwrdOrDrop+ 'ether', 'ether', '0x800','16')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+ 'ether', 'ether', 'NV', '', FwrdOrDrop, '', '')
    #
    #  icmpV6
    #
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'icmp6type', 'icmp6type','icmp6type de-ad mask 16', 'cos ' + cos_5_string)
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'icmp6type','icmp6type','icmp6type de-ad mask 16', ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_icmp6type(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'icmp6type','icmp6type','222.173','16')
    
        if createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'icmp6type','icmp6type', 'NV', '', '', cos_5_string, '')
        if createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'icmp6type','icmp6type','NV','',FwrdOrDrop,'','')
    #
    #  ipdestsocket
    #
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop + 'ipdestsocket','ipdestsocket', 'ipdestsocket ' + dst_ip_a_string + ':' + str_l4_port_c + ' mask 48',   ForwardOrDrop + ' syslog')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipdestsocket(self.pytestConfigHelper.dut1.name, FwrdOrDrop + 'ipdestsocket', 'ipdestsocket', dst_ip_a_string + ':' + str_l4_port_c, '48')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, FwrdOrDrop + 'ipdestsocket', 'ipdestsocket','NV','S', FwrdOrDrop, '', '')
    #
    #  ipfrag
    #
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'ipfrag','ipfrag','ipfrag', ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipfrag(self.pytestConfigHelper.dut1.name,  FwrdOrDrop + 'ipfrag', 'ipfrag')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, FwrdOrDrop + 'ipfrag','ipfrag','NV','', FwrdOrDrop, '', '')
    #
    #  ipproto
    #
        if createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop + 'ipproto', 'ipproto','ipproto 17', 'cos ' + cos_5_string)
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop + 'ipproto','ipproto','ipproto 17',ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipproto(self.pytestConfigHelper.dut1.name, FwrdOrDrop + 'ipproto','ipproto ','17','8')
    
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, FwrdOrDrop + 'ipproto', 'ipproto', 'NV', '', '', cos_5_string, '')
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords. policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop + 'ipproto', 'ipproto', 'NV', '', FwrdOrDrop, '',  '')
    #
    #  ipsourcesocket
    #
        if createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,FwrdOrDrop + 'ipSsock','ipSsock',
                                                                           'ipsourcesocket ' +  src_ip_a_string + ':' + str_l4_port_a, 'cos '+ cos_5_string )
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop + 'ipSsock','ipSsock','ipsourcesocket ' +  src_ip_a_string + ':' + str_l4_port_a, ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipsourcesocket(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'ipSsock','ipSsock', src_ip_a_string + ':' + str_l4_port_a,'48')
    
        if createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,FwrdOrDrop+'ipSsock',
                                                                              'ipSsock','NV', '', '' ,cos_5_string,'')
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,FwrdOrDrop + 'ipSsock', 'ipSsock', 'NV', '',
                                                                              FwrdOrDrop, '', '')
    #
    #  iptos
    #
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,FwrdOrDrop + 'iptos','iptos','iptos 31', 'cos ' + cos_5_string + ' mirror-destination 1')
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop + 'iptos','iptos','iptos 31', ForwardOrDrop + ' mirror-destination 1')
        self.networkElementPolicyGenKeywords.policy_verify_acl_iptos(self.pytestConfigHelper.dut1.name, FwrdOrDrop + 'iptos','iptos',' 31','8')
    
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,FwrdOrDrop +'iptos','iptos', 'NV','','',cos_5_string, '1')
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, FwrdOrDrop + 'iptos','iptos','NV','',FwrdOrDrop,'', '1')
    #
    #  ipttl
    #
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'ipttl','ipttl','ipttl 10','mirror-destination 1 ' + ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipttl(self.pytestConfigHelper.dut1.name,  FwrdOrDrop + 'ipttl', 'ipttl',' 10','8')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,FwrdOrDrop +'ipttl','ipttl', 'NV', '', FwrdOrDrop, '', '1')
    #
    #  tcpdestportip
    #
        if  createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'tcpDportIP','tcpDportIP','tcpdestportip ' + str_l4_port_c+':'+dst_ip_a_string, ForwardOrDrop + ' mirror-destination 1')
        self.networkElementPolicyGenKeywords.policy_verify_acl_tcpdestportip(self.pytestConfigHelper.dut1.name, FwrdOrDrop + 'tcpDportIP', 'tcpDportIP ' ,  str_l4_port_c+':'+dst_ip_a_string,  '48')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'tcpDportIP','tcpDportIP','NV', '', FwrdOrDrop, '', '1')
    #
    #  tcpsourceportip
    #
        if createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'tcpSportIP','tcpSportIP', 'tcpsourceportip ' + str_l4_port_a+':'+src_ip_a_string, 'cos ' + cos_5_string)
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'tcpSportIP', 'tcpSportIP','tcpsourceportip  ' + str_l4_port_a+':'+src_ip_a_string, ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_tcpsourceportip(self.pytestConfigHelper.dut1.name, FwrdOrDrop +'tcpSportIP','tcpSportIP' , str_l4_port_a+':'+src_ip_a_string,'48')
    
        if createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,FwrdOrDrop +'tcpSportIP','tcpSportIP','NV', '', '', cos_5_string, '')
        if createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'tcpSportIP','tcpSportIP','NV','',FwrdOrDrop,'','')
    #
    #  udpdestportup
    #
        if createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'udpDportIP','udpDportIP','udpdestportip ' + str_l4_port_c+':'+dst_ip_a_string,'cos  ' + cos_5_string)
        if createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'udpDportIP','udpDportIP','udpdestportip ' + str_l4_port_c+':'+dst_ip_a_string,ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_udpdestportip(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'udpDportIP','udpDportIP', str_l4_port_c+':'+dst_ip_a_string,'48')
    
        if createEntry == 'true' and FwrdOrDrop == 'fwrd':
           self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'udpDportIP','udpDportIP','NV','','', cos_5_string,'')
        if createEntry == 'true' and FwrdOrDrop == 'drop':
           self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'udpDportIP','udpDportIP','NV','',FwrdOrDrop,'','')
    #
    #  udpsourceportup
    #
        if createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'udpSportIP','udpSportIP','udpsourceportip ' + str_l4_port_a + ':' + src_ip_a_string,ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_udpsourceportip( self.pytestConfigHelper.dut1.name, FwrdOrDrop+'udpSportIP','udpSportIP', str_l4_port_a + ':' + src_ip_a_string, '48')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'udpSportIP','udpSportIP','NV','', FwrdOrDrop,'','')
    #
            # ===================================================================================================
            #  PARTIAL_MASK_VALUES
            # ===================================================================================================
    #
        print('Log_Create_and_Check_Partial_mask_single_match_Access-List_entries.')
    #
    #  icmp
    #
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,FwrdOrDrop+'p_icmptype','icmptype','icmptype 8.1 mask 8', 'cos ' + cos_5_string + ' mirror-destination 1')
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,FwrdOrDrop+'p_icmptype','icmptype','icmptype 8.1 mask 8', ForwardOrDrop+' mirror-destination 1')
        self.networkElementPolicyGenKeywords.policy_verify_acl_icmptype(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_icmptype','icmptype', '8.0','8')
    
        if createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,FwrdOrDrop+'p_icmptype','icmptype','NV','','', cos_5_string,'1')
        if createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,FwrdOrDrop+'p_icmptype','icmptype','NV','',FwrdOrDrop,'','1')
    #
    #  ethertype
    #
        if  createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,FwrdOrDrop+'p_ether','ether','ether 0x0888 mask 8',ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_ether(self.pytestConfigHelper.dut1.name,FwrdOrDrop+'p_ether','ether','0x800','8')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,FwrdOrDrop+'p_ether','ether','NV','',FwrdOrDrop,'','')
    #
    #  icmpV6
    #
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_icmp6type','icmp6type','icmp6type de-ad mask 8', 'cos ' + cos_5_string )
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
                self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,FwrdOrDrop+'p_icmp6type','icmp6type','icmp6type de-ad mask 8', ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_icmp6type(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_icmp6type','icmp6type', '222.0','8')
    
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
                self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'p_icmp6type','icmp6type','NV', '', '', cos_5_string, '')
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_icmp6type','icmp6type','NV',  '', FwrdOrDrop,  '', '')
    #
    #  ipdestsocket
    #
        if  createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_ipDsock','ipDsock','ipdestsocket ' + dst_ip_a_string+':'+str_l4_port_c + ' mask 32', ForwardOrDrop + ' syslog')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipdestsocket(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_ipDsock','ipDsock',dst_ip_a_string, '32')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_ipDsock','ipDsock','NV','S',FwrdOrDrop, '',  '')
    #
    #  Note: ipfrag_cannot_be_masked...
    #
    #
    #  ipproto
    #
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_ipproto','ipproto','ipproto 17 mask 4','cos '+cos_5_string)
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_ipproto','ipproto','ipproto 17 mask 4', ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipproto(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_ipproto','ipproto','16','4')
    
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'p_ipproto','ipproto','NV','','', cos_5_string, '')
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_ipproto','ipproto', 'NV', '', FwrdOrDrop, '', '')
    #
    #  ipsourcesocket
    #
    
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,FwrdOrDrop +'p_ipSsock','ipSsock', 'ipsourcesocket '+ src_ip_a_string + ':' + str_l4_port_a + ' mask 32','cos ' + cos_5_string)
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_ipSsock','ipSsock', 'ipsourcesocket ' + src_ip_a_string + ':' + str_l4_port_a + ' mask 32',ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipsourcesocket(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_ipSsock','ipSsock', src_ip_a_string,'32')
    
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'ipSsock','ipSsock','NV','','',cos_5_string, '')
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'ipSsock', 'ipSsock', 'NV', '', FwrdOrDrop, '', '')
    #
    #  iptos
    #
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_iptos','iptos','iptos 31 mask 6','cos ' +cos_5_string +' mirror-destination 1')
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,  FwrdOrDrop + 'p_iptos', 'iptos','iptos 31 mask 6',ForwardOrDrop + ' mirror-destination 1')
        self.networkElementPolicyGenKeywords.policy_verify_acl_iptos(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'p_iptos','iptos', '0x1c', '6')
    
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'iptos', 'iptos','NV','','',cos_5_string,'1')
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,FwrdOrDrop+'iptos','iptos','NV','',FwrdOrDrop,'','1')
    #
    #  ipttl
    #
    
        if  createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_ipttl','ipttl','ipttl 10 mask 6', ForwardOrDrop+' mirror-destination 1')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipttl(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_ipttl','ipttl', '0x8', '6')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_ipttl', 'ipttl','NV','', FwrdOrDrop, '', '1')
        #
        #  tcpdestportip
        #
        if  createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'p_tcpDportIP','tcpDportIP','tcpdestportip ' + str_l4_port_c + ':' + dst_ip_a_string +' mask 16',ForwardOrDrop+' mirror-destination 1')
        self.networkElementPolicyGenKeywords.policy_verify_acl_tcpdestportip(self.pytestConfigHelper.dut1.name,  FwrdOrDrop + 'p_tcpDportIP', 'tcpDportIP',  str_l4_port_c, '16')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_tcpDportIP', 'tcpDportIP','NV','', FwrdOrDrop, '','1')
    #
    #  tcpsoureportip
    #
    
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'p_tcpSportIP','tcpSportIP','tcpsourceportip ' + str_l4_port_a + ':' + src_ip_a_string  + ' mask 16', 'cos ' + cos_5_string)
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
                self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'p_tcpSportIP', 'tcpSportIP', 'tcpsourceportip ' + str_l4_port_a +':'+src_ip_a_string + ' mask 16',ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_tcpsourceportip(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'p_tcpSportIP','tcpSportIP', str_l4_port_a,'16')
    
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'tcpSportIP', 'tcpSportIP', 'NV', '', '',cos_5_string,'')
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'tcpSportIP', 'tcpSportIP','NV','',FwrdOrDrop,'','')
    #
    #  udpdestportup
    #
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'p_udpDportIP','udpDportIP','udpdestportip ' + str_l4_port_c + ':' + dst_ip_a_string + ' mask 16','cos ' + cos_5_string)
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'p_udpDportIP', 'udpDportIP', 'udpdestportip ' + str_l4_port_c + ':' + dst_ip_a_string + ' mask 16', ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_udpdestportip(self.pytestConfigHelper.dut1.name,   FwrdOrDrop+'p_udpDportIP','udpDportIP ', str_l4_port_c ,'16')
        if  createEntry == 'true' and FwrdOrDrop == 'fwrd':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'udpDportIP','udpDportIP','NV','','', cos_5_string, '')
        if  createEntry == 'true' and FwrdOrDrop == 'drop':
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'udpDportIP','udpDportIP','NV','', FwrdOrDrop, '',  '')
    #
    #  udpsourceportup
    #
        if  createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,  FwrdOrDrop+'p_udpSportIP','udpSportIP', 'udpsourceportip '+ str_l4_port_a+':'+dst_ip_a_string + ' mask 16',ForwardOrDrop)
        self.networkElementPolicyGenKeywords.policy_verify_acl_udpsourceportip(self.pytestConfigHelper.dut1.name,   FwrdOrDrop+'p_udpSportIP','udpSportIP' , str_l4_port_a, '16')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, FwrdOrDrop+'p_udpSportIP','udpSportIP','NV','',  FwrdOrDrop, '',  '')
    
    
    def Create_And_Verify_Basic_Multiple_Match_Access_List_Entries(self,createEntry):        
        # FULL_MASK_VALUES_MULTI_MATCH_CASES
        print('Log_Create_and_Check_Fully_masked_Access-List_entries_with_multiple_match_conditions.')
        cos_5_string = self.pytestConfigHelper.config.cos_5
        dst_ip_a_string = self.pytestConfigHelper.config.dst_ip_a
        src_ip_a_string = self.pytestConfigHelper.config.src_ip_a
        str_l4_port_c = self.pytestConfigHelper.config.l4_port_c
        str_l4_port_a = self.pytestConfigHelper.config.l4_port_a
        
        if  createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,'AclOne','TwoFull','iptos 55 icmp6type 100.100', 'forward')
        self.networkElementPolicyGenKeywords.policy_verify_acl_iptos(self.pytestConfigHelper.dut1.name, 'AclOne','TwoFull', '55', '8')
        self.networkElementPolicyGenKeywords.policy_verify_acl_icmp6type(self.pytestConfigHelper.dut1.name, 'AclOne','TwoFull','100.100','16')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, 'AclOne','TwoFull','NV', '', 'fwrd', '','')
    
        if  createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,'AclOne','ThreeFull', 
                            'ipdestsocket ' + dst_ip_a_string +' ' + 'ipttl 66 icmptype 6.1 mask 16','forward mirror-destination 1')
    
        self.networkElementPolicyGenKeywords.policy_verify_acl_icmptype(self.pytestConfigHelper.dut1.name, 'AclOne','ThreeFull', '6.1', '16')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipdestsocket(self.pytestConfigHelper.dut1.name, 'AclOne', 'ThreeFull', dst_ip_a_string, '32')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipttl(self.pytestConfigHelper.dut1.name, 'AclOne','ThreeFull','66')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, 'AclOne','ThreeFull','NV','','fwrd', '','1')
    
        '''if  createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,'AclTwo','FourFull',
                            'ipproto 0x50 mask 8' + ' ipsourcesocket '+ src_ip_a_string + ':' + str_l4_port_c + ' mask 48' +' iptos 255 mask 8' + '  ipttl 63 mask 8',
                                        'drop syslog cos ' + cos_5_string)
            self.networkElementPolicyGenKeywords.policy_verify_acl_ipproto(self.pytestConfigHelper.dut1.name, 'AclTwo','FourFull', '0x50','8')
            self.networkElementPolicyGenKeywords.policy_verify_acl_ipsourcesocket(self.pytestConfigHelper.dut1.name, 'AclTwo','FourFull', src_ip_a_string + ':' + str_l4_port_c ,'48')
            self.networkElementPolicyGenKeywords.policy_verify_acl_iptos(self.pytestConfigHelper.dut1.name,'AclTwo','FourFull','255','8')
            self.networkElementPolicyGenKeywords.policy_verify_acl_ipttl(self.pytestConfigHelper.dut1.name,'AclTwo','FourFull','63','8')
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, 'AclTwo','FourFull','NV','S','drop',cos_5_string,'')
    '''
        if  createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'AclTwo','FiveFull', 
                'ipsourcesocket ' + src_ip_a_string + ' ipdestsocket '+ dst_ip_a_string + ' ipfrag ether 0x0800 iptos 64 mask 8' ,
                ' mirror-destination 2 drop syslog cos ' + cos_5_string)
            self.networkElementPolicyGenKeywords.policy_verify_acl_ipsourcesocket(self.pytestConfigHelper.dut1.name,'AclTwo','FiveFull', src_ip_a_string)
            self.networkElementPolicyGenKeywords.policy_verify_acl_ipdestsocket(self.pytestConfigHelper.dut1.name,'AclTwo','FiveFull',  dst_ip_a_string)
            self.networkElementPolicyGenKeywords.policy_verify_acl_ipfrag(self.pytestConfigHelper.dut1.name, 'AclTwo','FiveFull')
            self.networkElementPolicyGenKeywords.policy_verify_acl_ether(self.pytestConfigHelper.dut1.name, 'AclTwo','FiveFull','0x800')
            self.networkElementPolicyGenKeywords.policy_verify_acl_iptos(self.pytestConfigHelper.dut1.name, 'AclTwo','FiveFull', '64','8')
            self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, 'AclTwo','FiveFull','NV', 'S', 'drop', cos_5_string,'2')
    
        # PARTIAL_MASK_VALUES_multi_match_case
        print('Log_Create_and_Check_Partially_masked_Access-List_entries_with_multiple_match_conditions.')
    
        if  createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,'AclOne','TwoPart','ipttl 111 mask 8' + ' icmp6type 100.100 mask 8','forward')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipttl(self.pytestConfigHelper.dut1.name, 'AclOne','TwoPart','111','8')
        self.networkElementPolicyGenKeywords.policy_verify_acl_icmp6type(self.pytestConfigHelper.dut1.name, 'AclOne','TwoPart','100.0','8')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, 'AclOne','TwoPart','NV','','fwrd','', '')
    
        if  createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'AclOne','ThreePart',
                                        'ipdestsocket ' + dst_ip_a_string + ':' + str_l4_port_c +  ' mask 32 ' + ' ipttl 44 mask 4 ' + ' icmptype 6.1 mask 8', ' forward mirror-destination 1')
    
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipdestsocket(self.pytestConfigHelper.dut1.name, 'AclOne','ThreePart',dst_ip_a_string,'32')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipttl(self.pytestConfigHelper.dut1.name, 'AclOne','ThreePart', '32','4')
        self.networkElementPolicyGenKeywords.policy_verify_acl_icmptype(self.pytestConfigHelper.dut1.name, 'AclOne','ThreePart','6.0','8')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name,'AclOne','ThreePart', 'NV', '', 'fwrd', '', '1')
    
        if  createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name, 'AclTwo','FourPart',
                'ipproto 0xFF mask 4 ' + ' ipsourcesocket ' + src_ip_a_string + ':' + str_l4_port_c + ' mask 32' + ' iptos 255 mask 4' + ' ipttl 255 mask 4',
                'drop syslog cos ' + cos_5_string)
    
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipproto(self.pytestConfigHelper.dut1.name, 'AclTwo','FourPart','0xf0','4')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipsourcesocket(self.pytestConfigHelper.dut1.name, 'AclTwo','FourPart', src_ip_a_string, '32')
        self.networkElementPolicyGenKeywords.policy_verify_acl_iptos(self.pytestConfigHelper.dut1.name, 'AclTwo','FourPart','240','4')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipttl(self.pytestConfigHelper.dut1.name, 'AclTwo','FourPart','240','4')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, 'AclTwo','FourPart','NV','S','drop', cos_5_string, '')
    
        if  createEntry == 'true':
            self.networkElementPolicyGenKeywords.policy_set_access_list(self.pytestConfigHelper.dut1.name,'AclTwo','FivePart',
                            'ipsourcesocket ' + src_ip_a_string + ' ipdestsocket ' + dst_ip_a_string + ' ipttl 0x8 ether 0x0800 iptos 64 mask 8',
                                                                        'mirror-destination 2 drop syslog cos ' + cos_5_string)
    
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipsourcesocket(self.pytestConfigHelper.dut1.name, 'AclTwo','FivePart', src_ip_a_string)
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipdestsocket(self.pytestConfigHelper.dut1.name, 'AclTwo','FivePart', dst_ip_a_string)
        self.networkElementPolicyGenKeywords.policy_verify_acl_ipttl(self.pytestConfigHelper.dut1.name, 'AclTwo','FivePart', '0x8')
        self.networkElementPolicyGenKeywords.policy_verify_acl_ether(self.pytestConfigHelper.dut1.name, 'AclTwo','FivePart','0x800')
        self.networkElementPolicyGenKeywords.policy_verify_acl_iptos(self.pytestConfigHelper.dut1.name, 'AclTwo','FivePart','64', '8')
        self.networkElementPolicyGenKeywords.policy_verify_acl_action_all(self.pytestConfigHelper.dut1.name, 'AclTwo','FivePart','NV','S','drop',cos_5_string,'2')
       
    
    def Configure_Basic_Single_Match_Access_List_Entries(self,):
            self.Create_And_Verify_Basic_Single_Match_Access_List_Entries('true')
    
    def Configure_Basic_Multiple_Match_Access_List_Entries(self,):
            self.Create_And_Verify_Basic_Multiple_Match_Access_List_Entries('true')
    
    def Verify_Basic_Single_Match_Access_List_Entries(self,):
            self.Create_And_Verify_Basic_Single_Match_Access_List_Entries('false')
    
    def Verify_Basic_Multiple_Match_Access_List_Entries(self,):
            self.Create_And_Verify_Basic_Multiple_Match_Access_List_Entries('false')
    
    def change_policy_access_list_profile_index(self,netelem,profile,newAcl):
            self.networkElementPolicyGenKeywords.policy_set_access_list_profile_none(self.pytestConfigHelper.dut1.name, profile)
            self.networkElementPolicyGenKeywords.policy_set_access_list_profile_index(netelem, profile, newAcl)
            time.sleep(int(self.pytestConfigHelper.config.policy_delay))  # Delay_for_EXOS_policy_hardware_config_batching.
    
    
    def change_policy_rule_model(self, netelem,   ruleModel,   verify='verify',  reEnablePolicy='true'):
        self.policyUdks.Disable_Policy_and_Verify_it_is_Disabled(self.pytestConfigHelper.dut1.name)
        if  ruleModel == 'Hierarchical':
            self.networkElementPolicyGenKeywords.policy_set_rule_model_hierarchical(self.pytestConfigHelper.dut1.name,  ignore_cli_feedback=True)
        if  verify == 'verify' and ruleModel == 'Hierarchical':
            self.networkElementPolicyGenKeywords.policy_verify_rule_model_hierarchical(self.pytestConfigHelper.dut1.name)
        if  ruleModel == 'Access-List':
            self.networkElementPolicyGenKeywords.policy_set_rule_model_access_list(self.pytestConfigHelper.dut1.name,)
        if  verify == 'verify' and ruleModel == 'Access-List':
              self.networkElementPolicyGenKeywords.policy_verify_rule_model_access_list(self.pytestConfigHelper.dut1.name)
        self.policyUdks.Enable_Policy_and_Verify_it_is_Enabled(self.pytestConfigHelper.dut1.name,)
        
    def TestCaseCleanupTrafficValidation(self):
        self.networkElementPolicyGenKeywords.policy_clear_access_list_all(self.pytestConfigHelper.config.netelem1.name)
        self.policyUdks.Remove_Policy_Profile_and_Verify_it_was_Removed(self.pytestConfigHelper.config.netelem1.name,  self.pytestConfigHelper.config.profile_a)
        self.policyUdks.Remove_Port_Admin_Profile_and_Verify_it_was_Removed(self.pytestConfigHelper.config.netelem1.name,  self.pytestConfigHelper.config.netelem1.tgen.port_a.ifname,
                                                     self.pytestConfigHelper.config.profile_a)
        self.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(
                                    self.pytestConfigHelper.config.netelem1.name,  self.pytestConfigHelper.config.dst_mac_a,      self.pytestConfigHelper.config.vlan_a,  self.pytestConfigHelper.config.netelem1.tgen.port_b.ifname)
        self.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed( self.pytestConfigHelper.config.netelem1.name,  self.pytestConfigHelper.config.vlan_a)
        self.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.pytestConfigHelper.config.netelem1.name,  self.pytestConfigHelper.config.vlan_b)
        self.Clear_all_Dot1p_QOS_Profiles(self.pytestConfigHelper.config.netelem1.name)
        #self.cosUdks.Configure_Port_Queue_Profile_and_Verify(self.pytestConfigHelper.config.netelem1.name,  self.pytestConfigHelper.config.netelem1.tgen.port_a.ifname, self.pytestConfigHelper.config.qos_none)
        #self.cosUdks.Remove_QOS_Profile_and_Verify_it_was_Removed(self.pytestConfigHelper.config.netelem1.name, self.pytestConfigHelper.config.qos_profile_all)
        self.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.pytestConfigHelper.config.netelem1.name,  self.pytestConfigHelper.config.netelem1.tgen.port_a.ifname)
        self.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.pytestConfigHelper.config.netelem1.name,  self.pytestConfigHelper.config.netelem1.tgen.port_b.ifname)
        #self.change_policy_rule_model(   self.pytestConfigHelper.config.netelem1.name, 'Hierarchical')
        self.networkElementCosGenKeywords.cos_set_port_qos_profile(self.pytestConfigHelper.config.netelem1.name,  self.pytestConfigHelper.dut1_tgen_port_a.ifname, 'none')
        self.networkElementCosGenKeywords.cos_delete_qos_profile(self.pytestConfigHelper.config.netelem1.name, self.pytestConfigHelper.config.qos_profile_all)
        
    
    def policy_set_rule_ipsourcesocket(self, device_name, profile_id=None, ip_addr=None, l4_port=None, mask=None,
                                       port_string=None, storage_type=None, vlan=None, forward=None, drop=None, cos=None,
                                       tci_overwrite=None, mirror_destination=None, syslog=None, trap=None, disable_port=None,
                                       quarantine_profile=None):
        
        self.networkElementPolicyGenKeywords.policy_set_rule_ipsourcesocket(device_name, profile_id=profile_id, ip_addr=ip_addr, l4_port=l4_port, mask=mask,
                                       port_string=port_string, storage_type=storage_type, vlan=vlan, forward=forward, drop=drop, cos=cos,
                                       tci_overwrite=tci_overwrite, mirror_destination=mirror_destination, syslog=syslog, trap=trap, disable_port=disable_port,
                                       quarantine_profile=quarantine_profile)
        
    def policy_verify_rule_ipsourcesocket_exists(self, device_name, profile_id=None, ip_addr=None, l4_port=None, mask=None,
                                                 port_string=None, storage_type=None, vlan=None, cos=None,
                                                 tci_overwrite=None, mirror_destination=None, syslog=None, trap=None,
                                                 disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_verify_rule_ipsourcesocket_exists(device_name, profile_id=profile_id, ip_addr=ip_addr, l4_port=l4_port, mask=mask,
                                                 port_string=port_string, storage_type=storage_type, vlan=vlan, cos=cos,
                                                 tci_overwrite=tci_overwrite, mirror_destination=mirror_destination, syslog=syslog, trap=trap,
                                                 disable_port=disable_port, quarantine_profile=quarantine_profile)
    
    def policy_set_rule_ipdestsocket(self, device_name, profile_id=None, ip_addr=None, l4_port=None, mask=None,
                                       port_string=None, storage_type=None, vlan=None, forward=None, drop=None, cos=None,
                                       tci_overwrite=None, mirror_destination=None, syslog=None, trap=None, disable_port=None,
                                       quarantine_profile=None):
        
        self.networkElementPolicyGenKeywords.policy_set_rule_ipdestsocket(device_name, profile_id=profile_id, ip_addr=ip_addr, l4_port=l4_port, mask=mask,
                                       port_string=port_string, storage_type=storage_type, vlan=vlan, forward=forward, drop=drop, cos=cos,
                                       tci_overwrite=tci_overwrite, mirror_destination=mirror_destination, syslog=syslog, trap=trap, disable_port=disable_port,
                                       quarantine_profile=quarantine_profile)
        
    def policy_verify_rule_ipdestsocket_exists(self, device_name, profile_id=None, ip_addr=None, l4_port=None, mask=None,
                                                 port_string=None, storage_type=None, vlan=None, cos=None,
                                                 tci_overwrite=None, mirror_destination=None, syslog=None, trap=None,
                                                 disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_verify_rule_ipdestsocket_exists(device_name, profile_id=profile_id, ip_addr=ip_addr, l4_port=l4_port, mask=mask,
                                                 port_string=port_string, storage_type=storage_type, vlan=vlan, cos=cos,
                                                 tci_overwrite=tci_overwrite, mirror_destination=mirror_destination, syslog=syslog, trap=trap,
                                                 disable_port=disable_port, quarantine_profile=quarantine_profile)
        
    def policy_set_rule_ip6dest(self, device_name, profile_id=None, ipv6_addr=None, l4_port=None, mask=None, port_string=None,
                                storage_type=None, vlan=None, forward=None, drop=None, cos=None, tci_overwrite=None,
                                mirror_destination=None, syslog=None, trap=None, disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_set_rule_ip6dest(device_name, profile_id=profile_id, ipv6_addr=ipv6_addr, l4_port=l4_port, mask=mask, port_string=port_string,
                                storage_type=storage_type, vlan=vlan, forward=forward, drop=drop, cos=cos, tci_overwrite=tci_overwrite,
                                mirror_destination=mirror_destination, syslog=syslog, trap=trap, disable_port=disable_port, quarantine_profile=quarantine_profile)
        
    def policy_verify_rule_ip6dest_exists(self, device_name, profile_id=None, ipv6_addr=None, l4_port=None, mask=None,
                                          port_string=None, storage_type=None, vlan=None, cos=None, tci_overwrite=None,
                                          mirror_destination=None, syslog=None, trap=None, disable_port=None,
                                          quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_verify_rule_ip6dest_exists(device_name, profile_id=profile_id, ipv6_addr=ipv6_addr, l4_port=l4_port, mask=mask,
                                          port_string=port_string, storage_type=storage_type, vlan=vlan, cos=cos, tci_overwrite=tci_overwrite,
                                          mirror_destination=mirror_destination, syslog=syslog, trap=trap, disable_port=disable_port,
                                          quarantine_profile=quarantine_profile)
    
    def policy_set_rule_tcpsourceportip(self, device_name, profile_id=None, tcp_port=None, ip_addr=None, mask=None,
                                        port_string=None, storage_type=None, vlan=None, forward=None, drop=None, cos=None,
                                        tci_overwrite=None, mirror_destination=None, syslog=None, trap=None, disable_port=None,
                                        quarantine_profile='', **kwargs):
        self.networkElementPolicyGenKeywords.policy_set_rule_tcpsourceportip( device_name, profile_id, tcp_port, ip_addr, mask,
                                        port_string, storage_type, vlan, forward, drop, cos, tci_overwrite, mirror_destination, syslog,
                                        trap, disable_port, quarantine_profile)
        
    def policy_verify_rule_tcpsourceportip_exists(self, device_name, profile_id=None, tcp_port=None, ip_addr=None, mask=None,
                                                  port_string=None, storage_type=None, vlan=None, cos=None,
                                                  tci_overwrite=None, mirror_destination=None, syslog=None, trap=None,
                                                  disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_verify_rule_tcpsourceportip_exists(self, device_name, profile_id, tcp_port, ip_addr, mask,
                                                  port_string, storage_type, vlan, cos, tci_overwrite, mirror_destination, syslog,trap,
                                                  disable_port, quarantine_profile)
    
    def policy_set_rule_tcpdestportip(self, device_name, profile_id=None, tcp_port=None, ip_addr=None, mask=None,
                                      port_string=None, storage_type=None, vlan=None, forward=None, drop=None, cos=None,
                                      tci_overwrite=None, mirror_destination=None, syslog=None, trap=None, disable_port=None,
                                      quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_set_rule_tcpdestportip(device_name, profile_id, tcp_port, ip_addr, mask, port_string, storage_type, 
                                                                           vlan, forward, drop, cos, tci_overwrite, mirror_destination, syslog, trap,
                                                                            disable_port, quarantine_profile)
        
    def policy_verify_rule_tcpdestportip_exists(self, device_name, profile_id=None, tcp_port=None, ip_addr=None, mask=None,
                                                port_string=None, storage_type=None, vlan=None, cos=None,
                                                tci_overwrite=None, mirror_destination=None, syslog=None, trap=None,
                                                disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_verify_rule_tcpdestportip_exists(device_name, profile_id, tcp_port, ip_addr, mask,
                                                port_string, storage_type, vlan, cos, tci_overwrite, mirror_destination, syslog, trap,
                                                disable_port, quarantine_profile)
            
        
    def policy_set_rule_udpsourceportip(self, device_name, profile_id=None, udp_port=None, ip_addr=None, mask=None,
                                        port_string=None, storage_type=None, vlan=None, forward=None, drop=None, cos=None,
                                        tci_overwrite=None, mirror_destination=None, syslog=None, trap=None, disable_port=None,
                                        quarantine_profile='', **kwargs):
        self.networkElementPolicyGenKeywords.policy_set_rule_udpsourceportip( device_name, profile_id, udp_port, ip_addr, mask,
                                        port_string, storage_type, vlan, forward, drop, cos, tci_overwrite, mirror_destination, syslog,
                                        trap, disable_port, quarantine_profile)
        
    def policy_verify_rule_udpsourceportip_exists(self, device_name, profile_id=None, udp_port=None, ip_addr=None, mask=None,
                                                  port_string=None, storage_type=None, vlan=None, cos=None,
                                                  tci_overwrite=None, mirror_destination=None, syslog=None, trap=None,
                                                  disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_verify_rule_udpsourceportip_exists(self, device_name, profile_id, udp_port, ip_addr, mask,
                                                  port_string, storage_type, vlan, cos, tci_overwrite, mirror_destination, syslog,trap,
                                                  disable_port, quarantine_profile)
    
    def policy_set_rule_udpdestportip(self, device_name, profile_id=None, udp_port=None, ip_addr=None, mask=None,
                                      port_string=None, storage_type=None, vlan=None, forward=None, drop=None, cos=None,
                                      tci_overwrite=None, mirror_destination=None, syslog=None, trap=None, disable_port=None,
                                      quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_set_rule_udpdestportip(device_name, profile_id, udp_port, ip_addr, mask, port_string, storage_type, 
                                                                           vlan, forward, drop, cos, tci_overwrite, mirror_destination, syslog, trap,
                                                                            disable_port, quarantine_profile)
        
    def policy_verify_rule_udpdestportip_exists(self, device_name, profile_id=None, udp_port=None, ip_addr=None, mask=None,
                                                port_string=None, storage_type=None, vlan=None, cos=None,
                                                tci_overwrite=None, mirror_destination=None, syslog=None, trap=None,
                                                disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_verify_rule_udpdestportip_exists(device_name, profile_id, udp_port, ip_addr, mask,
                                                port_string, storage_type, vlan, cos, tci_overwrite, mirror_destination, syslog, trap,
                                                disable_port, quarantine_profile)
        
    def policy_set_rule_ipttl(self, device_name, profile_id=None, ip_ttl=None, mask=None, port_string=None, storage_type=None,
                              vlan=None, forward=None, drop=None, cos=None, tci_overwrite=None, mirror_destination=None, syslog=None,
                              trap=None, disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_set_rule_ipttl(device_name, profile_id, ip_ttl, mask, port_string, storage_type,
                              vlan, forward, drop, cos, tci_overwrite, mirror_destination, syslog, trap, disable_port, quarantine_profile)
        
    def policy_verify_rule_ipttl_exists(self, device_name, profile_id=None, ip_ttl=None, mask=None, port_string=None,
                                        storage_type=None, vlan=None, cos=None, tci_overwrite=None,
                                        mirror_destination=None, syslog=None, trap=None, disable_port=None,
                                        quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_verify_rule_ipttl_exists(self, device_name, profile_id, ip_ttl, mask, port_string,
                                        storage_type, vlan, cos, tci_overwrite,
                                        mirror_destination, syslog, trap, disable_port,
                                        quarantine_profile)
    
    def policy_set_rule_iptos(self, device_name, profile_id=None, ip_tos=None, mask=None, port_string=None, storage_type=None,
                              vlan=None, forward=None, drop=None, cos=None, tci_overwrite=None, mirror_destination=None, syslog=None,
                              trap=None, disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_set_rule_iptos(device_name, profile_id, ip_tos, mask, port_string, storage_type,
                              vlan, forward, drop, cos, tci_overwrite, mirror_destination, syslog, trap, disable_port, quarantine_profile)
        
    def policy_verify_rule_iptos_exists(self, device_name, profile_id=None, ip_tos=None, mask=None, port_string=None,
                                        storage_type=None, vlan=None, cos=None, tci_overwrite=None,
                                        mirror_destination=None, syslog=None, trap=None, disable_port=None,
                                        quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_verify_rule_iptos_exists(device_name, profile_id, ip_tos, mask, port_string,
                                        storage_type, vlan, cos, tci_overwrite,
                                        mirror_destination, syslog, trap, disable_port,
                                        quarantine_profile)
        
    def policy_set_rule_ipproto(self, device_name, profile_id=None, ipproto=None, mask=None, port_string=None, storage_type=None,
                                vlan=None, forward=None, drop=None, cos=None, tci_overwrite=None, mirror_destination=None,
                                syslog=None, trap=None, disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_set_rule_ipproto(device_name, profile_id, ipproto, mask, port_string, storage_type,
                                vlan, forward, drop, cos, tci_overwrite, mirror_destination,
                                syslog, trap, disable_port, quarantine_profile)
        
    def policy_verify_rule_ipproto_exists(self, device_name, profile_id=None, ip_proto=None, mask=None, port_string=None,
                                          storage_type=None, vlan=None, cos=None, tci_overwrite=None,
                                          mirror_destination=None, syslog=None, trap=None, disable_port=None,
                                          quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_verify_rule_ipproto_exists(device_name, profile_id, ip_proto, mask, port_string,
                                          storage_type, vlan, cos, tci_overwrite,
                                          mirror_destination, syslog, trap, disable_port,
                                          quarantine_profile)
        
    def policy_set_rule_ether(self, device_name, profile_id=None, ether_type=None, mask=None, port_string=None,
                              storage_type=None, vlan=None, forward=None, drop=None, cos=None, tci_overwrite=None,
                              mirror_destination=None, syslog=None, trap=None, disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_set_rule_ether( device_name, profile_id, ether_type, mask, port_string,
                              storage_type, vlan, forward, drop, cos, tci_overwrite,
                              mirror_destination, syslog, trap, disable_port, quarantine_profile)
        
    def policy_verify_rule_ethertype_exists(self, device_name, profile_id=None, ether_type=None, mask=None, port_string=None,
                                            storage_type=None, vlan=None, cos=None, tci_overwrite=None,
                                            mirror_destination=None, syslog=None, trap=None, disable_port=None,
                                            quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_verify_rule_ethertype_exists(device_name, profile_id, ether_type, mask, port_string,
                                            storage_type, vlan, cos, tci_overwrite,
                                            mirror_destination, syslog, trap, disable_port,
                                            quarantine_profile)
        
    def policy_set_rule_macsource(self, device_name, profile_id=None, mac_addr=None, mask=None, port_string=None,
                                  storage_type=None, vlan=None, forward=None, drop=None, cos=None, tci_overwrite=None,
                                  mirror_destination=None, syslog=None, trap=None, disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_set_rule_macsource(self, device_name, profile_id, mac_addr, mask, port_string,
                                  storage_type, vlan, forward, drop, cos, tci_overwrite,
                                  mirror_destination, syslog, trap, disable_port, quarantine_profile)
        
    def policy_verify_rule_macsource_exists(self, device_name, profile_id=None, mac_addr=None, mask=None, port_string=None,
                                            storage_type=None, vlan=None, cos=None, tci_overwrite=None,
                                            mirror_destination=None, syslog=None, trap=None, disable_port=None,
                                            quarantine_profile=None, **kwargs):
        self.networkElementPolicyGenKeywords.policy_verify_rule_macsource_exists(device_name, profile_id, mac_addr, mask, port_string,
                                            storage_type, vlan, cos, tci_overwrite,
                                            mirror_destination, syslog, trap, disable_port,
                                            quarantine_profile)    
    
    def policy_set_rule_macdest(self, device_name, profile_id=None, mac_addr=None, mask=None, port_string=None,
                                  storage_type=None, vlan=None, forward=None, drop=None, cos=None, tci_overwrite=None,
                                  mirror_destination=None, syslog=None, trap=None, disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_set_rule_macdest(device_name, profile_id, mac_addr, mask, port_string,
                                  storage_type, vlan, forward, drop, cos, tci_overwrite,
                                  mirror_destination, syslog, trap, disable_port, quarantine_profile)
        
    def policy_verify_rule_macdest_exists(self, device_name, profile_id=None, mac_addr=None, mask=None, port_string=None,
                                            storage_type=None, vlan=None, cos=None, tci_overwrite=None,
                                            mirror_destination=None, syslog=None, trap=None, disable_port=None,
                                            quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_verify_rule_macdest_exists(device_name, profile_id, mac_addr, mask, port_string,
                                            storage_type, vlan, cos, tci_overwrite,
                                            mirror_destination, syslog, trap, disable_port,
                                            quarantine_profile)
    
    def policy_set_rule_port(self, device_name, profile_id=None, port=None, mask=None, port_string=None, storage_type=None,
                             vlan=None, forward=None, drop=None, cos=None, tci_overwrite=None, mirror_destination=None, syslog=None,
                             trap=None, disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_set_rule_port(device_name, profile_id, port, mask, port_string, storage_type,
                             vlan, forward, drop, cos, tci_overwrite, mirror_destination, syslog,
                             trap, disable_port, quarantine_profile)
        
    def policy_verify_rule_port_exists(self, device_name, profile_id=None, port=None, mask=None, port_string=None,
                                       storage_type=None, vlan=None, cos=None, tci_overwrite=None,
                                       mirror_destination=None, syslog=None, trap=None, disable_port=None,
                                       quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_verify_rule_port_exists(device_name, profile_id, port, mask, port_string,
                                       storage_type, vlan, cos, tci_overwrite,
                                       mirror_destination, syslog, trap, disable_port,
                                       quarantine_profile)
    
    def policy_set_rule_ipfrag(self, device_name, profile_id=None, mask=None, port_string=None, storage_type=None, vlan=None,
                               forward=None, drop=None, cos=None, tci_overwrite=None, mirror_destination=None, syslog=None,
                               trap=None, disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_set_rule_ipfrag(self, device_name, profile_id, mask, port_string, storage_type, vlan,
                               forward, drop, cos, tci_overwrite, mirror_destination, syslog,
                               trap, disable_port, quarantine_profile)
    
    def policy_verify_rule_ipfrag_exists(self, device_name, profile_id=None, mask=None, port_string=None, storage_type=None,
                                         vlan=None, cos=None, tci_overwrite=None, mirror_destination=None, syslog=None,
                                         trap=None, disable_port=None, quarantine_profile=None):
        self.networkElementPolicyGenKeywords.policy_verify_rule_ipfrag_exists(self, device_name, profile_id, mask, port_string, storage_type,
                                         vlan, cos, tci_overwrite, mirror_destination, syslog,
                                         trap, disable_port, quarantine_profile)
       