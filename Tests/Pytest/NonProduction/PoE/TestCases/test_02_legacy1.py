from Tests.Pytest.NonProduction.PoE.Resources.PoEBase import PoEBase


class InlinePowerLegacyTests(PoEBase):

    def test_02_01_verify_enable_inline_power_legacy(self):
        self.udks.enable_and_verify_inline_power_legacy(self.test_bed.dut1.name, self.test_bed.dut1.port_a)

    def test_02_02_verify_disable_inline_power_legacy(self):
        self.udks.disable_and_verify_inline_power_legacy(self.test_bed.dut1.name, self.test_bed.dut1.port_a)