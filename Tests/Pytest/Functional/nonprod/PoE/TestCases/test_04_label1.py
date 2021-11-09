from Tests.Pytest.Functional.nonprod.PoE.Resources.PoEBase import PoEBase


class InlinePowerLabelTests(PoEBase):

    def test_04_01_verify_inline_power_label(self):
        """
        todo: set label name in yaml file
        """
        test_label = 'testLabel'
        dut_name = self.test_bed.dut1.name
        port = self.test_bed.dut1.port_a
        self.udks.configure_and_verify_inline_power_label(dut_name, port, test_label)
