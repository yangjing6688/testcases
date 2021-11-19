from Tests.Pytest.Functional.nonprod.Policy.Resources.PolicyBase import PolicyBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.Functional.nonprod.Policy.Resources.Policy_Test_Suite_Udks import Policy_Test_Suite_Udks

@fixture()
def test_setup_teardown(request):
    # Setup_section
    def teardown():
        request.instance.Test_Case_Cleanup()
    request.addfinalizer(teardown)

class ActionSetCOATest(PolicyBase): 
    @mark.F_1000_401
    @mark.CoaAccessList
    @mark.NO30_4
    @mark.NIGHTLY
    @mark.NO30_6 
    def test_01_Policy_Access_List_COA_Action_Set_Configuration(self):
        #[Documentation]  Test_Objective: Verify_Access-List_Action_Sets_can_be_configured.
        
    
    # Setup_here_will_run_the "Test_Suite_Setup" in_the_Resources -> SuiteUdks.robot
    #  change_this_along_the_lines_of "[Setup]  Test_Case_Setup" if_you_have_a_setup_specific_to_a_subset_of_test_cases.
        self.localPolicyUdks.Base_Test_Suite_Setup()
    
    #   This_library_allows_us_to_pause_execution_with_the "pause_execution" keyword.
    #    "import_library_dialogs"
        print('  (Step_1) Base_Setup_Enable_Policy_and_MacAuth_on_selected_ports.')
        self.localPolicyUdks.Basic_Policy_Setup()
    
        self.localPolicyUdks.policyUdks.Disable_Policy_and_Verify_it_is_Disabled(self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,  'configure policy slices tci-overwrite 1')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,  'configure policy slices shared_1')
        self.localPolicyUdks.change_policy_rule_model(self.tb.config.netelem1.name, 'Access-List')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name, ' disable clipaging')
        self.localPolicyUdks.networkElementPortGenKeywords.port_enable_state(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_a.ifname)
        self.localPolicyUdks.networkElementPortGenKeywords.port_enable_state(self.tb.config.netelem1.name, self.tb.config.netelem1.tgen.port_b.ifname)
    
    
    
    
    #    Create_VLAN_with_Name_and_Verify_it_Exists  self.tb.config.netelem1.name,  ${vlanName_100}  self.tb.config.vlan_100
    #    Create_VLAN_with_Name_and_Verify_it_Exists  self.tb.config.netelem1.name,  ${vlanName_200}  self.tb.config.vlan_200
    #    Create_VLAN_with_Name_and_Verify_it_Exists  self.tb.config.netelem1.name,  ${vlanName_300}  self.tb.config.vlan_300
    #    Create_VLAN_with_Name_and_Verify_it_Exists  self.tb.config.netelem1.name,  ${vlanName_400}  self.tb.config.vlan_400
    #    Create_VLAN_with_Name_and_Verify_it_Exists  self.tb.config.netelem1.name,  ${vlanName_500}  self.tb.config.vlan_500
    
    #    Add_Port/s_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added  self.tb.config.netelem1.name,  self.tb.config.vlan_500  self.tb.config.netelem1.tgen.port_a.ifname,,self.tb.config.netelem1.tgen.port_b.ifname,
    
        print('  (Step_2) Test_Setup_Create_and_enable_Radius_Netlogin_and_radius_DynAuth_Server.')
        self.localPolicyUdks.radiusSuiteUdks.Configure_And_Enable_Radius_Netlogin_Server(
           self.tb.config.netelem1.name,  self.tb.config.endsysRadius.instance,  self.tb.config.endsysRadius.ip,  self.tb.config.endsysRadius.port,
           self.tb.config.endsysRadius.shared_secret,  self.tb.config.netelem1.ip,  self.tb.config.netelem1.mgmt_vlan)
    
        self.localPolicyUdks.radiusSuiteUdks.Configure_And_Enable_Radius_DynAuth_Server(
           self.tb.config.netelem1.name,  self.tb.config.endsysRadius.instance,  self.tb.config.endsysRadius.ip,
           self.tb.config.endsysRadius.shared_secret,  self.tb.config.netelem1.ip,  self.tb.config.netelem1.mgmt_vlan)
    
        self.localPolicyUdks.policyUdks.Enable_Policy_and_Verify_it_is_Enabled(self.tb.config.netelem1.name)
    #    Enable_Macauth_and_Verify_it_is_Enabled  self.tb.config.netelem1.name,   -- Currently_Broken_for_EXOS
        self.localPolicyUdks.macAuthUdks.Enable_Macauth_and_Verify_it_is_Enabled(self.tb.config.netelem1.name)
    #    self.localPolicyUdks.macAuthUdks.Enable_Macauth_Port_and_Verify_it_is_Enabled(_and_verify_it_is_enabled  self.tb.config.netelem1.name,  ${port_a},${port_b} -- Currently_Broken_for_EXOS
        self.localPolicyUdks.macAuthUdks.Enable_Macauth_Port_and_Verify_it_is_Enabled(  self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,self.tb.config.netelem1.tgen.port_b.ifname)
    #
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,'configure_netlogin_add_mac-list_ff:ff:ff:ff:ff:ff_48')
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,  'configure netlogin mac username format none')
    
        print(' (Step_3) setup_connection_to_the_RADIUS_server_to_transmit_COA_requests')
        self.localPolicyUdks.endsystemConnectionManager.connect_to_endsystem_element(self.tb.config.endsysRadius.name,  self.tb.config.endsysRadius.ip,  self.tb.config.endsysradius.username,
                                                                                         self.tb.config.endsysradius.password,self.tb.config.endsysradius.connection_method,self.tb.config.endsysradius.os)
    
        print(' =======================================================================================================')
        print(' (Init_Interface) compute_the_COA_interface_nbr_from_the_slot_and_port_nbr.')
        print( 'log_IfIndex = port + slot*0x10000, (0x10000 = 65536) - (port_is_formatted_as_port_or_slot:port)')
        print('  =======================================================================================================')
        '''${slotNum} =  get_slot_from_port_string   self.tb.config.netelem1.tgen.port_a.ifname,
        ${portNum} =  fetch_from_right   self.tb.config.netelem1.tgen.port_a.ifname,   :
        coaIfNum,  Evaluate  ${portNum} + ${slotNum} * 65536'''
        
        #set defaults
        slotNum = 0
        portNum = 0
        coaIfNum = 0
        if_num_offsetIntValue = 0
        
        #use raw value of port to get slot and port info        
        rawPortString = self.tb.config.netelem1.tgen.port_a.ifname
        
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
        coaIfNum = portNum + slotNum * int(if_num_offsetIntValue)
    
    #
    #   Policy_Profile_Authentication.
    #
        print('  (Step_4) Validate_Access_list_action_sets_can_be_created_and_deleted.')
    #    Clear_Netlogin_Port_State  self.tb.config.netelem1.name,  self.tb.config.netelem1.tgen.port_a.ifname,,self.tb.config.netelem1.tgen.port_b.ifname,
    #    Clear_Syslog  self.tb.config.netelem1.name,
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_action_set(  self.tb.config.netelem1.name,'1','syslog_drop')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_all(   self.tb.config.netelem1.name,'1','NV','S','drop','EMPTY','EMPTY')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_action_set(  self.tb.config.netelem1.name,'2','mirror 1','forward')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_all(   self.tb.config.netelem1.name,'2','NV','EMPTY','fwrd','EMPTY','1')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_action_set(  self.tb.config.netelem1.name,'3','syslog','drop','cos 5','mirror 2')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_all(   self.tb.config.netelem1.name,'3','NV','S','drop','5','2')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_access_list_action_set(  self.tb.config.netelem1.name,'4','mirror 1','forward','cos 3')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_all(   self.tb.config.netelem1.name,'4','NV','EMPTY','fwrd','3','1')
    
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(self.tb.config.netelem1.name,'1')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_does_not_exist(self.tb.config.netelem1.name,'1')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(   self.tb.config.netelem1.name, '2')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_does_not_exist(      self.tb.config.netelem1.name,'2')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(   self.tb.config.netelem1.name,'3')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_does_not_exist(      self.tb.config.netelem1.name,'3')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(   self.tb.config.netelem1.name,'4')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_verify_acl_action_set_does_not_exist(      self.tb.config.netelem1.name,'4')
    #self.localPolicyUdks.TrafficGenerationUdks.Create_IPv4_Packet(
    #    [Arguments]  ${packet_name}  ${dmac}=${NONE}        ${smac}=${NONE}           ${vlan_id}=${NONE}
    #                              ${vlan_prio}=${NONE}   ${vlan_tpid}=${NONE}      ${dip}=${NONE}
    #                              ${sip}=${NONE}         ${header_len}=${NONE}     ${ttl}=${NONE}
    #                              ${proto}=${NONE}       ${tos}=${NONE}            ${total_len}=${NONE}
    #                              ${id}=${NONE}          ${flags}=${NONE}          ${frag_offset}=${NONE}
    #                              ${checksum}=${NONE}    ${packet_len}=${NONE}
    
    
        print('  (Step_5) Create_IP_frames_to_validate_and_send_to_create_initial_authentication.')
        self.localPolicyUdks.trafficGenerationUdks.Create_IPv4_Packet(  self.tb.config.packetA.name,  self.tb.config.packetA.dst_mac,  self.tb.config.packetA.src_mac,  
                                                                        sip=self.tb.config.src_ip_a,  dip=self.tb.config.dst_ip_a)
        self.localPolicyUdks.trafficGenerationUdks.Create_IPv4_Packet(  self.tb.config.packetB.name,  self.tb.config.packetA.src_mac,  self.tb.config.packetA.dst_mac,  
                                                                        sip=self.tb.config.dst_ip_a,  dip=self.tb.config.src_ip_a)
    
        self.localPolicyUdkstrafficGenerationSuiteUdks.Setup_Packet_Streams(
               self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,
               self.tb.config.packetA.name,  self.tb.config.packetB.name)
    
        self.localPolicyUdkstrafficGenerationSuiteUdks.Send_Packets_Verify_Received(
               self.tb.config.tgen_ports.netelem1.port_a,  self.tb.config.tgen_ports.netelem1.port_b,
               self.tb.config.packetA.name,  self.tb.config.packetB.name,  self.tb.config.packetB.name,  self.tb.config.packetA.name,
               self.tb.config.packetA.src_mac,  self.tb.config.packetB.src_mac,)
    
        self.localPolicyUdks.networkElementFdbGenKeywords.fdb_verify_entry_exists(self.tb.config.netelem1.name,  self.tb.config.packetA.src_mac,
                                                                    self.tb.config.vlan_100,   self.tb.config.netelem1.tgen.port_a.ifname)
    
        self.localPolicyUdks.radiusSuiteUdks.Clear_Syslog(self.tb.config.netelem1.name)
        print('  (Step_6a) COA: Issue_a_Change_of_Auth_connect_followed_by_a_disconnect_with_various_attribute_combinations_and_ensure_an "Ack" is_received. ')
    #
    #  Sample_Method_to_separate_and_concatenate_human_readable_match_strings_into_a_single_long_string.
    #
        #MatchString=  catenate_SEPARATOR=
        MatchString="[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*"+self.tb.config.packetA.hyphenated_mac+"\[\\s\\S]*"\
            "IPSource[\\s\\S]*"+self.tb.config.src_ip_a+",\[\\s\\S]*32[\\s\\S]*"\
            "IPDest[\\s\\S]*"+self.tb.config.dst_ip_a+",\[\\s\\S]*32[\\s\\S]*"\
            "UDPSrcPort[\\s\\S]*"+self.tb.config.l4_port_c+"\[\\s\\S]*"\
            "TCPSrcPort[\\s\\S]*"+self.tb.config.l4_port_c+"\[\\s\\S]*"\
            "UDPDestPort[\\s\\S]*"+self.tb.config.l4_port_c+"\[\\s\\S]*"\
            "TCPDestPort[\\s\\S]*"+self.tb.config.l4_port_c+"\[\\s\\S]*"\
            "IPProto[\\s\\S]*6[\\s\\S]*32[\\s\\S]*"\
            "IPProto[\\s\\S]*17[\\s\\S]*32[\\s\\S]*"
    
    #
    #  Send_COA_connect_requests, check_that_dynamic_ACL_is_present.
    #  Follow_up_with_COA_disconnects_request_and_see_that_dynamic_ACL_has_been_removed.
    #
    #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,
          coaIfNum,  self.tb.config.macAuthClient,'"v:1_t:a_m:ipv4dst=' + self.tb.config.dst_ip_a + '/32_a:drop"' )
    
        MatchString="[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*"+self.tb.config.packetA.hyphenated_mac+"\[\\s\\S]*"\
            "IPDest[\\s\\S]*"+self.tb.config.dst_ip_a+",\[\\s\\S]*32[\\s\\S]*"\
            "\\| V\\| \\|drop\\|       \\|"
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show_policy_access-list',
                                                                                MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac, self.tb.config.policyName_b,  self.tb.config.vlan_400,
          coaIfNum,  self.tb.config.macAuthClient,'"v:1_t:d_m:ipv4dst=self.tb.config.dst_ip_a,/32_a:drop"')
        
        self.localPolicyUdks.networkElementCliSend.send_cmdverify_output_regex(self.tb.config.netelem1.name,  'show_policy_access-list',  '<dynamic-acl>' ,
                                                                                exists='false')
    #
    #
    #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,
            coaIfNum,  self.tb.config.macAuthClient, '"v:1_t:a_m:ipv4src=self.tb.config.src_ip_a,/32_a:fwd,sys"')
    
        MatchString="[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*"+self.tb.config.packetA.hyphenated_mac+"\[\\s\\S]*"\
            "IPSource[\\s\\S]*"+self.tb.config.src_ip_a+",\[\\s\\S]*32[\\s\\S]*"\
            "\\| V\\|S\\|fwrd\\|       \\|"
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,'show_policy_access-list',
                                                                                MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  
          self.tb.config.macAuthClient,'"v:1_t:d_m:ipv4src=self.tb.config.src_ip_a,/32_a:fwd,sys"')
        
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,'show_policy_access-list',
                                                                                '<dynamic-acl>',  exists='false')
    
    #
    #
    #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,
            coaIfNum,  self.tb.config.macAuthClient,'"v:1_t:a_m:ipproto=tcp_a:drop"')
    
        MatchString="[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*"+self.tb.config.packetA.hyphenated_mac+"\[\\s\\S]*"\
            "IPProto[\\s\\S]*6[\\s\\S]*8[\\s\\S]*"\
            "\\| V\\| \\|drop\\|       \\|"
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,'show_policy_access-list',
                                                                                MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac, self.tb.config.policyName_b,
          self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,'"v:1_t:d_m:ipproto=tcp_a:drop"')
        
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show_policy_access-list',
                                                                                  '<dynamic-acl>',  exists='false')
    
    #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,
            coaIfNum,  self.tb.config.macAuthClient,'"v:1_t:a_m:ipproto=udp_a:drop"')
    
        MatchString=  catenate_SEPARATOR="[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*"+self.tb.config.packetA.hyphenated_mac+"\[\\s\\S]*"\
            "IPProto[\\s\\S]*17[\\s\\S]*8[\\s\\S]*"\
            "\\| V\\| \\|drop\\|       \\|"
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show_policy_access-list',
                                                                                MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,'"v:1_t:d_m:ipproto=udp_a:drop"')
        
        self.localPolicyUdks.networkElementCliSend.send_cmdverify_output_regex(self.tb.config.netelem1.name,  'show_policy_access-list', 
                                                             '<dynamic-acl>',  exists='false')
    
    #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,
          coaIfNum,  self.tb.config.macAuthClient,'"v:1_t:a_m:ipproto=udp,ipv4dst=self.tb.config.dst_ip_a,/32_a:drop"')
    
        MatchString="[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*"+self.tb.config.packetA.hyphenated_mac+"\[\\s\\S]*"\
            "IPDest[\\s\\S]*self.tb.config.dst_ip_a,\[\\s\\S]*32[\\s\\S]*"\
            "IPProto[\\s\\S]*17[\\s\\S]*8[\\s\\S]*"\
            "\\| V\\| \\|drop\\|       \\|"
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show_policy_access-list',
                                                            MatchString)
    
    #  Send_Delete_in_a_different_order_than_the_add
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,'"v:1_t:d_m:ipv4dst=self.tb.config.dst_ip_a,/32,ipproto=udp_a:drop"')
    
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show_policy_access-list',
          '<dynamic-acl>',  exists='false')
    
    #  ----------------------------------------------------------------------------------------------------------
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
        self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,
            coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipv4dst=' + self.tb.config.dst_ip_a + ',/32,l4dstport='+self.tb.config.l4_port_c+'/16,ipproto=udp,l4srcport='+ +self.tb.config.l4_port_c+ +'/16,ipv4src=' + self.tb.config.src_ip_a + ',/32, a:drop"')
    
        MatchString =  "[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*self.tb.config.packetA.hyphenated_mac\[\\s\\S]*"\
            "IPSource[\\s\\S]*" + self.tb.config.src_ip_a + ",\[\\s\\S]*32[\\s\\S]*"\
            "IPDest[\\s\\S]*" + self.tb.config.dst_ip_a + ",\[\\s\\S]*32[\\s\\S]*"\
            "UDPSrcPort[\\s\\S]*" + self.tb.config.l4_port_c + "\[\\s\\S]*16[\\s\\S]*"\
            "UDPDestPort[\\s\\S]*" + self.tb.config.l4_port_c + "\[\\s\\S]*16[\\s\\S]*"\
            "IPProto[\\s\\S]*17[\\s\\S]*8[\\s\\S]*"\
            "\\| V\\| \\|drop\\|       \\|"
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, "show_policy_access-list" , 
                                                            MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,
            coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipv4dst=' + self.tb.config.dst_ip_a + ',/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp,ipv4src=' + self.tb.config.src_ip_a + ',/32, a:drop"')
    
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  "show_policy_access-list",
                                                                                "<dynamic-acl>",  exists="false")
    
    #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:l4srcport=' + self.tb.config.l4_port_b + '/16,ipv4dst=' + self.tb.config.dst_ip_a + ',/32,l4dstport=' + self.tb.config.l4_port_a + '/16,ipproto=tcp,ipv4src=' + self.tb.config.src_ip_a + ',/32, a:drop"')
    
        MatchString= "[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*" + self.tb.config.packetA.hyphenated_mac + "\[\\s\\S]*"\
            "IPSource[\\s\\S]*" + self.tb.config.src_ip_a + ",\[\\s\\S]*32[\\s\\S]*"\
            "IPDest[\\s\\S]*" + self.tb.config.dst_ip_a + ",\[\\s\\S]*32[\\s\\S]*"\
            "TCPSrcPort[\\s\\S]*" + self.tb.config.l4_port_b + "\[\\s\\S]*16[\\s\\S]*"\
            "TCPDestPort[\\s\\S]*" + self.tb.config.l4_port_a + "\[\\s\\S]*16[\\s\\S]*"\
            "IPProto[\\s\\S]*6[\\s\\S]*8[\\s\\S]*"\
            "\\| V\\| \\|drop\\|       \\|"
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show_policy_access-list',
                                                                                  MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:l4dstport=' + self.tb.l4_port_a + '/16,ipv4dst=' + self.tb.config.dst_ip_a + ',/32,l4srcport=' + self.tb.config.l4_port_b + '/16,ipv4src=' + self.tb.config.src_ip_a + ',/32,ipproto=tcp_a:drop"')
    
    #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  
          coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipv4dst=' + self.tb.config.dst_ip_a + ',/32,l4dstport=' + self.tb.config.l4_port_b + '/16,ipproto=udp,l4srcport=' + self.tb.config.l4_port_b + '/16,ipv4src=' + self.tb.config.src_ip_a + ',/32_a:drop"')
    
        MatchString=  "[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*" + self.tb.config.packetA.hyphenated_mac + "\[\\s\\S]*"\
            "IPSource[\\s\\S]*" + self.tb.config.src_ip_a + ",\[\\s\\S]*32[\\s\\S]*"\
            "IPDest[\\s\\S]*" + self.tb.config.dst_ip_a + ",\[\\s\\S]*32[\\s\\S]*"\
            "UDPSrcPort[\\s\\S]*" + self.tb.config.l4_port_b + "\[\\s\\S]*16[\\s\\S]*"\
            "UDPDestPort[\\s\\S]*" + self.tb.config.l4_port_b + "\[\\s\\S]*16[\\s\\S]*"\
            "IPProto[\\s\\S]*17[\\s\\S]*8[\\s\\S]*"\
            "\\| V\\| \\|drop\\|       \\|"
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  "show_policy_access-list", 
                                                                                MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  
          self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipproto=udp,l4srcport=' + self.tb.config.l4_port_b + '/16,ipv4dst=' + self.tb.config.dst_ip_a + ',/32,l4dstport=' + self.tb.config.l4_port_b + '/16,ipv4src=' + self.tb.config.src_ip_a + ',/32_a:drop"')
    
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show_policy_access-list',  
                                                                                '<dynamic-acl>',  exists='false')
    
    #  ----------------------------------------------------------------------------------------------------------
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipv4src=' + self.tb.config.src_ip_a + ',/32,ipv4dst=' + self.tb.config.dst_ip_a + ',/32,l4srcport=' + self.tb.config.l4_port_a + '/16,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp_a:drop"')
    
        MatchString= "[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*" + self.tb.config.packetA.hyphenated_mac + "\[\\s\\S]*"\
            "IPSource[\\s\\S]*" + self.tb.config.src_ip_a + ",\[\\s\\S]*32[\\s\\S]*"\
            "IPDest[\\s\\S]*" + self.tb.config.dst_ip_a + ",\[\\s\\S]*32[\\s\\S]*"\
            "TCPSrcPort[\\s\\S]*" + self.tb.config.l4_port_a + "\[\\s\\S]*16[\\s\\S]*"\
            "TCPDestPort[\\s\\S]*" +  self.tb.config.l4_port_c + "\[\\s\\S]*16[\\s\\S]*"\
            "IPProto[\\s\\S]*6[\\s\\S]*8[\\s\\S]*"\
            "\\| V\\| \\|drop\\|       \\|"
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name, 'show_policy_access-list',
                                                                                  MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,
          self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipv4dst=self.tb.config.dst_ip_a,/32,l4srcport=' + self.tb.config.l4_port_a + '/16,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp,ipv4src=' + self.tb.config.src_ip_a + ',/32_a:drop"')
    
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show_policy_access-list',  '<dynamic-acl>',  exists='false')
    
        print('   (Step_6b) COA: Issue_several_Change_of_Auth_connects / disconnects_with_missing/non-full_mask_values')
    
    #  Non "Default" full_mask_values_set.
    #  ----------------------------------------------------------------------------------------------------------
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:l4srcport=' + self.tb.config.l4_port_b + '/16,ipv4dst=' + self.tb.config.dst_ip_a + ',/16,l4dstport=' + self.tb.config.l4_port_a + '/16,ipproto=tcp,ipv4src=' + self.tb.config.src_ip_a + ',/8, a:drop"')
    
        MatchString="[\\s\\S]*<dynamic-acl>[\\s\\S]*MACSource[\\s\\S]*" + self.tb.config.packetA.hyphenated_mac + "\[\\s\\S]*"\
            "IPSource[\\s\\S]*" + self.tb.config.mask_ip_a + "\[\\s\\S]*8[\\s\\S]*"\
            "IPDest[\\s\\S]*" + self.tb.config.mask_ip_b + "\[\\s\\S]*16[\\s\\S]*"\
            "TCPSrcPort[\\s\\S]*" + self.tb.config.l4_port_b + "\[\\s\\S]*16[\\s\\S]*"\
            "TCPDestPort[\\s\\S]*" + self.tb.config.l4_port_a + "\[\\s\\S]*16[\\s\\S]*"\
            "IPProto[\\s\\S]*6[\\s\\S]*8[\\s\\S]*"\
            "\\| V\\| \\|drop\\|       \\|"
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show_policy_access-list',  
                                                                                MatchString)
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:l4dstport=' + self.tb.config.l4_port_a + '/16,ipv4dst=' + self.tb.config.dst_ip_a + ',/16,l4srcport=' + self.tb.config.l4_port_b + '/16,ipv4src=' + self.tb.config.src_ip_a + ',/8,ipproto=tcp_a:drop"')
    
    
    
    
    #  ----------------------------------------------------------------------------------------------------------
    
        print('  (Step_6c) COA: Issue_several_Change_of_Auth_connects_followed_by_several_disconnect_with_various_attribute_combinations (Same_Order)')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient, '"v:1_t:a_m:ipproto=udp_a:fwd,sys,cos=4,mir=1"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  
          self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient, '"v:1_t:a_m:l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp_a:drop,mir=1,sys"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,
          self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,'"v:1_t:a_m:ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16_a:fwd,mir=2,cos=10"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,
          self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient, '"v:1_t:a_m:ipproto=udp,l4srcport='+ self.tb.config.l4_port_c + '/16_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,
            self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,'"v:1_t:a_m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp_a:drop"')
    
        # ipv4dst/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,
          self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient, '"v:1_t:a_m:ipproto=udp,ipv4dst=' + self.tb.config.dst_ip_a + ',/32,l4dstport=' + self.tb.config.l4_port_c + '/16_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,
            self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,'"v:1_t:a_m:ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16,ipv4dst=' + self.tb.config.dst_ip_a + ',/32_a:drop"')
    
        # ipv4src/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipv4src=' + self.tb.config.src_ip_a + ',/32,l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipv4src=' + self.tb.config.src_ip_a + ',/32,ipproto=tcp_a:drop"')
    
       # ipv4dst/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp,ipv4dst=' + self.tb.config.dst_ip_a + ',/32_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipv4dst=self.tb.config.dst_ip_a,/32,l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp_a:drop"')
    
        # ipv4src/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipv4src=' + self.tb.config.src_ip_a + ',/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipv4src=' + self.tb.config.src_ip_a + ',/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp_a:drop"')
    
        print(' (Step_6b) Delete_the_dynamic_COA_rules_that_were_just_added_one_by_one. Verify_an_ack_is_received.')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipproto=udp_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipproto=udp,l4srcport=' + self.tb.config.l4_port_c + '/16_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp_a:drop"')
    
        # ipv4dst/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipproto=udp,ipv4dst=' + self.tb.config.dst_ip_a + ',/32,l4dstport=' + self.tb.config.l4_port_c + '/16_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16,ipv4dst=' + self.tb.config.dst_ip_a + ',/32_a:drop"')
    
        # ipv4src/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipv4src=' + self.tb.config.src_ip_a + ',/32,l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipv4src=' + self.tb.config.src_ip_a + ',/32,ipproto=tcp_a:drop"')
    
       # ipv4dst/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp,ipv4dst=' +self.tb.config.dst_ip_a + ',/32_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipv4dst=' + self.tb.config.dst_ip_a + ',/32,l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp_a:drop"')
    
        # ipv4src/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipv4src=' + self.tb.config.src_ip_a + ',/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipv4src=' + self.tb.config.src_ip_a + ',/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp_a:drop"')
    
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show_policy_access-list' ,
                                                             '<dynamic-acl>',  exists='false')
    
    
        print('  (Step_7a) COA: Issue_several_Change_of_Auth_connects_followed_by_several_disconnect_with_various_attribute_combinations (different_order)')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipproto=udp_a:fwd,sys,cos=4,mir=1"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp_a:drop,mir=1,sys"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16_a:fwd,mir=2,cos=10"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipproto=udp,l4srcport=' + self.tb.config.l4_port_c + '/16_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp_a:drop"')
    
        # ipv4dst/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipproto=udp,ipv4dst=' + self.tb.config.dst_ip_a + ',/32,l4dstport=' + self.tb.config.l4_port_c + '/16_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16,ipv4dst=' + self.tb.config.dst_ip_a + ',/32_a:drop"')
    
        # ipv4src/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipv4src=' + self.tb.config.src_ip_a + ',/32,l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipv4src=' + self.tb.config.src_ip_a + ',/32,ipproto=tcp_a:drop"')
    
       # ipv4dst/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp,ipv4dst=' + self.tb.config.dst_ip_a + ',/32_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipv4dst=' + self.tb.config.dst_ip_a + ',/32,l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp_a:drop"')
    
        # ipv4src/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipv4src=' + self.tb.config.src_ip_a + ',/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=udp_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:a_m:ipv4src=' + self.tb.config.src_ip_a + ',/32,l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp_a:drop"')
    
        print('  (Step_7b) Delete_the_dynamic_COA_rules_that_were_just_added_one_by_one. Verify_an_ack_is_received.')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipproto=udp_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipproto=udp,l4dstport=' + self.tb.config.l4_port_c + '/16_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:l4dstport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipproto=tcp,l4srcport=' + self.tb.config.l4_port_c + '/16_a:drop"')
    
        # ipv4dst/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipv4dst=' + self.tb.config.dst_ip_a + ',/32,ipproto=udp,l4dstport=' + self.tb.config.l4_port_c + '/16_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipv4dst=' + self.tb.config.dst_ip_a + ',/32,ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16_a:drop"')
    
        # ipv4src/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipproto=udp,l4srcport=' + self.tb.config.l4_port_c + '/16,ipv4src=' + self.tb.config.src_ip_a +' ,/32_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=tcp,ipv4src=' + self.tb.config.src_ip_a + ',/32_a:drop"')
    
       # ipv4dst/l4src
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipv4dst=' + self.tb.config.dst_ip_a + ',/32,l4srcport=' + self.tb.config.l4_port_c + '/16,ipproto=udp_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:l4srcport=' + self.tb.config.l4_port_c + '/16,ipv4dst=' + self.tb.config.dst_ip_a + ',/32,ipproto=tcp_a:drop"')
    
        # ipv4src/l4dst
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:l4dstport=' + self.tb.config.l4_port_c + '/16,ipv4src=' + self.tb.config.src_ip_a + ',/32,ipproto=udp_a:drop"')
    
        self.localPolicyUdks.radiusSuiteUdks.Send_COA_Auth_Request(
          self.tb.config.endsysRadius.name,  self.tb.config.netelem1.ip,  self.tb.config.packetA.hyphenated_mac,  self.tb.config.policyName_b,  self.tb.config.vlan_400,  coaIfNum,  self.tb.config.macAuthClient,
          '"v:1_t:d_m:ipproto=tcp,l4dstport=' + self.tb.config.l4_port_c + '/16,ipv4src=' + self.tb.config.src_ip_a + ',/32_a:drop"')
    
        self.localPolicyUdks.networkElementCliSend.send_cmd_verify_output_regex(self.tb.config.netelem1.name,  'show_policy_access-list',
                                                              '<dynamic-acl>',  exists='false')
    
    
        #self.localPolicyUdks.Test_Case_Cleanup()
    
    
    
    # This_section_is_used_to_create_a_user-defined_keyword_to_clean_up_configuration_made_by_this_test_case.
    #<Cleanup_User-Defined_Keyword_Name>
    def Test_Case_Cleanup (self):
    #    Remove_All_Policy_Rules                          self.tb.config.netelem1.name,
    
        #
        print('  (Step_29) Clean_up_config_specific_to_this_test.')
        self.localPolicyUdks.policyUdks.Disable_Policy_and_Verify_it_is_Disabled(self.tb.config.netelem1.name)
        self.localPolicyUdks.radiusSuiteUdks.configure_netlogin_mac_username_format('none')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_set_vlanauthorization_state(self.tb.config.netelem1.name,'disable')
        self.localPolicyUdks.policyUdks.Clear_Policy_Maptable_Response_and_Verify(self.tb.config.netelem1.name,  'policy')
    
    #   set_policy_maptable_response_and_verify  self.tb.config.netelem1.name,  policy
    #    Remove_Port/s_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed  self.tb.config.netelem1.name,  self.tb.config.vlan_500  self.tb.config.netelem1.tgen.port_a.ifname,,self.tb.config.netelem1.tgen.port_b.ifname,
    #    Remove_VLAN_and_Verify_it_is_Removed  self.tb.config.netelem1.name,  self.tb.config.vlan_100
    #    Remove_VLAN_and_Verify_it_is_Removed  self.tb.config.netelem1.name,  self.tb.config.vlan_200
    #    Remove_VLAN_and_Verify_it_is_Removed  self.tb.config.netelem1.name,  self.tb.config.vlan_300
    #    Remove_VLAN_and_Verify_it_is_Removed  self.tb.config.netelem1.name,  self.tb.config.vlan_400
    #    Remove_VLAN_and_Verify_it_is_Removed  self.tb.config.netelem1.name,  self.tb.config.vlan_500
    
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(   self.tb.config.netelem1.name,  '1',expect_error='true')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(   self.tb.config.netelem1.name,  '2',expect_error='true')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(   self.tb.config.netelem1.name,  '3',expect_error='true')
        self.localPolicyUdks.networkElementPolicyGenKeywords.policy_clear_access_list_action_set(   self.tb.config.netelem1.name,  '4',expect_error='true')
    #    Remove_the_RADIUS_configuration
        self.localPolicyUdks.radiusSuiteUdks.UnConfigure_And_Disable_Radius_Netlogin_Server(self.tb.config.netelem1.name,self.tb.config.endsysRadius.instance)
        self.localPolicyUdks.radiusSuiteUdks.UnConfigure_And_Disable_Radius_DynAuth_Server(self.tb.config.netelem1.name,  self.tb.config.endsysRadius.instance)
        self.localPolicyUdks.networkElementCliSend.send_cmd(  self.tb.config.netelem1.name,  'configure netlogin del mac-list ff:ff:ff:ff:ff:ff 48')
        self.localPolicyUdks.macAuthUdks.Disable_Macauth_and_Verify_it_is_Disabled(self.tb.config.netelem1.name)
        self.localPolicyUdks.macAuthUdks.Disable_Macauth_and_Verify_it_is_Disabled(self.tb.config.netelem1.name,self.tb.config.netelem1.tgen.port_a.ifname,
                                                                                   self.tb.config.netelem1.tgen.port_b.ifname)
        self.localPolicyUdks.policyUdks.Disable_Policy_and_Verify_it_is_Disabled(self.tb.config.netelem1.name)
        self.localPolicyUdks.networkElementCliSend.send_cmd(self.tb.config.netelem1.name,'configure_policy_slices_shared 0')
        self.localPolicyUdks.networkElementCliSend.send_cmd(  self.tb.config.netelem1.name, 'configure_policy_slices_tci-overwrite 4')
        self.localPolicyUdks.change_policy_rule_model (self.tb.config.netelem1.name,    "Hierarchical")
    
    
    #    Put_the_port(s) back_on_the_default_vlan.
    #     Add_Port/s_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added  self.tb.config.netelem1.name,  ${Vlan_Default}  self.tb.config.netelem1.tgen.port_a.ifname,,self.tb.config.netelem1.tgen.port_b.ifname,
    
        self.localPolicyUdks.Basic_Policy_Cleanup()