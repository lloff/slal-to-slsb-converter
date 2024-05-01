from converter.slate.SlateActionLogs import SlateActionLogs
from converter.slal.SLALPack import SLALPack

class SlateTags:

    def insert_slate_tags(tags: list[str], stage_name) -> None:

        if SlateActionLogs.slate_action_logs is not None:
            TagToAdd = ''
            TagToRemove = ''
            for slate_action_log in SlateActionLogs.slate_action_logs:
                for action in slate_action_log.actions:
                    if stage_name.lower() in action['anim'].lower():
                        if action['action'].lower() == 'addtag':
                            TagToAdd = action['tag'].lower()
                            if TagToAdd not in tags:
                                tags.append(TagToAdd)
                        elif action['action'].lower() == 'removetag':
                            TagToRemove = action['tag'].lower()
                            if TagToRemove in tags:
                                tags.remove(TagToRemove)


    def incorporate_stage_tags(tags: list[str], pack: SLALPack, stage_num: int):

        if (SlateActionLogs.slate_action_logs is not None):

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

