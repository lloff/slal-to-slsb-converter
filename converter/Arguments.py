class Arguments:
    slsb_path = None
    skyrim_path = None
    fnis_path = None
    slate_path = None
    remove_anims = None
    parent_dir = None
    author = None
    temp_dir = None
    no_build = None

    @staticmethod
    def load(args):
        Arguments.slsb_path = args.slsb

        Arguments.skyrim_path = args.skyrim
        Arguments.fnis_path = args.skyrim + '/Data/tools/GenerateFNIS_for_Modders' if args.skyrim is not None else None
        Arguments.remove_anims = args.remove_anims
        Arguments.parent_dir = args.working
        Arguments.slate_path = args.slate
        
        Arguments.author = args.author

        Arguments.temp_dir = 'tmp'

        Arguments.no_build = args.no_build
        Arguments.clean = args.clean