import discord
from discord.ext import commands
import random
import asyncio
import datetime
from discord.ext.commands import has_permissions, MissingPermissions
from discord_components import DiscordComponents, Button, ButtonStyle

# Config Kısmı

token             = ''
prefix            = ''
logkanali         = '' # kanal id
giriskanali       = '' # kanal id
cikiskanali       = '' # kanal id
kayıtsız          = '' # Rol adı
whitelist         = '' # Rol adı
tsip              = ''
serverip          = ''
discordurl        = 'http://discord.gg/'
aktifimage    = ''
restartimage  = ''
bakımimage    = ''
servericon    = ''

# Tüm Configleri Doldurmadan Bot Tam Anlamıyla Çalışmaz

intents = discord.Intents().all()
client = commands.Bot(command_prefix=prefix, intents = intents)
client.ticket_configs = {}
DiscordComponents(client)


@client.event
async def on_ready():
    async with aiofiles.open("ticket_configs.txt", mode="a") as temp:
        pass

    async with aiofiles.open("ticket_configs.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            client.ticket_configs[int(data[0])] = [int(data[1]), int(data[2]), int(data[3])]
    print('Discord Botu Aktif!')
    await client.change_presence(activity=discord.Game(name=f"🔥 Test Ediliyor...  🔥")) # Discord Botun Oynuyor Kısmı
    await client.change_presence(activity=discord.Game(name=f"🔥 Test Botu  🔥")) # İstediğiniz gibi değiştirebilirsiniz.
    client.remove_command('help')  # Bunu Silmenizi Önermem Kötü Bir help teması var siz yeni help yazarsanız daha hoş durur.

async def ch_pr():
    await client.wait_until_ready()

    statuses = ["🔥 Test Ediliyor...  🔥", "🔥 Test Botu  🔥"] # Yukarda Değiştirdiğiniz yazıyı burayada eklemeniz gerekir!

    while not client.is_closed():

        status = random.choice(statuses)
        await client.change_presence(activity=discord.Game(name=status))

        await asyncio.sleep(5) # Yazının Kaç Saniyede Bir Değişceğini ayarlayabilirsiniz
client.loop.create_task(ch_pr())

@client.event
async def on_raw_reaction_add(payload):
    global reaction
    global reaction2
    global ticket_channel
    
    if payload.member.id != client.user.id and str(payload.emoji) == u"📩":
        msg_id, channel_id, category_id = client.ticket_configs[payload.guild_id]

        if payload.message_id == msg_id:
            guild = client.get_guild(payload.guild_id)

            for category in guild.categories:
                if category.id == category_id:
                    break

            channel = guild.get_channel(channel_id)

            ticket_channel = await category.create_text_channel(f"ticket-{payload.member.display_name}", topic=f"Ticket Sahibi {payload.member.display_name}.", permission_synced=True)

            await ticket_channel.set_permissions(payload.member, read_messages=True, send_messages=True)

            message = await channel.fetch_message(msg_id)

            staff = discord.utils.get(payload.member.guild.roles, name=staffrol)
            
            ticketembedi = discord.Embed(
                description = f"{payload.member.mention} Başarıyla Ticket Oluşturuldu! {staff.mention} Ekibimiz En Kısa Sürede Sizle İlgilenecektir.",
                color = 2
            )
            
            ticketembedi.set_footer(text="Ticketi Sonlandırmak için -kapat Yazmalısın!")
            
            await ticket_channel.send(embed=ticketembedi)
            silincek = await ticket_channel.send(f"{staff.mention}")
            await asyncio.sleep(0.1)
            await silincek.delete()
                
                
            try:
                await client.wait_for("message", check=lambda m: m.channel == ticket_channel and m.author == payload.member and m.content == "-kapat")
            
            except:
                print('.')
                    
            else:
                await asyncio.sleep(0.7)
                await asyncio.sleep(0.7)
                await ticket_channel.edit(name=f"{payload.member.display_name} - Kapatıldı")
                await message.remove_reaction(payload.emoji, payload.member)
                await ticket_channel.set_permissions(payload.member, read_messages=False, send_messages=False)
                
                
                embed = discord.Embed(
                    title = 'Ticket Başarıyla Sonlandırılmıştır!',
                    description = f'{payload.member.mention} Kişisi Odadan Çıkarılmıştır.',
                    color = 0
                )

                embed.set_footer(text="Created By Fap")
                
                embed.set_author(name="Ticket system")
                
                ticketbuttons = [Button(label="Ticket Sil", custom_id="TicketSil", style=ButtonStyle.red, emoji="❌")]
                
                await ticket_channel.send(embed=embed, components=ticketbuttons)

@client.command()
@has_permissions(administrator=True)
async def ticketayarla(ctx, msg: discord.Message=None, category: discord.CategoryChannel=None):
    try:
        ctxguildkontrolmysqlbaglantisi(ctx)

        for x in guildkontrolresult:
            print(x)

            if msg is None or category is None:
                await ctx.channel.send("Lütfen Doğru Şekilde Ayarlayınız!.")
                return

            client.ticket_configs[ctx.guild.id] = [msg.id, msg.channel.id, category.id]

            async with aiofiles.open("ticket_configs.txt", mode="r") as file:
                data = await file.readlines()

            async with aiofiles.open("ticket_configs.txt", mode="w") as file:
                await file.write(f"{ctx.guild.id} {msg.id} {msg.channel.id} {category.id}\n")

                for line in data:
                    if int(line.split(" ")[0]) != ctx.guild.id:
                        await file.write(line)

            await msg.add_reaction(u"📩")
            await ctx.channel.send("Ticket Sistemi Başarıyla Kuruldu.")
        if x == None:
            print('test')
    except:
        print("Kayıtsız Sunucu Denemesi")

@client.command(pass_context=True)
@has_permissions(administrator=True)
async def ticket(ctx):
    embed = discord.Embed(
        title = 'Ticket system',
        description = 'Ticket Oluşturmak İçin 📩 Tıklayınız.',
        color = 0
    )

    embed.set_footer(text="Created By Fap")

    await ctx.send(embed=embed)
    return

#Destek Komutu
@client.command()
async def destek(ctx):        
    role = discord.utils.get(ctx.guild.roles, name=whitelist)
    if role in ctx.author.roles:
        embed = discord.Embed(
            title = f'{ctx.author.name} Destek Talebi',
            description = 'Destek Talebiniz Alınmıştır. En Yakın Zamanda Destek Ekibimiz Size Yardımcı Olacaktır.',
            color = 0
        )

        embed.set_footer(text=f"{ctx.guild.name}")

        await ctx.send(embed=embed)
        return
    else:
        await ctx.send('Kayıtlı Oyuncularımız Sadece Destek Talebinde Bulunabilir!')

#Kayıt Komutu
@client.command()
async def kayıt(ctx):

    role = discord.utils.get(ctx.guild.roles, name=kayıtsız)
    if role in ctx.author.roles:
        embed = discord.Embed(
            title = f'{ctx.author.name} Kayıt Talebi',
            description = 'Kayıt Talebiniz Alınmıştır. En yakın zamanda Kayıt Ekibimiz Size Yardımcı Olacaktır.',
            color = 0
        )

        embed.set_footer(text=f"{ctx.guild.name}")

        await ctx.send(embed=embed)
        return
    else:
        await ctx.send('Kayıtlı Oyuncularımız Kayıt Talebinde Bulunamaz!')


#Aktif Komutu
@client.command()
@has_permissions(manage_guild=True) # Sadece Manage_guild Yetkisi Olanlar Kullanabilir
async def aktif(ctx):
        aktifembed = discord.Embed(description="Sunucumuz Aktiftir! ✅")
        aktifembed.set_author(name="Discord Adresimiz", url=f"{discordurl}", icon_url=servericon)
        aktifembed.set_thumbnail(url=aktifimage)
        aktifembed.set_image(url=aktifimage)
        aktifembed.add_field(name=f'Server IP : {serverip} ', value= f'Ts3 : {tsip}', inline=False) 
        aktifembed.add_field(name=f'{ctx.guild.name} Herkese iyi roller diler.', value= '🎉', inline=False)
        await ctx.send(embed=aktifembed)

#Restart Komutu
@client.command()
@has_permissions(manage_guild=True) # Sadece Manage_guild Yetkisi Olanlar Kullanabilir
async def restart(ctx):
        restartembed = discord.Embed(description="Sunucumuza Restart Atılıyor ❗️❗️") 
        restartembed.set_thumbnail(url=restartimage)
        restartembed.set_image(url=restartimage)
        restartembed.set_author(name="Discord Adresimiz", url=f"{discordurl}", icon_url=servericon)
        restartembed.add_field(name=f'Datalarınızın Zarar Görmemesi İçin Lütfen Oyundan Çıkış Yapalım', value="Bizi Tercih Ettiğiniz İçin Teşekkür Ederiz", inline=False) 
        restartembed.add_field(name=f'{ctx.guild.name} Ailesi', value= '💖', inline=False)
        await ctx.send(embed=restartembed)

#Bakım Komutu
@client.command()
@has_permissions(manage_guild=True) # Sadece Manage_guild Yetkisi Olanlar Kullanabilir
async def bakım(ctx):
        bakımembed = discord.Embed(description="Sunucumuz Kısa Süreliğine Bakıma Alınmıştır ❗️❗️")
        bakımembed.set_thumbnail(url=bakımimage)
        bakımembed.set_author(name="Discord Adresimiz", url=f"{discordurl}", icon_url=servericon)
        bakımembed.set_image(url=bakımimage)
        bakımembed.add_field(name=f'En Kısa Sürede Tekrar Aktif Verilecektir', value="Bizi Tercih Ettiğiniz İçin Teşekkür Ederiz", inline=False) 
        bakımembed.add_field(name=f'{ctx.guild.name} Ailesi', value= '💖', inline=False)
        await ctx.send(embed=bakımembed)


# Kayıtal Komutu
@client.command(pass_context=True)
@has_permissions(manage_nicknames=True)
async def kayıtal(ctx, user: discord.Member):
    rol = discord.utils.get(ctx.guild.roles, name=whitelist)
    rol2 = discord.utils.get(ctx.guild.roles, name=kayıtsız)
    await user.add_roles(rol)
    await user.remove_roles(rol2)
    await ctx.message.add_reaction(u"✅")
    channel = client.get_channel(int(logkanali))
    await channel.send(f"<@!{ctx.author.id}> isimli yetkili , {user.mention} isimli Oyuncuya {rol.name} permi verdi!")

#Avatar Komutu
@client.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    if avamember == None:
        await ctx.send('Lütfen Birini Etiketleyiniz')
    else:
        userAvatarUrl = avamember.avatar_url
        await ctx.send(userAvatarUrl)
        return

#Clear Komutu
@client.command()
@has_permissions(manage_guild=True) # Sadece Manage_guild Yetkisi Olanlar Kullanabilir
async def clear(ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.channel.send(f'Başarıyla {amount} tane mesaj silindi', delete_after=2)

@client.event
async def on_member_join(member):
        date_format = "%x, %X"
        girisembed = discord.Embed(title=f"discord id : {member.id}")
        girisembed.set_thumbnail(url=f'{member.avatar_url}')
        girisembed.set_author(name=member.name, icon_url=member.avatar_url)
        girisembed.add_field(name="Hesap Kuruluş Tarihi: ", value=member.created_at.strftime(date_format))
        girisembed.set_footer(text=f"{member.guild.name}", icon_url=f"{member.avatar_url}")
        giriskanal = client.get_channel(int(giriskanali))
        await giriskanal.send(member.mention, embed=girisembed)

@client.event
async def on_member_remove(member):

        membercikis = datetime.datetime.now()
        membercikistarihi = membercikis.strftime("%x, %X")
        
        cikisembed = discord.Embed(title=f"Bir Kullanıcı Sunucudan Çıktı")
        cikisembed.set_author(name=f"{member.name}#{member.discriminator}" ,icon_url=member.avatar_url)
        cikisembed.set_thumbnail(url=f'{member.avatar_url}')
        cikisembed.add_field(name="Sunucudan Ayrılma Tarihi", value=f"{membercikistarihi}", inline=False)
        cikisembed.add_field(name="Kullanıcı Bilgileri:", value=f"{member.name}#{member.discriminator}  -  {member.id}", inline=False)
        cikisembed.set_footer(text=f"{member.guild.name}", icon_url=member.guild.icon_url)
        giriskanal = client.get_channel(int(cikiskanali))
        await giriskanal.send(member.mention, embed=cikisembed)
    
@client.event
async def on_guild_join(guild):
    async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url('https://discord.com/api/webhooks/944987365485715587/vpkUrIavQHXA34vbzNnZ7ilmlRuAMbE0GSovngNzx5ouNtEbCZB6WYljjFeb7wX0B8wL', adapter=AsyncWebhookAdapter(session))

            e = discord.Embed(title=f"Bot {guild} Sunucunda Kullanıldı", description=f"{guild.owner}")
            e.add_field(name="Sunucu İD :", value=f"{guild.id}")

            await webhook.send(embed=e)

client.run(f'{token}')