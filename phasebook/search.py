from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    # Implement search here!
    output = []
    #Add set to store unique ids and avoid duplicates
    ids_seen = set()

    def sort_priority(user):
        if args.get('id') == user['id']:
            return 1
        elif args.get('name') and args['name'].lower() in user['name'].lower():
            return 2
        elif args.get('age') and int(args['age']) - 1 <= user['age'] <= int(args['age']) + 1:
            return 3
        elif args.get('occupation') and args['occupation'].lower() in user['occupation'].lower():
            return 4
        else:
            return 5 #Default priority for unmatched users


    for key in args.keys():
        for user in USERS:
            user_id = user["id"]
            if user_id in ids_seen:
                #Skips user that already added to result
                continue
        
            if(
                (key == 'id' and args[key] == user_id) or \
                (key in ['name', 'occupation'] and args[key].lower() in user[key].lower()) or \
                (key == 'age' and int(args[key]) - 1 <= int(user[key]) <= int(args[key]) + 1)
            ):
                output.append(user)
                ids_seen.add(user_id)
    
    sorted_match = sorted(output, key=sort_priority)

    return sorted_match
