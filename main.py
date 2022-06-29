import os
from func import emojis

from nextcord.ext import commands
from nextcord import *

from nextcord.abc import GuildChannel

import random
# INTENTS = Intents.all()

INTENTS = Intents.default()

INTENTS.messages = True
INTENTS.guilds   = True
INTENTS.members  = True

client = commands.Bot(command_prefix = "asdf" , intents = INTENTS)

voteCount  = 0
voteCount2 = 0
voteCount3 = 0
voteCount4 = 0

@client.event
async def on_ready():
    print("ready")

@client.event
async def on_message(message : Message):
    try:
        if str(message.channel.type) == "private":
            if message.author.bot == False:
                embed = Embed(title = f"문의를 하실 건가요?",description = f"```\n내용: {message.content}```\n",timestamp=message.created_at , color = random_color())
                embed.set_footer(text = "문의는 영구적으로 보관됩니다")
                try: 
                    img = str(message.attachments[0])
                    embed.set_image(url = img)
                    embed.url = img
                except: 
                    pass
                await message.channel.send(embed = embed , view = inquiry())
    except:
        pass

def random_color():return random.randint(0 , 0xffffff)

@client.slash_command(description = "테스트")
async def 테스트(inter : Interaction):
    await inter.response.send_message("ㅁㄴㅇㄹ" , view = button())

@client.event
async def on_interaction(inter : Interaction):
    if inter.type == InteractionType.application_command:
        if inter.user.guild_permissions.administrator:return await inter.response.send_modal(verifyMake(inter = inter))
        if utils.get(inter.guild.members , id = client.user.id).guild_permissions.administrator:return await inter.response.send_message(embed = Embed(title = "오류" , description = "봇이 어드민이 아닙니다." , color = 0xff0000) , ephemeral = True)
        await inter.response.send_message(embed = Embed(title = "오류" , description = "당신은 어드민이 아닙니다." , color = 0xff0000) , ephemeral = True)

    elif inter.type == InteractionType.component:
        try:await inter.response.send_modal(verifyModal(length = int(inter.data["custom_id"].split("|")[1]) , role = int(inter.data["custom_id"].split("|")[0]) , inter = inter))
        except:pass
    print(inter.data)


class button(ui.View):
    def __init__(self , name : str , role : str , length : str):
        super().__init__(timeout = None)
        # self.button = ui.Button(label = name , style = ButtonStyle.green , custom_id = "verify")
        self.children[0].label = name
        self.children[0].custom_id = f"{role}|{length}"

    @ui.button(label = "loding..." , style = ButtonStyle.green)
    async def callback(self , button : Button , inter : Interaction):
        await inter.response.send_modal(verifyModal(length = int(button.custom_id.split("|")[1]) , role = int(button.custom_id.split("|")[0]) , inter = inter))

class verifyModal(ui.Modal):
    def __init__(self , length : int , role : int , inter : Interaction):
        super().__init__("코드를 입력해주세요!" , timeout = None)
        string  = "q w e r t y u i o p a s d f g h j k l z x c v b n m"
        integer = "1 2 3 4 5 6 7 8 9"

        self.code = ""
        for i in range(length):
            if random.randint(0 , 1) == 1:t = random.choice(string.split(" "))
            else:t = random.choice(integer.split(" "))
            self.code += t

        self.input = ui.TextInput(label = f"코드 : {self.code}" , placeholder = self.code)
        self.role = role
        self.inter = inter

        self.add_item(self.input)

    async def callback(self, inter : Interaction):
        if self.code == self.input.value.lower().replace("0" , "o"):
            try:await inter.user.add_roles(utils.get(self.inter.guild.roles , id = self.role))
            except:return await inter.response.send_message("알수없는 오류가있어요... DM으로 문의해주세요!" , ephemeral = True)

            await inter.response.send_message("성공" , ephemeral = True)
        else:
            await inter.response.send_message("실패" , ephemeral = True)

class verifyMake(ui.Modal):
    def __init__(self , inter : Interaction):
        super().__init__("인증만들기" , timeout = None)

        self.EmbedTitle       = ui.TextInput(label = "임베드 제목을 써주세요" , placeholder = "인증하기")
        self.EmbedDescription = ui.TextInput(label = "임베드 설명을 써주세요" , placeholder = "버튼을눌러 인증하고 {role}역할을 받으세요!")
        self.ButtonName       = ui.TextInput(label = "버튼이름을 써주세요"    , placeholder = "인증하기")
        self.Role             = verifySelect(inter = inter)
        self.Length           = ui.TextInput(label = "인증코드의 길이를 써주세요" , placeholder = "10")

        self.add_item(self.EmbedTitle)
        self.add_item(self.EmbedDescription)
        self.add_item(self.ButtonName)
        self.add_item(self.Role)
        self.add_item(self.Length)

    async def callback(self, inter : Interaction):
        await inter.response.send_message("만들기 성공!" , ephemeral = True)
        print(self.ButtonName.value);print(self.Role.values);print(self.Length.value)
        await inter.channel.send(embed = Embed(title = self.EmbedTitle.value , description = self.EmbedDescription.value.replace("{role}" , f"<@&{self.Role.values[0]}>")) , view = button(name = self.ButtonName.value , role = self.Role.values[0] , length = self.Length.value))

class verifySelect(ui.Select):
    def __init__(self , inter : Interaction):
        options = []
        roles : list[Role] = inter.guild.roles
        
        clientRole = utils.get(inter.guild.members , id = client.user.id).roles[1:]
        clientRole.reverse()
        clientRole = clientRole[0]

        ok = False
        roles = roles[1:]
        roles.reverse()
        for role in roles[1:]:
            print(ok)
            if ok:
                print(role)
                if not role.is_bot_managed():options.append(SelectOption(label = role.name , value = str(role.id)))
            if clientRole == role:ok = True
        
        if options == []:
            super().__init__(
                placeholder = "봇이 추가할수 있는역할이 없어요...",
                min_values  = 1,
                max_values  = 1,
                options     = [SelectOption(label = "." , value = 0)],
                disabled    = True
            )
        else:
            super().__init__(
                placeholder = "추가할 역할을 고르세요",
                min_values  = 1,
                max_values  = 1,
                options     = options
            )

    async def callback(self, inter : Interaction):
        return self
           
class inquiry(ui.View):
    def __init__(self):
        super().__init__(timeout=600)
    @ui.button(label="네" , style=ButtonStyle.green , emoji=emojis.check())
    async def yes(self , button : Button , inter : Integration):
        embed = Embed(title = "문의가 도착하였습니다." , description=f"{inter.message.embeds[0].description.replace('내용 : ' , '')} \n\nid : {inter.user.id}\nname:{inter.user}" , color = random_color())
        try:
            if "http" in str(inter.message.embeds[0].url):
                embed.set_image(url = str(inter.message.embeds[0].url))
        except:
            pass
        await client.get_channel(957508032038834186).send(embed=embed)
        self.clear_items()
        self.add_item(ui.Button(label = "공식서버", style = ButtonStyle.link , url = "https://discord.com/invite/w2Fw7UeZmY"))
        await inter.message.edit(embed = Embed(title = "문의가 완료되었습니다. 감사합니다!" , description=inter.message.embeds[0].description , color = inter.message.embeds[0].color) , view = self)
        del self
    @ui.button(label="아니요" , style=ButtonStyle.red , emoji=emojis.ax())
    async def no(self , button : Button , inter : Integration):
        await inter.message.delete()
        del self

token = os.environ['TOKEN']
client.run(token)
