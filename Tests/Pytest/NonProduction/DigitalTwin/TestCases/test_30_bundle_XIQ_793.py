"""
Digital Twin - test_30_bundle.py
"""

import os
from pytest_testconfig import config
from pytest import mark
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ..Resources.SuiteUdks import SuiteUdk
from ..Resources.shared import UPLOAD_PATH

@mark.testbed_1_node
@mark.usefixtures("dt_cl_test_env")
class BundleTests:
    """Digital Twin Bundle-Related Tests.

    Note that these tests are dependent on earlier tests.  For instance, the upload
    test will fail if the create test wasn't run or failed.
    """

    dt_file = "/usr/local/tmp/dtut_bundle.tgz"
    filename = os.path.basename(dt_file)
    local_file = os.path.join(UPLOAD_PATH, filename)

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
        # Cleanup by removing the local file
        if os.path.exists(cls.local_file):
            os.remove(cls.local_file)


    @mark.p1
    def test_01_create_bundle(self):
        self.defaultLibrary.apiLowLevelApis.hostUtils.enable_debug_mode(self.tb.dut1.name)
        assert self.suiteUdks.create_bundle(self.tb.dut1.name, self.dt_file)

    @mark.p1
    def test_02_upload_bundle(self, dt_cl_test_env):
        assert self.suiteUdks.upload_bundle(self.tb.dut1.name, dt_cl_test_env.get_dflt_mgmt_vrid(),
                                            self.local_file, self.filename, self.dt_file)

    @mark.p1
    def test_03_download_bundle(self, dt_cl_test_env):
        assert self.suiteUdks.download_bundle(self.tb.dut1.name,
                                              dt_cl_test_env.get_dflt_mgmt_vrid(), self.local_file,
                                              self.dt_file)

    @mark.p1
    def test_04_apply_bundle(self):
        assert self.suiteUdks.apply_bundle(self.tb.dut1.name, self.dt_file)
