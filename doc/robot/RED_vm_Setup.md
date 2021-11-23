# RED VM Setup
A VMWare image is provide that includes the RED IDE, the econ_robot_automation and the econ_robot_tests git repositories already installed and configurated. The VM is running Ubuntu 20.04. Only a few steps will need to be done to get this VM up and runnig. You can download the VM [here]()

-  Deploy the VM to a server.
-  Power on the VM and login with the following:

            Username: administrator

            Password: extreme  
-  You will need to copy your ssh keys for GIT into the home directory /export/home/administrator/.ssh and give them the correct permissions. 

        chmod 600 ~/.ssh/id_rsa
        chmod 644 ~/.ssh/id_rsa.pub

-  Next you will need to set your username and email for RED. Start the RED IDE by typing the folllowing command:

        ~/Red/RED &

-  Once RED has started. Set up the username for git by selecting the Window->preferences. From there type in git into the search windows and select Git->Configuraiton. You will need to add two Enties here.

    user.name = <your username>
    user.email = <your user email>

![Import project](img/Red_git_user.png)

-  Once that is completed restart RED and locate the Git Staging tab. You will see the files that have been added, deleted and changes in this tab. From here you can select the files to be checked into the branch. Also you will notice that your username / email are automaticly filled in.

![Import project](img/Red_git_staging.png)

You can read through this documenation for [RED](https://nokia.github.io/RED/help/) to see how to use this IDE.