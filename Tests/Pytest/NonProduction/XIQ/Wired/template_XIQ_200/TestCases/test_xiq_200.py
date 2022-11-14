""" 
    How to run Pytest tests using the runlist argument.

1 - Choose a name for the test class. First look in the project so you won't choose a name that is already being used.
    The class name should end with "Tests".
    
2 - Create the test functions in the said test class.
    Each name shoud begin with "test_".
    The "test_data" fixture is mandatory for every test function.
    
    The function should have only a test code marker (e.g. tcxm_XXXX, tcss_XXXX). 
    The only exception is when the tests are parameterized in the suitemap.
    Please check the "test_4" test of the "NewTestbedOneNodeTests" class.
    
    The test function should have only a testbed marker.
    
    The test function should have only a priority marker.

3 - Add this marker to your tests that need to test the onboarded nodes:
    @pytest.mark.dependson("tcxm_xiq_onboarding")
    By using this marker we make sure that the tests are skipped if the onboarding test fails.

4 - Create a suitemap yaml file. In this file you should define the tests you created.
    The "author", "tc" and "description" fields are mandatory.
    Each definition from suitemap can be accesses in corresponding test through the test_data fixture.
    ! Please check the suitemap.yaml file that is already created in this branch !
    
5 - Create a runlist yaml file. In this file you should put the tests you created in the specific order you want.
    In this file you must put the sutiemap file you have just created.
    ! Please check the runlist.yaml file that is already created in this branch !


The run command:
    pytest 
        --runlist extreme_automation_tests/vstefan/runlist.yaml // the path to the runlist file
        extreme_automation_tests/Tests/Pytest/NonProduction/XIQ // the path to the directory that contains the tests
        --tc-file extreme_automation_tests/vstefan/topo.yaml    // the topo yaml
        --tc-file extreme_automation_tests/vstefan/devices.yaml // the devices yaml
        --tc-file extreme_automation_tests/vstefan/env.yaml     // the env yaml
    

"""
import pytest


@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.testbed_1_node
class NewTestbedOneNodeTests:

    """ The tests marked with testbed_1_node run when in the given devices.yaml file there is at least a netelem.
        If the devices.yaml does not contain any netelem then the testbed_1_node tests will be removed from the test run.
    """
    
    @pytest.mark.tcxm_201
    @pytest.mark.p1
    def test_1(self, logger, test_data, xiq_library_at_class_level, test_bed):
        
        """ 
        The "xiq_library_at_class_level" fixture creates a XiqLibrary object before the start of the first test of this class.
        After the last test ran, the created XiqLibrary object is deleted.
        
        The "test_bed" fixture contains most of the tools needed for automation.
        e.g. 
            test_bed.node_1
            test_bed.node_2
            test_bed.node_stack
            test_bed.node_list
            test_bed.node_1_onboarding_options
            test_bed.node_2_onboarding_options
            test_bed.node_stack_onboarding_options
            test_bed.standalone_onboarding_options
            test_bed.onboarding_locations
            test_bed.node_1_onboarding_location
            test_bed.node_2_onboarding_location
            test_bed.node_stack_onboarding_location
            test_bed.created_onboarding_locations
            test_bed.policy_config
            test_bed.node_1_policy_config
            test_bed.node_2_policy_config
            test_bed.node_stack_policy_config
            test_bed.node_1_policy_name
            test_bed.node_2_policy_name
            test_bed.node_stack_policy_name
            test_bed.node_1_template_name
            test_bed.node_2_template_name
            test_bed.node_stack_template_name
            test_bed.node_stack_model_units
            test_bed.dut_1
            test_bed.dut_2
            test_bed.dut_3
            test_bed.dut_4
            test_bed.cli
            test_bed.network_manager
            test_bed.cloud_driver
            test_bed.utils
            test_bed.default_library
            test_bed.auto_actions
            test_bed.get_xiq_library
            test_bed.deactivate_xiq_library
            test_bed.open_spawn
            test_bed.navigator
            test_bed.dev_cmd
            test_bed.enter_switch_cli
        """
        
        logger.info(f"This test is {test_data['tc']}")
        logger.info(f"This test is writen by {test_data['author']}")
        
        node_1 = test_bed.node_1
        
        logger.info(f"The onboarded node has MAC='{node_1.mac}'.")
        
        logger.info(f"This policy is applied to node_1: '{test_bed.node_1_policy_name}'.")
        
        logger.info(f"This switch template was created for node_1: '{test_bed.node_1_template_name}'.")
        
        logger.info(f"This is the onboarding location for node_1: '{test_bed.node_1_onboarding_location}'.")

    @pytest.mark.tcxm_202
    @pytest.mark.p1
    def test_2(self, test_data, logger, test_bed):
        
        logger.info(f"This test is {test_data['tc']}")
        logger.info(f"This test is writen by {test_data['author']}")

        with test_bed.open_spawn(test_bed.node_1) as spawn_connection:
            
            test_bed.cli.disconnect_device_from_cloud(test_bed.node_1.cli_type, spawn_connection)
            
            test_bed.cli.configure_device_to_connect_to_cloud(
                test_bed.node_1.cli_type, test_bed.config['sw_connection_host'],
                spawn_connection, vr=test_bed.virtual_routers.get(test_bed.node_1.name, 'VR-Mgmt'), retry_count=30
            )

    @pytest.mark.tcxm_203
    @pytest.mark.p1
    def test_3(self, test_data, logger, test_bed):

        logger.info(f"This test is {test_data['tc']}")
        logger.info(f"This test is writen by {test_data['author']}")
        
        with test_bed.enter_switch_cli(test_bed.node_1) as dev_cmd:
            output = dev_cmd.send_cmd(test_bed.node_1.name, "show iqagent" if test_bed.node_1.cli_type.upper() == "EXOS" else "show filter acl")

        logger.cli(output[0].return_text)

    @pytest.mark.tcxm_204
    @pytest.mark.tcxm_205
    @pytest.mark.p1
    def test_4(self, test_data, logger, test_bed):
        
        """
        This test function will run twice, each time as a different test.
        Their order depends on the order they are placed in the runlist yaml.
        The only scenario when a test function can have two test markers (in this test case tcxm_204 and tcxm_205) is when the test function is parameterized with the values from suitemap.
        test_data['tc'] can be "tcxm_204" or "tcxm_205"
        
        ! Please check the suitemap.yaml to see how the test functions can be parameterized !
        """
        
        logger.info(f"This test is {test_data['tc']}")
        logger.info(f"This test is writen by {test_data['author']}")

        with test_bed.open_spawn(test_bed.node_1) as spawn_connection:
            
            test_bed.cli.disconnect_device_from_cloud(test_bed.node_1.cli_type, spawn_connection)
            
            test_bed.cli.configure_device_to_connect_to_cloud(
                test_bed.node_1.cli_type, test_bed.config['sw_connection_host'],
                spawn_connection, vr=test_bed.virtual_routers.get(test_bed.node_1.name, 'VR-Mgmt'), retry_count=30
            )


@pytest.mark.testbed_none
class NewTestbedNoneTests:

    """ The tests that are marked with testbed_none run even if in the devices.yaml there isn't any netelem.
    """
    
    @pytest.mark.tcxm_206
    @pytest.mark.p1
    def test_6(self, logger, test_data, xiq_library_at_class_level):
        logger.info(f"This test is {test_data['tc']}")
        logger.info(f"This test is writen by {test_data['author']}")

    @pytest.mark.tcxm_207
    @pytest.mark.p1
    def test_7(self, test_data, logger):
        logger.info(f"This test is {test_data['tc']}")
        logger.info(f"This test is writen by {test_data['author']}")


@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.testbed_2_node
class NewTestbedTwoNodeTests:

    """ The tests that are marked with testbed_2_node run only when in the devices.yaml are at least two netelems.
    """
    
    @pytest.mark.tcxm_208
    @pytest.mark.p1
    def test_8(self, logger, test_data, xiq_library_at_class_level, test_bed):
        
        logger.info(f"This test is {test_data['tc']}")
        logger.info(f"This test is writen by {test_data['author']}")

        node_1 = test_bed.node_1
        
        logger.info(f"The first onboarded node has MAC='{node_1.mac}'.")
        
        logger.info(f"This policy is applied to node_1: '{test_bed.node_1_policy_name}'.")
        
        logger.info(f"This switch template was created for node_1: '{test_bed.node_1_template_name}'.")
        
        logger.info(f"This is the onboarding location for node_1: '{test_bed.node_1_onboarding_location}'.")
        
        node_2 = test_bed.node_2
        
        logger.info(f"The second onboarded node has MAC='{node_2.mac}'.")
        
        logger.info(f"This policy is applied to node_2: '{test_bed.node_2_policy_name}'.")
        
        logger.info(f"This switch template was created for node_2: '{test_bed.node_2_template_name}'.")
        
        logger.info(f"This is the onboarding location for node_2: '{test_bed.node_2_onboarding_location}'.")

        logger.info(f"The list of nodes: {test_bed.node_list}")

    @pytest.mark.tcxm_209
    @pytest.mark.p1
    def test_9(self, test_data, logger, test_bed):
        
        logger.info(f"This test is {test_data['tc']}")
        logger.info(f"This test is writen by {test_data['author']}")

        with test_bed.open_spawn(test_bed.node_1) as spawn_connection:
            
            test_bed.cli.disconnect_device_from_cloud(test_bed.node_1.cli_type, spawn_connection)
            
            test_bed.cli.configure_device_to_connect_to_cloud(
                test_bed.node_1.cli_type, test_bed.config['sw_connection_host'],
                spawn_connection, vr=test_bed.virtual_routers.get(test_bed.node_1.name, 'VR-Mgmt'), retry_count=30
            )

        with test_bed.open_spawn(test_bed.node_2) as spawn_connection:
            
            test_bed.cli.disconnect_device_from_cloud(test_bed.node_2.cli_type, spawn_connection)
            
            test_bed.cli.configure_device_to_connect_to_cloud(
                test_bed.node_2.cli_type, test_bed.config['sw_connection_host'],
                spawn_connection, vr=test_bed.virtual_routers.get(test_bed.node_2.name, 'VR-Mgmt'), retry_count=30
            )


@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.testbed_stack
class NewTestbedStackTests:
    
    """ The tests that are marked with testbed_stack run only there is at a least a stack netelem in the devices.yaml.
    """
    
    @pytest.mark.tcxm_210
    @pytest.mark.p1
    def test_10(self, logger, test_data, xiq_library_at_class_level, test_bed):
        
        logger.info(f"This test is {test_data['tc']}")
        logger.info(f"This test is writen by {test_data['author']}")
        
        node_stack = test_bed.node_stack
        
        logger.info(test_bed.dump_data(node_stack))
        
        logger.info(f"This policy is applied to node_stack: '{test_bed.node_stack_policy_name}'.")
        
        logger.info(f"This switch template was created for node_stack: '{test_bed.node_stack_template_name}'.")
        
        logger.info(f"This is the onboarding location for node_stack: '{test_bed.node_stack_onboarding_location}'.")

        logger.info(f"The stack has {len(test_bed.node_stack.stack)} slots.")

        logger.info(f"The stack has these unit models: '{test_bed.node_stack_model_units}'.")

    @pytest.mark.tcxm_211
    @pytest.mark.p1
    def test_11(self, test_data, logger):
        
        logger.info(f"This test is {test_data['tc']}")
        logger.info(f"This test is writen by {test_data['author']}")


class NewCascadeTests:
    
    @pytest.mark.p1
    @pytest.mark.testbed_none
    @pytest.mark.tcxm_212
    def test_12(self, logger):
        """
        This test does not deppend on any test.
        """
        logger.info("This is tcxm_212!")
    
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_213
    @pytest.mark.dependson("tcxm_212")
    @pytest.mark.dependson("tcxm_xiq_onboarding")
    def test_13(self, logger):
        """
        This test dependson tcxm_212.
        If tcxm_212 fails -> tcxm_213 is skipped.
        If tcxm_212 is skipped -> tcxm_213 is skipped.
        """
        logger.info("This is tcxm_212!")
    
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_214
    @pytest.mark.dependson("tcxm_213")
    @pytest.mark.dependson("tcxm_xiq_onboarding")
    def test_14(self, logger):
        """
        This test dependson tcxm_213.
        If tcxm_213 fails -> tcxm_214 is skipped.
        If tcxm_213 is skipped -> tcxm_214 is skipped.
        """
        logger.info("This is tcxm_212!")
