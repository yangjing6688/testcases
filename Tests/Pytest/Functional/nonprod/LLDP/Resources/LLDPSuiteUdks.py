from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementLldpGenKeywords import NetworkElementLldpGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementCliSend import NetworkElementCliSend


class LLDPSuiteUdks:

    def __init__(self, pytest_config_helper):

        self.pytest_config_helper = pytest_config_helper
        self.networkElementLldpGenKeywords = NetworkElementLldpGenKeywords()
        self.networkElementCliSend = NetworkElementCliSend()

    def verify_tx_interval(self, dut_name):
        self.networkElementLldpGenKeywords.lldp_verify_tx_interval(dut_name, '30')
