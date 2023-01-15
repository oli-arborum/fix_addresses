#!/usr/bin/env python3

import argparse
import os
import pathlib
import re
import vobject
from typing import Tuple

def fix_street(street: str) -> Tuple[bool, str]:
    '''
    returns the fixed street entry (house number after street name) and a
    bool indication whether anything was changed
    '''

    # regarding the regex:
    # initally, it seemed r'(\d+[a-z]*)\s+(.+)' would be sufficient (hanling
    # house numbers like "20a"), but that doesn't include
    # "1-3 Lusshardtstraße", so '\-?\d*[a-z]*' was added
    m  = re.search(r'(\d+[a-z]*\-?\d*[a-z]*)\s+(.+)', street)
    if m:
        street = m.group(2) + " " + m.group(1)
        return True, street
    # nothing changed: return original string
    return False, street

def fix_vcf_file(filename: str, dry_run: bool):
    '''
    fixes one VCF file containing one address item and writes it back in case
    anything needed to be changed
    '''
    with open(filename, "r") as f:
        vcard = vobject.readOne(f)
        print(f"processing '{vcard.fn.value}' (file '{filename}')")
        anything_changed = False
        if 'adr' in vcard.contents:
            # handle multiple addresses
            for adr in vcard.contents['adr']:
                # do not try to fix street when country is set and not Germany
                # (other countries have other street notions)
                if not adr.value.country or adr.value.country in ["Deutschland", "Germany", "DE"]:
                    changed, fixed_street = fix_street(adr.value.street)
                    if changed:
                        anything_changed = True
                        print(f"FIXED street: '{adr.value.street}' => '{fixed_street}'")
                        adr.value.street = fixed_street
                else:
                    print(f"skipped fixing, country is '{adr.value.country}'")
    # only write back if anything was changed
    if anything_changed:
        # first serialize, then write to file to prevent writing
        # an empty file when serializing failed
        vcard_serialized = vcard.serialize()
        if dry_run:
            print(f"DRY-RUN: skipped writing file '{filename}'")
        else:
            with open(filename, "w") as f:
                f.write(vcard_serialized)


parser = argparse.ArgumentParser(description='Fix address in one or many VCF files.')
parser.add_argument("vcf_file_or_directory", help="input VCF file or directory containing VCF files", type=pathlib.Path)
parser.add_argument("-d", "--dry-run", action="store_true", help="dry run, do not write to files")
args = parser.parse_args()

if not args.vcf_file_or_directory.exists():
    raise RuntimeError(f"File or directory {args.vcf_file_or_directory} not found!")

if args.vcf_file_or_directory.is_file():
    fix_vcf_file(str(args.vcf_file_or_directory), args.dry_run)
elif args.vcf_file_or_directory.is_dir():
    for p in args.vcf_file_or_directory.iterdir():
        if p.suffix == ".vcf":
            fix_vcf_file(str(p), args.dry_run)
