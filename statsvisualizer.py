from github import Github
from config import GITHUB_TOKEN
from datetime import date
import pandas as pd
import plotly.express as px
import pickle
import os

class StatVis:

    _repo = None
    _xlsx_writer = None
    _dir = None

    _general_data = {}
    _visitors_data = {}
    _stargazers_data = {}
    _clones_data = {}
    _referral_data = {}

    def __init__(self, repo_url, visualize=True):
        self.repo_url = repo_url
        self.vis = visualize
        self.dir = "./stats"

        self.__load_github_instance(repo_url)

    def __load_github_serialized_data(self):
        self.general_data = self.__load_file_data("/general_data")
        self.visitors_data = self.__load_file_data("/visitors_data")
        self.stargazers_data = self.__load_file_data("/stargazers_data")
        self.clones_data = self.__load_file_data("/clones_data")
        self.referral_data = self.__load_file_data("/referral_data")

    def __init_github_data_dicts(self):

        if not self.general_data:
            self.general_data = {'index_labels': ['Name', 'Visitors', 'Unique Visitors', 'Watchers', 'Forks', 'Stargazers', 'Clones',
                                                  'Unique Clones'],
                                 'data': {}}
        if not self.visitors_data:
            self.visitors_data = {'index_labels': ['Visitors', 'Unique Visitors'], 'data': {}}

        if not self.clones_data:
            self.clones_data = {'index_labels': ['Clones', 'Unique Clones'], 'data': {}}

        if not self.stargazers_data:
            self.stargazers_data = {'data': {}}

        #if not self.referral_data:
        #      self.referral_data = {'index_labels': [], 'data': {} }

        #  if not self.stargazers_data:




    def __load_file_data (self,filename):
        filedir = self.dir + filename
        data = {}

        if os.path.isfile(filedir):
            with open(filedir, 'rb') as f:
                try:
                    data = pickle.load(f)
                except EOFError:
                    data = {}
            f.close()

        return data #todo init the dicts if the data is empty.

    def __write_serialized_data (self):
        self.__write_file_data("/general_data", self.general_data)
        self.__write_file_data("/visitors_data", self.visitors_data)
        self.__write_file_data("/stargazers_data",self.stargazers_data)
        self.__write_file_data("/clones_data",self.clones_data)
        self.__write_file_data("/referral_data",self.referral_data)

    def __write_file_data (self,filename,data):
        if data:
            with open(self.dir+filename, 'wb') as f:
                pickle.dump(data, f)
            f.close()

    def __load_github_instance(self, repo_url):
        # First create a Github instance:
        gitInst = Github(GITHUB_TOKEN)
        self.repo = gitInst.get_repo(repo_url)

    def __write_xlsx_workbook(self):
        workbook_path = r"./stats/github_data.xlsx"
        self.xlsx_writer = pd.ExcelWriter(workbook_path, engine='xlsxwriter')

        pd.DataFrame(self.general_data['data'], index=self.general_data['index_labels']).to_excel(self.xlsx_writer,
                                                                                                  sheet_name='General')
        pd.DataFrame(self.visitors_data['data'], index=self.visitors_data['index_labels']).to_excel(self.xlsx_writer,
                                                                                                    sheet_name='Views')
        pd.DataFrame(self.clones_data['data'], index=self.clones_data['index_labels']).to_excel(self.xlsx_writer,
                                                                                                sheet_name='Clones')

        #pd.DataFrame(pd.concat(pd.Series(self.stargazers_data['data']),ignore_index=True, axis=1)).to_excel(self.xlsx_writer, sheet_name='Star Gazers', index=False)
        #pd.DataFrame(self.referral_data['data'], index=self.referral_data['index_labels']).to_excel(self.xlsx_writer, sheet_name='Referrals')

        self.xlsx_writer.close()

    def __collect_stargazers_stats(self):
        stardates = self.repo.get_stargazers_with_dates()

        # Remove empty usernames
        stardates = [x for x in stardates if x.user.name]

        # Create build dict and create list based on date
        for stardate in stardates:
            if stardate.starred_at.date() not in self.stargazers_data['data']:
                self.stargazers_data['data'][stardate.starred_at.date()] = []
            self.stargazers_data['data'][stardate.starred_at.date()].append(stardate.user.name)

    def __collect_general_stats(self):
        watches = self.repo.get_subscribers().totalCount
        forks = self.repo.get_forks().totalCount
        clones = self.repo.get_clones_traffic()
        stars = self.repo.get_stargazers().totalCount
        views = self.repo.get_views_traffic()

        if date.today() not in self.general_data['data']:
            self.general_data['data'][date.today()] = [self.repo.name, views["count"], views["uniques"], watches, forks, stars, clones["count"],clones["uniques"]]
            
    def __collect_visitors_stats(self):
        visitors = self.repo.get_views_traffic()

        for visitor in visitors["views"]:
            if visitor.timestamp not in self.visitors_data['data']:
                self.visitors_data['data'][visitor.timestamp] = [ visitor.count, visitor.uniques]

    def __collect_clones_stats(self):
        clones = self.repo.get_clones_traffic()

        for clone in clones["clones"]:
            if clone.timestamp not in self.clones_data['data']:
                self.clones_data['data'][clone.timestamp] = [clone.count, clone.uniques]

    def __collect_referrals_stats(self):
        referrals = self.repo.get_top_referrers()

        #if date.today() not in self.referral_data['index_labels']:
        #    for ref in referrals:
        #        self.referral_data['index_labels'].append(date.today())
        #        self.referral_data['data'][ref.referrer] =
        #        self.referral_data['data']["Views"].append(ref.count)
        #        self.referral_data['data']["Unique Referrals"].append(ref.uniques)

        # print( self.referral_data)

    def collect_github_stats(self, load=True):
        if load:
            self.__load_github_serialized_data()

        # todo put and else if here!
        self.__init_github_data_dicts()

        self.__collect_general_stats()
        self.__collect_visitors_stats()
        self.__collect_clones_stats()
        self.__collect_stargazers_stats()

        #self.__collect_referrals_stats()

    def write_github_stats(self, ftype='bin'):
        if ftype == 'bin':
            self.__write_serialized_data()
        elif ftype == 'xlsx':
            self.__write_xlsx_workbook()


