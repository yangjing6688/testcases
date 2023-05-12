import json
import threading
import time
import os
import re
import string
import random
import subprocess
import traceback
import pytest
import platform
import yaml
import sys
import pexpect
import imp
import operator

from distutils.version import LooseVersion
from pytest import FixtureRequest
from pexpect.pxssh import pxssh
from _pytest import mark, fixtures
from collections import defaultdict
from pytest_testconfig import config
from contextlib import contextmanager
from typing import List, Dict, DefaultDict, Callable, Tuple, Iterator, Protocol, NewType, Union, Any
from pathlib import Path
from itertools import permutations
from collections.abc import MutableMapping
from selenium.webdriver.common.action_chains import ActionChains
from pytest_testconfig import config as pytest_config

from ExtremeAutomation.Library.Utils.Singleton import Singleton
from ExtremeAutomation.Library.Logger.PytestLogger import PytestLogger
from ExtremeAutomation.Library.Logger.Colors import Colors
from ExtremeAutomation.Keywords.NetworkElementKeywords.StaticKeywords.NetworkElementResetDeviceUtilsKeywords import NetworkElementResetDeviceUtilsKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import NetworkElementConnectionManager
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementListUtils import NetworkElementListUtils
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementCliSend import NetworkElementCliSend
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.Udks import Udks
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.EndSystemUtils import EndSystemUtils
from ExtremeAutomation.Imports.LowLevelApis import LowLevelApis
from ExtremeAutomation.Imports.VirtualMachineUtils import VirtualMachineUtils
from ExtremeAutomation.Imports.NetElementUtils import NetElementUtils
from ExtremeAutomation.Imports.LowLevelTrafficApis import LowLevelTrafficApis
from ExtremeAutomation.Imports.CommonObjectUtils import CommonObjectUtils
from extauto.common.Screen import Screen
from extauto.common.Rest import Rest
from extauto.common.WebElementHandler import WebElementHandler
from extauto.common.Tshark import Tshark
from extauto.common.WebElementController import WebElementController
from extauto.common.Utils import Utils
from extauto.common.CloudDriver import CloudDriver
from extauto.common.AutoActions import AutoActions
from extauto.common.Cli import Cli
from extauto.xiq.elements.ClientWebElements import ClientWebElements
from extauto.xiq.elements.Network360MonitorElements import Network360MonitorElements
from extauto.xiq.flows.common.Navigator import Navigator


Node = NewType("Node", Dict[str, Union[str, Dict[str, str]]])
Options = NewType("Options", Dict[str, Union[str, Dict[str, str]]])
PolicyConfig = NewType("PolicyConfig", DefaultDict[str, Dict[str, str]])
NodesData = NewType("NodesData", Dict[str, Dict[str, Any]])
TestCaseMarker = NewType("TestCaseMarker", str)
PriorityMarker = NewType("PriorityMarker", str)
TestbedMarker = NewType("TestbedMarker", str)
logger_obj: PytestLogger = PytestLogger()


class EnterSwitchCli(Protocol):
    def __call__(
        self,
        dut: Node
        ) -> Iterator[NetworkElementCliSend]: ...


class OpenSpawn(Protocol):
    def __call__(
        self, 
        dut: Node
        ) -> Iterator[pxssh]: ...


class OpenPxsshSpawn(Protocol):
    def __call__(
        self, 
        dut: Node,
        debug_mode: bool,
        disable_strict_host_key_checking: bool,
        **kwargs: Dict
        ) -> Iterator[pxssh]: ...


class LoginXiq(Protocol):
    def __call__(
        self,
        username: str,
        password: str,
        url: str,
        capture_version: bool,
        code: str,
        incognito_mode: str
        ) -> Iterator[XiqLibrary]: ...


class BounceIqagent(Protocol):
    def __call__(
        self,
        dut: Node,
        xiq: XiqLibrary,
        wait: bool
        ) -> None: ...


class CloseConnection(Protocol):
    def __call__(
        self,
        dut: Node
        ) -> None: ...


class CreateLocation(Protocol):
    def __call__(
        self,
        xiq: XiqLibrary,
        location: str
        ) -> None: ...


class ConfigureIqAgent(Protocol):
    def __call__(
        self,
        duts: List[Node], 
        ipaddress: str
        ) -> None: ...


class UnconfigureIqAgent(Protocol):
    def __call__(
        self,
        duts: List[Node]
        ) -> None: ...


class CheckDevicesAreReachable(Protocol):
    def __call__(
        self, 
        duts: List[Node],
        retries: int,
        step: int
        ) -> None: ...


class CheckDevicesAreOnboarded(Protocol):
    def __call__(
        self,
        xiq: XiqLibrary,
        node_list: List[Node],
        timeout: int
        ) -> None: ...


class Cleanup(Protocol):
    def __call__(
        self, 
        duts: List[Node], 
        location: str, 
        network_policies: List[str],
        templates_switch: List[str],
        ) -> None: ...


class CheckVim(Protocol):
    def __call__(
        self,
        xiq: XiqLibrary,
        ) -> None: ...


class CheckPoe(Protocol):
    def __call__(
        self,
    ) -> None: ...


class ConfigureNetworkPolicies(Protocol):
    def __call__(
        self,
        xiq: XiqLibrary,
        dut_config: PolicyConfig
        ) -> None: ...


class UpdateDevices(Protocol):
    def __call__(
        self,
        xiq: XiqLibrary,
        duts: List[Node]
        ) -> None: ...


class Onboarding(Protocol):
    def __call__(
        self,
        xiq: XiqLibrary,
        duts: List[Node]
        ) -> None: ...


class PreOnboardingConfiguration(Protocol):
    def __call__(
        self,
        xiq: XiqLibrary,
        duts: List[Node]
        ) -> None: ...


class PostOnboardingConfiguration(Protocol):
    def __call__(
        self,
        xiq: XiqLibrary,
        duts: List[Node]
        ) -> None: ...


class PreOnboardingVerifications(Protocol):
    def __call__(
    self,
    xiq: XiqLibrary,
    duts: List[Node]
    ) -> None: ...


class PostOnboardingVerifications(Protocol):
    def __call__(
        self,
        xiq: XiqLibrary,
        duts: List[Node]
        ) -> None: ...

class OnboardingFailure(Protocol):
    def __call__(
        self,
        xiq: XiqLibrary,
        duts: List[Node]
        ) -> None: ...


class OnboardingSucceeded(Protocol):
    def __call__(
        self,
        xiq: XiqLibrary,
        duts: List[Node]
        ) -> None: ...


class ResetSwitch(Protocol):
    def __call__(
        self,
        ) -> None: ... 


class SetHostname(Protocol):
    def __call__(
        self,
        duts: List[Node]
        ) -> None: ... 


class DevicesConfiguration(Protocol):
    def __call__(
        self,
        ) -> None: ...


class DevicesCleanup(Protocol):
    def __call__(
        self,
        ) -> None: ...


class DevicesVerifications(Protocol):
    def __call__(
        self,
        ) -> None: ...


class AccountConfiguration(Protocol):
    def __call__(
        self,
        xiq: XiqLibrary,
        ) -> None: ...


class DumpSwitchLogs(Protocol):
    def __call__(
        self,
        duts: List[Node]
        ) -> None: ...


class RebootDevice(Protocol):
    def __call__(
        self,
        duts: List[Node]
        ) -> None: ...


class RebootStackUnit(Protocol):
    def __call__(
        self,
        dut: Node,
        slot: int,
        save_config: str
        ) -> None: ...


class DeactivateXiqLibrary(Protocol):
    def __call__(
        self,
        xiq: XiqLibrary
        ) -> None: ...


class GetXiqLibrary(Protocol):
    def __call__(
        self,
        username: str,
        password: str,
        url: str,
        capture_version: bool,
        code: str,
        incognito_mode: str
        ) -> XiqLibrary: ...


class GetStackSlots(Protocol):
    def __call__(
        self,
        dut: Node
        ) -> Dict[str, Dict[str, str]]: ...


class ModifyStackingNode(Protocol):
    def __call__(
        self, 
        dut: Node,
        node_mac_address: str, 
        op: str
        ) -> None: ...


class SetLldp(Protocol):
    def __call__(
        self, 
        dut: Node, 
        ports: List[str],
        action: str
        ) -> None: ...


class ChangeDeviceManagementSettings(Protocol):
    def __call__(
        self,
        xiq: XiqLibrary,
        option: str,
        retries: int=5,
        step: int=5
        ) -> None: ...


class ClearTrafficCounters(Protocol):
    def __call__(
        self,
        dut: Node,
        *ports: List[str]
        ) -> None: ...


valid_test_markers: List[TestCaseMarker] = [
    "tcxm",
    "tccs",
    "xim_tcxm"
]


valid_priority_markers: List[PriorityMarker] = [
    "p0",
    "p1",
    "p2",
    "p3",
    "p4",
    "p5"
]


valid_testbed_markers: List[TestbedMarker] = [
    "testbed_1_node",
    "testbed_2_node",
    "testbed_stack",
    "testbed_none"
]


@pytest.fixture(scope="session")
def debug(logger: PytestLogger) -> Callable:
    def debug_func(func):
        def wrapped_func(*args, **kwargs):
            start_time = time.time()
            try:
                logger.step(f"Calling '{func.__name__}' function with args='{args}' and kwargs='{kwargs}'")
                result = func(*args, **kwargs)
            except Exception as exc:
                logger.error(
                    f"Failed during '{func.__name__}' function call with args='{args}' and kwargs='{kwargs}' "
                    f"after {int(time.time()-start_time)} seconds: {repr(exc)}")
                raise exc
            else:
                logger.info(
                    f"Call for '{func.__name__}' with args='{args}' and kwargs='{kwargs}' ended "
                    f"after {int(time.time()-start_time)} seconds")
                return result
        return wrapped_func
    return debug_func


def pytest_cmdline_preparse(config, args):
    args.extend([os.path.join(os.path.dirname(__file__), "conftest.py"), "-vv", "--tb=long"])


def get_test_marker(
        item: pytest.Function
) -> List[TestCaseMarker]:  
    return [m.name for m in item.own_markers if any(re.search(rf"^{test_marker}_", m.name) for test_marker in valid_test_markers)]


def log_git():
    
    repos = ['extreme_automation_framework', 'extreme_automation_tests']
    
    try:
        from git import Repo
        from git.exc import InvalidGitRepositoryError, NoSuchPathError
    except ImportError:
        logger_obj.warning("The 'GitPython' module is not installed.")
        return
    
    for repo_name in repos:
        for path in sys.path:
            if re.search(rf"(.*/{repo_name})$", path):
                try:
                    git_repo = Repo(path)
                except (InvalidGitRepositoryError, NoSuchPathError):
                    pass
                else:
                    try:
                        logger_obj.step(f"{repo_name} git dir: '{git_repo.git_dir}'.")
                        logger_obj.step(f"{repo_name} working tree dir: '{git_repo.working_tree_dir}'.")
                        logger_obj.step(f"{repo_name} feature branch: '{git_repo.active_branch.name}'.")
                        logger_obj.step(f"{repo_name} HEAD commit: '{git_repo.head.commit}'.")
                    except:
                        # TypeError: HEAD is a detached symbolic reference as it points to 'e893b741b753c3032f170500e19006c4cdbf6bde'
                        # FIX XAT-260
                        pass
                    break


def get_priority_marker(
        item: pytest.Function
) -> List[PriorityMarker]:
    return [m.name for m in item.own_markers if m.name in valid_priority_markers]


def get_testbed_markers(
        item: pytest.Function
) -> List[TestbedMarker]:
    return [m.name for m in item.own_markers if m.name in valid_testbed_markers]


def get_item_markers(
        item: pytest.Function
) -> List[mark.structures.Mark]:
    return item.own_markers


def get_node_markers(
        item: pytest.Function
) -> List[mark.structures.Mark]:
    return list(item.iter_markers())


def get_item_dependson_markers(
        item: pytest.Function
) -> List[mark.structures.Mark]:
    return [marker for marker in get_item_markers(item) if marker.name == "dependson"]


def get_node_dependson_markers(
     item: pytest.Function
) -> List[mark.structures.Mark]:
    return [marker for marker in get_node_markers(item) if marker.name == "dependson"]


def is_onboarding_test(
    item: pytest.Function
) -> bool:
    return get_test_marker(item)[0] == pytest.onboarding_test_name


def is_onboarding_cleanup_test(
    item: pytest.Function
) -> bool:
    return get_test_marker(item)[0] == pytest.onboarding_cleanup_test_name


def pytest_configure(config):
    pytest.runlist_name: str = ""
    pytest.runlist_path: str = "default"
    pytest.runlist_filtering_markers: str = ""
    pytest.suitemaps_name: List[str] = []
    pytest.runlist_tests: List[TestCaseMarker] = []
    pytest.suitemap_tests: Dict[str, Union[str, Dict[str, str]]] = {}
    pytest.suitemap_data: Dict[str, Union[str, Dict[str, str]]] = {}
    pytest.onboarding_options: Options = {}
    pytest.run_options: Options = {}
    pytest.onboard_1_node: bool = False 
    pytest.onboard_2_node: bool = False 
    pytest.onboard_stack: bool = False 
    pytest.onboard_none: bool = True
    pytest.all_nodes: List[Node] = []
    pytest.standalone_nodes: List[Node] = []
    pytest.stack_nodes: List[Node] = []
    pytest.config_helper: PytestConfigHelper = PytestConfigHelper(pytest_config)
    pytest.onboarding_test_name: str = "tcxm_xiq_onboarding"
    pytest.onboarding_cleanup_test_name: str = "tcxm_xiq_onboarding_cleanup"
    pytest.created_onboarding_locations: List[str] = []
    pytest.created_network_policies: List[str] = []
    pytest.created_switch_templates: List[str] = []
    pytest.items: List[pytest.Function] = []
    pytest.testbed_one_node_items: List[pytest.Function] = []
    pytest.testbed_two_node_items: List[pytest.Function] = []
    pytest.testbed_stack_items: List[pytest.Function] = []
    pytest.xiq_version: str = None
    pytest.data: Dict[str, str] = {}
    pytest.onboarding_config: str = "onboarding.config.json"


def log_features():

    root = Path(os.path.join(imp.find_module("extreme_automation_tests")[1], "data"))
    suitemaps: List[str] = [str(path) for path in root.rglob("suitemap_*.yaml")]
    suitemaps.sort()

    if suitemaps:
        
        data: Dict[str, Dict[str, str]] = {}
        max_len_values = 0
        automated_tests = 0
        story_tests_mapping: Dict[str, int] = {}
        story_directory_mapping: DefaultDict[str, List[str]] = defaultdict(lambda: [])
        
        for index, suitemap_path in enumerate(suitemaps):

            suitemap_file = re.search(r"suitemap_.*\.yaml", suitemap_path).group(0)
            
            try:
                with open(suitemap_path, "r") as content:
                    output_suitemap = yaml.safe_load(content.read())
            except:
                continue

            if not (feature_name := output_suitemap.get("data", {}).get("feature_name")):
                logger_obj.warning(f"{suitemap_file} suitemap file won't be parsed at it does not have the 'feature_name' key.")
                continue

            feature_jira_link = output_suitemap.get("data", {}).get("feature_jira_link")
            feature_qtest_link = output_suitemap.get("data", {}).get("feature_qtest_link")

            for directory in root.iterdir():
                if path_obj := Path(suitemap_path):
                    if directory in path_obj.parents:
                        story_directory_mapping[directory.name].append(feature_name)
                        break
    
            tests: List[TestCaseMarker] = []

            for k, v in output_suitemap.get("tests", {}).items():
                if tc := v.get("tc"):
                    tests.append(tc)
                else:
                    tests.extend([x.get("tc") for x in v.get("tests", [])])

            feature_tests = [test for test in tests if test not in [pytest.onboarding_test_name, pytest.onboarding_cleanup_test_name]]
            temp_lines: List[str] = []
            automated_tests += len(feature_tests)

            temp_data = {
                "Feature Index": index + 1,
                "Feature Name": feature_name,
                "Suitemap File": suitemap_file,
                "Suitemap Path": re.search("data/.*$", suitemap_path).group(0),
                "Automated Tests": str(len(feature_tests)),
                "Jira Link": feature_jira_link,
                "qTest Link": feature_qtest_link,
                "Data Directory": directory.name
            }

            story_tests_mapping[feature_name] = len(feature_tests)

            data[suitemap_path] = temp_data
            max_len_fields = max(len(str(k)) for k in temp_data)
            temp_max_len_values = max(len(str(v)) for v in temp_data.values())
            max_len_values = temp_max_len_values if temp_max_len_values > max_len_values else max_len_values

        temp_lines.append("\n+" + "-" * (max_len_fields + max_len_values + 4) + "+")
        for _, values in data.items():
            for k, v in values.items():
                if v:
                    temp_lines.append(f"| {k:<{max_len_fields}}: {v:<{max_len_values}} |")
            temp_lines.append("+" + "-" * (max_len_fields + max_len_values + 4) + "+")

        logger_obj.info("\n".join(temp_lines))
        logger_obj.info(f"Found {len(suitemaps)} automated features in the data/ directory.")
        logger_obj.info(f"Found {automated_tests} automated tests definitions in the data/ directory.")

        for directory, features in story_directory_mapping.items():
            if features:
                logger_obj.info(f"Found {len(features)} automated stories in the '{directory}' directory: '" + ", '".join(features) + "'.")
                logger_obj.info(f"Found {sum(v for k, v in story_tests_mapping.items() if k in features)} automated test cases in the '{directory}' directory.")
            else:
                logger_obj.info(f"Did not find any story in the '{directory}' directory.")

        try:
            logger_obj.info(f"The average number of automated test cases per story is {int(sum(story_tests_mapping.values())/len(story_tests_mapping))}.")
            logger_obj.info(
                f"The highest number of automated test cases per story is {max(story_tests_mapping.values())} ('" + \
                "', '".join(k for k, v in story_tests_mapping.items() if v == max(story_tests_mapping.values())) + "' feature(s)).")
            logger_obj.info(
                f"The least number of automated test cases per story is {min(story_tests_mapping.values())} ('" + \
                "', '".join(k for k, v in story_tests_mapping.items() if v == min(story_tests_mapping.values())) + "' feature(s)).")
        except:
            pass
    else:
        logger_obj.info("Did not find any suitemap file in the data/ directory.")


def pytest_collection_modifyitems(session, items):

    if pytest.runlist_path != "default":
        
        log_git()
        log_features()

        logger_obj.info(f"Collected {len(items)} test functions from given test directory path(s).")
        logger_obj.info(f"Current runlist ('{pytest.runlist_name}') is located in this yaml file: '{pytest.runlist_path}'.")
        logger_obj.info(f"Found {len(pytest.runlist_tests)} tests in given runlist: " + "'" + "', '".join(pytest.runlist_tests) + "'.")
                
        suitemap_tcs: List[TestCaseMarker] = []
        
        for _, test_info in pytest.suitemap_tests.items():
            if tc := test_info.get("tc"):
                suitemap_tcs.append(tc)
            elif tcs := test_info.get("tests"):
                for tc in tcs:
                    suitemap_tcs.append(tc['tc'])

        logger_obj.info(f"Found {len(suitemap_tcs)} test(s) defined in given suitemap yaml files: " + "'" + "', '".join(suitemap_tcs) + "'.")
        
        if tcs_found_in_runlist_but_not_in_suitemap := list(set(pytest.runlist_tests).difference(set(suitemap_tcs))):
            logger_obj.warning(
                f"Found {len(tcs_found_in_runlist_but_not_in_suitemap)} test case(s) in the runlist yaml file"
                f" that do not have definitions in the given suitemap yaml files: " + "'" + "', '".join(tcs_found_in_runlist_but_not_in_suitemap) + "'.")
        
        if tcs_found_in_suitemap_but_not_in_runlist := list(set(suitemap_tcs).difference(set(pytest.runlist_tests))):
            logger_obj.info(
                f"Found {len(tcs_found_in_suitemap_but_not_in_runlist)} test case(s) defined in the suitemap yaml "
                f"that are not used in the runlist yaml file: " + "'" + "', '".join(tcs_found_in_suitemap_but_not_in_runlist) + "'.")
        
        for item in items:
            
            if cls_markers := getattr(item.cls, "pytestmark", None):
                
                item_testbed_marker = [m for m in item.own_markers if m.name in valid_testbed_markers]
                cls_testbed_marker = [m for m in cls_markers if m.name in valid_testbed_markers]
                
                for cls_marker in cls_testbed_marker:
                    if not any(cls_marker.name == m.name for m in item_testbed_marker):
                        item.add_marker(
                            getattr(pytest.mark, cls_marker.name)
                        )

        for item in items:
            
            if callspec := getattr(item, "callspec", None):
                test_data = callspec.params["test_data"]
            else:
                test_data = pytest.suitemap_tests[f"{item.cls.__name__}::{item.originalname}"]
            
            try:
                test_marker_from_test_data = test_data["tc"]
            except KeyError:
                logger_obj.fail(
                    "Make sure the tests that use test parameterization use the 'test_data' fixture."
                    f"\nFailed at function '{item.nodeid}'.")

            tc_markers = get_test_marker(item)
            
            for marker in tc_markers:
                if marker != test_marker_from_test_data:
                    [marker_obj] = [mk for mk in item.own_markers if mk.name == marker]
                    item.own_markers.pop(item.own_markers.index(marker_obj))

            if re.search(r"(.*)_rerun_\d+$", test_marker_from_test_data):
                item.add_marker(
                    getattr(pytest.mark, test_marker_from_test_data))

        collected_items: List[pytest.Function] = []
            
        for item in items:
            if pytest.onboarding_test_name in [m.name for m in item.own_markers]:
                if not [it for it in collected_items if pytest.onboarding_test_name in [m.name for m in it.own_markers]]:
                    collected_items.append(item)
            elif pytest.onboarding_cleanup_test_name in [m.name for m in item.own_markers]:
                if not [it for it in collected_items if pytest.onboarding_cleanup_test_name in [m.name for m in it.own_markers]]:
                    collected_items.append(item)
            else:
                collected_items.append(item)

        for item in collected_items:
            logger_obj.info(f"Collected: '{item.nodeid}'.")

        [item_onboarding] = [
            it for it in collected_items if pytest.onboarding_test_name in [m.name for m in it.own_markers]]
        [item_onboarding_cleanup] = [
            it for it in collected_items if pytest.onboarding_cleanup_test_name in [m.name for m in it.own_markers]]
        
        collected_items.remove(item_onboarding)
        collected_items.remove(item_onboarding_cleanup)
        
        pytest.config_helper = PytestConfigHelper(config)
        pytest.all_nodes = list(filter(lambda d: d is not None, [getattr(pytest.config_helper, f"dut{i}", None) for i in range(1, 10)]))

        logger_obj.step("Check the capabilities of the testbed.")
        pytest.standalone_nodes = [node for node in pytest.all_nodes if node.get("platform", "").upper() != "STACK"]
        logger_obj.info(f"Found {len(pytest.standalone_nodes)} standalone node(s).")

        pytest.stack_nodes = [node for node in pytest.all_nodes if node not in pytest.standalone_nodes]
        logger_obj.info(f"Found {len(pytest.stack_nodes)} stack node(s).")

        temp_items: List[pytest.Function] = collected_items[:]

        testbed_item_mapping: Dict[str, List[pytest.Function]] = {}
        
        for testbed_marker in valid_testbed_markers:
            testbed_items = list(filter(lambda item: testbed_marker in [marker.name for marker in item.own_markers], items))
            logger_obj.info(f"Collected {len(testbed_items)} {testbed_marker} item(s).")
            testbed_item_mapping[testbed_marker] = testbed_items

        items_without_testbed_marker = [
            item for item in collected_items if not any([testbed_marker in [marker.name for marker in item.own_markers]
                                                         for testbed_marker in valid_testbed_markers])]
        if items_without_testbed_marker:
            logger_obj.info(
                f"Collected {len(items_without_testbed_marker)} item(s) that do not have a valid testbed marker ({valid_testbed_markers}).")

        pytest.onboard_stack = len(pytest.stack_nodes) >= 1
        pytest.onboard_2_node = len(pytest.standalone_nodes) > 1
        pytest.onboard_1_node = len(pytest.standalone_nodes) >= 1
        
        if not pytest.onboard_stack:
            logger_obj.warning(
                "There is no stack device in the provided yaml file. The test cases marked only with the 'testbed_stack' marker will be unselected.")

        if not pytest.onboard_2_node:
            logger_obj.warning(
                "There are not enough standalone devices in the provided yaml file. The test cases marked only with the 'testbed_2_node' marker will be unselected.")

        if not pytest.onboard_1_node:
            logger_obj.warning(
                "There is no standalone device in the provided yaml file. The test cases marked only with the 'testbed_1_node' marker will be unselected.")

        if items_without_testbed_marker:
            logger_obj.warning(
                f"{len(items_without_testbed_marker)} item(s) that do not have a valid testbed marker will be unselected.")
    
        filtered_items: List[pytest.Function] = []
        
        # keep the test cases that use at least one valid testbed marker
        
        for item in temp_items:
            testbed_markers = get_testbed_markers(item)
            if any([f"testbed_{node}" in testbed_markers and getattr(pytest, f"onboard_{node}") for node in [tb_marker.split("testbed_")[1] for tb_marker in valid_testbed_markers]]):
                filtered_items.append(item)
                
        temp_items = filtered_items[:]

        for item in collected_items:
            if item not in temp_items:
                logger_obj.info(
                    f"Unselected: '{item.nodeid}' (markers: '{[m.name for m in item.own_markers]}').")
        
        item_test_marker_mapping: DefaultDict[str, List[str]] = defaultdict(lambda: [])
        test_marker_item_mapping: DefaultDict[pytest.Function, List[str]] = defaultdict(lambda: [])
        items_without_valid_test_markers: List[str] = []

        test_codes: List[TestCaseMarker]
        test_code: TestCaseMarker
        priorities: List[PriorityMarker]
        
        for item in temp_items:
            test_codes = get_test_marker(item)

            if not test_codes:
                items_without_valid_test_markers.append(
                    f"This function does not have a valid test marker: '{item.nodeid}'.")

            for test_code in test_codes:
                item_test_marker_mapping[test_code].append(item.nodeid)
        
            test_marker_item_mapping[item] = test_codes

        if items_without_valid_test_markers:
            error = '\n' + '\n'.join(items_without_valid_test_markers)
            error += f"\nValid test markers should begin with any of these markers - {valid_test_markers}."
            logger_obj.fail(error)

        for test_code, functions in item_test_marker_mapping.items():
            if len(functions) > 1:
                error = f"Test marker '{test_code}' is used as marker for more than one test function:\n" +\
                        "\n".join(functions)
                logger_obj.fail(error)

        for item, test_markers in test_marker_item_mapping.items():
            if len(test_markers) > 1:
                temp_items.pop(temp_items.index(item))
                logger_obj.info(f"Unselected: '{item.nodeid}'.")

        all_tcs: List[TestCaseMarker] = [pytest.onboarding_test_name, pytest.onboarding_cleanup_test_name]
        [all_tcs.append(get_test_marker(item)[0]) for item in temp_items]
        
        found_tcs: List[TestCaseMarker] = []

        test_code: TestCaseMarker

        ordered_items: List[pytest.Function] = []

        if temp_items:
                    
            for item in temp_items:
                
                if cls_markers := getattr(item.cls, "pytestmark", None):
                    
                    item_markers: List[mark.structures.Mark] = get_item_dependson_markers(item)
                    cls_dependson_markers: List[mark.structures.Mark] = [
                        m for m in cls_markers if m.name == "dependson"]

                    for marker in cls_dependson_markers:
                        if not any(marker.name == m.name and marker.args == m.args for m in item_markers):
                            item.add_marker(
                                pytest.mark.dependson(*marker.args)
                            )
                            
                    priority_markers: List[PriorityMarker] = get_priority_marker(item)

                    if not priority_markers:
                        
                        cls_priority_marker: mark.structures.Mark
                        cls_priority_marker = [m for m in cls_markers if m.name in valid_priority_markers]
                        
                        if cls_priority_marker:
                            item.add_marker(
                                getattr(pytest.mark, cls_priority_marker[0].name)
                            )

            priority_item_mapping: DefaultDict[pytest.Function, List[PriorityMarker]] = defaultdict(lambda: [])
            items_without_priority_markers: List[str] = []

            for item in temp_items:
                priorities: List[PriorityMarker] = get_priority_marker(item)

                if not priorities:
                    items_without_priority_markers.append(
                        f"This function does not have a priority marker: '{item.nodeid}'.")

                priority_item_mapping[item] = priorities

            if items_without_priority_markers:
                error = '\n' + '\n'.join(items_without_priority_markers)
                error += f"\nValid test priorities: {valid_priority_markers}."
                logger_obj.fail(error)
                        
            for item, priority in priority_item_mapping.items():
                if len(priority) > 1:
                    error = f"\nThis test function has more than one valid priority marker: " \
                            f"{item.nodeid} (markers: '{priority}')."
                    logger_obj.fail(error)

            temp_items.extend([item_onboarding, item_onboarding_cleanup])
            
            filtered_by_priority_items: List[pytest.Function] = []
            runlist_tests_priority = pytest.run_options.get("priority") or valid_priority_markers
            
            if not all(priority in valid_priority_markers for priority in runlist_tests_priority):
                pytest.fail(
                    f"Not all the priority markers given in the runlist yaml are valid: {runlist_tests_priority}. "
                    f"Please use these priority markers: {valid_priority_markers}."
                )

            if sorted(runlist_tests_priority) != sorted(valid_priority_markers):
                logger_obj.step(
                    f"Filter the items by the list of priorities given in the runlist: {runlist_tests_priority}.")
                
                for item in temp_items:
                
                    test_marker: TestCaseMarker = get_test_marker(item)[0]
                    
                    if is_onboarding_test(item) or is_onboarding_cleanup_test(item):
                        filtered_by_priority_items.append(item)
                        continue
                    
                    priority_marker: PriorityMarker = get_priority_marker(item)[0]

                    if priority_marker in runlist_tests_priority:
                        filtered_by_priority_items.append(item)
                    else:
                        logger_obj.warning(
                            f"'{test_marker}' test case will be unselected because its priority "
                            f"('{priority_marker}') is not selected in the runlist yaml.")

                temp_items[:] = filtered_by_priority_items
            
            if pytest.runlist_filtering_markers:
               
                runlist_filtering_markers = [word.strip() for word in pytest.runlist_filtering_markers.split(",")]
                filtered_by_runlist_markers_items: List[pytest.Function] = []      
               
                logger_obj.info(
                    f"Pytest argument '--runlist-filtering-markers' given. "
                    f"Will filter current selected testcase using these markers: '{pytest.runlist_filtering_markers}'."
                )
                
                for item in temp_items:
                
                    test_marker: TestCaseMarker = get_test_marker(item)[0]
                    
                    if is_onboarding_test(item) or is_onboarding_cleanup_test(item):
                        filtered_by_runlist_markers_items.append(item)
                        continue
                    
                    item_markers = item.own_markers
                    for marker in getattr(item.cls, "pytestmark", []):
                        if not any(marker.name == m.name for m in item_markers):
                            item_markers.append(marker)
                    
                    for marker in item_markers:
                        if any(marker.name.upper() == m.upper() for m in runlist_filtering_markers):
                            filtered_by_runlist_markers_items.append(item)
                            break
                    else:
                        logger_obj.warning(
                            f"'{test_marker}' test will be unselected because it is not marked "
                            f"with any of these CLI given markers: '{pytest.runlist_filtering_markers}'.")
            
                temp_items[:] = filtered_by_runlist_markers_items
                
            for test in pytest.runlist_tests:
                
                test_found_in_suitemap: bool = test in suitemap_tcs
                found_item: pytest.Function = [item for item in temp_items if test == get_test_marker(item)[0]]
                
                if not test_found_in_suitemap:
                    logger_obj.warning(
                        f"'{test}' test is given in runlist but it is not defined in the specified suitemap files.")
                
                if not found_item:
                    logger_obj.warning(
                        f"'{test}' test is given in runlist but it is not found in the collected tests "
                        f"(it might have been removed because of its testbed marker or simply the test"
                        f" is not in the selected tests directory).")

                if test_found_in_suitemap and found_item:
                    ordered_items.append(found_item[0])

            all_tcs = [get_test_marker(item)[0] for item in ordered_items]
            
            for item in ordered_items:
                
                [test_code] = get_test_marker(item)
                
                found_tcs.append(test_code)
                item_markers: List[mark.structures.Mark] = item.own_markers
                
                for marker in item_markers:
                    
                    if marker.name == "dependson":
                        temp_markers: Tuple[str] = marker.args

                        if not temp_markers:
                            logger_obj.warning(
                                f"The dependson marker of '{test_code}' testcase does not have any arguments "
                                f"(test function: '{item.nodeid}'.")
                            
                        for temp_marker in temp_markers:
                            if temp_marker == test_code:
                                logger_obj.warning(
                                    f"'{test_code}' is marked as depending on itself (test function: '{item.nodeid}').")
                                
                            elif (temp_marker not in all_tcs) or (temp_marker not in pytest.runlist_tests):
                                item.add_marker(
                                    pytest.mark.skip(
                                        f"'{test_code}' depends on '{', '.join(temp_markers)}' but '{temp_marker}'"
                                        f" is not in the current list of testcases to be run. The '{test_code}'"
                                        f" test case will be skipped.")
                                )
                                
                            elif temp_marker not in found_tcs:
                                item.add_marker(
                                    pytest.mark.skip(
                                        f"Please modify the order of the test cases. '{test_code}' "
                                        f"depends on '{', '.join(temp_markers)}' but the order is not correct. "
                                        f"'{temp_marker}' should run before '{test_code}'."
                                        f" The '{test_code}' test case will be skipped.")
                                )

            for item in ordered_items:
                logger_obj.info(f"Selected: '{item.nodeid}' "
                                f"(markers: '{[m.name for m in item.own_markers]}').")
            
            if all(
                [
                    item_onboarding in ordered_items,
                    item_onboarding_cleanup in ordered_items,
                    len(ordered_items) == 2
                ]
            ):
                logger_obj.warning(
                    "There are no tests left selected to run for this session besides the onboarding tests.")
            
        else:
            message = "Did not find any test function to run this session."
            logger_obj.warning(message)

        pytest.testbed_one_node_items = list(
            filter(lambda item: "testbed_1_node" in [marker.name for marker in item.own_markers], ordered_items))
        pytest.testbed_two_node_items = list(
            filter(lambda item: "testbed_2_node" in [marker.name for marker in item.own_markers], ordered_items))
        pytest.testbed_stack_items = list(
            filter(lambda item: "testbed_stack" in [marker.name for marker in item.own_markers], ordered_items))
        
        if (not pytest.testbed_two_node_items) and pytest.onboard_2_node:
            logger_obj.info(
                "There are no testbed_two_node items left. Will make sure the second node is not onboarded.")
            pytest.onboard_2_node = False

        if (not pytest.testbed_one_node_items) and pytest.onboard_1_node:
            logger_obj.info(
                "There are no testbed_one_node items left. Will make sure the first node"
                "is not onboarded (except when the onboard_two_node flag is enabled)."
            )
            if not pytest.onboard_2_node:
                pytest.onboard_1_node = False
        
        if (not pytest.testbed_stack_items) and pytest.onboard_stack:
            logger_obj.info(
                "There are no testbed_stack items left. Will make sure the stack node is not onboarded.")
            pytest.onboard_stack = False

        if ordered_items:
            logger_obj.info(
                f"These {len(ordered_items)} test(s) will run this session: {[get_test_marker(item)[0] for item in ordered_items]}")
        
        # modify the name of each test case that will be shown in the html report
        #
        # [base_name] -> [base_name] + [test_marker][#priority][#test_index]
        # * added test_index because the tests are not in the order they ran (in the html report) if one or more of them failed
        
        for item_index, item in enumerate(ordered_items):
            try:
                [test_marker] = get_test_marker(item)
                priority_marker: PriorityMarker = "P0" if (is_onboarding_cleanup_test(item) or is_onboarding_test(item)) else get_priority_marker(item)[0].upper()
                nodeid = re.search(fr".*{item.originalname}", item.nodeid).group(0)
            except:
                pass
            else:
                item._nodeid = f"{nodeid}[{test_marker}][{priority_marker}][#{item_index + 1}]"
        
        pytest.items = ordered_items
        items[:] = ordered_items
        
    else:
        
        # Pytest enters this branch when the runlist is not specified as argument.
        # Remove the onboarding test cases if they are included as items for this run
        # The onboarding tests should be used only when a runlist yaml file is provided as input

        temp_items: List[pytest.Function]
        
        temp_items = [
            item for item in items if
            not any(m.name in [pytest.onboarding_test_name, pytest.onboarding_cleanup_test_name]
                for m in get_item_markers(item))
        ]

        items[:] = temp_items


def pytest_sessionstart(session):
    
    session.results = dict()
    session.setup_results = dict()
    session.teardown_results = dict()

    pytest.runlist_path = session.config.option.runlist
    pytest.runlist_filtering_markers = session.config.option.runlist_filtering_markers

    if pytest.runlist_path != "default":

        if os.path.isfile(pytest.runlist_path):
            # the pytest.runlist_path variable is given in this form: 'extreme_automation_tests/data/NonProduction/XIQ/runlists/smoke_runlist.yaml'
            # there is no need to do a lookup for it in the data/ directory as it already contains the path to the runlist
            pass
        
        else:
            # here we will try to search in the data/ directory for the given runlist name
            # e.g. 
            #           --runlist smoke_runlist.yaml 
            #                 is equivalent to
            #           --runlist extreme_automation_tests/data/NonProduction/XIQ/runlists/smoke_runlist.yaml
            try:
                
                [runlist_path, *same_name_runlists] = list(Path(os.path.join(imp.find_module("extreme_automation_tests")[1], "data")).rglob(pytest.runlist_path))
                
                if same_name_runlists:
                    logger_obj.warning(
                        f"Found multiple runlist yamls named '{pytest.runlist_path}':\n" + "\n".join(str(p) for p in [runlist_path, *same_name_runlists]) + \
                        f"\nWill use the first runlist yaml: '{runlist_path}'.")
                
                pytest.runlist_path = str(runlist_path)
    
            except ValueError:
                error = f"Failed to find this runlist yaml: '{pytest.runlist_path}'."
                logger_obj.fail(error)

        try:
            with open(pytest.runlist_path, "r") as run_list:
                output_runlist = run_list.read()
        except:
            error = f"Failed to read the content of this runlist file: '{pytest.runlist_path}'."
            logger_obj.fail(error)

        try:
            pytest.runlist = yaml.safe_load(output_runlist)
            pytest.runlist_name = list(pytest.runlist)[0]
        except:
            logger_obj.fail(f"Failed to load the runlist yaml file: '{pytest.runlist_path}'.")
        
        try:
            pytest.runlist_tests = pytest.runlist[pytest.runlist_name]['tests']
        except:
            logger_obj.fail(f"It seems that the runlist yaml does not have the 'tests' field: '{pytest.runlist_path}'.")
        
        try:
            temp_suitemaps_name = pytest.runlist[pytest.runlist_name]['suitemap']
        except:
            logger_obj.fail(f"It seems that the runlist yaml does not have the 'suitemap' field: '{pytest.runlist_path}'.")

        for suitemap in temp_suitemaps_name:
            try:
                [suitemap] = list(Path(os.path.join(imp.find_module("extreme_automation_tests")[1], "data")).rglob(suitemap))
                suitemap = str(suitemap)

                with open(suitemap, "r") as run_list:
                    output_suitemap = run_list.read()
                
                pytest.suitemaps_name.append(suitemap)
            except:
                logger_obj.warning(f"Did not find this suitemap file: '{suitemap}'")
            else:
                suitemap_dict = yaml.safe_load(output_suitemap)
                suitemap_tests_dict = suitemap_dict.get("tests", {})
                
                if not suitemap_tests_dict:
                    logger_obj.warning(
                        f"Did not find any tests defined in this suitemap file: '{suitemap}'."
                        f"Make sure that the tests are placed under the 'tests' key in the suitemap file.")
                    
                suitemap_data_dict = suitemap_dict.get('data', {})
                pytest.suitemap_tests = {**pytest.suitemap_tests, **suitemap_tests_dict}
                pytest.suitemap_data = {**pytest.suitemap_data, **suitemap_data_dict}

        rerun_mapping = defaultdict(lambda: int())
        
        for test in pytest.runlist_tests:
            rerun_mapping[test] += 1

        rerun_mapping = {k: v for k, v in rerun_mapping.items() if v > 1}

        temp_pytest_tests = list(pytest.runlist_tests)
        pytest.runlist_tests = []
        
        count = defaultdict(lambda: 1)
        for test in temp_pytest_tests:
            if test not in rerun_mapping:
                pytest.runlist_tests.append(test)
            else:
                cnt = count[test]
                if cnt == 1:
                    pytest.runlist_tests.append(test)
                else:
                    pytest.runlist_tests.append(f"{test}_rerun_{cnt - 1}")
                count[test] += 1

        for test in pytest.runlist_tests:
            if match := re.search(r"(.*)_rerun_\d+$", test):
                base_test = match.group(1)
                
                if base_test in pytest.runlist_tests:
                    for entry, data in pytest.suitemap_tests.items():
                        if data.get("tc") == base_test:
                            pytest.suitemap_tests[entry]["tests"] = [{"tc": base_test}, {"tc": test}]
                            del pytest.suitemap_tests[entry]["tc"]
                            break
                        
                        elif "tests" in data:
                            entry_tests = data.get("tests")
                            for entry_test in entry_tests:
                                if entry_test["tc"] == base_test:
                                    temp_data = entry_test.copy()
                                    temp_data["tc"] = test
                                    pytest.suitemap_tests[entry]["tests"].append(temp_data)
                                    break

        pytest.onboarding_options: Options = pytest.runlist[pytest.runlist_name].get('onboarding_options', {})
        pytest.run_options: Options = pytest.runlist[pytest.runlist_name].get("run_options", {}) or {}


def print_run_status(session, tests):
    
    try:
        max_tb_length = max(len(", ".join(m.upper() for m in get_testbed_markers(item))) for item in tests)
        max_tb_length = max([max_tb_length, 9])
        max_tc_length = max([len(get_test_marker(item)[0]) for item in tests])
        max_tc_length = max([max_tc_length, 9])
        result_witdh = 17
        line_width = max_tc_length + max_tb_length + 6 * result_witdh + 36
        
        output = "\n+" + "-" * line_width + "+"
        output += f"\n| {'ORDER':^5} | {'TEST CASE':^{max_tc_length}} | {'P':^2} | {'TESTBED':^{max_tb_length}} | {'SETUP_RESULT':^{result_witdh}} | " \
                    f"{'CALL_RESULT':^{result_witdh}} | {'TEARDOWN_RESULT':^{result_witdh}} | " \
                    f"{'SETUP_DURATION':^{result_witdh}} | {'CALL_DURATION':^{result_witdh}} | " \
                    f"{'TEARDOWN_DURATION':^{result_witdh}} |"
        output += "\n+" + "-" * line_width + "+"
        
        for index, item in enumerate(tests):
            
            test_marker: TestCaseMarker
            [test_marker] = get_test_marker(item)
            
            test_priority: PriorityMarker = "P0" if (is_onboarding_cleanup_test(item) or is_onboarding_test(item)) else get_priority_marker(item)[0].upper()
            testbed_marker: TestbedMarker = "N/A" if (is_onboarding_cleanup_test(item) or is_onboarding_test(item)) else ", ".join(m.upper() for m in get_testbed_markers(item))
            
            setup_results = session.setup_results.get(item)
            setup_outcome = setup_results.outcome.upper()
            setup_duration = round(setup_results.duration, 2)

            if call_results := session.results.get(item):
                call_outcome = call_results.outcome.upper()
                call_duration = round(call_results.duration, 2)
            else:
                call_outcome, call_duration = "N/A", 0.0
            
            teardown_results = session.teardown_results.get(item)
            teardown_outcome = teardown_results.outcome.upper()
            teardown_duration = round(teardown_results.duration - call_duration - setup_duration, 2)
            teardown_duration = 0.0 if teardown_duration <= 0 else teardown_duration
            
            output += f"\n| {index + 1:^5} | {test_marker:^{max_tc_length}} | {test_priority:^2} | {testbed_marker:^{max_tb_length}} | {setup_outcome:^{result_witdh}} | " \
                        f"{call_outcome:^{result_witdh}} | {teardown_outcome:^{result_witdh}} | " \
                        f"{setup_duration:^{result_witdh}} | {call_duration:^{result_witdh}} | " \
                        f"{teardown_duration:^{result_witdh}} |"
            output += "\n+" + "-" * line_width + "+"
        
        logger_obj.info(output)

    except:
        pass


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session):

    if pytest.runlist_path != "default":
        
        config['${TEST_NAME}'] = "RESULTS"
        logger_obj.info(f"Results of runlist '{pytest.runlist_name}' (path '{pytest.runlist_path}')")
        print_run_status(session, pytest.items)

        repos = ['extreme_automation_framework', 'extreme_automation_tests']
    
        try:
            from git import Repo
            from git.exc import InvalidGitRepositoryError, NoSuchPathError
        except:
            pass
        else:    
            for repo_name in repos:
                for path in sys.path:
                    if re.search(rf"(.*/{repo_name})$", path):
                        try:
                            git_repo = Repo(path)
                        except (InvalidGitRepositoryError, NoSuchPathError):
                            pass
                        else:
                            try:
                                session.config._metadata[f"{repo_name} git dir"] = git_repo.git_dir
                                session.config._metadata[f"{repo_name} working tree dir"] = git_repo.working_tree_dir
                                session.config._metadata[f"{repo_name} feature branch"] = git_repo.active_branch.name
                                session.config._metadata[f"{repo_name} HEAD commit"] = git_repo.head.commit
                            except:
                                # TypeError: HEAD is a detached symbolic reference as it points to 'e893b741b753c3032f170500e19006c4cdbf6bde'
                                # FIX XAT-260
                                pass
                            break

        session.config._metadata["Runlist Path"] = pytest.runlist_path
        session.config._metadata["Runlist Name"] = pytest.runlist_name
        session.config._metadata["Suitemaps"] = pytest.suitemaps_name
        
        if run_options := pytest.run_options:
            session.config._metadata["Run Options"] = run_options

        if xiq_version := pytest.xiq_version:
            session.config._metadata["XIQ version"] = xiq_version

        for field in pytest.data:
            if data := pytest.data.get(field):
                session.config._metadata[field] = data


def pytest_generate_tests(metafunc):
    
    if pytest.runlist_path != "default":
        
        try:
            test_identifier = f"{metafunc.definition.cls.__name__}::{metafunc.definition.originalname}"
        except AttributeError:
            logger_obj.warning(
                f"This test is not placed in a test class: '{metafunc.definition.nodeid}'.")
        else:
            try:
                test_data = pytest.suitemap_tests[test_identifier]
            except KeyError:
                logger_obj.warning(
                        f"This test does not have a definition in the suitemap files: '{metafunc.definition.nodeid}'.")
            else:
                parameteterized_test_data = []
                
                if "tests" in test_data:
                    base_data = {k: v for k, v in test_data.items() if k != "tests"}
                    for data in test_data["tests"]:
                        parameteterized_test_data.append({**base_data, **data})
                    test_data = parameteterized_test_data

                else:
                    test_data = [test_data]
                    
                if "test_data" in metafunc.fixturenames:
                    metafunc.parametrize("test_data", test_data)
                    
                if "suite_data" in metafunc.fixturenames:
                    metafunc.parametrize("suite_data", [pytest.suitemap_data])


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    
    outcome = yield
    
    if pytest.runlist_path != "default":
        
        result = outcome.get_result()

        current_test_marker: TestCaseMarker
        temp_test_marker: TestCaseMarker
        [current_test_marker] = get_test_marker(item)

        if result.when == 'call':
            
            item.session.results[item] = result

            if outcome := result.outcome: 
                if outcome == "passed":
                    logger_obj.info(
                        f"\n{Colors.Bg.GREEN}{Colors.Style.BRIGHT}{Colors.Fg.WHITE} --> {current_test_marker.upper()} PASSED <--"
                        f" {Colors.Bg.RESET}{Colors.Style.RESET_ALL}")
                elif outcome == "failed":
                    logger_obj.info(
                        f"\n{Colors.Bg.RED}{Colors.Style.BRIGHT}{Colors.Fg.WHITE} --> {current_test_marker.upper()} FAILED <-- "
                        f"{Colors.Bg.RESET}{Colors.Style.RESET_ALL}")
        
        elif result.when == "setup":
            
            item.session.setup_results[item] = result
            
            if (outcome := result.outcome) == "skipped":
                logger_obj.info(f"\n{Colors.Bg.BLUE}{Colors.Style.BRIGHT}{Colors.Fg.WHITE} --> {current_test_marker.upper()} SKIPPED "
                    f"<-- {Colors.Bg.RESET}{Colors.Style.RESET_ALL}")

        elif result.when == "teardown":
            
            item.session.teardown_results[item] = result
            
            next_tests: List[pytest.Function] = [get_test_marker(item)[0] for item in pytest.items[pytest.items.index(item) + 1:]]
            
            if next_tests:
                logger_obj.info(
                    f"These {len(next_tests)} test(s) will run next: " + "'" + "', '".join(next_tests) + "'.")
                
        if result.outcome in ["failed", "skipped"]:
            
            for it in item.session.items:
                [temp_test_marker] = get_test_marker(it)
                for mk in it.own_markers:
                    if mk.name == "dependson":
                        if len(mk.args) > 0:
                            if current_test_marker in mk.args:                            
                                it.add_marker(
                                    pytest.mark.skip(
                                        f"'{temp_test_marker}' depends on '{current_test_marker}' but "
                                        f"'{current_test_marker}' is {result.outcome}. The '{temp_test_marker}' "
                                        f"test case will be skipped."))

        if "skip" in [m.name for m in item.own_markers]:
            for it in item.session.items:
                [temp_test_marker] = get_test_marker(it)
                for mk in it.own_markers:
                    if mk.name == "dependson":
                        if current_test_marker in mk.args:
                            it.add_marker(
                                pytest.mark.skip(
                                    f"'{temp_test_marker}' depends on '{current_test_marker}' but "
                                    f"'{current_test_marker}' is skipped. The '{temp_test_marker}' "
                                    f"test case will be skipped.")
                                )


def pytest_runtest_setup(item):
    
    if pytest.runlist_path != "default":
        
        current_test_marker: TestCaseMarker
        
        [current_test_marker] = get_test_marker(item)
        
        if tests := pytest.items[:pytest.items.index(item)]:
            logger_obj.info("The results for the tests that have run so far:")
            print_run_status(item.session, tests=tests)

        try:
            config['${TEST_NAME}'] = f"{current_test_marker} | SETUP | {pytest.items.index(item) + 1}/{len(pytest.items)}"
        except:
            config['${TEST_NAME}'] = current_test_marker

        request: fixtures.SubRequest = FixtureRequest(item, _ispytest=True)

        for marker in item.own_markers:

            # valid markers: 
            #   @pytest.mark.skip_if_{node}_{field}(*args)
            #
            #   e.g.
            #        @pytest.mark.skip_if_node_1_platform("5420", "5520") -> will skip test case if the platform of the switch is in ["5420", "5520"]
            #
            #   node  -> node|node_1|node_2|node_stack
            #   field -> cli_type|make|model|platform
            #   args  -> values for given field
            
            for node in ["node", "node_1", "node_2", "node_stack"]:
                for field in ["cli_type", "make", "model", "platform"]:
                    if (marker.name == f'skip_if_{node}_{field}') and bool(marker.args):
                        node_fxt = request.getfixturevalue(node)
                        if node_fxt:
                            if field_value := node_fxt.get(field):
                                if any(field_value.upper() == str(arg).upper() for arg in marker.args):
                                    msg = f"'{current_test_marker}' test case will be skipped because " \
                                          f"it is not meant to run when '{node_fxt.node_name}' has" \
                                          f" '{field_value}' set for the '{field}' field."
                                    item.add_marker(pytest.mark.skip(msg))
                                    pytest.skip(msg)
            
            # valid markers: 
            #   @pytest.mark.run_if_{node}_{field}(*args)
            #
            #   e.g.
            #       @pytest.mark.run_if_node_1_platform("5420", "5520") -> will skip test case if the platform of the switch is not in ["5420", "5520"]
            #
            #   node -> node|node_1|node_2|node_stack
            #   field -> cli_type|make|model|platform
            #   args -> values for given field
               
                    if (marker.name == f'run_if_{node}_{field}') and bool(marker.args):
                        node_fxt = request.getfixturevalue(node)
                        if node_fxt:
                            if field_value := node_fxt.get(field):
                                if not any(field_value.upper() == arg.upper() for arg in marker.args):
                                    msg = f"'{current_test_marker}' test case will be skipped because " \
                                          f"it is meant to run when '{node_fxt.node_name}' has" \
                                          f" any of {marker.args} set for the '{field}' field."           
                                    item.add_marker(pytest.mark.skip(msg))
                                    pytest.skip(msg)
                                                
            # e.g.
            #     @pytest.mark.skip_if_browser("chrome")
            #

            if (marker.name == "skip_if_browser") and bool(marker.args):
                if browser := config.get("BROWSER"):
                    if any(browser.upper() == value.upper() for value in marker.args):
                        msg = f"'{current_test_marker}' test case will be skipped because " \
                              f"it is not meant to run when the used browser is '{browser}'."
                        item.add_marker(pytest.mark.skip(msg))
                        pytest.skip(msg)
            
            # e.g.
            #     @pytest.mark.skip_if_lab("BUCHAREST")
            #

            if (marker.name == "skip_if_lab") and bool(marker.args):
                if lab := config.get("lab"):
                    if any(lab.upper() == value.upper() for value in marker.args):
                        msg = f"'{current_test_marker}' test case will be skipped because " \
                              f"it is not meant to run when lab is '{lab}'."
                        item.add_marker(pytest.mark.skip(msg))
                        pytest.skip(msg)

            # e.g.
            #     @pytest.mark.skip_if_node_1_does_not_support_poe -> will skip test case if node_1 does not support poe
            #

            for node in ["node", "node_1", "node_2", "node_stack"]:
                if marker.name == f"skip_if_{node}_does_not_support_poe":
                    node_fxt = request.getfixturevalue(node)
                    if node_fxt:
                        if not request.getfixturevalue(f"{node}_poe_capability"):
                            msg = f"'{current_test_marker}' test case will be skipped because " \
                                  f"it is not meant to run when {node} does not support poe."
                            item.add_marker(pytest.mark.skip(msg))
                            pytest.skip(msg)  

            legacy_voss = ["1400", "4900", "7400"]
            unified_hardware = ["5200", "5300", "5400", "5500", "5700"]

            # valid markers: 
            #   @pytest.mark.run_if_{node}_{field}
            # 
            # e.g.
            #     @pytest.mark.run_if_node_1_legacy_voss        -> will not skip test case if node_1 is legacy voss
            #     @pytest.mark.run_if_node_1_unified_hardware   -> will not skip test case if node_1 is unified hardware
            #
            #   node  -> node|node_1|node_2|node_stack
            #   field -> legacy_voss|unified hardware
            #
            
            for node in ["node", "node_1", "node_2", "node_stack"]:
                for device_platform in ["legacy_voss", "unified_hardware"]:
                    if marker.name == f"run_if_{node}_is_{device_platform}":
                        node_fxt = request.getfixturevalue(node)
                        if node_fxt:
                            if node_fxt.node_name == "node_stack":
                                # will get the platform from the model field
                                model = node_fxt.model
                                platform_match = re.search(r"Engine(\d{4})", model)
                                if not platform_match:
                                    continue
                                node_platform = platform_match.group(1)[:2]
                            else:
                                node_platform = str(node_fxt.platform)[:2]
                                
                            if not any(node_platform == str(hw)[:2] for hw in locals()[device_platform]):
                                msg = f"'{current_test_marker}' test case will be skipped because " \
                                    f"it is meant to run when {node} is {device_platform} ({locals()[device_platform]})."
                                item.add_marker(pytest.mark.skip(msg))
                                pytest.skip(msg)

            # valid markers: 
            #   @pytest.mark.skip_if_{node}_{field}
            # 
            # e.g.
            #     @pytest.mark.skip_if_node_1_is_legacy_voss        -> will skip test case if node_1 is legacy voss
            #     @pytest.mark.skip_if_node_1_is_unified_hardware   -> will skip test case if node_1 is unified hardware
            #
            #   node  -> node|node_1|node_2|node_stack
            #   field -> legacy_voss|unified hardware
            #
            
            for node in ["node", "node_1", "node_2", "node_stack"]:
                for device_platform in ["legacy_voss", "unified_hardware"]:
                    if marker.name == f"skip_if_{node}_is_{device_platform}":
                        node_fxt = request.getfixturevalue(node)
                        if node_fxt:
                            if node_fxt.node_name == "node_stack":
                                # will get the platform from the model field
                                model = node_fxt.model
                                platform_match = re.search(r"Engine(\d{4})", model)
                                if not platform_match:
                                    continue
                                node_platform = platform_match.group(1)[:2]
                            else:
                                node_platform = str(node_fxt.platform)[:2]
                            if any(node_platform == str(hw)[:2] for hw in locals()[device_platform]):
                                msg = f"'{current_test_marker}' test case will be skipped because " \
                                    f"it is not meant to run when {node} is {device_platform} ({locals()[device_platform]})."
                                item.add_marker(pytest.mark.skip(msg))
                                pytest.skip(msg)

            # valid markers: 
            #   @pytest.mark.skip_if_{node}_{software}_version_{operator}({version}, {os})
            #   
            #   e.g. 
            #        @pytest.mark.skip_if_node_1_system_version_lt("8.8.0.0", "VOSS") -> will skip test case if switch is VOSS and has system version < 8.8.0.0
            #
            #           if box is VOSS and has iqagent_version='0.6.0', system_version='8.8.0.0'
            #
            #        @pytest.mark.skip_if_node_1_system_version_eq("8.8.0.0", "VOSS")  -> SKIPPED
            #        @pytest.mark.skip_if_node_1_system_version_eq("8.8.0.0", "EXOS")  -> NOT SKIPPED
            #        @pytest.mark.skip_if_node_1_system_version_eq("8.7.0.0", "VOSS")  -> NOT SKIPPED
            #        @pytest.mark.skip_if_node_1_system_version_lt("8.8.0.1", "VOSS")  -> SKIPPED
            #        @pytest.mark.skip_if_node_1_system_version_le("8.8.0.0", "VOSS")  -> SKIPPED
            #        @pytest.mark.skip_if_node_1_system_version_lt("7.8.0.0", "VOSS")  -> NOT SKIPPED
            #        @pytest.mark.skip_if_node_1_system_version_gt("7.8.0.0", "VOSS")  -> SKIPPED
            #        @pytest.mark.skip_if_node_1_system_version_ge("8.8.0.0", "VOSS")  -> SKIPPED
            #        @pytest.mark.skip_if_node_1_system_version_ge("8.8.0.0", "EXOS")  -> NOT SKIPPED
            #        @pytest.mark.skip_if_node_1_iqagent_version_eq("0.6.0", "VOSS")   -> SKIPPED
            #        @pytest.mark.skip_if_node_1_iqagent_version_eq("0.6.0", "EXOS")   -> NOT SKIPPED
            #        @pytest.mark.skip_if_node_1_iqagent_version_lt("0.6.0.1", "VOSS") -> SKIPPED
            #        @pytest.mark.skip_if_node_1_iqagent_version_le("0.6.0", "VOSS")   -> SKIPPED
            #        @pytest.mark.skip_if_node_1_iqagent_version_gt("0.5.0", "VOSS")   -> SKIPPED
            #        @pytest.mark.skip_if_node_1_iqagent_version_ge("0.6.0", "VOSS")   -> SKIPPED
            #        @pytest.mark.skip_if_node_1_iqagent_version_ge("0.6.0", "EXOS")   -> NOT SKIPPED
            #
            #   node     -> node|node_1|node_2|node_stack
            #   software -> system|iqagent
            #   operator -> lt|le|gt|ge|eq
            #   version  -> the expected {software} version
            #   os       -> the OS of the switch
            #
            #   note: currently implemented only for EXOS/VOSS

            for found_node in ["node", "node_1", "node_2", "node_stack"]:
                for found_operator in ["lt", "le", "gt", "ge", "eq"]:
                    for found_software in ["iqagent", "system"]:
                        if (marker.name == f"skip_if_{found_node}_{found_software}_version_{found_operator}") and len(marker.args) == 2:
                            marker_version = marker.args[0]
                            marker_os = marker.args[1].upper()
                            if node_fxt := request.getfixturevalue(found_node):  
                                if marker_os == node_fxt.cli_type.upper():
                                    if sys_fxt := request.getfixturevalue(f"{found_node}_starting_{found_software}_version"):
                                        if (found_software == "system") and (node_fxt.node_name == "node_stack"):
                                            sys_fxt = sys_fxt[0][1]
                                        try:
                                            op = f"getattr(operator, '{found_operator}')(LooseVersion('{sys_fxt}'), LooseVersion('{marker_version}'))"
                                            result = eval(op)
                                        except:
                                            logger_obj.warning("Failed to parse versions.")
                                        else:

                                            if result is True:
                                                msg = f"'{current_test_marker}' test case will be skipped because " \
                                                    f"it is not meant to run when '{node_fxt.node_name}' is '{marker_os}' and" \
                                                    f" its {found_software} version ('{sys_fxt}') is {found_operator} '{marker_version}'."
                                                item.add_marker(pytest.mark.skip(msg))
                                                pytest.skip(msg)

        if (not is_onboarding_test(item)) and (not is_onboarding_cleanup_test(item)):
            logger_obj.step(f"Start SETUP of test function '{current_test_marker}': '{item.nodeid}'.")


def pytest_runtest_teardown(item):
    
    if pytest.runlist_path != "default":
        
        current_test_marker: TestCaseMarker
        
        [current_test_marker] = get_test_marker(item)
        
        try:
            config['${TEST_NAME}'] = f"{current_test_marker} | TEARDOWN | {pytest.items.index(item) + 1}/{len(pytest.items)}"
        except:
            config['${TEST_NAME}'] = current_test_marker

        if (not is_onboarding_test(item)) and (not is_onboarding_cleanup_test(item)):
            logger_obj.step(f"Start TEARDOWN of test function '{current_test_marker}': '{item.nodeid}'.")


def pytest_runtest_call(item):
    
    if pytest.runlist_path != "default":
        
        current_test_marker: TestCaseMarker
        
        [current_test_marker] = get_test_marker(item)
        
        try:
            config['${TEST_NAME}'] = f"{current_test_marker} | {pytest.items.index(item) + 1}/{len(pytest.items)}"
        except:
            config['${TEST_NAME}'] = current_test_marker

        logger_obj.step(f"Start test function '{current_test_marker}': '{item.nodeid}'.")

        test_data = {}
        mandatory_fields = ["author", "tc", "description", "title", "steps"]

        if callspec := getattr(item, "callspec", None):
            if data := callspec.params.get("test_data"):
                test_data = data
        else:
            test_data = pytest.suitemap_tests[f"{item.cls.__name__}::{item.originalname}"]
            
        data = defaultdict(lambda: dict())
        for key, value in {k: test_data.get(k) for k in mandatory_fields}.items():
            if value:
                if key == "steps":
                    data["Test Steps"] = str(len(value))
                    for step_index, step in enumerate(value):
                        data[f"  Step {step_index + 1}"] = step
                elif key in mandatory_fields:
                    data[key.capitalize()] = value

        if not_mandatory_data := {k: v for k, v in test_data.items() if k not in mandatory_fields}:
            data["Test Data"] = ""
            for key, value in not_mandatory_data.items():
                data[f"  {key}"] = str(value)
        
        if data:
            max_len_fields = max(len(str(k)) for k in data)
            max_len_values = max(len(str(v)) for v in data.values())

            temp_lines = ["\n+" + "-" * (max_len_fields + max_len_values + 4) + "+"]
            for key, value in data.items():
                if key in ["Test Steps", "Test Data"]:
                    temp_lines.append("+" + "-" * (max_len_fields + max_len_values + 4) + "+")
                temp_lines.append(f"| {key:<{max_len_fields}}: {value:<{max_len_values}} |")
            temp_lines.append("+" + "-" * (max_len_fields + max_len_values + 4) + "+")
            logger_obj.step("\n".join(temp_lines))


@pytest.fixture(scope="session")
def reset_switch(
    node_list: List[Node],
    network_manager: NetworkElementConnectionManager,
    dev_cmd: NetworkElementCliSend,
    reset_utils: NetworkElementResetDeviceUtilsKeywords,
    request: fixtures.SubRequest,
    logger: PytestLogger,
    utils: Utils,
    debug: Callable
) -> ResetSwitch:
    """ 
    This fixture is intended to be used only in the onboarding fixture because 
    it uses the onboarding options given for each node in the runlist yaml. 
    """
    
    errors: List[str] = []

    @debug
    def reset_switch_func() -> None:
        def reset_switch_worker(
            node: Node
            ) -> None:
            
            onboarding_options: Options = request.getfixturevalue(f"{node.node_name}_onboarding_options")
            
            if onboarding_options.get("reset_switch_to_factory_defaults", False):
                
                logger.info(f"The 'reset_switch_to_factory_defaults' flag is enabled for the '{node.node_name}' node.")
                
                if not (node.get("console_ip") and node.get("console_port")):
                    logger.warning(
                        f"The 'reset_switch_to_factory_defaults' flag is enabled for the '{node.node_name}' node "
                        f"but this node does not have the console ip/console port configured in the yaml file.")
                    return

                if node.node_name == "node_stack":
                    logger.warning("Currently reset switch to factory defaults for stack is not implemented.")
                    return

                try:
                    if node.cli_type.upper() == "EXOS":
                        
                        try:
                            network_manager.connect_to_network_element_name(node.name)
                            
                            logger.step(f"Reset to the factory defaults the '{node.node_name}' node.")
                            reset_utils.reset_network_element_to_factory_defaults(node.name)
                            utils.wait_till(timeout=180)
                            logger.info(f"Successfully reset to the factory default the '{node.node_name}' node.")
                        
                        finally:
                            network_manager.close_connection_to_network_element(node.name)
                        
                        try:
                            network_manager.connect_to_network_element(
                                node.name, ip=node.console_ip, username=node.username, password=node.password, connection_method="telnet", 
                                device_cli_type=node.cli_type, port=node.console_port
                            )
                            reset_utils.bypass_initial_setup(node.name)

                        finally:
                            network_manager.close_connection_to_network_element(node.name)

                        try:
                            network_manager.connect_to_network_element(
                                node.name, ip=node.console_ip, username=node.username, password=node.password, connection_method="telnet", 
                                device_cli_type=node.cli_type, port=node.console_port
                            )
                            
                            dev_cmd.send_cmd(
                                node.name, "enable ssh2", max_wait=10, interval=2,
                                confirmation_phrases="Continue?",
                                confirmation_args='y'
                            )
                        finally:
                            network_manager.close_connection_to_network_element(node.name)
                                
                    elif node.cli_type.upper() == "VOSS":
                        
                        try:
                            network_manager.connect_to_network_element_name(node.name)
                            
                            output = dev_cmd.send_cmd(
                                node.name, 'show boot config choice',
                                max_wait=10, interval=2)[0].return_text
                            config_file = re.findall(r"choice primary config-file \"(.*)\"", output)[0]

                            logger.step(f"Delete this primary config file from '{node.node_name}' node: '{config_file}'.")
                            dev_cmd.send_cmd(
                                node.name, f"remove {config_file}", max_wait=10, interval=2,
                                confirmation_phrases="Are you sure (y/n)",
                                confirmation_args='y'
                            )
                            
                            logger.step(f"Reset to the factory defaults the '{node.node_name}' node.")
                            reset_utils.reboot_network_element_now_and_wait(node.name, max_wait=300)
                            logger.info(f"Successfully reset to the factory default the '{node.node_name}' node.")
                            
                        finally:
                            network_manager.close_connection_to_network_element(node.name)
                        
                        conn_str = f"telnet {node.console_ip} {node.console_port}"
                        
                        with pexpect.spawn(conn_str) as spawn_connection:
                            spawn_connection.sendline()
                            
                            i = spawn_connection.expect([pexpect.TIMEOUT, 'Login:'])
                            assert i == 1, "Failed to find this prompt after the reset: 'Login:'."
                            spawn_connection.sendline(node.username)
                            
                            i = spawn_connection.expect([pexpect.TIMEOUT, 'Password:'])
                            assert i == 1, "Failed to find this prompt after the reset: 'Password:'."
                            spawn_connection.sendline(node.password)
                            
                            i = spawn_connection.expect([pexpect.TIMEOUT, 'Enter the New password :'])
                            assert i == 1, "Failed to find this prompt after the reset: 'Enter the New password :'."
                            spawn_connection.sendline(node.password)
                            
                            i = spawn_connection.expect([pexpect.TIMEOUT, 'Re-enter the New password :'])
                            assert i == 1, "Failed to find this prompt after the reset: 'Re-enter the New password :'."
                            spawn_connection.sendline(node.password)
                            
                            i = spawn_connection.expect([pexpect.TIMEOUT, "Password changed successfully"])
                            assert i == 1, "Failed to find this message after the reset: 'Password changed successfully'."
                            
                            spawn_connection.sendline()
                            
                except Exception as exc:
                    errors.append(f"Failed to reset to factory defaults this node: '{node.node_name}'.\n{repr(exc)}")  
    
            elif onboarding_options.get("reboot_switch", False):
                
                logger.info(f"The 'reboot_switch' flag is enabled for the '{node.node_name}' node.")
                
                try:
                    logger.step(f"Reboot the '{node.node_name}' node.")
                    network_manager.connect_to_network_element_name(node.name)
                    reset_utils.reboot_network_element_now_and_wait(node.name, max_wait=300)
                    logger.info(f"Successfully reboot the '{node.node_name}' node.")
                except Exception as exc:
                    errors.append(f"Failed to reboot this node: '{node.node_name}'.\n{repr(exc)}")  
                finally:
                    network_manager.close_connection_to_network_element(node.name)

        threads: List[threading.Thread] = []
            
        try:
            for node in node_list:
                thread = threading.Thread(target=reset_switch_worker, args=(node, ))
                threads.append(thread)
                thread.start()
        finally:
            for thread in threads:
                thread.join()

        for error in errors:
            logger.error(error)
    
        if errors:
            pytest.fail("\n".join(errors))

    return reset_switch_func


class OnboardingTests:
    
    @pytest.mark.tcxm_xiq_onboarding
    def test_xiq_onboarding(
            self,
            request: fixtures.SubRequest,
            logger: PytestLogger
    ) -> None:
        """ 
        It should be the first test in the runlist in order to onboard the network devices before the other tests.
        The tests that depend on this test should use this marker '@pytest.mark.dependson("tcxm_xiq_onboarding")'
         in order to be skipped if the onboarding fails or is skipped.
        This test must be added to the suitemap yaml in order to be later used in the runlist yaml.
        """

        if pytest.run_options.get("skip_setup"):
            logger_obj.info(
                "The 'skip_setup' option is given in runlist. The onboarding test case is skipped.")
            request.getfixturevalue("test_bed")
            return

        if not any(getattr(pytest, f"onboard_{ntype}") for ntype in [tb.split("testbed_")[1] for tb in valid_testbed_markers if tb != "testbed_none"]): 
            logger.info(
                "There are no devices given in the yaml files or there are no tests left to run "
                "so the onboarding test won't configure anything.")
            return
        
        request.getfixturevalue("onboard")


    @pytest.mark.tcxm_xiq_onboarding_cleanup
    def test_xiq_onboarding_cleanup(
        self,
        request: fixtures.SubRequest,
        logger: PytestLogger
        ) -> None:
        """
        It should be the last test in the runlist in order to clean the onboarded devices after all the tests ran
        """

        if pytest.run_options.get("skip_teardown"):
            logger_obj.info(
                "The 'skip_teardown' option is given in runlist. The onboarding cleanup test case is skipped.")
            return
        
        if not any(getattr(pytest, f"onboard_{ntype}") for ntype in [tb.split("testbed_")[1] for tb in valid_testbed_markers if tb != "testbed_none"]): 
            logger.info(
                "There are no devices given in the yaml files or there were no tests left to run"
                " so the onboarding cleanup test won't unconfigure anything.")
            return

        request.getfixturevalue("onboard_cleanup")


@pytest.fixture(scope="session")
def login_xiq(
        debug: Callable,
        get_xiq_library,
        deactivate_xiq_library,
        logger: PytestLogger
) -> LoginXiq:

    @contextmanager
    @debug
    def login_xiq_func(
    ) -> Iterator[XiqLibrary]:

        xiq: XiqLibrary = None
        
        try:
            xiq = get_xiq_library()

            if not pytest.xiq_version:
                pytest.xiq_version = xiq.login.get_xiq_version()
                logger.info(f"XIQ has version '{pytest.xiq_version}'.")

            yield xiq
        finally:
            deactivate_xiq_library(xiq)

    return login_xiq_func


@pytest.fixture(scope="session")
def get_xiq_library(
    loaded_config: Dict[str, str],
    logger: PytestLogger,
    cloud_driver: CloudDriver,
    debug: Callable
) -> GetXiqLibrary:
    """
    Method that creates a XiqLibrary object and then authenticate to XIQ with the credentials available in the topology yaml.
    """

    @debug
    def get_xiq_library_func(
        username: str = loaded_config['tenant_username'],
        password: str = loaded_config['tenant_password'],
        url: str = loaded_config['test_url'],
        capture_version: bool = False,
        code: str = "default",
        incognito_mode: str = "False"
    ) -> XiqLibrary:
        
        xiq = XiqLibrary()

        try:
            assert xiq.login.login_user(
                username,
                password,
                capture_version=capture_version,
                code=code, url=url,
                incognito_mode=incognito_mode
            )
            cloud_driver.cloud_driver.maximize_window()
        except Exception as exc:
            logger.error(repr(exc))
            cloud_driver.close_browser()
            raise exc
        else:
            return xiq
    return get_xiq_library_func

    
@pytest.fixture(scope="class")
def xiq_library_at_class_level(
    request: fixtures.SubRequest
) -> XiqLibrary:
    """
    The fixture creates a XiqLibrary object before the start of the first test of this class.
    After the last test ran, the created XiqLibrary object is deleted.
    """
    
    get_xiq_library: GetXiqLibrary = request.getfixturevalue("get_xiq_library")
    deactivate_xiq_library: DeactivateXiqLibrary = request.getfixturevalue("deactivate_xiq_library")
    
    xiq: XiqLibrary = None
    
    try:
        xiq = get_xiq_library()
        yield xiq
    finally:
        deactivate_xiq_library(xiq)


@pytest.fixture
def xiq_library(
    request: fixtures.SubRequest
) -> XiqLibrary:
    """
    The fixture creates a XiqLibrary object before the start of the current test case.
    After the current test ran, the created XiqLibrary object is deleted.
    """
    
    get_xiq_library: GetXiqLibrary = request.getfixturevalue("get_xiq_library")
    deactivate_xiq_library: DeactivateXiqLibrary = request.getfixturevalue("deactivate_xiq_library")
    
    xiq: XiqLibrary = None
    
    try:
        xiq = get_xiq_library()
        yield xiq
    finally:
        deactivate_xiq_library(xiq)


@pytest.fixture(scope="session")
def deactivate_xiq_library(
    debug: Callable,
    cloud_driver: CloudDriver,
    logger: PytestLogger
) -> DeactivateXiqLibrary:
    """
    Fixture that deactivates the given XiqLibrary object.
    """
    
    @debug
    def deactivate_xiq_library_func(
        xiq: XiqLibrary
    ) -> None:
        
        try:
            xiq.login.logout_user()
            xiq.login.quit_browser()
        except Exception as exc:
            # this branch covers the case when a window in XIQ is not closed and the logout will raise an error -> e.g. the honeycomb port type editor
            logger.error(f"Failed to logout and close the browser. Will try to forcefully close the browser using the cloud driver object.\n{repr(exc)}")
            try:
                cloud_driver.cloud_driver.close()
            except:
                pass
    return deactivate_xiq_library_func


@pytest.fixture(scope="session")
def enter_switch_cli(
        network_manager: NetworkElementConnectionManager,
        close_connection: CloseConnection,
        dev_cmd: NetworkElementCliSend
) -> EnterSwitchCli:
    """
    Fixture that connects to a device and returns the NetworkElementCliSend object.
    At the end the connection to the device is closed.
    """

    @contextmanager
    def enter_switch_cli_func(
            dut: Node
    ) -> Iterator[NetworkElementCliSend]:
        try:
            close_connection(dut)
            network_manager.connect_to_network_element_name(dut.name)
            yield dev_cmd
        finally:
            close_connection(dut)
    return enter_switch_cli_func


@pytest.fixture(scope="session")
def cli() -> Cli:
    return Cli()


@pytest.fixture(scope="session")
def open_spawn(
        cli: Cli
) -> OpenSpawn:
    """
    Fixture that creates a spawn connection to the device and returns the said connection.
    At the end the spawn is closed.
    """

    @contextmanager
    def open_spawn_func(
            dut: Node
    ) -> Iterator[pxssh]:
        try:
            spawn_connection = cli.open_spawn(
                dut.ip, dut.port, dut.username, dut.password, dut.cli_type)
            yield spawn_connection
        finally:          
            cli.close_spawn(spawn_connection)
    return open_spawn_func


@pytest.fixture(scope="session")
def open_pxssh_spawn(
    cli: Cli
) -> OpenPxsshSpawn:

    @contextmanager
    def open_pxssh_spawn_func(
            dut: Node,
            debug_mode: bool=False,
            disable_strict_host_key_checking: bool=True,
            **kwargs
    ) -> Iterator[pxssh]:
        try:
            spawn_connection = cli._Cli__open_pxssh_spawn(
                dut.ip, dut.username, dut.password, disable_strict_host_key_checking=disable_strict_host_key_checking, **kwargs)
            
            if debug_mode:
                if 'EXOS' in dut.cli_type.upper():
                    cli.send(spawn_connection, 'disable cli paging', pxssh=True)
                    cli.send(spawn_connection, 'debug iqagent show log hive-agent tail', pxssh=True)

                elif 'VOSS' in dut.cli_type.upper():
                    cli.send(spawn_connection, 'enable', pxssh=True)
                    cli.send(spawn_connection, 'configure terminal', pxssh=True)
                    cli.send(spawn_connection, 'trace level 261 3', pxssh=True)
                    cli.send(spawn_connection, 'trace screen enable', pxssh=True)

            yield spawn_connection
        finally:          
            spawn_connection.close()
    return open_pxssh_spawn_func


@pytest.fixture(scope="session")
def connect_to_all_devices(
        network_manager: NetworkElementConnectionManager,
        dev_cmd: NetworkElementCliSend
) -> Callable[[], Iterator[NetworkElementCliSend]]:
    """
    Fixture that connects to all devices and returns the NetworkElementCliSend object.
    At the end the connections to the devices are closed.
    """

    @contextmanager
    def connect_to_all_devices_func(
    ) -> Iterator[NetworkElementCliSend]:
        try:
            network_manager.connect_to_all_network_elements()
            yield dev_cmd
        finally:
            network_manager.close_connection_to_all_network_elements()
    return connect_to_all_devices_func


@pytest.fixture(scope="session")
def create_location(
        logger: PytestLogger,
        screen: Screen,
        debug: Callable
) -> CreateLocation:
    
    @debug
    def create_location_func(
            xiq: XiqLibrary,
            location: str
    ) -> None:
        
        logger.step(f"Try to delete this location: '{location}'.")
        xiq.xflowsmanageLocation.delete_location_building_floor(*location.split(","))
        screen.save_screen_shot()
        
        logger.step(f"Create this location: '{location}'.")
        xiq.xflowsmanageLocation.create_location_building_floor(*location.split(","))
        screen.save_screen_shot()
        
    return create_location_func


def generate_template_for_given_model(
        dut: Node
) -> List[str]:

    model = dut.model
    platform = dut.platform
    slots = dut.get("stack")
    
    if platform.lower() == 'stack':
        if not slots:
            pytest.fail("No slots available in current stack")

        model_list: List[str] = []
        sw_model: str = ""

        for slot in slots.values():
            
            slot_model = slot.model
            
            if "SwitchEngine" in slot_model:
                mat = re.match('(.*)(Engine)(.*)', slot_model)
                model_md = mat.group(1) + ' ' + mat.group(2) + ' ' + mat.group(3).replace('_', '-')
                switch_type = re.match(r'(\d+).*', mat.group(3).split('_')[0]).group(1)
                sw_model = 'Switch Engine ' + switch_type + '-Series-Stack'

            else:
                model_act = slot_model.replace('10_G4', '10G4')
                m = re.match(r'(X\d+)(G2)(.*)', model_act)
                model_md = m.group(1) + '-' + m.group(2) + m.group(3).replace('_', '-')
                sw_model = m.group(1) + '-' + m.group(2) + '-Series-Stack'
            model_list.append(model_md)

        model_units = ','.join(model_list)
        return sw_model, model_units

    elif "Engine" in model:
        mat = re.match('(.*)(Engine)(.*)', model)
        sw_model = mat.group(1) + ' ' + mat.group(2) + ' ' + mat.group(3).replace('_', '-')

    elif "G2" in model:
        model_act = model.replace('10_G4', '10G4')
        m = re.match(r'(X\d+)(G2)(.*)', model_act)
        sw_model = m.group(1) + '-' + m.group(2) + m.group(3).replace('_', '-')

    else:
        sw_model = model.replace('_', '-')
    return sw_model, ""


@pytest.fixture(scope="session")
def close_connection(
        network_manager: NetworkElementConnectionManager,
        logger: PytestLogger
) -> CloseConnection:
    def close_connection_func(dut: Node) -> None:
        try:
            network_manager.close_connection_to_network_element(dut.name)
        except Exception as exc:
            logger.info(exc)
    return close_connection_func


@pytest.fixture(scope="session")
def virtual_routers(
        enter_switch_cli: EnterSwitchCli,
        node_list: List[Node],
        logger: PytestLogger,
        nodes_data: NodesData
) -> Dict[str, str]:
    return nodes_data.get("virtual_routers", {})
 

@pytest.fixture(scope="session")
def poe_capabilities(
    nodes_data: NodesData
) -> Dict[str, bool]:
    return {
        k: v["poe"] for k, v in nodes_data.items()
    }


@pytest.fixture(scope="session")
def node_1_poe_capability(
    poe_capabilities: Dict[str, bool]
) -> bool:
    return poe_capabilities.get("node_1")


@pytest.fixture(scope="session")
def node_2_poe_capability(
    poe_capabilities: Dict[str, bool]
) -> bool:
    return poe_capabilities.get("node_2")


@pytest.fixture(scope="session")
def node_stack_poe_capability(
    poe_capabilities: Dict[str, bool]
) -> bool:
    return poe_capabilities.get("node_stack")


@pytest.fixture(scope="session")
def starting_iqagent_versions(
        enter_switch_cli: EnterSwitchCli,
        node_list: List[Node],
        logger: PytestLogger,
        nodes_data: NodesData
) -> Dict[str, str]:
    return {
        k: v["iqagent_version"] for k, v in nodes_data.items()
    }


@pytest.fixture(scope="session")
def starting_system_versions(
        enter_switch_cli: EnterSwitchCli,
        node_list: List[Node],
        logger: PytestLogger,
        nodes_data: NodesData
) -> Dict[str, str]:
    return {
        k: v["system_version"] for k, v in nodes_data.items()
    }


@pytest.fixture(scope="session")
def node_1_data(
    nodes_data: NodesData
) -> Dict[str, Any]:
    return nodes_data.get("node_1", {})


@pytest.fixture(scope="session")
def node_2_data(
    nodes_data: NodesData
) -> Dict[str, Any]:
    return nodes_data.get("node_2", {})


@pytest.fixture(scope="session")
def node_stack_data(
    nodes_data: NodesData
) -> Dict[str, Any]:
    return nodes_data.get("node_stack", {})


@pytest.fixture(scope="session")
def node_data(
    node: Node,
    nodes_data: NodesData
) -> Dict[str, Any]:
    return nodes_data.get(node.node_name, {})


@pytest.fixture(scope="session")
def get_nodes_data(
    enter_switch_cli: EnterSwitchCli,
    node_list: List[Node],
    logger: PytestLogger,
    debug: Callable
) -> Callable:
    
    @debug
    def get_nodes_data_func():
        data = defaultdict(lambda: {})

        def worker(dut: Node):
            with enter_switch_cli(dut) as dev_cmd:
                
                # get iqagent versions'
                iqagent_version = "N/A"

                if dut.cli_type.upper() == "EXOS":
                    dev_cmd.send_cmd(dut.name, 'enable iqagent')
                    time.sleep(3)
                    output = dev_cmd.send_cmd(dut.name, 'show iqagent')[0].return_text
                    logger.cli(output)
                    if iqagent_version_match := re.search(r"Version\s+\s([\d\.]+)\s+\r\n", output):
                        iqagent_version = iqagent_version_match.group(1)
                
                elif dut.cli_type.upper() == "VOSS":
                    output = dev_cmd.send_cmd(dut.name, 'show application iqagent')[0].return_text
                    logger.cli(output)
                    if iqagent_version_match := re.search(fr"Agent Version\s+:\s([\d\.]+)\r\n", output):
                        iqagent_version = iqagent_version_match.group(1)
                
                else:
                    logger.warning("OS not yet supported.")

                data[dut.node_name]["iqagent_version"] = iqagent_version

                # get system versions
                system_version = "N/A"

                if dut.cli_type.upper() == "EXOS":
                    output = dev_cmd.send_cmd(dut.name, 'show version')[0].return_text
                    logger.cli(output)
                    
                    if dut.platform.upper() == "STACK":
                        system_version = re.findall(r"(Slot-\d).*\sIMG:\s([\d\.]+)", output)
                    else:
                        system_version = re.search(r"IMG:\s([\d\.]+)", output).group(1)

                elif dut.cli_type.upper() == "VOSS":
                    output = dev_cmd.send_cmd(dut.name, 'show sys software', ignore_cli_feedback=True)[0].return_text
                    logger.cli(output)
                    system_version = re.search(r"Version\s+:\sBuild\s([\d\.]+)\s", output).group(1)
                else:
                    logger.warning("OS not yet supported.")

                data[dut.node_name]["system_version"] = system_version

                # get vritual routers
                virtual_router = "N/A"

                if dut.cli_type.upper() == "EXOS":
                    output = dev_cmd.send_cmd(
                        dut.name, 'show vlan', max_wait=10, interval=2)[0].return_text
                    logger.cli(output)
                    pattern = fr'(\w+)(\s+)(\d+)(\s+)({dut.ip})(\s+)(\/.*)(\s+)(\w+)(\s+/)(.*)(VR-\w+)'
                    match = re.search(pattern, output)
                    try:
                        virtual_router = match.group(12)
                    except:
                        pass
                
                elif dut.cli_type.upper() == "VOSS":
                    pass
                else:
                    logger.warning("OS not yet supported.")

                data[dut.node_name]["virtual_router"] = virtual_router
                
                # get poe capability
                poe = False
                
                try:
                    if dut.cli_type.lower() == "voss":
                        dev_cmd.send_cmd(
                            dut.name, 'enable', max_wait=30, interval=10)
                        dev_cmd.send_cmd(
                            dut.name, 'configure terminal', max_wait=30, interval=10)
                        result = dev_cmd.send_cmd(
                            dut.name, 'show poe-main-status', max_wait=30, interval=10)[0].return_text
                        logger.cli(result)
                        assert re.search("PoE Main Status", result)
                        assert not re.search("Device is not a POE device", result)

                    elif dut.cli_type.lower() == 'exos':
                        dev_cmd.send_cmd(dut.name, 'enable telnet')
                        dev_cmd.send_cmd(dut.name, 'disable cli paging')
                        
                        result = dev_cmd.send_cmd(
                            dut.name, 'show inline-power', max_wait=30, 
                            interval=10)[0].cmd_obj._return_text
                        logger.cli(result)
                        assert re.search('Inline Power System Information', result)
                        
                        result = dev_cmd.send_cmd(
                            dut.name, 'show inline-power info ports', max_wait=30, 
                            interval=10, ignore_cli_feedback=True)[0].cmd_obj._return_text
                        logger.cli(result)
                        assert not re.search('None of the specified ports are inline-power capable', result)

                    else:
                        assert False, "OS not yet supported."
                        
                except Exception as exc:
                    warning = f"'{dut.node_name}' node ('{dut.name}') does not support POE.\n{repr(exc)}"
                    logger.warning(warning)
                else:
                    poe = True
                
                data[dut.node_name]["poe"] = poe

                # get hostname
                hostname = "N/A"
                
                if dut.cli_type.upper() in ["EXOS", "VOSS"]:
                    output = dev_cmd.send_cmd(
                        dut.name, 'show sys-info' if dut.cli_type.upper() == "VOSS" else "show system",
                        max_wait=10, interval=2, ignore_cli_feedback=True)[0].return_text
                    if match := re.search(fr"\r\n\s*SysName\s*:\s*(.*)\r\n", output):
                        hostname = match.group(1)
                else:
                    logger.warning("OS not yet supported.")
                
                data[dut.node_name]["hostname"] = hostname

                # get ports
                ports = []
                
                if dut.cli_type.upper() == "VOSS":
                    dev_cmd.send_cmd(
                        dut.name, 'enable', max_wait=10, interval=2)
                    output = dev_cmd.send_cmd(
                        dut.name, 'show int gig int | no-more',
                        max_wait=10, interval=2)[0].return_text
                    
                    p = re.compile(r'^\d+\/\d+', re.M)
                    match_port = re.findall(p, output)

                    p2 = re.compile(r'\d+\/\d+\/\d+', re.M)
                    filtered = [port for port in match_port if not p2.match(port)]
                    ports.extend(filtered)
                
                elif dut.cli_type.upper() == "EXOS":
                    
                    dev_cmd.send_cmd(
                        dut.name, 'disable cli paging', max_wait=10, interval=2)
                    output = dev_cmd.send_cmd(
                        dut.name, 'show ports info', max_wait=20, interval=5)[0].return_text
                    p = re.compile(r'^(\d+:\d+)\s+', re.M)
                    match_port = re.findall(p, output)
                    is_stack = True
                    if len(match_port) == 0:
                        is_stack = False
                        p = re.compile(r'^(\d+)\s+', re.M)
                        match_port = re.findall(p, output)

                    p_notPresent = re.compile(r'^\d+:\d+.*NotPresent.*$', re.M) if is_stack \
                        else re.compile(r'^\d+.*NotPresent.*$', re.M)
                    parsed_info = re.findall(p_notPresent, output)

                    for port in parsed_info:
                        port_num = re.findall(p, port)
                        match_port.remove(port_num[0])
                    ports.extend(match_port)
                
                else:
                    logger.warning("OS not yet supported.")

                data[dut.node_name]["ports"] = ports
                
        threads: List[threading.Thread] = []
        try:
            for dut in node_list:
                thread = threading.Thread(target=worker, args=(dut, ))
                threads.append(thread)
                thread.start()
        finally:
            for thread in threads:
                thread.join()
        return data
    
    return get_nodes_data_func


@pytest.fixture(scope="session")
def nodes_data(
    run_options: Options,
    cached_onboarding_config: Dict[str, Dict[str, str]],
    get_nodes_data: Callable
) -> NodesData:
    
    skip_setup: bool = run_options.get("skip_setup", False)
    
    if skip_setup and cached_onboarding_config:
        return cached_onboarding_config.get("nodes", {}).get("data", {})

    return get_nodes_data()


@pytest.fixture(scope="session")
def revert_node(
    open_spawn: OpenSpawn,
    cli: Cli,
    loaded_config: Dict[str, str],
    request: fixtures.SubRequest,
    debug: Callable,
    check_devices_are_onboarded: CheckDevicesAreOnboarded, 
    check_devices_are_reachable: CheckDevicesAreReachable,
    logger: PytestLogger,
    screen: Screen
) -> Callable:
    """
    This fixture is used to easily revert the node to a specific state.
    It is useful in test cases where the node was deleted|default network policy is no longer assigned to the node.
    
    All of its kwargs are True by default which means that the function will: 
        - downgrade the iqagent on the node
        - configure the iqagent on the node
        - navigate to the Devices page
        - onboard the node
        - assign the network policy to the node
        - push the network policy to the node
    
    args:
        :xiq: the XiqLibrary object
        :node: node_1|node_2|node_stack
    kwargs:
        :downgrade_iqagent: specifies if the iqagent needs to be downgraded
        :configure_iqagent: specifies if the iqagent needs to be configured
        :navigate_to_devices: specifies if the browser needs to navigate to the Devices page
        :onboard_node: specifies if the node needs to be onboarded
        :assign_network_policy: specifies if the default network policy needs to be assigned to the node
        :push_network_policy: specifies if the network poliy needs to be pushed to the node
        :raise_error: default value is True; if raise_error is False then in case of failure the error will be caught/won't be raised
        :custom_network_policy_name: a specific network policy to be assgined or the one created in the onboarding test
        :custom_onboarding_location: a specific location to be used or the one used in the onboarding test
    """

    @debug
    def revert_node_func(
        node: Node,
        xiq: XiqLibrary,
        configure_iqagent=True,
        downgrade_iqagent=True,
        onboard_node=True,
        assign_network_policy=True,
        push_network_policy=True,
        navigate_to_devices=True,
        raise_error=True,
        custom_network_policy_name=None,
        custom_onboarding_location=None
        ):
        
        onboarding_location: str = custom_onboarding_location or request.getfixturevalue(f"{node.node_name}_onboarding_location")
        policy_name: str = custom_network_policy_name or request.getfixturevalue(f"{node.node_name}_policy_name")

        try:
            if configure_iqagent or downgrade_iqagent:
                
                logger.step(f"Check that node '{node.node_name}' is reachable.")
                check_devices_are_reachable([node])
                logger.info(f"Successfully verified that node '{node.node_name}' is reachable.")
                
                with open_spawn(node) as spawn:
                    
                    if downgrade_iqagent:
                        logger.step(f"Downgrade iqagent on node '{node.node_name}'.")
                        cli.downgrade_iqagent(node.cli_type, spawn)
                        logger.info(f"Successfully downgraded iqagent on node '{node.node_name}'.")
                        
                    if configure_iqagent:
                        logger.step(f"Configure iqagent on node '{node.node_name}'.")
                        cli.configure_device_to_connect_to_cloud(
                            node.cli_type, loaded_config['sw_connection_host'],
                            spawn, vr=node.get("mgmt_vr", 'VR-Mgmt').upper(), retry_count=30
                        )
                        logger.info(f"Successfully configured iqagent on node '{node.node_name}'.")
            
            if navigate_to_devices:
                screen.save_screen_shot()
                xiq.xflowscommonNavigator.navigate_to_devices()
                screen.save_screen_shot()
                
            xiq.xflowscommonDevices.column_picker_select("Template", "Network Policy", "MAC Address")
            screen.save_screen_shot()
            
            if onboard_node:
                node_not_onboarded = xiq.xflowscommonDevices.search_device(device_mac=node.mac, IRV=False) == -1
                
                if not node_not_onboarded and not assign_network_policy:
                    logger.step(f"Node '{node.node_name}' is already onboarded but the assign network policy flag is disabled. "
                                "Will delete the device and then it will be onboarded again without any network policy assigned.")
                    screen.save_screen_shot()
                    xiq.xflowscommonDevices.delete_device(device_mac=node.mac)
                    screen.save_screen_shot()
                    node_not_onboarded = True

                if node_not_onboarded:
                    logger.step(f"Onboard node '{node.node_name}'.")
                    screen.save_screen_shot()
                    xiq.xflowscommonDevices.onboard_device_quick({**node, "location": onboarding_location})
                    check_devices_are_onboarded(xiq, [node])
                    screen.save_screen_shot()
                    logger.info(f"Successfully onboarded node '{node.node_name}'.")
                else:
                    logger.info(f"Node '{node.node_name}' is already onboarded.")

            if assign_network_policy:
                dev = xiq.xflowscommonDevices._get_row("device_mac", node.mac)
                
                if dev != -1:
                    if not re.search(policy_name, dev.text):
                        
                        logger.step(f"Assign network policy '{policy_name}' to node '{node.node_name}'.")
                        screen.save_screen_shot()
                        assert xiq.xflowsmanageDevices.assign_network_policy_to_switch_mac(
                            policy_name=policy_name, mac=node.mac) == 1, \
                            f"Couldn't assign policy {policy_name} to device '{node}' (node: '{node.name}')."
                        screen.save_screen_shot()
                        logger.info(f"Successfully assigned network policy '{policy_name}' to node '{node.node_name}'.")
                        
                        if push_network_policy:
                            
                            logger.step(f"Push network policy '{policy_name}' to node '{node.node_name}'.")
                            screen.save_screen_shot()
                            xiq.xflowscommonDevices.get_update_devices_reboot_rollback(
                                policy_name=policy_name, option="disable", device_mac=node.mac)
                            screen.save_screen_shot()
                            xiq.xflowscommonDevices.check_device_update_status_by_using_mac(device_mac=node.mac)
                            screen.save_screen_shot()
                            logger.info(f"Successfully pushed network policy '{policy_name}' to node '{node.node_name}'.")
                            
                    else:
                        logger.info(f"The network policy '{policy_name}' is already assigned to node '{node.node_name}'.")
                else:
                    logger.info(f"Won't assign network policy '{policy_name}' to node '{node.node_name}' because the node is not found in the Devices page.")
        except:
            if raise_error:
                raise   
    return revert_node_func


@pytest.fixture(scope="session")
def configure_iqagent(
        loaded_config: Dict[str, str],
        logger: PytestLogger,
        node_list: List[Node],
        debug: Callable,
        open_spawn: OpenSpawn,
        cli: Cli,
        request: fixtures.SubRequest
) -> ConfigureIqAgent:
    """
    Fixture that configures the IQAGENT on given devices.
    """

    @debug
    def configure_iqagent_func(
            duts: List[Node]=node_list,
            ipaddress: str=loaded_config['sw_connection_host']
    ) -> None:

        def worker(dut: Node):
            
            onboarding_options: Options = request.getfixturevalue(f"{dut.node_name}_onboarding_options")
            downgrade_iqagent_flag: bool = onboarding_options.get("downgrade_iqagent", True)
            logger.info(f"The 'downgrade_iqagent' flag is '{'enabled' if downgrade_iqagent_flag else 'disabled'}' for node '{dut.node_name}'.")

            configure_iqagent_flag: bool = onboarding_options.get("configure_iqagent", True)
            logger.info(f"The 'configure_iqagent' flag is '{'enabled' if configure_iqagent_flag else 'disabled'}' for node '{dut.node_name}'.")

            if loaded_config.get("lab", "Salem").upper() != "SALEM":
                if downgrade_iqagent_flag is True:
                    logger.warning(f"iqagent won't be downgraded for node '{dut.node_name}' because lab is not 'Salem' (found lab '{loaded_config.get('lab', '')}').")
                    downgrade_iqagent_flag = False
            
            if not downgrade_iqagent_flag:
                logger.info(f"iqagent won't be downgraded because the 'downgrade_iqagent' flag is disabled for node '{dut.node_name}'.")

            if not configure_iqagent_flag:
                logger.info(f"iqagent won't be configured because the 'configure_iqagent' flag is disabled for node '{dut.node_name}'.")

            if downgrade_iqagent_flag or configure_iqagent_flag:

                with open_spawn(dut) as spawn_connection:

                    if downgrade_iqagent_flag:
                        logger.step(f"Downgrade iqagent on node '{dut.node_name}'.")
                        cli.downgrade_iqagent(dut.cli_type, spawn_connection)
                        logger.info(f"Successfully downgraded iqagent on node '{dut.node_name}'.")


                    if configure_iqagent_flag:
                        logger.step(f"Configure iqagent on node '{dut.node_name}' (XIQ ip address: '{loaded_config['sw_connection_host']}').")
                        cli.configure_device_to_connect_to_cloud(
                            dut.cli_type, loaded_config['sw_connection_host'],
                            spawn_connection, vr=dut.get("mgmt_vr", 'VR-Mgmt').upper(), retry_count=30
                        )

                        logger.info(f"Successfully configured iqagent on node '{dut.node_name}'.")

        threads: List[threading.Thread] = []

        try:
            for dut in duts:
                thread = threading.Thread(target=worker, args=(dut, ))
                threads.append(thread)
                thread.start()
        finally:
            for thread in threads:
                thread.join()
    return configure_iqagent_func


@pytest.fixture(scope="session")
def onboarding_locations(
        node_list: List[Node],
        logger: PytestLogger,
        request: fixtures.SubRequest,
        cached_onboarding_config: Dict[str, Dict[str, str]],
        run_options: Options,
        get_random_word: Callable
) -> Dict[str, str]:
    """
    Fixture that choose the onboarding location for the available nodes.
    """
    
    ret: Dict[str, str] = {}
    
    hardcoded_locations = [
        "San Jose,building_01,floor_01",
    ]

    skip_setup: bool = run_options.get("skip_setup", False)
  
    for node in node_list:
        
        node_cached_onboarding_config: Dict[str, str] = cached_onboarding_config.get("nodes", {}).get(node.node_name)
        
        if skip_setup and node_cached_onboarding_config:
            ret[node.node_name] = node_cached_onboarding_config.get("onboarding_location")
        else:
            onboarding_options: Options = request.getfixturevalue(f"{node.node_name}_onboarding_options")
            onboarding_location: str = onboarding_options.get("onboarding_location")
            create_onboarding_location: bool = onboarding_options.get("create_onboarding_location")

            if onboarding_location:
                
                if onboarding_location == "random":
                    create_onboarding_location = True
                    onboarding_location = f"Salem_{get_random_word(length=4)}," \
                                          f"Northeastern_{get_random_word(length=4)}," \
                                          f"Floor_{get_random_word(length=4)}"
                    
                logger.info(
                    f"Successfully found this location in the runlist for node '{node.node_name}': '{onboarding_location}'")
                ret[node.node_name] = onboarding_location
                
                if create_onboarding_location:
                    logger.info(
                        f"The 'create_onboarding_location' flag is set to True. The '{onboarding_location}' location"
                        f" will be created so it can be used at the onboarding of the '{node.node_name}' node."
                    )
                    if onboarding_location not in pytest.created_onboarding_locations:
                        pytest.created_onboarding_locations.append(onboarding_location)

            else:
                locations = node.get("location")
                
                if locations:
                    logger.info(f"Found location(s) attached to '{node.node_name}': '{locations}'.")
                
                if isinstance(locations, str):
                    ret[node.node_name] = locations
                    
                elif isinstance(locations, dict):
                    logger.step("Choose one of them.")
                    found_location = random.choice(list(locations.values()))
                    logger.info(f"The chosen location for '{node.node_name}' is '{found_location}'.")
                    ret[node.node_name] = found_location
                
                else:
                    logger.info(f"Did not find any location attached to '{node.node_name}'.")

                    logger.step(f"Will choose a location out of these for '{node.node_name}': {hardcoded_locations}.")
                    found_location = random.choice(hardcoded_locations)
                    logger.info(f"The chosen location for '{node.node_name}' is '{found_location}'.")
                    ret[node.node_name] = found_location
        pytest.data[f"{node.node_name}_onboarding_location"] = ret[node.node_name]
    return ret


@pytest.fixture(scope="session")
def check_devices_are_reachable(
        logger: PytestLogger,
        debug: Callable,
        wait_till: Callable
) -> CheckDevicesAreReachable:
    """
    Fixture that checks if given devices are reachable from the test automation environment.
    """
    
    windows = platform.system() == "Windows"
    
    @debug
    def check_devices_are_reachable_func(
        duts: List[Node], 
        retries: int=3, 
        step: int=1
        ) -> None:
        
        results: List[str] = []
        
        def worker(dut: Node):
            
            for _ in range(retries):
                try:
                    ping_response = subprocess.Popen(
                        ["ping", f"{'-n' if windows else '-c'} 1", dut.ip],
                        stdout=subprocess.PIPE).stdout.read().decode()
                    logger.cli(ping_response)
                    if re.search("100% loss" if windows else "100% packet loss" , ping_response):
                        wait_till(timeout=1)
                    else:
                        results.append(f"({dut.ip}): Successfully verified that this dut is reachable: '{dut.name}'.")
                        break
                except:
                    wait_till(timeout=step)
            else:
                results.append(f"({dut.ip}): This dut is not reachable: '{dut.name}.'\n{ping_response}")

        threads: List[threading.Thread] = []
        try:
            for dut in duts:
                thread = threading.Thread(target=worker, args=(dut, ))
                threads.append(thread)
                thread.start()
        finally:
            for thread in threads:
                thread.join()
        
        for message in results:
            logger.info(message)
        
        if any(re.search("This dut is not reachable", message) for message in results):
            error_msg = "Failed! Not all the duts are reachable.\n" + '\n'.join(results)
            logger.error(error_msg)
            pytest.fail(error_msg)

    return check_devices_are_reachable_func


@pytest.fixture(scope="session")
def config_helper() -> PytestConfigHelper:
    return pytest.config_helper


@pytest.fixture(scope="session", autouse=True)
def loaded_config() -> Dict[str, str]:
    
    config['${TEST_NAME}'] = "onboarding"
    config['${OUTPUT DIR}'] = os.getcwd()
    config['${MAX_CONFIG_PUSH_TIME}'] = 600
    config['${EXIT_LEVEL}'] = "test_case"

    for word in ["tenant_username", "tenant_password", "test_url"]:
        if word in config:
            config[f"${{{word.upper()}}}"] = config[word]
    return config


@pytest.fixture(scope="session")
def dev_cmd() -> NetworkElementCliSend:
    return NetworkElementCliSend()


@pytest.fixture(scope="session")
def check_devices_are_onboarded(
        logger: PytestLogger,
        node_list: List[Node],
        debug: Callable,
        wait_till: Callable
) -> CheckDevicesAreOnboarded:
    """
    Fixture that checks if the nodes are successfully onboarded.
    """
    
    @debug
    def check_devices_are_onboarded_func(
            xiq: XiqLibrary,
            node_list: List[Node] = node_list,
            timeout: int = 240
    ) -> None:
        
        xiq.xflowscommonDevices.column_picker_select("MAC Address")
        
        start_time = time.time()
        
        devices_appeared_in_xiq = False
        devices_are_online = False
        devices_are_managed = False
        stack_is_connected = False
        
        while time.time() - start_time < timeout:
            try:
                xiq.xflowsmanageDevices.refresh_devices_page()
                wait_till(timeout=5)

                if not devices_appeared_in_xiq:
                    devices, _ = wait_till(
                        func=xiq.xflowscommonDeviceCommon.get_device_grid_rows,
                        exp_func_resp=True,
                        silent_failure=True
                    )
                    assert devices, "Did not find any onboarded devices in the XIQ."

                    found_all = True
                    for dut in node_list:
                        for device in devices:
                            if any([dut.mac.upper() in device.text, dut.mac.lower() in device.text]):
                                logger.info(f"Successfully found device with mac='{dut.mac}'.")
                                break
                        else:
                            logger.warning(f"Did not find device with mac='{dut.mac}'.")
                            found_all = False
                    assert found_all, "Not all the devices were found in the Manage -> Devices menu."
                    devices_appeared_in_xiq = True

                if not devices_are_online:
                    for dut in node_list:
                        
                        device_online = xiq.xflowscommonDevices.wait_until_device_online(dut.mac)
                        assert device_online == 1, f"This device did not come online in the XIQ: {dut}."
                        logger.info(f"This device did come online in the XIQ: {dut}.")
                        
                        res = xiq.xflowscommonDevices.get_device_status(device_serial=dut.mac)
                        assert res == 'green', f"This device does not have green status in the XIQ: {dut}."
                        logger.info(f"This device does have green status in the XIQ: {dut}.")

                    devices_are_online = True

                if not stack_is_connected:
                    
                    stack_node = [n for n in node_list if n.platform.upper() == "STACK"]
                    
                    if stack_node:
                        stack_node = stack_node[0]
                        stack_status = xiq.xflowsmanageDevices.get_device_stack_status(device_mac=stack_node.mac)
                        assert stack_status == "blue", "Stack status is disconnected."
                        
                        logger.info(f"Successfully verified this stack is fully connected: {stack_node}.")                    
                        stack_is_connected = True
                        
                    else:
                        stack_is_connected = True

                if not devices_are_managed:
                    
                    for dut in node_list:
                        res = xiq.xflowscommonDevices.wait_until_device_managed(device_serial=dut.mac)
                        assert res == 1, f"The device does not appear as Managed in the XIQ; Device: {dut}."
                        logger.info(f"This device does appear as Managed in the XIQ: {dut}.")

                    devices_are_managed = True

            except Exception as err:
                logger.warning(f"Not all the devices are up yet: {repr(err)}")
                wait_till(timeout=10)
            else:
                break
        else:
            pytest.fail("Not all the devices are up in XIQ")

    return check_devices_are_onboarded_func


@pytest.fixture(scope="session")
def cleanup(
        logger: PytestLogger,
        screen: Screen, 
        debug: Callable,
        request: fixtures.SubRequest,
        utils: Utils
) -> Cleanup:
    """
    Fixture that does the cleanup in XIQ.
    """
    
    @debug
    def cleanup_func(
            xiq: XiqLibrary,
            duts: List[Node]=[],
            locations: List[str]=[], 
            network_policies: List[str]=[],
            templates_switch: List[str]=[],
    ) -> None:
            
            xiq.xflowscommonDevices._goto_devices()
            
            for dut in duts:

                logger.step(f"Delete this device: '{dut.name}' (mac='{dut.mac}').")
                
                if xiq.xflowscommonDevices.search_device(device_mac=dut.mac, IRV=False, skip_refresh=True, skip_navigation=True) == -1:
                    screen.save_screen_shot()
                    logger.info(f"Did not find this device onboarded: '{dut.name}' (mac='{dut.mac}').")
                    continue

                try:             
                    screen.save_screen_shot()
                    xiq.xflowscommonDevices._goto_devices()
                    xiq.xflowscommonDevices.delete_device(
                        device_mac=dut.mac)
                    logger.info(f"Successfully deleted this device: '{dut.name}' (mac='{dut.mac}').")
                    screen.save_screen_shot()
                except Exception as exc:
                    screen.save_screen_shot()
                    logger.warning(repr(exc))
                    
            for location in locations:
                try:
                    logger.step(f"Delete this location: '{location}'.")
                    xiq.xflowsmanageLocation.delete_location_building_floor(
                        *location.split(","))
                    logger.info(f"Successfully deleted this location: '{location}'.")
                    screen.save_screen_shot()
                except Exception as exc:
                    screen.save_screen_shot()
                    logger.warning(repr(exc))   
            
            policy_config: PolicyConfig = request.getfixturevalue("policy_config")
            for template_switch in templates_switch:
                for node_name, config in policy_config.items():
                    if config["template_name"] == template_switch:
                        try:
                            logger.step("Enable the Override Policy Common Settings option from Switch Template configuration for '{template_switch}' template.")
                            xiq.xflowsconfigureSwitchTemplate.select_sw_template(
                                config["policy_name"], template_switch, request.getfixturevalue(node_name).cli_type)
                            screen.save_screen_shot()
                            xiq.xflowsconfigureSwitchTemplate.set_override_policy_common_settings(state=True)
                            screen.save_screen_shot()
                            utils.wait_till(timeout=2)
                            xiq.xflowsconfigureSwitchTemplate.switch_template_save()
                            screen.save_screen_shot()
                            utils.wait_till(timeout=4)
                            break
                        except Exception as exc:
                            screen.save_screen_shot()
                            logger.warning(repr(exc))

            for network_policy in network_policies:
                try:
                    screen.save_screen_shot()
                    logger.step(f"Delete this network policy: '{network_policy}'.")
                    xiq.xflowsconfigureNetworkPolicy.delete_network_polices(network_policy)
                    logger.info(f"Successfully deleted this network policy: '{network_policy}'")
                    screen.save_screen_shot()
                except Exception as exc:
                    screen.save_screen_shot()
                    logger.warning(repr(exc))   
                    
            for template_switch in templates_switch:
                          
                try:
                    screen.save_screen_shot()
                    logger.step(f"Delete this switch template: '{template_switch}'.")
                    
                    xiq.xflowsconfigureCommonObjects.delete_switch_template(
                        template_switch)
                    screen.save_screen_shot()
                except Exception as exc:
                    screen.save_screen_shot()
                    logger.warning(repr(exc))
                else:
                    logger.info(f"Successfully deleted this switch template: '{template_switch}'.")
                        
    return cleanup_func


def merge_dicts(dict_1, dict_2):
    for k, v in dict_1.items():
        if k in dict_2:
            if all(isinstance(e, MutableMapping) for e in (v, dict_2[k])):
                dict_2[k] = merge_dicts(v, dict_2[k])
    dict_3 = dict_1.copy()
    dict_3.update(dict_2)
    return dict_3


@pytest.fixture(scope="session")
def configure_network_policies(
        logger: PytestLogger, 
        node_list: List[Node],
        policy_config: PolicyConfig,
        screen: Screen,
        debug: Callable,
        request: fixtures.SubRequest,
        navigator: Navigator,
        utils: Utils
) -> ConfigureNetworkPolicies:
    """
    Fixture that configures the network policies and the switch templates for the onboarded nodes.
    This fixture should be used only in the onboarding test as it is using the onboarding options of the runlist.
    """
    
    @debug
    def configure_network_policies_func(
            xiq: XiqLibrary,
            dut_config: PolicyConfig=policy_config,
    ) -> None:
        
        for node_name, data in dut_config.items():
     
            node_info = request.getfixturevalue(node_name)
            dut = node_info.name
            onb_options: Options = request.getfixturevalue(f"{node_name}_onboarding_options")
            
            logger.step(f"Configuring the network policy and switch template for dut '{dut}' (node: '{node_name}').")
            network_policy = data['policy_name']
            template_switch = data['template_name']
            model_template = data['dut_model_template']
            units_model = data['units_model']

            create_network_policy_flag = onb_options.get('create_network_policy', True)
            create_switch_template_flag = onb_options.get('create_switch_template', True)
            assign_network_policy_to_device_flag = onb_options.get('assign_network_policy_to_device', True)

            if create_network_policy_flag:
                
                logger.step(f"Create this network policy for '{dut}' dut (node: '{node_name}'): '{network_policy}'.")
                assert xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                    network_policy), \
                    f"Policy {network_policy} wasn't created successfully "
                screen.save_screen_shot()
                logger.info(f"Successfully created the network policy '{network_policy}' for dut '{dut}' (node: '{node_name}').")
                
                pytest.created_network_policies.append(network_policy)
                
                default_network_policy_onboarding_options = {
                    "dns_server_options": {
                        "status": "disable"
                    }
                }
                
                if network_policy_onboarding_options := merge_dicts(default_network_policy_onboarding_options, onb_options.get("network_policy_onboarding_options", {})):
                
                    xiq.xflowsconfigureNetworkPolicy.navigate_to_np_edit_tab(network_policy)
                    screen.save_screen_shot()
                    
                    if dns_server_options := network_policy_onboarding_options.get("dns_server_options", {}):
                        xiq.xflowsconfigureNetworkPolicy.go_to_dns_server_tab()
                        screen.save_screen_shot()
                        
                        if status := dns_server_options.get("status", "disable"):
                            xiq.xflowsconfigureNetworkPolicy.set_dns_server_status(status)
                            screen.save_screen_shot()
                            
                        xiq.xflowsconfigureNetworkPolicy.save_dns_server_tab()
                        screen.save_screen_shot()
                        
                if create_switch_template_flag:
                    
                    navigator.navigate_to_devices()
                    navigator.navigate_configure_network_policies()
                    utils.wait_till(timeout=5)
                    screen.save_screen_shot()
                    
                    logger.step(f"Create and attach this switch template to '{dut}' dut (node: '{node_name}'): '{template_switch}'.")
                    if node_name == "node_stack":
                        xiq.xflowsconfigureSwitchTemplate.add_5520_sw_stack_template(
                            units_model, network_policy,
                            model_template, template_switch, cli_type=node_info.cli_type.upper())
                        screen.save_screen_shot()
                    else:
                        xiq.xflowsconfigureSwitchTemplate.add_sw_template(
                            network_policy, model_template, template_switch, cli_type=node_info.cli_type.upper())
                        screen.save_screen_shot()
                    logger.info(
                        f"Successfully created and attached this switch template to the network policy"
                        f"'{network_policy}' of dut '{dut}' (node: '{node_name}').")
                    
                    pytest.created_switch_templates.append(template_switch)

                    if node_name == "node_stack":
                        for index in range(1, len(node_info.stack) + 1):
                            pytest.created_switch_templates.append(f"{template_switch}-{index}")

                if assign_network_policy_to_device_flag:
                    assert xiq.xflowsmanageDevices.assign_network_policy_to_switch_mac(
                        policy_name=network_policy, mac=node_info.mac) == 1, \
                        f"Couldn't assign policy {network_policy} to device '{dut}' (node: '{node_name}')."
                    
                    screen.save_screen_shot()
                    logger.info(f"Successfully assigned the network policy '{network_policy}' to dut '{dut}' (node: '{node_name}').")
                    
    return configure_network_policies_func


@pytest.fixture(scope="session")
def all_nodes() -> List[Node]:
    return pytest.all_nodes


@pytest.fixture(scope="session")
def standalone_nodes() -> List[Node]:
    return pytest.standalone_nodes


@pytest.fixture(scope="session")
def stack_nodes() -> List[Node]:
    return pytest.stack_nodes

    
@pytest.fixture(scope="session")
def policy_config(
        node_list: List[Node],
        request: fixtures.SubRequest,
        cached_onboarding_config: Dict[str, Dict[str, str]],
        get_random_word: Callable
) -> PolicyConfig:
    """
    Fixture that selects the policy name and the template name for all the nodes.
    """
    
    dut_config: PolicyConfig = defaultdict(lambda: {})
    run_options: Options = request.getfixturevalue("run_options")
    skip_setup: bool = run_options.get("skip_setup", False)

    for dut in node_list:
        
        model, units_model = generate_template_for_given_model(dut)
        node_cached_onboarding_config = cached_onboarding_config.get("nodes", {}).get(dut.node_name)
        
        if skip_setup and node_cached_onboarding_config:
            policy_name: str = node_cached_onboarding_config.get("policy_name")
            template_name: str = node_cached_onboarding_config.get("template_name")
        else:
            onboarding_options: Options = request.getfixturevalue(f"{dut.node_name}_onboarding_options")
            
            random_policy_name = f"{get_random_word(length=4)}_np_{pytest.runlist_name.replace('runlist_', '')}"[:27]
            random_template_name = f"{get_random_word(length=4)}_template_{pytest.runlist_name.replace('runlist_', '')}"[:27]
            
            policy_name: str = onboarding_options.get("policy_name", random_policy_name)
            template_name: str = onboarding_options.get("template_name", random_template_name)
        
        dut_config[dut.node_name]["policy_name"] = policy_name
        dut_config[dut.node_name]['template_name'] = template_name
        dut_config[dut.node_name]['dut_model_template'] = model
        dut_config[dut.node_name]['units_model'] = units_model

        pytest.data[f"{dut.node_name}_policy_name"] = policy_name
        pytest.data[f"{dut.node_name}_template_name"] = template_name

    return dut_config


@pytest.fixture(scope="session")
def node_1_starting_iqagent_version(
    starting_iqagent_versions: Dict[str, str]
) -> str:
    return starting_iqagent_versions.get("node_1", "")


@pytest.fixture(scope="session")
def node_1_starting_system_version(
    starting_system_versions: Dict[str, str]
) -> str:
    return starting_system_versions.get("node_1", "")


@pytest.fixture(scope="session")
def node_2_starting_iqagent_version(
    starting_iqagent_versions: Dict[str, str]
) -> str:
    return starting_iqagent_versions.get("node_2", "")


@pytest.fixture(scope="session")
def node_2_starting_system_version(
    starting_system_versions: Dict[str, str]
) -> str:
    return starting_system_versions.get("node_2", "")


@pytest.fixture(scope="session")
def node_stack_starting_iqagent_version(
    starting_iqagent_versions: Dict[str, str]
) -> str:
    return starting_iqagent_versions.get("node_stack", "")


@pytest.fixture(scope="session")
def node_stack_starting_system_version(
    starting_system_versions: Dict[str, str]
) -> List[Tuple[str, str]]:
    return starting_system_versions.get("node_stack", "")


@pytest.fixture(scope="session")
def node_1_policy_config(
        policy_config: PolicyConfig,
        node_1: Node
) -> Dict[str, str]:
    return policy_config.get("node_1", {})


@pytest.fixture(scope="session")
def node_2_policy_config(
        policy_config: PolicyConfig,
        node_2: Node
) -> Dict[str, str]:
    return policy_config.get("node_2", {})


@pytest.fixture(scope="session")
def node_stack_policy_config(
        policy_config: PolicyConfig,
        node_stack: Node
) -> Dict[str, str]:
    return policy_config.get("node_stack", {})


@pytest.fixture(scope="session")
def node_stack_model_units(
    node_stack_policy_config: Dict[str, str]
) -> str:
    return node_stack_policy_config.get("units_model", "")


@pytest.fixture(scope="session")
def node_1_onboarding_location(
        onboarding_locations: Dict[str, str],
        node_1: Node
) -> str:
    return onboarding_locations.get("node_1", "")


@pytest.fixture(scope="session")
def node_2_onboarding_location(
        onboarding_locations: Dict[str, str],
        node_2: Node
) -> str:
    return onboarding_locations.get("node_2", "")


@pytest.fixture(scope="session")
def node_stack_onboarding_location(
        onboarding_locations: Dict[str, str],
        node_stack: Node
) -> str:
    return onboarding_locations.get("node_stack", "")


@pytest.fixture(scope="session")
def xiq_version() -> str:
    return pytest.xiq_version


@pytest.fixture(scope="session")
def node_1_policy_name(
    node_1_policy_config: Dict[str, str]
) -> str:
    return node_1_policy_config.get("policy_name", "")


@pytest.fixture(scope="session")
def node_2_policy_name(
    node_2_policy_config: Dict[str, str]
) -> str:
    return node_2_policy_config.get("policy_name", "")


@pytest.fixture(scope="session")
def node_stack_policy_name(
    node_stack_policy_config: Dict[str, str]
) -> str:
    return node_stack_policy_config.get("policy_name", "")


@pytest.fixture(scope="session")
def node_1_template_name(
    node_1_policy_config: Dict[str, str]
) -> str:
    return node_1_policy_config.get("template_name", "")


@pytest.fixture(scope="session")
def node_2_template_name(
    node_2_policy_config: Dict[str, str]
) -> str:
    return node_2_policy_config.get("template_name")


@pytest.fixture(scope="session")
def node_stack_template_name(
    node_stack_policy_config: Dict[str, str]
) -> str:
    return node_stack_policy_config.get("template_name", "")


@pytest.fixture(scope="session")
def node_list(
        standalone_nodes: List[Node],
        stack_nodes: List[Node],
        all_nodes: List[Node],
        standalone_onboarding_options: Options,
        node_1_onboarding_options: Options,
        node_2_onboarding_options: Options,
        node_stack_onboarding_options: Options,
        logger: PytestLogger,
        request: fixtures.SubRequest,
        cached_onboarding_config: Dict[str, Dict[str, str]],
        run_options: Options,
        check_devices_are_reachable: CheckDevicesAreReachable
) -> List[Node]:
    """
    Fixture that selects the devices to be onboarded from the devices.yaml.
    """
    
    duts: List[Node] = []

    skip_setup: bool = run_options.get("skip_setup", False)

    if skip_setup and cached_onboarding_config:
        
        for node_name, data in {k: v for k, v in cached_onboarding_config.get("nodes", {}).items() if k != "data"}.items():
            [temp_node] = [n for n in all_nodes if n.name == data["dut_name"]]
            setattr(temp_node, "node_name", node_name)
            duts.append(temp_node)
        
        [exec(f"{var}={flag}") for var, flag in {**cached_onboarding_config.get("testbed_flags", {}), **cached_onboarding_config.get("created_items", {})}.items()]
    
    else:
        
        if pytest.onboard_2_node:

            runos_node_1 = node_1_onboarding_options.get('run_os', [])
            platform_node_1 = node_1_onboarding_options.get('platform', "standalone")
            runos_node_2 = node_2_onboarding_options.get('run_os', [])
            platform_node_2 = node_2_onboarding_options.get('platform', "standalone")

            nodes_runos_should_be: str = standalone_onboarding_options.get("nodes_runos_should_be", "random")
            nodes_platform_should_be: str = standalone_onboarding_options.get("nodes_platform_should_be", "random")
            
            # this flag specifies if the nodes must have the same cli_type: 'random'(default) or 'identical'
            logger.info(f"The 'nodes_runos_should_be' flag is set to '{nodes_runos_should_be}'.")
            
            # this flag specifies if the nodes must have the same platform: 'random'(default) or 'identical'
            logger.info(f"The 'nodes_platform_should_be' flag is set to '{nodes_runos_should_be}'.")
            
            for permutation in permutations(standalone_nodes):
                
                temp_node_1, temp_node_2 = permutation[:2]
                found_node_1, found_node_2 = False, False
                
                if runos_node_1:
                    if any(temp_node_1.cli_type.upper() == os.upper() for os in runos_node_1):
                        if (platform_node_1.lower() == "standalone") or (temp_node_1.platform.lower() == platform_node_1.lower()):
                            found_node_1 = True
                else:
                    if (platform_node_1.lower() == "standalone") or (node.platform.lower() == platform_node_1.lower()):
                        found_node_1 = True
        
                if runos_node_2:
                    if any(temp_node_2.cli_type.upper() == os.upper() for os in runos_node_2):
                        if (platform_node_2.lower() == "standalone") or (temp_node_2.platform.lower() == platform_node_2.lower()):
                            found_node_2 = True
                else:
                    if (platform_node_2.lower() == "standalone") or (temp_node_2.platform.lower() == platform_node_2.lower()):
                        found_node_2 = True

                if found_node_1 and found_node_2:
                                                        
                    if nodes_runos_should_be == "random":
                        
                        if nodes_platform_should_be == "random":
                            break
                        
                        elif nodes_platform_should_be == "identical":
                            if temp_node_1.platform.upper() == temp_node_2.platform.upper():
                                break

                    elif nodes_runos_should_be == "identical":
                        
                        if temp_node_1.cli_type.upper() != temp_node_2.cli_type.upper():
                            continue
                        
                        if nodes_platform_should_be == "random":
                            break
                        elif nodes_platform_should_be == "identical":
                            if temp_node_1.platform.upper() == temp_node_2.platform.upper():
                                break
            else:
                error_msg = f"Failed to find two standalone nodes in the testbed yaml that satisfy these requirements:\n" \
                            f"node_1: run_os={runos_node_1}, platform='{platform_node_1}'\n" \
                            f"node_2: run_os={runos_node_2}, platform='{platform_node_2}'\n" \
                            f"The 'nodes_runos_should_be' flag is set to '{nodes_runos_should_be}'.\n" \
                            f"The 'nodes_platform_should_be' flag is set to '{nodes_platform_should_be}'.\n" \
                            "Available duts in the testbed yaml file: " + ", ".join([f"{dut.name}({dut.cli_type=}, {dut.platform=})" for dut in standalone_nodes])
                logger.fail(error_msg)
            
            temp_node_1.node_name = "node_1"
            temp_node_2.node_name = "node_2"
            duts.extend([temp_node_1, temp_node_2])
            
            logger.info(
                f"Successfuly chose this dut as 'node_1': '{temp_node_1.name}' "
                f"(cli_type='{temp_node_1.cli_type}', run_os={runos_node_1}, platform='{platform_node_1}').")
                        
            logger.info(
                f"Successfuly chose this dut as 'node_2': '{temp_node_2.name}' "
                f"(cli_type='{temp_node_2.cli_type}', run_os={runos_node_2}, platform='{platform_node_2}').")
                            
        elif pytest.onboard_1_node:
            
            runos_node_1 = node_1_onboarding_options.get('run_os', [])
            platform_node_1 = node_1_onboarding_options.get('platform', "standalone")
                    
            for node in standalone_nodes:
                if runos_node_1:
                    if any(node.cli_type.upper() == os.upper() for os in runos_node_1):
                        if (platform_node_1.lower() == "standalone") or (node.platform.lower() == platform_node_1.lower()):
                            break
                else:
                    if (platform_node_1.lower() == "standalone") or (node.platform.lower() == platform_node_1.lower()):
                        break
            else:
                error_msg = f"Failed to find a standalone node in the testbed yaml that satisfy these requirements:" \
                            f" run_os={runos_node_1}, platform='{platform_node_1}'."
                logger.error(error_msg)
                pytest.fail(error_msg)

            logger.info(
                f"Successfuly chose this dut as 'node_1': '{node.name}' "
                f"(cli_type='{node.cli_type}', run_os={runos_node_1}, platform='{platform_node_1}').")

            node.node_name = "node_1"
            duts.append(node)
        
        if pytest.onboard_stack:
            runos_node_stack = node_stack_onboarding_options.get('run_os', [])
            for node in stack_nodes:
                if runos_node_stack:
                    if any(node.cli_type.upper() == os.upper() for os in runos_node_stack):
                        break
                else:
                    break
            else:
                error_msg = f"Failed to find a stack node in the testbed yaml that satisfy these requirements: run_os={runos_node_stack}."
                logger.error(error_msg)
                pytest.fail(error_msg)

            logger.info(
                f"Successfuly chose this dut as 'node_stack': '{node.name}' "
                f"(cli_type='{node.cli_type}', run_os={runos_node_stack}, platform='stack').")
            
            node.node_name = "node_stack"
            duts.append(node)   

    for dut in duts:
        pytest.data[f"{dut.node_name}_netelem_name"] = dut.name
        pytest.data[f"{dut.node_name}_cli_type"] = dut.cli_type.upper() 

    check_devices_are_reachable(duts)

    return duts


@pytest.fixture(scope="session")
def update_devices(
        logger: PytestLogger,
        node_list: List[Node],
        policy_config: PolicyConfig,
        debug: Callable,
        wait_till: Callable,
        request: fixtures.SubRequest,
        screen: Screen
) -> UpdateDevices:
    """ 
    Fixture that updates the onboarded nodes after the onboarding.
    This fixture should be used only in the onboarding test as it uses the onboarding options of each onboarded node.
    """
    
    @debug
    def update_devices_func(
            xiq: XiqLibrary,
            duts: List[Node]=node_list
    ) -> None:
        
        wait_till(timeout=5)
        xiq.xflowscommonDevices._goto_devices()
        wait_till(timeout=5)
        screen.save_screen_shot()
        
        for dut in duts:
            
            onb_options: Options = request.getfixturevalue(f"{dut.node_name}_onboarding_options")
            policy_name: str = policy_config[dut.node_name]['policy_name']
            
            create_network_policy_flag = onb_options.get('create_network_policy', True)
            assign_network_policy_to_device_flag = onb_options.get('assign_network_policy_to_device', True)
            initial_network_policy_push_flag = onb_options.get('initial_network_policy_push', True)

            if all(
                [
                    create_network_policy_flag,
                    assign_network_policy_to_device_flag,
                    initial_network_policy_push_flag
                ]
            ):
                logger.step(f"Select switch row with serial '{dut.mac}'.")
                if not xiq.xflowscommonDevices.select_device(device_mac=dut.mac):
                    screen.save_screen_shot()
                    error_msg = f"Switch '{dut.mac}' is not present in the grid."
                    logger.error(error_msg)
                    pytest.fail(error_msg)
                wait_till(timeout=2)
                
                logger.step(f"Update the switch: '{dut.mac}'.")
                if xiq.xflowscommonDevices._update_switch(update_method="PolicyAndConfig") != 1:
                    screen.save_screen_shot()
                    error_msg = f"Failed to push the update to this switch: '{dut.mac}'."
                    logger.error(error_msg)
                    pytest.fail(error_msg)
                wait_till(timeout=2)

        for dut in duts:
            
            onb_options: Options = request.getfixturevalue(f"{dut.node_name}_onboarding_options")
            policy_name = policy_config[dut.node_name]['policy_name']

            create_network_policy_flag = onb_options.get('create_network_policy', True)
            assign_network_policy_to_device_flag = onb_options.get('assign_network_policy_to_device', True)
            initial_network_policy_push_flag = onb_options.get('initial_network_policy_push', True)
            
            if all(
                [
                    create_network_policy_flag,
                    assign_network_policy_to_device_flag,
                    initial_network_policy_push_flag
                ]
            ):

                if xiq.xflowscommonDevices._check_update_network_policy_status(policy_name, dut.mac, IRV=False) != 1:
                    
                    screen.save_screen_shot()
                    logger.warning(
                        f"It looks like the update failed for this switch: '{dut.mac}'. "
                        "Will try to do a delta configuration update for this switch.")
                    
                    if xiq.xflowscommonDevices.update_device_delta_configuration(dut.mac) != 1:
                        screen.save_screen_shot()
                        logger.fail(f"Failed to do a delta confguration update for this switch: '{dut.mac}'.")
                    
                    logger.info(f"Successfully initialised a delta configuration update for this switch: '{dut.mac}'.")
                    
                    if xiq.xflowscommonDevices._check_update_network_policy_status(policy_name, dut.mac, IRV=False) != 1:
                        screen.save_screen_shot()
                        logger.fail(f"It looks like both type of device update failed for this switch: '{dut.mac}'.")

                    logger.info(f"Successfully completed the delta configuration update for this switch: '{dut.mac}'.")
                else:
                    logger.info(f"Successfully completed the network policy update for this switch: '{dut.mac}'.")

    return update_devices_func


@pytest.fixture(scope="session")
def onboarding(
        node_list: List[Node],
        logger: PytestLogger,
        screen: Screen,
        debug: Callable,
        request: fixtures.SubRequest
) -> Onboarding:
    """ This fixture should be used only in the onboarding test as it uses the onboarding options of each onboarded node.
    """
    
    @debug
    def onboarding_func(
        xiq: XiqLibrary, 
        duts: List[Node]=node_list
        ) -> None:
        
        onboarding_locations: Dict[str, str] = request.getfixturevalue("onboarding_locations")
        create_location: CreateLocation = request.getfixturevalue("create_location")
        
        for location in pytest.created_onboarding_locations:
            create_location(xiq, location)
            screen.save_screen_shot()
            
        for dut in duts:
            
            if xiq.xflowscommonDevices.onboard_device_quick({**dut, "location": onboarding_locations[dut.node_name]}) == 1: 
                logger.info(f"Successfully onboarded this device: '{dut}'.")
                screen.save_screen_shot()
            else:
                error_msg = f"Failed to onboard this device: '{dut}'."
                logger.error(error_msg)
                screen.save_screen_shot()
                pytest.fail(error_msg)
                
    return onboarding_func


def dump_data(data) -> str:
    return json.dumps(data, indent=4)


@pytest.fixture(scope="session")
def dump_switch_logs(
        enter_switch_cli: EnterSwitchCli,
        check_devices_are_reachable: CheckDevicesAreReachable,
        node_list: List[Node],
        logger: PytestLogger
) -> DumpSwitchLogs:
    
    exos_cmds = [
        "show mgmt",
        "show ssh2",
        "show iproute",
        "show system",
        "show iqagent",
        "show stacking",
        "show stacking-support",
        "show vlan",
        "show vr",
        "show virtual-network",
        "show ports info",
        "show dns-client",
        "show memory",
        "show session",
        "show cli journal"
    ]
    voss_cmds = [
        "show mgmt interface",
        "show sys-info | no-more",
        "show application iqagent",
        "show ssh session",
        "show vlan members",
        "show ip dns",
        "show int gig int | no-more",
        "show boot config flags",
        "show history",
        "show clock"
    ]

    def dump_switch_logs_func(
        duts: List[Node]=node_list
        ) -> None:
        
        def worker(dut: Node):
            try:
                check_devices_are_reachable([dut])
            except:
                logger.warning(f"'{dut.name}' is not reachable so won't dump any info for it.")
                return
        
            with enter_switch_cli(dut) as dev_cmd:
                
                if dut.cli_type.upper() == "EXOS":
                    dev_cmd.send_cmd(dut.name, "disable cli paging", max_wait=10, interval=2)
                    cmds = exos_cmds
                
                elif dut.cli_type.upper() == "VOSS":
                    dev_cmd.send_cmd(dut.name, "enable", max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, "configure terminal", max_wait=10, interval=2)
                    cmds = voss_cmds
                    
                for cmd in cmds:
                    try:
                        output = dev_cmd.send_cmd(dut.name, cmd, max_wait=10, interval=2)[0].return_text
                        logger.cli("*" * 20 + f" {dut.name}: '{cmd.upper()}' " + "*" * 20)
                        logger.cli(output)
                        logger.cli("*" * 20 + f" {dut.name}: '{cmd.upper()}' " + "*" * 20)
                    except Exception:
                        logger.warning(f"Failed to get output of this command from '{dut.name}': '{cmd}'.")
                        
        for dut in duts:
            worker(dut)

    return dump_switch_logs_func


@pytest.fixture(scope="session")
def log_options(
        request: fixtures.SubRequest,
        logger: PytestLogger,
        node_list: List[Node],
        global_settings: Dict[str, Any]
) -> None:
    """ Fixture that logs the onboarding options that are selected in the runlist yaml file.
    """
    
    for node in node_list:
        fxt: Options = request.getfixturevalue(f"{node.node_name}_onboarding_options")
        if fxt:
            logger.info(f"The onboarding options for '{node.node_name}':\n{json.dumps(fxt, indent=4)}")

    run_options: Options = request.getfixturevalue("run_options")
    if run_options:
        logger.info(f"The run options for this session: {json.dumps(run_options, indent=4)}")

    if global_settings:
        logger.info(f"The settings that will be modified in Global Settings menu of XIQ: {json.dumps(global_settings, indent=4)}")


@pytest.fixture(scope="session")
def action_chains() -> type:
    return ActionChains


@pytest.fixture(scope="session")
def get_new_action_chains(
    cloud_driver: CloudDriver,
    action_chains: type
) -> Callable[[], ActionChains]:
    return lambda: action_chains(cloud_driver.cloud_driver)


@pytest.fixture(scope="session")
def log_devices_versions(
    nodes_data: NodesData,
    logger: PytestLogger
) -> None:
    for node, values in nodes_data.items():

        logger.info(f"Node '{node}' has iqagent version '{values['iqagent_version']}'.")
        pytest.data[f"{node}_starting_iqagent_version"] = values["iqagent_version"]

        if node == "node_stack":
            for slot, version in values["system_version"]:
                logger.info(f"Node '{node}' ('{slot}') has system version '{version}'.")
                pytest.data[f"{node}_starting_system_version ('{slot}')"] = version

        else:
            logger.info(f"Node '{node}' has system version '{values['system_version']}'.")
            pytest.data[f"{node}_starting_system_version"] = values["system_version"]


@pytest.fixture(scope="session")
def devices_verifications(
    request: fixtures.SubRequest,
    debug: Callable
) -> DevicesVerifications:
    """ Fixture that verifies the devices before they are configured for the onboarding.
    """
    
    @debug
    def devices_verifications_func() -> None:

        node_list: List[Node] = request.getfixturevalue("node_list")
        check_devices_are_reachable: CheckDevicesAreReachable = request.getfixturevalue("check_devices_are_reachable")
        check_poe: CheckPoe = request.getfixturevalue("check_poe")

        check_devices_are_reachable(node_list)
        check_poe()
        
    return devices_verifications_func


@pytest.fixture(scope="session")
def devices_configuration(
    request: fixtures.SubRequest,
    debug: Callable
) -> DevicesConfiguration:
    """ Fixture that configures the devices for the onboarding.
    """
    
    @debug
    def devices_configuration_func() -> None:
        
        reset_switch: ResetSwitch = request.getfixturevalue("reset_switch")
        set_hostname: SetHostname = request.getfixturevalue("set_hostname")
        configure_iqagent: ConfigureIqAgent = request.getfixturevalue("configure_iqagent")
        node_list: List[Node] = request.getfixturevalue("node_list")

        reset_switch()
        configure_iqagent(duts=node_list)
        set_hostname()

        request.getfixturevalue("log_devices_versions")

    return devices_configuration_func


@pytest.fixture(scope="session")
def set_hostname(
    enter_switch_cli: EnterSwitchCli,
    logger: PytestLogger,
    debug: Callable,
    node_list: List[Node],
    request: fixtures.SubRequest
):

    @debug
    def set_hostname_func(
        duts: List[Node]=node_list
        ) -> None:

        def worker(dut: Node):
            
            onboarding_options: Options = request.getfixturevalue(f"{dut.node_name}_onboarding_options")

            if hostname := onboarding_options.get("hostname"):
                logger.info(f"Found field 'hostname' in runlist for node '{dut.node_name}' set to '{hostname}'.")
            elif hostname := dut.get("hostname"):
                logger.info(f"Found field 'hostname' in devices yaml for node '{dut.node_name}' ('{dut.name}') set to '{hostname}'.")
            else:
                logger.info(f"Did not find the 'hostname' field in runlist or devices yaml for node '{dut.node_name}'.")
                return
            
            logger.step(f"Set hostname to '{hostname}' for the '{dut.node_name}' node.")

            with enter_switch_cli(dut) as dev_cmd:
                if dut.cli_type.upper() == "EXOS":
                    dev_cmd.send_cmd(dut.name, f'configure snmp sysName {hostname}')
                    dev_cmd.send_cmd(
                        dut.name, 'disable iqagent', max_wait=10, interval=2,
                        confirmation_phrases='Do you want to continue?', confirmation_args='Yes')
                    dev_cmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)
                elif dut.cli_type.upper() == "VOSS":
                    dev_cmd.send_cmd(dut.name, "enable")
                    dev_cmd.send_cmd(dut.name, "configure terminal")
                    dev_cmd.send_cmd(dut.name, f"sys name {hostname}")
                    dev_cmd.send_cmd(dut.name, 'application', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'no iqagent enable', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'iqagent enable', max_wait=10, interval=2)
                else:
                    logger.warning("OS not yet supported.")

        threads: List[threading.Thread] = []

        try:
            for dut in duts:
                thread = threading.Thread(target=worker, args=(dut, ))
                threads.append(thread)
                thread.start()
        finally:
            for thread in threads:
                thread.join()

    return set_hostname_func


@pytest.fixture(scope="session")
def global_settings() -> Dict[str, Any]:
    return pytest.onboarding_options.get("global_settings", {})


@pytest.fixture(scope="session")
def account_configuration(
    request: fixtures.SubRequest,
    debug: Callable,
    global_settings: Dict[str, Any]
) -> AccountConfiguration:
    """ Fixture that configures the XIQ account at the start of the session.
    """

    @debug
    def account_configuration_func(
        xiq: XiqLibrary
    ) -> None:

        accounts = global_settings.get("accounts", {})

        administration = global_settings.get("administration", {})
        device_management_settings = administration.get("device_management_settings", {})
        viq_management = administration.get("viq_management", {})

        api = global_settings.get("api", {})
        alert_notifications = global_settings.get("alert_notifications", {})
        logs = global_settings.get("logs", {})

        if option := device_management_settings.get("change_device_management_settings", "disable"):

            change_device_management_settings: ChangeDeviceManagementSettings = request.getfixturevalue(
                "change_device_management_settings")
            
            change_device_management_settings(
                xiq,
                option=option
            )

        if option := viq_management.get("supplemental_cli_option"):
            if option in ["disable", "enable"]:
                xiq.xflowsglobalsettingsGlobalSetting.get_supplemental_cli_option(option)
    
    return account_configuration_func


@pytest.fixture(scope="session")
def pre_onboarding_verifications(
    request: fixtures.SubRequest,
    debug: Callable
) -> PreOnboardingVerifications:
    """
    Fixture that does verifications in XIQ before the onboarding.
    """

    @debug
    def pre_onboarding_verifications_func(
        xiq: XiqLibrary
    ) -> None:
         pass
     
    return pre_onboarding_verifications_func
 
    
@pytest.fixture(scope="session")
def pre_onboarding_configuration(
    request: fixtures.SubRequest,
    debug: Callable
) -> PreOnboardingConfiguration:
    """
    Fixture that prepares the XIQ account for the onboarding.
    """
    
    @debug
    def pre_onboarding_xiq_configuration_func(
        xiq: XiqLibrary
    ) -> None:
        
        cleanup: Cleanup = request.getfixturevalue("cleanup")
        node_list: List[Node] = request.getfixturevalue("node_list")
        account_configuration: AccountConfiguration = request.getfixturevalue("account_configuration")
        
        account_configuration(xiq)
        
        cleanup(
            xiq=xiq,                                      # by default pytest.created_onboarding_locations is an empty list
            duts=node_list,                               # it has elements only if there are locations specified to be created
            locations=pytest.created_onboarding_locations # in the runlist file
        )
                                                          
    return pre_onboarding_xiq_configuration_func


@pytest.fixture(scope="session")
def check_vim(
    request: pytest.FixtureRequest,
    debug: Callable,
    logger: PytestLogger,
    node_list: List[Node],
    screen: Screen
    ) -> CheckVim:
    
    @debug
    def check_vim_func(xiq):
        
        for node in node_list:
            
            onboarding_options: Options = request.getfixturevalue(f"{node.node_name}_onboarding_options")
            check_vim_flag: bool = onboarding_options.get("check_vim", False)
            
            if check_vim_flag:
                logger.step(f"The 'check_vim' flag is enabled for the '{node.node_name}' node.")
                
                try:
                    xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac)
                    screen.save_screen_shot()
                    
                    time.sleep(10)
                    assert xiq.xflowsmanageDevice360.d360_check_if_vim_is_installed()
                except AssertionError:
                    screen.save_screen_shot()
                    error = f"Invalid setup, no actual VIM module installed for chosen dut: '{node.name}' ({node.node_name})."
                    logger.error(error)
                    raise AssertionError(error)
                finally:
                    xiq.xflowsmanageDevice360.close_device360_window()

    return check_vim_func


@pytest.fixture(scope="session")
def check_poe(
    debug: Callable,
    enter_switch_cli: EnterSwitchCli, 
    logger: PytestLogger,
    request: fixtures.SubRequest,
    node_list: List[Node],
    poe_capabilities: Dict[str, bool]
) -> CheckPoe:
    
    errors: List[str] = []
    
    @debug
    def check_poe_func():
        def check_poe_worker(node: Node):
            
            onboarding_options: Options = request.getfixturevalue(f"{node.node_name}_onboarding_options")
            check_poe_flag: bool = onboarding_options.get("check_poe", False)
            
            if check_poe_flag:
                
                logger.info(f"The 'check_poe' flag is enabled for the '{node.node_name}' node ('{node.name}').")
                
                logger.step(f"Verify that the '{node.node_name}' ('{node.name}') supports POE.")

                if not poe_capabilities[node.node_name]:
                    errors.append(f"'{node.node_name}' node does not support poe")
                    return
                
                logger.info(f"'{node.node_name}' node supports poe")
                        
        threads: List[threading.Thread] = []
        
        try:
            for node in node_list:
                thread = threading.Thread(target=check_poe_worker, args=(node, ))
                threads.append(thread)
                thread.start()
        finally:
            for thread in threads:
                thread.join()

        for error in errors:
            logger.error(error)
    
        if errors:
            pytest.fail("\n".join(errors))

    return check_poe_func


@pytest.fixture(scope="session")
def post_onboarding_verifications(
    request: fixtures.SubRequest,
    debug: Callable
) -> PostOnboardingVerifications:
    """ Fixture that verifies the devices are onboarded successfully.
    """
    
    @debug
    def post_onboarding_verifications_func(
        xiq: XiqLibrary
    ) -> None:
        
        check_devices_are_onboarded: CheckDevicesAreOnboarded = request.getfixturevalue(
            "check_devices_are_onboarded")
        check_vim: CheckVim = request.getfixturevalue("check_vim")
        
        check_devices_are_onboarded(xiq)
        check_vim(xiq)

    return post_onboarding_verifications_func


@pytest.fixture(scope="session")
def post_onboarding_configuration(
    request: fixtures.SubRequest,
    debug: Callable
) -> PostOnboardingConfiguration:
    """ Fixture that does additional configuration in XIQ for the onboarded devices.
    """
    
    @debug
    def post_onboarding_configuration_func(
        xiq: XiqLibrary
    ) -> None:
                    
            update_devices: UpdateDevices = request.getfixturevalue("update_devices")
            configure_network_policies: ConfigureNetworkPolicies = request.getfixturevalue(
                "configure_network_policies")

            configure_network_policies(xiq)
            update_devices(xiq)

    return post_onboarding_configuration_func


@pytest.fixture(scope="session")
def onboarding_failure(
    request: fixtures.SubRequest, 
    debug: Callable
) -> OnboardingFailure:
    """ Fixture that is called when the onboarding fails.
    """
    
    @debug
    def onboarding_failure_func() -> None:
        
        dump_switch_logs: DumpSwitchLogs = request.getfixturevalue("dump_switch_logs")
        dump_switch_logs()
    
    return onboarding_failure_func


@pytest.fixture(scope="session")
def cached_onboarding_config(
    run_options: Options,
    logger: PytestLogger
) -> Dict[str, Dict[str, str]]:
    
    skip_setup: bool = run_options.get("skip_setup", False)
    
    if skip_setup:
        # cached onboarding config is loaded only when the skip_setup is used
        # in order for this to work, the onboarding must have been run successfully before 
        # and its config dumped into the pytest.onboarding_config file
        if os.path.exists(pytest.onboarding_config):
            with open(pytest.onboarding_config, "r") as outfile:
                if content := json.loads(outfile.read()):
                    logger.info(f"Found this onboarding configuration stored in the '{pytest.onboarding_config}' file:\n{json.dumps(content, indent=4)}")
                    return content
    return {}


@pytest.fixture(scope="session")
def store_onboarding_config(
    node_list: List[Node],
    request: fixtures.SubRequest,
    logger: PytestLogger, 
    run_options: Options,
    nodes_data: NodesData
) -> None:
    """
    This fixtures dumps the onboarding config data into the pytest.onboarding_config file at the end of the onboarding if
        -> the onboarding is successful
        -> skip_setup is not given in runlist as run_options
        -> node_list is not empty (the list of devices that were onboarded)
        
    Currently the onboarding config file has this format:
        {
            "nodes": {
                "node_1": {
                    "policy_name": "XIQ_200_np_c36wCbGU",
                    "template_name": "XIQ_200_template_s0ozQBiN",
                    "onboarding_location": "auto_location_01, Santa Clara, building_02, floor_04",
                    "dut_name": "dut2"
                },
                "node_stack": {
                    "policy_name": "XIQ_200_np_sTVm0AEs",
                    "template_name": "XIQ_200_template_qERzEBP5",
                    "onboarding_location": "auto_location_01, Santa Clara, building_02, floor_04",
                    "dut_name": "dut1"
                },
                "data": {
                    "node_stack": {
                        "iqagent_version": "0.7.1",
                        "system_version": [
                            [
                                "Slot-1",
                                "32.3.1.11"
                            ],
                            [
                                "Slot-2",
                                "32.3.1.11"
                            ]
                        ],
                        "virtual_router": "VR-Mgmt",
                        "poe": true,
                        "hostname": "Stack",
                        "ports": [
                            "1:1",
                            "1:2",
                            "1:3",
                            "1:4",
                            "1:5",
                            "1:6",
                            "1:7",
                            "1:8",
                            "1:9",
                            "1:10",
                            "1:11",
                            "1:12",
                            "1:13",
                            "1:14",
                            "1:15",
                            "1:16",
                            "1:17",
                            "1:18",
                            "1:19",
                            "1:20",
                            "1:21",
                            "1:22",
                            "1:23",
                            "1:24",
                            "1:25",
                            "1:26",
                            "1:27",
                            "1:28",
                            "1:29",
                            "1:30",
                            "1:31",
                            "1:32",
                            "1:33",
                            "1:34",
                            "1:35",
                            "1:36",
                            "1:37",
                            "1:38",
                            "1:39",
                            "1:40",
                            "1:41",
                            "1:42",
                            "1:43",
                            "1:44",
                            "1:45",
                            "1:46",
                            "1:47",
                            "1:48",
                            "1:49",
                            "1:50",
                            "1:51",
                            "1:52",
                            "2:1",
                            "2:2",
                            "2:3",
                            "2:4",
                            "2:5",
                            "2:6",
                            "2:7",
                            "2:8",
                            "2:9",
                            "2:10",
                            "2:11",
                            "2:12",
                            "2:13",
                            "2:14",
                            "2:15",
                            "2:16",
                            "2:17",
                            "2:18",
                            "2:19",
                            "2:20",
                            "2:21",
                            "2:22",
                            "2:23",
                            "2:24",
                            "2:25",
                            "2:26",
                            "2:27",
                            "2:28",
                            "2:29",
                            "2:30",
                            "2:31",
                            "2:32",
                            "2:33",
                            "2:34",
                            "2:35",
                            "2:36",
                            "2:37",
                            "2:38",
                            "2:39",
                            "2:40",
                            "2:41",
                            "2:42",
                            "2:43",
                            "2:44",
                            "2:45",
                            "2:46",
                            "2:47",
                            "2:48",
                            "2:49",
                            "2:50",
                            "2:51",
                            "2:52"
                        ]
                    },
                    "node_1": {
                        "iqagent_version": "0.7.1",
                        "system_version": "32.1.1.6",
                        "virtual_router": "VR-Mgmt",
                        "poe": true,
                        "hostname": "5420M-48W-4YE-SwitchEngine",
                        "ports": [
                            "1",
                            "2",
                            "3",
                            "4",
                            "5",
                            "6",
                            "7",
                            "8",
                            "9",
                            "10",
                            "11",
                            "12",
                            "13",
                            "14",
                            "15",
                            "16",
                            "17",
                            "18",
                            "19",
                            "20",
                            "21",
                            "22",
                            "23",
                            "24",
                            "25",
                            "26",
                            "27",
                            "28",
                            "29",
                            "30",
                            "31",
                            "32",
                            "33",
                            "34",
                            "35",
                            "36",
                            "37",
                            "38",
                            "39",
                            "40",
                            "41",
                            "42",
                            "43",
                            "44",
                            "45",
                            "46",
                            "47",
                            "48",
                            "49",
                            "50",
                            "51",
                            "52"
                        ]
                    }
                }
            },
            "testbed_flags": {
                "pytest.onboard_1_node": true,
                "pytest.onboard_2_node": false,
                "pytest.onboard_stack": true,
                "pytest.onboard_none": true
            },
            "created_items": {
                "pytest.created_onboarding_locations": [],
                "pytest.created_network_policies": [
                    "XIQ_200_np_c36wCbGU",
                    "XIQ_200_np_sTVm0AEs"
                ],
                "pytest.created_switch_templates": [
                    "XIQ_200_template_s0ozQBiN",
                    "XIQ_200_template_qERzEBP5",
                    "XIQ_200_template_qERzEBP5-1",
                    "XIQ_200_template_qERzEBP5-2"
                ]
            }
        }
    """
    
    skip_setup: bool = run_options.get("skip_setup", False)
    
    if not skip_setup and node_list:
        store = defaultdict(lambda: dict())
        
        for node in node_list:
            node_name = node.node_name
            store["nodes"][node_name] = {
                "policy_name": request.getfixturevalue(f"{node_name}_policy_name"),
                "template_name": request.getfixturevalue(f"{node_name}_template_name"),
                "onboarding_location": request.getfixturevalue(f"{node_name}_onboarding_location"),
                "dut_name": node.name
            }
        
        store["nodes"]["data"] = nodes_data

        store["testbed_flags"] = {
            f'pytest.onboard_{node}': getattr(pytest, f"onboard_{node}") for node in [tb_marker.split("testbed_")[1] for tb_marker in valid_testbed_markers]}
        
        store["created_items"] = {
            "pytest.created_onboarding_locations": pytest.created_onboarding_locations,
            "pytest.created_network_policies": pytest.created_network_policies,
            "pytest.created_switch_templates": pytest.created_switch_templates
        }
        
        content = json.dumps(store, indent=4)
        logger.step(f"Will dump this onboarding configuration in the '{pytest.onboarding_config}' file:\n{content}")
        
        with open(pytest.onboarding_config, "w") as outfile:
            outfile.write(content)


@pytest.fixture(scope="session")
def onboarding_succeeded(
    request: fixtures.SubRequest, 
    debug: Callable
) -> OnboardingSucceeded:
    """ Fixture that is called when the onboarding succeeds.
    """
    
    @debug
    def onboarding_succeeded_func(
        xiq: XiqLibrary
    ) -> None:
        request.getfixturevalue("test_bed")
        request.getfixturevalue("store_onboarding_config")
    return onboarding_succeeded_func


@pytest.fixture(scope="session")
def onboard(
        request: fixtures.SubRequest
) -> None:
    """ This fixture does the onboarding of the selected devices.
        It is called in the onboarding test ('test_xiq_onboarding').
    """
    
    logger: PytestLogger = request.getfixturevalue("logger")
    login_xiq: LoginXiq = request.getfixturevalue("login_xiq")
    
    devices_verifications: DevicesVerifications = request.getfixturevalue("devices_verifications")
    devices_configuration: DevicesConfiguration = request.getfixturevalue("devices_configuration")

    onboarding: Onboarding = request.getfixturevalue("onboarding")
    pre_onboarding_verifications: PreOnboardingVerifications = request.getfixturevalue("pre_onboarding_verifications")
    pre_onboarding_configuration: PreOnboardingConfiguration = request.getfixturevalue("pre_onboarding_configuration")
    post_onboarding_verifications: PostOnboardingVerifications = request.getfixturevalue("post_onboarding_verifications")
    post_onboarding_configuration: PostOnboardingConfiguration = request.getfixturevalue("post_onboarding_configuration")
    onboarding_succeeded: OnboardingSucceeded = request.getfixturevalue("onboarding_succeeded")
    onboarding_failure: OnboardingFailure = request.getfixturevalue("onboarding_failure")
    
    request.getfixturevalue("log_options")

    node_list: List[Node] = request.getfixturevalue("node_list")
    logger.info(f"These are the devices that will be onboarded ({len(node_list)} device(s)): " + "'" +
                '\', \''.join([dut.name for dut in node_list]) + "'.")

    onboarding_locations: Dict[str, str] = request.getfixturevalue("onboarding_locations")
    logger.info(f"These locations will be used for the onboarding:\n'{dump_data(onboarding_locations)}'")
    
    policy_config: PolicyConfig = request.getfixturevalue("policy_config")
    logger.info(f"These are the policies and switch templates that will be applied to the onboarded devices:"
                f"\n{dump_data(policy_config)}")

    try:
        
        devices_verifications()
        
        devices_configuration()

        xiq: XiqLibrary

        with login_xiq() as xiq:
            
            pre_onboarding_verifications(xiq)

            pre_onboarding_configuration(xiq)
            
            onboarding(xiq)
            
            post_onboarding_verifications(xiq)
            
            post_onboarding_configuration(xiq)
            
            onboarding_succeeded(xiq)

    except Exception as exc:
        
        logger.error(repr(exc))
        logger.error(traceback.format_exc())
        
        onboarding_failure()
        
        pytest.fail(f"The onboarding failed for these devices: {node_list}\n{traceback.format_exc()}")
    

@pytest.fixture(scope="session")
def devices_cleanup(
    request: fixtures.SubRequest,
    debug: Callable
) -> DevicesConfiguration:
    """ Fixture that unconfigures the devices in the onboarding cleanup test.
    """
    
    @debug
    def device_cleanup_func() -> None:
        
        unconfigure_iqagent: UnconfigureIqAgent = request.getfixturevalue("unconfigure_iqagent")
        node_list: List[Node] = request.getfixturevalue("node_list")

        unconfigure_iqagent(duts=node_list)

    return device_cleanup_func


@pytest.fixture(scope="session")
def unconfigure_iqagent(
        logger: PytestLogger,
        node_list: List[Node],
        debug: Callable,
        open_spawn: OpenSpawn,
        cli: Cli,
        loaded_config: Dict[str, str],
        request: fixtures.SubRequest
) -> UnconfigureIqAgent:
    """
    Fixture that unconfigures the IQAGENT on given devices.
    """

    @debug
    def unconfigure_iqagent_func(
        duts: List[Node]=node_list
    ) -> None:

        def worker(dut: Node):
            
            onboarding_options: Options = request.getfixturevalue(f"{dut.node_name}_onboarding_options")

            unconfigure_iqagent_flag: bool = onboarding_options.get("unconfigure_iqagent", True)
            logger.info(f"The 'unconfigure_iqagent' flag is '{'enabled' if unconfigure_iqagent_flag else 'disabled'}' for node '{dut.node_name}'.")

            if not unconfigure_iqagent_flag:
                logger.info(f"iqagent won't be unconfigured because the 'unconfigure_iqagent' flag is disabled for node '{dut.node_name}'.")
                return

            with open_spawn(dut) as spawn_connection:
                cli.disconnect_device_from_cloud(dut.cli_type, spawn_connection)
                logger.info(f"Successfully unconfigured iqagent on node '{dut.node_name}'.")

        threads: List[threading.Thread] = []

        try:
            for dut in duts:
                thread = threading.Thread(target=worker, args=(dut, ))
                threads.append(thread)
                thread.start()
        finally:
            for thread in threads:
                thread.join()

    return unconfigure_iqagent_func


@pytest.fixture(scope="session")
def onboard_cleanup(
    request: fixtures.SubRequest
) -> None:
    """ This fixture does the onboarding cleanup of the selected devices.
        It is called in the onboarding cleanup test ('test_xiq_onboarding_cleanup').
    """
    
    login_xiq: LoginXiq = request.getfixturevalue("login_xiq")
    stack_nodes: List[Node] = request.getfixturevalue("stack_nodes")
    cleanup: Cleanup = request.getfixturevalue("cleanup")
    devices_cleanup: DevicesCleanup = request.getfixturevalue("devices_cleanup")
    node_list: List[Node] = request.getfixturevalue("node_list")
    
    with login_xiq() as xiq:

        cleanup(
            xiq=xiq, 
            duts=node_list, 
            network_policies=pytest.created_network_policies,
            templates_switch=pytest.created_switch_templates,
            locations=pytest.created_onboarding_locations
        )

    devices_cleanup()


@pytest.fixture(scope="session")
def created_onboarding_locations() -> List[str]:
    return pytest.created_onboarding_locations


@pytest.fixture(scope="session")
def run_options() -> Options:
    return pytest.run_options


@pytest.fixture(scope="session")
def node(
    request: fixtures.SubRequest, 
    node_1: Node, 
    node_stack: Node
) -> Node:
    return node_stack or node_1


@pytest.fixture(scope="session")
def node_onboarding_location(
    node: Node,
    onboarding_locations: Dict[str, str]
) -> str:
    return onboarding_locations.get(node.node_name, "")


@pytest.fixture(scope="session")
def node_policy_config(
    node: Node,
    request: fixtures.SubRequest
) -> PolicyConfig:
    return request.getfixturevalue(f"{node.node_name}_policy_config")


@pytest.fixture(scope="session")
def node_policy_name(
    node: Node,
    request: fixtures.SubRequest
) -> str:
    return request.getfixturevalue(f"{node.node_name}_policy_config").get("policy_name", "")


@pytest.fixture(scope="session")
def node_template_name(  
    node: Node,
    request: fixtures.SubRequest
) -> str:
    return request.getfixturevalue(f"{node.node_name}_policy_config").get("template_name", "")


@pytest.fixture(scope="session")
def node_poe_capability(
    node: Node, 
    poe_capabilities: Dict[str, bool]
) -> bool:
    return poe_capabilities.get(node.node_name, False)


@pytest.fixture(scope="session")
def node_starting_iqagent_version(
    node: Node, 
    starting_iqagent_versions: Dict[str, str]
) -> str:
    return starting_iqagent_versions.get(node.node_name, "")


@pytest.fixture(scope="session")
def node_starting_system_version(
    node: Node, 
    starting_system_versions: str
) -> str: 
    return starting_system_versions.get(node.node_name, "")


@pytest.fixture(scope="session")
def node_model_units(
    node_policy_config: Dict[str, str]
) -> str:
    return node_policy_config.get("units_model", "")


@pytest.fixture(scope="session")
def node_1(
        request: fixtures.SubRequest,
) -> Node:
    if pytest.onboard_1_node or pytest.onboard_2_node:
        node_list: List[Node] = request.getfixturevalue("node_list")
        return [dut for dut in node_list if dut.node_name == "node_1"][0]
    return {}


@pytest.fixture(scope="session")
def node_1_ports(
    node_1_data: Dict[str, Any]
) -> List[str]:
    return node_1_data.get("ports", [])


@pytest.fixture(scope="session")
def node_2_ports(
    node_2_data: Dict[str, Any]
) -> List[str]:
    return node_2_data.get("ports", [])


@pytest.fixture(scope="session")
def node_stack_ports(
    node_stack_data: Dict[str, Any]
) -> List[str]:
    return node_stack_data.get("ports", [])


@pytest.fixture(scope="session")
def node_hostname(
    node_data: Dict[str, Any]
) -> str:
    return node_data.get("hostname", "")


@pytest.fixture(scope="session")
def node_1_hostname(
    node_1_data: Dict[str, Any]
) -> str:
    return node_1_data.get("hostname", "")


@pytest.fixture(scope="session")
def node_2_hostname(
    node_2_data: Dict[str, Any]
) -> str:
    return node_2_data.get("hostname", "")


@pytest.fixture(scope="session")
def node_stack_hostname(
    node_stack_data: Dict[str, Any]
) -> str:
    return node_stack_data.get("hostname", "")


@pytest.fixture(scope="session")
def node_ports(
    node_data: Dict[str, Any]
) -> List[str]:
    return node_data.get("ports", [])


@pytest.fixture(scope="session")
def standalone_onboarding_options(
) -> Options:
    return pytest.onboarding_options.get("standalone", {})


@pytest.fixture(scope="session")
def node_1_onboarding_options(
) -> Options:
    return pytest.onboarding_options.get("standalone", {}).get("node_1", {})


@pytest.fixture(scope="session")
def node_2_onboarding_options(
) -> Options:
    return pytest.onboarding_options.get("standalone", {}).get("node_2", {})


@pytest.fixture(scope="session")
def node_stack_onboarding_options(
) -> Options:
    return pytest.onboarding_options.get("node_stack", {})


@pytest.fixture(scope="session")
def node_2(
        request: fixtures.SubRequest,
) -> Node:
    if pytest.onboard_2_node:
        node_list: List[Node] = request.getfixturevalue("node_list")
        return [dut for dut in node_list if dut.node_name == "node_2"][0]
    return {}


@pytest.fixture(scope="session")
def node_stack(
        request: fixtures.SubRequest,
) -> Node:
    if pytest.onboard_stack:
        node_list: List[Node] = request.getfixturevalue("node_list")
        return [dut for dut in node_list if dut.node_name == "node_stack"][0]
    return {}

 
@pytest.fixture(scope="session")
def dut_ports(
    nodes_data: NodesData,
    request: fixtures.SubRequest
) -> Dict[str, List[str]]:
    return {request.getfixturevalue(n).name: values["ports"] for n, values in nodes_data.items()}


@pytest.fixture(scope="session")
def bounce_iqagent(
        enter_switch_cli: EnterSwitchCli,
        debug: Callable
) -> BounceIqagent:

    @debug
    def bounce_iqagent_func(
            dut: Node,
            xiq: XiqLibrary=None,
            wait: bool=False
    ) -> None:
        
        with enter_switch_cli(dut) as dev_cmd:
            if dut.cli_type.upper() == "EXOS":
                dev_cmd.send_cmd(
                    dut.name, 'disable iqagent', max_wait=10, interval=2,
                    confirmation_phrases='Do you want to continue?',
                    confirmation_args='Yes')
                dev_cmd.send_cmd(
                    dut.name, 'enable iqagent', max_wait=10, interval=2)
        
            elif dut.cli_type.upper() == "VOSS":
                dev_cmd.send_cmd(dut.name, 'enable', max_wait=10, interval=2)
                dev_cmd.send_cmd(
                    dut.name, 'configure terminal', max_wait=10, interval=2)
                dev_cmd.send_cmd(
                    dut.name, 'application', max_wait=10, interval=2)
                dev_cmd.send_cmd(
                    dut.name, 'no iqagent enable', max_wait=10, interval=2)
                dev_cmd.send_cmd(
                    dut.name, 'iqagent enable', max_wait=10, interval=2)
        
        if wait is True and xiq is not None:
            xiq.xflowscommonDevices.wait_until_device_online(dut.mac)
    
    return bounce_iqagent_func


@pytest.fixture(scope="session")
def reboot_device(
        node_list: List[Node],
        enter_switch_cli: EnterSwitchCli,
        logger: PytestLogger,
        debug: Callable,
        wait_till: Callable
) -> RebootDevice:

    @debug
    def reboot_device_func(
            duts: List[Node]=node_list
    ) -> None:
        
        def worker(dut: Node):
            with enter_switch_cli(dut) as dev_cmd:
                try:
                    
                    if dut.cli_type.upper() == "EXOS":
                        dev_cmd.send_cmd(
                            dut.name, 'reboot all', max_wait=10, interval=2,
                            confirmation_phrases='Are you sure you want to reboot the switch?',
                            confirmation_args='y'
                        )
                    elif dut.cli_type.upper() == "VOSS":
                        dev_cmd.send_cmd(dut.name, 'reset -y', max_wait=10, interval=2)
                        
                    elif dut.cli_type.upper() == "AH-FASTPATH":
                        try:
                            dev_cmd.send_cmd(dut.name, "enable")
                        except:
                            dev_cmd.send_cmd(dut.name, "exit")
                            
                        dev_cmd.send_cmd(
                            dut.name, 'reload', max_wait=10, interval=2,
                            confirmation_phrases='Would you like to save them now? (y/n)', confirmation_args='y'
                        )
                except Exception as exc:
                    error_msg = f"Failed to reboot this dut: '{dut.name}'\n{repr(exc)}"
                    logger.error(error_msg)
                    wait_till(timeout=5)
                    pytest.fail(error_msg)
                else:
                    wait_till(timeout=120)
    
        threads: List[threading.Thread] = []
        try:
            for dut in duts:
                thread = threading.Thread(target=worker, args=(dut, ))
                threads.append(thread)
                thread.start()
        finally:
            for thread in threads:
                thread.join()
    return reboot_device_func


@pytest.fixture(scope="session")
def reboot_stack_unit(
        wait_till: Callable,
        enter_switch_cli: EnterSwitchCli,
        debug: Callable,
        logger: PytestLogger
) -> RebootStackUnit:
    
    @debug
    def reboot_stack_unit_func(
            dut: Node,
            slot: int = 1,
            save_config: str = 'n'
    ) -> None:
        
        if not (dut.platform.upper() == "STACK" and dut.cli_type.upper() == "EXOS"):
            error = f"Given device is not an EXOS stack: '{dut}'"
            logger.error(error)
            pytest.fail(error)

        with enter_switch_cli(dut) as dev_cmd:
            try:
                dev_cmd.send_cmd(
                    dut.name, f'reboot slot {slot}', max_wait=10, interval=2,
                    confirmation_phrases='Do you want to save configuration changes to currently selected configuration',
                    confirmation_args=save_config
                )
            except Exception as exc:
                error_msg = f"Failed to reboot slot '{slot}' of dut: '{dut.name}'\n{repr(exc)}"
                logger.error(error_msg)
                pytest.fail(error_msg)
            else:
                wait_till(timeout=120)
    return reboot_stack_unit_func


@pytest.fixture(scope="session")
def get_stack_slots(
        logger: PytestLogger,
        enter_switch_cli: EnterSwitchCli,
        debug: Callable
) -> GetStackSlots:
    
    @debug
    def get_stack_slots_func(
            dut: Node
    ) -> Dict[str, Dict[str, str]]:
        
        if not (dut.platform.upper() == "STACK" and dut.cli_type.upper() == "EXOS"):
            error = f"Given device is not an EXOS stack: '{dut}'"
            logger.error(error)
            pytest.fail(error)

        slots_info = {}
        with enter_switch_cli(dut) as dev_cmd:
            output = dev_cmd.send_cmd(dut.name, 'show stacking', max_wait=10, interval=2)[0].return_text
            logger.cli(output)
            rows = re.findall(r'((?:[0-9a-fA-F]:?){12})\s+(\d+)\s+(\w+)\s+(\w+)\s+(.*)\r\n', output, re.IGNORECASE)
            
            for row in rows:
                slots_info[row[1]] = dict(zip(["Node MAC Address", "Slot", "Stack State", "Role", "Flags"], row))
            logger.info(f"Found these slots on the stack device '{dut.name}': {dump_data(slots_info)}.")
            return slots_info
    return get_stack_slots_func


@pytest.fixture(scope="session")
def modify_stacking_node(
        enter_switch_cli: EnterSwitchCli,
        reboot_device: RebootDevice,
        debug: Callable,
        logger: PytestLogger
) -> ModifyStackingNode:
    
    @debug
    def modify_stacking_node_func(
            dut: Node,
            node_mac_address: str,
            op: str
    ) -> None:
        if not (dut.platform.upper() == "STACK" and dut.cli_type.upper() == "EXOS"):
            error = f"Given device is not an EXOS stack: '{dut}'"
            logger.error(error)
            pytest.fail(error)

        assert op in ["enable", "disable"], "Op argument should be 'enable' or 'disable'"
        
        with enter_switch_cli(dut) as dev_cmd:
            cmd = f"{op} stacking node-address {node_mac_address}"
            dev_cmd.send_cmd(dut.name, cmd, max_wait=10, interval=2)
        
        reboot_device(dut)
    return modify_stacking_node_func


@pytest.fixture(scope="session")
def set_lldp(
        enter_switch_cli: EnterSwitchCli,
        debug: Callable
) -> SetLldp:
    
    @debug
    def set_lldp_func(
            dut: Node,
            ports: List[str],
            action: str = "enable"
    ) -> None:
        
        with enter_switch_cli(dut) as dev_cmd:
            if dut.cli_type.upper() == "EXOS":
                if action == "enable":
                    dev_cmd.send_cmd(dut.name, 'enable cdp ports all', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'enable edp ports all', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'enable lldp ports all', max_wait=10, interval=2)
                elif action == "disable":
                    dev_cmd.send_cmd(dut.name, 'disable cdp ports all', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'disable edp ports all', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'disable lldp ports all', max_wait=10, interval=2)

            elif dut.cli_type.upper() == "VOSS":
                dev_cmd.send_cmd(dut.name, "enable", max_wait=10, interval=2)
                dev_cmd.send_cmd(dut.name, "configure terminal", max_wait=10, interval=2)
                dev_cmd.send_cmd(
                    dut.name, f"interface gigabitEthernet {ports[0]}-{ports[-1]}", max_wait=10, interval=2)
                cmd_action = f"lldp port {ports[0]}-{ports[-1]} cdp enable"
                if action == "enable":
                    dev_cmd.send_cmd(dut.name, "no auto-sense enable", max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, "no fa enable", max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, cmd_action, max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, "fa enable", max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, "auto-sense enable", max_wait=10, interval=2)
                elif action == "disable":
                    dev_cmd.send_cmd(dut.name, "no " + cmd_action, max_wait=10, interval=2)
    return set_lldp_func


@pytest.fixture(scope="session")
def clear_traffic_counters(
        enter_switch_cli: EnterSwitchCli,
        debug: Callable
) -> ClearTrafficCounters:
    
    @debug
    def clear_traffic_counters_func(
        dut: Node,
        *ports: List[str]
        ) -> None:
        with enter_switch_cli(dut) as dev_cmd:
            if dut.cli_type.upper() == "EXOS":
                    dev_cmd.send_cmd(
                    dut.name, f"clear counters ports {','.join(ports)}", max_wait=10, interval=2)
            elif dut.cli_type.upper() == "VOSS":
                dev_cmd.send_cmd(
                    dut.name, f"clear-stats port {','.join(ports)}", max_wait=10, interval=2)
    return clear_traffic_counters_func


@pytest.fixture(scope="session")
def change_device_management_settings(
        logger: PytestLogger, 
        standalone_nodes: List[Node], 
        stack_nodes: List[Node], 
        screen: Screen, 
        debug: Callable, 
        wait_till: Callable
) -> ChangeDeviceManagementSettings:
    
    @debug
    def change_device_management_settings_func(
            xiq: XiqLibrary,
            option: str,
            retries: int=5,
            step: int=5
    ) -> None:

        for _ in range(retries):
            try:
                xiq.xflowsglobalsettingsGlobalSetting.change_device_management_settings(option=option)

                screen.save_screen_shot()
            except Exception as exc:
                logger.warning(repr(exc))
                screen.save_screen_shot()
                wait_till(timeout=step)
            else:
                xiq.xflowscommonNavigator.navigate_to_devices()
                break
        else:
            pytest.fail("Failed to change device management settings.")
    return change_device_management_settings_func


@pytest.fixture(scope="session")
def sw_connection_host(
    loaded_config: Dict[str, str]
) -> str:
    return loaded_config.get("sw_connection_host", "")


@pytest.fixture(scope="session")
def dut1(
        config_helper: PytestConfigHelper,
        logger: PytestLogger
) -> Node:
    try:
        return getattr(config_helper, "dut1")
    except AttributeError:
        logger.error(f"The testbed does not have the 'dut1' netelem.")
        return {}


@pytest.fixture(scope="session")
def dut2(
        config_helper: PytestConfigHelper,
        logger: PytestLogger
) -> Node:
    try:
        return getattr(config_helper, "dut2")
    except AttributeError:
        logger.error(f"The testbed does not have the 'dut2' netelem.")
        return {}


@pytest.fixture(scope="session")
def dut3(
        config_helper: PytestConfigHelper, 
        logger: PytestLogger
) -> Node:
    try:
        return getattr(config_helper, "dut3")
    except AttributeError:
        logger.error(f"The testbed does not have the 'dut3' netelem.")
        return {}
    

@pytest.fixture(scope="session")
def dut4(
        config_helper: PytestConfigHelper, 
        logger: PytestLogger
) -> Node:
    try:
        return getattr(config_helper, "dut4")
    except AttributeError:
        logger.error(f"The testbed does not have the 'dut4' netelem.")
        return {}


@pytest.fixture(scope="session")
def dut5(
        config_helper: PytestConfigHelper, 
        logger: PytestLogger
) -> Node:
    try:
        return getattr(config_helper, "dut5")
    except AttributeError:
        logger.error(f"The testbed does not have the 'dut5' netelem.")
        return {}


@pytest.fixture(scope="session")
def reset_utils() -> NetworkElementResetDeviceUtilsKeywords:
    return NetworkElementResetDeviceUtilsKeywords()


@pytest.fixture(scope="session")
def network_manager() -> NetworkElementConnectionManager:
    return NetworkElementConnectionManager()


@pytest.fixture(scope="session")
def screen() -> Screen:
    return Screen()


@pytest.fixture(scope="session")
def navigator() -> Navigator:
    return Navigator()


@pytest.fixture(scope="session")
def rest() -> Rest:
    return Rest()


@pytest.fixture(scope="session")
def weh() -> WebElementHandler:
    return WebElementHandler()


@pytest.fixture(scope="session")
def wec() -> WebElementController:
    return WebElementController()


@pytest.fixture(scope="session")
def tshark() -> Tshark:
    return Tshark()


@pytest.fixture(scope="session")
def utils() -> Utils:
    return Utils()


@pytest.fixture(scope="session")
def wait_till(utils: Utils) -> Callable:
    return utils.wait_till


@pytest.fixture(scope="session")
def cloud_driver() -> CloudDriver:
    return CloudDriver()


@pytest.fixture(scope="session")
def cloud_driver_capabilities(
    cloud_driver: CloudDriver
) -> Dict[str, Union[str, Dict[str, Union[str, int, bool]]]]:
    return getattr(cloud_driver.cloud_driver, "capabilities", {})


@pytest.fixture(scope="session")
def auto_actions() -> AutoActions:
    return AutoActions()


@pytest.fixture(scope="session")
def get_random_word() -> Callable:
    def get_random_word_func(**kwargs) -> str:
        
        pool: List[str] = []
        length = kwargs.pop("length", 6)
        punctuation = kwargs.pop("punctuation", False)
        
        if punctuation:
            pool.extend(list(string.punctuation))
            
        for item in ["ascii_lowercase", "ascii_uppercase", "digits"]:
            if kwargs.get(item, True):
                pool.extend(list(getattr(string, item)))
                
        word = ''.join(random.choice(pool) for _ in range(length))
        return word
    return get_random_word_func


def add_switch_template_to_teardown(switch_template: str) -> None:
    pytest.created_switch_templates.append(switch_template)


def add_network_policy_to_teardown(network_policy: str) -> None:
    pytest.created_network_policies.append(network_policy)


def add_onboarding_location_to_teardown(onboarding_location: str) -> None:
    pytest.created_onboarding_locations.append(onboarding_location)


@pytest.fixture(scope="session")
def update_test_name(
    loaded_config: Dict[str, str]
    ) -> Callable[[str], None]:
    def func(test_name: str):
        loaded_config['${TEST_NAME}'] = test_name
    return func


@pytest.fixture(scope="session")
def update_pytest_config(
    loaded_config: Dict[str, str]
) -> Callable[[str], None]:
    def func(key: str, value: str):
        loaded_config[f'{key}'] = value
    return func


@pytest.fixture(scope="session")
def default_library() -> DefaultLibrary:
    return DefaultLibrary()


@pytest.fixture(scope="session")
def udks() -> Udks:
    return Udks()

@pytest.fixture(scope="session")
def network_360_monitor_elements() -> Network360MonitorElements:
    return Network360MonitorElements()

@pytest.fixture(scope="session")
def netelem_listutils() -> NetworkElementListUtils:
    return NetworkElementListUtils()


@pytest.fixture(scope="session")
def client_web_elements() -> ClientWebElements:
    return ClientWebElements()


@pytest.fixture(scope="session")
def poll(debug, logger):
    """
    The poll function will rerun a function until some conditions are met.
    If the conditions are not met in given time then the poll will raise TimeoutError.
    
    e.g.:
    
        def test_(self, poll, ...):
        
            def get_status():
                return random.choice(["green", "yellow", "red", "blue"])
            
            for status in poll(get_status, max_poll_retries=10, poll_interval=1):
                if status == "green":
                    logger.info("Status is green")
                    break
            
            # the poll will execute the get_status function 10 times with a 4 seconds pause between each run
            # if the status variable is "green" then the poll will end
            # if the status variable is not green after 10 runs then the poll will raise TimeoutError

    """
    
    @debug
    def poll_func(caller, *args, **kwargs):
        
        poll_interval = kwargs.pop("poll_interval", 30)
        max_poll_retries = kwargs.pop("max_poll_retries", None)
        max_poll_time = kwargs.pop("max_poll_time", None)
        verbose = kwargs.pop("verbose", True)
        
        if not max_poll_retries and not max_poll_time:
            raise ValueError("max_poll_retries or max_poll_time must be provided")
        
        if not max_poll_retries and max_poll_time:
            max_poll_retries = max_poll_time // poll_interval
        
        max_poll_time = max_poll_time or (max_poll_retries * poll_interval)
        
        exception = kwargs.pop('exception', Exception)
        re_raise = kwargs.pop('re_raise', False)
        
        verbose and logger.step(f"Poller initiated with caller: {caller.__name__} | args: {args} | kwargs: {kwargs}")

        retries = 0
        start_time = time.time()
        
        while retries < max_poll_retries and (time.time() - start_time) < max_poll_time:
            try:
                verbose and logger.info(f"Retry# {retries + 1}")
                output = caller(*args, **kwargs)
                verbose and logger.info(f"Poller received output - \n {output}")
                yield output
            except exception as error:
                verbose and logger.error("Poller received exception")
                if re_raise:
                    verbose and logger.info(f"re_raise flag is enabled, raising the exception")
                    logger.error(repr(error))
                    raise error
            verbose and logger.info(f"Poller sleeping for {poll_interval} seconds")
            time.sleep(poll_interval)
            retries += 1
        
        verbose and logger.error(
            f"Poller timedout with caller: {caller.__name__} | retries: {retries} | polltime(secs): {round(time.time() - start_time, 2)}")
        raise TimeoutError(f"Poller timedout with retries: {retries} | Poller ended after {round(time.time() - start_time, 2)} seconds")
    return poll_func


def _retry(caller, exception, max_retries, retry_interval, max_retry_time, verbose, *args, **kwargs):

    retries = 0
    start = time.time()
    interval = retry_interval
    
    verbose and logger_obj.step(f"Retry initiated with caller: {caller.__name__} | args: {args} | kwargs: {kwargs}")
    
    while True:
        try:
            verbose and logger_obj.info(f"Retry# {retries + 1}")
            return caller(*args, **kwargs)
        except exception as error:
            verbose and logger_obj.warning(f"retry received exception - \n {repr(error)}")
            
            retries += 1
        
            if max_retries >= 0 and retries == max_retries:
                logger_obj.error(f"Retry reached max retries limit: {max_retries} for caller: {caller.__name__}")
                raise error
            
            if max_retry_time and max_retry_time < (time.time() - start):
                logger_obj.error(f"Retry reached max retry time limit: {max_retry_time} for caller: {caller.__name__}")
                raise error
            
            verbose and logger_obj.info(f"Retry sleeping for {interval} seconds")
            time.sleep(interval)

        except Exception as error:
            raise error


@pytest.fixture(scope="session")
def retry():
    """
    The retry decorator will rerun a function until the given error is not raised anymore.
    
    e.g.:
    
        def test_(self, retry, ...):

            count = 0
            
            @retry(exception=KeyError, retry_interval=1, max_retries=10)
            def func():
                global count
                if count < 3:
                    count += 1                
                    raise KeyError("KeyError")

            func() # the func will run maximum 10 times with a one second pause between each run 
                   # for the first 3 runs the retry will catch the KeyError exception raised by func
                   # because the 4th run does not raise the KeyError exception-> the retry will end
    """
    
    def retry_func(exception=Exception, max_retries=5, retry_interval=10, max_retry_time=None, verbose=True):
        def retry_decorator(caller):
            def retry_wrapper(*args, **kwargs):
                return _retry(caller, exception, max_retries, retry_interval, max_retry_time, verbose, *(args or []), **(kwargs or {}))
            return retry_wrapper
        return retry_decorator
    return retry_func


class Testbed(metaclass=Singleton):
    
    def __init__(
        self, 
        request: fixtures.SubRequest
    ) -> None:
        
        self.request: fixtures.SubRequest = request
        self.logger: PytestLogger = request.getfixturevalue("logger")
        self.config: Dict[str, Union[str, Dict[str, str]]] = request.getfixturevalue("loaded_config")
        self.run_options: Options = request.getfixturevalue("run_options")
        
        self.all_nodes: List[Node] = request.getfixturevalue("all_nodes")
        self.standalone_nodes: List[Node] = request.getfixturevalue("standalone_nodes")
        self.node_list: List[Node] = request.getfixturevalue("node_list")
        self.stack_nodes: List[Node] = request.getfixturevalue("stack_nodes")
        self.node_1: Node = request.getfixturevalue("node_1")
        self.node_2: Node = request.getfixturevalue("node_2")
        self.node_stack: Node = request.getfixturevalue("node_stack")
        self.node: Node = request.getfixturevalue("node")
        self.nodes_data: NodesData = request.getfixturevalue("nodes_data")

        self.username: str = self.config.get("tenant_username")
        self.password: str = self.config.get("tenant_password")
        self.test_url: str = self.config.get("test_url")
        self.sw_connection_host: str = request.getfixturevalue("sw_connection_host")
        self.xiq_version: str = request.getfixturevalue("xiq_version")
        self.cloud_driver_capabilities: Dict[str, Union[str, Dict[str, Union[str, int, bool]]]] = request.getfixturevalue("cloud_driver_capabilities")

        self.dut_1: Node = request.getfixturevalue("dut1")
        self.dut_2: Node = request.getfixturevalue("dut2")
        self.dut_3: Node = request.getfixturevalue("dut3")
        self.dut_4: Node = request.getfixturevalue("dut4")
        self.dut_5: Node = request.getfixturevalue("dut5")

        self.node_1_onboarding_options: Options = request.getfixturevalue("node_1_onboarding_options")
        self.node_2_onboarding_options: Options = request.getfixturevalue("node_2_onboarding_options")
        self.node_stack_onboarding_options: Options = request.getfixturevalue("node_stack_onboarding_options")
        self.standalone_onboarding_options: Options = request.getfixturevalue("standalone_onboarding_options")

        self.onboarding_locations: Dict[str, str] = request.getfixturevalue("onboarding_locations")
        self.node_1_onboarding_location: str = request.getfixturevalue("node_1_onboarding_location")
        self.node_2_onboarding_location: str = request.getfixturevalue("node_2_onboarding_location")
        self.node_stack_onboarding_location: str = request.getfixturevalue("node_stack_onboarding_location")
        self.node_onboarding_location: str = request.getfixturevalue("node_onboarding_location")
        self.created_onboarding_locations: List[str] = request.getfixturevalue("created_onboarding_locations")
   
        self.starting_iqagent_versions: Dict[str, str] = request.getfixturevalue("starting_iqagent_versions")
        self.node_1_starting_iqagent_version: str = request.getfixturevalue("node_1_starting_iqagent_version")
        self.node_2_starting_iqagent_version: str = request.getfixturevalue("node_2_starting_iqagent_version")
        self.node_stack_starting_iqagent_version: str = request.getfixturevalue("node_stack_starting_iqagent_version")
        self.node_starting_iqagent_version: str = request.getfixturevalue("node_starting_iqagent_version")

        self.starting_system_versions: Dict[str, str] = request.getfixturevalue("starting_system_versions")
        self.node_1_starting_system_version: str = request.getfixturevalue("node_1_starting_system_version")
        self.node_2_starting_system_version: str = request.getfixturevalue("node_2_starting_system_version")
        self.node_stack_starting_system_version: List[Tuple[str, str]] = request.getfixturevalue("node_stack_starting_system_version")
        self.node_starting_system_version: str = request.getfixturevalue("node_starting_system_version")

        self.policy_config: PolicyConfig = request.getfixturevalue("policy_config")
        self.node_1_policy_config: Dict[str, str] = request.getfixturevalue("node_1_policy_config")
        self.node_2_policy_config: Dict[str, str] = request.getfixturevalue("node_2_policy_config")
        self.node_policy_config: Dict[str, str] = request.getfixturevalue("node_policy_config")
        self.node_stack_policy_config: Dict[str, str] = request.getfixturevalue("node_stack_policy_config")
        
        self.node_1_policy_name: str = request.getfixturevalue("node_1_policy_name")
        self.node_2_policy_name: str = request.getfixturevalue("node_2_policy_name")
        self.node_stack_policy_name: str = request.getfixturevalue("node_stack_policy_name")
        self.node_policy_name: str = request.getfixturevalue("node_policy_name")
        
        self.node_1_template_name: str = request.getfixturevalue("node_1_template_name")
        self.node_2_template_name: str = request.getfixturevalue("node_2_template_name")
        self.node_stack_template_name: str = request.getfixturevalue("node_stack_template_name")
        self.node_template_name: str = request.getfixturevalue("node_template_name")
        self.node_stack_model_units: str = request.getfixturevalue("node_stack_model_units")
        self.node_model_units: str = request.getfixturevalue("node_model_units")
        self.virtual_routers: Dict[str, str] = request.getfixturevalue("virtual_routers")

        self.node_1_ports: List[str] = request.getfixturevalue("node_1_ports")
        self.node_2_ports: List[str] = request.getfixturevalue("node_2_ports")
        self.node_stack_ports: List[str] = request.getfixturevalue("node_stack_ports")
        self.node_ports: List[str] = request.getfixturevalue("node_ports")
        
        self.node_hostname: str = request.getfixturevalue("node_hostname")
        self.node_1_hostname: str = request.getfixturevalue("node_1_hostname")
        self.node_2_hostname: str = request.getfixturevalue("node_2_hostname")
        self.node_stack_hostname: str = request.getfixturevalue("node_stack_hostname")
        
        self.poe_capabilities: Dict[str, bool] = request.getfixturevalue("poe_capabilities")
        self.node_1_poe_capability: bool = request.getfixturevalue("node_1_poe_capability")
        self.node_2_poe_capability: bool = request.getfixturevalue("node_2_poe_capability")
        self.node_stack_poe_capability: bool = request.getfixturevalue("node_stack_poe_capability")
        self.node_poe_capability: bool = request.getfixturevalue("node_poe_capability")
        
        self.network_manager: NetworkElementConnectionManager = request.getfixturevalue("network_manager")
        self.cli: Cli = request.getfixturevalue("cli")
        self.auto_actions: AutoActions = request.getfixturevalue("auto_actions")
        self.screen: Screen = request.getfixturevalue("screen")
        self.navigator: Navigator = request.getfixturevalue("navigator")
        self.utils: Utils = request.getfixturevalue("utils")
        self.default_library: DefaultLibrary = request.getfixturevalue("default_library")
        self.udks: Udks = request.getfixturevalue("udks")
        self.cloud_driver: CloudDriver = request.getfixturevalue("cloud_driver")
        self.weh: WebElementHandler = request.getfixturevalue("weh")
        self.wec: WebElementController = request.getfixturevalue("wec")
        self.tshark: Tshark = request.getfixturevalue("tshark")
        self.rest: Rest = request.getfixturevalue("rest")
        self.reset_utils: NetworkElementResetDeviceUtilsKeywords = request.getfixturevalue("reset_utils")
        self.action_chains: type = request.getfixturevalue("action_chains")
        self.dump_data: Callable[[Union[str, List, Dict]], str] = dump_data
        self.update_test_name: Callable[[str], None] = request.getfixturevalue("update_test_name")
        self.end_system_utils: EndSystemUtils = EndSystemUtils()
        self.low_level_apis: LowLevelApis = LowLevelApis()
        self.virtual_machine_utils: VirtualMachineUtils = VirtualMachineUtils()
        self.netelem_utils: NetElementUtils = NetElementUtils()
        self.low_level_traffic_apis: LowLevelTrafficApis = LowLevelTrafficApis()
        self.common_object_utils: CommonObjectUtils = CommonObjectUtils()
        
        self.get_xiq_library: GetXiqLibrary = request.getfixturevalue("get_xiq_library")
        self.deactivate_xiq_library: DeactivateXiqLibrary = request.getfixturevalue("deactivate_xiq_library")
        self.revert_node: Callable = request.getfixturevalue("revert_node")
        self.poll: Callable = request.getfixturevalue("poll")
        self.retry: Callable = request.getfixturevalue("retry")
        self.bounce_iqagent: BounceIqagent = request.getfixturevalue("bounce_iqagent")
        self.login_xiq: LoginXiq = request.getfixturevalue("login_xiq")
        self.enter_switch_cli: EnterSwitchCli = request.getfixturevalue("enter_switch_cli")
        self.open_spawn: OpenSpawn = request.getfixturevalue("open_spawn")
        self.open_pxssh_spawn: OpenPxsshSpawn = request.getfixturevalue("open_pxssh_spawn")
        self.connect_to_all_devices: Callable[[], Iterator[NetworkElementCliSend]] = request.getfixturevalue("connect_to_all_devices")
        self.close_connection: CloseConnection = request.getfixturevalue("close_connection")
        self.configure_iqagent: ConfigureIqAgent = request.getfixturevalue("configure_iqagent")
        self.check_devices_are_reachable: CheckDevicesAreReachable = request.getfixturevalue("check_devices_are_reachable")
        self.dump_switch_logs: DumpSwitchLogs = request.getfixturevalue("dump_switch_logs")
        self.check_devices_are_onboarded: CheckDevicesAreOnboarded = request.getfixturevalue("check_devices_are_onboarded")
        self.modify_stacking_node: ModifyStackingNode = request.getfixturevalue("modify_stacking_node")
        self.reboot_device: RebootDevice = request.getfixturevalue("reboot_device")
        self.reboot_stack_unit: RebootStackUnit = request.getfixturevalue("reboot_stack_unit")
        self.get_stack_slots: GetStackSlots = request.getfixturevalue("get_stack_slots")
        self.clear_traffic_counters: ClearTrafficCounters = request.getfixturevalue("clear_traffic_counters")
        self.dev_cmd: NetworkElementCliSend = request.getfixturevalue("dev_cmd")
        self.debug: Callable = request.getfixturevalue("debug")
        self.get_random_word: Callable[[str], str] = request.getfixturevalue("get_random_word")
        self.add_switch_template_to_teardown: Callable[[str], None] = add_switch_template_to_teardown
        self.add_network_policy_to_teardown: Callable[[str], None] = add_network_policy_to_teardown
        self.add_onboarding_location_to_teardown: Callable[[str], None] = add_onboarding_location_to_teardown
        self.create_location: CreateLocation = request.getfixturevalue("create_location")
        self.get_new_action_chains: Callable[[], ActionChains] = request.getfixturevalue("get_new_action_chains")
        self.cleanup: Cleanup = request.getfixturevalue("cleanup")
        self.generate_template_for_given_model: Callable[[Node], Tuple[str]] = generate_template_for_given_model


@pytest.fixture(scope="session")
def test_bed(
    request: fixtures.SubRequest
) -> Testbed:
    return Testbed(request)
