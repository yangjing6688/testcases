from Tests.Pytest.Functional.nonprod.BGP.Resources.BgpBase import BgpBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.Functional.nonprod.BGP.Resources.BgpSuiteUdks import BgpSuiteUdks
@fixture()
def test_setup_teardown(request):
     def teardown():
         request.instance.Test_Case_Cleanup()
     request.addfinalizer(teardown)
class License15Tests(BgpBase):
     
     @mark.ONE_BOX
     def test_15_BGP_Base_License(self):
         '''[Documentation]  Test Objective: This test is intended to be run on unified hardware running EXOS, version 31.4 or later. Configure a base license only and verify 3 auto-peers are created on the default VR.  Then create 2 manual peers and verify they reach the established state, finally verify an attempt to create a 3d manually peer is unsuccessful.'''
         # Setup_here_will_run_the "Test_Suite_Setup" in_the_Resources -> SuiteUdks.robot
         #  change_this_along_the_lines_of "[Setup]  Test_Case_Setup" if_you_have_a_setup_specific_to_a_subset_of_test_cases.
         #[Setup]
         print('  (Step 1) Verify effective license level is Base')
         self.localsuiteudks.Verify_Base_License(self.tb.config.netelem1.name)
         self.localsuiteudks.Verify_Base_License(self.tb.config.netelem2.name)
         print('  (Step 2) Configure auto-peering on dut1')
         self.localsuiteudks.Create_Bgp_Autopeering(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.localAS,self.tb.config.dut1.bgp.router_id)
         self.localsuiteudks.Create_BGP_Autopeering(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.localAS,self.tb.config.dut2.bgp.router_id)
         print('  (Step 3) Verify Number of BGP neighbors on dut1 is 3.')
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.numAutoPeers)
         print('  (Step 4) Verify Number of BGP neighbors on dut2 is 3.')
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem2.name,self.tb.config.globalvars.bgp.numAutoPeers)
         print('  (Step 5) Verify 3 peers are established on dut1.')
         self.localsuiteudks.Verify_Three_Auto_Peers_Established(self.tb.config.netelem1.name)
         print('  (Step 6) Verify 3 peers are established on dut2.')
         self.localsuiteudks.Verify_Three_Auto_Peers_Established(self.tb.config.netelem2.name)
         print('  (Step 7) Create 2 BGP neighbors on dut1.')
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer1,self.tb.config.dut1.bgp.remoteAS)
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer2,self.tb.config.dut1.bgp.remoteAS)
         print('  (Step 8) Create 2 BGP neighbors on dut2.')
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer1,self.tb.config.dut2.bgp.remoteAS)
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer2,self.tb.config.dut2.bgp.remoteAS)
         print('  (Step 9) Enable BGP neighbors on dut1.')
         self.localsuiteudks.bgp_enable_neighbor(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer1)
         self.localsuiteudks.bgp_enable_neighbor(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer2)
         print('  (Step 10) Enable BGP neighbors on dut2.')
         self.localsuiteudks.bgp_enable_neighbor(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer1)
         self.localsuiteudks.bgp_enable_neighbor(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer2)
         print('  (Step 11) Verify peering sessions reach the establish state.')
         self.localsuiteudks.bgp_verify_neighbor_state(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer1,state='ESTABLISHED')
         self.localsuiteudks.bgp_verify_neighbor_state(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer2,state='ESTABLISHED')
         self.localsuiteudks.bgp_verify_neighbor_state(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer1,state='ESTABLISHED')
         self.localsuiteudks.bgp_verify_neighbor_state(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer2,state='ESTABLISHED')
         print('  (Step 12) Attempt to create a 3rd peer on dut1')
         self.localsuiteudks.Create_BGP_Neighbor_Ignore_Error(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer3,self.tb.config.dut1.bgp.remoteAS)
         print('  (Step 13) Verify the 3rd peer is not created on dut1')
         self.localsuiteudks.Verify_BGP_Neighbor_Does_Not_Exist(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer3,self.tb.config.dut1.bgp.remoteAS)
         print('  (Step_14) Verify only the number of neighbors on VR-Default is 2 plus the 3 auto-peers (total of 5)')
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.numAutoPlusBase)
         self.TestCase15Cleanup()
     def TestCase15Cleanup(self):
         print('  (Step 15) Cleanup delete the BGP neighbors')
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer1)
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer2)
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer1)
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer2)
         self.localsuiteudks.Delete_BGP_Neighbor_Ignore_Invalid(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer3)
         print('  (Step 16) Delete BGP auto-peering from dut1')
         self.localsuiteudks.Delete_BGP_Autopeering(self.tb.config.netelem1.name)
         print('  (Step 17) Delete BGP auto-peering from dut2')
         self.localsuiteudks.Delete_BGP_Autopeering(self.tb.config.netelem2.name)
