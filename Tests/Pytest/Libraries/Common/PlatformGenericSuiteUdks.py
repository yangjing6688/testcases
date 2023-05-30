from ExtremeAutomation.Keywords.Utils.NetworkUtils import NetworkUtils
from ExtremeAutomation.Keywords.NetworkElementKeywords.StaticKeywords.NetworkElementFirmwareUtilsKeywords import NetworkElementFirmwareUtilsKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils.NetworkElementCliSend import NetworkElementCliSend


# Documentation   These are Keywords that can be used for all EXOS platforms as needed.

class PlatformGenericSuiteUdks():
    def __init__(self):
        self.networkElementFirmwareUtilsKeywords = NetworkElementFirmwareUtilsKeywords()
        self.networkElementCliSend = NetworkElementCliSend()
        self.networkUtils = NetworkUtils()

    def Upgrade_Netelem_to_Latest_Firmware(self, netelem_name, tftp_server_ip, build_location, build, mgmt_vlan, netelem_ip):
        # Upgrades the provided netelem to the latest firmware on the TFTP server provided.
        # Wait Until Keyword Succeeds  3x  200ms  
        self.networkElementFirmwareUtilsKeywords.load_firmware_on_network_element(netelem_name,tftp_server_ip, build_location, vr=mgmt_vlan, server_type='https')
        #
        #  I don't think we should need to reboot and then unconfigure and reboot, hopefully an unconfigure (which causes
        #    a reboot will suffice.
        #
        #    reboot_network_element_now_and_wait  ${netelem_name}  300  20  60
    
        self.networkElementCliSend.send_cmd(netelem_name, 'unconfigure switch' , wait_for_prompt=False)
        self.networkElementCliSend.send_cmd(netelem_name, 'y' , check_initial_prompt=False)
        self.networkUtils.wait_for_pingable(netelem_ip, 300, 20, 30)
        self.networkElementFirmwareUtilsKeywords.firmware_version_should_be_equal(netelem_name, build)
        #
        #  On stacked systems we may need to wait a bit for the configs to sync so we will put in a simple test here
        #    the show config will return an error if stack element configurations are not yet synced up.
        #  CAVEAT though.. after reboot there is a short window that commands can be entered, then a short window where they
        #    cannot be entered followed by the normal processing of commands.
        #
        self.networkElementCliSend.send_cmd(netelem_name, 'show config ntp')
        