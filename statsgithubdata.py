import json
import os
import pickle
from datetime import date

import pandas as pd

class GithubRepoStats:
    _repo = None
    _dir = None
    _github_data = {}

    def __init__(self, repo_info, output_dir="stats"):
        self._repo = repo_info
        self._dir = os.path.join(output_dir, self._repo.name)

    def __init_github_data_dicts(self):

        if not self._github_data:
            self._github_data = {'general_data': {'index_labels': ['Name', 'Visitors', 'Unique Visitors', 'Watchers',
                                                                   'Forks', 'Stargazers', 'Clones', 'Unique Clones'],
                                                  'data': {}},
                                 'visitors_data': {'index_labels': ['Visitors', 'Unique Visitors'], 'data': {}},
                                 'clones_data': {'index_labels': ['Clones', 'Unique Clones'], 'data': {}},
                                 'stargazers_data': {'index_labels': ['Count'], 'data': {}},
                                 'referral_data': {'index_labels': ['Views', 'Unique Visitors'], 'data': {},
                                                   'timeframes': {}}}

    def __load_github_file_data(self):
        file_handle = None
        access_type = 'rb'
        write_function = pickle.load
        filedir = os.path.join(self._dir, "github_data")

        if not os.path.isdir(filedir) or (not os.path.isfile(filedir) and not os.path.isfile(filedir+".json")):
            self.__init_github_data_dicts()
            return
        elif os.path.isfile(filedir+".json"):
            filedir += ".json"
            access_type = 'r'
            write_function = json.load

        with open(filedir, access_type) as file_handle:
            self._github_data = write_function(file_handle)

        file_handle.close()

    def __write_github_data_file(self, file_type='bin'):
        file_handle = None
        filedir = os.path.join(self._dir, "github_data") if file_type == 'bin' else os.path.join(self._dir, "github_data.json")
        access_type = 'wb' if file_type == 'bin' else 'w'
        write_function = pickle.dump if file_type == 'bin' else json.dump

        if not os.path.isdir(self._dir):
            os.makedirs(self._dir)

        if self._github_data:
            with open(filedir, access_type) as file_handle:
                write_function(self._github_data, file_handle)
            file_handle.close()

    def __write_xlsx_workbook(self):
        workbook_path = os.path.join(self._dir, "github_data.xlsx")
        xlsx_writer = pd.ExcelWriter(workbook_path, engine='xlsxwriter')

        pd.DataFrame(self._github_data['general_data']['data'],
                     index=self._github_data['general_data']['index_labels']).to_excel(xlsx_writer,
                                                                                       sheet_name='General')
        pd.DataFrame(self._github_data['visitors_data']['data'],
                     index=self._github_data['visitors_data']['index_labels']).to_excel(xlsx_writer,
                                                                                        sheet_name='Views')
        pd.DataFrame(self._github_data['clones_data']['data'],
                     index=self._github_data['clones_data']['index_labels']).to_excel(xlsx_writer,
                                                                                      sheet_name='Clones')
        pd.DataFrame(self._github_data['stargazers_data']['data'],
                     index=self._github_data['stargazers_data']['index_labels']).transpose().to_excel(xlsx_writer,
                                                                                                      sheet_name='Stargazers')
        pd.DataFrame(self._github_data['referral_data']['data'],
                     index=self._github_data['referral_data']['index_labels']).to_excel(xlsx_writer,
                                                                                        sheet_name='Referrals')

        xlsx_writer.close()

    def __collect_github_data(self):
        self.__collect_general_stats()
        self.__collect_clones_stats()
        self.__collect_visitors_stats()
        self.__collect_referrals_stats()
        self.__collect_stargazers_stats()

    def __collect_referrals_stats(self):
        date_string = str(date.today())
        referrals = self._repo.get_top_referrers()
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
        stardates = self._repo.get_stargazers_with_dates()
        # Remove empty usernames
        stardates = [x for x in stardates if x.user.name]

        # Create build dict and create list based on date
        for stardate in stardates:
            if str(stardate.starred_at.date()) not in self._github_data['stargazers_data']['data']:
                self._github_data['stargazers_data']['data'][str(stardate.starred_at.date())] = 0
            self._github_data['stargazers_data']['data'][str(stardate.starred_at.date())] += 1

    def __collect_visitors_stats(self):
        visitors = self._repo.get_views_traffic()

        for visitor in visitors["views"]:
            if str(visitor.timestamp.date()) not in self._github_data['visitors_data']['data']:
                self._github_data['visitors_data']['data'][str(visitor.timestamp.date())] = [visitor.count,
                                                                                             visitor.uniques]

    def __collect_clones_stats(self):
        clones = self._repo.get_clones_traffic()

        for clone in clones["clones"]:
            if str(clone.timestamp.date()) not in self._github_data['clones_data']['data']:
                self._github_data['clones_data']['data'][str(clone.timestamp.date())] = [clone.count, clone.uniques]

    def __collect_general_stats(self):
        watches = self._repo.get_subscribers().totalCount
        forks = self._repo.get_forks().totalCount
        clones = self._repo.get_clones_traffic()
        stars = self._repo.get_stargazers().totalCount
        views = self._repo.get_views_traffic()
        date_string = str(date.today())

        if date_string not in self._github_data['general_data']['data']:
            self._github_data['general_data']['data'][date_string] = [self._repo.name, views["count"], views["uniques"],
                                                                      watches, forks, stars, clones["count"],
                                                                      clones["uniques"]]

    def collect_github_stats(self, load_binary=True):

        if load_binary:
            self.__load_github_file_data()
        else:
            self.__init_github_data_dicts()

        self.__collect_github_data()

    def write_github_stats(self, file_type='bin'):
        if file_type == 'xlsx':
            self.__write_xlsx_workbook()
        else:
            self.__write_github_data_file(file_type)



