from github import Github
from config import GITHUB_TOKEN
from datetime import date
import pandas as pd
import pickle
import json
import os


class StatVis:

    _repo = None
    _xlsx_writer = None
    _dir = None

    _github_data = {}

    def __init__(self, repo_url, visualize=True):
        self.repo_url = repo_url
        self.vis = visualize
        self.dir = "./stats"

        self.__load_github_instance(repo_url)

    def __load_github_serialized_data(self):
        self.general_data = self.__load_file_data("/github_data")

    def __init_github_data_dicts(self):

        if not self._github_data:
            self._github_data = {'general_data': {'index_labels': ['Name', 'Visitors', 'Unique Visitors', 'Watchers',
                                                                  'Forks', 'Stargazers', 'Clones', 'Unique Clones'], 'data': {}},
                                'visitors_data': {'index_labels': ['Visitors', 'Unique Visitors'], 'data': {}},
                                'clones_data': {'index_labels': ['Clones', 'Unique Clones'], 'data': {}},
                                'stargazers_data': {'index_labels': ['Count'], 'data': {}},
                                'referral_data': {'index_labels': ['Views', 'Unique Visitors'], 'data': {}, 'timeframes': {}}
                                 }

    def __load_file_data(self, filename):
        filedir = self.dir + filename
        data = {}

        if os.path.isfile(filedir):
            with open(filedir, 'rb') as f:
                try:
                    data = pickle.load(f)
                except EOFError:
                    data = {}
            f.close()

        return data  # todo init the dicts if the data is empty.

    def __write_binary_file(self):
        self.__write_json_data("/github_data", self._github_data)

    def __write_json_file(self):
        self.__write_json_data("/github_data.json", self._github_data)

    def __write_json_data(self, filename, data):
        if data:
            with open(self.dir+filename, 'w') as f:
                json.dump(data, f, indent=4)
            f.close()

    def __write_binary_data(self, filename, data):
        if data:
            with open(self.dir+filename, 'wb') as f:
                pickle.dump(data, f)
            f.close()

    def __load_github_instance(self, repo_url):
        # First create a GitHub instance:
        git_inst = Github(GITHUB_TOKEN)
        self.repo = git_inst.get_repo(repo_url)

    def __write_xlsx_workbook(self):
        workbook_path = r"./stats/github_data.xlsx"
        self.xlsx_writer = pd.ExcelWriter(workbook_path, engine='xlsxwriter')

        pd.DataFrame(self._github_data['general_data']['data'], index=self._github_data['general_data']['index_labels']).to_excel(self.xlsx_writer, sheet_name='General')
        pd.DataFrame(self._github_data['visitors_data']['data'], index=self._github_data['visitors_data']['index_labels']).to_excel(self.xlsx_writer, sheet_name='Views')
        pd.DataFrame(self._github_data['clones_data']['data'], index=self._github_data['clones_data']['index_labels']).to_excel(self.xlsx_writer, sheet_name='Clones')
        pd.DataFrame(self._github_data['stargazers_data']['data'], index=self._github_data['stargazers_data']['index_labels']).transpose().to_excel(self.xlsx_writer, sheet_name='Stargazers')
        pd.DataFrame(self._github_data['referral_data']['data'], index=self._github_data['referral_data']['index_labels']).to_excel(self.xlsx_writer, sheet_name='Referrals')

        self.xlsx_writer.close()

    def __collect_referrals_stats(self):
        date_string = str(date.today())
        referrals = self.repo.get_top_referrers()
        data_totals = self._github_data['referral_data']['data']

        # todo clean up and make entire function more readable
        if date_string not in self._github_data['referral_data']['timeframes']:
            self._github_data['referral_data']['timeframes'][date_string] = []
            for ref in referrals:
                self._github_data['referral_data']['timeframes'][date_string].append(ref.raw_data)
                data_totals.setdefault(ref.referrer, [0, 0])

                # calculate cumulative data
        for timeframe, ref_info in self._github_data['referral_data']['timeframes'].items():
            for top_ref in ref_info:
                data_totals[top_ref['referrer']][0] += int(top_ref['count'])
                data_totals[top_ref['referrer']][1] += int(top_ref['uniques'])

    def __collect_stargazers_stats(self):
        stardates = self.repo.get_stargazers_with_dates()
        # Remove empty usernames
        stardates = [x for x in stardates if x.user.name]

        # Create build dict and create list based on date
        for stardate in stardates:
            if str(stardate.starred_at.date()) not in self._github_data['stargazers_data']['data']:
                self._github_data['stargazers_data']['data'][str(stardate.starred_at.date())] = 0
            self._github_data['stargazers_data']['data'][str(stardate.starred_at.date())] += 1

    def __collect_visitors_stats(self):
        visitors = self.repo.get_views_traffic()

        for visitor in visitors["views"]:
            if str(visitor.timestamp.date()) not in self._github_data['visitors_data']['data']:
                self._github_data['visitors_data']['data'][str(visitor.timestamp.date())] = [visitor.count, visitor.uniques]

    def __collect_clones_stats(self):
        clones = self.repo.get_clones_traffic()

        for clone in clones["clones"]:
            if str(clone.timestamp.date()) not in self._github_data['clones_data']['data']:
                self._github_data['clones_data']['data'][str(clone.timestamp.date())] = [clone.count, clone.uniques]

    def __collect_general_stats(self):
        watches = self.repo.get_subscribers().totalCount
        forks = self.repo.get_forks().totalCount
        clones = self.repo.get_clones_traffic()
        stars = self.repo.get_stargazers().totalCount
        views = self.repo.get_views_traffic()
        date_string = str(date.today())

        if date_string not in self._github_data['general_data']['data']:
            self._github_data['general_data']['data'][date_string] = [self.repo.name, views["count"], views["uniques"],
                                                                      watches, forks, stars, clones["count"],
                                                                      clones["uniques"]]

    def collect_github_stats(self, load=True):
        if load:
            self.__load_github_serialized_data()


        # todo put and else if here!
        self.__init_github_data_dicts()

        self.__collect_general_stats()
        self.__collect_clones_stats()
        self.__collect_visitors_stats()
        self.__collect_referrals_stats()
        self.__collect_stargazers_stats()

        print(self._github_data)

    def write_github_stats(self, ftype='bin'):
        self.__write_json_file()
        self.__write_xlsx_workbook()
        self.__write_binary_file()
