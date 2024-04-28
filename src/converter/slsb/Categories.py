from converter.Keywords import Keywords
from converter.slsb.Tags import Tags

class SubCategories:
    unconscious = False   # necro stuff
    gore = False          # something gets chopped off
    amputee = False       # missing one/more limbs
    ryona = False         # dilebrately hurting sub
    humiliation = False   # includes punishments too
    forced = False        # rape and general non-consensual
    asphyxiation = False  # involving choking sub
    spanking = False      # you guessed it
    dominant = False       # consensual bdsm

class Categories:
    sub = False
    sub_categories: SubCategories = SubCategories()
    maledom = False
    femdom = False
    maybe_femdom = False
    dead = False
    #leadin = False
    applied_restraint = False 
    restraint = ''
    furn = ''
    gay = False
    lesbian = False
    has_strap_on = False
    has_sos_value = False
    has_add_cum = False


    def get_categories(tags: list[str]):
        categories = Categories()

        for tag in tags:
            if tag in Keywords.sub:
                categories.sub = True
                categories.maledom = True
            if tag in Keywords.restraints:
                categories.sub = True
                categories.maledom = True
                categories.restraint = Keywords.restraints[tag]
            if tag in Keywords.femdom:
                categories.maybe_femdom = True
            if tag in Keywords.dead:
                categories.dead = True
            if tag == 'leadin':
                categories.leadin = True
            
        if categories.sub and categories.maybe_femdom:
            categories.maledom = False
            categories.femdom = True

        return categories

    def update_sub_categories(self, tags: list[str], scene_name: str, anim_dir_name: str) -> None:     
            self.sub_categories.asphyxiation = 'asphyxiation' in tags
            self.sub_categories.spanking = 'spanking' in tags
            self.sub_categories.gore = 'gore' in tags

            self.sub_categories.dominant = Tags._if_in_tags(tags, scene_name, anim_dir_name, Keywords.dominant)
            self.sub_categories.ryona = Tags._if_in_tags(tags, scene_name, anim_dir_name, ['nya', 'psycheslavepunishment'])
            self.sub_categories.unconscious = Tags._if_in_tags(tags, scene_name, anim_dir_name, Keywords.unconscious)
            self.sub_categories.amputee = Tags._if_in_tags(tags, scene_name, anim_dir_name, ['amputee'])
            self.sub_categories.humiliation = Tags._if_in_tags(tags, scene_name, anim_dir_name, ['humiliation', 'punishment'])
            self.sub_categories.forced = Tags._if_in_tags(tags, scene_name, anim_dir_name, ['forced', 'rape', 'fbrape', 'force', 'rough', 'aggressive'])
            ## Note: for forced, I removed the check for 'Keywords.uses_only_agg_tag' because is there ever going to be a use of the 'aggressive' tag without it being forced?

              

                