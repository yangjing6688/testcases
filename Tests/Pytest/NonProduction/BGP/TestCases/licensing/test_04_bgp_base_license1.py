from Tests.Pytest.NonProduction.BGP.Resources.BgpBase import BgpBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.NonProduction.BGP.Resources.BgpSuiteUdks import BgpSuiteUdks
@fixture()
def test_setup_teardown(request):
     def teardown():
         request.instance.Test_Case_Cleanup()
     request.addfinalizer(teardown)
class License04Tests(BgpBase):
     
     @mark.ONE_BOX
     def test_04_BGP_Base_License(self):
         '''[Documentation]  Test_Objective: This_test_is_intended_to_be_run_on_unified_hardware_running_EXOS, version_31.4_or_later. Configure_a_base_license_only_and_verify_2_EBGP_peers_can_be_configured. Attempt_to_configure_a_3rd_peer_and_verify_an_error_is_returned. The_above_steps_are_performed_on_a_child_VRF_of_VR-Default.'''
         # Setup here will run the "Test Suite Setup" in the Resources -> SuiteUdks.robot
         #  change this along the lines of "[Setup]  Test Case Setup" if you have a setup specific to a subset of test cases.
         #[Setup]
         print('  (Step 1) Verify effective license level is Base')
         self.localsuiteudks.Verify_Base_License(self.tb.config.netelem1.name)
         print('  (Step 2) Configure local BGP AS and Router ID and Enable BGP on VRF')
         self.localsuiteudks.Create_BGP_Instance(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp,self.tb.config.globalvars.vr.vrf_name)
         self.localsuiteudks.Verify_BGP_Enabled(self.tb.config.netelem1.name,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 3) Create 2 BGP neighbors on VRF')
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.bgp.remoteAS,self.tb.config.globalvars.vr.vrf_name)
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.remoteAS,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 4) Attempt to create a third neighbor with base license on VRF.')
         self.localsuiteudks.Create_BGP_Neighbor_Ignore_Error(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer3,self.tb.config.globalvars.bgp.remoteAS,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 5) Verify the first two neighbors exist on VRF')
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.bgp.remoteAS,self.tb.config.globalvars.vr.vrf_name)
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.remoteAS,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 6) Verify the third neighbor does not exist on VRF')
         self.localsuiteudks.Verify_BGP_Neighbor_Does_Not_Exist(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer3,self.tb.config.globalvars.bgp.remoteAS,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 7) Verify only the number of neighbors on VRF is 2')
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.baseNumPeers,self.tb.config.globalvars.vr.vrf_name)
         self.TestCase4Cleanup()
     def TestCase4Cleanup(self):
         print('  (Step 8) Cleanup delete the BGP neighbors')
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.vr.vrf_name)
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.vr.vrf_name)
         self.localsuiteudks.Delete_BGP_Neighbor_Ignore_Invalid(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer3,self.tb.config.globalvars.vr.vrf_name)
         print('  (Step 9) Disable BGP and reset AS and router ID')
         self.localsuiteudks.Disable_BGP_Instance(self.tb.config.netelem1.name,self.tb.config.globalvars.vr.vrf_name)
