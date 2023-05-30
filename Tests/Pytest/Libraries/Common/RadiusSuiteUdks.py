from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementRadiusGenKeywords import NetworkElementRadiusGenKeywords
from ExtremeAutomation.Keywords.UserDefinedKeywords.NetworkElements.Security.RadiusUdks import RadiusUdks
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementCliSend import NetworkElementCliSend


class RadiusSuiteUdks(RadiusUdks):
    def __init__(self) -> None:
        self.networkElementRadiusGenKeywords = NetworkElementRadiusGenKeywords()
        self.networkElementCliSend = NetworkElementCliSend()        
        
    #EXOS     
    def Configure_And_Enable_Radius_Netlogin_Server(self, device_name, Instance, Server, UDP_Port, Secret, Ip, Vr):
        self.Add_a_Radius_Server_and_Verify_it_was_Added(device_name, Instance, Server, UDP_Port, Secret, Ip, Vr)
        self.Enable_Radius_for_Netlogin_Users_and_Verify(device_name)
    

    def UnConfigure_And_Disable_Radius_Netlogin_Server(self, device_name, Instance, Ip = ''):
        self.Remove_Radius_Server_and_Verify_it_is_Removed(device_name, Instance, Ip)

    '''def UnConfigure_And_Disable_Radius_Netlogin_Server(self, device_name, Instance, addr):
        self.Remove_Radius_Server_and_Verify_it_is_Removed(device_name, Instance, addr)'''

        #self.disable_radius  ${NetElem}
     
    def Configure_And_Enable_Radius_DynAuth_Server(self, device_name, Instance, Server, Secret, Ip, Vr):
        self.networkElementCliSend.send_cmd(device_name, 'configure radius dynamic-authorization ' + str(Instance) + ' server '+ str(Server) + ' client-ip ' + str(Ip) + ' vr ' + str(Vr) +  ' shared-secret ' + str(Secret))
        self.networkElementCliSend.send_cmd(device_name, 'enable radius dynamic-authorization')
        
    def UnConfigure_And_Disable_Radius_DynAuth_Server(self, device_name, Instance):
        self.networkElementCliSend.send_cmd(device_name, 'unconfigure radius dynamic-authorization server ' + str(Instance))
        self.networkElementCliSend.send_cmd(device_name, 'disable radius dynamic-authorization')
        
    
    def Send_COA_Auth_Request(self, EndSysName, Ip, HyphenatedMac,PolicyProfile = '-', RFC3580Vlan = '4096', NasPort = '0',
                              AuthClient = '0', PolicyAcl = ''):                              
     # [Arguments]  ${EndSysName}  ${Ip}  ${HyphenatedMac}
      # ...     ${PolicyProfile}=${noPolicyProfile}  ${RFC3580Vlan}=${NoVlan}
      # ...     ${NasPort}=${noNasPort}  ${AuthClient}=${NoAuthClient}
      # ...     ${PolicyAcl}=${noPolicyAcl}
      no_policy_profile = PolicyProfile
      no_vlan = RFC3580Vlan
      no_nas_port = NasPort
      no_auth_client = AuthClient
      no_policy_acl = PolicyAcl
      cmd_str = '/root/RobotScripts/COA-Auth-Send-Python ' + str(Ip) + ' ' + str(HyphenatedMac) + ' ' + str(no_policy_profile) + ' ' + str(no_vlan) + ' '+ str(no_nas_port) + ' ' + str(no_auth_client) +' ' + str(no_policy_acl)
      return_val =  self.networkElementCliSend.send_cmd(EndSysName,cmd_str)
      
     
    def Send_COA_Disconnect_Request(self, device_name, EndSysName, Ip, hyphenatedMac, NasPort=0):
      self.networkElementCliSend.send_cmd(device_name, )
      
    def configure_netlogin_mac_username_format(self, device_name, format):
        self.networkElementCliSend.send_cmd(device_name, 'configure netlogin mac username format ' + str(format))
        
    def Clear_Netlogin_Port_State(self, device_name, portOrPorts):
        self.networkElementCliSend.send_cmd(device_name, 'clear netlogin state port ' + str(portOrPorts))
        
    def Clear_Syslog(self, device_name):
        self.networkElementCliSend.send_cmd(device_name, 'clear log static')

