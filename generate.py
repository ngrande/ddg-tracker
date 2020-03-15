#!/usr/bin/env python3

import datetime
import os
import json
import argparse


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("path", help="path to the domain files", type=str)
	parser.add_argument("--categories", help="comma separated list of categories to block", type=str)
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
	if args.categories:
		categories_to_block = args.categories.split(",")

	path = args.path
	domains = set()

	for domain in os.listdir(path):
		domain_file = os.path.join(path, domain)
		print("reading file {}".format(domain_file))
		with open(domain_file, "r", encoding="utf-8") as f:
			domain_json = json.load(f)

			categories = domain_json['categories']
			print(categories)
			for cat in categories:
				cat = cat.lower()
				if cat in categories_to_block:
					domain = domain_json['domain']
					domains.add(domain)
					print("adding domain: {}".format(domain))
					break

	with open(args.output, "w", encoding="utf-8") as dest:
		dest.write("# generated at {}\n".format(datetime.datetime.now()))
		dest.writelines(["0.0.0.0 " + d + "\n" for d in domains])

# vim: tabstop=4 shiftwidth=4 noexpandtab ft=python
