from converter.slate.SlateActionLog import SlateAction, SlateActionLog
from converter.Arguments import Arguments
import os
import json

class SlateParser:
    def parse():

        ## TODO - at the moment this code must only load at the base slate_path
        ## Was it intended? Was it intended to look in the individual pack url instead?

        slate_logs: list[SlateActionLog] = []

        if Arguments.slate_path is not None:
            for filename in os.listdir(Arguments.slate_path):
                path = os.path.join(Arguments.slate_path, filename)
                if os.path.isfile(path) and filename.startswith('SLATE_ActionLog') and filename.endswith('.json'):
                    with open(path, "r") as file:
                        js = json.load(file)
                        slate_log = SlateParser._parse_json(js)

                        slate_logs.append(slate_log)

        return slate_logs


    def parse_slate_actionlogs(json):
        slate_log = SlateActionLog()

        string_list = json["stringList"]["slate.actionlog"]
        
        for item in string_list:
            action, anim, tag = item.split(',', 2)
            action = action.lower()
            anim = anim.strip()
            tag = tag.strip()

            slate_action = SlateAction(action, anim, tag)
            slate_log.actions.append(slate_action)

        return slate_log

        
