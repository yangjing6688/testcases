from Tests.Pytest.NonProduction.PoE.Resources.PoEBase import PoEBase


class InlinePowerTests(PoEBase):

    def test_01_01_verify_disable_inline_power(self):
        self.udks.disable_and_verify_inline_power(self.test_bed.dut1.name)

    def test_01_02_verify_enable_inline_power(self):
        self.udks.enable_and_verify_inline_power(self.test_bed.dut1.name)

    def test_01_03_verify_disable_inline_power_port(self):
        self.udks.disable_and_verify_inline_power_port(self.test_bed.dut1.name, self.test_bed.dut1.port_a)

    def test_01_04_verify_enable_inline_power_port(self):
        self.udks.enable_and_verify_inline_power_port(self.test_bed.dut1.name, self.test_bed.dut1.port_a)
