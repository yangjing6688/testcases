from Tests.Pytest.Functional.nonprod.Auto_Peering.Resources.AutoPeeringSuiteUdks import AutoPeeringSuiteUdks
from Tests.Pytest.Functional.nonprod.Auto_Peering.Resources.AutoPeeringBase import AutoPeeringBase
from pytest import fixture


@fixture()
def test_01_auto_peering_teardown(request):
    print("setup - test_01_auto_peering_teardown")

    def teardown():
        print("teardown - test_01_auto_peering_teardown")
        request.instance.defaultLibrary.apiLowLevelApis.bgp.bgp_clear_router_id(request.instance.tb.config.netelem1.name)
        request.instance.defaultLibrary.apiLowLevelApis.bgp.bgp_delete_as(request.instance.tb.config.netelem1.name)
        request.instance.defaultLibrary.apiLowLevelApis.bgp.bgp_clear_auto_peering(request.instance.tb.config.netelem1.name)
        request.instance.defaultLibrary.apiLowLevelApis.bgp.bgp_verify_auto_peering(request.instance.tb.config.netelem1.name, peering_value='0')
        request.instance.defaultLibrary.apiLowLevelApis.bgp.bgp_verify_as(request.instance.tb.config.netelem1.name, asnum='0')
        request.instance.defaultLibrary.apiLowLevelApis.bgp.bgp_verify_routerid(request.instance.tb.config.netelem1.name, '0.0.0.0')
        request.instance.defaultLibrary.deviceNetworkElement.networkElementConnectionManager.close_connection_to_network_element(request.instance.tb.config.netelem1.name)

    request.addfinalizer(teardown)

class AutoPeeringTests(AutoPeeringBase):
  
    def test_01_auto_peering(self, test_01_auto_peering_teardown):
        #Sample Rest BGP auto peering keyword test
        """ Test Objective: Testing BGP auto-peering REST functionalities """
        self.defaultLibrary.deviceNetworkElement.networkElementConnectionManager.connect_to_network_element(self.tb.config.netelem1.name, '10.52.16.34', 'admin', 'enterasysTPB', 'rest', 'exos', auth_mode='basic')
        self.defaultLibrary.apiLowLevelApis.bgp.bgp_set_auto_peering(self.tb.config.netelem1.name, rtrid='10.52.16.32', asnum='32')
        self.defaultLibrary.apiLowLevelApis.bgp.bgp_verify_auto_peering(self.tb.config.netelem1.name, peering_value='1')
        self.defaultLibrary.apiLowLevelApis.bgp.bgp_verify_routerid(self.tb.config.netelem1.name, rtrid='10.52.16.32')
        self.defaultLibrary.apiLowLevelApis.bgp.bgp_verify_as(self.tb.config.netelem1.name, asnum='32')
       