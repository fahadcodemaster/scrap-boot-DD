import requests
# from requests_html import HTMLSession
import re
from bs4 import BeautifulSoup
#from autopost import run_post
import urllib.request
import os
from time import sleep
import time
from random import randint
from datetime import datetime

base_dir = os.path.dirname(os.path.realpath(__file__))

import json
import pickle
Debug =  False



def label_finder(doc_to_search , label_text):

    try:
        select_part = doc_to_search.find('label',string=label_text)
        selected_string = select_part.parent.find("span").get_text().strip()
        return selected_string
    except Exception as e:

        return False


def write_log(log_message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{current_time}] #Scarper# {str(log_message)}"
        
    log_file = "ErrorLog.log"
    with open(base_dir+"/"+ log_file, 'a') as file:
        file.write(formatted_message + '\n\n\n\n')


def scrape_url(url):
    

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Content-type':'application/json', 
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Connection' : 'keep-alive',
        'Host' : 'v3.torontomls.net',
        'Accept-Encoding':'gzip, deflate',
        'Upgrade-Insecure-Requests' : '1',
        'Cache-Control' : 'max-age=0'
        }
    
    


    r = requests.get(url,headers=headers)
    # with open("s_demo", 'wb') as file:
    #     pickle.dump(r, file)

    # filename = 's_demo'
    # with open(filename, 'rb') as file:
    #     r = pickle.load(file)


    html = r.text
    soup = BeautifulSoup(html, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    report_panel = soup.find('div',attrs={'class' : 'reports'})
    items = report_panel.find_all('div',attrs={'class' : 'link-item'})
    
    # r.html.render()
    i=0
    links = []
    for item in items:
        if(item.get('data-deferred-load')):
            links.append(item.get('data-deferred-load'))
        else:
            links.append(item.get('data-deferred-loaded'))

    results = []
    i = 0
    for link in links:
        try:
            r = requests.get(link,headers=headers)
            # with open("s_L_demo2", 'wb') as file:
            #     pickle.dump(r, file)

            # filename = 's_L_demo2'
            # with open(filename, 'rb') as file:
            #     r = pickle.load(file)




            html = r.text
            soup = BeautifulSoup(html, features="html.parser")

            for script in soup(["script", "style"]):
                script.extract()    # rip it out


            result = {}

            #full_doc
            full_doc = soup.find(attrs={'class' : 'formitem legacyBorder formgroup vertical'})


            #______________________________row_1______________________________

            #Images list
            image_list_url=[]
            images_html = full_doc.find("img")
            image_list_url.append(images_html["src"])

            if 'data-multi-photos' in images_html.attrs:
                # Check if the image variable has the multi_image class attribute
                data = json.loads(images_html['data-multi-photos'])
                for mp in range(len(data['multi-photos'])):
                    image_list_url.append(data['multi-photos'][mp].get('url'))


            # state
            state = full_doc.select(
                'div.formitem.form.viewform > div > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(2) > span:nth-child(3)')[
                0].get_text().strip()
            result["State"] = state
            print("state", state)

            #Address
            address = full_doc.select('div.formitem.form.viewform > div > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(1) > div > div > span:nth-child(1) > span')[0].get_text().strip()
            result["Address"] = address
            print(address)


            #City
            city = full_doc.select('div.formitem.form.viewform > div > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(2) > span:nth-child(1) > span')[0].get_text().strip()
            result["City"] = city

            # Neighborhood
            neighborhood = full_doc.select(
                'div.formitem.form.viewform > div > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(1) > span:nth-child(4)')[
                0].get_text().strip()
            result["Neighborhood"] = neighborhood
            print(neighborhood)


            print("HEREEE")
            #zip_code
            zip_code = full_doc.select('div.formitem.form.viewform > div > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(2) > span:nth-child(5) > span')[0].get_text().strip()
            result["Zip_code"] = zip_code

            #List:
            result['List'] = label_finder(full_doc , "List:")

            #For:
            result['For'] = label_finder(full_doc , "For:")

            #Bedrooms:
            result['Bedrooms'] = label_finder(full_doc , "Bedrooms:")

            #Washrooms:
            result['Washrooms'] = label_finder(full_doc , "Washrooms:")
            # type_style
            try:

                type_style = full_doc.select('div:nth-child(2) > div:nth-child(5) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > span')[0].get_text().strip()

            except IndexError:
                type_style = full_doc.select('div.formitem.form.viewform > div > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(4) > div.formitem.formgroup.horizontal > div:nth-child(1) > span:nth-child(1) > span')[0].get_text().strip()
            result["type_style"] = type_style


            #office
            office = full_doc.find('a', attrs={"class": "formlink value"}).get_text().strip()
            result['office'] = office

            #______________________________row_3______________________________

            #Heat:
            result['Heat'] = label_finder(full_doc , "Heat:")


            #AC
            result['A/C'] = label_finder(full_doc , "A/C:")

            #Heat
            result['Heat'] = label_finder(full_doc , "Heat:")


            #Exterior:
            result['Exterior'] = label_finder(full_doc , "Exterior:")


            #Bldg Amen
            result['Bldg Amen'] = label_finder(full_doc , "Bldg:")


            #Apx Sqft:
            result['Apx Sqft'] = label_finder(full_doc , "Apx:")


            #Gar/Gar Spcs:
            result['Gar/Gar Spcs'] = label_finder(full_doc , "Gar/Gar Pk Spcs:")
            if not result['Gar/Gar Spcs']:
                result['Gar/Gar Spcs'] = label_finder(full_doc, "Gar/Gar Spcs:")
            #______________________________row_3______________________________

            #Client Remks:
            result['Client Remks'] = label_finder(full_doc , "Client Remks:")

            #Extras:
            result['Extras'] = label_finder(full_doc , "Extras:")





            result['Extras item'] = []
            if result['Extras'] :
                Extras_item = result['Extras']
                Extras_item =  Extras_item.split(" ")
                Extras_item = [x.lower().strip() for x in Extras_item]
                result['Extras item'] = Extras_item

            if result['A/C']:
                for x in result['A/C'].split("/"):
                    result['Extras item'].append(x.lower().strip())

            if result['Heat']:
                for x in result['Heat'].split("/"):
                    result['Extras item'].append(x.lower().strip())






            #Exterior:
            if result['Exterior']:
                result['Extras item'].append(label_finder(full_doc , "Exterior:").strip().lower())





            for key , val in result.items():
                if type(val) == str:
                    result[key] = val.strip().lower()





            dir_name = base_dir + '/listings/' + result['Address']

            if(not os.path.exists(dir_name)):
                os.makedirs(dir_name)

            os.makedirs(os.path.join(base_dir,dir_name),exist_ok=True)


            image_list_file = []
            if Debug == False:

                for image in image_list_url:
                    image:str

                    image_file_name =str(time.time_ns()) + ".jpg"
                    image_file_name = image_file_name
                    image_file_path = os.path.join(base_dir,dir_name + '/' + image_file_name)
                    image_list_file.append(image_file_path)

                    if not os.path.exists(image_file_path):
                        print("Try Download Image:"+ result['Address'] +" -->  "+ image_file_name)

                        try:
                            response = requests.get(image,timeout=300)
                            with open(image_file_path , 'wb') as f:
                                f.write(response.content)
                        except Exception as e:
                            write_log("error in downloader image : " + str(e))
                            print (e)


            result["images"] = image_list_file


            result["__dir"] = dir_name
            result["__posted"] = False
            with open(dir_name  + "/info", 'wb') as file:
                pickle.dump(result, file)




            results.append(result)
            print('success : ' + result['Address'])
            i +=1
        except Exception as e:
            print('fail')
            print(e)
            write_log("error main while : " + str(e))

        sleep(randint(1,2))
        
    
    return results , i , len(results) - i





# result , s, f = scrape_url("http://v3.torontomls.net/Live/Pages/Public/Link.aspx?Key=1955ff40866640f6a7e1acfd365d666e&App=TREB")







    
