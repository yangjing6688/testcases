from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from pytest import mark
from time import sleep
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper


class citQadTests:
    # Test Case Setup
    def setup_class(self):
        try:
            # Create the pytest execution helper
            self.executionHelper = PytestExecutionHelper()

            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            self.tb = PytestConfigHelper(config)
            # TB / Suite Variables.
            self.dut1TgenPorts = [self.tb.dut1_tgen_port_a.ifname]
            self.dut1TgenPorts.append(self.tb.dut1_tgen_port_b.ifname)
            self.dut1TgenPorts.append(self.tb.dut1_tgen_port_c.ifname)
            self.dut1TgenPorts.append(self.tb.dut1_tgen_port_d.ifname)
            self.tgenDictA = self.tb.createTgenPort(self.tb.tgen1_name, self.tb.tgen_dut1_port_a.ifname)
            self.tgenDictB = self.tb.createTgenPort(self.tb.tgen1_name, self.tb.tgen_dut1_port_b.ifname)
            self.tgenDictC = self.tb.createTgenPort(self.tb.tgen1_name, self.tb.tgen_dut1_port_c.ifname)
            self.tgenDictD = self.tb.createTgenPort(self.tb.tgen1_name, self.tb.tgen_dut1_port_d.ifname)
            self.tgenall_Dict = []
            self.tgenall_Dict.append(self.tgenDictA)
            self.tgenall_Dict.append(self.tgenDictB)
            self.tgenall_Dict.append(self.tgenDictC)
            self.tgenall_Dict.append(self.tgenDictD)
            self.tgenBCD_Dict = []
            self.tgenBCD_Dict.append(self.tgenDictB)
            self.tgenBCD_Dict.append(self.tgenDictC)
            self.tgenBCD_Dict.append(self.tgenDictD)
            self.tgenBC_Dict = []
            self.tgenBC_Dict.append(self.tgenDictB)
            self.tgenBC_Dict.append(self.tgenDictC)
            self.tgenCD_Dict = []
            self.tgenCD_Dict.append(self.tgenDictC)
            self.tgenCD_Dict.append(self.tgenDictD)

            self.vl_layer2     = '5'
            self.vl_layer2tag  = '100'
            self.vl_layer2line = '1000'
            self.vl_layer2stp  = '500'
            self.vl_layer3     = '11'
            self.vl_10         = '10'
            self.vl_layer2_name = 'VLAN_0005'
            self.vl_layer2tag_name = 'VLAN_0100'
            self.vl_layer2line_name = 'VLAN_1000'
            self.vl_layer2stp_name = 'VLAN_0500'
            self.vl_layer3_name= 'VLAN_0011'
            self.vl_10_name = 'VLAN_0010'
            self.vl_layer2_ports = self.dut1TgenPorts
            self.vl_layer2tag_ports = self.dut1TgenPorts
            self.vl_layer2line_ports = [self.tb.dut1_tgen_port_c.ifname, self.tb.dut1_tgen_port_d.ifname]
            self.vl_layer2stp_ports = [self.tb.dut1_tgen_port_a.ifname, self.tb.dut1_tgen_port_d.ifname]
            self.vl_layer3_ports = []
            self.vl_10_ports = [self.tb.dut1_tgen_port_a.ifname, self.tb.dut1_tgen_port_b.ifname]
            # VLANS
            self.vlan_a = '11'
            self.vlan_a_name = 'vlan_0011'
            self.vlan_a_ip = '11.11.11.1'
            self.vlan_a_ip_mask = '24'
            self.vlan_b = '22'
            self.vlan_b_name = 'vlan_0022'
            self.vlan_b_ip = '22.22.22.1'
            self.vlan_b_ip_mask = '24'

            self.allvlans = [self.vl_layer2, self.vl_layer2tag, self.vl_layer2line, self.vl_layer2stp]
            self.allvlannames = [self.vl_layer2_name, self.vl_layer2tag_name, self.vl_layer2line_name, self.vl_layer2stp_name]
            sep = ','
            self.stpPortStr1 = sep.join(self.vl_layer2stp_ports)
            self.alldut1portstr = sep.join(self.dut1TgenPorts)

            # Create new objects to use in test. Here we will import everything from the default library
            self.defaultLibrary = DefaultLibrary()
            # Create a shorter version for the UDKs
            self.udks = self.defaultLibrary.apiUdks
            self.netElem = self.defaultLibrary.deviceNetworkElement

            ''' Log  (Setup) Create qad vlans. '''
            self.udks.setupTeardownUdks.Base_Test_Suite_Setup()
            self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name, 'configure default delete port all')
            self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name, 'clear log stat')
            self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name, 'disable edp port all')
            self.udks.lldpUdks.Disable_LLDP_Tx_Rx_and_Verify_it_is_Disabled(self.tb.dut1_name, self.dut1TgenPorts)
            self.defaultLibrary.apiLowLevelApis.spanningtree.spanningtree_disable_global(self.tb.dut1_name)
            self.defaultLibrary.apiLowLevelApis.spanningtree.spanningtree_set_stp_mode(self.tb.dut1_name,
                                                                                       mode='dot1d', sid='0')
            self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut1_name,
                                                                        self.tb.dut1_tgen_port_a.ifname)
            self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut1_name,
                                                                        self.tb.dut1_tgen_port_b.ifname)
            self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut1_name,
                                                                        self.tb.dut1_tgen_port_c.ifname)
            self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut1_name,
                                                                        self.tb.dut1_tgen_port_d.ifname)

            #self.udks.portUdks.Enable_Jumbo_Frames_and_Verify_it_is_Enabled(self.tb.dut1_name,self.dut1TgenPorts)
            self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name, 'enable jumbo port all')
            # create the vlans
            self.udks.vlanUdks.Create_VLAN_and_Add_Ports_Untagged_then_Verify(self.tb.dut1_name,self.vl_layer2,
                                                                            self.vl_layer2_ports)
            self.udks.vlanUdks.Create_VLAN_and_Add_Ports_Tagged_then_Verify(self.tb.dut1_name,self.vl_layer2tag,
                                                                            self.vl_layer2tag_ports)
            self.udks.vlanUdks.Create_VLAN_and_Add_Ports_Tagged_then_Verify(self.tb.dut1_name,self.vl_layer2line,
                                                                            self.vl_layer2line_ports)
            self.udks.vlanUdks.Create_VLAN_and_Add_Ports_Tagged_then_Verify(self.tb.dut1_name, self.vl_layer2stp,
                                                                            self.vl_layer2stp_ports)
            self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name, 'show vlan')
            self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name, 'clear counter')
        except Exception:
            # Setup has failed, so set the flag
            self.executionHelper.setSetupFailure(True)

    # [Teardown]  Test Case Cleanup
    def teardown_class(self):

        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name, 'show vlan')
        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name, 'show port {} stat no'.format(self.alldut1portstr))
        sleep(5)
        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name, 'show port {} stat no'.format(self.alldut1portstr))

        self.udks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.dut1_name,
                                                                      self.tb.dut1_tgen_port_a.ifname)
        self.udks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.dut1_name,
                                                                      self.tb.dut1_tgen_port_b.ifname)
        self.udks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.dut1_name,
                                                                      self.tb.dut1_tgen_port_c.ifname)
        self.udks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.dut1_name,
                                                                      self.tb.dut1_tgen_port_d.ifname)

        self.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.dut1_name,self.vl_layer2_name)
        self.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.dut1_name,self.vl_layer2tag_name)
        self.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.dut1_name,self.vl_layer2line_name)
        self.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.dut1_name, self.vl_layer2stp_name)
        #self.udks.portUdks.Disable_Jumbo_Frames_and_Verify_it_is_Disabled(self.tb.dut1_name, self.dut1TgenPorts)
        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name, 'disable jumbo port all')
        self.udks.setupTeardownUdks.Base_Test_Suite_Cleanup()

    # Test Cases
    @mark.p1
    @mark.testbed_1_node
    def test_1_1(self):
        # Helper to see if the setup failed and skip the test
        self.executionHelper.testSkipCheck()
        ''' L2 broadcast flood to all ports (untagged) '''

        self.udks.trafficGenerationUdks.Start_Capture_with_DMAC_and_SMAC_Filter(self.tgenDictA,
                                                                                'FF:FF:FF:FF:FF:FF', '00:00:00:00:00:01')
        self.udks.trafficGenerationUdks.Start_Capture_with_DMAC_and_SMAC_Filter(self.tgenBCD_Dict, 'FF:FF:FF:FF:FF:FF',
                                                                                '00:00:00:00:00:01')
        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet('stream_1', 'FF:FF:FF:FF:FF:FF', '00:00:00:00:00:01')
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(self.tgenDictA,'stream_1',1,50,100)
        print("Sleeping for 3 seconds")
        sleep(3)
        self.udks.trafficGenerationUdks.Stop_Transmit_and_Clear_all_Streams_on_Port(self.tgenDictA)

        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.get_captured_count(self.tgenall_Dict)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_equal(self.tgenDictA, 0)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_plus_or_minus_percent(
            self.tgenBCD_Dict, 50, 4)

    @mark.p1
    @mark.testbed_1_node
    def test_1_2(self):
        # Helper to see if the setup failed and skip the test
        self.executionHelper.testSkipCheck()
        ''' L2 broadcast Flood to all ports (tagged) '''
        self.udks.trafficGenerationUdks.Start_Capture_with_DMAC_and_SMAC_Filter(self.tgenall_Dict,
                                                                           'FF:FF:FF:FF:FF:FF', '00:00:00:00:00:11')

        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet('stream_1', 'FF:FF:FF:FF:FF:FF',
                                                                                        '00:00:00:00:00:11', 100)
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(self.tgenDictA,'stream_1',1,500,500)
        print("Sleeping for 3 seconds")
        sleep(3)
        self.udks.trafficGenerationUdks.Stop_Transmit_and_Clear_all_Streams_on_Port(self.tgenDictA)

        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.get_captured_count(self.tgenall_Dict)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_equal(self.tgenDictA, 0)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_plus_or_minus_percent(
            self.tgenBCD_Dict, 500, 1)

    @mark.p1
    @mark.testbed_1_node
    def test_1_3(self):
        # Helper to see if the setup failed and skip the test
        self.executionHelper.testSkipCheck()
        '''Port gets traffic only when member of vlan (removal/reinsert port)'''

        self.udks.vlanUdks.Remove_Ports_from_Tagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.tb.dut1_name,
                                                self.vl_layer2,self.tb.dut1_tgen_port_d.ifname)
        self.udks.trafficGenerationUdks.Start_Capture_with_DMAC_and_SMAC_Filter(self.tgenall_Dict,
                                                                           'FF:FF:FF:FF:FF:FF', '00:00:00:00:01:11')

        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet('stream_1', 'FF:FF:FF:FF:FF:FF',
                                                                                        '00:00:00:00:01:11')
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(self.tgenDictA,'stream_1',1,500,500)
        print("Sleeping for 3 seconds")
        sleep(3)
        self.udks.trafficGenerationUdks.Stop_Transmit_and_Clear_all_Streams_on_Port(self.tgenDictA)

        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.get_captured_count(self.tgenall_Dict)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_equal(self.tgenDictA, 0)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_plus_or_minus_percent(
            self.tgenBC_Dict, 500, 1)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_equal(self.tgenDictD, 0)
        self.udks.vlanUdks.Add_Ports_to_Tagged_Egress_for_VLAN_and_Verify_it_is_Added(self.tb.dut1_name,
                                                                                             self.vl_layer2,
                                                                                             self.tb.dut1_tgen_port_d.ifname)

    @mark.p1
    @mark.testbed_1_node
    def test_1_4(self):

        # Helper to see if the setup failed and skip the test
        self.executionHelper.testSkipCheck()
        '''Vlan with tag x doesn't recieve traffic with tag y'''
        self.udks.trafficGenerationUdks.Start_Capture_with_DMAC_and_SMAC_Filter(self.tgenall_Dict,
                                                                           'FF:FF:FF:FF:FF:FF', '00:00:00:00:11:11')

        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet('stream_1', 'FF:FF:FF:FF:FF:FF',
                                                                                        '00:00:00:00:11:11', 111)
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(self.tgenDictA,'stream_1',1,900,500)
        print("Sleeping for 3 seconds")
        sleep(3)
        self.udks.trafficGenerationUdks.Stop_Transmit_and_Clear_all_Streams_on_Port(self.tgenDictA)

        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.get_captured_count(self.tgenall_Dict)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_equal(self.tgenall_Dict, 0)

    @mark.p1
    @mark.testbed_1_node
    def test_1_5(self):
        # Helper to see if the setup failed and skip the test
        self.executionHelper.testSkipCheck()
        ''' Changing vlan tag from x to y back to x '''
        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name,
                                'clear counter')
        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name,
                                'configure vlan {} tag 111'.format(self.vl_layer2tag_name))

        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name,
                                        'show port {} statistics no-refresh'.format(self.alldut1portstr))
        sleep(1)
        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name,
                                        'show port {} statistics no-refresh'.format(self.alldut1portstr))

        self.udks.trafficGenerationUdks.Start_Capture_with_DMAC_and_SMAC_Filter(self.tgenall_Dict,
                                                                'FF:FF:FF:FF:FF:FF', '00:00:00:01:11:11')
        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet('stream_1',
                                                                'FF:FF:FF:FF:FF:FF','00:00:00:01:11:11', 111)
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(self.tgenDictA,'stream_1',1,500,500)
        print("Sleeping for 3 seconds")
        sleep(3)
        self.udks.trafficGenerationUdks.Stop_Transmit_and_Clear_all_Streams_on_Port(self.tgenDictA)

        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name,
                                        'show port {} statistics no-refresh'.format(self.alldut1portstr))

        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.get_captured_count(self.tgenall_Dict)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_equal(self.tgenDictA, 0)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_plus_or_minus_percent(
            self.tgenBCD_Dict, 500, 1)

        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name,
                                        'configure vlan {} tag {}'.format(self.vl_layer2tag_name,self.vl_layer2tag))

    @mark.p1
    @mark.testbed_1_node
    def test_1_6(self):
        # Helper to see if the setup failed and skip the test
        self.executionHelper.testSkipCheck()
        '''Flood unknown unicast traffic'''
        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name,
                                'clear counter')

        self.udks.trafficGenerationUdks.Start_Capture_with_DMAC_and_SMAC_Filter(self.tgenall_Dict,
                                                                '00:BB:BB:BB:BB:BB', '00:AA:AA:AA:AA:AA')

        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet('stream_1',
                                                                '00:BB:BB:BB:BB:BB', '00:AA:AA:AA:AA:AA')
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(self.tgenDictA,'stream_1',1,500,500)
        print("Sleeping for 3 seconds")
        sleep(3)
        self.udks.trafficGenerationUdks.Stop_Transmit_and_Clear_all_Streams_on_Port(self.tgenDictA)

        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.get_captured_count(self.tgenall_Dict)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_equal(self.tgenDictA, 0)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_plus_or_minus_percent(
            self.tgenBCD_Dict, 500, 1)

    @mark.p1
    @mark.testbed_1_node
    def test_1_7(self):
        # Helper to see if the setup failed and skip the test
        self.executionHelper.testSkipCheck()

        '''Verify fdb learning, no flooding '''
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.traffic_gen = {}

        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name,
                                'clear fdb')
        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name,
                                'clear counter')

        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet('stream_1',
                                                        '00:BB:BB:BB:BB:BB', '00:AA:AA:AA:AA:AA', ether_type=0x0800)
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(self.tgenDictA,'stream_1',1,50,50)

        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet('stream_2',
                                                        '00:AA:AA:AA:AA:AA', '00:BB:BB:BB:BB:BB', ether_type=0x0800)
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(self.tgenDictB,'stream_2',1,50,50)
        print("Sleeping for 1 seconds")
        sleep(1)
        self.udks.trafficGenerationUdks.Stop_Transmit_and_Clear_all_Streams_on_Port(self.tgenall_Dict)

        self.udks.trafficGenerationUdks.Start_Capture_with_DMAC_and_SMAC_Filter(self.tgenall_Dict,
                                                        '00:BB:BB:BB:BB:BB', '00:AA:AA:AA:AA:AA', ether_type=0x0800)

        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet('stream_1',
                                                        '00:BB:BB:BB:BB:BB', '00:AA:AA:AA:AA:AA', ether_type=0x0800)
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(self.tgenDictA,'stream_1',1,900,500)
        print("Sleeping for 1 seconds")
        sleep(2)
        self.udks.trafficGenerationUdks.Stop_Transmit_and_Clear_all_Streams_on_Port(self.tgenDictA)

        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.get_captured_count(self.tgenall_Dict)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_equal(self.tgenDictA, 0)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_equal(self.tgenCD_Dict, 0)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_plus_or_minus_percent(
            self.tgenDictB, 900, 1)

    @mark.p1
    @mark.testbed_1_node
    def test_1_8(self):
        # Helper to see if the setup failed and skip the test
        self.executionHelper.testSkipCheck()
        '''FDB Learning II,send 10k incremental srcMac'''
        self.udks.trafficGenerationUdks.Start_Capture_with_DMAC_and_SMAC_Filter(self.tgenall_Dict,
                                '00:DD:DD:DD:DD:DD', '00:CC:CC:CC:CC:CC', None, '00:00:00:FF:FF:FF')

        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet('stream_1', '00:DD:DD:DD:DD:DD',
                                                                        '00:CC:CC:CC:CC:CC', 1000)
        self.udks.trafficGenerationUdks.send_stream_with_incrementing_smac(self.tgenDictC,'stream_1',1,10000,
                                                                           500,'pps',10000,120)
        print("Sleep 15 seconds")
        sleep(15)
        self.udks.trafficGenerationUdks.Stop_Transmit_and_Clear_all_Streams_on_Port(self.tgenall_Dict)

        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.get_captured_count(self.tgenDictD)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_plus_or_minus_percent(
            self.tgenDictD,10000,1)

    @mark.p1
    @mark.testbed_1_node
    @mark.dev
    def test_1_9(self):
        # Helper to see if the setup failed and skip the test
        self.executionHelper.testSkipCheck()
        '''Oversize packet forwarding'''
        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name,
                                'clear counter')
        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name,
                                        'show port {} statistics no-refresh'.format(self.alldut1portstr))

        self.udks.trafficGenerationUdks.Start_Capture_with_DMAC_and_SMAC_Filter(self.tgenall_Dict,
                                                                'FF:FF:FF:FF:FF:FF', '00:00:00:00:00:03')

        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet('stream_1','FF:FF:FF:FF:FF:FF', '00:00:00:00:00:03',1000,None,None,None,4000)
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(self.tgenDictC,'stream_1',1,500,500)
        self.udks.trafficGenerationUdks.Stop_Transmit_and_Clear_all_Streams_on_Port(self.tgenDictC)
        self.netElem.networkElementCliSend.send_cmd(self.tb.dut1_name,
                                        'show port {} statistics no-refresh'.format(self.alldut1portstr))

        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.get_captured_count(self.tgenall_Dict)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_equal(self.tgenDictC, 0)
        self.udks.trafficGenerationUdks.trafficStatisticsKeywords.stat_value_should_be_plus_or_minus_percent(
            self.tgenDictD, 500, 1)
