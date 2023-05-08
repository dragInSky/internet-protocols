import vk_api
import configparser
import argparse

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


class ApiVk:
    def __init__(self, user_id):
        self._session = vk_api.VkApi(token=get_token())
        self._user_id = user_id

    @staticmethod
    def _items_list_to_str(items):
        str_items = ''
        for item in items['items']:
            str_items += str(item) + ','
        return str_items.removesuffix(',')

    def print_friends(self):
        friends = self._session.method("friends.get", {"user_id": self._user_id})

        str_friends = self._items_list_to_str(friends)

        friends_info = self._session.method("users.get", {"user_ids": str_friends})

        print("Friends list:")
        pretty_items_print(friends_info, second_column='first_name', third_column='last_name')

    def print_followers(self):
        followers = self._session.method("users.getFollowers", {"user_id": self._user_id})

        str_followers = self._items_list_to_str(followers)

        followers_info = self._session.method("users.get", {"user_ids": str_followers})

        print("Followers list:")
        pretty_items_print(followers_info, second_column='first_name', third_column='last_name')

    def print_subscriptions(self):
        subscriptions = self._session.method("users.getSubscriptions", {"user_id": self._user_id})

        group_ids = self._items_list_to_str(subscriptions['groups'])

        subscriptions_info = self._session.method("groups.getById", {"group_ids": group_ids})

        print("Subscriptions list:")
        pretty_items_print(subscriptions_info, second_column='name', third_column='screen_name')

    def print_groups(self):
        groups = self._session.method("groups.get", {"user_id": self._user_id})

        group_ids = self._items_list_to_str(groups)

        groups_info = self._session.method("groups.getById", {"group_ids": group_ids})

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

    api_vk = ApiVk(args.userId)
    if args.friends:
        api_vk.print_friends()
    if args.followers:
        api_vk.print_followers()
    if args.subscriptions:
        api_vk.print_subscriptions()
    if args.groups:
        api_vk.print_groups()


if __name__ == '__main__':
    main()
