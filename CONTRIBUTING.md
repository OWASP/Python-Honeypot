# Contributing to OWASP-Honeypot

First off, thanks for taking the time to contribute!
We gladly support and appreciate anyone is interested to contribute to the OWASP Honeypot Project. Overall developers may focus on developing core framework or modules. Please consider that we are using PEP8 python code style and using Codacy to figure the code quality. In addition, Travis-CI will check your PR automatically on several Python versions (3.x). Before sending your PR, make sure you added code-based documentation to your codes. If you use any code/library/module with a license, add the license into external license file.

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

## Steps to follow :scroll:

### 1. Fork it :fork_and_knife:

You can get your own fork/copy of [OWASP-Honeypot]( https://github.com/zdresearch/OWASP-Honeypot) by using the <kbd><b>Fork</b></kbd></a> button.

 [![Fork Button](https://help.github.com/assets/images/help/repository/fork_button.jpg)](https://github.com/zdresearch/OWASP-Honeypot)

### 2. Clone it :busts_in_silhouette:

You need to clone (download) it to local machine using

```sh
git clone https://github.com/Your_Username/OWASP-Honeypot.git
```

> This makes a local copy of repository in your machine.

Once you have cloned the ` OWASP-Honeypot ` repository in GitHub, move to that folder first using change directory command.

```sh
# This will change directory to a folder OWASP-Honeypot
cd OWASP-Honeypot
```

Move to this folder for all other commands.

### 3. Set it up :arrow_up:

Run the following commands to see that *your local copy* has a reference to *your forked remote repository* in GitHub :octocat:

```sh
git remote -v
origin  https://github.com/Your_Username/OWASP-Honeypot.git (fetch)
origin  https://github.com/Your_Username/OWASP-Honeypot.git (push)
```

Now, add a reference to the original [OWASP-Honeypot](https://github.com/zdresearch/OWASP-Honeypot) repository using

```sh
git remote add upstream https://github.com/zdresearch/OWASP-Honeypot.git
```

> This adds a new remote named ***upstream***.

See the changes using

```sh
git remote -v
origin    https://github.com/Your_Username/OWASP-Honeypot.git (fetch)
origin    https://github.com/Your_Username/OWASP-Honeypot.git (push)
upstream  https://github.com/zdresearch/OWASP-Honeypot.git    (fetch)
upstream  https://github.com/zdresearch/OWASP-Honeypot.git    (push)
```

### 4. Sync it 

Always keep your local copy of repository updated with the original repository.
Before making any changes and/or in an appropriate interval, run the following commands *carefully* to update your local repository.

```sh
# Fetch all remote repositories and delete any deleted remote branches
git fetch --all --prune

# Switch to `master` branch
git checkout master

# Reset local `master` branch to match `upstream` repository's `master` branch
git reset --hard upstream/master

# Push changes to your forked `Plant_Disease_Detection` repo
git push origin master
```

### 5. Ready Steady Go... 

Once you have completed these steps, you are ready to start contributing by checking our `Help Wanted` Issues and creating [pull requests](https://github.com/zdresearch/OWASP-Honeypot/pulls).

### 6. Create a new branch :bangbang:

Whenever you are going to make contribution. Please create separate branch using command and keep your `master` branch clean (i.e. synced with remote branch).

```sh
# It will create a new branch with name Branch_Name and will switch to that branch.
git checkout -b Branch_Name
```

Create a separate branch for contribution and try to use same name of branch as of folder.

To switch to desired branch

```sh
# To switch from one folder to other
git checkout Branch_Name
```

To add the changes to the branch. Use

```sh
# To add all files to branch Branch_Name
git add .
```

Type in a message relevant for the code reviewer using

```sh
# This message gets associated with all files you have changed
git commit -m 'relevant message'
```

Now, Push your awesome work to your remote repository using

```sh
# To push your work to your remote repository
git push -u origin Branch_Name
```

Finally, go to your repository in browser and click on `compare and pull requests`.
Add a title and description to your pull request that explains your precious effort.

Sit and relax till we review your PR, you've made your contribution to our project.
