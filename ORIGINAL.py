import os
import pathlib
import subprocess
import shutil
import json
import argparse
import json
import re
import pprint

pp = pprint.PrettyPrinter(indent=4)
parser = argparse.ArgumentParser(
                    prog='Sexlab Catalytic Converter',
                    description='Converts SLAL anims to SLSB automagically')

parser.add_argument('slsb', help='path to your slsb executable')
parser.add_argument('working', help='path to your working directory; should be structured as {<working_dir>/<slal_pack>/SLAnims/json/}')
parser.add_argument('-a', '--author', help='name of the author of the pack', default="Unknown")
parser.add_argument('-c', '--clean', help='clean up temp dir after conversion', action='store_true')
parser.add_argument('-s', '--skyrim', help='path to your skyrim directory', default=None)
parser.add_argument('-slt', '--slate', help='path to the directory containig SLATE_ActionLog jsons', default=None) 
parser.add_argument('-ra', '--remove_anims', help='remove copied animations during fnis behaviour gen', action='store_true')
parser.add_argument('-nb', '--no_build', help='do not build the slsb project', action='store_true')

args = parser.parse_args()
slsb_path = args.slsb
skyrim_path = args.skyrim
slate_path = args.slate
fnis_path = skyrim_path + '/Data/tools/GenerateFNIS_for_Modders' if skyrim_path is not None else None
remove_anims = args.remove_anims
parent_dir = args.working

if os.path.exists(parent_dir + "\\conversion"):
    shutil.rmtree(parent_dir + "\\conversion")

def convert(parent_dir, dir):
    working_dir = os.path.join(parent_dir, dir)
    
    slal_dir = working_dir + "\\SLAnims\\json"
    anim_source_dir = working_dir + "\\SLAnims\\source"
    out_dir = parent_dir + "\\conversion\\" + dir
    tmp_dir = './tmp'

    if not os.path.exists(slal_dir):
        return

    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    os.makedirs(tmp_dir + '/edited')
    os.makedirs(out_dir + '/SKSE/Sexlab/Registry/Source')

    dom_kwds = ['rough', 'bound', 'dominant', 'defeated', 'conquering', 'humiliation', 'domsub', 'femdom', 'femaledomination', 'maledom', 'lezdom', 'gaydom', 'bdsm']
    uses_only_agg_tag = ['leito', 'kom', 'flufyfox', 'gs', 'cobalt', 'mastermike', 'nya', 'rydin', 'nibbles', 'anubs']
    unconscious_kwds = ['necro', 'guro', 'gore', 'dead']
    futa_kwds = ['futa', 'futanari', 'futaxfemale']
    leadin_kwds = ['kissing', 'hugging', 'holding', 'loving', 'foreplay', 'lying', 'kneeling', 'cuddle', 'sfw', 'romance']
    not_leadin_kwds = ['vaginal', 'anal', 'oral', 'blowjob', 'cunnilingus', 'forced', 'sex', 'masturbation']
    magic_kwds = ['mage', 'staff', 'alteration', 'rune', 'magicdildo', 'magick']
    furni_kwds = [
        'alchemywb', 'bed', 'bench', 'cage', 'chair', 'coffin', 'counter', 'couch', 'desk',
        'doublebed', 'doublebeds', 'drawer', 'dwemerchair', 'enchantingwb', 'furn', 'furotub',
        'gallows', 'haybale', 'javtable', 'lowtable', 'necrochair', 'pillory', 'pillorylow',
        'pole', 'rpost', 'shack', 'sofa', 'spike', 'table', 'throne', 'torturerack', 'tub',
        'wall', 'wheel', 'woodenpony', 'workbench', 'xcross'
    ]
    allowed_furnitures = {
        'beds': ['BedDouble', 'BedSingle', 'BedRoll'],
        'benches': ['Bench', 'BenchNoble'],
        'chairs': ['Chair', 'ChairArm', 'ChairBar', 'ChairWing', 'ChairNoble'],
        'contraptions': ['XCross', 'Pillory'],
        'crafting': ['CraftCookingPot', 'CraftAlchemy', 'CraftEnchanting', 'CraftSmithing', 'CraftWorkbench'],
        'tables': ['Table', 'TableCounter'],
        'thrones': ['Throne', 'ThroneRiften', 'ThroneNordic'],
        'walls': ['Wall', 'Railing']
    }
    acyclic_stages = ['leito_f_solo_toy_re_cow_anal_a1_s1', 'babo_zazpillory01_a1_s1', 'babo_zazpillory01_a1_s1e', 'babo_zazpillory01_a1_s5', 'babo_zazpillory01_a1_s5e', 'extrapocketpullin', 'extrapocketpullout', 'dd_zaparmbkissing01_a1_s1', 'dd_zaparmbkissing01_a1_s3', 'dd_zapyokekissing01_a1_s1', 'dd_zapyokekissing01_a1_s3', 'dd_zapkissing01_a1_s1', 'dd_zapkissing01_a1_s3', 'dd_zapkissing01_a2_s1', 'dd_zapkissing01_a2_s3']

    print("---------> PARSING SLAL JSON AND SOURCE")
    #------------------------- SLAL JSON PARSER -------------------------#
    slal_json_data = {}
    def parse_slal_json(file):
        json_array = json.load(file)
        for json_object in json_array:

            for scene_data in json_array["animations"]:
                scene_info = {
                    "scene_name": scene_data["name"],
                    "scene_id": scene_data["id"],
                    "scene_tags": scene_data["tags"].split(","),
                    "scene_sound": scene_data["sound"],
                    "actors": {},
                    "stage_params": {}
                }
                
                for key, actor_data in enumerate(scene_data["actors"], 1):
                    actor_key = f"a{key}"
                    
                    actor_info = {
                        "actor_key": actor_key,
                        "gender": actor_data["type"],
                        "add_cum": actor_data.get("add_cum", 0),
                        f"{actor_key}_stage_params": {}
                    }
                    
                    for idx, actor_stage_data in enumerate(actor_data["stages"], 1):
                        actor_stage_params_key = f"Stage {idx}"
                       
                        actor_stage_params_info = {
                            "actor_stage_params_key": actor_stage_params_key,
                            "stage_id": actor_stage_data["id"],
                            "open_mouth": actor_stage_data.get("open_mouth", "False"),
                            "strap_on": actor_stage_data.get("strap_on", "False"),
                            "silent": actor_stage_data.get("silent", "False"),
                            "sos": actor_stage_data.get("sos", 0),
                            "up": actor_stage_data.get("up", 0),
                            "side": actor_stage_data.get("side", 0),
                            "rotate": actor_stage_data.get("rotate", 0),
                            "forward": actor_stage_data.get("forward", 0)
                        }
                        
                        actor_info[f"{actor_key}_stage_params"][actor_stage_params_key] = actor_stage_params_info
                    
                    scene_info["actors"][actor_key] = actor_info
                
                for scene_stage_data in scene_data.get("stages", []):
                    stage_params_key = f"Stage {scene_stage_data.get('number', 'None')}"
                    
                    scene_stage_params_info = {
                        "stage_params_key": stage_params_key,
                        "sound": scene_stage_data.get("sound", "None"),
                        "timer": scene_stage_data.get("timer", 0)
                    }
                    scene_info["stage_params"][stage_params_key] = scene_stage_params_info
                
                slal_json_data[scene_info["scene_name"]] = scene_info
                
        return slal_json_data
     
    #------------------------- SOURCE TXT PARSER -------------------------#
    animations = dict()
    def reset_source_animation():
        return {
            "id": None,
            "name": None,
            "actors": {},
        }
    source_metadata = {
        "anim_name_prefix": None,
    }
    source_file_data = []
    def parse_source_type(file):
        current_animation = None
        inside_animation = False
        
        for line in file:
            line = line.strip()
            
            if re.match(r'^\s*anim_name_prefix\("([^"]*)"\)', line):
                source_metadata["anim_name_prefix"] = re.search(r'anim_name_prefix\("([^"]*)"\)', line).group(1)
            if re.match(r'^\s*Animation\(', line):
                if current_animation:
                    animations[source_metadata["anim_name_prefix"] + current_animation["name"]] = current_animation
                    
                current_animation = reset_source_animation()
                inside_animation = True
                current_actor_number = None
                
            elif inside_animation and re.match(r'^\s*\)', line):
                inside_animation = False
                
            elif inside_animation:
                if re.match(r'^\s*id=', line):
                    current_animation["id"] = re.search(r'id="([^"]*)"', line).group(1)
                elif re.match(r'^\s*name=', line):
                    current_animation["name"] = re.search(r'name="([^"]*)"', line).group(1)
                    
                elif actor_match := re.search(r'actor\s*(\d+)\s*=\s*([^()]+)\(([^)]*)\)', line):
                    current_actor_number = actor_match.group(1)
                    current_actor_gender = actor_match.group(2)
                    
                    if current_actor_gender:
                        source_file_data.append({
                            "scene_name": current_animation['name'],
                            "actor_number": current_actor_number,
                            "gender_type": current_actor_gender
                        })
                        
        if current_animation:
            if source_metadata["anim_name_prefix"] in animations:
                animations[source_metadata["anim_name_prefix"] + current_animation["name"]] = current_animation
            else:
                current_animation["name"] = current_animation
        
        return source_file_data
  
  
    print("---------> CONVERTING SLAL TO SLSB PROJECTS")
    if os.path.exists(anim_source_dir):
        for filename in os.listdir(anim_source_dir):
            path = os.path.join(anim_source_dir, filename)
            ext = pathlib.Path(filename).suffix
            if os.path.isfile(path) and ext == ".txt":
                with open(path, "r") as file:
                    parse_source_type(file)

    json_files = [json_file for json_file in os.listdir(slal_dir) if json_file.lower().endswith(".json")]
    json_count = len(json_files)
    anim_dir_name = None
    
    for filename in os.listdir(slal_dir):
        path = os.path.join(slal_dir, filename)
        ext = pathlib.Path(filename).suffix
        if os.path.isfile(path) and filename.lower().endswith(".json"):
            with open(path, "r") as file:
                parse_slal_json(file)
                
            json_base_name = pathlib.Path(filename).stem
            matching_source_path = None
            if os.path.exists(anim_source_dir):
                for source_file in os.listdir(anim_source_dir):
                    if source_file.lower().endswith(".txt") and pathlib.Path(source_file).stem.lower() == json_base_name.lower():
                        matching_source_path = os.path.join(anim_source_dir, source_file)
                        break
                if matching_source_path is not None:
                    with open(matching_source_path, 'r') as txt_file:
                        for line in txt_file:
                            if match := re.match(r'anim_dir\("([^"]*)"\)', line):
                                anim_dir_name = match.group(1)
                                break
            else:
                anim_dir_path = working_dir + "\\meshes\\actors\\character\\animations"
                if os.path.exists(anim_dir_path):
                    for dir_name in os.listdir(anim_dir_path):
                        if json_count == 1:
                            anim_dir_name = dir_name
                        else:
                            anim_dir_name = json_base_name
            
            changes_made = False
            if anim_dir_name is not None:
                with open(path, 'r+') as json_file:
                    #fixes directory names
                    json_data = json.load(json_file)
                    if "name" in json_data and json_data["name"].lower() != anim_dir_name.lower():
                        json_data["name"] = anim_dir_name
                        changes_made = True
                    #fixes type-type gender
                    if "animations" in json_data:
                        for scene_data in json_data["animations"]:
                            for key, actor_data in enumerate(scene_data["actors"], 1):
                                actor_key = f"a{key}"
                                if actor_data["type"].lower() == "type" and os.path.exists(anim_source_dir):
                                    slal_type_scene = scene_data["name"]
                                    slal_actor_key = actor_key
                                    for info in source_file_data:
                                        if source_metadata['anim_name_prefix'] and source_metadata['anim_name_prefix'] is not None:
                                            source_scene_name = source_metadata['anim_name_prefix'] + info['scene_name']
                                        else:
                                            source_scene_name = info['scene_name']
                                        source_actor_key = f"a{info['actor_number']}"
                                        if (slal_type_scene in source_scene_name) and (slal_actor_key in source_actor_key):
                                            actor_data["type"] = info['gender_type']
                                            changes_made = True
                    if changes_made:
                        json_file.seek(0)
                        json.dump(json_data, json_file, indent=2)
                        json_file.truncate()

            print('converting', filename)
            output = subprocess.Popen(f"{slsb_path} convert --in \"{path}\" --out \"{tmp_dir}\"", stdout=subprocess.PIPE).stdout.read()


    print("---------> PARSING FNIS LISTS")
    def parse_fnis_list(parent_dir, file):
        path = os.path.join(parent_dir, file)
        with open(path) as topo_file:
            last_seq = None
            for line in topo_file:
                line = line.strip()
                if len(line) > 0 and line[0] != "'":
                    splits = line.split()
                    if (len(splits)) == 0 or splits[0].lower() == 'version' or splits[0].lower() == 'ï»¿version':
                        continue

                    anim_file_name = None
                    anim_event_name = None
                    options = []
                    anim_objects = []

                    for i in range(len(splits)):
                        split = splits[i].lower()
                        if anim_event_name is not None:
                            anim_objects.append(split)
                        if '.hkx' in split:
                            anim_file_name = splits[i]
                            anim_event_name = splits[i - 1]
                        if '-' in split:
                            options.append(split)
                            
                    anim_event_name = anim_event_name.lower()
                    
                    if '-a,' in line or '-a ' in line or '-o,a,' in line or '-o,a ' in line:
                        last_seq = anim_event_name
                    
                    anim_path = os.path.join(parent_dir, anim_file_name)
                    out_path = os.path.normpath(anim_path)
                    out_path = out_path.split(os.sep)

                    for i in range(len(out_path) - 1, -1, -1):
                        if (out_path[i].lower() == 'meshes'):
                            out_path = out_path[i:]
                            break
                
                    out_path = os.path.join('', *out_path)
                    
                    data = {
                        'anim_file_name': anim_file_name,
                        'sequence': [],
                        'options': options,
                        'anim_obj': anim_objects,
                        'path': anim_path,
                        'out_path': out_path
                    }

                    if last_seq is None:
                        anim_data[anim_event_name] = data
                    else:
                        try:
                            anim_data[last_seq]['sequence'].append(data)    #don't know what this is supposed to do; the ['sequence'] is empty so always KeyError
                        except KeyError:
                            anim_data[last_seq] = data
                        last_seq = None

    anim_data = dict()

    def iter_fnis_lists(dir, func):
        anim_dir = os.path.join(dir, 'animations')
        if os.path.exists(anim_dir) and os.path.exists(os.path.join(dir, 'animations')):
            for filename in os.listdir(anim_dir):
                path = os.path.join(anim_dir, filename)
                if os.path.isdir(path):
                    for filename in os.listdir(path):
                        if filename.startswith('FNIS_') and filename.endswith('_List.txt'):
                            func(path, filename)
        else:
            for filename in os.listdir(dir):
                path = os.path.join(dir, filename)
                iter_fnis_lists(path, func)

    anim_dir = working_dir + '\\meshes\\actors'
    if os.path.exists(anim_dir):
        
        for filename in os.listdir(anim_dir):
            path = os.path.join(anim_dir, filename)

            if os.path.isdir(path):
                iter_fnis_lists(path, parse_fnis_list)
                
    ActionLogFound = False
    if slate_path is not None:
        print("---------> PARSING SLATE ACTION_LOGS")
        
        parsed_slate_data = []
        def parse_slate_actionlogs(filename):
            info = json.load(file)
            string_list = info["stringList"]["slate.actionlog"]
            
            for item in string_list:
                action, anim, tag = item.split(',', 2)
                action = action.lower()
                anim = anim.strip()
                tag = tag.strip()
                
                parsed_slate_data.append({
                    "action": action,
                    "anim": anim,
                    "tag": tag
                })
            return parsed_slate_data
            
        for filename in os.listdir(slate_path):
            path = os.path.join(slate_path, filename)
            if os.path.isfile(path) and filename.startswith('SLATE_ActionLog') and filename.endswith('.json'):
                ActionLogFound = True
                with open(path, "r") as file:
                    parse_slate_actionlogs(file) 
    
    print("---------> APPLYING TAGS AND ACTOR FLAGS")
    def process_stage(scene, stage, stage_num):
        name = scene['name']
        tags = [tag.lower().strip() for tag in stage['tags']]

        if ActionLogFound:
            TagToAdd = ''
            TagToRemove = ''
            for entry in parsed_slate_data:
                if name.lower() in entry['anim'].lower():
                    if entry['action'].lower() == 'addtag':
                        TagToAdd = entry['tag'].lower()
                        if TagToAdd not in tags:
                            tags.append(TagToAdd)
                    elif entry['action'].lower() == 'removetag':
                        TagToRemove = entry['tag'].lower()
                        if TagToRemove in tags:
                            tags.remove(TagToRemove)

        if 'basescale' in name.lower() or 'base scale' in name.lower() or 'setscale' in name.lower() or 'set scale' in name.lower() or 'bigguy' in anim_dir_name.lower():
            tags.append('scaling')
        if ('femdom' in name.lower() or 'amazon' in name.lower() or 'femaledomination' in tags or 'female domination' in tags or 'femdom' in anim_dir_name.lower() \
            or 'leito xcross standing' in name.lower() or 'amazon' in tags) and 'femdom' not in tags:
            tags.append('femdom')
        if ('guro' in tags or 'execution' in tags or 'guro' in name.lower() or 'guro' in anim_dir_name.lower()) and 'gore' not in tags:
            tags.append('gore')
        if any(kwd in name.lower() or kwd in tags for kwd in magic_kwds) and 'magic' not in tags:
            tags.append('magic')
        if ('choke' in tags or 'choking' in tags or 'choke' in name.lower()) and 'asphyxiation' not in tags:
            tags.append('asphyxiation')
        if ('inv' in name.lower() or 'inv' in anim_dir_name.lower()) and 'invisfurn' not in tags:
            tags.append('invisfurn')
        if 'invisfurn' in tags and 'furniture' in tags:
            tags.remove('furniture')
        if any(kwd in name.lower() or kwd in tags for kwd in furni_kwds) and 'invisfurn' not in tags and 'furniture' not in tags:
            tags.append('furniture')
        if ('facesit' in tags or 'facesit' in name.lower()) and 'facesitting' not in tags:
            tags.append('facesitting')
        if ('lotus' in tags or 'lotus' in name.lower()) and 'lotusposition' not in tags:
            tags.append('lotusposition')
        if ('trib' in name.lower() or 'tribbing' in tags) and 'tribadism' not in tags:
            tags.append('tribadism')
        if ('doggystyle' in tags or 'doggy' in name.lower()) and 'doggy' not in tags:
            tags.append('doggy')
        if ('spank' in tags or 'spank' in name.lower()) and 'spanking' not in tags:
            tags.append('spanking')
        if 'dp' in tags or 'doublepen' in tags and 'doublepenetration' not in tags:
            tags.append('doublepenetration')
        if 'tp' in tags or 'triplepen' in tags and 'triplepenetration' not in tags:
            tags.append('triplepenetration')
        if 'lying' in tags and 'laying' in tags and 'eggs' not in tags:
            tags.remove('laying')
        if 'rimjob' in tags and 'rimming' not in tags:
            tags.append('rimming')
        if 'kiss' in tags and 'kissing' not in tags:
            tags.append('kissing')
        if 'hold' in tags and 'holding' not in tags:
            tags.append('holding')
        if '69' in tags and 'sixtynine' not in tags:
            tags.append('sixtynine')
        if '' in tags:
            tags.remove('')

        if ActionLogFound:
            asl_en = str(stage_num) + "en"  # end_stage
            if asl_en in tags:
                stage_num = stage_num - 1
            asl_li = str(stage_num) + "li"  # lead_in
            asl_sb = str(stage_num) + "sb"  # slow_oral
            asl_fb = str(stage_num) + "fb"  # fast_oral
            asl_sv = str(stage_num) + "sv"  # slow_vaginal
            asl_fv = str(stage_num) + "fv"  # fast_vaginal
            asl_sa = str(stage_num) + "sa"  # slow_anal
            asl_fa = str(stage_num) + "fa"  # fast_anal
            asl_sr = str(stage_num) + "sr"  # spit_roast
            asl_dp = str(stage_num) + "dp"  # double_pen
            asl_tp = str(stage_num) + "tp"  # triple_pen

            if (asl_li in tags or asl_sb in tags or asl_fb in tags or asl_sv in tags or asl_fv in tags or asl_sa in tags or asl_fa in tags \
                or asl_sr in tags or asl_dp in tags or asl_tp in tags or asl_en in tags) and 'asltagged' not in tags:
                tags.append('asltagged')

            if 'asltagged' in tags:
                # stores info on vaginal/anal tag presence (for spitroast)
                if 'anal' in tags and 'vaginal' not in tags:
                    tags.append('sranaltmp')
                else:
                    tags.append('srvagtmp')
                # removes all scene tags that would be added by ASL
                if 'leadin' in tags:
                    tags.remove('leadin')
                if 'oral' in tags:
                    tags.remove('oral')
                if 'vaginal' in tags:
                    tags.remove('vaginal')
                if 'anal' in tags:
                    tags.remove('anal')
                if 'spitroast' in tags:
                    tags.remove('spitroast')
                if 'doublepenetration' in tags:
                    tags.remove('doublepenetration')
                if 'triplepenetration' in tags:
                    tags.remove('triplepenetration')
                # each stage tagged differently based on ASL
                if asl_li in tags and 'leadin' not in tags:
                    tags.append('leadin')
                if (asl_sb in tags or asl_fb in tags) and 'oral' not in tags:
                    tags.append('oral')
                if (asl_sv in tags or asl_fv in tags) and 'vaginal' not in tags:
                    tags.append('vaginal')
                if (asl_sa in tags or asl_fa in tags) and 'anal' not in tags:
                    tags.append('anal')
                if asl_sr in tags:
                    if 'spitroast' not in tags:
                        tags.append('spitroast')
                    if 'oral' not in tags:
                        tags.append('oral')
                    if 'sranaltmp' in tags:
                        tags.append('anal')
                    if 'srvagtmp' in tags:
                        tags.append('vaginal')
                if asl_dp in tags:
                    if 'doublepenetration' not in tags:
                        tags.append('doublepenetration')
                    if 'vaginal' not in tags:
                        tags.append('vaginal')
                    if 'anal' not in tags:
                        tags.append('anal')
                if asl_tp in tags:
                    if 'triplepenetration' not in tags:
                        tags.append('triplepenetration')
                    if 'oral' not in tags:
                        tags.append('oral')
                    if 'vaginal' not in tags:
                        tags.append('vaginal')
                    if 'anal' not in tags:
                        tags.append('anal')
                if asl_sb in tags or asl_sv in tags or asl_sa in tags:
                    tags.append('aslslow')
                if asl_fb in tags or asl_fv in tags or asl_fa in tags:
                    tags.append('aslfast')
                if 'sranaltmp' in tags:
                    tags.remove('sranaltmp')
                if 'srvagtmp' in tags:
                    tags.remove('srvagtmp')
                    
        sub = False
        futa = False
        #leadin = False

        sub_tags = {
            'unconscious': False,   # necro stuff
            'gore': False,          # something gets chopped off
            'amputee': False,       # missing one/more limbs
            'ryona': False,         # dilebrately hurting sub
            'humiliation': False,   # includes punishments too
            'forced': False,        # rape and general non-consensual
            'asphyxiation': False,  # involving choking sub
            'spanking': False,      # you guessed it
            'dominant': False       # consensual bdsm
        }
        
        for i in range(len(tags)):
            try:
                tag = tags[i]
            except:
                tag = tags[i - 1]
            
            if tag == 'cunnilingius':
                tags[i] = 'cunnilingus'
            if tag == 'agressive':
                tags[i] = 'aggressive'
            if tag == 'femodm':
                tags[i] = 'femdom'
            if tag == 'invfurn':
                tags[i] = 'invisfurn'
            if tag == 'invisible obj':
                tags[i] = 'invisfurn'
            if tag == 'laying' and 'eggs' not in tags:
                tags[i] = 'lying'
            
            if tag in unconscious_kwds or 'necro' in name.lower() or 'necro' in anim_dir_name.lower():
                sub_tags['unconscious'] = True
            if 'gore' in tags:
                sub_tags['gore'] = True
            if 'amputee' in tags or 'amputee' in name.lower() or 'amputee' in anim_dir_name.lower():
                sub_tags['amputee'] = True
            if 'nya' in tags or 'psycheslavepunishment' in name.lower():
                sub_tags['ryona'] = True
            if 'humiliation' in tags or 'punishment' in tags or 'punishment' in name.lower():
                sub_tags['humiliation'] = True
            if 'forced' in tags or 'rape' in tags or 'fbrape' in tags or (tag in uses_only_agg_tag and 'aggressive' in tags) \
                or 'rape' in name.lower() or 'force' in name.lower() or 'rough' in name.lower() or 'rape' in anim_dir_name.lower():
                sub_tags['forced'] = True
            if 'asphyxiation' in tags:
                sub_tags['asphyxiation'] = True
            if 'spanking' in tags:
                sub_tags['spanking'] = True
            if any(kwd in tags for kwd in dom_kwds):
                sub_tags['dominant'] = True

            sub = any(sub_tags.values())
            for sub_tag, sub_flag in sub_tags.items():
                if sub_flag and sub_tag not in tags:
                    tags.append(sub_tag)
                elif not sub_flag and sub_tag in tags:
                    tags.remove(sub_tag)

            if tag in futa_kwds or 'futa' in name.lower() or 'futa' in anim_dir_name.lower():
                futa = True
        
        if 'asltagged' not in tags:
            if 'leadin' in tags:
                tags.remove('leadin')
            if any(kwd in tags for kwd in leadin_kwds) and all(kwd not in tags for kwd in not_leadin_kwds):
                tags.append('leadin')
                #leadin = True
        
        positions = stage['positions']
        
        male_count = 0
        female_count = 0
        for pos in positions:
            if pos['sex']['male']:
                male_count += 1
            if pos['sex']['female']:
                female_count += 1
        straight = male_count > 0 and female_count > 0
        gay = male_count > 0 and female_count == 0
        lesbian = female_count > 0 and male_count == 0
        
        for i in range(len(positions)):
            pos = positions[i]

            if sub:
                if straight and female_count == 1 and 'femdom' not in tags and pos['sex']['female']:
                    pos['extra']['submissive'] = True
                if straight and female_count == 2 and 'femdom' not in tags: #needs_testing
                    if pos['sex']['female']:
                        pos['extra']['submissive'] = True
                if straight and ('femdom' in tags or 'ffffm' in tags) and pos['sex']['male']:
                    pos['extra']['submissive'] = True
                if gay and (('m2m' in tags and male_count == 2 and i == 0) or ('hcos' in tags and (pos['race'] == 'Rabbit' or pos['race'] == 'Skeever' or pos['race'] == 'Horse'))):
                    pos['extra']['submissive'] = True
                if lesbian and i == 0: # needs_testing
                    pos['extra']['submissive'] = True

                if sub_tags['unconscious'] == True and pos['extra']['submissive']:
                    pos['extra']['submissive'] = False
                    pos['extra']['dead'] = True

            if 'vamp' in pos['event'][0].lower() and 'vampirelord' not in tags:
                human_vampire_anim = all(pos['race'] != "Vampire Lord" for pos in stage['positions'])
                if human_vampire_anim:
                    if 'vampire' not in tags:
                        tags.append('vampire')
                    if 'vampirefemale' in tags or 'vampirelesbian' in tags or 'femdom' in tags or 'cowgirl' in tags or 'vampfeedf' in pos['event'][0].lower():
                        if pos['sex']['female']:
                            pos['extra']['vampire'] = True
                    else:
                        if pos['sex']['male']:
                            pos['extra']['vampire'] = True
                            
            if futa: #initial_prep
                if 'kom_futaduo' in pos['event'][0].lower():
                    pos['sex']['female'] = False
                    pos['sex']['male'] = True
                if 'futafurniture01(bed)' in pos['event'][0].lower():
                    for pos in [positions[0]]:
                        pos['sex']['female'] = False
                        pos['sex']['futa'] = True
                    for pos in [positions[1]]:
                        pos['sex']['male'] = False
                        pos['sex']['female'] = True
                        
            #if leadin:
            #    for pos in stage['positions']:
            #        pos['strip_data']['default'] = False
            #        pos['strip_data']['helmet'] = True
            #        pos['strip_data']['gloves'] = True
            
            if pos['event'] and len(pos['event']) > 0:
                event = pos['event'][0].lower()
                if event in anim_data.keys():
                    data = anim_data[event]
                    pos['event'][0] = os.path.splitext(data['anim_file_name'])[0]
                    os.makedirs(os.path.dirname(os.path.join(out_dir, data['out_path'])), exist_ok=True)
                    if skyrim_path is not None:
                        shutil.copyfile(data['path'], os.path.join(out_dir, data['out_path']))
                    if 'anim_obj' in data and data['anim_obj'] is not None: #anim_object incorporation
                        pos['anim_obj'] = ','.join(data['anim_obj'])
             
            anim_obj_found = any(pos['anim_obj'] != "" and "cum" not in pos['anim_obj'].lower() for pos in stage['positions'])
            if not anim_obj_found and 'toys' in tags:
                tags.remove('toys') 
            if anim_obj_found and 'toys' not in tags:
                tags.append('toys')
                
            furniture = scene['furniture']
            if 'lying' in tags and not anim_obj_found:
                furniture['allow_bed'] = True

            #if 'invisfurn' in tags:
            #    furniture['furni_types'] = allowed_furnitures['type']
            #    do something...
                    
            has_strap_on = ''
            has_sos_value = ''
            has_schlong = ''
            has_add_cum = ''
            has_forward = ''
            has_side = ''
            has_up = ''
            has_rotate = ''

            if name in slal_json_data:
                source_anim_data = slal_json_data[name]
                actor_map = source_anim_data['actors']
                for i, actor_dict in enumerate(actor_map):
                    for key, value in actor_map.items():
                        actor_key = key
                        if actor_key.startswith('a'):
                            source_actor_data = actor_map[actor_key]

                            if 'add_cum' in source_actor_data and source_actor_data['add_cum'] != 0:
                                if has_add_cum and actor_key[1:] not in has_add_cum:
                                    has_add_cum += f",{actor_key[1:]}"
                                else:
                                    has_add_cum = actor_key[1:]

                            actor_stage_params_map = source_actor_data[f'{actor_key}_stage_params']
                            for key, value in actor_stage_params_map.items():
                                actor_stage_params_key = key
                                event_key = f"{actor_key}" + f"_s{actor_stage_params_key[6:]}"
                                if actor_stage_params_key.startswith('Stage'):
                                    source_actor_stage_params = actor_stage_params_map[actor_stage_params_key]

                                    if 'strap_on' in source_actor_stage_params and source_actor_stage_params['strap_on'] is not False:
                                        if has_strap_on and actor_key[1:] not in has_strap_on:
                                            has_strap_on += f",{actor_key[1:]}"
                                        else:
                                            has_strap_on = actor_key[1:]
                                    if 'sos' in source_actor_stage_params and source_actor_stage_params['sos'] != 0:
                                        has_sos_value = event_key
                                        #if event_key in has_sos_value and int(event_key[4:]) == stage_num:
                                        #    pos_num = int(actor_key[1:]) - 1
                                        #    for pos in [positions[pos_num]]:
                                        #        pos['schlong'] = source_actor_stage_params['sos']
                                        # for futa
                                        if has_schlong and actor_key[1:] not in has_schlong:
                                            has_schlong += f",{actor_key[1:]}"
                                        else:
                                            has_schlong = actor_key[1:]

                                    if 'forward' in source_actor_stage_params and source_actor_stage_params['forward'] != 0:
                                        has_forward = event_key
                                        if event_key in has_forward and int(event_key[4:]) == stage_num:
                                            pos_num = int(actor_key[1:]) - 1
                                            for pos in [positions[pos_num]]:
                                                pos['offset']['y'] = source_actor_stage_params['forward']
                                    if 'side' in source_actor_stage_params and source_actor_stage_params['side'] != 0:
                                        has_side = event_key
                                        if event_key in has_side and int(event_key[4:]) == stage_num:
                                            pos_num = int(actor_key[1:]) - 1
                                            for pos in [positions[pos_num]]:
                                                pos['offset']['x'] = source_actor_stage_params['side']
                                    if 'up' in source_actor_stage_params and source_actor_stage_params['up'] != 0:
                                        has_up = event_key
                                        if event_key in has_up and int(event_key[4:]) == stage_num:
                                            pos_num = int(actor_key[1:]) - 1
                                            for pos in [positions[pos_num]]:
                                                pos['offset']['z'] = source_actor_stage_params['up']
                                    if 'rotate' in source_actor_stage_params and source_actor_stage_params['rotate'] != 0:
                                        has_rotate = event_key
                                        if event_key in has_rotate and int(event_key[4:]) == stage_num:
                                            pos_num = int(actor_key[1:]) - 1
                                            for pos in [positions[pos_num]]:
                                                pos['offset']['r'] = source_actor_stage_params['rotate']
                            
                            ####### actor-specific fine tuning #######
                            if futa:
                                if 'anubs' in tags and ('ff' in tags or 'fff' in tags):
                                    if actor_key[1:] in has_schlong:
                                        pos_num = int(actor_key[1:]) - 1
                                        for pos in [positions[pos_num]]:
                                            pos['sex']['female'] = False
                                            pos['sex']['futa'] = True
                                if 'flufyfox' in tags:
                                    if actor_key[1:] in has_strap_on:
                                        pos_num = int(actor_key[1:]) - 1
                                        for pos in [positions[pos_num]]:
                                            pos['sex']['female'] = False
                                            pos['sex']['futa'] = True
                            #------------------------------------------
                            
                        stage_params_map = source_anim_data['stage_params']
                        for key, value in stage_params_map.items():
                            stage_params_key = key
                            if stage_params_key.startswith('Stage'):
                                source_stage_params = stage_params_map[stage_params_key]

                                if 'timer' in source_stage_params and source_stage_params['timer'] != 0:
                                    stage['extra']['fixed_len'] = round(float(source_stage_params['timer']), 2)

            ####### animator-specific fine tuning #######
            if futa:
                if 'solo' in tags or 'futaall' in tags or ('anubs' in tags and 'mf' in tags) or ('ff' in tags and ('frotting' in tags or 'milking' in tags)):
                    for pos in stage['positions']:
                        if pos['sex']['female']:
                            pos['sex']['female'] = False
                            pos['sex']['futa'] = True
                if 'billyy' in tags and 'cf' in tags:
                    if pos['race'] == 'Flame Atronach':
                        pos['sex']['female'] = False
                        pos['sex']['futa'] = True
                if 'billyy' in tags and '2futa' in tags and len(positions) == 3:
                    for pos in [positions[0], positions[1]]:
                        pos['sex']['female'] = False
                        pos['sex']['futa'] = True
                if 'ff' in tags and pos['sex']['male']:
                    pos['sex']['male'] = False
                    pos['sex']['futa'] = True

            if 'bigguy' in tags or 'scaling' in tags:
                pattern_bigguy = re.findall(r'(base\s?scale)\s?(\d+\.\d+)', name.lower())
                for match in pattern_bigguy:
                    if match[1] and pos['sex']['male']:
                        value = float(match[1].replace('"', ''))
                        pos['scale'] = round(value, 2)          
                pattern_scaling = re.findall(r'(set\s?scale)\s?(\d+(?:\.\d+)?)?', name.lower())
                for match in pattern_scaling:
                    if match[1]:
                        value = float(match[1].replace('"', ''))
                        if 'gs orc' in name.lower() and pos['sex']['male']:
                            pos['scale'] = round(value, 2)
                        if 'gs giantess' in name.lower() and pos['sex']['female']:
                            pos['scale'] = round(value, 2)
                        if 'hcos small' in name.lower() and pos['race'] == 'Dragon':
                            pos['scale'] = round(value, 2)
                #--------------------------------------------       
                
        stage['tags'] = tags
        
    print("---------> EDITING AND BUILDING SLSB PROJECTS")
    for filename in os.listdir(tmp_dir):
        path = os.path.join(tmp_dir, filename)
        
        if os.path.isdir(path):
            continue

        print('building slsb', filename)

        data = None
        with open(path, 'r') as f:
            data = json.load(f)

            scenes = data['scenes']
            data['pack_author'] = args.author

            for id in scenes:
                scene = scenes[id]
                stages = scene['stages']

                for i in range(len(stages)):
                    stage = stages[i]
                    stage_num = i + 1
                    process_stage(scene, stage, stage_num)

        edited_path = tmp_dir + '/edited/' + filename

        with open(edited_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        if not args.no_build:
            output = subprocess.Popen(f"{slsb_path} build --in \"{edited_path}\" --out \"{out_dir}\"", stdout=subprocess.PIPE).stdout.read()
            shutil.copyfile(edited_path, out_dir + '/SKSE/Sexlab/Registry/Source/' + filename)

    def build_behaviour(parent_dir, list_name):
        list_path = os.path.join(parent_dir, list_name)

        if '_canine' in list_name.lower():
            return

        behavior_file_name = list_name.lower().replace('fnis_', '')
        behavior_file_name = behavior_file_name.lower().replace('_list.txt', '')
        behavior_file_name = 'FNIS_' + behavior_file_name + '_Behavior.hkx'
        
        print('generating', behavior_file_name)

        cwd = os.getcwd()
        os.chdir(fnis_path)
        output = subprocess.Popen(f"./commandlinefnisformodders.exe \"{list_path}\"", stdout=subprocess.PIPE).stdout.read()
        os.chdir(cwd)

        out_path = os.path.normpath(list_path)
        out_path = out_path.split(os.sep)

        start_index = -1
        end_index = -1

        for i in range(len(out_path) - 1, -1, -1):
            split = out_path[i].lower()

            if split == 'meshes':
                start_index = i
            elif split == 'animations':
                end_index = i

        behaviour_folder = 'behaviors' if '_wolf' not in list_name.lower() else 'behaviors wolf'
        behaviour_path = os.path.join(skyrim_path, 'data', *out_path[start_index:end_index], behaviour_folder, behavior_file_name)

        if os.path.exists(behaviour_path):
            out_behavior_dir = os.path.join(out_dir, *out_path[start_index:end_index], behaviour_folder)
            out_behaviour_path = os.path.join(out_behavior_dir, behavior_file_name)
            os.makedirs(out_behavior_dir, exist_ok=True)
            shutil.copyfile(behaviour_path, out_behaviour_path)
        #else:
        if " " in anim_dir_name:
            print("")
            print(f'WARNING: FNIS could not generate HKX for {list_name}; use HKXCONV to manually convert the temporarily generated xml to hkx (xml generated into Data/tools/GenerateFNIS_for_Modders/temporary_logs/)')

        if remove_anims:
            for filename in os.listdir(parent_dir):
                if os.path.splitext(filename)[1].lower() == '.hkx':
                    os.remove(os.path.join(parent_dir, filename))
                    

    def edit_output_fnis(file_path, filename):
        full_path = os.path.join(file_path, filename)
        modified_lines = []
        with open(full_path, 'r') as file:
            for line in file:
                line = re.sub(r'b -a ', 'b ', line)         # option "-a" is not in original animlist (2500+ instances, plz fix condition)
                line = re.sub(r'b -o,a', 'b -o', line)      # unnecessary "a"; plus the correct format is -o,a
                line = re.sub(r'b -o, ', 'b -o ', line)     # correct format is -o (no additional comma)
                line = re.sub(r',', ' ', line)              # fix for script-added anim-objects
                if any(kwd in line.lower() for kwd in acyclic_stages):
                    if '-' in line:
                        line = re.sub(r'b -o ', 'b -o,a ', line)
                    elif '-' not in line:
                        line = re.sub(r'b ', 'b -a ', line)
                modified_lines.append(line)
        with open(full_path, 'w') as file:
            file.writelines(modified_lines)

    if fnis_path is not None:
        print("---------> BUILDING FNIS BEHAVIOUR")
        anim_dir = out_dir + '\\meshes\\actors'
        iter_fnis_lists(anim_dir, edit_output_fnis)
        iter_fnis_lists(anim_dir, build_behaviour)

    if args.clean:
        shutil.rmtree(tmp_dir)

for dir in os.listdir(parent_dir):
    mesh_dir = os.path.join(parent_dir, dir, 'meshes')
    slal_dir = os.path.join(parent_dir, dir, 'SLAnims')
    if os.path.exists(slal_dir):
        print("")
        print("============== PROCESSING " + dir + " ==============")
        convert(parent_dir, dir)