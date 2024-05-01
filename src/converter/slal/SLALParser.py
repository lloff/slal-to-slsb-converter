import json

##TODO: We dont rely on source parser but this slal parser for all stage params and actor stage params

slal_json_data = {}

class SLALParser:

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