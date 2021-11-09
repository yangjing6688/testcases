from Tests.Pytest.Functional.nonprod.PoE.Resources.PoEBase import PoEBase


class InlinePowerDetectionTests(PoEBase):

    """
    configure inline-power detection bypass ports 1
    configure inline-power detection 802.3af-only ports 1
    configure inline-power detection legacy-and-802.3af 2-point ports 1
    configure inline-power detection legacy-and-802.3af 4-point ports 1
    configure inline-power detection legacy-and-802.3af ports 1 (default: 4-point)
    """

    def test_08_01_verify_configure_inline_power_bypass_detection(self):

        dut_name = self.test_bed.dut1.name
        port = self.test_bed.dut1.port_a
        detection_type = 'bypass'

        self.udks.configure_and_verify_inline_power_detection(dut_name, port, detection_type)

    def test_08_02_verify_configure_inline_power_802_3_af_detection(self):

        dut_name = self.test_bed.dut1.name
        port = self.test_bed.dut1.port_a
        detection_type = '802.3af-only'

        self.udks.configure_and_verify_inline_power_detection(dut_name, port, detection_type)

    def test_08_03_verify_configure_inline_power_legacy_and_802_3_af_2_point_detection(self):

        dut_name = self.test_bed.dut1.name
        port = self.test_bed.dut1.port_a
        detection_type = 'legacy-and-802.3af 2-point'

        self.udks.configure_and_verify_inline_power_detection(dut_name, port, detection_type)

    def test_08_04_verify_configure_inline_power_legacy_and_802_3_af_4_point_detection(self):

        dut_name = self.test_bed.dut1.name
        port = self.test_bed.dut1.port_a
        detection_type = 'legacy-and-802.3af 4-point'

        self.udks.configure_and_verify_inline_power_detection(dut_name, port, detection_type)

    def test_08_05_verify_configure_inline_power_legacy_and_802_3_af_detection(self):

        dut_name = self.test_bed.dut1.name
        port = self.test_bed.dut1.port_a
        detection_type = 'legacy-and-802.3af'

        self.udks.configure_and_verify_inline_power_detection(dut_name, port, detection_type)
