from Tests.Pytest.Functional.nonprod.PoE.Resources.PoEBase import PoEBase


class InlinePowerDisconnectPrecedenceTests(PoEBase):

    def test_03_01_verify_configure_inline_power_disconnect_deny_port(self):
        self.udks.disconnect_deny_port_and_verify(self.test_bed.dut1.name)

    def test_03_02_verify_configure_inline_power_disconnect_lowest_priority(self):
        self.udks.disconnect_lowest_priority_and_verify(self.test_bed.dut1.name)

    def test_03_03_verify_unconfigure_inline_power_disconnect(self):
        self.udks.unconfigure_disconnect_and_verify(self.test_bed.dut1.name)