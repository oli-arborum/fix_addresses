# fix_addresses - Polish your address book by fixing address schema

Reads one or multiple VCF files (each containing one contact) and fixes the street in all contacts according to the following rule:

> When country is "DE", "Germany", "Deutschland" or not set, move the house number after the street. Otherwise don't touch it.

In case anything needed to be changed, the VCF file is rewritten.

**NOTE:** This script does not handle VCF files *containing more than one contact* and will **not warn** when reading such one. Contacts following the first contact will not be fixed and are possibly not contained in the re-written VCF file. (This does ***not*** affect multiple addresses for one contact. These are handled as expected!)

The script is intended to be used together with [vdirsyncer](https://github.com/pimutils/vdirsyncer). Use vdirsyncer to create a synced copy of your address book (which may be located at Google, Apple iCloud or another -- possibly self-hosted -- CardDAV server like [NextCloud](https://github.com/nextcloud/server) or [Radicale](https://github.com/Kozea/Radicale)), modify it with this script and then sync it back onto the server.

## Usage

Use `./fix_addr.py -h` to see usage information.

## License

see file LICENSE
