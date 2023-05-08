import vk_api
import configparser
import argparse

from tabulate import tabulate


def get_token():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['vk_api']['access_token']


session = vk_api.VkApi(token=get_token())
vk = session.get_api()


def pretty_items_print(items_info, first_name='first_name', last_name='last_name'):
    output = list(list())
    for user_info in items_info:
        row = [
            user_info['id'],
            user_info[first_name],
            user_info[last_name],
        ]
        output.append(row)
    print(tabulate(output, headers=['id', first_name, last_name]))


def items_list_to_str(items):
    str_users = ''
    for user in items['items']:
        str_users += str(user) + ','
    return str_users.removesuffix(',')


def print_users(user_id, method_name, title):
    users = session.method(method_name, {"user_id": user_id})

    str_users = items_list_to_str(users)

    users_info = session.method("users.get", {"user_ids": str_users})

    print(title)
    pretty_items_print(users_info, first_name='first_name', last_name='last_name')


def print_subscriptions(user_id):
    subscriptions = session.method("users.getSubscriptions", {"user_id": user_id})

    group_ids = items_list_to_str(subscriptions['groups'])

    subscriptions_info = session.method("groups.getById", {"group_ids": group_ids})

    print("Subscriptions list:")
    pretty_items_print(subscriptions_info, first_name='name', last_name='screen_name')


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
        help='friends pretty print'
    )
    parser.add_argument(
        '-l',
        '--followers',
        action="store_true",
        help='followers pretty print'
    )
    parser.add_argument(
        '-s',
        '--subscriptions',
        action="store_true",
        help='subscriptions pretty print'
    )
    args = parser.parse_args()

    if args.friends:
        print_users(args.userId, method_name="friends.get", title="Friends list:")
    if args.followers:
        print_users(args.userId, method_name="users.getFollowers", title="Followers list:")
    if args.subscriptions:
        print_subscriptions(args.userId)


if __name__ == '__main__':
    main()
