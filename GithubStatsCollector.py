from github import Github
from config import GITHUB_TOKEN
from datetime import date
import pandas as pd
import plotly.express as px

gitInst = None

def initialize ( repo_url):
    # First create a Github instance:
    global gitInst
    gitInst = Github(GITHUB_TOKEN)
    repo = gitInst.get_repo(repo_url)
    return repo


def collect_stargazers_stats(repo,excel_writer):

    stardates = repo.get_stargazers_with_dates()
    stargazers_data = []

    for stardate in stardates:
        stargazers_data.append({'Star Date': stardate.starred_at, 'Stargazer': stardate.user.name})

    pd.DataFrame(stargazers_data).to_excel(excel_writer, sheet_name='Star Gazers')


def collect_visitors_stats(repo,excel_writer):

    views = repo.get_views_traffic()
    visitors_data = []

    for visitors in views["views"]:
        visitors_data.append({'View Date': visitors.timestamp, 'Visitors': visitors.count, 'Unique Visitors': visitors.uniques})

    pd.DataFrame(visitors_data).to_excel(excel_writer, sheet_name='Views')


def collect_clones_stats(repo, excel_writer):
    clones = repo.get_clones_traffic()
    clones_data = []

    for clone in clones["clones"]:
        clones_data.append({'Cloning Date': clone.timestamp, 'Clones': clone.count, 'Unique Clones': clone.uniques})

    pd.DataFrame(clones_data).to_excel(excel_writer, sheet_name='Clones')


def collect_referrals_stats(repo , excel_writer):
    referrals = repo.get_top_referrers()
    referral_data = []
    for ref in referrals:
        referral_data.append({'Referrer Name': ref.referrer, 'Date': date.today(), 'Unique referrals': ref.uniques, 'Views': ref.count})

    pd.DataFrame(referral_data).to_excel(excel_writer, sheet_name='Referrals')

def collect_general_stats(repo, excel_writer):

    watches = repo.get_subscribers().totalCount
    forks = repo.get_forks().totalCount
    clones = repo.get_clones_traffic()
    stars = repo.get_stargazers().totalCount
    views = repo.get_views_traffic()

    general_data = [{'Repo': repo.name, 'Date': date.today(), 'Visitors': views["count"], 'Unique Visitors': views["uniques"],
                     'Watchers': watches, 'Forks': forks, 'Stargazers': stars,
                     'Clones': clones["count"], 'Unique Clones': clones["uniques"]}]

    pd.DataFrame(general_data).to_excel(excel_writer, sheet_name='General')

def collect_stats(repo_url, excel_writer):
    repo = initialize(repo_url)

    collect_general_stats(repo, excel_writer)
    collect_referrals_stats(repo, excel_writer)
    collect_clones_stats(repo, excel_writer)
    collect_visitors_stats(repo, excel_writer)
    collect_stargazers_stats(repo, excel_writer)



