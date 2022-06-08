"""
Digital Twin - conftest.py
"""

# pylint: disable=import-error
import sys
import os
import logging
import time
import random
import subprocess
import uuid
import yaml
import pytest
from ..Resources import shared

DFLT_HTTP_PORT = "8181"

CONFIGS_HELP = """Comma-separated list of configurations to test:
               all         - Run all the different test configurations
               standard    - Run the standard, pre-created YAML configs (default)
               <yaml_file> - Specify a single yaml file from the dtyaml directory
               <sys_type>  - Specify a single sys_type
               sys_sample  - Create a simple YAML file for one of each system type
"""
HELP_FMT = "               {0:<11} - Create a simple YAML file for each {0} {1} type\n"
for plat in shared.PLATFORMS:
    CONFIGS_HELP += HELP_FMT.format("sys_" + plat["family"], "system")

for plat in shared.PLATFORMS:
    if plat.get("vims") and len(plat["vims"]) > 0:
        CONFIGS_HELP += HELP_FMT.format("vim_" + plat["family"], "VIM")

STACKING_HELP = """Include or exclude configurations that use stacking:
               include     - Include stacking test configurations (default)
               exclude     - Exclude any stacking test configurations
               only        - Only include stacking tests configurations
"""

def pytest_addoption(parser):
    parser.addoption("--configs", action="append", default=[], help=CONFIGS_HELP)
    parser.addoption("--docker-image", action="store",
                     default="engartifacts1.extremenetworks.com:8099/dtec/dtec:latest",
                     help="Downloadable DTEC GNS3 Docker container")
    parser.addoption("--http-ip", action="store",
                     help="Define the HTTP server IP address to access DT YAML files")
    parser.addoption("--http-port", action="store", default=DFLT_HTTP_PORT,
                     help="Define the HTTP server port to access DT YAML files")
    parser.addoption("--max-instances", action="store",
                     help="Limit the number of DT instances per test")
    parser.addoption("--no-dt-mgmt", action="store_true", help="Don't use DT Mgmt Interface")
    parser.addoption("--nos-image", action="store", required=True,
                     help="Full path of NOS QCOW2 image file (mandatory)")
    parser.addoption("--stacking", action="store", default="include", help=STACKING_HELP)


def handle_misc_cli_options(config):
    """Parse any miscellaneous CLI options.  Note that logging doesn't work in here"""

    nos_image = config.getoption("nos_image")
    docker_image = config.getoption("docker_image")

    pytest.USE_DT_MGMT = not config.getoption("no_dt_mgmt")

    # Generate a random UUID for the instance name
    inst_name = str(uuid.uuid4())
    pytest.gns3_inst = shared.Gns3(nos_image, inst_name, docker_image,
                                   use_dt_mgmt=pytest.use_dt_mgmt)

    # If http_ip is None, server will auto-bind to all addresses, so we need
    # to preserve that in the "global" configuration...
    pytest.http_ip = config.getoption("http_ip")
    pytest.http_port = config.getoption("http_port") or pytest.http_port

    # ...but here, where we define the HTTP server URL, we need a real value
    http_ip = pytest.http_ip or shared.get_my_ip_address()
    pytest.cfg_urls = f"http://{http_ip}:{pytest.http_port}/"


def handle_generic_tests_cli_options(config): # pylint: disable=too-many-branches
    """Parse custom CLI options for Generic Tests.  Note that logging doesn't work in here"""

    # This will hold a list of DtTestEnv instances to be used
    params = []

    # Handle "configs" option
    options = []
    for opt in config.getoption("configs") or ["standard"]:
        options += opt.split(",")

    print("options = {}".format(str(options)))

    # "configs" - handle hard-coded options pecified
    if any(p in options for p in ["standard", "all"]):
        params += shared.VM_CFGS["standard"]
    if any(p in options for p in ["sys_sample"]):
        params += shared.VM_CFGS["sys_sample"]

    # "configs" - handle any sys/family types options specified
    families = [plat["family"] for plat in shared.PLATFORMS]
    for fam in families:
        if any(opt in options for opt in ["sys_"+fam, "all"]):
            params += shared.VM_CFGS["sys"][fam]

    # "configs" - handle VIM types options specified
    vim_families = [plat["family"] for plat in shared.PLATFORMS
                    if plat.get("vims") and len(plat["vims"]) > 0]
    for fam in vim_families:
        if any(opt in options for opt in ["vim_"+fam, "all"]):
            params += shared.VM_CFGS["vim"][fam]

    # "configs" - handle single yaml file options specified
    for opt in options:
        if opt.endswith(".yaml"):
            for cfg in shared.VM_CFGS["standard"]:
                if cfg.yaml_file == opt:
                    params.append(cfg)

    # "configs" - handle a single sys_type option specified
    for opt in options:
        cfg = shared.get_vm_cfg_if_valid_sys_type(opt)
        if cfg:
            params.append(cfg)
    print("{} number of inital test environments".format(len(params)))

    # Ensure the items in the list are unique (requires Python 3.7+)
    params = list(dict.fromkeys(params))
    print("{} number of test environments after removing duplicates".format(len(params)))

    # Handle "stacking" option
    if config.getoption("stacking") == "exclude":
        params = [elem for elem in params if not elem.uses_stacking()]
    elif config.getoption("stacking") == "only":
        params = [elem for elem in params if elem.uses_stacking()]
    print("{} number of test environments after adjustments for stacking".format(len(params)))

    # Handle "max-instances" option
    if config.getoption("max_instances") is not None:
        max_instances = int(config.getoption("max_instances"))
    else:
        max_instances = None

    if max_instances and max_instances < len(params):
        params = random.sample(params, k=max_instances)
    elif max_instances is not None and not max_instances:
        # max_instances=0 -- Special case for debugging
        print("params = {}".format(str(params)))
        print("User requested no DT instances")
        params = []
    print("{} number of test environments after adjustments for max-instances".format(len(params)))

    print("params = {}".format(str(params)))
    shared.set_generic_test_envs(params)


def pytest_configure(config):
    """Note that logging doesn't work in here"""

    # Init these "globals" here to better define which data is available

    # Instance of Gns3 from shared.py
    pytest.gns3_inst = None
    pytest.cfg_urls = None
    pytest.use_dt_mgmt = True
    pytest.http_ip = None
    pytest.http_port = DFLT_HTTP_PORT

    # Parse custom CLI options
    handle_misc_cli_options(config)
    handle_generic_tests_cli_options(config)


def pytest_generate_tests(metafunc):
    logging.debug("pytest_generate_tests - function=%s", metafunc.function.__name__)

    if metafunc.cls.__name__ == "GenericTests":
        metafunc.parametrize("dte_cl_envs", shared.get_generic_test_envs(), ids=str, scope="class")


###############################################################################
# A note on these fixtures:
# They are broken up into multiple stages to allow for consistent teardown: aka.
# "safe teardowns".  See:
# https://docs.pytest.org/en/latest/how-to/fixtures.html#safe-teardowns
#
# Also, since the fixtures are scoped differently, they can't be easily re-used.
# Something like "invocation-scoped fixtures" is needed.  See:
# https://github.com/pytest-dev/pytest/issues/1681
###############################################################################

class EnvSetupStage1():
    @staticmethod
    def setup(dt_env):
        logging.info("dt_env = %s", dt_env)
        logging.info("DT YAML:\n%s", yaml.safe_dump(dt_env.yaml))
        dt_env.setup()

    @staticmethod
    def teardown(dt_env):
        dt_env.cleanup()

class EnvSetupStage2():
    @staticmethod
    def setup(dt_env):
        pytest.gns3_inst.create_dt_node(dt_env.ram, dt_env.sys_mac, dt_env.yaml_file,
                                        pytest.cfg_urls)

    @staticmethod
    def teardown():
        pytest.gns3_inst.delete_dt_node()

class EnvSetupStage3():
    @staticmethod
    def setup():
        pytest.gns3_inst.setup_dt_node()

    @staticmethod
    def teardown():
        pass

class EnvSetupStage4():
    @staticmethod
    def setup(dt_env):
        logging.info("Sleep %d seconds while system boots", dt_env.get_boot_wait_time())
        time.sleep(dt_env.get_boot_wait_time())

    @staticmethod
    def teardown(dt_env):
        pass

class EnvSetupStage5():
    @staticmethod
    def setup(request):
        try:
            request.cls.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()
        except Exception:
            request.cls.executionHelper.setSetupFailure(True)

    @staticmethod
    def teardown(request):
        request.cls.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()

# DT Env Function-scoped stages/environments
@pytest.fixture(scope="function")
def _dte_fn_stage1(dte_fn_envs):
    dt_env = dte_fn_envs
    EnvSetupStage1.setup(dt_env)
    yield dt_env
    EnvSetupStage1.teardown(dt_env)

@pytest.fixture(scope="function")
def _dte_fn_stage2(_dte_fn_stage1):
    dt_env = _dte_fn_stage1
    EnvSetupStage2.setup(dt_env)
    yield dt_env
    EnvSetupStage2.teardown()

@pytest.fixture(scope="function")
def _dte_fn_stage3(_dte_fn_stage2):
    dt_env = _dte_fn_stage2
    EnvSetupStage3.setup()
    yield dt_env
    EnvSetupStage3.teardown()

@pytest.fixture(scope="function")
def _dte_fn_stage4(_dte_fn_stage3):
    dt_env = _dte_fn_stage3
    EnvSetupStage4.setup(dt_env)
    yield dt_env
    EnvSetupStage4.teardown(dt_env)

@pytest.fixture(scope="function")
def dt_fn_test_env(request, _dte_fn_stage4):
    dt_env = _dte_fn_stage4
    EnvSetupStage5.setup(request)
    yield dt_env
    EnvSetupStage5.teardown(request)


# DT Env Class-scoped stages/environments
@pytest.fixture(scope="class")
def _dte_cl_stage1(dte_cl_envs):
    dt_env = dte_cl_envs
    EnvSetupStage1.setup(dt_env)
    yield dt_env
    EnvSetupStage1.teardown(dt_env)

@pytest.fixture(scope="class")
def _dte_cl_stage2(_dte_cl_stage1):
    dt_env = _dte_cl_stage1
    EnvSetupStage2.setup(dt_env)
    yield dt_env
    EnvSetupStage2.teardown()

@pytest.fixture(scope="class")
def _dte_cl_stage3(_dte_cl_stage2):
    dt_env = _dte_cl_stage2
    EnvSetupStage3.setup()
    yield dt_env
    EnvSetupStage3.teardown()

@pytest.fixture(scope="class")
def _dte_cl_stage4(_dte_cl_stage3):
    dt_env = _dte_cl_stage3
    EnvSetupStage4.setup(dt_env)
    yield dt_env
    EnvSetupStage4.teardown(dt_env)

@pytest.fixture(scope="class")
def dt_cl_test_env(request, _dte_cl_stage4):
    dt_env = _dte_cl_stage4
    EnvSetupStage5.setup(request)
    yield dt_env
    EnvSetupStage5.teardown(request)


@pytest.fixture(scope="session")
def _sst_stage1():
    try:
        pytest.gns3_inst.start_instance()
    except Exception:
        try:
            pytest.gns3_inst.stop_instance()
        except Exception:
            pass # Best effort to stop any running container
        err_msg = "Exception starting GNS3 instance"
        logging.exception(err_msg)
        pytest.exit(err_msg)
    except BaseException as exc:
        try:
            pytest.gns3_inst.stop_instance()
        except Exception:
            pass # Best effort to stop any running container
        raise exc
    yield
    pytest.gns3_inst.stop_instance()

@pytest.fixture(scope="session")
def _sst_stage2(_sst_stage1):
    try:
        pytest.gns3_inst.create_common_infrastructure()
    except Exception:
        err_msg = "Exception creating common GNS3 infrastructure"
        logging.exception(err_msg)
        pytest.exit(err_msg)
    yield
    pytest.gns3_inst.delete_common_infrastructure()

@pytest.fixture(scope="session", autouse=True)
def session_setup_and_teardown(_sst_stage2):
    try:
        pytest.gns3_inst.copy_nos_image()
    except Exception:
        err_msg = "Exception copying NOS image to GNS3 container"
        logging.exception(err_msg)
        pytest.exit(err_msg)
    yield
    # This is done as a best-effort...just-in-case cleanup
    if os.path.exists(shared.DT_YAML_FILE_PATH):
        os.remove(shared.DT_YAML_FILE_PATH)


@pytest.fixture(scope="session", autouse=True)
def start_http_server(request):
    """Start an http server to server the YAML files to DTs when they boot"""
    cmd = [sys.executable, "-m", "http.server", pytest.http_port, "--directory", shared.DT_YAML_DIR]
    if pytest.http_ip:
        cmd += ["--bind", pytest.http_ip]
    proc = subprocess.Popen(cmd) # pylint: disable=consider-using-with
    request.addfinalizer(proc.kill)
