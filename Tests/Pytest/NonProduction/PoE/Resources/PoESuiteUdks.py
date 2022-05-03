from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementPoeGenKeywords import NetworkElementPoeGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementCliSend import NetworkElementCliSend
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from time import sleep
from ExtremeAutomation.Keywords.FailureException import FailureException


class PoESuiteUdks:

    def __init__(self, pytest_config_helper):

        self.pytest_config_helper = pytest_config_helper
        self.default_library = DefaultLibrary()
        self.network_element_poe_gen_keywords = NetworkElementPoeGenKeywords()
        self.network_element_cli_send = NetworkElementCliSend()
        self.poe = self.default_library.apiLowLevelApis.poe

    def disable_and_verify_inline_power(self, dut_name):

        self.poe.poe_disable_inline_power(dut_name)
        sleep(3)
        self.poe.poe_verify_inline_power_disabled(dut_name)

    def enable_and_verify_inline_power(self, dut_name):

        self.poe.poe_enable_inline_power(dut_name)
        sleep(3)
        self.poe.poe_verify_inline_power_enabled(dut_name)

    def disable_and_verify_inline_power_port(self, dut_name, port):

        self.poe.poe_disable_port(dut_name, port)
        sleep(3)
        self.poe.poe_verify_inline_power_port_disabled(dut_name, port)

    def enable_and_verify_inline_power_port(self, dut_name, port):

        self.poe.poe_enable_port(dut_name, port)
        sleep(3)
        self.poe.poe_verify_inline_power_port_enabled(dut_name, port)

    def enable_and_verify_inline_power_legacy(self, dut_name, port):

        self.poe.poe_enable_inline_power_legacy(dut_name)
        sleep(3)
        self.poe.poe_verify_inline_power_legacy_enabled(dut_name, port)

    def disable_and_verify_inline_power_legacy(self, dut_name, port):

        self.poe.poe_disable_inline_power_legacy(dut_name)
        sleep(3)
        self.poe.poe_verify_inline_power_legacy_disabled(dut_name, port)

    def disconnect_deny_port_and_verify(self, dut_name):

        self.poe.poe_set_inline_power_disconnect_deny_port(dut_name)
        sleep(3)
        self.poe.poe_verify_inline_power_disconnect_deny_port(dut_name)

    def disconnect_lowest_priority_and_verify(self, dut_name):

        self.poe.poe_set_inline_power_disconnect_lowest_priority(dut_name)
        sleep(3)
        self.poe.poe_verify_inline_power_disconnect_lowest_priority(dut_name)

    def unconfigure_disconnect_and_verify(self, dut_name):

        self.poe.poe_clear_inline_power_disconnect(dut_name)
        sleep(3)
        self.poe.poe_verify_inline_power_unconfigure_disconnect(dut_name)

    def configure_and_verify_inline_power_label(self, dut_name, port, test_label):

        self.poe.poe_set_inline_power_label(dut_name, port, test_label)
        sleep(3)
        self.poe.poe_verify_inline_power_label(dut_name, port, test_label)

    def configure_and_verify_inline_power_operator_limit_min(self, dut_name, port, min_operator_limit):

        self.poe.poe_set_port_power_limit(dut_name, port, min_operator_limit)
        sleep(3)
        self.poe.poe_verify_inline_power_operator_limit(dut_name, port, min_operator_limit)

    def configure_and_verify_inline_power_operator_limit_max(self, dut_name, port, max_operator_limit):

        self.poe.poe_set_port_power_limit(dut_name, port, max_operator_limit)
        sleep(3)
        self.poe.poe_verify_inline_power_operator_limit(dut_name, port, max_operator_limit)

    def configure_and_verify_inline_power_operator_limit_less_than_min(self, dut_name, port, min_operator_limit, error_message):

        """
        min_operator_limit is less than the allowed values so the cli error is ignored
        """
        resp = self.poe.poe_set_port_power_limit(dut_name, port, min_operator_limit, ignore_error="Error")
        sleep(3)

        if error_message in resp[0].cmd_obj.return_text:
            return
        raise FailureException("Error '{}' not found in return error string".format(error_message))

    def configure_and_verify_inline_power_operator_limit_greater_than_max(self, dut_name, port, max_operator_limit, error_message):

        """
        max_operator_limit is greater than the allowed values so the cli error is ignored
        """

        resp = self.poe.poe_set_port_power_limit(dut_name, port, max_operator_limit, ignore_error="Error")
        sleep(3)

        if error_message in resp[0].cmd_obj.return_text:
            return
        raise FailureException("Error '{}' not found in return error string".format(error_message))

    def configure_and_verify_inline_power_priority(self, dut_name, port, priority):

        self.poe.poe_set_port_power_priority(dut_name, port, priority)
        sleep(3)
        self.poe.poe_verify_port_priority(dut_name, port, priority)

    def configure_and_verify_usage_threshold(self, dut_name, threshold):

        self.poe.poe_set_power_usage_threshold(dut_name, threshold)
        sleep(3)
        self.poe.poe_verify_power_threshold(dut_name, threshold)

    def configure_and_verify_invalid_usage_threshold(self, dut_name, threshold, error_message=None):

        resp = self.poe.poe_set_power_usage_threshold(dut_name, threshold, ignore_error='Error')
        sleep(3)

        if error_message in resp[0].cmd_obj.return_text:
            return
        raise FailureException("Error '{}' not found in return error string".format(error_message))

    def configure_and_verify_inline_power_detection(self, dut_name, port, detection_type):

        self.poe.poe_set_port_detect_type(dut_name, port, detection_type)
        sleep(3)

        detection_type_list = detection_type.split(' ')

        if len(detection_type_list) > 1:
            detection_type = '{} {}'.format(detection_type_list[1], detection_type_list[0])

        elif detection_type == 'legacy-and-802.3af':
            detection_type = '4-point legacy-and-802.3af'

        self.poe.poe_verify_port_detect_type(dut_name, port, detection_type)