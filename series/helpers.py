from django.db import connection
from common import utils

def find_team(player, date):
    with connection.cursor() as cursor:
        cursor.execute("SELECT teamID, MAX(dateJoined) FROM registers WHERE summonerName = %s "
                       "AND dateJoined <= date(%s) GROUP BY teamID", [player, date])
        return utils.dictfetchone(cursor)["teamID"]