from Tests.Pytest.NonProduction.PoE.Resources.PoEBase import PoEBase
import random


class InlinePowerUsageThresholdTests(PoEBase):

    def test_07_01_verify_configure_valid_usage_threshold(self):

        dut_name = self.test_bed.dut1.name
        threshold = str(random.randrange(1, 99))

        self.udks.configure_and_verify_usage_threshold(dut_name, threshold)

    def test_07_02_verify_configure_invalid_usage_threshold(self):

        dut_name = self.test_bed.dut1.name
        threshold = str(random.choice([0, 100]))
        error_message = "Invalid usage-threshold percentage"

        self.udks.configure_and_verify_invalid_usage_threshold(dut_name, threshold, error_message)
