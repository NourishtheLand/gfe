#!/usr/bin/env python3
import json
import http.client

user_id = input("Enter your user id: ")

while user_id == "":
   user_id = input("Enter your user id: ")

def fetch_json():
    host = "gelbooru.com"
    endpoint = f"/index.php?page=dapi&s=post&q=index&json=1&tags=fav:{user_id}"

    conn = http.client.HTTPSConnection(host)

    conn.request("GET", endpoint)

    response = conn.getresponse()

    if response.status != 200:
        print("There was an error retrieving favorites.")
        print("Make sure it is the correct user id.")
        exit(1)

    res_data = response.read().decode()

    conn.close()

    return json.loads(res_data)

def get_file_type(url):
    if ".jpg" or ".jpeg" in url:
        return "jpg"
    elif ".png" in url:
        return "png"
    elif ".gif" in url:
        return "gif"
    elif ".mp4" in url:
        return "mp4"
    else:
        return ""

data = fetch_json()

# New dictionary to properly sort for anime boxes client
favorites = []

for current_post in data['post']:
    # Start of it
    formatted_dict = {
        "source": current_post['source'],
        "has_children": current_post['has_children'],
    }

    # Setting up dictionaries to be merged
    preview = {
        "height": current_post['preview_height'],
        "ext": get_file_type(current_post['preview_url']),
        "contentType": 1,
        "url": current_post['preview_url'],
        "width": current_post['preview_width']
    }
    file = {
        "height": current_post['height'],
        "ext": get_file_type(current_post['file_url']),
        "contentType": 1,
        "url": current_post['file_url'],
        "width": current_post['width']
    }
    sample = {
        "height": current_post['sample_height'],
        "ext": get_file_type(current_post['sample_url']),
        "contentType": 1,
        "url": current_post['sample_url'],
        "width": current_post['sample_width']
    }

    filetype = "jpeg" if get_file_type(current_post['file_url']) == 'jpg' else get_file_type(current_post['file_url'])

    filetype_dict = {
        "height": current_post['sample_height'],
        "ext": get_file_type(current_post['sample_url']),
        "contentType": 1,
        "url": current_post['sample_url'],
        "width": current_post['sample_width']
    }


    formatted_dict['preview'] = preview
    formatted_dict['tags'] = current_post['tags']
    formatted_dict['file'] = file
    formatted_dict['has_notes'] = current_post['has_notes']
    formatted_dict['parent_id'] = current_post['parent_id']
    formatted_dict['score'] = current_post['score']
    formatted_dict['enforceOriginalImage'] = False
    formatted_dict['isVisible'] = True
    formatted_dict['has_comments'] = current_post['has_comments']
    formatted_dict['metadataReloaded'] = False
    formatted_dict['sample'] = sample
    formatted_dict['ppostId'] = current_post['id']
    # Obviously so
    formatted_dict['isFavorite'] = True
    formatted_dict['md5'] = current_post['md5']
    formatted_dict['disableStorage'] = False
    formatted_dict[f"{filetype}"] = filetype_dict
    formatted_dict['upload'] = "true"
    formatted_dict['ppostUrl'] = f"http://gelbooru.com/index.php?page=post&s=view&id={current_post['id']}"
    formatted_dict['dateAdded'] = current_post['created_at']
    formatted_dict['rating'] = current_post['rating']

    favorites.append(formatted_dict)

with open('favorites.json', 'w') as json_file:
    json.dump(favorites, json_file, indent=2)

print("Favorites have been successfully extracted.")
print('Copy all the contents in the "favorites.json" file and paste it inside the "favorites" section of the "{date you exported}.abbj" file.')
exit(0)
