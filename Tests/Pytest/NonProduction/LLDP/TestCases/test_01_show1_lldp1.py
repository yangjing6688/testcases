from Tests.Pytest.NonProduction.LLDP.Resources.LLDPBase import LLDPBase
from pytest import mark


class ShowLLDPTests(LLDPBase):

    def test_01_01_show_lldp_interval(self):
        self.udks.verify_tx_interval(self.test_bed.dut1_name)
