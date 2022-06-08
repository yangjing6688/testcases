"""
Digital Twin - test_10_generic.py
"""

# pylint: disable=import-error
import pytest
from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ..Resources.SuiteUdks import SuiteUdk

@pytest.mark.testbed_1_node
@pytest.mark.usefixtures("dt_cl_test_env")
class GenericTests:
    """Digital Twin Generic Tests"""

    @classmethod
    def setup_class(cls):
        try:
            # Create the pytest execution helper
            cls.executionHelper = PytestExecutionHelper()

            # Create an instance of the helper class that will read in the test bed yaml file and
            # provide basic methods and variable access. The user can also get to the test bed yaml
            # by using the config dictionary
            cls.tb = PytestConfigHelper(config)

            # Load up the suite
            cls.suiteUdks = SuiteUdk()

            # Create new objects to use in test. Import everything from the default library
            cls.defaultLibrary = DefaultLibrary()
        except Exception:
            cls.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(cls):
        pass


    @pytest.mark.p1
    def test_01_dt_logs(self):
        assert self.suiteUdks.verify_no_dt_logs(self.tb.dut1.name)

    @pytest.mark.p1
    def test_02_dt_active(self):
        assert self.suiteUdks.verify_dt_active(self.tb.dut1.name)

    @pytest.mark.p1
    def test_03_system_type(self, dt_cl_test_env):
        if dt_cl_test_env.uses_stacking():
            slot = dt_cl_test_env.get_slot(dt_cl_test_env.get_prim_slot_num())
            sys_type = slot["type"] + " (Stack)"
        else:
            sys_type = dt_cl_test_env.yaml["system"]["slots"][0]["type"] + "-SwitchEngine"

        assert self.suiteUdks.verify_system_type(self.tb.dut1.name, sys_type)

    @pytest.mark.p1
    def test_04_serial_number(self, dt_cl_test_env):
        for slot in dt_cl_test_env.yaml["system"]["slots"]:
            snum = slot.get("serial-number", None)

            if not snum:
                snum = self.suiteUdks.get_serial_num_from_mac(dt_cl_test_env.sys_mac)
                if dt_cl_test_env.uses_stacking():
                    snum += "-" + str(slot["num"])

            # All serial numbers are converted and stored as uppercase in the DT
            snum = "SIM" + snum.upper()

            assert self.suiteUdks.verify_serial_number(self.tb.dut1.name, str(slot["num"]), snum)

    @pytest.mark.p1
    def test_05_vims(self, dt_cl_test_env):
        vims = []

        for slot in dt_cl_test_env.yaml["system"]["slots"]:
            for vim in slot.get("vims", []):
                vims.append(vim["type"] + "-" + str(slot["num"]))

        assert self.suiteUdks.verify_vims(self.tb.dut1.name, vims)

    @pytest.mark.p1
    def test_06_stacking(self, dt_cl_test_env):
        if dt_cl_test_env.uses_stacking():
            assert self.suiteUdks.verify_stacking(self.tb.dut1.name,
                                                  dt_cl_test_env.get_prim_slot_num(),
                                                  len(dt_cl_test_env.yaml["system"]["slots"]))
        else:
            assert self.suiteUdks.verify_no_stacking(self.tb.dut1.name)

    @pytest.mark.p1
    def test_07_switch_mac(self, dt_cl_test_env):
        assert self.suiteUdks.verify_switch_mac(self.tb.dut1.name, dt_cl_test_env.sys_mac)

    @pytest.mark.p1
    def test_08_licenses(self, dt_cl_test_env):
        lic_str = dt_cl_test_env.yaml["system"].get("license")
        if not lic_str:
            lic_str = ""
        licenses = lic_str.split(",")
        assert self.suiteUdks.verify_licenses(self.tb.dut1.name, licenses)

    @pytest.mark.p1
    def test_09_cloudserver(self, dt_cl_test_env):
        server = dt_cl_test_env.yaml["system"].get("cloud-server")
        if not server:
            server = ""
        assert self.suiteUdks.verify_cloudserver(self.tb.dut1.name, server)

    @pytest.mark.p1
    def test_10_oper_states(self, dt_cl_test_env):
        slot_nums = [str(slot["num"]) for slot in dt_cl_test_env.yaml["system"]["slots"]]
        assert self.suiteUdks.verify_card_states(self.tb.dut1.name, slot_nums, "Operational")

    @pytest.mark.p1
    def test_11_node_states(self, dt_cl_test_env):
        if dt_cl_test_env.uses_stacking():
            slot_nums = [str(slot["num"]) for slot in dt_cl_test_env.yaml["system"]["slots"]]
            assert self.suiteUdks.verify_node_states(self.tb.dut1.name, slot_nums,
                                                     dt_cl_test_env.get_prim_slot_num())
    @pytest.mark.p1
    def test_12_dt_mgmt(self):
        assert self.suiteUdks.verify_dt_mgmt(self.tb.dut1.name,
                                             pytest.use_dt_mgmt) # pylint: disable=no-member
