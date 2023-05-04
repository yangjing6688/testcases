# Author        : Andreea Braitoru
# Description   : This script run the below tests for verifying the Power Supply Status details and PoE details for EXOS devices according with XIQ-3155 feature story
# Testcases     : TCXM-19906, TCXM-19907, TCXM-19911, TCXM-19912, TCXM-19914, TCXM-19915, TCXM-19919, TCXM-19920
# Comments      : This script is applicable for EXOS standalone and EXOS stacks

import pytest


@pytest.mark.testbed_stack
@pytest.mark.testbed_1_node
@pytest.mark.development
@pytest.mark.dependson("tcxm_xiq_onboarding")
class XIQ3155Tests:

    @pytest.fixture
    def make_sure_windows_are_closed(xiq_library_at_class_level):
        """ This fixture makes sure that the device360 window is closed at the TEARDOWN of the test case.
        """
        try:
            yield
        finally:
            try:
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            except:
                # device360 window is not opened
                pass

    @pytest.fixture
    def connect_to_switch(self, node, enter_switch_cli):
        with enter_switch_cli(node):
            yield

    @pytest.fixture(scope="class", autouse=True)
    def poe_stack_slots(self, cli, node, enter_switch_cli):
        with enter_switch_cli(node):
            output = cli.get_stack_slot_poe(node) if node.platform.upper() == "STACK" else None
        return output

    @pytest.mark.skip_if_node_does_not_support_poe
    @pytest.mark.tcxm_19906
    @pytest.mark.p1
    def test_verify_poe_details_tcxm19906(
        self, xiq_library_at_class_level, node, cli, poll, logger, connect_to_switch, make_sure_windows_are_closed, poe_stack_slots):
        """
        TCXM-19906 - Verify if PoE details showing in XIQ are same as the details showing in CLI - EXOS standalone
        TCXM-19914 - Verify if PoE details showing in XIQ are same as the details showing in CLI - EXOS stack
        """
        
        try:
            for cli_values in poll(lambda: cli.get_cli_poe_details(node), max_poll_time=600):
 
                if node.platform.upper() == "STACK":
                    res = True
                    
                    for slot in poe_stack_slots:
                        try:
                            slot_power_details = xiq_library_at_class_level.xflowsmanageDevice360.device360_power_details_stack(
                                slot=slot, device_mac=node.mac)
                        except Exception as exc:
                            logger.warning(exc)
                            res = False
                        else:
                            if not any(cli_values_elem in slot_power_details for cli_values_elem in cli_values):
                                res = False
                                logger.warning("Values for stack are not the same both in CLI and XIQ")
                            else:
                                logger.info("Values for stack are the same both in CLI and XIQ")
                            
                    if res:
                       break 
                else:               
                    try:
                        power_details = xiq_library_at_class_level.xflowsmanageDevice360.device360_power_details(device_mac=node.mac, device_name="")
                    except Exception as exc:
                        logger.warning(exc)
                        continue

                    if any(cli_values_elem in power_details for cli_values_elem in cli_values):
                        logger.info("Values are the same both in CLI and XIQ")
                        break
        except TimeoutError:
            pytest.fail("The values are not the same")

    @pytest.mark.skip_if_node_does_not_support_poe
    @pytest.mark.tcxm_19907
    @pytest.mark.p1
    def test_verify_psu_details_tcxm19907(
        self, node, xiq_library_at_class_level, cli, logger, utils, make_sure_windows_are_closed, poll, connect_to_switch, poe_stack_slots):
        """
        TCXM-19907 - Veriy if Power Supply Status details values are shown correctly in XIQ - EXOS standalone
        TCXM-19915 - Veriy if Power Supply Status details values are shown correctly in XIQ - EXOS stack
        """
        try:
            for power_details_cli in poll(lambda: cli.get_cli_psu_details(node), max_poll_time=600):

                *_, power_consumed_cli = power_details_cli
                logger.debug(f"{power_consumed_cli=}")

                if node.platform.upper() == "STACK":
                    
                    length_list = len(power_details_cli)
                    middle_index = length_list // 2
                    first_half_operational = power_details_cli[:middle_index]
                    second_half_usage = power_details_cli[middle_index:]
                    res = True
                
                    for count, slot in enumerate(poe_stack_slots):
                            
                        slot_power_details = xiq_library_at_class_level.xflowsmanageDevice360.device360_power_details_stack(slot=slot, device_mac=node.mac)
                        logger.info(f"Power details BGD:  {slot_power_details}")
                        power_consumed_xiq = utils.get_regexp_matches(slot_power_details, r"\w+['Total']\s+\w+['Power']\s+\w+['Consumed:']\s+(\d+)", 1)[1]
                        logger.info(f"Power consumed : {power_consumed_xiq}")
                        logger.info(f"check it into power details: {first_half_operational[count]}")
                        
                        if first_half_operational[count] in slot_power_details:
                            logger.info(f"Operational power values are the same for slot {slot}")
                        else:
                            res = False
                            logger.info(f"Fail first condition : {(int(second_half_usage[count]) + 1)  , int(power_consumed_xiq)}")
                            
                        if (int(second_half_usage[count]) + 1) >= int(power_consumed_xiq) or (int(second_half_usage[count]) - 1) <= int(power_consumed_xiq):
                            logger.info(f"Usage power values are the same for slot {slot}")
                        else:
                            res = False
                            logger.info(f"Fail second condition : {(int(second_half_usage[count]) + 1) , int(power_consumed_xiq)}")
                    
                    if res:
                        break
                    
                else:
                    power_details = xiq_library_at_class_level.xflowsmanageDevice360.device360_power_details(device_mac=node.mac, device_name="")
                    power_consumed_xiq = utils.get_regexp_matches(power_details, r"\w+['Total']\s+\w+['Power']\s+\w+['Consumed:']\s+(\d+)", 1)[1]
                    
                    t = 0.1
                    
                    if (1 - t) * int(power_consumed_cli) <= int(power_consumed_xiq) <= (1 + t) * int(power_consumed_cli):
                        logger.info("Values are the same both in CLI and XIQ")
                        break
                    
        except TimeoutError:
            pytest.fail("The values are not the same")

    @pytest.mark.skip_if_node_does_not_support_poe
    @pytest.mark.tcxm_19911
    @pytest.mark.p2
    def test_change_threshold_power_from_cli_tcxm19911(
        self, node, xiq_library_at_class_level, cli, poll, logger, make_sure_windows_are_closed, connect_to_switch, poe_stack_slots):
        """
        TCXM-19911 - Change the POE Threshold Power value from CLI and verifiy that the value si shown correctly in XIQ - EXOS standalone
        TCXM-19919 - Change the POE Threshold Power value from CLI and verifiy that the value si shown correctly in XIQ - EXOS stack
        """
        cli_values = cli.change_threshold_power_from_cli(dut=node, os=node.cli_type, new_threshold_value=50)

        try:
            for _ in poll(lambda: (), max_poll_time=600):
                
                if node.platform.upper() == "STACK":
                    
                    res = True
                    
                    for slot in poe_stack_slots:
                        slot_power_details = xiq_library_at_class_level.xflowsmanageDevice360.device360_power_details_stack(slot=slot, device_mac=node.mac)
                        logger.info(f"power details: {slot_power_details}")
                        if cli_values[0] in slot_power_details and cli_values[1] in slot_power_details:
                            logger.info(f"Values are the same both in CLI and XIQ for slot: {slot}")
                        else:
                            res = False
                    if res:
                        logger.info("Values are the same both in CLI and XIQ")
                        break
                else:
                    power_details = xiq_library_at_class_level.xflowsmanageDevice360.device360_power_details(device_mac=node.mac, device_name="")
                    if cli_values[0] in power_details and cli_values[1] in power_details:
                        logger.info("Values are the same both in CLI and XIQ")
                        break
                    logger.debug(f"{power_details=}, {cli_values=}")

        except TimeoutError:
            pytest.fail("The values are not the same")

    @pytest.mark.skip_if_node_does_not_support_poe
    @pytest.mark.tcxm_19912
    @pytest.mark.p2
    def test_change_threshold_power_from_xiq_tcxm19912(
        self, node, xiq_library_at_class_level, cli, logger, make_sure_windows_are_closed,
        connect_to_switch, dev_cmd, request, utils, poe_stack_slots):
        """
        TCXM-19912 - Change the POE Threshold Power value from XIQ and verifiy that the value si shown correctly in CLI - EXOS standalone
        TCXM-19920 - Change the POE Threshold Power value from XIQ and verifiy that the value si shown correctly in CLI - EXOS stack
        """

        def func():
            cli.change_threshold_power_from_cli(dut=node, new_threshold_value='70')
            dev_cmd.send_cmd(node.name, 'save config file ', confirmation_phrases='overwrite it? (y/N)', confirmation_args='yes')
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            xiq_library_at_class_level.xflowsmanageDevices.revert_device_to_template(node.mac)
            
        request.addfinalizer(func)

        threshold_value = 50

        if node.platform.upper() == "STACK":
            for slot in poe_stack_slots:
                threshold_power_XIQ_modified = xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_poe_threshold_value_stack(
                    threshold_value=threshold_value, slot=slot, device_mac=node.mac)
                assert threshold_power_XIQ_modified == 1, "The Threshold Power value can't be updated"
        else:
            threshold_power_xiq_modified = xiq_library_at_class_level.xflowsmanageDevice360.device360_configure_poe_threshold_value(
                threshold_value=threshold_value, device_mac=node.mac)
            
            assert threshold_power_xiq_modified == 1, "The Threshold Power value can't be updated"
            
        utils.wait_till(timeout=10)
        
        if node.platform.upper() == "STACK":
            assert xiq_library_at_class_level.xflowsmanageDevices.update_policy_and_configuration_stack(node.mac) == 1
        else:
            assert xiq_library_at_class_level.xflowsmanageDevices.update_switch_policy_and_configuration(device_mac=node.mac) == 1
        
        cli_values_updated = cli.get_cli_poe_details_updated(node)

        if cli_values_updated != threshold_value:
            logger.info(f"cli_values_updated : {cli_values_updated}")
            pytest.fail("The values are not the same")
