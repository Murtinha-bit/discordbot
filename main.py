from email import header
from click import pass_context
import requests
import json
import nextcord
from nextcord.ext import commands
from nextcord import FFmpegPCMAudio

from variables import api_variables



intents = nextcord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix= '$', intents=intents)



def get_cat():
    CATurl="https://api.thecatapi.com/v1/images/search"

    headers = {
        'x-rapidapi-key' : api_variables.CATTOKEN,
        'x-rapidapi-host': 'api.thecatapi.com'
    }

    response=requests.request("GET", CATurl, headers=headers)
    json_data= json.loads(response.content)
    imgcat = json_data[0]['url']
    return(imgcat)


def get_quote():
   #  Essa função pega uma api de frases aleatorias de starwars
    response = requests.get("http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote", verify=False)
    json_data= json.loads(response.content)
    quote= json_data['content']
    return(quote)

def poke_info(pokemon):
   #  Essa função pega uma api de informacoes de pokemons
   
    response = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon, verify=False)
    json_data= json.loads(response.content)
    quote= json_data['forms']["name"]
    return(quote)


@client.event
async def on_ready():
    print("O bot esta online!")
    print("---------------------------")

@client.event
async def on_member_join(member):
    response = get_cat()
    channel = client.get_channel(880479289055797348)
    await channel.send(response)
    await channel.send("Bem-vindoooooooo")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(880479289055797348)
    await channel.send("Nunca gostei dela mesmo")

@client.command()
async def oi(ctx):
    await ctx.send("Ola")

@client.command()
async def thau(ctx):
    await ctx.send("Bye Bye")

@client.command(pass_context= True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('ratinho.mp3')
        player = voice.play(source)
    else:
        await ctx.send("Cara conecta ai em um voice fdp")


@client.command(pass_context= True)
async def leave(ctx):
    if(ctx.author.voice):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Vão se fuder, fuiii")
    else:
        await ctx.send("Eu não estou em um voice burro")


@client.command(pass_context= True)
async def pause(ctx):
    voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Mas não tem audio tocando maluco")

@client.command(pass_context= True)
async def resume(ctx):
    voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Não tem musica pausada lindo")

@client.command(pass_context= True)
async def stop(ctx):
    voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command(pass_context= True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(arg)
    player = voice.play(source)

@client.command()
async def gato(ctx):
    gatinho = get_cat()
    await ctx.send(gatinho)

@client.command()
async def starwars(ctx):
    frase = get_quote()
    await ctx.send(frase)

@client.command()
async def pokemon(ctx):
    frase = poke_info("Pikachu")
    await ctx.send(frase)

client.run(api_variables.TOKEN)