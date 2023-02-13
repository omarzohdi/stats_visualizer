import argparse
from statsvisualizer import StatVis

def main():
    # This is the result of a -h command
    parser = argparse.ArgumentParser(description="Welcome to the Stats Collector! - "
                                                 "Here you'll be able to collect stats for Github and Google analytics")
    parser.add_argument("--repo", help="URL of The Github repository to collect data from", default="A")
    args = parser.parse_args()

    workbook_path = r"./stats/github_data.xlsx"
    repo_url = "omarzohdi/omarzohdi.github.io"

    sv = StatVis(repo_url, 'xls')
    sv.run_github_statcollectors()

if __name__ == "__main__":
    main()