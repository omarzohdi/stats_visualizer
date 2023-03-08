import argparse
import os
from statsvisualizer import StatsVisualizer as statVis


def main():
    print("Starting VisStat!")
    try:
        print("Loading Environment Variables")
        GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
        GITHUB_VIS_REPO = os.environ["GITHUB_WEB_REPO"]

    except KeyError:
        print("Environment variables (GITHUB_TOKEN or REPOs) not set")
        return

    sv = statVis()
    sv.init_github_user_info(GITHUB_TOKEN)
    sv.add_github_repo_info(GITHUB_VIS_REPO, output_dir='stats')
    sv.collect_all_repos_stats()

    print("VisStat Done!")

if __name__ == "__main__":
    main()
