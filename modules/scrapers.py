import wikipedia
from google_images_download import google_images_download
import urbandict
import re
@bot.on(events.NewMessage(outgoing=True, pattern=".img (.*)"))
@bot.on(events.MessageEdited(outgoing=True, pattern=".img (.*)"))
async def img_sampler(e):
 await e.edit('Processing...')
 start=round(time.time() * 1000)
 s = e.pattern_match.group(1)
 lim = re.findall(r"lim=\d+", s)
 try:
  lim = lim[0]
  lim = lim.replace('lim=', '')
  s = s.replace('lim='+lim[0], '')
 except IndexError:
  lim = 2
 response = google_images_download.googleimagesdownload()
 arguments = {"keywords":s,"limit":lim, "format":"jpg"}   #creating list of arguments
 paths = response.download(arguments)   #passing the arguments to the function
 lst = paths[s]
 await bot.send_file(await bot.get_input_entity(e.chat_id), lst)
 end=round(time.time() * 1000)
 msstartend=int(end) - int(start)
 await e.edit("Done. Time taken: "+str(msstartend) + 's')
@bot.on(events.NewMessage(outgoing=True,pattern=r'.google (.*)'))
@bot.on(events.MessageEdited(outgoing=True,pattern=r'.google (.*)'))
async def gsearch(e):
        match = e.pattern_match.group(1)
        result_=subprocess.run(['gsearch', match], stdout=subprocess.PIPE)
        result=str(result_.stdout.decode())
        await bot.send_message(await bot.get_input_entity(e.chat_id), message='**Search Query:**\n`' + match + '`\n\n**Result:**\n' + result, reply_to=e.id, link_preview=False)
        if LOGGER:
           await bot.send_message(LOGGER_GROUP,"Google Search query "+match+" was executed successfully")
@bot.on(events.NewMessage(outgoing=True,pattern=r'.wiki (.*)'))
@bot.on(events.MessageEdited(outgoing=True,pattern=r'.wiki (.*)'))
async def wiki(e):
        match = e.pattern_match.group(1)
        result=wikipedia.summary(match)
        await bot.send_message(await bot.get_input_entity(e.chat_id), message='**Search:**\n`' + match + '`\n\n**Result:**\n' + result, reply_to=e.id, link_preview=False)
        if LOGGER:
           await bot.send_message(LOGGER_GROUP,"Wiki query "+match+" was executed successfully")
@bot.on(events.NewMessage(outgoing=True, pattern='^.ud (.*)'))
@bot.on(events.MessageEdited(outgoing=True, pattern='^.ud (.*)'))
async def ud(e):
  await e.edit("Processing...")
  str = e.pattern_match.group(1)
  mean = urbandict.define(str)
  if len(mean) >= 0:
    await e.edit('Text: **'+str+'**\n\nMeaning: **'+mean[0]['def']+'**\n\n'+'Example: \n__'+mean[0]['example']+'__')
    if LOGGER:
        await bot.send_message(LOGGER_GROUP,"ud query "+str+" executed successfully.")
  else:
    await e.edit("No result found for **"+str+"**")
@bot.on(events.NewMessage(outgoing=True,pattern='.imdb (.*)'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.imdb (.*)'))
async def imdb(e):
    movie_name = e.pattern_match.group(1)
    remove_space = movie_name.split(' ')
    final_name = '+'.join(remove_space)
    page = requests.get("https://www.imdb.com/find?ref_=nv_sr_fn&q="+final_name+"&s=all")
    lnk = str(page.status_code)
    soup = bs4.BeautifulSoup(page.content,'lxml')
    results = soup.findAll("td","result_text")
    mov_title = results[0].text
    mov_link = "http://www.imdb.com/"+results[0].a['href'] 
    page1 = requests.get(mov_link)
    soup = bs4.BeautifulSoup(page1.content,'lxml')
    story_line = soup.find('div', "inline canwrap")
    story_line = story_line.findAll("p")[0].text
    info = soup.findAll('div', "txt-block")
    for node in info:
      a = node.findAll('a')
      for i in a:
        if "country_of_origin" in i['href']:
          mov_country = i.string
    for node in info:
      a = node.findAll('a')
      for i in a:
        if "primary_language" in i['href']:
          mov_language = i.string
    rating = soup.findAll('div',"ratingValue")
    for r in rating:
      mov_rating = r.strong['title']
    await e.respond('**Title : **`'+mov_title+'`\n**Rating : **`'+mov_rating+'`\n**Country : **`'+mov_country+'`\n**Language : **`'+mov_language+'`\n**IMDB Url : **`'+mov_link+'`\n**Story Line : **`'+story_line+'`')



