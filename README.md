# webpig 🐷

A web-based host discovery tool that helps you sniff out web-accessible hosts.

## What's This All About?

DNS Pig is a tool designed to help you discover and identify hosts that are accessible through the web. For simple research, I found myself using crt.sh and dnsdumpster quite a lot to determine which subdomains were available, but then had to manually determine which were otherwise reachable/interesting. 

_There are many tools out there, but this one is mine_

## Usage 

Using '--help' will pop up the help:

```
 Usage: python -m webpig [OPTIONS] DOMAIN                                                                                                 
                                                                                                                                          
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    domain      TEXT  [default: None] [required]                                                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│    --verbosity  -v      [debug|info|warning|error|critical]  Logging verbosity [default: info]                                         │
│ *  --source             [crt.sh]                             Sources to use for subdomain enumeration. If not provided, all sources    │
│                                                              will be used.                                                             │
│                                                              [default: None]                                                           │
│                                                              [required]                                                                │
│ *  --probe              [http]                               Probes to use for subdomain probing. If not provided, all probes will be  │
│                                                              used.                                                                     │
│                                                              [default: None]                                                           │
│                                                              [required]                                                                │
│    --help                                                    Show this message and exit.                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Everything is currently formatted in a json lines format (`.jsonl`) to stdout. To filter, parse, etc.. Use `jq`, for example:

```
python -m webpig google.com --source crt.sh --probe http | jq 'select(.reachable == true)'
```

This will keep only reachable hosts probed through `http`.

## Features

- Web-based interface for easy host discovery
- DNS enumeration capabilities (only crt.sh for now, more to come)
- User-friendly approach to network reconnaissance
- Helps identify potential targets in a web environment

## Getting Started

(Coming soon - installation and usage instructions will be added as the project develops)

## Contributing

Feel free to contribute! This is an open-source project, and we welcome pull requests, bug reports, and feature suggestions.
