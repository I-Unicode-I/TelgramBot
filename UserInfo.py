"""
Work with user info payload
"""
from typing import Dict, List, NamedTuple

import db
import logging

logging.basicConfig(filename='user.log', level=logging.DEBUG,
                    format='%(asctime)s:%(name)s:%(message)s')


class User(NamedTuple):
    """ Structure Info about user """
    id: str
    full_name: str
    user_name: str
    company: List[str]
    reminder_action: str


class Company(NamedTuple):
    """ Structure Info about company """
    market_name: str
    company_name: str
    close_price: float


class Info:
    def __init__(self):
        self._info_user = self._load_info_user()
        self._info_company = self._load_info_company()

    @staticmethod
    def insert_info_user(user: User):
        """ Insert all info about user """
        db.insert(
            'users', user._asdict()
        )

    @staticmethod
    def update_info_user(column: str, values: str, user_id: str):
        """ Updating info about companies or reminder in table users"""
        db.update(
            'users', column, values, user_id
        )

    def _load_info_user(self) -> List[User]:
        """ Get help for category payload from DB """
        info = db.fetchall(
            'users', 'id full_name user_name company reminder_action'.split()
        )
        info = self._fill_info_user(info)
        return info

    def _load_info_company(self) -> List[Company]:
        """ Get help for category payload from DB """
        info = db.fetchall(
            'company', 'market_name company_name close_price'.split()
        )
        info = self._fill_info_company(info)
        return info

    @staticmethod
    def _fill_info_user(info: List[Dict]) -> List[User]:
        """ Fill to each Users aliases, anything users name"""
        user_info_result = []
        for index, user in enumerate(info):
            if user['company'] is not None:
                info_user_company = user['company'].split(',')
                info_user_company = list(filter(None, map(str.strip, info_user_company)))
            else:
                info_user_company = ""
            user_info_result.append(User(
                id=user['id'],
                full_name=user['full_name'],
                user_name=user['user_name'],
                company=info_user_company,
                reminder_action=user['reminder_action']
            ))
        return user_info_result

    @staticmethod
    def _fill_info_company(info: List[Dict]) -> List[Company]:
        """ Fill to each Users aliases, anything users name"""
        company_info_result = []
        for index, company in enumerate(info):
            info_company = []
            info_company.append(company['company_name'])
            info_company.append(company['market_name'])
            info_company.append(company['close_price'])
            company_info_result.append(Company(
                market_name=company['market_name'],
                company_name=company['company_name'],
                close_price=company['close_price']
            ))
        return company_info_result

    def get_all_users(self) -> List[Dict]:
        """ Get info to users """
        return self._info_user

    def get_all_companies(self) -> List[Dict]:
        """ Get info to users """
        return self._info_company

    def get_user(self, user_id: str) -> User:
        """ Getting user info from his aliases """
        finded = None
        for user in self._info_user:
            for id in user.id:
                if user_id in id:
                    finded = user
        return finded

    def get_company(self, company_name: str) -> Company:
        """ Getting user info from his aliases """
        finded = None
        for company in self._info_company:
            for compan in company.company_name:
                if company_name in compan:
                    finded = company
        return finded

