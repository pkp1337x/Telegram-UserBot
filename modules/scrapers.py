import requests
import bs4 
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
    odds = soup.findAll("tr","odd")
    mov_title = odds[0].findNext('td').findNext('td').text
    mov_link = "http://www.imdb.com/"+odds[0].findNext('td').findNext('td').a['href'] 
    page1 = requests.get(mov_link)
    soup = bs4.BeautifulSoup(page1.content,'lxml')
    if soup.find('div','poster'):
    	poster = soup.find('div','poster').img['src']
    else:
    	poster = ''
    if soup.find('div','title_wrapper'):
    	pg = soup.find('div','title_wrapper').findNext('div').text
    	mov_details = re.sub(r'\s+',' ',pg)
    else:
    	mov_details = ''
    credits = soup.findAll('div', 'credit_summary_item')
    if len(credits)==1:
    	director = credits[0].a.text
    	writer = 'Not available'
    	stars = 'Not available'
    elif len(credits)>2:
    	director = credits[0].a.text
    	writer = credits[1].a.text
    	actors = []
    	for x in credits[2].findAll('a'):
    		actors.append(x.text)
    	actors.pop()
    	stars = actors[0]+','+actors[1]+','+actors[2]
    else:
    	director = credits[0].a.text
    	writer = 'Not available'
    	actors = []
    	for x in credits[1].findAll('a'):
    		actors.append(x.text)
    	actors.pop()
    	stars = actors[0]+','+actors[1]+','+actors[2]	 
    if soup.find('div', "inline canwrap"):
    	story_line = soup.find('div', "inline canwrap").findAll('p')[0].text
    else:
    	story_line = 'Not available'
    info = soup.findAll('div', "txt-block")
    if info:
    	mov_country = []
    	mov_language = []
    	for node in info:
    		a = node.findAll('a')
    		for i in a:
    			if "country_of_origin" in i['href']:
    				mov_country.append(i.text)
    			elif "primary_language" in i['href']:
    				mov_language.append(i.text) 
    if soup.findAll('div',"ratingValue"):
    	for r in soup.findAll('div',"ratingValue"):
    		mov_rating = r.strong['title']
    else:
    	mov_rating = 'Not available'
    await e.edit('<a href='+poster+'>&nbsp;</a>\n'
    			'<b>Title : </b><code>'+mov_title+
    			'</code>\n<code>'+mov_details+
    			'</code>\n<b>Rating : </b><code>'+mov_rating+
    			'</code>\n<b>Country : </b><code>'+mov_country[0]+
    			'</code>\n<b>Language : </b><code>'+mov_language[0]+
    			'</code>\n<b>Director : </b><code>'+director+
    			'</code>\n<b>Writer : </b><code>'+writer+
    			'</code>\n<b>Stars : </b><code>'+stars+
    			'</code>\n<b>IMDB Url : </b>'+mov_link+
    			'\n<b>Story Line : </b>'+story_line,
    			link_preview = True , parse_mode = 'HTML'
    			)
@bot.on(events.NewMessage(outgoing=True,pattern='.ly (.*)'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.ly (.*)'))
async def ly(e):
    name = e.pattern_match.group(1)
    splitting = name.split(' ')
    final = '+'.join(splitting)
    page = requests.get("https://www.malayalachalachithram.com/search.php?q="+final)
    soup = bs4.BeautifulSoup(page.content,'lxml')
    results = soup.findAll("table","mdetails")
    if results[0].a:
      page = requests.get("https://www.malayalachalachithram.com/"+results[0].a['href'])
      soup = bs4.BeautifulSoup(page.content,'lxml')
      table = soup.find(id="tbllyrics") 
      if table.findNext("td").findNext("td"):
        lyrics_mal = table.findNext("td").findNext("td")
        lyrics_eng = table.findNext("td")
        lyrics_final = lyrics_mal.text+'\n\n'+lyrics_eng.text  
      else:
        lyrics_final = table.findNext("td").text
      table = soup.find("table","mdetails")
      movie_name = table.findNext("td").findNext("a")     
      await e.edit('**Song : **`'+results[0].a.text+'`\n**Movie : **`'+movie_name.text+'`\n**Lyrics : **`'+lyrics_final+'`')
    else:
      await e.edit('No results') 


