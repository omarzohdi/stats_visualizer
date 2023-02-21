import argparse
import os
from statsvisualizer import StatsVisualizer as statVis



if __name__ == "__main__":
    try:
        GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
    except KeyError:
        print("No GITHUB_TOKEN environment variable found")
        #GITHUB_TOKEN = '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'

    repo_url_web = "powervr-graphics/Native_SDK"
    repo_url_sot = "powervr-graphics/PowerVR-Series1"

    sv = statVis()
    sv.init_github_user_info(GITHUB_TOKEN)
    sv.add_github_repo_info(repo_url_web, output_dir='stats')
    sv.add_github_repo_info(repo_url_sot, output_dir='stats')
    sv.collect_all_repos_stats()
