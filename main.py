import argparse
import GithubStatsCollector as gsc
import pandas as pd

def initialize_workbook(workbook_path):
    writer = pd.ExcelWriter(workbook_path, engine = 'xlsxwriter')
    return writer

def deinitialize_workbook(writer):
    writer.close()

def main():
    # This is the result of a -h command
    parser = argparse.ArgumentParser(description="Welcome to the Stats Collector! - "
                                                 "Here you'll be able to collect stats for Github and Google analytics")
    parser.add_argument("--repo", help="URL of The Github repository to collect data from", default="A")
    args = parser.parse_args()

    workbook_path = r"./stats/github_data.xlsx"
    repo_url = "omarzohdi/omarzohdi.github.io"

    excel_writer = initialize_workbook(workbook_path)

    # Collect Stats for Github
    gsc.collect_stats(repo_url, excel_writer)

    deinitialize_workbook(excel_writer)

if __name__ == "__main__":
    main()


#for pages in stars_dates:
#    print(pages)

#print(clones_json)

#df = pd.read_json(clones_json)
#df.to_csv()


#forksdata = {}

# Then play with your Github objects:
#for repo in g.get_user().get_repos():
#    if repo.name == "Native_SDK":
#        for fork in repo.get_forks():
#            forksdata[fork.name] = fork.created_at

#print(forksdata)
#data = px.data.gapminder(forksdata)
#fig = go.Figure(data=go.Bar(x=df_month['month'].astype(dtype=str),
#                        y=df_month['counts'],
#                        marker_color='indianred', text="counts"))
#fig.show()