"""
Digital Twin - SuiteUdks.py
"""

import os
import re
import random
import json
import pytest
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Library.Logger.PytestLogger import PytestLogger

class SuiteUdk():
    """Digital Twin Suite User-Defined-Keywords"""

    def __init__(self):
        self.defaultLibrary = DefaultLibrary()  # pylint: disable=invalid-name
        self.send_cmd = self.defaultLibrary.deviceNetworkElement.networkElementCliSend.send_cmd
        self.logger = PytestLogger()

    @staticmethod
    def get_serial_num_from_mac(mac):
        octets = mac.upper().split(":")
        if len(octets) != 6:
            return "__MAC_ERR__"
        return "".join(octets[2:4]) + "-" + "".join(octets[4:6])

    @staticmethod
    def get_random_unicast_mac():
        # Skip multicast
        first = random.randint(0, 255) & 0xfe
        return "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}"\
            .format(first, *(random.randint(0, 255) for v in range(5))).upper()

    def verify_dt_active(self, dut_name, is_active=True):
        kw_results = self.send_cmd(dut_name, "debug hal run platform config-dump")
        txt = kw_results[0].cmd_obj.return_text

        if is_active:
            return re.search(r"^ +EXOS_DT_ACTIVE: 1", txt, re.M) is not None
        return re.search(r"^ +EXOS_DT_ACTIVE: \(null\)", txt, re.M) is not None

    def verify_dt_mgmt(self, dut_name, in_use=True):
        kw_results = self.send_cmd(dut_name, "debug hal run platform config-dump")
        txt = kw_results[0].cmd_obj.return_text

        if in_use:
            return re.search(r"^ +EXOS_DT_MGMT_VRID: 2000", txt, re.M) is not None
        return re.search(r"^ +EXOS_DT_MGMT_VRID: \(null\)", txt, re.M) is not None

    def verify_system_type(self, dut_name, sys_type):
        kw_results = self.send_cmd(dut_name, "show switch")
        txt = kw_results[0].cmd_obj.return_text

        return re.search(r"System Type:\s+{}".format(re.escape(sys_type)), txt) is not None

    def verify_switch_mac(self, dut_name, mac):
        kw_results = self.send_cmd(dut_name, "show switch")
        txt = kw_results[0].cmd_obj.return_text

        return re.search(r"System MAC:\s+{}".format(re.escape(mac)), txt, re.I) is not None

    def verify_serial_number(self, dut_name, slot_num, serial_number):
        kw_results = self.send_cmd(dut_name, "debug cfgmgr show next dm.card_info")
        txt = kw_results[0].cmd_obj.return_text

        jdoc = json.loads(re.search(r"{[^\n]+}", txt).group())

        for slot in jdoc["data"]:
            if slot["slot"] == slot_num:
                return slot["serial_num"].split(" ", 1)[1] == serial_number

        return False

    def verify_vims(self, dut_name, vims):
        kw_results = self.send_cmd(dut_name, "show version")
        txt = kw_results[0].cmd_obj.return_text

        if not vims:
            # Verify no VIMS listed (with or w/o stacking)
            return (re.search(r"^Switch.*$\nPSU-1", txt, re.M) is not None or
                    re.search(r"Slot-8.*$\n\n^Image", txt, re.M))

        for vim in vims:
            prog = re.compile(r"^{}".format(re.escape(vim)), re.M)
            if len(prog.findall(txt)) != 1:
                return False

        return True

    def verify_licenses(self, dut_name, licenses):
        kw_results = self.send_cmd(dut_name, "show licenses detail")
        txt = kw_results[0].cmd_obj.return_text

        for lic in licenses:
            if not lic:
                continue

            prog = re.compile(r"^[\d\s]*{}.*\s+Yes\s+".format(re.escape(lic)), re.M)
            if len(prog.findall(txt)) != 1:
                return False

        return True

    def verify_no_stacking(self, dut_name):
        kw_results = self.send_cmd(dut_name, "show slot", ignore_cli_feedback=True)
        txt = kw_results[0].cmd_obj.return_text

        # Verify the "show slot" command is not supported
        if re.search(r"Invalid input detected", txt) is None:
            return False

        kw_results = self.send_cmd(dut_name, "debug hal run platform config-dump")
        txt = kw_results[0].cmd_obj.return_text

        return (re.search(r"\n +EXOS_SLOT_ID: (1|\(null\))", txt) is not None and
                re.search(r"\n +EXOS_STACK_SLOT: 1", txt) is not None and
                re.search(r"\n +EXOS_STACK_MODE: 0", txt) is not None and
                re.search(r"\n +numCards: 1", txt) is not None)

    def verify_stacking(self, dut_name, prim_slot_num, num_slots):
        kw_results = self.send_cmd(dut_name, "show slot", ignore_cli_feedback=True)
        txt = kw_results[0].cmd_obj.return_text

        # Verify the "show slot" command is supported
        if re.search(r"Invalid input detected", txt) is not None:
            return False

        kw_results = self.send_cmd(dut_name, "debug hal run platform config-dump")
        txt = kw_results[0].cmd_obj.return_text

        return (re.search(r"\n +EXOS_SLOT_ID: {}".format(prim_slot_num), txt) is not None and
                re.search(r"\n +EXOS_STACK_SLOT: {}".format(prim_slot_num), txt) is not None and
                re.search(r"\n +EXOS_STACK_MODE: 1", txt) is not None and
                re.search(r"\n +numCards: {}".format(num_slots), txt) is not None)

    def verify_no_dt_logs(self, dut_name):
        kw_results = self.send_cmd(dut_name, "debug hal run platform config-dump")
        txt = kw_results[0].cmd_obj.return_text

        return re.search(r"warnings/errors:\s+None", txt) is not None

    def verify_dt_log_error(self, dut_name, log_regex=None):
        """Verify that an error log was generated.  If log_regex is specified,
        it should be a regex expression, already escaped if necessary."""
        kw_results = self.send_cmd(dut_name, "debug hal run platform config-dump",
                                   ignore_cli_feedback=True)
        txt = kw_results[0].cmd_obj.return_text

        unable_to_load_str = "Unable to load configuration from file:"
        if log_regex:
            s_str = fr"warnings/errors:\s+^{unable_to_load_str}.*{log_regex}"
            return re.search(s_str, txt, re.M|re.S) is not None

        s_str = fr"warnings/errors:\s+^{unable_to_load_str}"
        return re.search(s_str, txt, re.M) is not None

    def verify_dt_log_warning(self, dut_name, log_regex=None):
        """Verify that a warning log was generated.  If log_regex is specified,
        it should be a regex expression, already escaped if necessary."""
        kw_results = self.send_cmd(dut_name, "debug hal run platform config-dump",
                                   ignore_cli_feedback=True)
        txt = kw_results[0].cmd_obj.return_text

        if log_regex:
            s_str = fr"warnings/errors:\s+^Warning:.*{log_regex}"
            return re.search(s_str, txt, re.M|re.S) is not None

        return re.search(r"warnings/errors:\s+^Warning:", txt, re.M) is not None

    def verify_cloudserver(self, dut_name, server):
        kw_results = self.send_cmd(dut_name, "debug hal run platform config-dump")
        txt = kw_results[0].cmd_obj.return_text

        if not server:
            # cloud-server was not specified...ensure a value isn't shown in the debug output
            return re.search(r"^\s+cloud-server:\s*$", txt, re.M) is not None

        return re.search(r"^\s+cloud-server: {}".format(re.escape(server)), txt, re.M) is not None

    def verify_cloudserver_type(self, dut_name, server_type):
        kw_results = self.send_cmd(dut_name, "debug hal run platform config-dump")
        txt = kw_results[0].cmd_obj.return_text

        return re.search(r"^\s+cloud-server-type: {}"
                         .format(re.escape(server_type)), txt, re.M) is not None

    def verify_card_states(self, dut_name, slot_nums, state):
        kw_results = self.send_cmd(dut_name, "debug cfgmgr show next dm.card_info")
        txt = kw_results[0].cmd_obj.return_text

        jdoc = json.loads(re.search(r"{[^\n]+}", txt).group())

        for slot in jdoc["data"]:
            if slot["slot"] in slot_nums:
                if slot["card_state_str"] != state:
                    return False

        return True

    def verify_node_states(self, dut_name, slot_nums, prim_slot_num):
        kw_results = self.send_cmd(dut_name, "debug cfgmgr show next dm.card_info")
        txt = kw_results[0].cmd_obj.return_text

        jdoc = json.loads(re.search(r"{[^\n]+}", txt).group())

        node_states = {True: "MASTER", False: "STANDBY"}
        for slot in jdoc["data"]:
            if slot["slot"] in slot_nums:
                if slot["node_state_str"] != node_states[slot["slot"] == prim_slot_num]:
                    return False

        return True

    def create_bundle(self, dut_name, dt_file):
        self.defaultLibrary.apiLowLevelApis.fileManagementUtils.save_current_config(dut_name)
        kw_results = self.send_cmd(dut_name, f"!python -m bundle_handler --overwrite --create "
                                   f"--file {dt_file}")
        txt = kw_results[0].cmd_obj.return_text

        if rf'Bundle "{dt_file}" created' not in txt:
            self.logger.error(f"{dt_file} not created")
            return False

        return True

    def upload_bundle(self, dut_name, vrid, local_file, filename, dt_file):
        kw_results = self.send_cmd(dut_name, f"!python -m bundle_handler --delete "
                                   f"--upload {pytest.upload_url} --file {dt_file} "
                                   f"--upload-file {filename} --vr {vrid}")
        txt = kw_results[0].cmd_obj.return_text

        if rf'Bundle "{dt_file}" uploaded' not in txt:
            self.logger.error(f"{dt_file} not uploaded")
            return False
        if rf'Bundle "{dt_file}" removed' not in txt:
            self.logger.error(f"{dt_file} not removed")
            return False

        # Ensure bundle was uploaded
        if not os.path.isfile(local_file):
            self.logger.error(f"{local_file} not uploaded")
            return False

        return True

    def download_bundle(self, dut_name, vrid, local_file, dt_file):
        if not os.path.isfile(local_file):
            self.logger.error(f"{local_file} does not exist")
            return False

        url = "/".join((pytest.download_url, os.path.basename(dt_file)))
        kw_results = self.send_cmd(dut_name, f"!python -m bundle_handler --overwrite "
                                   f"--download {url} --file {dt_file} --vr {vrid}")
        txt = kw_results[0].cmd_obj.return_text

        if rf'Bundle "{dt_file}" downloaded' not in txt:
            self.logger.error(f"{dt_file} not downloaded")
            return False

        return True

    def apply_bundle(self, dut_name, dt_file):
        kw_results = self.send_cmd(dut_name, f"!python -m bundle_handler --delete --apply "
                                   f"--file {dt_file}")
        txt = kw_results[0].cmd_obj.return_text

        if rf'Bundle "{dt_file}" applied' not in txt:
            self.logger.error(f"{dt_file} not applied")
            return False
        if rf'Bundle "{dt_file}" removed' not in txt:
            self.logger.error(f"{dt_file} not removed")
            return False

        return True

    def apply_bundle_failure(self, dut_name, dt_file, error_str):
        kw_results = self.send_cmd(dut_name, f"!python -m bundle_handler --delete --apply "
                                   f"--file {dt_file}", ignore_cli_feedback=True)
        txt = kw_results[0].cmd_obj.return_text

        if rf'Bundle "{dt_file}" applied' in txt:
            self.logger.error(f"{dt_file} was applied, but should have failed")
            return False

        # Apply failed.  Now ensure it failed for the correct reason
        if re.search(error_str, txt):
            return True

        return False
