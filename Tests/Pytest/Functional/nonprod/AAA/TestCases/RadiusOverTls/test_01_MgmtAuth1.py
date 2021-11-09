from pytest import fixture, mark
import time
from Tests.Pytest.Functional.nonprod.AAA.Resources.AAASuiteUdks import AAASuiteUdks
from Tests.Pytest.Functional.nonprod.AAA.Resources.AAABase import AAABase


class MgmtTests(AAABase):
    
    @mark.BUILD
    def test_01_Telnet_to_DUT_using_Local_Authentication(self):
        '''[Documentation]  Verify_that_a_Local_Auth_user_can_Telnet_to_the_DUT'''  
        self.aaaSuiteUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name,self.tb.config.netelem1.ip,self.tb.config.netelem1.username,
                                                                                                      self.tb.config.netelem1.password, 'telnet', self.tb.config.netelem1.os, max_wait=30 )
        self.Verify_Successful_Login_of_Local_User()
        self.aaaSuiteUdks.networkElementConnectionManager.close_connection_to_network_element(self.tb.config.netelem1.name)
    
    @mark.NIGHTLY
    @mark.BUILD
    def test_02_SSH_to_DUT_using_Local_Authentication(self):
        '''[Documentation]  Verify_that_a_Local_Auth_user_can_SSH_to_the_DUT'''
        self.aaaSuiteUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name,self.tb.config.netelem1.ip,self.tb.config.netelem1.username,
                                                                                                      self.tb.config.netelem1.password, 'telnet', self.tb.config.netelem1.os, max_wait=30 )
        self.Verify_Successful_Login_of_Local_User()
        self.aaaSuiteUdks.networkElementConnectionManager.close_connection_to_network_element(self.tb.config.netelem1.name)
    
    @mark.NIGHTLY
    @mark.BUILD
    def test_03_SSH_to_DUT_using_RADIUS_Authentication(self):
        '''[Documentation]  Verify_that_a_Remote_user (i.e., RADIUS_auth) can_SSH_to_the_DUT'''
        self.aaaSuiteUdks.radiusUdks.Enable_Radius_for_Management_Users_and_Verify(self.tb.config.netelem1.name)
        #Connect_to_Network_Element  ${DUT.name}  ${DUT.ip}  ${USER_CREDENTIALS_REMOTE.username}  ${USER_CREDENTIALS_REMOTE.password}  ssh  ${DUT.os}  max_wait=30
        self.aaaSuiteUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name,self.tb.config.netelem1.ip,self.tb.config.netelem1.username,
                                                                                                      self.tb.config.netelem1.password, 'ssh', self.tb.config.netelem1.os, max_wait=30 )
        self.Verify_Successful_Login_of_Local_User()
        self.aaaSuiteUdks.networkElementConnectionManager.close_connection_to_network_element(self.tb.config.netelem1.name)
        self.aaaSuiteUdks.radiusUdks.Disable_Radius_for_Management_Users_and_Verify(self.tb.config.netelem1.name)
    
    @mark.NIGHTLY
    def test_04_SSH_to_DUT_when_RADIUS_Not_Enabled(self):
        '''[Documentation]  Verify_that_a_Remote_user (i.e., RADIUS_auth) cannot_SSH_to_the_DUT when_RADIUS_authentication_is_not_enabled.'''
        #run_keyword_and_expect_error
          #NetMikoAuthenticationException: Authentication_failure: unable_to_connect*
        #Connect_to_Network_Element  ${DUT.name}  ${DUT.ip}  ${USER_CREDENTIALS_REMOTE.username}  ${USER_CREDENTIALS_REMOTE.password}  ssh  ${DUT.os}  max_wait=30
        self.aaaSuiteUdks.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name,self.tb.config.netelem1.ip,self.tb.config.netelem1.username,
                                                                                                      self.tb.config.netelem1.password, 'ssh', self.tb.config.netelem1.os, max_wait=30 )
    
    def Management_Auth_Setup(self):
        '''[Documentation]  Initialize_test_variables, create_a_local_user_account, and_enable_the_switch's_SSH_Server'''
        #${DUT}=  Create_DUT_Dictionary  ${netelem1}
        #set_test_variable  ${DUT}
        #set_test_variable  ${USER_CREDENTIALS_LOCAL}   ${user.local}
        #set_test_variable  ${USER_CREDENTIALS_REMOTE}  ${user.remote}
        self.Create_and_Verify_Admin_Account(self.tb.config.netelem1.name,self.tb.config.netelem1.username,self.tb.config.netelem1.password)
        self.Enable_SSH_Server_on_Network_Element(self.tb.config.netelem1.name)
    
    def Management_Auth_Teardown(self):
        '''[Documentation]  Delete_the_local_user_account_and_disable_the_switch's_SSH_Server'''
        self.Delete_and_Verify_Admin_Account(self.tb.config.netelem1.name, self.tb.config.username)
        self.Disable_SSH_Server_on_Network_Element(self.tb.config.netelem1.name)
    
    def Create_and_Verify_Admin_Account(self, netelem_name, username, password):
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_create_admin_account(netelem_name, username=username, 
                                                                                   passwd=password)
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_admin_account_exists(netelem_name, 
                                                                                          username=username)
    def Delete_and_Verify_Admin_Account(self, netelem_name, username):   
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_delete_account(netelem_name, username=username)
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_admin_account_does_not_exist(netelem_name,username)
    
    def Enable_SSH_Server_on_Network_Element(self,dut_name):
        self.aaaSuiteUdks.networkElementSshGenKeywords.ssh_enable(dut_name)
        self.aaaSuiteUdks.networkElementSshGenKeywords.ssh_verify_enabled(dut_name)
    
    def Disable_SSH_Server_on_Network_Element(self, dut_name):
        self.aaaSuiteUdks.networkElementSshGenKeywords.ssh_disable(dut_name)
        self.aaaSuiteUdks.networkElementSshGenKeywords.ssh_verify_disabled(dut_name)
    
    def Create_DUT_Dictionary(self, netelem):
        '''[Documentation]  Create_dictonary_which_represents_a_secondary_handle_for
        ...              an_existing_network_element.  This_allows_us_to "Connect
        ...              to_Network_Element" twice_for_the_same_piece_of_hardware.
        ...              The_primary_handle_is_named ${netlelem.name} and_is_how
        ...              ROBOT_configures_the_box.  The_secondary_handle_is_named
        ...              ${netelem.name}-ConnectionTest_and_is_how_this_test_suite
        ...              exercises_telnet_and_SSH_authentications.'''
        dut =  {}
        #dut.name =  catenate_SEPARATOR=-  ${netelem.name}  ConnectionTest        
        #dut.ip =  set_variable  ${netelem.ip}
        #dut.os =  set_variable  ${netelem.os}
        dut.name = netelem.name
        dut.ip =  netelem.ip
        dut.os =  netelem.os
        return  [dut]
    
    def Verify_Successful_Login_of_Local_User(self):
        #loginconfig_verify_user_auth_method  ${netelem1.name}  ${USER_CREDENTIALS_LOCAL.username}  local
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_user_auth_method(self.tb.config.netelem1.name,
                                    self.tb.config.username,'local')
        #loginconfig_verify_total_failed_login_attempts  ${netelem1.name}  ${USER_CREDENTIALS_LOCAL.username}  0
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_total_failed_login_attempts(self, device_name, username=self.tb.config.username, 
                                                                                                               login_attempts=0)
    
    def Verify_Successful_Login_of_Remote_User(self):
        #loginconfig_verify_user_auth_method  ${netelem1.name}  ${USER_CREDENTIALS_REMOTE.username}  RADIUS
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_user_auth_method(self.tb.config.netelem1.name,
                                    self.tb.config.username,'Radius')
       
        # EXOS_does_not_monitor_login_attempts_for_remote_users
