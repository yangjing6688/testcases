"""
Digital Twin - test_20_negative.py
"""

# pylint: disable=import-error
from pytest_testconfig import config
from pytest import mark
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ..Resources.SuiteUdks import SuiteUdk
from ..Resources.shared import DtTestEnv


@mark.testbed_1_node
@mark.usefixtures("dt_fn_test_env")
class NegativeTests:
    """Digital Twin Negative Tests"""

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


    @mark.p3
    @mark.parametrize("dte_fn_envs", [DtTestEnv('neg_004.yaml'), DtTestEnv('neg_006.yaml'),
                                      DtTestEnv('neg_007.yaml'), DtTestEnv('neg_008.yaml'),
                                      DtTestEnv('neg_009.yaml')],
                      ids=str)
    def test_01_verify_error(self):
        """Look for the "Unable to load..." error, but not the specific error details"""
        assert self.suiteUdks.verify_dt_log_error(self.tb.dut1.name)

    @mark.p3
    @mark.parametrize("dte_fn_envs", [DtTestEnv('neg_005.yaml')], ids=str)
    def test_02_verify_warning(self):
        """Look for a "Warning", but not the specific warning details"""
        assert self.suiteUdks.verify_dt_log_warning(self.tb.dut1.name)

    @mark.p3
    @mark.parametrize("dte_fn_envs", [DtTestEnv('neg_001.yaml')], ids=str)
    def test_03_wrong_single_slot_num(self):
        assert self.suiteUdks.verify_dt_log_error(self.tb.dut1.name, "Slot 1 must be defined")

    @mark.p3
    @mark.parametrize("dte_fn_envs", [DtTestEnv('neg_002.yaml')], ids=str)
    def test_04_serial_num_too_long(self):
        assert self.suiteUdks.verify_dt_log_error(self.tb.dut1.name,
                                                  r"\"serial-number\".*is too long")

    @mark.p3
    @mark.parametrize("dte_fn_envs", [DtTestEnv('neg_003.yaml')], ids=str)
    def test_05_primary_true_no_stacking(self):
        warn_str = r"Ignoring primary definition for slot \d+ \(stacking is not enabled\)"
        assert self.suiteUdks.verify_dt_log_warning(self.tb.dut1.name, warn_str)

    @mark.p3
    @mark.parametrize("dte_fn_envs", [DtTestEnv('neg_010.yaml')], ids=str)
    def test_06_invalid_cloudserver_type(self):
        warn_str = r"Ignoring invalid \"cloud-server-type\""
        assert self.suiteUdks.verify_dt_log_warning(self.tb.dut1.name, warn_str)
