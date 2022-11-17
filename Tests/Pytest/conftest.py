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

from pexpect.pxssh import pxssh
from _pytest import mark, fixtures
from collections import defaultdict
from pytest_testconfig import config
from contextlib import contextmanager
from typing import List, Dict, DefaultDict, Callable, Tuple, Iterator, Protocol, NewType, Union

from ExtremeAutomation.Library.Utils.Singleton import Singleton
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Library.Logger.PytestLogger import PytestLogger
from ExtremeAutomation.Library.Logger.Colors import Colors
from selenium.webdriver.common.action_chains import ActionChains
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import NetworkElementConnectionManager
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementCliSend import NetworkElementCliSend
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.Udks import Udks
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
from extauto.xiq.flows.common.Navigator import Navigator
from extauto.common.Utils import Utils
from extauto.common.CloudDriver import CloudDriver
from extauto.common.AutoActions import AutoActions
from extauto.common.Cli import Cli


Node = NewType("Node", Dict[str, Union[str, Dict[str, str]]])
Options = NewType("Options", Dict[str, Union[str, Dict[str, str]]])
PolicyConfig = NewType("PolicyConfig", DefaultDict[str, Dict[str, str]])
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
        slots: int
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

class DevicesConfiguration(Protocol):
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
    args.append(os.path.join(os.path.dirname(__file__), "conftest.py"))


def get_test_marker(
        item: pytest.Function
) -> List[TestCaseMarker]:  
    return [m.name for m in item.own_markers if any(re.search(rf"^{test_marker}_", m.name) for test_marker in valid_test_markers)]


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
    pytest.runlist_path: str = ""
    pytest.suitemaps_name: List[str] = []
    pytest.runlist_tests: List[TestCaseMarker] = []
    pytest.suitemap_tests: Dict[str, Union[str, Dict[str, str]]] = {}
    pytest.suitemap_data: Dict[str, Union[str, Dict[str, str]]] = {}
    pytest.onboarding_options: Options = {}
    pytest.run_options: Options = {}
    pytest.onboard_one_node: bool = False 
    pytest.onboard_two_node: bool = False 
    pytest.onboard_stack: bool = False 
    pytest.all_nodes: List[Node] = []
    pytest.standalone_nodes: List[Node] = []
    pytest.stack_nodes: List[Node] = []
    pytest.config_helper: PytestConfigHelper = PytestConfigHelper(config)
    pytest.onboarding_test_name: str = "tcxm_xiq_onboarding"
    pytest.onboarding_cleanup_test_name: str = "tcxm_xiq_onboarding_cleanup"
    pytest.created_onboarding_locations: List[str] = []
    pytest.items: List[pytest.Function] = []
    pytest.testbed_one_node_items: List[pytest.Function] = []
    pytest.testbed_two_node_items: List[pytest.Function] = []
    pytest.testbed_stack_items: List[pytest.Function] = []


def pytest_collection_modifyitems(session, items):

    if pytest.runlist_path != "default":
        
        logger_obj.info(f"Current runlist ('{pytest.runlist_name}') is located in this yaml file: '{pytest.runlist_path}'.")
        logger_obj.info(f"Found {len(pytest.runlist_tests)} tests in given runlist: " + "'" + "', '".join(pytest.runlist_tests) + "'.")
        logger_obj.info(f"Collected {len(items)} test functions from given test directory path(s).")

        for item in items:
            
            if (cls_markers := getattr(item.cls, "pytestmark", None)) is not None:
                
                item_testbed_marker = [m for m in item.own_markers if m.name in valid_testbed_markers]
                cls_testbed_marker = [m for m in cls_markers if m.name in valid_testbed_markers]
                                
                if cls_testbed_marker and not item_testbed_marker:
                    cls_marker = cls_testbed_marker[0]
                    item.add_marker(
                        getattr(pytest.mark, cls_marker.name)
                    )

        for item in items:
            if (callspec := getattr(item, "callspec", None)) is not None:
                test_data = callspec.params["test_data"]
                test_marker_from_test_data = test_data["tc"]
                tc_markers = get_test_marker(item)
                for marker in tc_markers:
                    if marker != test_marker_from_test_data:
                        [marker_obj] = [mk for mk in item.own_markers if mk.name == marker]
                        item.own_markers.pop(item.own_markers.index(marker_obj))

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
        if not pytest.onboard_stack:
            logger_obj.warning(
                "There is no stack device in the provided yaml file. The stack test cases will be unselected.")
            
            if testbed_item_mapping['testbed_stack']:
                logger_obj.warning(
                    f"{len(testbed_item_mapping['testbed_stack'])} testbed_stack item(s) will be unselected.")
            
            temp_items = [
                item for item in temp_items if 'testbed_stack' not in [marker.name for marker in item.own_markers]]

        pytest.onboard_two_node = len(pytest.standalone_nodes) > 1
        if not pytest.onboard_two_node:
            logger_obj.warning(
                "There are not enough standalone devices in the provided yaml file. "
                "The testbed two node test cases will be unselected.")
            
            if testbed_item_mapping['testbed_2_node']:
                    logger_obj.warning(
                        f"{len(testbed_item_mapping['testbed_2_node'])} testbed_2_node item(s) will be unselected.")
            
            temp_items = [
                item for item in temp_items if 'testbed_2_node' not in [marker.name for marker in item.own_markers]]
        
        pytest.onboard_one_node = len(pytest.standalone_nodes) >= 1
        if not pytest.onboard_one_node:
            logger_obj.warning(
                "There is no standalone device in the provided yaml file. "
                "The testbed one node test cases will be unselected.")
        
            if testbed_item_mapping['testbed_1_node']:
                logger_obj.warning(
                    f"{len(testbed_item_mapping['testbed_1_node'])} testbed_1_node item(s) will be unselected.")
            
            temp_items = [
                item for item in temp_items if 'testbed_1_node' not in [marker.name for marker in item.own_markers]]
        
        if items_without_testbed_marker:
            logger_obj.warning(
                f"{len(items_without_testbed_marker)} item(s) that do not have a valid testbed marker will be unselected.")
        
        temp_items = [
            item for item in temp_items if any(
                [testbed_marker in [marker.name for marker in item.own_markers]
                 for testbed_marker in valid_testbed_markers]
        )]

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
            logger_obj.error(error)
            pytest.fail(error)

        for test_code, functions in item_test_marker_mapping.items():
            if len(functions) > 1:
                error = f"Test marker '{test_code}' is used as marker for more than one test function:\n" +\
                        "\n".join(functions)
                logger_obj.error(error)
                pytest.fail(error)

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
                
                if (cls_markers := getattr(item.cls, "pytestmark", None)) is not None:
                    
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
                logger_obj.error(error)
                pytest.fail(error)
                        
            for item, priority in priority_item_mapping.items():
                if len(priority) > 1:
                    error = f"\nThis test function has more than one valid priority marker: " \
                            f"{item.nodeid} (markers: '{priority}')."
                    logger_obj.error(error)
                    pytest.fail(error)

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
            
            suitemap_tcs: List[TestCaseMarker] = []
            
            for test_identifier, test_info in pytest.suitemap_tests.items():
                if (tc := test_info.get("tc")) is not None:
                    suitemap_tcs.append(tc)
                elif (tcs := test_info.get("tests")) is not None:
                    for tc in tcs:
                        suitemap_tcs.append(tc['tc'])

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
                    "There are no test left selected to run for this session besides the onboarding tests.")
            
        else:
            message = "Did not find any test function to run this session."
            logger_obj.warning(message)

        pytest.testbed_one_node_items = list(
            filter(lambda item: "testbed_1_node" in [marker.name for marker in item.own_markers], ordered_items))
        pytest.testbed_two_node_items = list(
            filter(lambda item: "testbed_2_node" in [marker.name for marker in item.own_markers], ordered_items))
        pytest.testbed_stack_items = list(
            filter(lambda item: "testbed_stack" in [marker.name for marker in item.own_markers], ordered_items))
        
        if (not pytest.testbed_two_node_items) and pytest.onboard_two_node:
            logger_obj.info(
                "There are no testbed_two_node items left. Will make sure the second node is not onboarded.")
            pytest.onboard_two_node = False

        if (not pytest.testbed_one_node_items) and pytest.onboard_one_node:
            logger_obj.info(
                "There are no testbed_one_node items left. Will make sure the first node"
                "is not onboarded (except when the onboard_two_node flag is enabled)."
            )
            if not pytest.onboard_two_node:
                pytest.onboard_one_node = False
        
        if (not pytest.testbed_stack_items) and pytest.onboard_stack:
            logger_obj.info(
                "There are no testbed_stack items left. Will make sure the stack node is not onboarded.")
            pytest.onboard_stack = False

        logger_obj.debug(f"{pytest.onboard_one_node=}, {pytest.onboard_two_node=}, {pytest.onboard_stack=}")

        if ordered_items:
            logger_obj.info(
                f"These {len(ordered_items)} test(s) will run this session: {[get_test_marker(item)[0] for item in ordered_items]}")
        
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
    
    if pytest.runlist_path != "default":
        try:
            with open(pytest.runlist_path, "r") as run_list:
                output_runlist = run_list.read()
        except FileNotFoundError:
            error = f"Did not find this runlist file: '{pytest.runlist_path}'."
            logger_obj.error(error)
            pytest.fail(error)

        pytest.runlist = yaml.safe_load(output_runlist)
        pytest.runlist_name = list(pytest.runlist)[0]
        pytest.runlist_tests = pytest.runlist[pytest.runlist_name]['tests']
        pytest.suitemaps_name = pytest.runlist[pytest.runlist_name]['suitemap']

        for suitemap in pytest.suitemaps_name:
            try:
                with open(suitemap, "r") as run_list:
                    output_suitemap = run_list.read()
            except FileNotFoundError:
                logger_obj.warning(f"Did not find this suitemap file: '{suitemap}'")
            else:
                suitemap_dict = yaml.safe_load(output_suitemap)
                suitemap_tests_dict = suitemap_dict['tests']
                suitemap_data_dict = suitemap_dict.get('data', {})
                pytest.suitemap_tests = {**pytest.suitemap_tests, ** suitemap_tests_dict}
                pytest.suitemap_data = {**pytest.suitemap_data, **suitemap_data_dict}
        
        pytest.onboarding_options: Options = pytest.runlist[pytest.runlist_name].get('onboarding_options', {})
        pytest.run_options: Options = pytest.runlist[pytest.runlist_name].get("run_options", {}) or {}


def pytest_sessionfinish(session):

    if pytest.runlist_path != "default":

        try:
            config['${TEST_NAME}'] = "RESULTS"
            
            max_tc_length = max([len(get_test_marker(item)[0]) for item in pytest.items])
            result_witdh = 17
            line_width = max_tc_length + 7 * result_witdh + 38
            
            output = "\n" + "-" * line_width
            output += f"\n| {'ORDER':^5} | {'TEST CASE':^{max_tc_length}} | {'P':^2} | {'TB':^{result_witdh}} | {'SETUP_RESULT':^{result_witdh}} | " \
                      f"{'CALL_RESULT':^{result_witdh}} | {'TEARDOWN_RESULT':^{result_witdh}} | " \
                      f"{'SETUP_DURATION':^{result_witdh}} | {'CALL_DURATION':^{result_witdh}} | " \
                      f"{'TEARDOWN_DURATION':^{result_witdh}} |"
            output += "\n" + "-" * line_width
            
            for index, item in enumerate(pytest.items):
                
                test_marker: TestCaseMarker
                [test_marker] = get_test_marker(item)
                
                test_priority: PriorityMarker = "P0" if (is_onboarding_cleanup_test(item) or is_onboarding_test(item)) else get_priority_marker(item)[0].upper()
                testbed_marker: TestbedMarker = "N/A" if (is_onboarding_cleanup_test(item) or is_onboarding_test(item)) else get_testbed_markers(item)[0]
                
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
                
                output += f"\n| {index + 1:^5} | {test_marker:^{max_tc_length}} | {test_priority:^2} | {testbed_marker:^{result_witdh}} | {setup_outcome:^{result_witdh}} | " \
                          f"{call_outcome:^{result_witdh}} | {teardown_outcome:^{result_witdh}} | " \
                          f"{setup_duration:^{result_witdh}} | {call_duration:^{result_witdh}} | " \
                          f"{teardown_duration:^{result_witdh}} |"
                output += "\n" + "-" * line_width
            
            logger_obj.info(output)

        except:
            pass


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
                    f"The {len(next_tests)} test(s) that will run next: " + "'" + "', '".join(next_tests) + "'.")
                
        if result.when == 'call' and result.outcome != "passed":
            for it in item.session.items:
                [temp_test_marker] = get_test_marker(it)
                for mk in it.own_markers:
                    if mk.name == "dependson":
                        if len(mk.args) > 0:
                            if current_test_marker in mk.args:                            
                                it.add_marker(
                                    pytest.mark.skip(
                                        f"'{temp_test_marker}' depends on '{current_test_marker}' but "
                                        f"'{current_test_marker}' failed. The '{temp_test_marker}' "
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
        
        try:
            config['${TEST_NAME}'] = f"{current_test_marker} | SETUP | {pytest.items.index(item) + 1}/{len(pytest.items)}"
        except:
            config['${TEST_NAME}'] = current_test_marker

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

        output = ""
        test_data = {}
        mandatory_fields = ["author", "tc", "description", "title", "steps"]

        if (callspec := getattr(item, "callspec", None)) is not None:
            if (data := callspec.params.get("test_data")) is not None:
                test_data = data
        else:
            test_data = pytest.suitemap_tests[f"{item.cls.__name__}::{item.originalname}"]
            
        for field in mandatory_fields:
            
            if field == "steps":
                if (steps := test_data.get("steps")) is not None:
                    output += "\nSteps:"
                    for index, step in enumerate(steps):
                        output += f"\n  Step {(index + 1)}: '{step}'"
            
            elif (field_value := test_data.get(field)) is not None:
                output += f"\n{field.capitalize()}: '{field_value}'"

        for k, v in test_data.items():
            if k not in mandatory_fields:
                output += f"\n{k}: '{v}'"
        output and logger_obj.step(output)


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
                "The 'skip_setup' option is given in runlist. The onboarding is skipped.")
            return

        if not any(
            [
                pytest.onboard_one_node,
                pytest.onboard_two_node,
                pytest.onboard_stack
            ]
        ):
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
                "The 'skip_teardown' option is given in runlist. The onboarding cleanup is skipped.")
            return
        
        if not any(
            [
                pytest.onboard_one_node,
                pytest.onboard_two_node,
                pytest.onboard_stack
            ]
        ):
            logger.info(
                "There are no devices given in the yaml files or there were no tests left to run"
                " so the onboarding cleanup test won't unconfigure anything.")
            return

        request.getfixturevalue("onboard_cleanup")


@pytest.fixture(scope="session")
def login_xiq(
        debug: Callable,
        get_xiq_library,
        deactivate_xiq_library
) -> LoginXiq:

    @contextmanager
    @debug
    def login_xiq_func(
    ) -> Iterator[XiqLibrary]:

        xiq: XiqLibrary = None
        
        try:
            xiq = get_xiq_library()
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


@pytest.fixture(scope="session")
def deactivate_xiq_library(
    debug: Callable
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
                switch_type=re.match('(\d+).*', mat.group(3).split('_')[0]).group(1)
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
        logger: PytestLogger
) -> Dict[str, str]:
    
    vrs = {}

    def worker(dut: Node):
        with enter_switch_cli(dut) as dev_cmd:
            try:
                output = dev_cmd.send_cmd(
                    dut.name, 'show vlan', max_wait=10, interval=2)[0].return_text
                pattern = f'(\w+)(\s+)(\d+)(\s+)({dut.ip})(\s+)(\/.*)(\s+)(\w+)(\s+/)(.*)(VR-\w+)'
                match = re.search(pattern, output)

                assert match, "Pattern not found, unable to get virtual router info!"
                assert int(match.group(9)) > 0, f"There is no active port in the mgmt vlan {match.group(1)}"
                
                vrs[dut.name] = match.group(12)
            except Exception as exc:
                logger.warning(repr(exc))
                vrs[dut.name] = ""
            
    threads: List[threading.Thread] = []
    try:
        for dut in [d for d in node_list if d.cli_type.upper() == "EXOS"]:
            thread = threading.Thread(target=worker, args=(dut, ))
            threads.append(thread)
            thread.start()
    finally:
        for thread in threads:
            thread.join()
    return vrs


@pytest.fixture(scope="session")
def configure_iq_agent(
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
    def configure_iq_agent_func(
            duts: List[Node]=node_list,
            ipaddress: str=loaded_config['sw_connection_host']
    ) -> None:
        
        virtual_routers: Dict[str, str] = request.getfixturevalue("virtual_routers")

        logger.step(
            f"Configure IQAGENT with IP-Address='{ipaddress}' on these devices: {', '.join([d.name for d in node_list])}.")

        def worker(dut: Node):
            
            with open_spawn(dut) as spawn_connection:
                if loaded_config.get("lab", "").upper() == "SALEM":
                    cli.downgrade_iqagent(dut.cli_type, spawn_connection)
                
                cli.configure_device_to_connect_to_cloud(
                    dut.cli_type, loaded_config['sw_connection_host'],
                    spawn_connection, vr=virtual_routers.get(dut.name, 'VR-Mgmt'), retry_count=30
                )
                
                if dut.cli_type.upper() == "EXOS":
                    spawn_connection.sendline("enable iqagent")

        threads: List[threading.Thread] = []
        try:
            for dut in duts:
                thread = threading.Thread(target=worker, args=(dut, ))
                threads.append(thread)
                thread.start()
        finally:
            for thread in threads:
                thread.join()
    return configure_iq_agent_func


@pytest.fixture(scope="session")
def onboarding_locations(
        node_list: List[Node],
        logger: PytestLogger,
        request: fixtures.SubRequest,
        
) -> Dict[str, str]:
    """
    Fixture that choose the onboarding location for the available nodes.
    """
    
    ret = {}
    
    hardcoded_locations = [
        "San Jose,building_01,floor_01",
    ]
    
    for node in node_list:
        
        onboarding_options: Options = request.getfixturevalue(f"{node.node_name}_onboarding_options")
        onboarding_location: str = onboarding_options.get("onboarding_location")
        create_onboarding_location: bool = onboarding_options.get("create_onboarding_location")

        if onboarding_location:
            
            logger.info(f"Successfully found this location in the runlist for node '{node.node_name}': '{onboarding_location}'")
            ret[node.name] = onboarding_location
            
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
                logger.info(f"Found location(s) attached to '{node.node_name}': {locations}.")
            
            if isinstance(locations, str):
                ret[node.name] = locations
                
            elif isinstance(locations, dict):
                logger.step("Choose one of them.")
                found_location = random.choice(list(locations.values()))
                logger.info(f"The chosen location for '{node.node_name}' is '{found_location}'.")
                ret[node.name] = found_location
            
            else:
                logger.info(f"Did not find any location attached to '{node.node_name}'.")

                logger.step(f"Will choose a location out of these for '{node.node_name}': {hardcoded_locations}.")
                found_location = random.choice(hardcoded_locations)
                logger.info(f"The chosen location for '{node.name}' is '{found_location}'.")
                ret[node.name] = found_location
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
    config['${EXIT_LEVEL}'] = -600

    for word in ["tenant_username", "tenant_password", "test_url"]:
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
        debug: Callable
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
            slots: int=1
    ) -> None:
            
            xiq.xflowscommonDevices._goto_devices()
            
            for dut in duts:
                try:
                    screen.save_screen_shot()
                    logger.info(f"Delete this device: '{dut.name}', '{dut.mac}'.")
                    xiq.xflowscommonDevices._goto_devices()
                    xiq.xflowscommonDevices.delete_device(
                        device_mac=dut.mac)
                    screen.save_screen_shot()
                except Exception as exc:
                    screen.save_screen_shot()
                    logger.warning(repr(exc))
                    
            for location in locations:
                try:
                    logger.info(f"Delete this location: '{location}'.")
                    xiq.xflowsmanageLocation.delete_location_building_floor(
                        *location.split(","))
                    screen.save_screen_shot()
                except Exception as exc:
                    screen.save_screen_shot()
                    logger.warning(repr(exc))   
                                    
            for network_policy in network_policies:
                try:
                    screen.save_screen_shot()
                    logger.info(f"Delete this network policy: '{network_policy}'.")
                    xiq.xflowsconfigureNetworkPolicy.delete_network_policy(
                        network_policy)
                    screen.save_screen_shot()
                except Exception as exc:
                    screen.save_screen_shot()
                    logger.warning(repr(exc))   
                    
            for template_switch in templates_switch:
                logger.info(f"Delete this switch template: '{template_switch}'.")
                for _ in range(slots):
                    try:
                        screen.save_screen_shot()
                        xiq.xflowsconfigureCommonObjects.delete_switch_template(
                            template_switch)
                        screen.save_screen_shot()
                    except Exception as exc:
                        screen.save_screen_shot()
                        logger.warning(repr(exc))   
    return cleanup_func


@pytest.fixture(scope="session")
def configure_network_policies(
        logger: PytestLogger, 
        node_list: List[Node],
        policy_config: PolicyConfig,
        screen: Screen,
        debug: Callable,
        request: fixtures.SubRequest
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
        
        for dut, data in dut_config.items():
     
            [dut_info] = [dut_iter for dut_iter in node_list if dut_iter.name == dut]
            node_name = dut_info.node_name
            onb_options: Options = request.getfixturevalue(f"{node_name}_onboarding_options")
            
            logger.step(f"Configuring the network policy and switch template for dut '{dut}' (node: '{node_name}').")
            network_policy = data['policy_name']
            template_switch = data['template_name']
            model_template = data['dut_model_template']
            units_model = data['units_model']

            if onb_options.get('create_network_policy', True):
                
                logger.step(f"Create this network policy for '{dut}' dut (node: '{node_name}'): '{network_policy}'.")
                assert xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                    network_policy), \
                    f"Policy {network_policy} wasn't created successfully "
                screen.save_screen_shot()
                logger.info(f"Successfully created the network policy '{network_policy}' for dut '{dut}' (node: '{node_name}').")
                
                if onb_options.get('create_switch_template', True):
                    logger.step(f"Create and attach this switch template to '{dut}' dut (node: '{node_name}'): '{template_switch}'.")
                    if dut_info.platform.upper() == "STACK":
                        xiq.xflowsconfigureSwitchTemplate.add_5520_sw_stack_template(
                            units_model, network_policy,
                            model_template, template_switch)
                    else:
                        xiq.xflowsconfigureSwitchTemplate.add_sw_template(
                            network_policy, model_template, template_switch)
                        screen.save_screen_shot()
                    logger.info(f"Successfully created and attached this switch template to the network policy '{network_policy}' of dut '{dut}' (node: '{node_name}').")

                if onb_options.get('assign_network_policy_to_device', True):
                    assert xiq.xflowsmanageDevices.assign_network_policy_to_switch_mac(
                        policy_name=network_policy, mac=dut_info.mac) == 1, \
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
        request: fixtures.SubRequest
) -> PolicyConfig:
    """
    Fixture that selects the policy name and the template name for all the nodes.
    """
    
    dut_config: PolicyConfig = defaultdict(lambda: {})
    pool = list(string.ascii_letters) + list(string.digits)

    for dut in node_list:
        
        model, units_model = generate_template_for_given_model(dut)
        
        onboarding_options: Options = request.getfixturevalue(f"{dut.node_name}_onboarding_options")
        
        random_policy_name = f"{pytest.runlist_name}_np_{''.join(random.sample(pool, k=8))}"[:32]
        random_template_name = f"{pytest.runlist_name}_template_{''.join(random.sample(pool, k=8))}"[:32]
        
        policy_name: str = onboarding_options.get("policy_name", random_policy_name)
        template_name: str = onboarding_options.get("template_name",random_template_name)
        
        dut_config[dut.name]["policy_name"] = policy_name
        dut_config[dut.name]['template_name'] = template_name
        dut_config[dut.name]['dut_model_template'] = model
        dut_config[dut.name]['units_model'] = units_model

    return dut_config


@pytest.fixture(scope="session")
def node_1_policy_config(
        policy_config: PolicyConfig,
        node_1: Node
) -> Dict[str, str]:
    return policy_config.get(node_1.get("name"), {})


@pytest.fixture(scope="session")
def node_2_policy_config(
        policy_config: PolicyConfig,
        node_2: Node
) -> Dict[str, str]:
    return policy_config.get(node_2.get("name"), {})


@pytest.fixture(scope="session")
def node_stack_policy_config(
        policy_config: PolicyConfig,
        node_stack: Node
) -> Dict[str, str]:
    return policy_config.get(node_stack.get("name"), {})


@pytest.fixture(scope="session")
def node_stack_model_units(
    node_stack_policy_config: Dict[str, str]
) -> str:
    return node_stack_policy_config.get("units_model")


@pytest.fixture(scope="session")
def node_1_onboarding_location(
        onboarding_locations: Dict[str, str],
        node_1: Node
) -> str:
    return onboarding_locations.get(node_1.get("name", ""), "")


@pytest.fixture(scope="session")
def node_2_onboarding_location(
        onboarding_locations: Dict[str, str],
        node_2: Node
) -> str:
    return onboarding_locations.get(node_2.get("name", ""), "")


@pytest.fixture(scope="session")
def node_stack_onboarding_location(
        onboarding_locations: Dict[str, str],
        node_stack: Node
) -> str:
    return onboarding_locations.get(node_stack.get("name", ""), "")


@pytest.fixture(scope="session")
def node_1_policy_name(
    node_1_policy_config: Dict[str, str]
) -> str:
    return node_1_policy_config.get("policy_name")


@pytest.fixture(scope="session")
def node_2_policy_name(
    node_2_policy_config: Dict[str, str]
) -> str:
    return node_2_policy_config.get("policy_name")


@pytest.fixture(scope="session")
def node_stack_policy_name(
    node_stack_policy_config: Dict[str, str]
) -> str:
    return node_stack_policy_config.get("policy_name")


@pytest.fixture(scope="session")
def node_1_template_name(
    node_1_policy_config: Dict[str, str]
) -> str:
    return node_1_policy_config.get("template_name")


@pytest.fixture(scope="session")
def node_2_template_name(
    node_2_policy_config: Dict[str, str]
) -> str:
    return node_2_policy_config.get("template_name")


@pytest.fixture(scope="session")
def node_stack_template_name(
    node_stack_policy_config: Dict[str, str]
) -> str:
    return node_stack_policy_config.get("template_name")


@pytest.fixture(scope="session")
def node_list(
        standalone_nodes: List[Node],
        stack_nodes: List[Node],
        node_1_onboarding_options,
        node_2_onboarding_options,
        node_stack_onboarding_options,
        logger: PytestLogger
) -> List[Node]:
    """
    Fixture that selects the devices to be onboarded from the devices.yaml.
    """
    
    duts: List[Node] = []

    if pytest.onboard_two_node or pytest.onboard_one_node:
        
        runos_node_1 = node_1_onboarding_options.get('run_os', [])
        platform_node_1 = node_1_onboarding_options.get('platform', "standalone")
        runos_node_2 = node_2_onboarding_options.get('run_os', [])
        platform_node_2 = node_2_onboarding_options.get('platform', "standalone")
                
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
    
        if pytest.onboard_two_node:
            for node in standalone_nodes:
                if node not in duts:
                    if runos_node_2:
                        if any(node.cli_type.upper() == os.upper() for os in runos_node_2):
                                if (platform_node_2.lower() == "standalone") or (node.platform.lower() == platform_node_2.lower()):
                                    break
                    else:
                        if (platform_node_2.lower() == "standalone") or (node.platform.lower() == platform_node_2.lower()):
                            break  
            else:
                error_msg = f"Failed to find a standalone node in the testbed yaml that satisfy these requirements:" \
                            f"run_os={runos_node_2}, platform='{platform_node_2}'. " \
                            f"Already used node: '{duts[0].name}'."
                logger.error(error_msg)
                pytest.fail(error_msg)

            logger.info(
                f"Successfuly chose this dut as 'node_2': '{node.name}' "
                f"(cli_type='{node.cli_type}', run_os={runos_node_2}, platform='{platform_node_2}').")
            
            node.node_name = "node_2"
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

    return duts


@pytest.fixture(scope="session")
def update_devices(
        logger: PytestLogger,
        node_list: List[Node],
        policy_config: PolicyConfig,
        debug: Callable,
        wait_till: Callable,
        request: fixtures.SubRequest
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

        for dut in duts:
            onb_options: Options = request.getfixturevalue(f"{dut.node_name}_onboarding_options")
            policy_name: str = policy_config[dut.name]['policy_name']
            
            if all(
                [
                    onb_options.get('initial_network_policy_push', True),
                    onb_options.get('assign_network_policy_to_device', True),
                    onb_options.get('create_network_policy', True)
                ]
            ):
                logger.step(f"Select switch row with serial '{dut.mac}'.")
                if not xiq.xflowscommonDevices.select_device(dut.mac):
                    error_msg = f"Switch '{dut.mac}' is not present in the grid."
                    logger.error(error_msg)
                    pytest.fail(error_msg)
                wait_till(timeout=2)
                
                logger.step(f"Update the switch: '{dut.mac}'.")
                if xiq.xflowscommonDevices._update_switch(update_method="PolicyAndConfig") != 1:
                    error_msg = f"Failed to push the update to this switch: '{dut.mac}'."
                    logger.error(error_msg)
                    pytest.fail(error_msg)
                wait_till(timeout=2)

        for dut in duts:
            onb_options: Options = request.getfixturevalue(f"{dut.node_name}_onboarding_options")
            policy_name = policy_config[dut.name]['policy_name']
            if onb_options.get('initial_network_policy_push', True):
                if xiq.xflowscommonDevices._check_update_network_policy_status(policy_name, dut.mac) != 1:
                    error_msg = f"It look like the update failed this switch: '{dut.mac}'."
                    logger.error(error_msg)
                    pytest.fail(error_msg) 

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
                            
        for dut in duts:
            
            if xiq.xflowscommonDevices.onboard_device_quick(
                {
                    "location": onboarding_locations[dut.name],
                    "serial": dut.serial,
                    "make": dut.cli_type,
                    "onboard_device_type": "real"
                }
            ) == 1: 
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
        logger: PytestLogger
) -> None:
    """ Fixture that logs the onboarding options that are selected in the runlist yaml file.
    """
    
    for node_name in ["node_1", "node_2", "node_stack"]:
        fxt: Options = request.getfixturevalue(f"{node_name}_onboarding_options")
        if fxt:
            logger.info(f"The onboarding options for '{node_name}':\n{json.dumps(fxt, indent=4)}")

    run_options: Options = request.getfixturevalue("run_options")
    logger.info(f"The run options for this session: {json.dumps(run_options, indent=4)}")


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
        
        check_devices_are_reachable(node_list)

    return devices_verifications_func


@pytest.fixture(scope="session")
def devices_configuration(
    request: fixtures.SubRequest,
    debug: Callable
) -> DevicesConfiguration:
    """ Fixture that configures the devices for the onboarding.
    """
    
    @debug
    def device_configuration_func() -> None:
        
        configure_iq_agent: ConfigureIqAgent = request.getfixturevalue("configure_iq_agent")
        node_list: List[Node] = request.getfixturevalue("node_list")
        
        configure_iq_agent(duts=node_list)

    return device_configuration_func


@pytest.fixture(scope="session")
def account_configuration(
    request: fixtures.SubRequest,
    debug: Callable
) -> AccountConfiguration:
    """ Fixture that configures the XIQ account at the start of the session.
    """

    @debug
    def account_configuration_func(
        xiq: XiqLibrary
    ) -> None:
        
        if (option := pytest.onboarding_options.get("change_device_management_settings", "disable")):
            
            change_device_management_settings: ChangeDeviceManagementSettings = request.getfixturevalue(
                "change_device_management_settings")
            
            change_device_management_settings(
                xiq,
                option=option
            )

    return account_configuration_func


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
        
        check_devices_are_onboarded(xiq)
    
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
def onboard_cleanup(
        request: fixtures.SubRequest
) -> None:
    """ This fixture does the onboarding cleanup of the selected devices.
        It is called in the onboarding cleanup test ('test_xiq_onboarding_cleanup').
    """
    
    login_xiq: LoginXiq = request.getfixturevalue("login_xiq")
    stack_nodes: List[Node] = request.getfixturevalue("stack_nodes")
    cleanup: Cleanup = request.getfixturevalue("cleanup")
    node_list: List[Node] = request.getfixturevalue("node_list")
    policy_config: PolicyConfig = request.getfixturevalue("policy_config")
    
    with login_xiq() as xiq:

        cleanup(
            xiq=xiq, 
            duts=node_list, 
            network_policies=[dut_info['policy_name'] for dut_info in policy_config.values()],
            templates_switch=[dut_info['template_name'] for dut_info in policy_config.values()],
            slots=len(stack_nodes[0].stack) if len(stack_nodes) > 0 else 1,
            locations=pytest.created_onboarding_locations
        )


@pytest.fixture(scope="session")
def created_onboarding_locations() -> List[str]:
    return pytest.created_onboarding_locations


@pytest.fixture(scope="session")
def run_options() -> Options:
    return pytest.run_options


@pytest.fixture(scope="session")
def node_1(
        request: fixtures.SubRequest,
        logger: PytestLogger
) -> Node:
    if pytest.onboard_one_node or pytest.onboard_two_node:
        node_list: List[Node] = request.getfixturevalue("node_list")
        return [dut for dut in node_list if dut.node_name == "node_1"][0]
    logger.warning("Testbed does not have a standalone node.")
    return {}


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
        logger: PytestLogger
) -> Node:
    if pytest.onboard_two_node:
        node_list: List[Node] = request.getfixturevalue("node_list")
        return [dut for dut in node_list if dut.node_name == "node_2"][0]
    logger.warning("Testbed does not have two standalone nodes.")
    return {}


@pytest.fixture(scope="session")
def node_stack(
        request: fixtures.SubRequest,
        logger: PytestLogger
) -> Node:
    if pytest.onboard_stack:
        node_list: List[Node] = request.getfixturevalue("node_list")
        return [dut for dut in node_list if dut.node_name == "node_stack"][0]
    logger.warning("Testbed does not have a stack node.")
    return {}

 
@pytest.fixture(scope="session")
def dut_ports(
        enter_switch_cli: EnterSwitchCli, 
        node_list: List[Node], 
        debug: Callable
) -> Dict[str, List[str]]:
    
    ports = {}
    
    @debug
    def dut_ports_worker(dut: Node):
        
        with enter_switch_cli(dut) as dev_cmd:
            
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
                ports[dut.name] = filtered
            
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
                ports[dut.name] = match_port
            
            elif dut.cli_type.upper() == "AH-FASTPATH":
                try:
                    dev_cmd.send_cmd(dut.name, "enable")
                except:
                    dev_cmd.send_cmd(dut.name, "exit")
                output = dev_cmd.send_cmd(
                    dut.name, "show port all", max_wait=10, interval=2)[0].return_text
                output = re.findall(r"\r\n(\d+/\d+/\d+)\s+", output)
                ports[dut.name] = output
                dev_cmd.send_cmd(dut.name, "exit")

    threads: List[threading.Thread] = []
    
    try:
        for dut in node_list:
            thread = threading.Thread(target=dut_ports_worker, args=(dut, ))
            threads.append(thread)
            thread.start()
    
    finally:
        for thread in threads:
            thread.join()
    
    return ports


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
        
        platform = "EXOS" if any(node.cli_type.upper() == "EXOS" for node in standalone_nodes + stack_nodes) else "VOSS"
        for _ in range(retries):
            try:
                xiq.xflowsglobalsettingsGlobalSetting.change_exos_device_management_settings(
                    option=option, platform=platform)
                screen.save_screen_shot()
            except Exception as exc:
                logger.warning(repr(exc))
                screen.save_screen_shot()
                wait_till(timeout=step)
            else:
                xiq.xflowscommonNavigator.navigate_to_devices()
                break
        else:
            pytest.fail("Failed to change exos device management settings.")
    return change_device_management_settings_func


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
def auto_actions() -> AutoActions:
    return AutoActions()


@pytest.fixture(scope="session")
def update_test_name(
    loaded_config: Dict[str, str]
    ) -> Callable[[str], None]:
    def func(test_name: str):
        loaded_config['${TEST_NAME}'] = test_name
    return func


@pytest.fixture(scope="session")
def default_library() -> DefaultLibrary:
    return DefaultLibrary()


@pytest.fixture(scope="session")
def udks() -> Udks:
    return Udks()


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
        self.stack_nodes: List[Node] = request.getfixturevalue("stack_nodes")
        self.node_1: Node = request.getfixturevalue("node_1")
        self.node_2: Node = request.getfixturevalue("node_2")
        self.node_stack: Node = request.getfixturevalue("node_stack")
        self.node_list: List[Node] = request.getfixturevalue("node_list")
        
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
        self.created_onboarding_locations: List[str] = request.getfixturevalue("created_onboarding_locations")
   
        self.policy_config: PolicyConfig = request.getfixturevalue("policy_config")
        self.node_1_policy_config: Dict[str, str] = request.getfixturevalue("node_1_policy_config")
        self.node_2_policy_config: Dict[str, str] = request.getfixturevalue("node_2_policy_config")
        self.node_stack_policy_config: Dict[str, str] = request.getfixturevalue("node_stack_policy_config")
        
        self.node_1_policy_name: str = request.getfixturevalue("node_1_policy_name")
        self.node_2_policy_name: str = request.getfixturevalue("node_2_policy_name")
        self.node_stack_policy_name: str = request.getfixturevalue("node_stack_policy_name")
        self.node_1_template_name: str = request.getfixturevalue("node_1_template_name")
        self.node_2_template_name: str = request.getfixturevalue("node_2_template_name")
        self.node_stack_template_name: str = request.getfixturevalue("node_stack_template_name")
        self.node_stack_model_units: str = request.getfixturevalue("node_stack_model_units")

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
        self.bounce_iqagent: BounceIqagent = request.getfixturevalue("bounce_iqagent")
        self.dut_ports: Dict[str, List[str]] = request.getfixturevalue("dut_ports")
        self.login_xiq: LoginXiq = request.getfixturevalue("login_xiq")
        self.enter_switch_cli: EnterSwitchCli = request.getfixturevalue("enter_switch_cli")
        self.open_spawn: OpenSpawn = request.getfixturevalue("open_spawn")
        self.connect_to_all_devices: Callable[[], Iterator[NetworkElementCliSend]] = request.getfixturevalue("connect_to_all_devices")
        self.close_connection: CloseConnection = request.getfixturevalue("close_connection")
        self.virtual_routers: Dict[str, str] = request.getfixturevalue("virtual_routers")
        self.configure_iq_agent: ConfigureIqAgent = request.getfixturevalue("configure_iq_agent")
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
        self.create_location: CreateLocation = request.getfixturevalue("create_location")
        self.get_new_action_chains: Callable[[], ActionChains] = request.getfixturevalue("get_new_action_chains")
        self.cleanup: Cleanup = request.getfixturevalue("cleanup")
        self.generate_template_for_given_model: Callable[[Node], Tuple[str]] = generate_template_for_given_model


@pytest.fixture(scope="session")
def test_bed(
    request: fixtures.SubRequest
) -> Testbed:
    return Testbed(request)
