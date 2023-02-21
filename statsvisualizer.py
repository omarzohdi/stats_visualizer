from statsgithubuser import StatsGitHubUser as sgUser


class StatsVisualizer:
    _github_user = None

    def __init__(self):
        pass

    def init_github_user_info(self, github_token):
        self._github_user = sgUser(github_token)

    def add_github_repo_info(self, repo_url, output_dir): #  todo return index of new repo added
        if self._github_user:
            git_repo_obj = self._github_user.add_github_repo(repo_url, output_dir)

    def collect_all_repos_stats(self, load_binary=True, ftype='all'):

        repo_list = self._github_user.get_repos_list()

        for repo in repo_list:
            repo.collect_github_stats(load_binary=True)

            if ftype == 'all':
                repo.write_github_stats('json')
                repo.write_github_stats('bin')
                repo.write_github_stats('xlsx')
            else:
                repo.write_github_stats(ftype)

    def collect_repo_stats(self, index=0):
        if not self._github_user:
            return  # todo return error message? Exception maybe.

        if not self._github_user.get_repos_list():
            return  # todo return error message? Exception maybe.

        repo_data = self._github_user.get_repos_list()
        repo_data[index].collect_github_stats(load_binary=True)
        repo_data[index].write_github_stats('json')
        repo_data[index].write_github_stats('bin')
        repo_data[index].write_github_stats('xlsx')
