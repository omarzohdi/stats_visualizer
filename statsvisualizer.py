from github import Github
from config import GITHUB_TOKEN
from datetime import date
import pandas as pd
import plotly.express as px

class StatVis:

    repo = None

    general_data = []
    visitors_data = []
    stargazers_data = []
    clones_data = []
    referral_data = []

    xls_writer = None

    def __init__(self, repo_url, format, visualize=True):
        self.repo_url = repo_url
        self.format = format
        self.vis = visualize

        self.load_github_instance(repo_url)
        self.load_xls_workbook()

    def __del__(self):
        self.xls_writer.close()

    def load_github_instance(self, repo_url):
        # First create a Github instance:
        gitInst = Github(GITHUB_TOKEN)
        self.repo = gitInst.get_repo(repo_url)

    def load_xls_workbook(self):
        workbook_path = r"./stats/github_data.xlsx"
        self.xls_writer = pd.ExcelWriter(workbook_path, engine='xlsxwriter')

    def collect_stargazers_stats(self):
        stardates = self.repo.get_stargazers_with_dates()

        for stardate in stardates:
            self.stargazers_data.append({'Star Date': stardate.starred_at, 'Stargazer': stardate.user.name})

        pd.DataFrame(self.stargazers_data).to_excel(self.xls_writer, sheet_name='Star Gazers')

    def collect_general_stats(self):
        watches = self.repo.get_subscribers().totalCount
        forks = self.repo.get_forks().totalCount
        clones = self.repo.get_clones_traffic()
        stars = self.repo.get_stargazers().totalCount
        views = self.repo.get_views_traffic()

        self.general_data.append({'Repo': self.repo.name, 'Date': date.today(), 'Visitors': views["count"],
                         'Unique Visitors': views["uniques"],
                         'Watchers': watches, 'Forks': forks, 'Stargazers': stars,
                         'Clones': clones["count"], 'Unique Clones': clones["uniques"]})

        pd.DataFrame(self.general_data).to_excel(self.xls_writer, sheet_name='General')

    def collect_visitors_stats(self):
        visitors = self.repo.get_views_traffic()

        for visitor in visitors["views"]:
            self.visitors_data.append({'View Date': visitor.timestamp, 'Visitors': visitor.count, 'Unique Visitors': visitor.uniques})

        pd.DataFrame(self.visitors_data).to_excel(self.xls_writer, sheet_name='Views')

    def collect_clones_stats(self):
        clones = self.repo.get_clones_traffic()

        for clone in clones["clones"]:
            self.clones_data.append({'Cloning Date': clone.timestamp, 'Clones': clone.count, 'Unique Clones': clone.uniques})

        pd.DataFrame(self.clones_data).to_excel(self.xls_writer, sheet_name='Clones')

    def collect_referrals_stats(self):
        referrals = self.repo.get_top_referrers()

        for ref in referrals:
            self.referral_data.append({'Referrer Name': ref.referrer, 'Date': date.today(), 'Unique referrals': ref.uniques, 'Views': ref.count})

        pd.DataFrame(self.referral_data).to_excel(self.xls_writer, sheet_name='Referrals')

    def run_github_statcollectors(self):
        self.collect_general_stats()
        self.collect_referrals_stats()
        self.collect_clones_stats()
        self.collect_visitors_stats()
        self.collect_stargazers_stats()