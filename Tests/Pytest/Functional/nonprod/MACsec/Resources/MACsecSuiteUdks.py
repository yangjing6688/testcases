from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from Tests.Pytest.Functional.nonprod.Resources.PlatformGenericSuiteUdks import PlatformGenericSuiteUdks
from ExtremeAutomation.Keywords.TrafficKeywords.ProtocolEmulationTcpKeywords import ProtocolEmulationTcpKeywords
from Tests.Pytest.Functional.nonprod.Resources.TrafficSuiteUdks import TrafficGenerationSuiteUdks
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementMacsecGenKeywords import NetworkElementMacsecGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementCliSend import NetworkElementCliSend
import pytest




class MACsecSuiteUdks():
    
    """ Documentation_User_Defined_Keywords (UDKs) used_by_the_MACsec_ROBOT_Test_Suite """
    
    def __init__(self, pytestConfigHelper):
        self.pytestConfigHelper = pytestConfigHelper        
        self.platformGenericSuiteUdks = PlatformGenericSuiteUdks()
        self.localTrafficSuiteUdks = TrafficGenerationSuiteUdks()
        self.defaultLibrary = DefaultLibrary()
        self.macsec = self.defaultLibrary.apiLowLevelApis.macsec
        self.tgenUdks = self.defaultLibrary.apiUdks.trafficGenerationUdks
        self.vlanUdks = self.defaultLibrary.apiUdks.vlanUdks
        self.send_cli = self.defaultLibrary.deviceNetworkElement.networkElementCliSend
        self.portApi = self.defaultLibrary.apiLowLevelApis.port
        self.vlanApi = self.defaultLibrary.apiLowLevelApis.vlan
        self.tcp = ProtocolEmulationTcpKeywords()
        self.traffic_port = self.defaultLibrary.apiLowLevelTrafficApis.trafficPortKeywords
        self.networkElementMacsecGenKeywords = NetworkElementMacsecGenKeywords()
        self.networkElementCliSend = NetworkElementCliSend()
    
    def Macsec_Verify_Port_Connect_Secure(self, dut_name, port):
        # Verify the MACsec connect status is SECURE
        self.networkElementMacsecGenKeywords.macsec_verify_port_connection_status(dut_name, port,'SECURE', wait_for=True, max_wait=10)

    def Macsec_Verify_Port_Connect_Pending(self, dut_name, port):
        # Verify the MACsec connect status is PENDING
       
        self.networkElementMacsecGenKeywords.macsec_verify_port_connection_status(dut_name, port, 'PENDING', wait_for=True, max_wait=10)

    def Set_Macsec_Cipher_Suite(self, dut_name, port, cipher_suite='gcm-aes-128'):
        # Configure specified cipher suite on given port.  If the
        # cipher_suite argument is ommitted then the port will be
        # set to the default cipher suite.
        if cipher_suite == 'gcm-aes-128':
            self.networkElementMacsecGenKeywords.macsec_set_cipher_suite_128(dut_name, port)
        elif cipher_suite == 'gcm-aes-256':
            self.networkElementMacsecGenKeywords.macsec_set_cipher_suite_256(dut_name, port)
        else:
            pytest.fail('Unsupported cipher suite {0}'.format(cipher_suite))

    def Macsec_Set_Pending_PN_Exhaustion(self, dut_name, pn_exhaustion ):
        # Debug command to lower the packet number (PN) threshold.
        # When the Key Server detects Tx or Rx PN exceeds this value
        # it will refresh the SAK.  Lowering the value is useful
        # for SAK rollover testing.
        self.networkElementCliSend.send_cmd(dut_name, 'debug macsec configure kay ' + str(pn_exhaustion) )

    def Reboot_Slot_in_EXOS_Stack(self, dut_name, slot):
        # Reboot single slot in a stacked system.  If this keyword
        # is run on a standalone then the system will be rebooted.
        
        self.networkElementCliSend.send_cmd(dut_name, 'reboot slot ' +  str(slot), wait_for_prompt=False)
        self.networkElementCliSend.send_cmd(dut_name, 'y', heck_initial_prompt=False)


    def Test_Suite_Setup(self):
        self.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()
        self.Upgrade_Netelems()

        self.Create_MACsec_DUT_Dictionary(self.pytestConfigHelper.dut1)
        self.Create_MACsec_DUT_Dictionary(self.pytestConfigHelper.dut2)
        
        # Added to cleanup
        self.Disable_and_Verify_Macsec_on_Port(self.pytestConfigHelper.dut1.name, 
                                               self.pytestConfigHelper.dut1.ca,
                                               self.pytestConfigHelper.dut1.port, 
                                               ignore_error="Error", 
                                               ignore_cli_feedback=True) 
        self.Disable_and_Verify_Macsec_on_Port(self.pytestConfigHelper.dut2.name, 
                                               self.pytestConfigHelper.dut2.ca,
                                               self.pytestConfigHelper.dut2.port, 
                                               ignore_error="Error", 
                                               ignore_cli_feedback=True)
        
        self.Setup_DUT(self.pytestConfigHelper.dut1)
        self.Setup_DUT(self.pytestConfigHelper.dut2)
        
        
        
        self.Setup_Traffic_Generator() 
        self.portApi.port_verify_operational(self.pytestConfigHelper.dut1.name, 
                                             self.pytestConfigHelper.dut1.tg_port, 
                                             wait_for=True, wait_max=10)
        self.portApi.port_verify_operational(self.pytestConfigHelper.dut2.name, 
                                             self.pytestConfigHelper.dut2.tg_port, 
                                             wait_for=True, wait_max=10)

    def Test_Suite_Cleanup(self):
        self.Cleanup_DUT(self.pytestConfigHelper.dut1)
        self.Cleanup_DUT(self.pytestConfigHelper.dut1)

    #----------------------------------------------------------------------------------------------------------
    
    
    def Create_List_of_Ports(self, port_dict):
        ports = []
        for port_key in port_dict.keys():
            port = port_dict[port_key]
            if port and 'ifname' in port:
                ports.append(port['ifname'])
        return ports
    
    def Create_List_of_MACsec_Ports(self, port_dict):
        ports = []
        for port_key in port_dict.keys():
            value = port_dict[port_key]
            if value:
                ports.append(value)
        return ports
    
    def Create_MACsec_DUT_Dictionary(self, dut):
        """ Copy "netelem" dictionary_into_new "dut" and_add_keys for_MACsec-capable_ports_and_traffic_VLAN """
        #ISL Ports                                                                      
        isl_ports = self.Create_List_of_Ports(dut.isl)
        dut.isl_ports = isl_ports
       
        #TGEN Ports
        tgen_ports = self.Create_List_of_Ports(dut.tgen)
        dut.tgen_ports = tgen_ports
        
        ports_128 = self.Create_List_of_MACsec_Ports(dut.macsec.gcm_aes_128)
        dut.ports_128 = ports_128
        ports_256 = self.Create_List_of_MACsec_Ports(dut.macsec.gcm_aes_256)
        dut.ports_256 = ports_256
        
        print("ports_128: " + str(ports_128))
        print("ports_256: " + str(ports_256))
        
        dut.ports = ports_128 + ports_256
        dut.port = dut.ports[0]
        dut.port_a = dut.ports[0]
        dut.port_b = dut.ports[1]
        if len(ports_128) == 0:
            dut.port128 = None
        else:
            dut.port128 = ports_128[0]
        if len(ports_256) == 0:
            dut.port256 = None
        else:
            dut.port256 = ports_256[0]
        dut.ports_all = dut.ports
        # ${ports_all}=  Get_Variable_Value  ${elem.macsec.ports.all}
        
        dut.ca = self.pytestConfigHelper.config.ca256
        dut.tg_port=dut.tgen.port_a.ifname
        
        if len(dut.ports) == 0:
            print("DUT " + str(dut1.name) + " has_no_MACsec-capable_ports_defined!")
            

    def Setup_Traffic_Generator(self):
        """ One_Time_setup_of_Traffic_Generator """
        self.tcp.create_tcp_stack(self.pytestConfigHelper.config.tgen_ports.netelem1.port_a, 
                                  self.pytestConfigHelper.config.traffic.tgen1.ip, 
                                  netmask=self.pytestConfigHelper.config.traffic.netmask, 
                                  mac_address=self.pytestConfigHelper.config.traffic.tgen1.mac)
        self.tcp.create_tcp_stack(self.pytestConfigHelper.config.tgen_ports.netelem2.port_a, 
                                  self.pytestConfigHelper.config.traffic.tgen2.ip, 
                                  netmask=self.pytestConfigHelper.config.traffic.netmask, 
                                  mac_address=self.pytestConfigHelper.config.traffic.tgen2.mac)

    def Setup_DUT(self, dut):
        """ Connect_to_DUT, create_VLANs, and_verify_links_to_traffic_generator and_to_peer_DUT_are_up """
        print(dut.name + ', IP ' + dut.ip + ' , MAC ' + dut.host_mac)
        
        # we already did this in the Base_Test_Suite_Setup call
        # Connect_to_Network_Element  ${dut.name}  ${dut.ip}
        # ...                         ${dut.username}  ${dut.password}
        # ...                         ${dut.connection_method}  ${dut.os}
        # ...                         max_wait=30
        
        print ('!!!!!!!!!!!!! MIKES: TODO: create_a_keyword_which_unconfigures_all_MACsec_on_a_DUT !!!!!!!!!!!!!')
        print (dut.ports)
        
        self.Disable_and_Verify_Macsec_on_Port(dut.name, dut.ca, dut.ports_all, ignore_error="Error", ignore_cli_feedback=True)
        self.macsec.macsec_delete_ca(dut.name, dut.ca.name, ignore_error="Error", ignore_cli_feedback=True)
        self.Remove_Port_from_Traffic_VLAN(dut.name, dut.port, ignore_error="Error", ignore_cli_feedback=True)
        self.Macsec_Verify_DUT_Capabilities(dut)
        
        #
        # # Disable_all_ports; Enable_1_MACsec_port_and_1_Traffic_Gen_port
        #for port in dut.tgen_ports:
        self.portApi.port_disable_state(dut.name, dut.tgen_ports, ignore_error="Error", ignore_cli_feedback=True)
        self.portApi.port_disable_state(dut.name, dut.isl_ports, ignore_error="Error", ignore_cli_feedback=True)
        self.portApi.port_disable_state(dut.name, dut.ports, ignore_error="Error", ignore_cli_feedback=True)
        self.portApi.port_enable_state(dut.name, dut.port)
        self.portApi.port_enable_state(dut.name, dut.tg_port)
        self.vlanUdks.Create_VLAN_and_Add_Ports_Untagged_then_Verify(dut.name, self.pytestConfigHelper.config.vlan_traffic, dut.tg_port)
        self.Disable_Noisy_Protocols(dut.name)
        
        
    def Disable_Noisy_Protocols(self, dut_name):
        """  Disable_CDP, EDP_and_LLDP_as_they_might_send_packets_which_would_skew_counter_tests """
        self.send_cli.send_cmd(dut_name, 'disable cdp ports all')
        self.send_cli.send_cmd(dut_name, 'disable edp ports all')
        self.send_cli.send_cmd(dut_name, 'disable lldp ports all')
        
    def Upgrade_Netelems(self):
        if self.pytestConfigHelper.dut1.upgrade_firmware == 'True':
            self.platformGenericSuiteUdks.Upgrade_Netelem_to_Latest_Firmware(self.pytestConfigHelper.dut1.name,  
                                                                             self.pytestConfigHelper.config.tftp_server.ip, 
                                                                             self.pytestConfigHelper.dut1.build_directory, 
                                                                             self.pytestConfigHelper.dut1.build, 
                                                                             self.pytestConfigHelper.dut1.mgmt_vlan, 
                                                                             self.pytestConfigHelper.dut1.ip)
        
        if self.pytestConfigHelper.dut2.upgrade_firmware == 'True':
            self.platformGenericSuiteUdks.Upgrade_Netelem_to_Latest_Firmware(self.pytestConfigHelper.dut2.name,  
                                                                             self.pytestConfigHelper.config.tftp_server.ip, 
                                                                             self.pytestConfigHelper.dut2.build_directory, 
                                                                             self.pytestConfigHelper.dut2.build, 
                                                                             self.pytestConfigHelper.dut2.mgmt_vlan, 
                                                                             self.pytestConfigHelper.dut2.ip)
    def Reboot_DUT(self, dut):
        """  Save_config_to_a_file, then_Reboot_using_the_saved_config. This_keyword_will_not_return_until_DUT_is_up_and_running. """
        config_file = "robot-macsec-temp"
        print("Rebooting " + str(dut.name))
        self.defaultLibrary.apiLowLevelApis.fileManagementUtils.save_current_config_to_file(dut.name, config_file, overwrite_answer="y")
        self.defaultLibrary.apiLowLevelApis.resetDeviceUtils.reboot_network_element_with_config(dut.name, config_file)
        self.defaultLibrary.deviceNetworkElement.pingKeywords.wait_until_ip_is_reachable(dut.ip, max_wait=300, wait_before=60, wait_after_success=5, interval=5, message="Ping_DUT")
        
    def Add_Port_to_Traffic_VLAN(self, dut_name, port):
        self.vlanUdks.Add_Ports_to_Untagged_Egress_for_VLAN_and_Verify_it_is_Added(dut_name, self.pytestConfigHelper.config.vlan_traffic, port)
        self.vlanApi.vlan_set_pvid(dut_name, port, self.pytestConfigHelper.config.vlan_traffic, 'modify-egress')
        
    def Remove_Port_from_Traffic_VLAN(self, dut_name, port, **kwags):
        self.vlanUdks.Remove_Ports_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed(dut_name,  self.pytestConfigHelper.config.vlan_traffic , port, **kwags)
        
    def Add_Port_to_Traffic_VLAN_Tagged(self, dut_name, port):
        self.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(dut_name, self.pytestConfigHelper.config.vlan_traffic, port)
        self.vlanApi.vlan_set_pvid(dut_name, port, self.pytestConfigHelper.config.vlan_traffic,  'modify-egress')
        
    def Remove_Port_from_Traffic_VLAN_Tagged(self, dut_name, port):
        self.vlanUdks.Remove_Ports_from_Tagged_Egress_for_VLAN_and_Verify_it_is_Removed(dut_name, self.pytestConfigHelper.config.vlan_traffic, port)
        
    def Macsec_Verify_DUT_Capabilities(self, dut):
        """ Verify_ports_to_be_used_from_MACsec_testing_actually_support_MACsec.
            dut.port_is_mandatory. It_represents_a_port_that_supports_MACsec.
            dut.port128_is_optional. It_represents_a_port_that_only_supports_gcm-aes-128.
            dut.port256_is_optional. It_represents_a_port_that_supports_gcm-aes-128_and_gcm-aes-256 """
        self.Macsec_Verify_Port_Capable_128(dut.name, dut.port)
        if len(dut.ports_128) != 0:
            self.Macsec_Verify_Port_Capable_128(dut.name, dut.port)
        if len(dut.ports_256) != 0:
            self.Macsec_Verify_Port_Capable_256(dut.name, dut.port256)
        
    def Macsec_Verify_Port_Capable_128(self, dut_name, port):
        """  Verify_port_supports_cipher_suite_gcm-aes-128_by_attempting_to
                  configure_it_as_such. """
        self.macsec.macsec_set_cipher_suite_128(dut_name, port)
        self.macsec.macsec_verify_port_cipher_suite(dut_name, port, '128')
        
    def Macsec_Verify_Port_Capable_256(self, dut_name, port):
        """  Verify_port_supports_cipher_suite_gcm-aes-256_by_attempting_to
             configure_it_as_such.  Restore_cipher_suite_to_default_value
             (gcm-aes-128) at_the_end_of_the_test. """
        self.macsec.macsec_set_cipher_suite_256(dut_name, port)
        self.macsec.macsec_verify_port_cipher_suite(dut_name, port, '256')
        self.macsec.macsec_set_cipher_suite_128(dut_name, port)
        
    def Cleanup_DUT(self, dut):
        print(dut.name + " " + dut.ip + " " + dut.host_mac)
        # run_keyword_and_ignore_error_Disable_Macsec_on_DUT  ${dut}
        # run_keyword_and_ignore_error_Macsec_Delete_CA  ${dut.name}  ${dut.ca}
        self.Disable_and_Verify_Macsec_on_Port(dut.name, dut.ca, dut.port, ignore_error="Error", ignore_cli_feedback=True) # Added to cleanup
        self.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(dut.name, self.pytestConfigHelper.config.vlan_traffic)
        self.portApi.port_disable_state(dut.name, dut.tgen_ports, ignore_error="Error", ignore_cli_feedback=True)
        self.portApi.port_disable_state(dut.name, dut.ports, ignore_error="Error", ignore_cli_feedback=True)
        
    def Ping_Test(self, count=3, **kwargs):
        # log_to_console   !!!!! Skip_ping_test_until_Broadcast/ICMP_traffic_is_supported_by_5420 !!!!!
        self.traffic_port.ping(self.pytestConfigHelper.config.tgen_ports.netelem1.port_a, 
                               self.pytestConfigHelper.config.traffic.tgen1.ip,
                               self.pytestConfigHelper.config.traffic.tgen2.ip,  
                               timeout_secs=5,
                               ping_count=count,
                               **kwargs)
        self.traffic_port.ping(self.pytestConfigHelper.config.tgen_ports.netelem2.port_a,
                               self.pytestConfigHelper.config.traffic.tgen2.ip,
                               self.pytestConfigHelper.config.traffic.tgen1.ip,  
                               timeout_secs=5,
                               ping_count=count,
                               **kwargs)
        
        
        
    def Verify_Connectivity(self):
        self.Transmit_Test()
        
    def Verify_No_Connectivity(self):
        self.Ping_Test(expect_error=True)
        
    def Create_and_Verify_Connectivity_Association(self, dut_name, ca):
        self.macsec.macsec_create_ca(dut_name, ca.name, ca.psk.ckn, ca.psk.cak)
        self.macsec.macsec_verify_ca_exists(dut_name, ca.name)
        
    def Delete_and_Verify_Connectivity_Association(self, dut_name, ca, **kwargs):
        self.macsec.macsec_delete_ca(dut_name, ca.name, **kwargs)
        self.macsec.macsec_verify_ca_does_not_exist(dut_name, ca.name, **kwargs)
        
    # #
    # # Use_the_following_Transmit_Test_keyword_if_your_test_needs_to_vary_packet_length.
    # #
    def Transmit_Test(self, tx_count=2000, tx_count_b=-1, tx_rate=500, prime_packet_pump=True, packet_len=64, ignore_error=False):
        """  Send ${tx_count} packets_from_DUT1's_Traffic_Generator_to_DUT2's_Traffic
        ...              Generator, and ${tx_count_b} packets_in_the_reverse_direction.
        ...              If ${tx_count} is_not_specified_then_value_will_default_to_2000_packets.
        ...              If ${tx_count_b} is_not_specified_then_value_will_default_to ${tx_count}. """
        
        if tx_count_b < 0:
            tx_count_b = tx_count
        print(":" + str(tx_count) + " tx_count_b:" + str(tx_count_b) + " len: " + str(packet_len))
        self.tgenUdks.Create_Ethernet2_Packet(self.pytestConfigHelper.config.packetA.name, 
                                              self.pytestConfigHelper.config.packetA.dst_mac, 
                                              self.pytestConfigHelper.config.packetA.src_mac, 
                                              packet_len=packet_len)
        self.tgenUdks.Create_Ethernet2_Packet(self.pytestConfigHelper.config.packetB.name, 
                                              self.pytestConfigHelper.config.packetB.dst_mac, 
                                              self.pytestConfigHelper.config.packetB.src_mac, 
                                              packet_len=packet_len)
        
        print("Setup_Packet_Streams_DUT1=" + str(self.pytestConfigHelper.config.tgen_ports.netelem1.port_a) + 
              " DUT2=" + str(self.pytestConfigHelper.config.tgen_ports.netelem2.port_a) + 
              " count= " + str(tx_count) + "/" + str(tx_count_b) + 
              " rate=" + str(tx_rate))
        
        
        self.localTrafficSuiteUdks.Setup_Packet_Streams(self.pytestConfigHelper.config.tgen_ports.netelem1.port_a,
                                            self.pytestConfigHelper.config.tgen_ports.netelem2.port_a,
                                            self.pytestConfigHelper.config.packetA.name,
                                            self.pytestConfigHelper.config.packetB.name, 
                                            tx_count=tx_count,
                                            tx_count_b=tx_count_b,
                                            tx_rate=tx_rate)
                                                   
        self.localTrafficSuiteUdks.Send_Packets_Verify_Received(self.pytestConfigHelper.config.tgen_ports.netelem1.port_a,
                                                        self.pytestConfigHelper.config.tgen_ports.netelem2.port_a,
                                                        self.pytestConfigHelper.config.packetA.name,
                                                        self.pytestConfigHelper.config.packetB.name,
                                                        self.pytestConfigHelper.config.packetB.name,
                                                        self.pytestConfigHelper.config.packetA.name,
                                                        self.pytestConfigHelper.config.packetA.src_mac,
                                                        self.pytestConfigHelper.config.packetB.src_mac,
                                                        tx_count=tx_count,
                                                        tx_count_b=tx_count_b,
                                                        tx_rate=tx_rate,
                                                        prime_packet_pump=prime_packet_pump,
                                                        ignore_error = ignore_error)
        
        
    # #
    # # Use_the_following_Transmit_Test_keyword_if_your_test_needs_to_vary_QoS_priority.
    # #
    # # Note: I_tried_to_add_priority_to_existing "Transmit_Test" keyword, but_doing_so
    # #       broke_the "packet_len" parameter.  Seems_like_when_a_VLAN_tag (with_or
    # #       without_priority_bit) is_added_to_JETS_traffic, each_packet_is_64-bytes
    # #       regardless_of "packet_len" parameter_passed_to "Create_Ethernet2_Packet".
    # #
    def Transmit_Test_with_Priority(self, tx_count=2000, tx_count_b=-1, tx_rate=500, prime_packet_pump=True, exp_priority=None):
        """  Send ${tx_count} packets_from_DUT1's_Traffic_Generator_to_DUT2's_Traffic
             Generator, and ${tx_count_b} packets_in_the_reverse_direction.
             If ${tx_count} is_not_specified_then_value_will_default_to_2000_packets.
             If ${tx_count_b} is_not_specified_then_value_will_default_to ${tx_count}. """ 
        if  tx_count_b < 0:
            tx_count_b = tx_count
        else:
            tx_count_b = tx_count_b
        print("tx_count: " + str(tx_count) + " tx_count_b: " + str(tx_count_b) + " prio: " + str(exp_priority))
        self.tgenUdks.Create_Ethernet2_Packet(self.pytestConfigHelper.config.packetA.name, 
                                              self.pytestConfigHelper.config.packetA.dst_mac, 
                                              self.pytestConfigHelper.config.packetA.src_mac, 
                                              vlan_id=self.pytestConfigHelper.config.vlan_traffic, 
                                              vlan_prio=exp_priority)
        self.tgenUdks.Create_Ethernet2_Packet(self.pytestConfigHelper.config.packetB.name, 
                                              self.pytestConfigHelper.config.packetB.dst_mac, 
                                              self.pytestConfigHelper.config.packetB.src_mac, 
                                              vlan_id=self.pytestConfigHelper.config.vlan_traffic, 
                                              vlan_prio=exp_priority)
        
        print("Setup_Packet_Streams_DUT1=" + str(self.pytestConfigHelper.config.tgen_ports.netelem1.port_a) +
              " DUT2=" + str(self.pytestConfigHelper.config.tgen_ports.netelem2.port_a) + 
              " count=" + str(tx_count/tx_count_b) + " rate=" +  str(tx_rate))
        # trafficSuiteUdks
        self.localTrafficSuiteUdks.Setup_Packet_Streams(self.pytestConfigHelper.config.tgen_ports.netelem1.port_a, 
                                                   self.pytestConfigHelper.config.tgen_ports.netelem2.port_a,
                                                   self.pytestConfigHelper.config.packetA.name,
                                                   self.pytestConfigHelper.config.packetB.name,
                                                   tx_count=tx_count,
                                                   tx_count_b=tx_count_b,
                                                   tx_rate=tx_rate)
        self.localTrafficSuiteUdks.Send_Packets_Verify_Received(self.pytestConfigHelper.config.tgen_ports.netelem1.port_a,
                                                                self.pytestConfigHelper.config.tgen_ports.netelem2.port_a,
                                                                self.pytestConfigHelper.config.packetA.name,
                                                                self.pytestConfigHelper.config.packetB.name,
                                                                self.pytestConfigHelper.config.packetB.name,
                                                                self.pytestConfigHelper.config.packetA.name,
                                                                self.pytestConfigHelper.config.packetA.src_mac,
                                                                self.pytestConfigHelper.config.packetB.src_mac,
                                                                tx_count=tx_count,
                                                                tx_count_b=tx_count_b,
                                                                tx_rate=tx_rate,
                                                                prime_packet_pump=prime_packet_pump)
        
        
    def Macsec_Set_Confidentiality_Offset(self, dut_name, offset, port):
        """  Keyword_wrapper_that_allows_caller_to_pass_Confidentiality_Offset
             as_an_argument_rather_than_embedding_into_keyword """
        print("offset:" + str(offset))
        if str(offset) == '0':
            self.macsec.macsec_set_confidentiality_offset_0(dut_name, port)
        elif str(offset) == '30':
            self.macsec.macsec_set_confidentiality_offset_30(dut_name, port)
        elif str(offset) == '50':
            self.macsec.macsec_set_confidentiality_offset_50(dut_name, port)
        else: 
            pytest.fail(msg="Fail_Unsupported_Confidentiality_Offset" + offset)
        
    def Skip_Test_if_gcm_aes_256_Not_Supported(self):
        if (self.pytestConfigHelper.dut1.port256 == None):
            pytest.skip(msg="Skip test because_DUT " + self.tb.dut1.name + " does not have a MACsec gcm-aes-256 port")
        if (self.pytestConfigHelper.dut2.port256 == None):
            pytest.skip(msg="Skip test because_DUT " + self.tb.dut2.name + " does not have a MACsec gcm-aes-256 port")
        
    def Skip_Test_if_Not_Stacked_System(self, dut):
        """  Test_cases_should_call_this_the_tests_are_only_applicable_to_stacked_systems.
             Determine_if_a_system_is_stacked_by_looking_for_a_colon (:) in_the_DUT's_port_name.
             TODO: come_up_with_a_better_way_to_determine_if_DUT_is_stacked. """
             
        if not ":" in self.tb.dut.port:
            pytest.skip(reason="Skip_test_because_DUT " + dut1.name + " is_not_a_stacked_system")
        
    def Skip_Test_if_DUT_Has_No_HW_Limits(self, dut, limit_type):
        if limit_type in dut.macsec:
            pytest.skip(msg=dut.name + " does_not_have " + limit_type)
        if "limit_type" not in dut.macsec:
            pytest.skip(msg=dut.name + " does_not_have " + limit_type)
        
    # ### Keywords_to_Create_Macsec_Connections ###
    def Create_and_Verify_Macsec_Connection_DUT1_Key_Server(self, dut1_name, dut1_port, dut2_name, dut2_port, ca):
        self.macsec.macsec_set_mka_actor_priority(dut1_name,  '1', dut1_port)
        self.macsec.macsec_set_mka_actor_priority(dut2_name, '3', dut2_port)
        self.Create_and_Verify_Macsec_Connection(dut1_name, dut1_port, dut2_name, dut2_port, ca)
        
    def Create_and_Verify_Macsec_Connection(self, dut1_name, dut1_port, dut2_name, dut2_port, ca):
        self.Enable_and_Verify_Macsec_on_Port(dut1_name, ca, dut1_port)
        self.Enable_and_Verify_Macsec_on_Port(dut2_name, ca, dut2_port)
        self.Macsec_Verify_Port_Connect_Secure(dut1_name, dut1_port)
        self.Macsec_Verify_Port_Connect_Secure(dut2_name, dut2_port)
        
    def Disable_and_Verify_Macsec_Connection(self, dut1_name, dut1_port, dut2_name, dut2_port, ca):
        self.Disable_and_Verify_Macsec_on_Port(dut1_name, ca, dut1_port)
        self.Disable_and_Verify_Macsec_on_Port(dut2_name, ca, dut2_port)
        
    def Enable_and_Verify_Macsec_on_Port(self, dut_name, ca, port):
        self.Create_and_Verify_Connectivity_Association(dut_name, ca)
        self.macsec.macsec_enable_ca_port(dut_name, ca.name, port)
        self.macsec.macsec_verify_ca_port(dut_name, ca.name, port)
        self.macsec.macsec_verify_enabled_on_port(dut_name, port)
        
    def Disable_and_Verify_Macsec_on_Port(self, dut_name, ca, port, **kwargs):
        self.macsec.macsec_disable_ca_port(dut_name, ca.name, port, **kwargs)
        self.macsec.macsec_verify_disabled_on_port(dut_name, port, **kwargs)
        self.Delete_and_Verify_Connectivity_Association(dut_name, ca, **kwargs)
        self.Unconfigure_Macsec_Port_Options(dut_name, port, **kwargs)
        
    def Unconfigure_Macsec_Port_Options(self, dut_name, port, **kwargs):
        self.macsec.macsec_set_mka_actor_priority(dut_name, '0x10' ,port, **kwargs)
        self.macsec.macsec_set_confidentiality_offset_0(dut_name, port, **kwargs)
        self.macsec.macsec_set_cipher_suite_128(dut_name, port, **kwargs)
        self.macsec.macsec_set_include_sci_disable(dut_name, port, **kwargs)
        
    def Verify_No_Macsec_Errors_on_Port(self,dut_name,port):
         self.macsec.macsec_verify_tx_port_no_errors(dut_name, port)
         self.macsec.macsec_verify_rx_port_no_errors(dut_name, port)
        
    def Macsec_Set_Pending_PN_Exhaustion_to_Default(self, dut_name):
        default = int(0xC0000000)
        self.Macsec_Set_Pending_PN_Exhaustion(dut_name, default)
        
        
    # #
    # # Use_the_following_pair_of_Transmit_Test_keywords_if_your
    # # test_needs_to_do_something_while_packets_are_in_flight.
    # #
    # def Transmit_Test_Part_1_of_2(self, tx_count=2000, tx_count_b=-1, tx_rate=500, prime_packet_pump=True, packet_len=64):
        # """  Send ${tx_count} packets_from_DUT1's_Traffic_Generator_to_DUT2's_Traffic
        # ...              Generator, and ${tx_count_b} packets_in_the_reverse_direction.
        # ...              Packet_verification_is_done_by 'Transmit_Test_Part_2_of_2'.
        # ...              If ${tx_count} is_not_specified_then_value_will_default_to_2000_packets.
        # ...              If ${tx_count_b} is_not_specified_then_value_will_default_to ${tx_count}. """
        # ${tx_count_b}=  Set_Variable_If  ${tx_count_b}<0  ${tx_count}  ${tx_count_b}
        # log_tx_count:${tx_count} tx_count_b:${tx_count_b} len:${packet_len}
        # self.tgenUdks.Create_Ethernet2_Packet  ${packetA.name}  ${packetA.dst_mac}  ${packetA.src_mac}  packet_len=${packet_len}
        # self.tgenUdks.Create_Ethernet2_Packet  ${packetB.name}  ${packetB.dst_mac}  ${packetB.src_mac}  packet_len=${packet_len}
        #
        # log_Setup_Packet_Streams_DUT1=${tgen_ports.netelem1.port_a} DUT2=${tgen_ports.netelem2.port_a} count=${tx_count}/${tx_count_b} rate=${tx_rate}
        # self.localTrafficSuiteUdks.Setup_Packet_Streams
        # ...       ${tgen_ports.netelem1.port_a}  ${tgen_ports.netelem2.port_a}
        # ...       ${packetA.name}  ${packetB.name}  tx_count=${tx_count}  tx_count_b=${tx_count_b}  tx_rate=${tx_rate}
        #
        # Just_Send_Packets
        # ...       ${tgen_ports.netelem1.port_a}  ${tgen_ports.netelem2.port_a}
        # ...       ${packetA.src_mac}  ${packetB.src_mac}
        # ...       prime_packet_pump=${prime_packet_pump}
        
        
    # def Transmit_Test_Part_2_of_2(self, tx_count=2000, tx_count_b=-1, tx_rate=500):
        # """  Verify_the_packets_sent_by 'Transmit_Test_Part_1_of_2' """
        # Just_Verify_Received
        # ...       ${tgen_ports.netelem1.port_a}  ${tgen_ports.netelem2.port_a}
        # ...       rx_packet_a=${packetB.name}  rx_packet_b=${packetA.name}
        # ...       tx_count=${tx_count}  tx_count_b=${tx_count_b}  tx_rate=${tx_rate}
