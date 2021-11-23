##  Introduction

Various features and utilities have been implemented via kwargs (Keyword Arguments). Keyword arguments are arguments that must be named and must be provided as the last arguments in a keyword or method.

##  How are keyword arguments defined?
* Here is an example of a defined keyword:

        def configure_port_enable(self, device_name, ports, **kwargs):
        """
        Keyword Arguments:
        [device_name] - The device the keyword should be run against.
        [ports]       - The port(s) to enable.

        Enables the given port(s) on a network element.
        """
        return self.gen_port.port_enable_state(device_name, ports, **kwargs)

* As you can see the **kwargs are defined as the last argument in the method above. Any named arguments provided after the 'ports' argument will be contained in a python dictionary called kwargs.

* Example of using kwargs in a python method.

        cmd_kws.send_cmd("dut1", "unconfigure switch", wait_for_prompt=False)
        cmd_kws.send_cmd("dut1", "y", check_initial_prompt=False)

##  List and examples of currently implemented kwargs
* `wait_for_prompt`: If set to True, keyword will move on without waiting for the device prompt to return. This is often used in cli commands that have follow-up questions or outputs that do not contain the prompt. Default is False.

                Send_CMD(netelem_name, 'unconfigure switch', wait_for_prompt=False)
                Send_CMD(netelem_name, y, check_initial_prompt=False)

* `check_initial_prompt`: If set to False, keyword will not check for prompt before issuing a command to agent. Default is True.

                Send_CMD(netelem_name, 'unconfigure switch', wait_for_prompt=False)
                Send_CMD(netelem_name,  y, check_initial_prompt=False)

* `expect_error`: This will cause a keyword to fail unless an error is seen in the commands output. This is disabled by default.

                Delete_Policy_Access_List_Action_Set(netelem1.name, 1, expect_error=True)

* `wait_for` and `interval`: This function executes a wait for validation. It checks the result of the passed parse function every <interval> (The time in seconds between each status check of the keyword function) until it matches the expected result or <max_wait> seconds have passed.

                MultiAuth_Session_Idle_Time_Should_be_Greater(netelem1.name, dot1x_user_a_mac, 39, 90, interval=2, wait_for=True)

* `max_wait`: The amount of time in seconds the keyword should wait before it is considered a failure.

                FDB_Entry_Should_Exist(netelem1.name, mac_invalid_filter, vlan_a, netelem1.tgen.port_a.ifname, interval=2, wait_for=True  max_wait=60)

* `ignore_error`: This adds errors to the devices error checker to ignore for the given keyword.

                Send_CMD(netelem1.name, 'clear log', ignore_error=Error)

* `ignore_cli_feedback`: If set to True CLI feedback is ignored. This is set to False by default. This will ignore any errors that may be returned from running this keyword. This could be used to make sure the device is in a clean state before a test will begin. In some cases the keyword would execute with and without errors but the user doesn't want to report on the errors that may be returned.

                Remove_FDB_Entry(netelem1.name, dst_mac_a, vlan_a, ignore_cli_feedback=True)

* `get_only`: If set to True on a verify keyword, the keyword will execute and not check for any return value. The value will be returned from the call so the user can interact with the return. This is set to False by default.

               spanningtree_verify_mode_mstp(netelem_name, get_only=True)