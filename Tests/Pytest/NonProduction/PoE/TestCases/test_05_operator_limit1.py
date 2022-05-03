from Tests.Pytest.NonProduction.PoE.Resources.PoEBase import PoEBase


class InlinePowerOperatorLimitTests(PoEBase):

    def test_05_01_verify_configure_inline_power_operator_limit_min_value(self):
        dut_name = self.test_bed.dut1.name
        port = self.test_bed.dut1.port_a

        """
        3w is standard min operator limit
        todo: set the min limit in the yaml file
        """
        min_operator_limit = 3 * 1000  # EXOS switch accepts in mW ( milli watts )

        self.udks.configure_and_verify_inline_power_operator_limit_min(dut_name, port, min_operator_limit)

    def test_05_02_verify_configure_inline_power_operator_limit_max_value(self):
        """
        max limit depends on variants
        variant U supports upto 60W
        variant W supports upto 90W
        variant P supports upto 30W

        todo: set the max limit in the yaml file
        """

        dut_name = self.test_bed.dut1.name
        port = self.test_bed.dut1.port_a
        max_operator_limit = 30 * 1000  # EXOS switch accepts in mW ( milli watts )

        self.udks.configure_and_verify_inline_power_operator_limit_max(dut_name, port, max_operator_limit)

    def test_05_03_verify_configure_inline_power_operator_limit_less_than_min_value(self):
        dut_name = self.test_bed.dut1.name
        port = self.test_bed.dut1.port_a

        """
        3w is standard min operator limit
        todo: set the min limit in the yaml file
        """
        min_operator_limit = 2 * 1000  # EXOS switch accepts in mW ( milli watts )
        error_message = "Error: Invalid operator-limit value."

        self.udks.configure_and_verify_inline_power_operator_limit_less_than_min(dut_name, port, min_operator_limit, error_message)

    def test_05_04_verify_configure_inline_power_operator_limit_greater_than_max_value(self):
        """
        max limit depends on variants
        variant U supports upto 60W
        variant W supports upto 90W
        variant P supports upto 30W

        todo: set the max limit in the yaml file
        """

        dut_name = self.test_bed.dut1.name
        port = self.test_bed.dut1.port_a
        max_operator_limit = 90 * 1000 + 500  # EXOS switch accepts in mW ( milli watts )
        error_message = "Error: Invalid operator-limit value."

        self.udks.configure_and_verify_inline_power_operator_limit_greater_than_max(dut_name, port, max_operator_limit, error_message)
