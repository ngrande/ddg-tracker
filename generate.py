#!/usr/bin/env python3

import datetime
import sys
import os
import json
import argparse


def dump(json_data):
	for key, val in json_data.items():
		print("[{}]: {}".format(key, val))

def is_whitelisted(categories, whitelist):
	for white in whitelist:
		if white in categories:
			return True
	return False


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("path", help="path to the domain files", type=str)
	parser.add_argument("--exclude", help="comma separated list of domains to exclude (from blocking)", type=str)
	parser.add_argument("--categories", help="comma separated list of categories to block", type=str)
	parser.add_argument("--categories-w", help="comma separated list of categories to whitelist", type=str)
	parser.add_argument("--output", help="absolute output file path", type=str, default="./duckduckgo_tracker.list")
	args = parser.parse_args()

	categories_to_block = ["action pixels",
							"ad fraud",
							"ad motivated tracking",
							"advertising",
							"analytics",
							"audience measurement",
							"malware",
							"obscure ownership",
							"third-party analytics marketing",
							"unknown high risk behavior"]
	categories_whitelist = ["CDN"]

	if args.categories:
		categories_to_block = args.categories.split(",")
	if args.categories_w:
		categories_whitelist = args.categories_w.split(",")

	path = args.path
	domains = set()

	for domain in os.listdir(path):
		domain_file = os.path.join(path, domain)
		print("reading file {}".format(domain_file))
		with open(domain_file, "r", encoding="utf-8") as f:
			domain_json = json.load(f)

			categories = domain_json['categories']
			domain = domain_json['domain']

			if is_whitelisted(categories, categories_whitelist):
				print("white listed domain: {}".format(domain))
				continue

			for cat in categories:
				cat = cat.lower()
				if cat in categories_to_block:
					domains.add(domain)
					print("adding domain: {}".format(domain))
					break

	if args.exclude:
		for exclude in args.exclude.split(","):
			if exclude not in domains:
				continue
			domains.remove(exclude)

	with open(args.output, "w", encoding="utf-8") as dest:
		dest.write("# generated at {}\n".format(datetime.datetime.now()))
		dest.writelines(["0.0.0.0 " + d + "\n" for d in domains])

# vim: tabstop=4 shiftwidth=4 noexpandtab ft=python
