from Tests.Pytest.Functional.nonprod.BGP.Resources.BgpBase import BgpBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.Functional.nonprod.BGP.Resources.BgpSuiteUdks import BgpSuiteUdks
@fixture()
def test_setup_teardown(request):
     def teardown():
         request.instance.Test_Case_Cleanup()
     request.addfinalizer(teardown)
class License13Tests(BgpBase):
     
     @mark.ONE_BOX
     def test_13_BGP_Base_License(self):
         '''[Documentation]  Test Objective: This test is intended to be run on unified hardware running EXOS, version 31.4 or later. Configure a base license only and verify 2 EBGP peers can be configured and esablish on the default VR.'''
         # Setup here will run the "Test Suite Setup" in the Resources -> SuiteUdks.robot
         #  change this along the lines of "[Setup]  Test Case Setup" if you have a setup specific to a subset of test cases.
         #[Setup]
         print('  (Step 1) Verify effective license level is Base')
         self.localsuiteudks.Verify_Base_License(self.tb.config.netelem1.name)
         self.localsuiteudks.Verify_Base_License(self.tb.config.netelem2.name)
         print('  (Step 2) Configure local BGP AS and Router ID and Enable BGP and Verify its enabled')
         self.localsuiteudks.Create_BGP_Instance(self.tb.config.netelem1.name,self.tb.config.dut1.bgp)
         self.localsuiteudks.Create_BGP_Instance(self.tb.config.netelem2.name,self.tb.config.dut2.bgp)
         print('  (Step 3) Create 2 BGP neighbors on dut1.')
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer1,self.tb.config.dut1.bgp.remoteAS)
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer2,self.tb.config.dut1.bgp.remoteAS)
         print('  (Step 4) Create 2 BGP neighbors on dut2.')
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer1,self.tb.config.dut2.bgp.remoteAS)
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer2,self.tb.config.dut2.bgp.remoteAS)
         print('  (Step 5) Enable BGP neighbors on dut1.')
         self.localsuiteudks.bgp_enable_neighbor(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer1)
         self.localsuiteudks.bgp_enable_neighbor(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer2)
         print('  (Step 6) Enable BGP neighbors on dut2.')
         self.localsuiteudks.bgp_enable_neighbor(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer1)
         self.localsuiteudks.bgp_enable_neighbor(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer2)
         print('  (Step 7) Verify peering sessions reach the establish state.')
         self.localsuiteudks.bgp_verify_neighbor_state(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer1,state='ESTABLISHED')
         self.localsuiteudks.bgp_verify_neighbor_state(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer2,state='ESTABLISHED')
         self.localsuiteudks.bgp_verify_neighbor_state(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer1,state='ESTABLISHED')
         self.localsuiteudks.bgp_verify_neighbor_state(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer2,state='ESTABLISHED')
         self.TestCase13Cleanup()
     def TestCase13Cleanup(self):
         print('  (Step 8) Cleanup delete the BGP neighbors')
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer1)
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.peer2)
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer1)
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.peer2)
         print('  (Step 9) Disable BGP and reset AS and router ID')
         self.localsuiteudks.Disable_BGP_Instance(self.tb.config.netelem1.name)
         self.localsuiteudks.Disable_BGP_Instance(self.tb.config.netelem2.name)
