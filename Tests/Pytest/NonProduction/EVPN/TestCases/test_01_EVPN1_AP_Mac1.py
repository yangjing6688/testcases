from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from pytest import mark
from Tests.Pytest.NonProduction.EVPN.Resources.SuiteUdks import SuiteUdk


################################################
# Run all tests:
#    pytest --tc-file=<path to test bed yaml>
# Run all P1:
#    pytest -m p1 --tc-file=<path to test bed yaml>
# Run all P1 and P2:
#    pytest -m "p1 or p2" --tc-file=<path to test bed yaml>
#
# Note: There are extra options in the pytest.ini file that will be appended.
#
# The test should produce a report.html file when the run is completed
#

@mark.required_capability('Fabric')
class EvpnApMacTests:
    ###########################################################################
    # This test suite is responsible for testing the Mac Move functionality
    # within the EVPN framework.
    #
    # Variables used by tests in this class
    vlan_a_name = 'vlan_a'
    vlan_a_tag = '10'
    vlan_a_nsi = '10010'
    dut1_rtrid = '1.1.1.101'
    dut1_asnum = '101'
    dut2_rtrid = '2.2.2.102'
    dut2_asnum = '102'


    # [Setup]  Test class Setup
    # This is a class method and the instance(self) is not passed.
    # Hence the cls parameter and not the self parameter.
    def setup_class(cls):
        try:
            # Create the pytest execution helper
            cls.executionHelper = PytestExecutionHelper()
            
            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            cls.tb = PytestConfigHelper(config)
            
            # Load up the suite
            cls.suiteUdks = SuiteUdk()
            
            # Create new objects to use in test. Here we will import everything from the default library
            cls.defaultLibrary = DefaultLibrary()

            # Create a shorter version for the UDKs
            cls.udks = cls.defaultLibrary.apiUdks

            # Create a shorter version for the UDKs
            cls.llapis = cls.defaultLibrary.apiLowLevelApis

            # Create a shorter version for cli send
            cls.cliSend = cls.defaultLibrary.deviceNetworkElement.networkElementCliSend

            # Call the setup
            cls.udks.setupTeardownUdks.Base_Test_Suite_Setup()

            # DUT 1 Configuration
            cls.dut1_vlan_port_list = [cls.tb.dut1_tgen_port_a.ifname]
            cls.dut1_test_port_list = [cls.tb.dut1_isl_dut2_port_a.ifname,
                                       cls.tb.dut1_isl_dut2_port_b.ifname,
                                       cls.tb.dut1_isl_dut2_port_c.ifname,
                                       cls.tb.dut1_isl_dut2_port_d.ifname,
                                       cls.tb.dut1_tgen_port_a.ifname]
            cls.suiteUdks.setup_AP_and_one_vnet_cfg(cls.tb.dut1_name,
                                                    cls.dut1_rtrid,
                                                    cls.dut1_asnum,
                                                    cls.vlan_a_name,
                                                    cls.vlan_a_tag,
                                                    cls.vlan_a_nsi,
                                                    cls.dut1_vlan_port_list,
                                                    cls.dut1_test_port_list)

            # DUT 2 Configuration
            cls.dut2_vlan_port_list = [cls.tb.dut2_tgen_port_a.ifname]
            cls.dut2_test_port_list = [cls.tb.dut2_isl_dut1_port_a.ifname,
                                       cls.tb.dut2_isl_dut1_port_b.ifname,
                                       cls.tb.dut2_isl_dut1_port_c.ifname,
                                       cls.tb.dut2_isl_dut1_port_d.ifname,
                                       cls.tb.dut2_tgen_port_a.ifname]
            cls.suiteUdks.setup_AP_and_one_vnet_cfg(cls.tb.dut2_name,
                                                    cls.dut2_rtrid,
                                                    cls.dut2_asnum,
                                                    cls.vlan_a_name,
                                                    cls.vlan_a_tag,
                                                    cls.vlan_a_nsi,
                                                    cls.dut2_vlan_port_list,
                                                    cls.dut2_test_port_list)

        except Exception:
            # Setup has failed, so set the flag
            cls.executionHelper.setSetupFailure(True)

    # [Teardown]  Test class Cleanup
    # This is a class method and the instance(self) not passed.
    # Hence the cls parameter and not the self parameter.
    def teardown_class(cls):
        # DUT 1 Configuration
        cls.suiteUdks.teardown_AP_and_one_vlan_cfg(cls.tb.dut1_name,cls.vlan_a_tag)
        # DUT 2 Configuration
        cls.suiteUdks.teardown_AP_and_one_vlan_cfg(cls.tb.dut2_name,cls.vlan_a_tag)

        cls.udks.setupTeardownUdks.Base_Test_Suite_Cleanup()



    # Test Cases:
    # The test case name must be test_[number]_action format. If pytest is going to treat this as a test case the prefix must be test_.
    # Any other utility classes can be written in the ../Resources
    # The marks are defined in the pytest.ini file at the root of this project.
    #

    # Test: do_mac_move_to_limit
    # This test uses a two node auto-peer BGP network and then
    # moves a single mac between the two peers on either side of
    # the EVPN created tunnel. The movement of the mac is checked after
    # each move, and the sequence number increment is verified until the
    # maximum number of moves has been done within the permitted EVPN
    # move interval.
    # Then the log is checked to see if the the proper "max move" notification has been logged.
    # Finally the log is checked after the hold down interval has expired to see if the condition has cleared.
    @mark.p1  # Marked as a P1 test case
    def test_01_do_mac_move_to_limit(self):
        # Don't bother executing this test if setup failed.
        self.executionHelper.testSkipCheck()

        print("###############################################################################")
        print("# TEST 01                                                                     #")
        print("# test_01_do_mac_move_to_limit                                                #")
        print("###############################################################################")

        # first make sure we are converged
        cmd = "show bgp routes l2vpn-evpn inclusive-multicast all"
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut1_name,cmd,"102\s+10010\s+fe",max_wait=65)
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut2_name,cmd,"101\s+10010\s+fe",max_wait=65)

        # Create the packet information
        packet_a = 'packetA'
        packet_b = 'packetB'
        packet_a_bcast = 'packetA_bcast'
        packet_b_bcast = 'packetB_bcast'

        # Clear out the fdb entries on vlan_a
        # self.udks.fdbUdks.NetworkElementFdbGenKeywords.fdb_clear_all_vlan(self.tb.dut1_name,vlan_a_tag,vlan_a_name)
        # self.udks.fdbUdks.NetworkElementFdbGenKeywords.fdb_clear_all_vlan(self.tb.dut2_name,vlan_a_tag,vlan_a_name)

        tgen_port_a = self.tb.createTgenPort(self.tb.tgen1_name, self.tb.tgen_dut1_port_a.ifname)
        tgen_port_b = self.tb.createTgenPort(self.tb.tgen1_name, self.tb.tgen_dut2_port_a.ifname)

        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet(packet_a, '00:22:22:22:22:22', '00:11:11:11:11:11', self.vlan_a_tag)
        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet(packet_b, '00:11:11:11:11:11', '00:22:22:22:22:22', self.vlan_a_tag)
        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet(packet_a_bcast, 'FF:FF:FF:FF:FF:FF', '00:11:11:11:11:11', self.vlan_a_tag)
        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet(packet_b_bcast, 'FF:FF:FF:FF:FF:FF', '00:22:22:22:22:22', self.vlan_a_tag)

        # Prime the pump
        self.udks.trafficGenerationUdks.Prime_Traffic_Bidirectionally(tgen_port_a,
                                                                      tgen_port_b,
                                                                      packet_a,
                                                                      packet_b)
        # send the bidirectional packets
        self.udks.trafficGenerationUdks.Transmit_Traffic_Bidirectionally_and_Verify_it_was_Received(tgen_port_a,
                                                                                                    tgen_port_b,
                                                                                                    packet_a,
                                                                                                    packet_b,
                                                                                                    packet_b,
                                                                                                    packet_a,
                                                                                                    tx_count=10)
        # send packet_a_bcast.
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(tgen_port_a, packet_a_bcast);
        # Sequence count should be 0.
        cmd = "show bgp evpn mac mac-address 00:11:11:11:11:11"
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut2_name,cmd,"R\s+10\s+00:11:11:11:11:11\s+1\.1\.1\.101\s+10010\s+Yes\s+0")

        # send packet_a_bcast from other side.
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(tgen_port_b,packet_a_bcast);
        # sequence count should be local and 1.
        cmd = "show bgp evpn mac mac-address 00:11:11:11:11:11"
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut2_name, cmd,"L\s+10\s+00:11:11:11:11:11\s+10010\s+Yes\s+1")

        # And back again.
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(tgen_port_a,packet_a_bcast);
        # sequence count should be remote and 2.
        cmd = "show bgp evpn mac mac-address 00:11:11:11:11:11"
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut2_name,cmd,"R\s+10\s+00:11:11:11:11:11\s+1\.1\.1\.101\s+10010\s+Yes\s+2")

        # And again.
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(tgen_port_b,packet_a_bcast);
        # sequence count should be local and 3.
        cmd = "show bgp evpn mac mac-address 00:11:11:11:11:11"
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut2_name, cmd,"L\s+10\s+00:11:11:11:11:11\s+10010\s+Yes\s+3")

        # And back again.
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(tgen_port_a,packet_a_bcast);
        # sequence count should be remote and 4.
        cmd = "show bgp evpn mac mac-address 00:11:11:11:11:11"
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut2_name,cmd,"R\s+10\s+00:11:11:11:11:11\s+1\.1\.1\.101\s+10010\s+Yes\s+4")

        # And again.
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(tgen_port_b,packet_a_bcast);
        # sequence count should be local and 5.
        cmd = "show bgp evpn mac mac-address 00:11:11:11:11:11"
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut2_name, cmd,"L\s+10\s+00:11:11:11:11:11\s+10010\s+Yes\s+5")

        # And back again.
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(tgen_port_a,packet_a_bcast);
        # sequence count should be remote and 6.
        cmd = "show bgp evpn mac mac-address 00:11:11:11:11:11"
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut2_name,cmd,"R\s+10\s+00:11:11:11:11:11\s+1\.1\.1\.101\s+10010\s+Yes\s+6")

        # And again.
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(tgen_port_b,packet_a_bcast);
        # sequence count should be local and 7.
        cmd = "show bgp evpn mac mac-address 00:11:11:11:11:11"
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut2_name, cmd,"L\s+10\s+00:11:11:11:11:11\s+10010\s+Yes\s+7")

        # And back again.
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(tgen_port_a,packet_a_bcast);
        # sequence count should be remote and 8.
        cmd = "show bgp evpn mac mac-address 00:11:11:11:11:11"
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut2_name,cmd,"R\s+10\s+00:11:11:11:11:11\s+1\.1\.1\.101\s+10010\s+Yes\s+8")

        # And again.
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(tgen_port_b,packet_a_bcast);
        # sequence count should be local and 9.
        cmd = "show bgp evpn mac mac-address 00:11:11:11:11:11"
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut2_name, cmd,"L\s+10\s+00:11:11:11:11:11\s+10010\s+Yes\s+9")

        # The next move should cause a log entry. Clear the log show we now that we found a new entry
        self.llapis.logging.logging_clear_log(self.tb.dut2_name)

        # And back again.
        self.udks.trafficGenerationUdks.Transmit_Packet_on_Port_Single_Burst(tgen_port_a,packet_a_bcast);

        # We should have hit the max and the LOG should have a notification.
        strtomatch = "EVPN Entity.+has multiple moves of MAC 00:11:11:11:11:11"
        self.llapis.logging.logging_verify_regex_in_log(self.tb.dut2_name,strtomatch)

        # After the show command below returns ~60 seconds, we should have returned to normal learning for this mac.
        # and a log entry should be added. Clear the log so we know it will be a new message.
        self.llapis.logging.logging_clear_log(self.tb.dut2_name)

        # sequence count should be remote and 10.
        cmd = "show bgp evpn mac mac-address 00:11:11:11:11:11"
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut2_name,cmd,"R\s+10\s+00:11:11:11:11:11\s+1\.1\.1\.101\s+10010\s+Yes\s+10",max_wait=65)

        # The notification interval of 60 seconds should have elapsed by now and
        # a LOG entry should exist.
        strtomatch = "EVPN Entity.+cleared multiple moves of MAC 00:11:11:11:11:11"
        self.llapis.logging.logging_verify_regex_in_log(self.tb.dut2_name,strtomatch)


    # Test: test_02_sticky_mac_detect_and_clear
    # This test uses a two node auto-peer BGP network left configured from the
    # previous test. It invokes an fdb create mac command to create the same
    # static mac on the same vlan on both sides of the EVPN/VXLAN tunnel.
    # this should cause a Sticky MAC error to appear in the log. Then the mac
    # deleted from one side and the condition should be logged as cleared.
    @mark.p1  # Marked as a P1 test case
    def test_02_sticky_mac_detect_and_clear(self):
        # Don't bother executing this test if setup failed.
        self.executionHelper.testSkipCheck()

        print("###############################################################################")
        print("# TEST 02                                                                     #")
        print("# test_02_sticky_mac_detect_and_clear                                         #")
        print("###############################################################################")
        sticky_mac = "00:00:00:01:01:01"

        # first make sure we are converged
        cmd = "show bgp routes l2vpn-evpn inclusive-multicast all"
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut1_name,cmd,"102\s+10010\s+fe",max_wait=65)
        self.cliSend.send_cmd_verify_output_regex(self.tb.dut2_name,cmd,"101\s+10010\s+fe",max_wait=65)

        # Clear the log
        self.llapis.logging.logging_clear_log(self.tb.dut1_name)
        self.llapis.logging.logging_clear_log(self.tb.dut2_name)

        # On DUT 1
        self.udks.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.tb.dut1_name,sticky_mac,self.vlan_a_tag,self.tb.dut1_tgen_port_a.ifname,self.vlan_a_name)
        # On DUT 2 - this Should create the log condition
        self.udks.fdbUdks.Add_Static_FDB_Entry_and_Validate_It_Exists(self.tb.dut2_name,sticky_mac,self.vlan_a_tag,self.tb.dut2_tgen_port_a.ifname,self.vlan_a_name)

        # Check the logs
        strtomatch = "\s*EVPN Entity\s+" + self.vlan_a_tag + "\s+has detected a sticky mac\s*" + sticky_mac
        # We should have a notification on DUT1.
        self.llapis.logging.logging_verify_regex_in_log(self.tb.dut1_name,strtomatch)
        # We should have a notification on DUT2.
        self.llapis.logging.logging_verify_regex_in_log(self.tb.dut2_name,strtomatch)

        # Clear the log on the duts
        self.llapis.logging.logging_clear_log(self.tb.dut1_name)
        self.llapis.logging.logging_clear_log(self.tb.dut2_name)

        # On DUT 1 - Note the validate variant of this command does not validate the port. Trust it worked.
        self.llapis.fdb.fdb_delete_entry(self.tb.dut1_name,sticky_mac,self.vlan_a_tag,self.vlan_a_name,ignore_cli_feedback=True)

        # Check the logs
        strtomatch = "\s*EVPN Entity\s+" + self.vlan_a_tag + "\s+cleared a sticky mac\s*" + sticky_mac
        # We should have cleared the notification on DUT1.
        self.llapis.logging.logging_verify_regex_in_log(self.tb.dut1_name,strtomatch)
        # We should have cleared the notification on DUT2.
        self.llapis.logging.logging_verify_regex_in_log(self.tb.dut2_name,strtomatch)

        # Clean up DUT 2 - Note the validate variant of this command does not validate the port. Trust it worked.
        self.llapis.fdb.fdb_delete_entry(self.tb.dut2_name,sticky_mac,self.vlan_a_tag,self.vlan_a_name,ignore_cli_feedback=True)
