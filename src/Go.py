from converter.Arguments import Arguments
from converter.Loader import Loader
from converter.SLALPackConverter import SLALPackConverter

import argparse
import os
import shutil

class Go:
    def go() -> None:
        Go._parse_arguments()

        Go._setup_folders()

        Go._load_slate_action_logs()

        Go._convert_all()

        Go._clean()


    def _parse_arguments() -> None:
        parser = argparse.ArgumentParser(
                            prog='Sexlab Catalytic Converter',
                            description='Converts SLAL anims to SLSB automagically')

        parser.add_argument('-slsb', '--slsb', help='path to your slsb executable')
        parser.add_argument('-t', '--temp', help='path to a temp directory', default='/temp')
        parser.add_argument('-a', '--author', help='name of the author of the pack', default="Unknown")
        parser.add_argument('-c', '--clean', help='clean up temp dir after conversion', action='store_true')
        parser.add_argument('-s', '--skyrim', help='path to your skyrim directory', default=None)
        parser.add_argument('-slt', '--slate', help='path to the directory containing SLATE_ActionLog jsons', default=None) 
        parser.add_argument('-ra', '--remove_anims', help='remove copied animations during fnis behaviour gen', action='store_true')
        parser.add_argument('-nb', '--no_build', help='do not build the slsb project', action='store_true')
        parser.add_argument('working', help='path to your working directory; should be structured as {<working_dir>/<slal_pack>/SLAnims/json/}')

        Arguments.load(parser.parse_args())
    
    def _setup_folders() -> None:
        if os.path.exists(Arguments.parent_dir + "\\conversion"):
            shutil.rmtree(Arguments.parent_dir + "\\conversion")

        if os.path.exists(Arguments.temp_dir):
            shutil.rmtree(Arguments.temp_dir)

        os.makedirs(Arguments.temp_dir + '\\edited')

    def _clean() -> None:
        if Arguments.clean:
            shutil.rmtree(Arguments.temp_dir)

    def _load_slate_action_logs() -> None:
        Loader.load_slate_action_logs()

    def _convert_all() -> None:
        for dir in os.listdir(Arguments.parent_dir):
            SLALPackConverter.start(dir)
