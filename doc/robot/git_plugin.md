# **** PLEASE NOTE ****
The documentation on this page is deprecated and is no longer up-to-date.  It remains as a reference in the event someone wants to try to setup RED to use a debugger for robot scripts.

# **** PLEASE NOTE ****

## Install the GIT plugin
Next you will need to install GIT Plugin into RED. Select '`Help->Eclipse Marketplace...`'

Enter in `git` in the search and press the `go` button. Once the search comes back click on the install button next to Git Integration for Eclpse. Take the default and completed the installation process.

![Import project](img/Red_git_plugin.png)

Once RED has restarted, click on Windows->Show View->Other.
Select the GIT Repositories and GIT Staging views and select open.

![Import project](img/Red_git_view.png)


Locate the GIT Repositories window and select '`Add an exsiting local Git repository`'.

![Import project](img/Red_git_repos.png)


Select the econ-robot-automation and the econ-automation-tests repository from your system and click on add.

![Import project](img/Red_git_select_repos.png)

Now the repositories are configured. 

![Import project](img/Red_git_repos_configured.png)


Set up the username for git by selecting the Window->preferences. From there type in git into the search windows and select Git->Configuraiton. You will need to add two Enties here.

    user.name = <your username>
    user.email = <your user email>

![Import project](img/Red_git_user.png)

Once that is completed restart RED and locate the Git Staging tab. You will see the files that have been added, deleted and changes in this tab. From here you can select the files to be checked into the branch. Also you will notice that your username / email are automaticly filled in.

![Import project](img/Red_git_staging.png)

