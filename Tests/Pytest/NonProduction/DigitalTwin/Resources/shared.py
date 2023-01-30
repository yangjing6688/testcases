"""
Digital Twin - shared.py

This file is a place for items that are shared between test-related files and the conftest.py.
The desire is to keep conftest.py simplified by limiting its content to pytest and fixture-related
items.
"""

import os
import random
import time
import re
import subprocess
import requests
import yaml
from ExtremeAutomation.Library.Logger.PytestLogger import PytestLogger
from ..Resources.SuiteUdks import SuiteUdk


logger = PytestLogger()


TMP_YAML_FILE = "cfg_tmp.yaml"
DT_YAML_DIR = os.path.join("Resources", "dtyaml")
DT_YAML_FILE_PATH = os.path.join(DT_YAML_DIR, TMP_YAML_FILE)

UPLOAD_PATH = os.path.join(DT_YAML_DIR, "upload_files")

PLATFORMS_YAML_FILE = os.path.join("Resources", "platforms.yaml")

GNS3_API_URL = "http://localhost:3801/v2"
GNS3_NOS_LOCATION = "/ext/ro/images/QEMU/exos.qcow2"
GNS3_DFLT_DOCKER_IMG = "engartifacts1.extremenetworks.com:8099/dtec/dtec:latest"

DT_DFLT_RAM_AMOUNT = 1024

# Time to wait for a system to boot up (in seconds)
SYS_BOOT_SLEEP = 25
SYS_BOOT_SLEEP_STACK = 45

DT_MGMT_VRF = "vrf_2256"

# List of platform prefixes/family that do not have OOB Mgmt (no VR-Mgmt)
PLATFORMS_WITHOUT_OOB_MGMT = ["5320"]

def get_platforms():
    """Returns a dictionary of supported platforms"""
    with open(PLATFORMS_YAML_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)["platforms"]

PLATFORMS = get_platforms()


# This will be the list of DtTestEnv instances to be used by the Generic Tests
GENERIC_TEST_ENVS = []

def set_generic_test_envs(newlist):
    global GENERIC_TEST_ENVS # pylint: disable=global-statement
    GENERIC_TEST_ENVS.clear()
    GENERIC_TEST_ENVS += newlist

def get_generic_test_envs():
    return GENERIC_TEST_ENVS


# This will be the list of DtTestEnv instances to be used by the Bundle Tests
BUNDLE_TEST_ENVS = []

def set_bundle_test_envs(newlist):
    global BUNDLE_TEST_ENVS # pylint: disable=global-statement
    BUNDLE_TEST_ENVS.clear()
    BUNDLE_TEST_ENVS += newlist

def get_bundle_test_envs():
    return BUNDLE_TEST_ENVS


class DtTestEnv:
    """Define a Digital Twin Test Environment for creating a DT instance."""

    def __init__(self, yaml_file=None, sys_mac=None, sys_type=None, vim_type=None):
        self.yaml_file = yaml_file if yaml_file else TMP_YAML_FILE
        self.sys_mac = sys_mac if sys_mac else SuiteUdk.get_random_unicast_mac()
        self.sys_type = sys_type
        self.yaml = None if not sys_type else self.gen_yaml(sys_type, vim_type)
        self.vim_type = vim_type

        if self.yaml_file != TMP_YAML_FILE:
            self.read_yaml_file()

        self.ram = self._get_ram()

    def __str__(self):
        ret = "{} | {} | {}MB".format(self.yaml_file, self.sys_mac, self.ram)
        if self.sys_type:
            ret += " | {}".format(self.sys_type)
            if self.vim_type:
                ret += " | {}".format(self.vim_type)
        return ret

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def gen_yaml(sys_type, vim_type):
        yaml_dict = {"system": {"slots": [{"num": 1, "type": sys_type}]}}
        if vim_type:
            yaml_dict["system"]["slots"][0]["vims"] = [{"slot": "A", "type": vim_type}]
        return yaml_dict

    def yaml_file_path(self):
        return os.path.join(DT_YAML_DIR, self.yaml_file)

    def write_yaml_file(self):
        with open(self.yaml_file_path(), "w", encoding="utf-8") as file:
            yaml.dump(self.yaml, file)

    def read_yaml_file(self):
        with open(self.yaml_file_path(), "r", encoding="utf-8") as file:
            self.yaml = yaml.safe_load(file)

    def setup(self):
        if self.yaml_file == TMP_YAML_FILE:
            self.write_yaml_file()

    def cleanup(self):
        if self.yaml_file == TMP_YAML_FILE:
            os.remove(self.yaml_file_path())

    def uses_stacking(self):
        return self.yaml["system"].get("stacking", False)

    def get_slot(self, slot_num):
        for slot in self.yaml["system"]["slots"]:
            if str(slot["num"]) == slot_num:
                return slot
        return None

    def get_first_slot_num(self):
        slot_nums = [slot["num"] for slot in self.yaml["system"]["slots"]]
        return str(min(slot_nums)) if slot_nums else None

    def get_prim_slot_num(self):
        if self.uses_stacking():
            for slot in self.yaml["system"]["slots"]:
                if slot.get("primary", False):
                    return str(slot["num"])

            return self.get_first_slot_num()
        return None

    def get_boot_wait_time(self):
        if self.uses_stacking():
            return SYS_BOOT_SLEEP_STACK
        return SYS_BOOT_SLEEP

    def get_dflt_mgmt_vrid(self):
        if self.uses_stacking():
            sys_type = self.get_slot(self.get_prim_slot_num())["type"]
        else:
            sys_type = self.yaml["system"]["slots"][0]["type"]

        if any(re.match(plat, sys_type) for plat in PLATFORMS_WITHOUT_OOB_MGMT):
            return 2  # VR-Default
        return 0  # VR-Mgmt

    @staticmethod
    def get_ram_for_sys_type(sys_type):
        for plat in PLATFORMS:
            for card in plat["cards"]:
                if card["type"] == sys_type:
                    return card["ram"]
        return None

    def _get_ram(self):
        # This is sortof best-effort, because the YAML file could be invalid
        # (for testing).  We will just choose the first "primary" slot or the
        # first slot if no slot is marked as primary.
        ram = None
        sys_type = None
        try:
            if not self.uses_stacking:
                # Get first slot...for negative testcases, we may choose the wrong
                # one or raise an exception, which is fine.
                sys_type = self.yaml["system"]["slots"][0]["type"]
                ram = self.get_ram_for_sys_type(sys_type)
            else:
                lowest_slot = self.yaml["system"]["slots"][0]["num"]
                for slot in self.yaml["system"]["slots"]:
                    if slot["num"] <= lowest_slot:
                        sys_type = slot["type"]
                        ram = self.get_ram_for_sys_type(sys_type)
                    if slot.get("primary") and slot["primary"]:
                        sys_type = slot["type"]
                        ram = self.get_ram_for_sys_type(sys_type)
                        break
        except Exception:
            logger.debug("Exception detecting RAM value")

        if ram is None:
            ram = DT_DFLT_RAM_AMOUNT
            logger.info("System type %s has no configured RAM value...using default: %d "
                        "(normal for negative tests)", sys_type, ram)

        return ram


# List of standard/hard-coded configs for manually-created YAML files.  We
# could eventually just load these automatically from  cfg_*.yaml or something,
# but the entries with hard-coded MAC addresses will need to be dealt with
STD_CFG = [
    DtTestEnv("cfg_001.yaml"),
    DtTestEnv("cfg_002.yaml", "0c:b9:04:92:33:22"),
    DtTestEnv("cfg_003.yaml", "0c:b9:03:02:14:04"),
    DtTestEnv("cfg_004.yaml"),
    DtTestEnv("cfg_005.yaml"),
    DtTestEnv("cfg_006.yaml"),
    DtTestEnv("cfg_007.yaml", "0a:49:26:16:99:02"),
    DtTestEnv("cfg_008.yaml"),
    ]


#############################################################################################
# All the DtTestEnv's must be created ahead of time because when pytest_generate_tests
# is run, it creates fixture parameters for every function separately.  If the parameters
# don't match, dt_cl_test_env will be called separately and end up starting/stopping a DT
# for each test.  As long as pytest can match the parameters across tests, the "class" scope
# will work and all tests will be run on the same DT instance.
#############################################################################################
VM_CFGS = {}

def populate_vm_cfgs():
    """Populate VM_CFGS.  Use a function to keep the globals down and pylint happy"""
    # Hard-coded above
    VM_CFGS["standard"] = STD_CFG

    # Create a single random entry from each supported card type
    VM_CFGS["sys_sample"] = [DtTestEnv(sys_type=random.choice(cards)["type"])
                             for cards in [plat["cards"] for plat in PLATFORMS]]

    # Create an entry for each supported card type
    VM_CFGS["sys"] = {}
    for plat in PLATFORMS:
        VM_CFGS["sys"][plat["family"]] = \
            [DtTestEnv(sys_type=card["type"]) for card in plat["cards"]]

    # Create an entry for each supported VIM type for each related card type
    VM_CFGS["vim"] = {}
    for plat in PLATFORMS:
        if plat.get("vims") and len(plat["vims"]) > 0:
            VM_CFGS["vim"][plat["family"]] = []
            for card in plat["cards"]:
                VM_CFGS["vim"][plat["family"]] += \
                    [DtTestEnv(sys_type=card["type"], vim_type=vim["type"]) for vim in plat["vims"]]

populate_vm_cfgs()


def get_vm_cfg_if_valid_sys_type(sys_type):
    """Return an environment for a single sys_type, if it is valid.  Note this
    will be a different intance than the same sys_type created from sys_<family>."""
    for plat in PLATFORMS:
        for card in plat["cards"]:
            if sys_type == card["type"]:
                return DtTestEnv(sys_type=card["type"])
    return None


def get_my_ip_address():
    """Quick and dirty get the usable IP address of the device running pytest"""
    cmd = ["ip", "route", "get", "8.8.8.8"]
    output = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    logger.debug("output: %s", output)
    match = re.search(r"src (\d+\.\d+\.\d+.\d+) ", str(output.stdout))
    if match:
        return match.group(1)
    return None


class Gns3:
    """Provide GNS3 functions and runtime info"""

    def __init__(self, nos_image, name, docker_image=GNS3_DFLT_DOCKER_IMG, base_url=GNS3_API_URL,
                 use_dt_mgmt=True):
        self.base_url = base_url
        self.name = name
        self.nos_image = nos_image
        self.docker_image = docker_image
        self.xiq_template = None
        self.switch_template = None
        self.project = None
        self.use_dt_mgmt = use_dt_mgmt

    @staticmethod
    def _run_sys_cmd(cmd):
        output = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logger.debug("output: %s", output)

    @staticmethod
    def _send_post(url, json=None):
        logger.debug("Post Request: %s", json)
        req = requests.post(url, json=json if json else {})
        logger.debug("Status Code: %s (%d)", req.reason, req.status_code)
        return req.json()

    @staticmethod
    def _send_put(url, json):
        logger.debug("Put Request: %s", json)
        req = requests.put(url, json=json)
        logger.debug("Status Code: %s (%d)", req.reason, req.status_code)
        return req.json()

    @staticmethod
    def _send_get(url):
        req = requests.get(url)
        logger.debug("Status Code: %s (%d)", req.reason, req.status_code)
        logger.debug("Get Request: %s", req.json())
        return req.json()

    @staticmethod
    def _send_delete(url):
        req = requests.delete(url)
        logger.debug("Status Code: %s (%d)", req.reason, req.status_code)

    def get_vrf_exec_prefix(self):
        """If DT Mgmt is in-use, not every command can access the mgmt network
        without special sauce.  One example is the bundle_handler upload and
        download commands.  They need the calling environment to manually
        setup use of DT Mgmt if https (what IQA uses) is not being used."""
        if self.use_dt_mgmt:
            return f"ip vrf exec {DT_MGMT_VRF}"
        else:
            return ""

    def get_templates(self):
        logger.info("Getting GNS3 Templates")
        url = self.base_url + "/templates"
        resp = self._send_get(url)
        for template in resp:
            if template.get("name") == "Ethernet switch":
                self.switch_template = template.get("template_id")
            elif template.get("name") == "NAT":
                self.xiq_template = template.get("template_id")
        if not self.xiq_template or not self.switch_template:
            raise LookupError

    def start_instance(self):
        logger.info("Pulling docker image %s", self.docker_image)
        self._run_sys_cmd(["docker", "image", "pull", self.docker_image])

## TODO:JLB This is temporary.  Once a new "fixed" container image is available, this can be removed
#
#if container has been fixed
#       logger.info("Starting docker container %s", self.name)
#       self._run_sys_cmd(["docker", "container", "run", "--rm", "--name", self.name,
#                          "--hostname", self.name, "--detach", "--privileged",
#                          "--publish", "3801:3080", "--publish", "5000:5002",
#                          "--publish", "8801:8080",
#                          self.docker_image, "--start-gns3-be", "--start-gns3-fe"])
#else use workaround
        logger.info("Creating docker container %s", self.name)
        self._run_sys_cmd(["docker", "container", "create", "--rm", "--name", self.name,
                           "--hostname", self.name, "--privileged",
                           "--publish", "3801:3080", "--publish", "5000:5002",
                           "--publish", "8801:8080",
                           self.docker_image, "--start-gns3-be", "--start-gns3-fe"])

        logger.info("Copying new qemu_vm.py to docker container %s", self.name)
        self._run_sys_cmd(["docker", "container", "cp", "/home/jbarnhill/qemu_vm.py",
                           self.name+":"+"/usr/share/gns3/gns3-server/lib/python3.9/site-packages/gns3server/compute/qemu/qemu_vm.py"])

        logger.info("Starting docker container %s", self.name)
        self._run_sys_cmd(["docker", "container", "start", self.name])
#end
        wait_time = 5
        logger.info("Sleep %d seconds while container starts", wait_time)
        time.sleep(wait_time)
        self.get_templates()

    def stop_instance(self):
        logger.info("Stopping docker instance %s", self.name)
        self._run_sys_cmd(["docker", "container", "stop", self.name])

    def copy_nos_image(self):
        assert os.path.exists(self.nos_image), f"NOS image {self.nos_image} does not exist"
        #JLB:New Container
        qemu_dir = os.path.dirname(GNS3_NOS_LOCATION)
        logger.info("Creating QEMU directory %s in docker instance %s", qemu_dir, self.name)
        self._run_sys_cmd(["docker", "exec", self.name, "mkdir", "-p", qemu_dir])
        logger.info("Copying %s to docker instance %s", self.nos_image, self.name)
        self._run_sys_cmd(["docker", "container", "cp", self.nos_image,
                           self.name + ":" + GNS3_NOS_LOCATION])

    def create_project(self, project_name):
        logger.info("Creating GNS3 Project %s", project_name)

        url = self.base_url + "/projects"
        json = {"name": project_name}
        resp = self._send_post(url, json)
        proj_id = resp["project_id"]
        logger.debug("proj_id = %s", proj_id)

        url += "/" + proj_id
        json = {"scene_width": 500, "scene_height": 500, "drawing_grid_size": 25, "grid_size": 75,
                "show_grid": True, "snap_to_grid": True}
        self._send_put(url, json)
        self.project = {"name": project_name, "id": proj_id, "url": url}

    def delete_project(self):
        logger.info("Delete project %s", self.project["name"])
        self._send_delete(self.project["url"])

    def create_xiq_node(self):
        logger.info("Create XIQ Node in project %s", self.project["name"])

        node_name = "XIQ"
        url = self.project["url"] + "/templates/" + self.xiq_template
        json = {"name": node_name, "compute_id": "local", "x": 0, "y": 0}
        resp = self._send_post(url, json)
        self.project["xiq"] = {"name": node_name, "id": resp["node_id"]}
        width = resp["width"]
        height = resp["height"]

        url = self.project["url"] + "/nodes/" + self.project["xiq"]["id"]
        json = {"name": node_name, "x": -int(width/2), "y": -int(height/2+175)}
        self._send_put(url, json)

    def create_mgmt_switch_node(self):
        logger.info("Create Mgmt Switch Node in project %s", self.project["name"])

        node_name = "Mgmt_SW"
        url = self.project["url"] + "/templates/" + self.switch_template
        json = {"name": node_name, "compute_id": "local", "x": 0, "y": 0}
        resp = self._send_post(url, json)
        self.project["switch"] = {"name": node_name, "id": resp["node_id"]}
        width = resp["width"]
        height = resp["height"]

        url = self.project["url"] + "/nodes/" + self.project["switch"]["id"]
        json = {"name": node_name, "x": -int(width/2), "y": -int(height/2+50)}
        self._send_put(url, json)

    def create_dt_node(self, ram_size, mac_addr, cfg_name, cfg_urls):
        logger.info("Create DT Node in project %s", self.project["name"])

        node_name = "EXOS-DT"
        url = self.project["url"] + "/nodes"
        json = {"name": node_name, "compute_id": "local", "x": 0, "y": 0, "node_type": "qemu",
                "properties": {"platform": "x86_64"}}
        resp = self._send_post(url, json)
        self.project["dt"] = {"name": node_name, "id": resp["node_id"]}

        # Copy the qcow2 file before assigning the hda_disk_image
        self.copy_nos_image()

        bios_opts = f"-extreme-dt 'version=22.4;{'dt_mgmt=enabled;' if self.use_dt_mgmt else ''}"\
                    f"cfg_name={cfg_name};cfg_urls={cfg_urls}'"
        json = {"x": 125, "y": -100, "first_port_name": "Mgmt", "port_name_format": "Port{port1}",
                "symbol": ":/symbols/multilayer_switch.svg",
                "properties": {"adapters": 5, "boot_priority": "cd", "cpus": 2,
                               "process_priority": "normal", "hda_disk_image": "exos.qcow2",
                               "adapter_type": "virtio-net-pci", "hda_disk_interface": "virtio",
                               "mac_address": mac_addr, "ram": ram_size, "options": bios_opts}}
        url += "/" + self.project["dt"]["id"]
        self._send_put(url, json)

    def setup_dt_node(self):
        self.create_link(self.project["switch"], self.project["dt"], 1, 0)
        self.start_dt_node()

    def start_dt_node(self):
        logger.info("Start DT Node in project %s", self.project["name"])
        url = self.project["url"] + "/nodes/" + self.project["dt"]["id"] + "/start"
        self._send_post(url)

    def delete_dt_node(self):
        logger.info("Delete DT Node in project %s", self.project["name"])
        url = self.project["url"] + "/nodes/" + self.project["dt"]["id"]
        self._send_delete(url)

    def create_link(self, ep1, ep2, ep1_port=0, ep2_port=0):
        json = {"nodes": [{"node_id": ep1["id"], "adapter_number": 0, "port_number": ep1_port},
                          {"node_id": ep2["id"], "adapter_number": 0, "port_number": ep2_port}]}
        url = self.project["url"] + "/links"
        self._send_post(url, json)

    def create_common_infrastructure(self):
        """Convenience wrapper"""
        self.create_project("UT-Project")
        self.create_xiq_node()
        self.create_mgmt_switch_node()
        self.create_link(self.project["xiq"], self.project["switch"])

    def delete_common_infrastructure(self):
        """Convenience wrapper"""
        self.delete_project()
