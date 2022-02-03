from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from pytest import mark
from Tests.Pytest.Demos.DefaultTemplate.Resources.SuiteUdks import SuiteUdk


class DetermineTBStatusTests:

    # [Setup]  Test class Setup
    @classmethod
    def setup_class(cls):
        try:
            # Create the pytest execution helper
            cls.executionHelper = PytestExecutionHelper()

            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            cls.tb = PytestConfigHelper(config)

            # Create new objects to use in test. Here we will import everything from the default library
            cls.defaultLibrary = DefaultLibrary()

            cls.trafficGeneratorConnectionManager = cls.defaultLibrary.apiLowLevelTrafficApis.trafficGeneratorConnectionManager

            cls.networkElementConnectionManager = cls.defaultLibrary.deviceNetworkElement.networkElementConnectionManager

            cls.connection_report = []
        except Exception:
            cls.executionHelper.setSetupFailure(True)

    # [Teardown]  Test class Cleanup
    @classmethod
    def teardown_class(cls):
        cls.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()

        print("Test Bed Report")
        print("******************************************************************************************")
        for element in cls.connection_report:
            print(" Element: " + str(element['name']) + " Type: " + str(element['type']) + " IP: " + str(
                element['ip']) + " Port: " + str(element['port']) + " Connected: " + str(element['connected']))
        print("******************************************************************************************")

    def connect_to_elements(self, **kwargs):
        netelem_dict = self.networkElementConnectionManager.build_dict_of_netelems(**kwargs)
        for netelem_name in netelem_dict:
            if not netelem_dict[netelem_name]["skip_connect"]:
                netelem_ip = netelem_dict[netelem_name]["netelem_ip"]
                netelem_user = netelem_dict[netelem_name]["netelem_user"]
                netelem_pass = netelem_dict[netelem_name]["netelem_pass"]
                netelem_con_method = netelem_dict[netelem_name]["netelem_con_method"]
                netelem_os = netelem_dict[netelem_name]["netelem_os"]
                netelem_port = netelem_dict[netelem_name]["netelem_port"]
                netelem_platform = netelem_dict[netelem_name]["netelem_platform"]
                netelem_version = netelem_dict[netelem_name]["netelem_version"]
                netelem_unit = netelem_dict[netelem_name]["netelem_unit"]
                snmp_info = netelem_dict[netelem_name]["snmp_info"]
                auth_mode = netelem_dict[netelem_name]["auth_mode"]
                verify_cert = netelem_dict[netelem_name]["verify_cert"]

                element_connection = dict()
                element_connection['name'] = netelem_name
                element_connection['ip'] = netelem_ip
                element_connection['user'] = netelem_user
                element_connection['password'] = netelem_pass
                element_connection['port'] = netelem_port
                element_connection['type'] = 'netelem'
                try:
                    self.networkElementConnectionManager.connect_to_network_element(netelem_name, netelem_ip,
                                                                                    netelem_user, netelem_pass,
                                                                                    netelem_con_method, netelem_os,
                                                                                    netelem_port, netelem_platform,
                                                                                    netelem_version, netelem_unit,
                                                                                    snmp_info=snmp_info,
                                                                                    auth_mode=auth_mode,
                                                                                    verify_cert=verify_cert, **kwargs)
                    element_connection['connected'] = True
                except:
                    element_connection['connected'] = False
                finally:
                    self.connection_report.append(element_connection)

        tgen_dict = self.trafficGeneratorConnectionManager.build_dict_of_tgens(**kwargs)

        for device_name in tgen_dict:
            if not tgen_dict[device_name]["skip_connect"]:
                tgen_vendor = tgen_dict[device_name]["tgen_vendor"]
                tgen_chassis_ip = tgen_dict[device_name]["tgen_chassis_ip"]
                tgen_vm_ip = tgen_dict[device_name]["tgen_vm_ip"]
                tgen_user = tgen_dict[device_name]["tgen_user"]
                tgen_pass = tgen_dict[device_name]["tgen_pass"]
                tgen_port = tgen_dict[device_name]["tgen_port"]
                tgen_max_wait = tgen_dict[device_name]["tgen_max_wait"]
                jets_dir = tgen_dict[device_name]["jets_dir"]
                view_tag = tgen_dict[device_name]["view_tag"]

                element_connection = dict()
                element_connection['name'] = device_name
                element_connection['ip'] = tgen_chassis_ip
                element_connection['user'] = tgen_user
                element_connection['password'] = tgen_pass
                element_connection['port'] = tgen_port
                element_connection['type'] = 'tgen'

                try:
                    if tgen_vendor.lower() == "jets":
                        self.trafficGeneratorConnectionManager.connect_to_traffic_generator(device_name, tgen_vendor,
                                                                                            tgen_chassis_ip, tgen_vm_ip,
                                                                                            tgen_user,
                                                                                            tgen_port, tgen_max_wait,
                                                                                            tgen_pass,
                                                                                            jets_dir=jets_dir,
                                                                                            view_tag=view_tag, **kwargs)
                        element_connection['connected'] = True
                    else:
                        self.trafficGeneratorConnectionManager.connect_to_traffic_generator(device_name, tgen_vendor,
                                                                                            tgen_chassis_ip, tgen_vm_ip,
                                                                                            tgen_user,
                                                                                            tgen_port, tgen_max_wait,
                                                                                            tgen_pass, **kwargs)
                        element_connection['connected'] = True
                except:
                    element_connection['connected'] = False
                finally:
                    self.connection_report.append(element_connection)

    def test_01_testConnection_with_switches(self):
        self.executionHelper.testSkipCheck()
        self.connect_to_elements()


