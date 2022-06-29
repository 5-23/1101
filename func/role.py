from nextcord import Member , Guild , utils
from nextcord.utils import get

def premium(guild : Guild , member : Member) -> bool:
    try:return (guild.get_role(874207259536797756) in utils.get(guild.members , id = member.id).roles)
    except:return False

def dev(guild : Guild , member : Member) -> bool:
    try:return (guild.get_role(869937710117322792) in utils.get(guild.members , id = member.id).roles)
    except:return False

def artist(guild : Guild , member : Member) -> bool:
    try:return (guild.get_role(955655494100484117) in utils.get(guild.members , id = member.id).roles)
    except:return False

def bughunt(guild : Guild , member : Member) -> bool:
    try:return (guild.get_role(969018408970620958) in utils.get(guild.members , id = member.id).roles)
    except:return False

def donate(guild : Guild , member : Member) -> bool:
    try:return (guild.get_role(963735688862400512) in utils.get(guild.members , id = member.id).roles)
    except:return False

def earlyUser(guild : Guild , member : Member) -> bool:
    try:return (guild.get_role(959739652825313320) in utils.get(guild.members , id = member.id).roles)
    except:return False

def idea(guild : Guild , member : Member) -> bool:
    try:return (guild.get_role(964455387388588062) in utils.get(guild.members , id = member.id).roles)
    except:return False