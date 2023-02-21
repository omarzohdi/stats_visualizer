import argparse
from statsvisualizer import StatsVisualizer as statVis

def cli():
    # This is the result of a -h command
    parser = argparse.ArgumentParser(description="Welcome to the Stats Collector! - "
                                                 "Here you'll be able to collect stats for Github and Google analytics")
    parser.add_argument("--repo", help="URL of The Github repository to collect data from", default="A")
    args = parser.parse_args()


if __name__ == "__main__":
    #cli()  # todo add cli integration here.

    repo_url_web = "omarzohdi/omarzohdi.github.io"
    repo_url_sot = "omarzohdi/Soteria"
    token = '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'

    sv = statVis()
    sv.init_github_user_info(token)
    sv.add_github_repo_info(repo_url_web, output_dir='stats')
    sv.add_github_repo_info(repo_url_sot, output_dir='stats')

    sv.collect_all_repos_stats()
