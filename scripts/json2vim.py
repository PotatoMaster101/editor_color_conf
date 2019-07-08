#!/usr/bin/env python3
###############################################################################
# Converts JSON to vim colour settings. 
#
# Author: PotatoMaster101
# Date:   08/07/2019
###############################################################################

import argparse
import json

def get_args():
    """
    Returns the user arguments. 
    """
    p = argparse.ArgumentParser(description="JSON to VIM colour scheme.")
    p.add_argument("json", type=str, 
            help="the JSON file to convert")
    p.add_argument("-o", "--out-file", type=str, default="", dest="outf", 
            help="output file name")
    return p


def get_vim_hi(opt, optval):
    """
    Returns a VIM highlight command using the given options. 
    """
    # TODO need a mapping since cterm does not accept hex colours
    cmd = "hi %s" %opt
    if "background" in optval:
        cmd += " ctermbg=%s" %optval["background"]
    if "foreground" in optval:
        cmd += " ctermfg=%s" %optval["foreground"]
    return cmd


def get_vim_start(settings):
    """
    Returns the init lines for a VIM colour file. 
    """
    theme = "dark" if settings.get("theme", "Dark") == "Dark" else "light"
    name = settings.get("name", "TheUnknown")
    return ("highlight clear\n"
            "set background=%s\n"
            "if exists(\"syntax_on\")\n"
            "    syntax reset\n"
            "endif\n"
            "let g:colors_name = \"%s\"\n" %(theme, name)
            )


if __name__ == "__main__":
    """
    Entry point. 
    """
    args = get_args().parse_args()
    with open(args.json) as j:
        data = json.load(j)

    outf = args.outf if args.outf else "%s.vim" %args.json.split(".")[0]
    with open(outf, "w+") as out:
        print(get_vim_start(data.get("Settings", {})), file=out)
        for (k, v) in data.items():
            if k != "Settings":
                print(get_vim_hi(k, v), file=out)

