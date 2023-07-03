from main_project import client, collection, db


def add_user(new_user):
    result = client.UserDb.UserCollection.insert_one(new_user)
    return result


def find_user(email):
    result = client.UserDb.UserCollection.find_one({"email": email}, {"object_id": 0})
    return result
