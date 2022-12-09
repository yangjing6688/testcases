import pytest
import os

from Tests.Pytest.SystemTest.XIQ.Wired.Resources.SuiteUdks import SuiteUdks


@pytest.mark.p1
@pytest.mark.development
@pytest.mark.testbed_1_node
class OnboardDeviceVSP4900UsingCsvTests:
    """ Make sure that the location which is provided in the yaml file for dut1 is created in XIQ before the run of these tests.

    Ran these test cases when the location of dut1 is 'auto_location_01, Santa Clara, building_02, floor_04'.
    """

    current_directory = os.path.dirname(os.path.abspath(__file__))
    suite_udks = SuiteUdks()

    @pytest.fixture(scope="class")
    def csv_file_location_1(self, dut1):
        try:
            csv_file_location = self.suite_udks.create_csv_file(work_dir=self.current_directory,
                                        dut_serial=dut1.serial,
                                        platform=dut1.platform)
            yield csv_file_location
        finally:
            self.suite_udks.delete_csv(csv_file_location)

    @pytest.fixture(scope="class")
    def csv_file_location_2(self, dut1):
        try:
            csv_file_location = self.suite_udks.create_csv_file(work_dir=self.current_directory,
                                                    dut_serial=dut1.serial,
                                                    platform=dut1.platform,
                                                    location=",".join(dut1.location.split(", ")[1:]))
            yield csv_file_location
        finally:
            self.suite_udks.delete_csv(csv_file_location)

    @pytest.fixture(scope="class", autouse=True)
    def setup(self, dut1, cli, open_spawn, loaded_config, check_devices_are_reachable):

        check_devices_are_reachable([dut1])

        with open_spawn(dut1) as spawn_connection:
            if loaded_config.get("lab", "").upper() == "SALEM":
                cli.downgrade_iqagent(dut1.cli_type, spawn_connection)

            cli.configure_device_to_connect_to_cloud(
                dut1.cli_type, loaded_config['sw_connection_host'],
                spawn_connection, vr=dut1.mgmt_vr, retry_count=30
            )

            if dut1.cli_type.upper() == "EXOS":
                cli.send(spawn_connection, "enable iqagent")

    @pytest.fixture
    def cleanup(self, xiq_library_at_class_level, dut1):
        try:
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=dut1.serial)
            yield
        finally:
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=dut1.serial)

    @pytest.mark.tccs_7651
    def test_onboard_device_using_csv_without_location(self, test_data, xiq_library_at_class_level, dut1, logger, csv_file_location_1, cleanup):
        '''[Documentation]  Test_Objective: Verify a device can be onboared using a csv file'''

        res = xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(
            {**dut1, "csv_location": csv_file_location_1, "device_make": dut1.make})

        if res != 1:
            pytest.fail(f'Could not onboard device {dut1.platform} with serial {dut1.serial}')

        logger.info(f'Device {dut1.platform} with serial {dut1.serial} has been onboarded')

        xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(dut1.serial)

        managed_res = xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(dut1.serial)

        if managed_res == 1:
            logger.info('Status for device with serial number: {} is equal to managed'.format(dut1.serial))
        else:
            pytest.fail('Status for serial {} not equal to managed: {}'.format(dut1.serial, managed_res))

        res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(device_serial=dut1.serial)
        if res != 'green':
            pytest.fail('Status for serial {} not equal to Green: {}'.format(dut1.serial, res))
        else:
            logger.info('Status for device with serial number: {} is equal to Green'.format(dut1.serial))

        device_location = self.suite_udks.get_value_specific_column(xiq_library_at_class_level, dut1.serial, "LOCATION")

        location_to_verify = "Assign Location"
        if device_location != location_to_verify:
            pytest.fail('Current location {} did not match the expected location {} assigned to device {} having serial {}'.format(
                    device_location, location_to_verify, dut1.platform, dut1.serial))
        else:
            logger.info('Current location {} matched the expected location {} assigned to device {} having serial {}'.format(
                device_location, location_to_verify, dut1.platform, dut1.serial))

    @pytest.mark.tccs_7651
    def test_onboard_device_using_csv_with_location(self, test_data, xiq_library_at_class_level, dut1, logger, csv_file_location_1, cleanup):
        '''[Documentation]  Test_Objective: Verify a device can be onboared using a csv file and selecting the location field'''

        res = xiq_library_at_class_level.xflowscommonDevices.quick_onboarding_cloud_csv(
            csv_location=csv_file_location_1, location=",".join(dut1.location.split(", ")[1:]), device_make=dut1.make)

        if res != 1:
            pytest.fail(f'Could not onboard device {dut1.platform} with serial {dut1.serial}')
        else:
            logger.info(f'Device {dut1.platform} with serial {dut1.serial} has been onboarded')

        xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(dut1.serial)

        managed_res = xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(dut1.serial)

        if managed_res == 1:
            logger.info('Status for device with serial number: {} is equal to managed'.format(dut1.serial))
        else:
            pytest.fail('Status for serial {} not equal to managed: {}'.format(dut1.serial, managed_res))

        res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(device_serial=dut1.serial)
        if res != 'green':
            pytest.fail('Status for serial {} not equal to Green: {}'.format(dut1.serial, res))
        else:
            logger.info('Status for device with serial number: {} is equal to Green'.format(dut1.serial))

        location_to_verify = self.suite_udks.expected_location_in_gui(",".join(dut1.location.split(", ")[1:]))

        device_location = self.suite_udks.get_value_specific_column(xiq_library_at_class_level, dut1.serial, "LOCATION")

        if location_to_verify not in device_location:
            pytest.fail('Current location {} did not match the expected location {} assigned to device {}'.format(
                device_location, location_to_verify, dut1.serial))
        else:
            logger.info('Current location {} matched the expected location {} assigned to device {}'.format(
                device_location, location_to_verify, dut1.serial))

    @pytest.mark.tccs_7651
    def test_onboard_device_using_csv_with_location_in_csv(self, test_data, xiq_library_at_class_level, dut1, logger, csv_file_location_2, cleanup):
        '''[Documentation]  Test_Objective: Verify a device can be onboared using a csv file with location in csv file
        Starting in 22R5 version of XIQ the location in the csv file will be ignore, updated test case to check that the
        location is equal to Assign Location'''

        res = xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(
            {**dut1, "csv_location": csv_file_location_2, "device_make": dut1.make})

        if res != 1:
            pytest.fail(f'Could not onboard device {dut1.platform} with serial {dut1.serial}')
        else:
            logger.info(f'Device {dut1.platform} with serial {dut1.serial} has been onboarded')

        xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(dut1.serial)

        managed_res = xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(dut1.serial)

        if managed_res == 1:
            logger.info('Status for device with serial number: {} is equal to managed'.format(dut1.serial))
        else:
            pytest.fail('Status for serial {} not equal to managed: {}'.format(dut1.serial, managed_res))

        res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(device_serial=dut1.serial)
        if res != 'green':
            pytest.fail('Status for serial {} not equal to Green: {}'.format(dut1.serial, res))
        else:
            logger.info('Status for device with serial number: {} is equal to Green'.format(dut1.serial))

        location_to_verify = "Assign Location"

        device_location = self.suite_udks.get_value_specific_column(xiq_library_at_class_level, dut1.serial, "LOCATION")

        if location_to_verify not in device_location:
            pytest.fail('Current location {} did not match the expected location {} assigned to device {}'.format(
                device_location, location_to_verify, dut1.serial))
        else:
            logger.info('Current location {} matched the expected location {} assigned to device {}'.format(
                device_location, location_to_verify, dut1.serial))
