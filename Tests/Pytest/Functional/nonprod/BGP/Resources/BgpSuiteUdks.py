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
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementInterfaceGenKeywords import NetworkElementInterfaceGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementBgpGenKeywords import NetworkElementBgpGenKeywords

class BgpSuiteUdks():
    
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
        self.networkElementInterfaceGenKeywords = NetworkElementInterfaceGenKeywords()
        self.networkElementBgpGenKeywords = NetworkElementBgpGenKeywords()

    def Reboot_DUT(self, dut):
        '''[Documentation]Save config to a file, then Reboot using the saved config.
        ...              This keyword will not return until DUT is up and running.'''
        #[Arguments]  ${dut}
        config_file =  'robot-bgp-temp'
        print('Rebooting ' + dut.name)        
        self.networkElementFileManagementUtilsKeywords.save_current_config_to_file(dut.name, config_file, overwrite_answer="y")
        self.networkElementResetDeviceUtilsKeywords.reboot_network_element_with_config(dut.name, config_file)
        self.pingKeywords.wait_until_ip_is_reachable(dut.ip, max_wait='300', wait_before='60', wait_after_success='30',interval='5', message='Ping_DUT')
        self.networkElementConnectionManager.close_connection_to_network_element(dut.name)
        self.networkElementConnectionManager.connect_to_network_element(dut.name,  dut.ip,  dut.username,  dut.password, dut.connection_method,  dut.os)
        
    
    def Use_Configuration_File(self, device_name, nameOfFile):
        '''[Documentation]  Specify a save configuration file to use on the next reboot'''
        #[Arguments]  ${device_name}  ${file}
        self.networkElementCliSend.send_cmd(device_name, 'use configuration ' +  nameOfFile)
       
    def Enable_Premier_Trial_License(self, device_name):
        '''[Documentation]  Enable the 30 day trial Premier license'''
        #[Arguments]  ${device_name}
        self.networkElementCliSend.send_cmd(device_name, 'debug epm enable trial-license')
    
    def Disable_Premier_Trial_License(self, device_name):
        '''[Documentation]  Disable the 30 day trial Premier license'''
        #[Arguments]  ${device_name}
        self.networkElementCliSend.send_cmd(device_name,  'debug epm clear trial-license',
           confirmation_phrases='Are you sure you want to clear license information stored in EEPROM?',
           confirmation_args='y')
    
    def Verify_Premier_License(self,device_name):
        '''[Documentation]  Enable the 30 day trial Premier license'''
        #[Arguments]  ${device_name}
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(device_name, 'show_license',
                                                                           '.*Level.*Premier')    
    def Verify_Base_License(self, device_name):
        '''[Documentation]  Enable the 30 day trial Premier license'''
        #[Arguments]  ${device_name}
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(device_name, 'show license',
                                                                           '.*Level.*Base')
    
    def Clear_License_Persistant_Data(self, dut):
        '''[Documentation]  Clear any existing persistant license `data'''
        #[Arguments]  ${dut}
        self.networkElementCliSend.send_cmd(dut,  'debug licMgr clear license cpd',
           confirmation_phrases='Removed licenses will need to be re-installed after reboot.',
           confirmation_args='y')
        self.pingKeywords.wait_until_ip_is_reachable(dut.ip, max_wait='300', wait_before='60', wait_after_success='30',interval='5', message='Ping_DUT')
        self.networkElementConnectionManager.close_connection_to_network_element(dut.name)
        self.networkElementConnectionManager.connect_to_network_element(dut.name,  dut.ip,  dut.username,  dut.password, dut.connection_method,  dut.os)
     
    def Set_VR_Context(self, device_name,  vrName='VR-Default'):
        '''[Documentation]  Enter the CLI mode for the specified VR or VRF'''
        #[Arguments]  ${device_name}  ${vrName}=VR-Default
        self.networkElementCliSend.send_cmd(device_name,  ' vr ' + vrName )
    
    def Create_VLAN(self, device_name, vlanName,  vrName='VR-Default'):
        '''[Documentation]  Configure a local instance of BGP.'''
        #[Arguments]  ${device_name}  ${vlanName}  ${vrName}=VR-Default
        self.Set_VR_Context(device_name, vrName)
        self.networkElementVlanGenKeywords.vlan_create_vlan(device_name, vlanName)
        self.Set_VR_Context(device_name)
    
    def Delete_VLAN(self, device_name, vlanName,  vrName='VR-Default' ):
        '''[Documentation]  Configure a local instance of BGP.'''
        #[Arguments]  ${device_name}  ${vlanName}  ${vrName}=VR-Default        
        self.Set_VR_Context(device_name, vrName)
        self.networkElementVlanGenKeywords.vlan_delete_vlan(device_name, vlanName)
        self.Set_VR_Context(device_name)
        
    def Configure_VLAN_IP_Address(self, device_name,  vlanName, ip, mask, vrName='VR-Default'):
        '''[Documentation]  Configure a local instance of BGP.'''
        #[Arguments]  ${device_name}  ${vlanName}  ${ip}  ${mask}  ${vrName}=VR-Default        
        self.Set_VR_Context(device_name, vrName)
        self.networkElementInterfaceGenKeywords.interface_set_ipv4_primary_addr_netmask(device_name, vlanName, ip, netmask='')
        self.Set_VR_Context(device_name, vrName)
    
    
    def Create_BGP_Instance(self, device_name,  vlanName, bgp, vrName='VR-Default'):
        '''[Documentation]  Configure a local instance of BGP.'''
        #[Arguments]  ${device_name}  ${bgp}  ${vrName}=VR-Default        
        self.Set_VR_Context(device_name, vrName)
        self.networkElementBgpGenKeywords.bgp_create_as(device_name, bgp.localAS)
        self.networkElementBgpGenKeywords.bgp_set_router_id(device_name, bgp.router_id)
        self.networkElementBgpGenKeywords.bgp_enable_global(device_name)
        self.Set_VR_Context(device_name)
    
    def Disable_BGP_Instance(self, device_name,  vrName='VR-Default'):
        '''[Documentation]  Disable a local instance of BGP.'''
        #[Arguments]  ${device_name}  ${vrName}=VR-Default
        self.Set_VR_Context(device_name, vrName)
        self.networkElementBgpGenKeywords.bgp_disable_global(device_name)
        self.Set_VR_Context(device_name, vrName)
    
    def Verify_BGP_Enabled(self, device_name,  vrName='VR-Default'):
        '''[Documentation]  Verify the BGP instance is enabled on the specified VR'''
        #[Arguments]  ${device_name}  ${vrName}=VR-Default
        self.Set_VR_Context(device_name, vrName)
        self.networkElementBgpGenKeywords.bgp_enable_global(device_name)
        self.Set_VR_Context(device_name, vrName)
    
    def Create_BGP_Neighbor_Ignore_Error(self, device_name, neighborIP,  remoteAS, vrName='VR-Default'):
        '''[Documentation]  Creates and enable a BGP neighbor ignoring Error'''
        #[Arguments]  ${device_name}  ${neighborIP}  ${remoteAS}  ${vrName}=VR-Default
        self.Set_VR_Context(device_name, vrName)
        self.networkElementBgpGenKeywords.bgp_create_neighbor(device_name, neighborIP, remoteAS, ignore_error="Error")
        self.Set_VR_Context(device_name)
    
    def Create_BGP_Neighbor(self, device_name,  neighborIP,  remoteAS,  vrName='VR-Default' ):
        '''[Documentation]  Creates and enable a BGP neighbor'''
        #[Arguments]  ${device_name}  ${neighborIP}  ${remoteAS}  ${vrName}=VR-Default
        self.Set_VR_Context(device_name, vrName)
        self.networkElementBgpGenKeywords.bgp_create_neighbor(device_name, neighborIP, remoteAS)
        self.Set_VR_Context(device_name, vrName)
    
    def Delete_BGP_Neighbor(self, device_name,  neighborIP,  vrName='VR-Default'):
        '''[Documentation]  Delete a BGP neighbor'''
        #[Arguments]  ${device_name}  ${neighborIP}  ${vrName}=VR-Default       
        self.Set_VR_Context(device_name, vrName)
        self.networkElementBgpGenKeywords.bgp_delete_neighbor(device_name, neighborIP)
        self.Set_VR_Context(device_name)
    
    def Delete_BGP_Neighbor_Ignore_Error(self, device_name, neighborIP, vrName='VR-Default' ):
        '''[Documentation]  Delete a BGP neighbor ignoring Error'''
        #[Arguments]  ${device_name}  ${neighborIP}  ${vrName}=VR-Default
        self.Set_VR_Context(device_name, vrName)
        self.networkElementBgpGenKeywords.bgp_delete_neighbor(device_name, neighborIP, ignore_error="Error")
        self.Set_VR_Context(device_name, vrName)
    
    def Delete_BGP_Neighbor_Ignore_Invalid(self, device_name,  neighborIP,  vrName='VR-Default'):
        '''[Documentation]  Delete a BGP neighbor ignoring Error'''
        #[Arguments]  ${device_name}  ${neighborIP}  ${vrName}=VR-Default
        self.Set_VR_Context(device_name, vrName)
        self.networkElementBgpGenKeywords.bgp_delete_neighbor(device_name, neighborIP, ignore_error='^')
        self.Set_VR_Context(device_name)
    
    def Verify_BGP_Number_Neighbors(self, device_name, number, vrName='VR-Default' ):
        '''[Documentation]  Verify total number of BGP neighbors configured'''
        #[Arguments]  ${device_name}  ${number}  ${vrName}=VR-Default
        self.Set_VR_Context(device_name, vrName)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(device_name, 'show bgp neighbor',
                                                                           '.*Total_Peers.*$' + number )
        self.Set_VR_Context(device_name)
    
    def Create_BGP_Autopeering(self, device_name,  localAS,  routerId ):
        '''[Documentation]  Configures BGP auto peering'''
        '''[Arguments]  ${device_name}  ${localAS}  ${routerId}'''        
        self.networkElementCliSend.send_cmd(device_name,'create auto-peering bgp routerid ' + routerId + ' AS-number ' + localAS)
    
    def Delete_BGP_Autopeering(self, device_name):
        '''[Documentation]  Deletes auto-peering'''
        #[Arguments]  ${device_name}
        self.networkElementCliSend.send_cmd(device_name,  'delete auto-peering',
           confirmation_phrases='Are you sure you want to delete auto-peering?',
           confirmation_args='y')
    
    def Verify_Three_Auto_Peers_Established(self, device_name):
        '''[Documentation]  Verify 3 auto-peers reach established state'''
        #[Arguments]  ${device_name}
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(device_name, 'show bgp neighbor',
            '.*SYS_BGP.*ESTABLISHED.*SYS_BGP.*ESTABLISHED.*SYS_BGP.*ESTABLISHED.*')
    
    def Verify_BGP_Neighbor_Exists(self, device_name,  neighborIP,  remoteAS,  vrName='VR-Default'):
        '''[Documentation]  Verify a particular neighbor exists on the VR specified'''
        #[Arguments]  ${device_name}  ${neighborIP}  ${remoteAS}  ${vrName}=VR-Default
        self.Set_VR_Context(device_name, vrName)
        self.networkElementBgpGenKeywords.bgp_verify_neighbor_exists(device_name, neighborIP, remoteAS)
        self.Set_VR_Context(device_name)
    
    def Verify_BGP_Neighbor_Does_Not_Exist(self, device_name, neighborIP, remoteAS, vrName='VR-Default'):
        '''[Documentation]  Verify a particular neighbor does not exist on the VR specified'''
        #[Arguments]  ${device_name}  ${neighborIP}  ${remoteAS}  ${vrName}=VR-Default
        self.Set_VR_Context(device_name, vrName)
        self.networkElementBgpGenKeywords.bgp_verify_neighbor_does_not_exist(device_name, neighborIP, remoteAS)
        self.Set_VR_Context(device_name)
    
    def Create_User_VR(self, device_name, vr_name):
        '''[Documentation]  Create a user VR from the default VR.'''
        #[Arguments]  ${device_name}  ${vr_name}
        self.Set_VR_Context(device_name)
        self.networkElementCliSend.send_cmd(device_name, 'create vr ' + vr_name)
    
    def Create_VRF(self, device_name,  vrf_name, parent_vr_name='VR-Default'):
        '''[Documentation]  Create a VRF from a parent VR.'''
        #[Arguments]  ${device_name}  ${vrf_name}  ${parent_vr_name}=VR-Default
        self.Set_VR_Context(device_name)
        self.networkElementCliSend.send_cmd(device_name, 'create vr ' + vrf_name + ' type vrf ' + parent_vr_name)
    
    def Delete_VR(self, device_name,  vr_name ):
        '''[Documentation]  Delete a user VR or VRF.'''
        #[Arguments]  ${device_name}  ${vr_name}
        self.Set_VR_Context(device_name)
        self.networkElementCliSend.send_cmd(device_name, 'delete vr ' + vr_name)
        
    def Add_Protocol_to_VR(self, device_name, vr_name,  protocol='bgp'):
        '''[Documentation]  Add a protocol to a VR or VRF.'''
        #[Arguments]  ${device_name}  ${vr_name}  ${protocol}=bgp
        self.Set_VR_Context(device_name)
        self.networkElementCliSend.send_cmd(device_name, ' configure vr ' + vr_name + ' add protocol ' + protocol)
    
    def Delete_Protocol_from_VR(self, device_name, vr_name, protocol='bgp'):
        '''[Documentation]  Delete a protocol from a VR or VRF..'''
        #[Arguments]  ${device_name}  ${vr_name}  ${protocol}=bgp
        self.Set_VR_Context(device_name)
        self.networkElementCliSend.send_cmd(device_name, ' configure vr ' + vr_name + ' delete protocol ' + protocol)
    
    def Create_and_Configure_Tagged_VLAN(self,  device_name,  vlan):
        '''[Documentation]  Creates a VLAN with a name and tag and adds port and IP address to it.'''
        #[Arguments]  ${device_name}  ${vlan}         
        self.networkElementCliSend.send_cmd(device_name, 'create vlan ' + vlan.name + ' tag ' + vlan.tag)
        self.networkElementCliSend.send_cmd(device_name, 'configure vlan  ' + vlan.name + ' add ports' + vlan.port + ' tagged')
        self.networkElementCliSend.send_cmd(device_name, 'configure vlan  ' + vlan.name + ' ipaddress ' + vlan.ip.addr + ' ' + vlan.ip.mask)
    
        