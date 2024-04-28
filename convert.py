from converter.slate.SlateParser import SlateParser
from converter.SLALPackConverter import SLALPackConverter
from converter.Arguments import Arguments
import os
import shutil
import argparse
import pprint
import time

start = time.time()

pp = pprint.PrettyPrinter(indent=4)

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

args = parser.parse_args()

Arguments.load(args)

if os.path.exists(Arguments.parent_dir + "\\conversion"):
    shutil.rmtree(Arguments.parent_dir + "\\conversion")

if os.path.exists(Arguments.temp_dir):
    shutil.rmtree(Arguments.temp_dir)

os.makedirs(Arguments.temp_dir + '\\edited')

for dir in os.listdir(Arguments.parent_dir):
    SLALPackConverter.start(dir)

if Arguments.clean:
    shutil.rmtree(Arguments.temp_dir)

total_time = time.time() - start

print(f"Time Taken: {round(total_time)}")