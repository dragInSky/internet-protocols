import configparser
import argparse
import requests

from tabulate import tabulate


def get_token():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['vk_api']['access_token']


def pretty_items_print(items_info, second_column, third_column):
    output = list(list())
    for item_info in items_info:
        row = [
            item_info['id'],
            item_info[second_column],
            item_info[third_column],
        ]
        output.append(row)
    print(tabulate(output, headers=['id', second_column, third_column]))


class VkApi:
    def __init__(self, user_id):
        self._user_id = user_id

    @staticmethod
    def _items_list_to_str(items):
        str_items = ''
        for item in items['items']:
            str_items += str(item) + ','
        return str_items.removesuffix(',')

    @staticmethod
    def request_pattern(method_name, params):
        return f"https://api.vk.com/method/{method_name}?" \
               f"{params}&access_token={get_token()}&v=5.131"

    def print_friends(self):
        friends = requests.get(
            self.request_pattern("friends.get", f"user_id={self._user_id}")
        ).json()['response']

        str_friends = self._items_list_to_str(friends)

        friends_info = requests.get(
            self.request_pattern("users.get", f"user_ids={str_friends}")
        ).json()['response']

        print("Friends list:")
        pretty_items_print(friends_info, second_column='first_name', third_column='last_name')

    def print_followers(self):
        followers = requests.get(
            self.request_pattern("users.getFollowers", f"user_id={self._user_id}")
        ).json()['response']

        str_followers = self._items_list_to_str(followers)

        followers_info = requests.get(
            self.request_pattern("users.get", f"user_ids={str_followers}")
        ).json()['response']

        print("Followers list:")
        pretty_items_print(followers_info, second_column='first_name', third_column='last_name')

    def print_subscriptions(self):
        subscriptions = requests.get(
            self.request_pattern("users.getSubscriptions", f"user_id={self._user_id}")
        ).json()['response']

        group_ids = self._items_list_to_str(subscriptions['groups'])

        subscriptions_info = requests.get(
            self.request_pattern("groups.getById", f"group_ids={group_ids}")
        ).json()['response']

        print("Subscriptions list:")
        pretty_items_print(subscriptions_info, second_column='name', third_column='screen_name')

    def print_groups(self):
        groups = requests.get(
            self.request_pattern("groups.get", f"user_id={self._user_id}")
        ).json()['response']

        group_ids = self._items_list_to_str(groups)

        groups_info = requests.get(
            self.request_pattern("groups.getById", f"group_ids={group_ids}")
        ).json()['response']

        print("Groups list:")
        pretty_items_print(groups_info, second_column='name', third_column='screen_name')


def main():
    parser = argparse.ArgumentParser(description='vk_api pretty print')
    parser.add_argument(
        '-i',
        '--userId',
        type=int,
        default=145488443,
        help='target user id'
    )
    parser.add_argument(
        '-f',
        '--friends',
        action="store_true",
        help='friends print'
    )
    parser.add_argument(
        '-l',
        '--followers',
        action="store_true",
        help='followers print'
    )
    parser.add_argument(
        '-s',
        '--subscriptions',
        action="store_true",
        help='subscriptions print'
    )
    parser.add_argument(
        '-g',
        '--groups',
        action="store_true",
        help='groups print'
    )
    args = parser.parse_args()

    vk_api = VkApi(args.userId)
    if args.friends:
        vk_api.print_friends()
    if args.followers:
        vk_api.print_followers()
    if args.subscriptions:
        vk_api.print_subscriptions()
    if args.groups:
        vk_api.print_groups()


if __name__ == '__main__':
    main()
