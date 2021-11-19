from Tests.Pytest.Functional.nonprod.BGP.Resources.BgpBase import BgpBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.Functional.nonprod.BGP.Resources.BgpSuiteUdks import BgpSuiteUdks
@fixture()
def test_setup_teardown(request):
     def teardown():
         request.instance.Test_Case_Cleanup()
     request.addfinalizer(teardown)
class License02Tests(BgpBase):
     @mark.ONE_BOX
     def test_02_BGP_Base_License(self):
         '''[Documentation]  Test Objective: This test is intended to be run on unified hardware running EXOS, version 31.4 or later. Configure a base license only and verify 2 BGP peers can be configured. Attempt to configure a 3rd peer and verify an error is returned. The above steps are performed on a child VRF of VR-Default.'''
         # Setup here will run the "Test Suite Setup" in the Resources -> SuiteUdks.robot
         #  change this along the lines of "[Setup]  Test Case Setup" if you have a setup specific to a subset of test cases.
         #[Setup]
         print('  (Step 1) Verify effective license level is Base')
         self.localsuiteudks.Verify_Base_License(self.tb.config.netelem1.name)
         print('  (Step 2) Configure local BGP AS and Router ID and Enable BGP on VRF')
         self.localsuiteudks.Create_BGP_Instance(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp,self.tb.config.globalvars.vr.vrf_name)
         self.localsuiteudks.Verify_BGP_Enabled(self.tb.config.netelem1.name,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 3) Create 2 BGP neighbors on VRF')
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vrf_name)
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 4) Attempt to create a third neighbor with base license on VRF.')
         self.localsuiteudks.Create_BGP_Neighbor_Ignore_Error(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer3,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 5) Verify the first two neighbors exist on VRF')
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vrf_name)
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 6) Verify the third neighbor does not exist on VRF')
         self.localsuiteudks.Verify_BGP_Neighbor_Does_Not_Exist(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer3,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 7) Verify only the number of neighbors on VRF is 2')
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.baseNumPeers,self.tb.config.globalvars.vr.vrf_name)
         self.TestCase2Cleanup()
     def TestCase2Cleanup(self):
         print('  (Step 8) Cleanup delete the BGP neighbors')
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.vr.vrf_name)
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.vr.vrf_name)
         self.localsuiteudks.Delete_BGP_Neighbor_Ignore_Invalid(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer3,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 9) Disable BGP and reset AS and router ID')
         self.localsuiteudks.Disable_BGP_Instance(self.tb.config.netelem1.name,self.tb.config.globalvars.vr.vrf_name)
