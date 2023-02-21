from github import Github
from statsgithubdata import GithubRepoStats as grStats


class StatsGitHubUser:
    _git_inst = None
    _repos = []

    def __init__(self, github_token):
        self._git_inst = Github(github_token)

    def add_github_repo(self, repo_url, output_dir="stats"):
        repo_inst = None

        if self._git_inst:
            repo_inst = self._git_inst.get_repo(repo_url)
            repo = grStats(repo_inst, output_dir)
            self._repos.append(repo)

        return len(self._repos) - 1

    def get_repos_list(self):
        return self._repos
