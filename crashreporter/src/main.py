import datetime
import hashlib
import logging
import pytz
import re
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from webexteamssdk import WebexTeamsAPI
import requests
# WEBEX_BOT_TOKEN = "ZmFlNDY1YTMtOTc5ZS00NDc3LWJmMzEtMTdhZTRhMTA3ZjI5NGU2MThkMDktNzU1_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
WEBEX_BOT_TOKEN = "OTYxZWNmMmMtMDZjNy00OWRiLTgwMzQtMWUwOGMzY2Y2MzQyNzAxOWJlYzUtYmY1"
india_timezone = pytz.timezone('Asia/Kolkata')
api = WebexTeamsAPI(access_token=WEBEX_BOT_TOKEN)
# Declaring empty list and later adding only links with private or cec id builder
private_or_cec_links = []
# Declaring empty list and later adding only links with build as builder
links_as_build = []
annotated_list_of_links = []
unannotated_list_of_links = []
unannotated_list = []
annotated_table = PrettyTable()
annotated_table.field_names = ["Submitted (Date,time)","Who(cec id)","Text","Crash id"]
unannotated_table = PrettyTable()
unannotated_table.field_names = ["Time","Build","Program","Occurence"]
private_builds_table = PrettyTable()
private_builds_table.field_names = ["Submitted","Unitname(IP)"]
#Declaring required variables
annotated = 0
unannotated = 0
build_count = 0
s = 0
private_build_count = 0
recent_signatures_url = "https://cc-reports.cisco.com/acr/signatures/recent"
For_triage_guidelines = "https://confluence-eng-gpk1.cisco.com/conf/pages/viewpage.action?spaceKey=EXP&title=Step+by+step+guide+to+ACRs#StepbystepguidetoACRs-Contactsforlogs"
cc_reports_host = 'cc-reports.cisco.com'
# room_id = "849790a0-3b2e-11e8-a360-59378cd31b23"
room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vNDlkNTVjYTAtNjk5NC0xMWVlLTlmMDAtODViMDM2ZTRkZTVk"
# room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vYmIwZDIyNzAtZTc1NS0xMWVkLThmMWItMjcyODI3ZGMwOWJm"
length_of_end_list = 0
# Specify the path to the external text file
file_path = "file.txt"
def sending_message_to_user():
    if private_build_count == 1 and build_count == 0:
        sending_private_builds_table()
    elif private_build_count == 0 and build_count == 1:
        if annotated == 1 and unannotated == 0:
            sending_only_anno_table()
        elif annotated == 0 and unannotated == 1:
            sending_only_unanno_table()    
        elif annotated == 1 and unannotated == 1:
            sending_anno_table()
            sending_only_unanno_table()
    elif private_build_count == 1 and build_count == 1:
        if annotated == 1 and unannotated == 0:
            sending_anno_table()
            sending_private_builds_table()
        elif annotated == 0 and unannotated == 1:
            sending_unnanno_table()
            sending_private_builds_table()
        elif annotated == 1 and unannotated == 1:
            sending_anno_table()
            sending_unnanno_table()
            sending_private_builds_table()
def sending_only_unanno_table():
    try:
        current_time = datetime.datetime.now(india_timezone)
        three_hours_ago = current_time - datetime.timedelta(hours=3)
        formatted_current_time = current_time.strftime("%I:%M %p")
        formatted_three_hours_ago = three_hours_ago.strftime("%I:%M %p")
        res = "Unannotated crashes table %s - %s " % (formatted_three_hours_ago,formatted_current_time)

        #!!!!!!To output list of links as hyperlinks into the webex platform !!!!!
        # !!!!!!response_text_1 = "\n".join([f"- [{new['date submitted']}] [{new['name']}]({new['url']})" for new in newlist])!!!!!1
        result_table_for_unannotated = "```%s```" % str(unannotated_table)
        api.messages.create(roomId=room_id,text = res)
        api.messages.create(roomId=room_id,markdown=result_table_for_unannotated)
        final_msg()
    except Exception as e:
        # Log the exception as an error
        logging.error("Error: %s" % str(e))
    finally:
        unannotated_list_of_links.clear()
        # Clear the rows of the table
        unannotated_table.clear_rows()
def sending_only_anno_table():
    try:
        current_time = datetime.datetime.now(india_timezone)
        three_hours_ago = current_time - datetime.timedelta(hours=3)
        formatted_current_time = current_time.strftime("%I:%M %p")
        formatted_three_hours_ago = three_hours_ago.strftime("%I:%M %p")
        result_table_for_annotated = "```%s```" % str(annotated_table)
        res = "Annotated crashes  table  %s - %s" % (formatted_three_hours_ago,formatted_current_time)
        # Define the message text with a hyperlink
        api.messages.create(roomId=room_id,text = res)
        api.messages.create(roomId=room_id,markdown=result_table_for_annotated)
        final_msg()
    except Exception as e:
        # Log the exception as an error
        logging.error("Error: %s" % str(e))
    finally:
        annotated_table.clear_rows()
        annotated_list_of_links.clear()
def final_msg():

    signatures_url_as_link = "Click [here](%s) to refer recent signatures." % recent_signatures_url
    triage_as_link = "Click [here](%s) to refer for triage guidelines." % For_triage_guidelines
    api.messages.create(roomId=room_id,markdown=signatures_url_as_link)
    api.messages.create(roomId=room_id,markdown=triage_as_link)
#Returning to the webex user all the 
def sending_anno_table():
    try:
        current_time = datetime.datetime.now(india_timezone)
        three_hours_ago = current_time - datetime.timedelta(hours=3)
        formatted_current_time = current_time.strftime("%I:%M %p")
        formatted_three_hours_ago = three_hours_ago.strftime("%I:%M %p")
        result_table_for_annotated = "```%s```" % str(annotated_table)
        res = "Annotated crashes table %s and %s" % (formatted_three_hours_ago, formatted_current_time)

        # result_table_for_annotated = f'````{(str(annotated_table))}````'
        # res = f"Annotated crashes table between {formatted_three_hours_ago} and {formatted_current_time}"
        # Define the message text with a hyperlink
        api.messages.create(roomId=room_id,text = res)
        api.messages.create(roomId=room_id,markdown=result_table_for_annotated)
    except Exception as e:
        # Log the exception as an error
        logging.error("Error: %s" % str(e))
    finally:
        annotated_list_of_links.clear()
        annotated_table.clear_rows()
def sending_unnanno_table():
    try:
        current_time = datetime.datetime.now(india_timezone)
        three_hours_ago = current_time - datetime.timedelta(hours=3)
        formatted_current_time = current_time.strftime("%I:%M %p")
        formatted_three_hours_ago = three_hours_ago.strftime("%I:%M %p")
        
        
        result_table_for_unannotated = "```%s```" % str(unannotated_table)
        res = "Unannotated crashes table %s - %s" % (formatted_three_hours_ago, formatted_current_time)
        #!!!!!!To output list of links as hyperlinks into the webex platform !!!!!
        # !!!!!!response_text_1 = "\n".join([f"- [{new['date submitted']}] [{new['name']}]({new['url']})" for new in newlist])!!!!!1
        # Define the recent signatures and triage guidelines message text with a hyperlink
        api.messages.create(roomId=room_id,text = res)
        api.messages.create(roomId=room_id,markdown=result_table_for_unannotated)
    except Exception as e:
        # Log the exception as an error
        logging.error("Error: %s" % str(e))
    finally:
        unannotated_list_of_links.clear()
        # Clear the rows of the table
        unannotated_table.clear_rows()
def sending_private_builds_table():
    try:
        current_time = datetime.datetime.now(india_timezone)
        three_hours_ago = current_time - datetime.timedelta(hours=3)
        formatted_current_time = current_time.strftime("%I:%M %p")
        formatted_three_hours_ago = three_hours_ago.strftime("%I:%M %p")
        result_table_for_private_builds = "```%s```" % str(private_builds_table)
        res = "Private builds table %s - %s." % (formatted_three_hours_ago, formatted_current_time)
        # Define the message
        api.messages.create(roomId=room_id,markdown=res)
        api.messages.create(roomId=room_id,markdown=result_table_for_private_builds)
        final_msg()
    except Exception as e:
        # Log the exception as an error
        logging.error("Error: %s" % str(e))
    finally:
        private_or_cec_links.clear()
        private_builds_table.clear_rows()
#Funciton which checks whether the crashes are annotated or unannotated
def check_anno_or_unnanno(links_as_build):
    global annotated,unannotated
    for i in links_as_build:
        try:
            response_1 = requests.get(i)
            if response_1.status_code == 200:
                link_data = BeautifulSoup(response_1.content, 'html.parser')
                headings= link_data.find_all('h3')
                a = headings[0]
                b = headings[1]
                if a.text == 'Related Annotations' and a.find_next_sibling('table') and b.text == 'Related Reports':
                    annotated = 1
                    annotated_list_of_links.append(i)

                else:
                    unannotated_list_of_links.append(i)
                    new_i = re.sub(r'https://cc-reports.cisco.com', '', i)
                    unannotated_list.append(new_i)
                    unannotated = 1
        except Exception as e:
            # Log the exception as an error
            logging.error("Error: %s" % str(e))
    if annotated == 1 and unannotated == 1:
        try:
            table_for_annotated(annotated_list_of_links)
            table_for_unannotated(unannotated_list)
        except Exception as e:
            # Log the exception as an error
            logging.error("Error: %s" % str(e))
    elif annotated != 1 and unannotated == 1:
        try:
            table_for_unannotated(unannotated_list)
        except Exception as e:
            # Log the exception as an error
            logging.error("Error: %s" % str(e))
    elif annotated == 1 and unannotated != 1:
        try:
            table_for_annotated(annotated_list_of_links) 
        except Exception as e:
            # Log the exception as an error
            logging.error("Error: %s" % str(e))
def table_for_annotated(annotated_list_of_links):
    for i in annotated_list_of_links:
        try:
            response_1 = requests.get(i)
            if response_1.status_code == 200:
                link_data = BeautifulSoup(response_1.content, 'html.parser')
                headings= link_data.find_all('h3')
                a = headings[0]
                b = headings[1]
                if a.text == 'Related Annotations' and a.find_next_sibling('table') and b.text == 'Related Reports':
                    try:
                        match = re.search(r'\d+$', i)
                        if match:
                            last_number = int(match.group())
                        else:
                            logging.info("Doesn't match the condition")                        
                        row_0 = link_data.find_all('tr')[1]
                        var_1 = row_0.find_all('td')[0].get_text()
                        var_2 = row_0.find_all('td')[1].get_text()
                        var_3 = row_0.find_all('td')[2].get_text()
                        var_4 = last_number
                        if var_2 != "ACR":    
                            annotated_table.add_row([var_1,var_2,var_3,var_4])
                    except:
                            # Log the exception as an error
                            logging.error("Error: %s" % str(e))


        except Exception as e:
            # Log the exception as an error
            logging.error("Error: %s" % str(e))
def table_for_unannotated(unannotated_list):
    global unannotated
    for i in unannotated_list:
        if i not in private_or_cec_links:
            try:
                unannotated = 1
                response = requests.get(recent_signatures_url)
                if response.status_code == 200:
                    page_data = BeautifulSoup(response.content, 'html.parser')
                    # Find the first table element on the webpage
                    table = page_data.find('table')
                    # Check if a table was found
                    if table:
                        # Find all <a> (anchor) tags within the table
                        anchor_tags = table.find_all('a', href=i)
                        # Check if any matching <a> tag(s) were found
                        if anchor_tags:
                            for tag in anchor_tags:
                            # Find the parent <tr> element of the matching <a> tag
                                row = tag.find_parent('tr')
                                if row:
                                    # Find all <td> tags within the row
                                    td_tags = row.find_all('td')
                                    time = td_tags[0].get_text(strip=True)
                                    build = td_tags[2].get_text(strip=True)
                                    program = td_tags[4].get_text(strip=True)
                                    occurence = td_tags[7].get_text(strip=True)
                                    unannotated_table.add_row([time,build,program,occurence])
                                    break           
                        else:
                            logging.info("No <a> tags found in the table.")
                    else:
                        logging.info("No table found on the webpage.")
                else:
                    logging.info("Failed to retrieve the webpage.")
            except:
                logging.info("Exception occured")
def table_for_private_builds(private_builds_links):
    for i in private_builds_links:
        try:
            response_1 = requests.get(i)
            if response_1.status_code == 200:
                link_data = BeautifulSoup(response_1.content, 'html.parser')
                headings= link_data.find_all('h3')
                a = headings[0]
                b = headings[1]
                
                table_2 = b.find_next_sibling('table')
                row_0 = table_2.find_all('tr')[1]
                var_1 = row_0.find_all('td')[0].get_text()
                var_2 = row_0.find_all('td')[2].get_text()
                private_builds_table.add_row([var_1,var_2])
        except Exception as e:
            # Log the exception as an error
            logging.error("Error: %s" % str(e))
def is_substring_in_array(substring, string_array):
    for string in string_array:
        if substring in string:
            return True
    return False
def process_func():
    global private_build_count,build_count,links_as_build,private_or_cec_links
    try:
        response = requests.get(recent_signatures_url)
        if response.status_code == 200:
            page_data = BeautifulSoup(response.content, 'html.parser')
            all_tr_elements = page_data.find_all('tr')
            #To get crashes which are appeared today only
            text = "Today"
            target_tr = None
            for tr_element in all_tr_elements:
                td_elements = tr_element.find_all('td')
                for td_element in td_elements:
                    if text in td_element.get_text():
                        target_tr = tr_element
                        if len(td_element) > 0:
                            #To get the tag associated with build/private_build/cec - id
                            td_ele = target_tr.find_all('td')
                            #To get tag associated with href value 
                            a_element = td_ele[0].find('a')
                            build = "build"
                            #Getting build/private_build/cec - id to compare 
                            builder = td_ele[3].get_text().strip()
                            if builder == build:
                                #Getting the href value using the tag we got earlier
                                href_value = a_element['href']
                                link = 'https://' + cc_reports_host + href_value 
                                #Checking if it is already present in thcde file
                                with open(file_path, "r+") as file2:
                                    lines = file2.readlines()
                                    if not is_substring_in_array(link, lines):
                                            file2.write(link)
                                            links_as_build.append(link)
                                            build_count = 1
                            else:
                                href_value = a_element['href']
                                link = 'https://' + cc_reports_host + href_value 
                                #Checking if it is already present in the day_end list
                                with open(file_path, "r+") as file2:
                                   lines = file2.readlines()
                                   if not is_substring_in_array(link, lines):
                                            file2.write(link)
                                            private_or_cec_links.append(link)
                                            private_build_count = 1
    except Exception as e:
        # Log the exception as an error
        logging.error("Error: %s" % str(e))

    if private_build_count == 1 and build_count == 1:
        check_anno_or_unnanno(links_as_build)
        table_for_private_builds(private_or_cec_links)
        sending_message_to_user()
    elif private_build_count == 0 and build_count == 1:
        check_anno_or_unnanno(links_as_build)
        sending_message_to_user()
    elif private_build_count == 1 and build_count == 0:
        table_for_private_builds(private_or_cec_links)
        sending_message_to_user()
#Function to calculate hash 
def calculate_hash(content):
    try:
    # Calculate an SHA-256 hash of the content
        sha256 = hashlib.sha256()
        sha256.update(content.encode('utf-8'))
        return sha256.hexdigest()
    except Exception as e:
        # Log the exception as an error
        logging.error("Error: %s" % str(e))

#Function to compare current hash and previous hash so that we will know whether the webpage is changed or no 
def perform_action():
    previous_hash = None
    try :
        response = requests.get(recent_signatures_url)
        if response.status_code == 200:
            current_content = response.text
            #Calculate hash function
            current_hash = calculate_hash(current_content)
            if current_hash != previous_hash:
                #Whenever there is difference in the previous hash and current hash, process function gets called to execute if there are any crashes present
                process_func()
                previous_hash = current_hash
            else:
                logging.info("There webpage hash value isn't changed, so there are no new crashes")
    except requests.exceptions.RequestException as e:
        # Log the exception as an error
        logging.error("Error: %s" % str(e))
"""To schedule the bot to run every 3 hours
schedule.every(180).minutes.do(perform_action)
"""
perform_action()
    # time.sleep(1)  # Sleep for 1 second to avoid high CPU usage