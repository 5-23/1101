import os
from func import emojis

from nextcord.ext import commands , tasks
from nextcord import *

from nextcord.abc import GuildChannel

import random

INTENTS = Intents.default()

INTENTS.messages = True
INTENTS.guilds   = True
INTENTS.members  = True

client = commands.Bot(command_prefix = "asdf" , intents = INTENTS)

@tasks.loop(seconds = 30)
async def loop():
    await client.change_presence(activity = Game(name = f"{len(client.guilds)}개의 서버에서 인증"))

@client.event
async def on_ready():
    loop.start()
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

@client.slash_command(description = "인증을 만듭니다")
async def 인증만들기(inter : Interaction):
    pass

@client.event
async def on_interaction(inter : Interaction):
    if inter.type == InteractionType.application_command:
        try:
            if str(inter.channel.type) == "private":return await inter.followup.send(embed = Embed(title = "오류" , description = "DM에서는 사용하실수 없어요!" , color = 0xff0000) , ephemeral = True)

            if inter.user.guild_permissions.administrator:return await inter.response.send_modal(verifyMake(inter = inter))
            if utils.get(inter.guild.members , id = client.user.id).guild_permissions.administrator:return await inter.followup.send(embed = Embed(title = "오류" , description = "봇이 어드민이 아닙니다." , color = 0xff0000) , ephemeral = True)
            await inter.followup.send(embed = Embed(title = "오류" , description = "당신은 어드민이 아닙니다." , color = 0xff0000) , ephemeral = True)
        except Exception as e:
            print(e)

    elif inter.type == InteractionType.component:
        try:await inter.response.send_modal(verifyModal(length = int(inter.data["custom_id"].split("|")[1]) , role = int(inter.data["custom_id"].split("|")[0]) , inter = inter))
        except Exception as e:print(e)


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
        await inter.response.defer()
        if self.code == self.input.value.lower().replace("0" , "o"):
            try:await inter.user.add_roles(utils.get(self.inter.guild.roles , id = self.role))
            except:return await inter.followup.send("알수없는 오류가있어요... DM으로 문의해주세요!" , ephemeral = True)

            await inter.followup.send(embed = Embed(title = "인증 성공!" , description = "인증에 성공하셨어요!" , color = 0x00b9ff) , ephemeral = True)
        else:
            await inter.followup.send(embed = Embed(title = "인증 실패!" , description = "인증에 실패하셨어요... 혹시 로봇은 아니죠...?" , color = 0xff8d00) , ephemeral = True)

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
        await inter.response.defer()
        try:a = int(self.Length.value)
        except:return await inter.followup.send(embed = Embed(title = "오류" , description = "인증코드의 길이가 숫자가 아닙니다" , color = 0xff0000) , ephemeral = True)
        
        if a < 1:return await inter.followup.send(embed = Embed(title = "오류" , description = "인증코드의 최소길이는 1입니다" , color = 0xff0000) , ephemeral = True)


        await inter.followup.send("만들기 성공!" , ephemeral = True)
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
            if ok:
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
    async def yes(self , button : Button , inter : Interaction):
        await inter.response.defer()
        embed = Embed(title = "문의가 도착하였습니다." , description=f"{inter.message.embeds[0].description.replace('내용 : ' , '')} \n\nid : {inter.user.id}\nname:{inter.user}" , color = random_color())
        try:
            if "http" in str(inter.message.embeds[0].url):
                embed.set_image(url = str(inter.message.embeds[0].url))
        except:
            pass
        await client.get_channel(957508032038834186).send(inter.user.id , embed=embed)
        self.clear_items()
        self.add_item(ui.Button(label = "공식서버", style = ButtonStyle.link , url = "https://discord.com/invite/w2Fw7UeZmY"))
        await inter.message.edit(embed = Embed(title = "문의가 완료되었습니다. 감사합니다!" , description=inter.message.embeds[0].description , color = inter.message.embeds[0].color) , view = self)
        del self
    @ui.button(label="아니요" , style=ButtonStyle.red , emoji=emojis.ax())
    async def no(self , button : Button , inter : Integration):
        await inter.message.delete()
        del self



        
token = os.environ['TOKEN']
# client.run(token)
