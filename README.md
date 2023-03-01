
# GitHub Stats Visualizer 

A series of python scripts to collect GitHub repository stats and use GitHub actions to commit them back into the repository. Aside from cumulative data (i.e. forks, stars, watchers) GitHub only ever keeps stats history for a period of 14 days. Anything older than that cannot be retrieved. This script will help circumvent that limitation.

The scripts support exporting data to binary, json and xlsx format. 

### Planned Features

- Add plotly support and visualize data in HTML.
- Generate and update graphs in xlsx file. 

# Setup

To use the script you'll need to generate a GitHub Token, define environment variables for the GitHub Actions agent to use and modify the workflow and python files to match the defined variables.

## 1. Generate GitHub Token

Go to your account's **Settings**, in the sidebar go to **Developer Settings**, expand **Personal Access Tokens** and select **Tokens (classic)**

Click on **Generate new Token** and **Generate new Token (Classic)**. Name the token and pick an expiration date. Give the GitHub token full repo control and workflow control then generate the token. Copy the new token string.

More info on how to generate tokens can be found [here](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)  

## 2. Set Secret Variable

Go to the repository's **Settings**, in the sidebar go to **Security**, expand **secrets and variables** select **Actions**

In the **Secrets** tab add a new secret variable and name it TOKEN_GITHUB and assign it the previously generate token string

### Optional:

Move to the **Variables** tab and add a variable for each repo you want to collect stats for and assign it the GitHub repository's URL path.
Example:
 
 >Variable Name: REPO_DOCS_GITHUB
 
 >Value: github/docs

More info on how to add environment variables to a repository can be found [here](https://docs.github.com/en/actions/learn-github-actions/variables#creating-configuration-variables-for-a-repository)

## 3. Modify GitHub Actions Workflow 

By default, GitHub Actions will collect the stats every Monday at 23.55 UTC. To modify this behaviour you'll have to edit the cron job timing at the top of the workflow in ```main.yml```:

```yml
name: "Collect GitHub Stats"
on:
  workflow_dispatch:
  schedule:
  - cron: "55 23 * * 1"
```

You can use this [website](https://crontab.guru/) to pick the correct cron job string

In the ```jobs``` section find the ```execute python script``` job. Here you can define the environment variables for the GitHub repositories you want to collect data for. 

***Note**: if you set up the environment variables in the repository's settings you can skip this part.* 

```yml
- name: execute python script
  env:
    GITHUB_TOKEN: ${{ secrets.TOKEN_GITHUB }}
    GITHUB_VIS_REPO: "omarzohdi/github_stats_visualizer"
  run: python __main__.py
```

In the ```commit new file``` job you can modify the commit message that the GitHub Actions agent will use when committing the new stats to the repository

```yml
- name: commit new files
  run: |
    git config --local user.email "action@github.com"
    git config --local user.name "GitHub Action"
    git add -A
    git diff-index --quiet HEAD || (git commit -a -m "Updates Stats" --allow-empty)
```

## 4. Modify Python Script

In the ```__main__.py``` you'll have to modify the name of the environment variables to reflect the ones that you've set up in the workflow file or the repository's settings.

```python
try:
	GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
	GITHUB_WEB_REPO = os.environ["GITHUB_WEB_REPO"]
	GITHUB_SOT_REPO = os.environ["GITHUB_SOT_REPO"]
except KeyError:
	print("Environment variables (GITHUB_TOKEN or REPOs) not set")
return
```

After setting up the environment variable call ```add_github_repo_info``` for each repository you want to collect data for and specify the ```output_dir``` to it queue up. 

```add_github_repo_info``` returns the index of the repository in the queue.

```python
sv = statVis()
sv.init_github_user_info(GITHUB_TOKEN)
sv.add_github_repo_info(GITHUB_WEB_REPO, output_dir='stats')
sv.add_github_repo_info(GITHUB_SOT_REPO, output_dir='stats')
```

Finally, you can call ```collect_all_repos_stats``` or ```collect_repo_stats``` to collect the repository stats.

```python
sv.collect_all_repos_stats()
sv.collect_repo_stats(1)
```

### Parameters for stats collection functions 

```python
def collect_all_repos_stats(self, load_binary=True, ftype='all')
```
| Parameter         | Values                                                | Description                                                                                                                                                                                                                     |
|-------------------|-------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ```load_binary``` | **bool**                                              | Whether to load data from previous binary or Json files already present in the output folder. **WARNING**: if set to ```False``` and binary or Json files are present it will overwrite them base on the ```ftype``` parameter. |
| ```ftype```       | **str**: ```all```, ```json```, ```bin```, ```xlsx``` | The type of file you want the stats to be written to. ```all``` will write all three types of files.                                                                                                                            |

```python
def collect_repo_stats(self, index=0, ftype='all')
```

| Parameter         | Values                                                | Description                                                                                                                                                                                                                     |
|-------------------|-------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ```index```       | **int**                                               | The index of the repository queued up in the repo list. The index of the repo is returned when ```add_github_repo_info``` is called.                                                                                            |
| ```load_binary``` | **bool**                                              | Whether to load data from previous binary or Json files already present in the output folder. **WARNING**: if set to ```False``` and binary or Json files are present it will overwrite them base on the ```ftype``` parameter. |
| ```ftype```       | **str**: ```all```, ```json```, ```bin```, ```xlsx``` | The type of file you want the stats to be written to. ```all``` will write all three types of files.                                                                                                                            |
