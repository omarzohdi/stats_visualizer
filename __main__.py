import argparse
import os
from statsvisualizer import StatsVisualizer as statVis


def main():
    try:
        GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
        GITHUB_WEB_REPO = os.environ["GITHUB_WEB_REPO"]
        GITHUB_SOT_REPO = os.environ["GITHUB_SOT_REPO"]

    except KeyError:
        print("Environment variables (GITHUB_TOKEN or REPOs) not set")
        return

    sv = statVis()
    sv.init_github_user_info(GITHUB_TOKEN)
    sv.add_github_repo_info(GITHUB_WEB_REPO, output_dir='stats')
    sv.add_github_repo_info(GITHUB_SOT_REPO, output_dir='stats')
    sv.collect_all_repos_stats()


if __name__ == "__main__":
    main()
