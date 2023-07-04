from main_project import client, collection, db


def add_user(new_user):
    result = client.UserDb.UserCollection.insert_one(new_user)
    return result


def find_user(email):
    result = client.UserDb.UserCollection.find_one({"email": email}, {"object_id": 0})
    return result

def update_Verify(email):
        try:
            result = client.UserDb.UserCollection.update_one({"email": email}, {"$set": {"is_verified": True}})
            result = True if result.acknowledged else False
            # if result.acknowledged == True:
            #
            #     return True
            # else:
            #     return False
            return result
        except Exception as e:
            return str(e)

def update_password(email, new_password):
    try:
        result = client.UserDb.UserCollection.update_one({"email": email}, {"$set": {"password": new_password}})
        return result
    except Exception as e:
        return str(e)

def remove_user(email):
    try:
        result = client.UserDb.UserCollection.update_one({"email": email}, {"$set": {"is_verified": False}})
        result = True if result.acknowledged else False
        return result
    except Exception as e:
        return str(e)