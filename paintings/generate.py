import json
import os
import shutil
import sys


def read_json(path: str) -> dict:
    # get file pointer
    try:
        with open(path) as file:
            loaded = json.load(file)
    except json.JSONDecodeError as err:
        print("ERR: JSON parsing error in file", path, "\n\t", err)
        return
    except:
        print("ERR: Unable to decode JSON from file", path)
        return
    # validate extracted json
    if type(loaded) != dict:
        print("ERR: Expected a dictionary from JSON file but loaded a", type(loaded))
        return
    return loaded


def read_template(file_path: str) -> str | None:
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except:
        print("ERR: Unable to read content from template", file_path)
        return


def fill_template(template: str, data: dict) -> str | None:
    out = template
    for key in data:
        key_cap = key.upper()
        out = out.replace(key_cap, data[key])
    return out


def write_file(dest_path: str, content: str) -> bool:
    try:
        with open(dest_path, 'w') as file:
            file.write(content)
    except:
        print("ERR: Unable to create/write to", dest_path)
        return False
    return True


def handle_file(dest_dir: str) -> bool:
    json_path = dest_dir + "/info.json"
    output_path = dest_dir + "/details.html"
    if len(sys.argv) == 3:
        template_path = sys.argv[2]
    else:
        template_path = "./TEMPLATE.html"
    
    info = read_json(json_path)
    if not info: return False
    
    template_text = read_template(template_path)
    if not template_text: return False
    
    template_filled = fill_template(template_text, info)
    if not template_filled: return False
    
    if not write_file(output_path, template_filled): return False
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3 or type(sys.argv[1]) != str:
        print("\nusage:  generate destination_path[,destination2,destination3,...] [template_path]\n")
        print("   destination_path(s)  Path to directory containing an info.json file")
        print("   template_path        Path to the template.html file (default: ./TEMPLATE.html)\n")
        exit(0)
    # process argv
    directories = sys.argv[1].split(',')
    # process each item in list
    for directory in directories:
        if handle_file(directory):
            print("Successfully wrote to", directory)
        else:
            print("Did not complete processing", directory)
    exit(0)
