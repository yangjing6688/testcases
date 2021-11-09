from Tests.Pytest.Functional.nonprod.PoE.Resources.PoEBase import PoEBase


class InlinePowerPriorityTests(PoEBase):

    def test_06_01_verify_configure_inline_power_low_priority(self):

        dut_name = self.test_bed.dut1.name
        port = self.test_bed.dut1.port_a
        priority = 'Low'

        self.udks.configure_and_verify_inline_power_priority(dut_name, port, priority)

    def test_06_01_verify_configure_inline_power_high_priority(self):

        dut_name = self.test_bed.dut1.name
        port = self.test_bed.dut1.port_a
        priority = 'High'

        self.udks.configure_and_verify_inline_power_priority(dut_name, port, priority)

    def test_06_01_verify_configure_inline_power_critical_priority(self):

        dut_name = self.test_bed.dut1.name
        port = self.test_bed.dut1.port_a
        priority = 'Critical'

        self.udks.configure_and_verify_inline_power_priority(dut_name, port, priority)
