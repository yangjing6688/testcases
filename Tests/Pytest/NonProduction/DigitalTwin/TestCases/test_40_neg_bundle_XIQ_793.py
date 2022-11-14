"""
Digital Twin - test_40_neg_bundle.py
"""

import os
from pytest_testconfig import config
from pytest import mark
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ..Resources.SuiteUdks import SuiteUdk
from ..Resources.shared import UPLOAD_PATH
from ..Resources.shared import DtTestEnv


@mark.testbed_1_node
@mark.usefixtures("dt_fn_test_env")
class NegativeBundleTests:
    """Digital Twin Negative Bundle-Related Tests.

    Note that these tests are dependent on earlier tests.  For instance, the create
    must be done to get the initial bundle for applying to other DTs.
    """

    class Data:  # pylint: disable=too-few-public-methods
        """Simple Data class to make sharing data across tests and DtTestEnv's easier"""
        def __init__(self, prefix):
            # The prefix will be something like bc_00
            self.dt_file = os.path.join("/usr/local/tmp", prefix + ".tgz")
            self.filename = os.path.basename(self.dt_file)
            self.local_file = os.path.join(UPLOAD_PATH, self.filename)

        def cleanup(self):
            """Cleanup any local data that may be leftover"""
            if os.path.exists(self.local_file):
                os.remove(self.local_file)

    data_objects = {}

    @classmethod
    def data_object(cls, yaml_file):
        """Get or create the data object for this environment"""
        # For a file like bc_001.yaml, the key will be bc_00
        key = os.path.splitext(yaml_file)[0][:-1]
        if key not in cls.data_objects:
            cls.data_objects[key] = cls.Data(key)
        return cls.data_objects[key]


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
        # Cleanup by removing the local files
        for data in cls.data_objects.values():
            data.cleanup()


    @mark.p3
    @mark.parametrize("dte_fn_envs", [DtTestEnv('bc_001.yaml'), DtTestEnv('bc_011.yaml')], ids=str)
    def test_01_neg_create_bundle(self, dt_fn_test_env):
        self.defaultLibrary.apiLowLevelApis.hostUtils.enable_debug_mode(self.tb.dut1.name)
        data = self.data_object(dt_fn_test_env.yaml_file)

        assert self.suiteUdks.create_bundle(self.tb.dut1.name, data.dt_file)
        assert self.suiteUdks.upload_bundle(self.tb.dut1.name, dt_fn_test_env.get_dflt_mgmt_vrid(),
                                            data.local_file, data.filename, data.dt_file)

    @mark.p3
    @mark.parametrize("dte_fn_envs", [DtTestEnv('bc_002.yaml'), DtTestEnv('bc_012.yaml')], ids=str)
    def test_02_neg_apply_bad_type(self, dt_fn_test_env):
        self.defaultLibrary.apiLowLevelApis.hostUtils.enable_debug_mode(self.tb.dut1.name)
        data = self.data_object(dt_fn_test_env.yaml_file)

        assert os.path.isfile(data.local_file), \
            "Bundle {data.local_file} was not uploaded for test setup"
        assert self.suiteUdks.download_bundle(self.tb.dut1.name,
                                              dt_fn_test_env.get_dflt_mgmt_vrid(), data.local_file,
                                              data.dt_file)
        assert self.suiteUdks.apply_bundle_failure(self.tb.dut1.name, data.dt_file,
            r"Slot .* card type in bundle (.*) must match slot .* "
            r"card type in the running system (.*)")

    @mark.p3
    @mark.parametrize("dte_fn_envs", [DtTestEnv('bc_003.yaml'), DtTestEnv('bc_013.yaml')], ids=str)
    def test_03_neg_apply_bad_stack(self, dt_fn_test_env):
        self.defaultLibrary.apiLowLevelApis.hostUtils.enable_debug_mode(self.tb.dut1.name)
        data = self.data_object(dt_fn_test_env.yaml_file)

        assert os.path.isfile(data.local_file), \
            "Bundle {data.local_file} was not uploaded for test setup"
        assert self.suiteUdks.download_bundle(self.tb.dut1.name,
                                              dt_fn_test_env.get_dflt_mgmt_vrid(), data.local_file,
                                              data.dt_file)
        assert self.suiteUdks.apply_bundle_failure(self.tb.dut1.name, data.dt_file,
            r"Stacking status in bundle (.*) must match stacking status in the running system (.*)")

    @mark.p3
    @mark.parametrize("dte_fn_envs", [DtTestEnv('bc_004.yaml'), DtTestEnv('bc_014.yaml')], ids=str)
    def test_04_neg_apply_bad_license(self, dt_fn_test_env):
        self.defaultLibrary.apiLowLevelApis.hostUtils.enable_debug_mode(self.tb.dut1.name)
        data = self.data_object(dt_fn_test_env.yaml_file)

        assert os.path.isfile(data.local_file), \
            "Bundle {data.local_file} was not uploaded for test setup"
        assert self.suiteUdks.download_bundle(self.tb.dut1.name,
                                              dt_fn_test_env.get_dflt_mgmt_vrid(), data.local_file,
                                              data.dt_file)
        assert self.suiteUdks.apply_bundle_failure(self.tb.dut1.name, data.dt_file,
            r"Device license in bundle (.*) is not compatible with device license "
            r"in the running system (.*)")

    @mark.p3
    @mark.parametrize("dte_fn_envs", [DtTestEnv('bc_005.yaml'), DtTestEnv('bc_015.yaml')], ids=str)
    def test_05_neg_apply_bad_vim_type(self, dt_fn_test_env):
        self.defaultLibrary.apiLowLevelApis.hostUtils.enable_debug_mode(self.tb.dut1.name)
        data = self.data_object(dt_fn_test_env.yaml_file)

        assert os.path.isfile(data.local_file), \
            "Bundle {data.local_file} was not uploaded for test setup"
        assert self.suiteUdks.download_bundle(self.tb.dut1.name,
                                              dt_fn_test_env.get_dflt_mgmt_vrid(), data.local_file,
                                              data.dt_file)
        assert self.suiteUdks.apply_bundle_failure(self.tb.dut1.name, data.dt_file,
            r"VIM type for slot .* in bundle (.*) must match VIM type for slot .* "
            r"in the running system (.*)")

    @mark.p3
    @mark.parametrize("dte_fn_envs", [DtTestEnv('bc_006.yaml'), DtTestEnv('bc_016.yaml')], ids=str)
    def test_06_neg_apply_bad_vim_cfg(self, dt_fn_test_env):
        self.defaultLibrary.apiLowLevelApis.hostUtils.enable_debug_mode(self.tb.dut1.name)
        data = self.data_object(dt_fn_test_env.yaml_file)

        assert os.path.isfile(data.local_file), \
            "Bundle {data.local_file} was not uploaded for test setup"
        assert self.suiteUdks.download_bundle(self.tb.dut1.name,
                                              dt_fn_test_env.get_dflt_mgmt_vrid(), data.local_file,
                                              data.dt_file)
        assert self.suiteUdks.apply_bundle_failure(self.tb.dut1.name, data.dt_file,
            r"Number of VIMs for slot .* in bundle (.*) must match number of VIMs "
            r"for slot .* in the running system (.*)")
