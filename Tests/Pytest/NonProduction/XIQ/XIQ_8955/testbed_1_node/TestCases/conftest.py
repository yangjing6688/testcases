import pytest
import os
import random
import string

from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
    NetworkElementConnectionManager
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from extauto.common.Utils import Utils


@pytest.fixture(scope="session", autouse=True)
def onboard_location():
    pool = list(string.ascii_letters) + list(string.digits)
    return f"Salem_{''.join(random.sample(pool, k=4))},Northeastern_{''.join(random.sample(pool, k=4))}" \
           f",Floor_{''.join(random.sample(pool, k=4))}"


@pytest.fixture(scope="session", autouse=True)
def setup_switch(onboard_location):
    default_library = DefaultLibrary()
    network_manager = NetworkElementConnectionManager()
    tb = PytestConfigHelper(config)
    utils = Utils()
    xiq = XiqLibrary()

    config['${TEST_NAME}'] = "setup_XIQ_8955"
    config['${OUTPUT DIR}'] = os.getcwd()

    if tb.config.netelem1.cli_type.upper() != "EXOS":
        assert -1, "Other platform than EXOS is not yet supported"

    if tb.config.netelem1.platform.upper() == "STACK":
        assert -1, "Stacks are not yet supported"

    dut = tb.dut1
    assert dut is not None, "Failed to get the dut from tb"

    dut.location = onboard_location
    create_first_org = None

    try:
        network_manager.connect_to_network_element_name(dut.name)

        assert xiq.login.login_user(config['tenant_username'], config['tenant_password'], url=config['test_url']) \
               == 1, "Failed to login the user"

        assert xiq.xflowsmanageLocation.create_location_building_floor(*onboard_location.split(",")) == 1, \
            "Failed to create location"

        global_settings = xiq.xflowsglobalsettingsGlobalSetting
        assert global_settings.change_exos_device_management_settings(option="disable",
                                                                      platform=tb.config.netelem1.cli_type) == 1, \
            "Failed to change exos device management settings"

        xiq.login.logout_user()
        xiq.login.quit_browser()
        default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()

        yield dut

    finally:
        config['${TEST_NAME}'] = 'teardown_XIQ_8955'

        try:
            xiq.login.login_user(config['tenant_username'], config['tenant_password'], url=config['test_url'])
            xiq.xflowsmanageLocation.delete_location_building_floor(*onboard_location.split(","))
        except Exception as exc:
            utils.print_info(exc)
        finally:
            xiq.login.logout_user()
            xiq.login.quit_browser()
            default_library.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()
