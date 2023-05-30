from Tests.Pytest.NonProduction.Policy.Resources.PolicyBase import PolicyBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.NonProduction.Policy.Resources.Policy_Test_Suite_Udks import Policy_Test_Suite_Udks

@fixture()
def test_setup_teardown(request):
    # Setup_section
    def teardown():
        request.instance.Test_Case_Cleanup()
    request.addfinalizer(teardown)

class ActionSetCOATests(PolicyBase): 
    @mark.F_1000_401
    @mark.CoaAccessList
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6 
    def test_01_Policy_Access_List_COA_Action_Set_Configuration(self):
        
        self.localPolicyUdks.Basic_Policy_Setup()
        
        print('  (Step_1) Base_Setup_Enable_Policy_and_MacAuth_on_selected_ports.')
        
        self.localPolicyUdks.Policy_Test_Case_Setup_Precedence()
    
        self.localPolicyUdks.policyUdks.Disable_Policy_and_Verify_it_is_Disabled(self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,  'configure policy slices tci-overwrite 1')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,  'configure policy slices shared 1')
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Access-List')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name, ' disable clipaging')
        self.localPolicyUdks.networkElementPortGenKeywords.port_enable_state(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.networkElementPortGenKeywords.port_enable_state(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_b.ifname)
    
        print('  (Step_2) Test_Setup_Create_and_enable_Radius_Netlogin_and_radius_DynAuth_Server.')
        
        radius_server = self.tb.config.endsysRadius.name
        radius_instance = self.tb.config.endsysRadius.instance
        radius_ip_address = self.tb.config.endsysRadius.ip
        radius_port = self.tb.config.endsysRadius.port
        radius_secret = self.tb.config.endsysRadius.shared_secret
        radius_vr = "VR-Mgmt"
        radius_username = self.tb.config.endsysRadius.username
        radius_password = self.tb.config.endsysRadius.password
        radius_connection_method = self.tb.config.endsysRadius.connection_method
        radius_os = self.tb.config.endsysRadius.os
        macAuthClient = 3
                
        self.localPolicyUdks.radiusSuiteUdks.Configure_And_Enable_Radius_Netlogin_Server( self.tb.dut1.name, radius_instance, radius_ip_address, radius_port , radius_secret,  self.tb.dut1.ip,radius_vr)
        self.localPolicyUdks.radiusSuiteUdks.Configure_And_Enable_Radius_DynAuth_Server( self.tb.dut1.name, radius_instance, radius_ip_address, radius_secret, self.tb.dut1.ip, radius_vr) 
        
        self.localPolicyUdks.policyUdks.Enable_Policy_and_Verify_it_is_Enabled(self.tb.config.netelem1.name)
        self.localPolicyUdks.macAuthUdks.Enable_Macauth_and_Verify_it_is_Enabled(self.tb.config.netelem1.name)
        self.localPolicyUdks.macAuthUdks.Enable_Macauth_Port_and_Verify_it_is_Enabled(  self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.macAuthUdks.Enable_Macauth_Port_and_Verify_it_is_Enabled(  self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,'configure netlogin add mac-list ff:ff:ff:ff:ff:ff 48')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,'configure netlogin add mac-list 00:00:00:bb:bb:bb 48')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,'configure netlogin add mac-list 00:00:00:aa:aa:aa 48')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,  'configure netlogin mac username format none')
    
        print(' (Step_3) setup_connection_to_the_RADIUS_server_to_transmit_COA_requests')
        self.localPolicyUdks.endsystemConnectionMan.connect_to_endsystem_element(self.tb.config.endsysRadius.name,  self.tb.config.endsysRadius.ip,  self.tb.config.endsysRadius.username,
                                                                                         self.tb.config.endsysRadius.password,self.tb.config.endsysRadius.connection_method,self.tb.config.endsysRadius.os)
    
        print(' =======================================================================================================')
        print(' (Init_Interface) compute_the_COA_interface_nbr_from_the_slot_and_port_nbr.')
        print( 'log_IfIndex = port + slot*0x10000, (0x10000 = 65536) - (port_is_formatted_as_port_or_slot:port)')
        print('  =======================================================================================================')
        
        #set defaults
        slotNum = 1 
        portNum = 0
        coaIfNum = 0
        if_num_offsetIntValue = 65536
        #use raw value of port to get slot and port info        
        '''rawPortString = self.tb.config.netelem1.tgen.port_a.ifname
        
        if "." in rawPortString:
            rawPortStringList = rawPortString.split(".")
            lengthOfPortStringList = len(rawPortStringList)
            
            if lengthOfPortStringList == 1:
                portNum = int(rawPortStringList[0])
            if lengthOfPortStringList > 1:
                slotNum = int(rawPortStringList[0])
                portNum = int(rawPortStringList[1])
        else:
            portNum = int(rawPortString)        #set coaIfNum        
        coaIfNum = portNum + (slotNum * if_num_offsetIntValue)'''
        
        #can get coa port for test suite file
        coaIfNum = self.tb.config.Port_A_MIB2_IfIndex
        
        #Policy_Profile_Authentication.
        print('  (Step_4) Validate_Access_list_action_sets_can_be_created_and_deleted.')
        
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_action_set(  self.tb.config.netelem1.name,'1','syslog drop')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_all(   self.tb.config.netelem1.name,'1','NV','S','drop','','')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_action_set(  self.tb.config.netelem1.name,'2', 'forward mirror-destination 1')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_all(   self.tb.config.netelem1.name,'2','NV','','fwrd','','1')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_action_set(  self.tb.config.netelem1.name,'3','syslog drop cos 5 mirror-destination 2')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_all(   self.tb.config.netelem1.name,'3','NV','S','drop','5','2')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_action_set(  self.tb.config.netelem1.name,'4','forward mirror-destination 1 cos 3')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_all(   self.tb.config.netelem1.name,'4','NV','','fwrd','3','1')
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(self.tb.config.netelem1.name,'1')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_does_not_exist(self.tb.config.netelem1.name,'1')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(   self.tb.config.netelem1.name, '2')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_does_not_exist(      self.tb.config.netelem1.name,'2')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(   self.tb.config.netelem1.name,'3')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_does_not_exist(      self.tb.config.netelem1.name,'3')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(   self.tb.config.netelem1.name,'4')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_does_not_exist(      self.tb.config.netelem1.name,'4')
        
        print('  (Step_5) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(  self.tb.config.packetA.name,  self.tb.config.packetA.dst_mac,  self.tb.config.packetA.src_mac, 
                                                                        sip=self.tb.config.src_ip_a,  dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.tgenUdks.Create_IPv4_Packet(  self.tb.config.packetB.name,  self.tb.config.packetA.src_mac,  self.tb.config.packetA.dst_mac,
                                                                        sip=self.tb.config.dst_ip_a,  dip=self.tb.config.src_ip_a)
    
        self.localPolicyUdks.trafficGenerationSuiteUdks.Setup_Packet_Streams(
               self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,
               self.tb.config.packetA.name,  self.tb.config.packetB.name)
    
        self.localPolicyUdks.trafficGenerationSuiteUdks.Send_Packets_Verify_Received(
               self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,
               self.tb.config.packetA.name,  self.tb.config.packetB.name,  self.tb.config.packetB.name,  self.tb.config.packetA.name,
               self.tb.config.packetA.src_mac,  self.tb.config.packetB.src_mac,)
       
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,  self.tb.config.packetA.src_mac,
                                                                    self.tb.config.vlan_100,  self.tb.config.netelem1.tgen.port_a.ifname)
    
        self.localPolicyUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)
        print('  (Step_6a) COA: Issue_a_Change_of_Auth_connect_followed_by_a_disconnect_with_various_attribute_combinations_and_ensure_an "Ack" is_received. ')
    #
    #  Sample_Method_to_separate_and_concatenate_human_readable_match_strings_into_a_single_long_string.
    #
    #  Send_COA_connect_requests, check_that_dynamic_ACL_is_present.
    #  Follow_up_with_COA_disconnects_request_and_see_that_dynamic_ACL_has_been_removed.
    #
    #  ---------------------------------------------------------------------------------------------------------- 
        
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,
          coaIfNum, macAuthClient, '\"v:1 t:a m:ipv4dst=' + self.tb.config.dst_ip_a + '/32 a:drop\"')
        
        MatchString="[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*" + self.tb.config.packetA.hyphenated_mac + "[\\s\\S]*48"\
        "[\\s\\S]*IPDest[\\s\\S]*" + self.tb.config.dst_ip_a + "[\\s\\S]*32[\\s\\S]*1[\\s\\S]*V[\\s\\S]*drop"
        
        
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
                                                                                MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac, self.tb.config.policyName_b,  self.tb.config.vlan_400,
          coaIfNum,  macAuthClient,'\"v:1 t:d m:ipv4dst=' + self.tb.config.dst_ip_a + '/32 a:drop\"')
        
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show policy access-list',  '<dynamic-acl>' ,
                                                                                exists='false')
        #  ----------------------------------------------------------------------------------------------------------
        
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,
            coaIfNum,  macAuthClient, '\"v:1 t:a m:ipv4src=' + self.tb.config.src_ip_a + '/32 a:fwd,sys\"')
        
        MatchString="[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*" + self.tb.config.packetA.hyphenated_mac + "[\\s\\S]*48"\
        "[\\s\\S]*IPSource[\\s\\S]*" + self.tb.config.src_ip_a + "[\\s\\S]*32[\\s\\S]*1[\\s\\S]*V[\\s\\S]*fwrd"
        
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,'show policy access-list',
                                                                                MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  
          macAuthClient,'\"v:1 t:d m:ipv4src=' + self.tb.config.src_ip_a + '/32 a:fwd,sys\"')
        
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,'show policy access-list',
                                                                                '<dynamic-acl>',  exists='false')
    
    #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,
            coaIfNum,  macAuthClient,'\"v:1 t:a m:ipproto=tcp a:drop\"')
        
        MatchString="[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*" + self.tb.config.packetA.hyphenated_mac + "[\\s\\S]*48"\
        "[\\s\\S]*IPProto[\\s\\S]*6[\\s\\S]*8[\\s\\S]*V[\\s\\S]*drop"
        
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,'show policy access-list',
                                                                                MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac, self.tb.config.policyName_b,
          self.tb.config.vlan_400,  coaIfNum,  macAuthClient,'\"v:1 t:d m:ipproto=tcp a:drop\"')
        
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show policy access-list',
                                                                                  '<dynamic-acl>',  exists='false')
        #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,
            coaIfNum,  macAuthClient,'\"v:1 t:a m:ipproto=udp a:drop\"')
        
        MatchString="[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*" + self.tb.config.packetA.hyphenated_mac + "[\\s\\S]*48"\
        "[\\s\\S]*IPProto[\\s\\S]*17[\\s\\S]*8[\\s\\S]*V[\\s\\S]*drop"
        
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
                                                                                MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  macAuthClient,'\"v:1 t:d m:ipproto=udp a:drop\"')
        
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show policy access-list', 
                                                             '<dynamic-acl>',  exists='false')
    
    #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,
          coaIfNum,  macAuthClient,'\"v:1 t:a m:ipproto=udp,ipv4dst=' + self.tb.config.dst_ip_a + '/32 a:drop\"')
        
        MatchString="[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*" + self.tb.config.packetA.hyphenated_mac + "[\\s\\S]*"\
            "IPDest[\\s\\S]*" + self.tb.config.dst_ip_a + "[\\s\\S]*32[\\s\\S]*"\
            "IPProto[\\s\\S]*17[\\s\\S]*8[\\s\\S]*V[\\s\\S]*drop"
            
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
                                                            MatchString)
    #  Send_Delete_in_a_different_order_than_the_add
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  macAuthClient,'\"v:1 t:d m:ipv4dst=' + self.tb.config.dst_ip_a + '/32,ipproto=udp a:drop\"')
    
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show policy access-list',
          '<dynamic-acl>',  exists='false')
    #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
        self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,
            coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp,l4srcport=' + self.tb.config.l4_port_c + '/16,ipv4src=' + self.tb.config.src_ip_a + '/32 a:drop\"')
        
        MatchString =  "[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*" + self.tb.config.packetA.hyphenated_mac + "[\\s\\S]*"\
            "IPSource[\\s\\S]*" + self.tb.config.src_ip_a + "[\\s\\S]*32[\\s\\S]*"\
            "IPDest[\\s\\S]*" + self.tb.config.dst_ip_a + "[\\s\\S]*32[\\s\\S]*"\
            "UDPSrcPort[\\s\\S]*" + self.tb.config.l4_port_c + "[\\s\\S]*16[\\s\\S]*"\
            "UDPDestPort[\\s\\S]*" + self.tb.config.l4_port_c + "[\\s\\S]*16[\\s\\S]*"\
            "IPProto[\\s\\S]*17[\\s\\S]*8[\\s\\S]*V[\\s\\S]*drop"
        
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, "show policy access-list" , 
                                                            MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,
            coaIfNum,  macAuthClient,
          '\"v:1 t:d m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp,ipv4src=' + self.tb.config.src_ip_a + '/32 a:drop\"')
    
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  "show policy access-list",
                                                                                "<dynamic-acl>",  exists="false")
    
    #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:l4srcport=' + self.tb.config.l4_port_b + '/16,ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_a + '/16,ipproto=tcp,ipv4src=' + self.tb.config.src_ip_a + '/32 a:drop"')
    
        
        MatchString= "[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*" + self.tb.config.packetA.hyphenated_mac + "[\\s\\S]*"\
            "IPSource[\\s\\S]*" + self.tb.config.src_ip_a + "[\\s\\S]*32[\\s\\S]*"\
            "IPDest[\\s\\S]*" + self.tb.config.dst_ip_a + "[\\s\\S]*32[\\s\\S]*"\
            "TCPSrcPort[\\s\\S]*" + self.tb.config.l4_port_b + "[\\s\\S]*16[\\s\\S]*"\
            "TCPDestPort[\\s\\S]*" + self.tb.config.l4_port_a + "[\\s\\S]*16[\\s\\S]*"\
            "IPProto[\\s\\S]*6[\\s\\S]*8[\\s\\S]*V[\\s\\S]*drop"
        
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show policy access-list',
                                                                                  MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:l4dstport=' + self.tb.config.l4_port_a + '/16,ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4srcport=' + self.tb.config.l4_port_b + '/16,ipv4src=' + self.tb.config.src_ip_a + '/32,ipproto=tcp a:drop\"')
    
    #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  
          coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_b + '/16,ipproto=udp,l4srcport=' + self.tb.config.l4_port_b + '/16,ipv4src=' + self.tb.config.src_ip_a + '/32 a:drop\"')
        
        MatchString=  "[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*" + self.tb.config.packetA.hyphenated_mac + "[\\s\\S]*"\
            "IPSource[\\s\\S]*" + self.tb.config.src_ip_a + "[\\s\\S]*32[\\s\\S]*"\
            "IPDest[\\s\\S]*" + self.tb.config.dst_ip_a + "[\\s\\S]*32[\\s\\S]*"\
            "UDPSrcPort[\\s\\S]*" + self.tb.config.l4_port_b + "[\\s\\S]*16[\\s\\S]*"\
            "UDPDestPort[\\s\\S]*" + self.tb.config.l4_port_b + "[\\s\\S]*16[\\s\\S]*"\
            "IPProto[\\s\\S]*17[\\s\\S]*8[\\s\\S]*V[\\s\\S]*drop"
            
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  "show policy access-list", 
                                                                                MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  
          self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipproto=udp,l4srcport=' + self.tb.config.l4_port_b + '/16,ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_b + '/16,ipv4src=' + self.tb.config.src_ip_a + '/32 a:drop\"')
    
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',  
                                                                                '<dynamic-acl>',  exists='false')
    
    #  ----------------------------------------------------------------------------------------------------------
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipv4src=' + self.tb.config.src_ip_a + '/32,ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4srcport=' + self.tb.config.l4_port_a + '/16,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp a:drop\"')
        
        MatchString= "[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*" + self.tb.config.packetA.hyphenated_mac + "[\\s\\S]*"\
            "IPSource[\\s\\S]*" + self.tb.config.src_ip_a + "[\\s\\S]*32[\\s\\S]*"\
            "IPDest[\\s\\S]*" + self.tb.config.dst_ip_a + "[\\s\\S]*32[\\s\\S]*"\
            "TCPSrcPort[\\s\\S]*" + self.tb.config.l4_port_a + "[\\s\\S]*16[\\s\\S]*"\
            "TCPDestPort[\\s\\S]*" + self.tb.config.l4_port_c + "[\\s\\S]*16[\\s\\S]*"\
            "IPProto[\\s\\S]*6[\\s\\S]*8[\\s\\S]*V[\\s\\S]*drop"
        
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show policy access-list',
                                                                                  MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,
          self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4srcport='+ self.tb.config.l4_port_a + '/16,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp,ipv4src=' + self.tb.config.src_ip_a + '/32 a:drop\"')
    
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show policy access-list',  '<dynamic-acl>',  exists='false')
    
        print('   (Step_6b) COA: Issue_several_Change_of_Auth_connects / disconnects_with_missing/non-full_mask_values')
    
    #  Non "Default" full_mask_values_set.
    #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:l4srcport=' + self.tb.config.l4_port_b + '/16,ipv4dst=' + self.tb.config.dst_ip_a + '/16,l4dstport=' + self.tb.config.l4_port_a + '/16,ipproto=tcp,ipv4src=' + self.tb.config.src_ip_a + '/8, a:drop\"')
        
        MatchString="[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*" + self.tb.config.packetA.hyphenated_mac + "[\\s\\S]*"\
            "IPSource[\\s\\S]*" + self.tb.config.mask_ip_a + "[\\s\\S]*8[\\s\\S]*"\
            "IPDest[\\s\\S]*" + self.tb.config.mask_ip_b + "[\\s\\S]*16[\\s\\S]*"\
            "TCPSrcPort[\\s\\S]*" + self.tb.config.l4_port_b + "[\\s\\S]*16[\\s\\S]*"\
            "TCPDestPort[\\s\\S]*" + self.tb.config.l4_port_a + "[\\s\\S]*16[\\s\\S]*"\
            "IPProto[\\s\\S]*6[\\s\\S]*8[\\s\\S]*V[\\s\\S]*drop"
            
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show policy access-list',  
                                                                                MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:l4dstport=' +  self.tb.config.l4_port_a + '/16,ipv4dst=' + self.tb.config.dst_ip_a + '/16,l4srcport=' + self.tb.config.l4_port_b + '/16,ipv4src=' + self.tb.config.src_ip_a + '/8,ipproto=tcp a:drop\"')
    
     #  ----------------------------------------------------------------------------------------------------------
    
        print('  (Step_6c) COA: Issue_several_Change_of_Auth_connects_followed_by_several_disconnect_with_various_attribute_combinations (Same_Order)')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  macAuthClient, '\"v:1 t:a m:ipproto=udp a:fwd,sys,cos=4,mir=1\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  macAuthClient, '\"v:1 t:a m:l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp a:drop,mir=1,sys\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,
          self.tb.config.vlan_400,  coaIfNum,  macAuthClient,'\"v:1 t:a m:ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16 a:fwd,mir=2,cos=10\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,
          self.tb.config.vlan_400,  coaIfNum,  macAuthClient, '\"v:1 t:a m:ipproto=udp,l4srcport=' + self.tb.config.l4_port_c + '/16 a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,
            self.tb.config.vlan_400,  coaIfNum,  macAuthClient,'\"v:1 t:a m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp a:drop\"')
    
        # ipv4dst/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,
          self.tb.config.vlan_400,  coaIfNum,  macAuthClient, '\"v:1 t:a m:ipproto=udp,ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_c + '/16 a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,
            self.tb.config.vlan_400,  coaIfNum,  macAuthClient,'\"v:1 t:a m:ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16,ipv4dst=' + self.tb.config.dst_ip_a + '/32 a:drop\"')
    
        # ipv4src/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipv4src=' + self.tb.config.src_ip_a + '/32,l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipv4src=' + self.tb.config.src_ip_a + '/32,ipproto=tcp a:drop\"')
    
       # ipv4dst/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp,ipv4dst=' + self.tb.config.dst_ip_a + '/32 a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp a:drop\"')
    
        # ipv4src/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipv4src=' + self.tb.config.src_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipv4src=' + self.tb.config.src_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp a:drop\"')
    
        print(' (Step_6b) Delete_the_dynamic_COA_rules_that_were_just_added_one_by_one. Verify_an_ack_is_received.')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipproto=udp a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16 a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipproto=udp,l4srcport=' + self.tb.config.l4_port_c + '/16 a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp a:drop\"')
    
        # ipv4dst/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipproto=udp,ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_c + '/16 a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16,ipv4dst=' + self.tb.config.dst_ip_a + '/32 a:drop\"')
    
        # ipv4src/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipv4src=' + self.tb.config.src_ip_a + '/32,l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipv4src=' + self.tb.config.src_ip_a + '/32,ipproto=tcp a:drop\"')
    
       # ipv4dst/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp,ipv4dst=' + self.tb.config.dst_ip_a + '/32 a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp a:drop"')
    
        # ipv4src/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipv4src=' + self.tb.config.src_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipv4src=' + self.tb.config.src_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp a:drop\"')
    
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show policy access-list' ,
                                                             '<dynamic-acl>',  exists='false')
    
        print('  (Step_7a) COA: Issue_several_Change_of_Auth_connects_followed_by_several_disconnect_with_various_attribute_combinations (different_order)')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipproto=udp a:fwd,sys,cos=4,mir=1\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp a:drop,mir=1,sys\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16 a:fwd,mir=2,cos=10\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipproto=udp,l4srcport=' + self.tb.config.l4_port_c + '/16 a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp a:drop\"')
        # ipv4dst/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipproto=udp,ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_c + '/16 a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16,ipv4dst=' + self.tb.config.dst_ip_a + '/32 a:drop\"')
    
        # ipv4src/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipv4src=' + self.tb.config.src_ip_a + '/32,l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipv4src=' + self.tb.config.src_ip_a + '/32,ipproto=tcp a:drop"')
    
       # ipv4dst/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp,ipv4dst=' + self.tb.config.dst_ip_a + '/32 a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp a:drop\"')
    
        # ipv4src/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipv4src=' + self.tb.config.src_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:a m:ipv4src=' + self.tb.config.src_ip_a + '/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp a:drop\"')
    
        print('  (Step_7b) Delete_the_dynamic_COA_rules_that_were_just_added_one_by_one. Verify_an_ack_is_received.')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '"v:1 t:d m:ipproto=udp a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipproto=udp,l4dstport=' + self.tb.config.l4_port_c + '/16 a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipproto=tcp,l4srcport=' + self.tb.config.l4_port_c + '/16 a:drop\"')
    
        # ipv4dst/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipv4dst=' + self.tb.config.dst_ip_a + '/32,ipproto=udp,l4dstport=' + self.tb.config.l4_port_c + '/16 a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipv4dst=' + self.tb.config.dst_ip_a + '/32,ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16 a:drop\"')
    
        # ipv4src/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipproto=udp,l4srcport=' + self.tb.config.l4_port_c + '/16,ipv4src=' + self.tb.config.src_ip_a + '/32 a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp,ipv4src=' + self.tb.config.src_ip_a + '/32 a:drop\"')
    
       # ipv4dst/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipv4dst=' + self.tb.config.dst_ip_a + '/32,l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipv4dst=' + self.tb.config.dst_ip_a + '/32,ipproto=tcp a:drop\"')
    
        # ipv4src/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:l4dstport=' + self.tb.config.l4_port_c + '/16,ipv4src=' + self.tb.config.src_ip_a + '/32,ipproto=udp a:drop\"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  macAuthClient,
          '\"v:1 t:d m:ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16,ipv4src=' + self.tb.config.src_ip_a + '/32 a:drop\"')
    
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show policy access-list',
                                                              '<dynamic-acl>',  exists='false')
    #self.localPolicyUdks.Test_Case_Cleanup()
    
    # This_section_is_used_to_create_a_user-defined_keyword_to_clean_up_configuration_made_by_this_test_case.
    #<Cleanup_User-Defined_Keyword_Name>
    def Test_Case_Cleanup (self):
    #    Remove_All_Policy_Rules                          self.tb.config.netelem1.name,
        print('  (Step_29) Clean_up_config_specific_to_this_test.')
        self.localPolicyUdks.networkElementCosGenKeywords.cos_set_port_qos_profile(self.tb.config.netelem1.name,  self.tb.dut1_tgen_port_a.ifname, 'none')
        self.localPolicyUdks.networkElementCosGenKeywords.cos_delete_qos_profile(self.tb.config.netelem1.name, self.tb.config.qos_profile_all)
        self.localPolicyUdks.fdbUdks.Remove_Static_FDB_Entry_and_Validate_It_Does_Not_Exist(
                                    self.tb.config.netelem1.name, self.tb.config.dst_mac_a, self.tb.config.vlan_a, self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed( self.tb.config.netelem1.name,  self.tb.config.vlan_a)
        self.localPolicyUdks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.config.netelem1.name,  self.tb.config.vlan_b)
    
        self.localPolicyUdks.policyUdks.Disable_Policy_and_Verify_it_is_Disabled(self.tb.config.netelem1.name)
        self.localPolicyUdks.radiusSuiteUdks.configure_netlogin_mac_username_format(self.tb.config.netelem1.name,'none')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_vlanauthorization_state(self.tb.config.netelem1.name,'disable')
        self.localPolicyUdks.policyUdks.Clear_Policy_Maptable_Response_and_Verify(self.tb.config.netelem1.name,  'policy')
    
    #   set_policy_maptable_response_and_verify  self.tb.config.netelem1.name,  policy
    #    Remove_Port/s_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed  self.tb.config.netelem1.name,  self.tb.config.vlan_500  self.tb.config.netelem1.tgen.port_a.ifname,,self.tb.config.netelem1.tgen.port_b.ifname,
    #    Remove_VLAN_and_Verify_it_is_Removed  self.tb.config.netelem1.name,  self.tb.config.vlan_100
    #    Remove_VLAN_and_Verify_it_is_Removed  self.tb.config.netelem1.name,  self.tb.config.vlan_200
    #    Remove_VLAN_and_Verify_it_is_Removed  self.tb.config.netelem1.name,  self.tb.config.vlan_300
    #    Remove_VLAN_and_Verify_it_is_Removed  self.tb.config.netelem1.name,  self.tb.config.vlan_400
    #    Remove_VLAN_and_Verify_it_is_Removed  self.tb.config.netelem1.name,  self.tb.config.vlan_500
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(   self.tb.config.netelem1.name,  '1',ignore_cli_feedback='true') 
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(   self.tb.config.netelem1.name,  '2',ignore_cli_feedback='true')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(   self.tb.config.netelem1.name,  '3',ignore_cli_feedback='true')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(   self.tb.config.netelem1.name,  '4',ignore_cli_feedback='true')
    #    Remove_the_RADIUS_configuration
        # self.localPolicyUdks.radiusSuiteUdks.UnConfigure_And_Disable_Radius_Netlogin_Server(self.tb.config.netelem1.name,self.tb.config.endsysRadius.instance,self.tb.config.endsysRadius.ip)
        self.localPolicyUdks.networkElementRadiusGenKeywords.radius_clear_server(self.tb.config.netelem1.name, self.tb.config.endsysRadius.ip, self.tb.config.endsysRadius.instance)
        # def radius_clear_server(self, device_name, client_ip='', index='', **kwargs):
        self.localPolicyUdks.radiusSuiteUdks.UnConfigure_And_Disable_Radius_DynAuth_Server(self.tb.config.netelem1.name,  self.tb.config.endsysRadius.instance)
    
        self.localPolicyUdks.networkElementCliSend.send_cmd(  self.tb.config.netelem1.name,  'configure netlogin del mac-list ff:ff:ff:ff:ff:ff 48')
        self.localPolicyUdks.networkElementCliSend.send_cmd(  self.tb.config.netelem1.name,  'configure netlogin del mac-list 00:00:00:bb:bb:bb 48')
        self.localPolicyUdks.networkElementCliSend.send_cmd(  self.tb.config.netelem1.name,  'configure netlogin del mac-list 00:00:00:aa:aa:aa 48')
        self.localPolicyUdks.macAuthUdks.Disable_Macauth_and_Verify_it_is_Disabled(self.tb.config.netelem1.name, "")
        self.localPolicyUdks.macAuthUdks.Disable_Macauth_and_Verify_it_is_Disabled(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.macAuthUdks.Disable_Macauth_and_Verify_it_is_Disabled(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.policyUdks.Disable_Policy_and_Verify_it_is_Disabled(self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,'configure policy slices shared 0')
        self.localPolicyUdks.networkElementCliSend.send_cmd(  self.tb.config.netelem1.name, 'configure policy slices tci-overwrite 4')
        self.localPolicyUdks.change_policy_rule_model (self.tb.config.netelem1.name,    "Hierarchical")
    
    #    Put_the_port(s) back_on_the_default_vlan.
    #     Add_Port/s_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added  self.tb.config.netelem1.name,  ${Vlan_Default}  self.tb.config.netelem1.tgen.port_a.ifname,,self.tb.config.netelem1.tgen.port_b.ifname,
    
        self.localPolicyUdks.Basic_Policy_Cleanup()