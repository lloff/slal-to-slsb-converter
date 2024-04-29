from converter.slate.SlateActionLog import SlateAction, SlateActionLog

class SlateActionLogs:
    slate_action_logs: list[SlateActionLog] = []

    def parse_slate_action_log(json):
        slate_log = SlateActionLog()

        string_list = json["stringList"]["slate.actionlog"]
        
        for item in string_list:
            action, anim, tag = item.split(',', 2)
            action = action.lower()
            anim = anim.strip()
            tag = tag.strip()

            slate_action = SlateAction(action, anim, tag)
            slate_log.actions.append(slate_action)
            

        SlateActionLogs.slate_action_logs.append(slate_log)

        
