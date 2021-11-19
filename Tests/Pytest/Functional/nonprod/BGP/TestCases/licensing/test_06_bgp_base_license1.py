from Tests.Pytest.Functional.nonprod.BGP.Resources.BgpBase import BgpBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.Functional.nonprod.BGP.Resources.BgpSuiteUdks import BgpSuiteUdks
@fixture()
def test_setup_teardown(request):
     def teardown():
         request.instance.Test_Case_Cleanup()
     request.addfinalizer(teardown)
class License06Tests(BgpBase):
     
     @mark.ONE_BOX
     def test_06_BGP_Base_License(self):
         '''[Documentation]  Test Objective: This test is intended to be run on unified hardware running EXOS, version 31.4 or later. Configure a base license only and verify peers can not be created on a VRF residing under a parent non default user VR.'''
         # Setup here will run the "Test Suite Setup" in the Resources -> SuiteUdks.robot
         #  change this along the lines of "[Setup]  Test Case Setup" if you have a setup specific to a subset of test cases.
         #[Setup]
         print('  (Step 1) Verify effective license level is Base')
         self.localsuiteudks.Verify_Base_License(self.tb.config.netelem1.name)
         print('  (Step 2) Configure local BGP AS and Router ID and Enable BGP on VRF under non default user VR')
         self.localsuiteudks.Create_BGP_Instance(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp,self.tb.config.globalvars.vr.vrf_off_user_name)
         print('  (Step 3) Attempt to create 2 BGP neighbors on VRF under non default user VR')
         self.localsuiteudks.Create_BGP_Neighbor_Ignore_Error(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vrf_off_user_name)
         self.localsuiteudks.Create_BGP_Neighbor_Ignore_Error(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vrf_off_user_name)
         print('  (Step 4) Verify neither neighbor exists on VRF under non default user VR')
         self.localsuiteudks.Verify_BGP_Neighbor_Does_Not_Exist(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vrf_off_user_name)
         self.localsuiteudks.Verify_BGP_Neighbor_Does_Not_Exist(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vrf_off_user_name)
         print('  (Step 5) Verify only the number of neighbors on VRF under non default is 0')
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.zeroPeers,self.tb.config.globalvars.vr.vrf_off_user_name)
         self.TestCase6Cleanup()
     def TestCase6Cleanup(self):
         print('  (Step 6) Delete neighbors if necessary')
         self.localsuiteudks.Delete_BGP_Neighbor_Ignore_Invalid(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.vr.vrf_off_user_name)
         self.localsuiteudks.Delete_BGP_Neighbor_Ignore_Invalid(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.vr.vrf_off_user_name)
         print('  (Step 7) Disable BGP and reset AS and router ID')
         self.localsuiteudks.Disable_BGP_Instance(self.tb.config.netelem1.name,self.tb.config.globalvars.vr.vrf_off_user_name)
