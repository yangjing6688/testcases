from Tests.Pytest.NonProduction.BGP.Resources.BgpBase import BgpBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.NonProduction.BGP.Resources.BgpSuiteUdks import BgpSuiteUdks
@fixture()
def test_setup_teardown(request):
     def teardown():
         request.instance.Test_Case_Cleanup()
     request.addfinalizer(teardown)
class License09Tests(BgpBase):
     
     @mark.ONE_BOX
     def test_09_BGP_Base_License(self):
         '''[Documentation]  Test Objective: This test is intended to be run on unified hardware running EXOS, version 31.4 or later. Configure a base license only and configure 2 peers one on the default VR and one on a VRF residing under the default VR. Delete 1 peer from the VRF, verify a second peer can then be configured on the default VR.'''
         # Setup here will run the "Test Suite Setup" in the Resources -> SuiteUdks.robot
         #  change this along the lines of "[Setup]  Test Case Setup" if you have a setup specific to a subset of test cases.
         #[Setup]
         print('  (Step 1) Verify effective license level is Base')
         self.localsuiteudks.Verify_Base_License(self.tb.config.netelem1.name)
         print('  (Step 2) Configure local BGP AS and Router ID and Enable BGP on default VR')
         self.localsuiteudks.Create_BGP_Instance(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp)
         print('  (Step 3) Configure local BGP AS and Router ID and Enable BGP on VRF')
         self.localsuiteudks.Create_BGP_Instance(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 4) Create 1 BGP neighbor on default VR')
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.bgp.localAS)
         print('  (Step 5) Create 1 BGP neighbor on VRF')
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 6) Verify the first and only 1 neighbor exist on default VR')
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.bgp.localAS)
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.onePeer)
         print('  (Step 7) Verify the second and only 1 neighbor exist on the VRF')
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vrf_name)
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.onePeer,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 8) Delete 1 BGP neighbor on VRF')
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 9) Verify the neighbor does not exist on the VRF')
         self.localsuiteudks.Verify_BGP_Neighbor_Does_Not_Exist(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vrf_name)
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.zeroPeers,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 10) Create a 2nd BGP neighbor on default VR')
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.localAS)
         print('  (Step 11) Verify only the number of neighbors on default VR is 2')
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.localAS)
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.baseNumPeers)
         self.TestCase9Cleanup()
     def TestCase9Cleanup(self):
         print('  (Step 12) Cleanup delete the BGP neighbors')
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1)
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2)
         print('  (Step 13) Disable BGP and reset AS and router ID')
         self.localsuiteudks.Disable_BGP_Instance(self.tb.config.netelem1.name,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 14) Disable BGP and reset AS and router ID on default-vr')
         self.localsuiteudks.Disable_BGP_Instance(self.tb.config.netelem1.name)
