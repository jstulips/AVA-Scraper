from utils import extractPage

from bs4 import BeautifulSoup

import urllib.request
import requests
import re
import time

# Variables
challenge_url = 'http://dpchallenge.com/challenge_history.php?order_by=0d&open=1&member=1&speed=1&invitational=1&show_all=1'
gallery_url = 'http://dpchallenge.com/photo_gallery.php'

# Get the latest challenge number from AVA 1.0
def getLastChallenge():

	# Last challenge to be stored in this variable
	last_challenge_id = None

	# Read the text file
	with open('AVA 1.0/challenges.txt') as file:

		# 1 line = Challenge ID followed by Challenge Name
		for line in file:
			challenge_info = line.split()

			# Compare with current number
			if (last_challenge_id is None) or (last_challenge_id < int(challenge_info[0])):
				last_challenge_id = int(challenge_info[0])

	return last_challenge_id

# Scrape the gallery page for semantic tags
def scrapeGalleryPage(url):

	# Scrape using BeautifulSoup
	gallery_page = extractPage(url)

	# Dictionary to store tags
	new_semantic_dict = {}

	# Find all the rows of galleries
	gallery_rows = gallery_page.findAll(
		lambda tag:
		'width' in tag.attrs and
		'cellspacing' in tag.attrs and
		'cellpadding' in tag.attrs and
		tag.attrs['width'] == '100%' and
		tag.attrs['cellspacing'] == '0' and
		tag.attrs['cellpadding'] == '3'
	)[0].findChildren('td')

	# Loop over row by row
	for row in gallery_rows:
		
		# Extract all links for a row
		gallery_links = row.findAll(
			lambda tag:
			'href' in tag.attrs and
			tag.attrs['href'].startswith('/photo_gallery.php?')
		)

		# Loop over link by link
		for gallery in gallery_links:

			# Extract ID
			tag_id = int(re.findall('\d+', gallery['href'])[0])

			# Extract text
			tag_name = gallery.text.replace(' ','_')

			# Store in key-value format ('ID': 'Name')
			new_semantic_dict[tag_id] = tag_name

	# Save in a text file
	with open('AVA 2.0/AVA 2.0 Semantics.txt', 'w', encoding='utf-8') as outfile:
		for key, value in new_semantic_dict.items():
			outfile.write(str(key) + ' ' + value + "\n")

# Scrape the challenge page (ALL results)
def scrapeChallengePage(url, stop_id):

	# Scrape using BeautifulSoup
	challenge_page = extractPage(url)

	# JSON File
	new_challenge_dict = {}

	'''
	# Find all rows (Each row is one challenge)
	challenge_rows = challenge_page.findAll(
		lambda tag:
		'href' in tag.attrs and
		tag.attrs['href'].startswith('/challenge_results.php')
	)


	# Loop challenge by challenge 
	for row in challenge_rows:

		# Extract ID
		row_id = int(re.findall('\d+', row['href'])[0])

		# If ID matches the last challenge of AVA 1.0, break
		if row_id == stop_id:
			break

		# Extract Challenge name (Replace spaces with _)
		row_name = row.text.split()
		row_name = "_".join(row_name)

		# Save in json format ('ID':'Challenge Name')
		new_challenge_dict[row_id] = row_name

	# Save in a text file
	with open("AVA 2.0/AVA 2.0 challenges.txt", "w", encoding='utf-8') as outfile:
		for key, value in new_challenge_dict.items():
			outfile.write(str(key) + " " + value + "\n")
	'''
	
	# Add in the entries (Rough idea of new photographs)
	# This area can be used for metadata purposes
	challenge_rows = challenge_page.findAll(
		lambda tag:
		'id' in tag.attrs and
		tag.attrs['id'] == 'challenges'
	)[1].findChildren('tr')

	challenge_rows.pop(0)

	for row in challenge_rows:

		# Challenge data to be stored in an array
		challenge_data = []

		# Find challenge tag and rule tag
		challenge_rule_td = row.findChildren('a')
		challenge_id = re.findall('\d+', challenge_rule_td[0]['href'])[0]
		rule_id = re.findall('\d+', challenge_rule_td[1]['href'])[0]

		# Append to array
		challenge_data += [challenge_id, rule_id]
		
		# Find metadata		
		row_td = row.findChildren('td', {'align': 'center'})

		# Add in number of new pictures, votes, comments
		challenge_data += [row_td[0].text.replace(',',''), 
			row_td[5].text.replace(',', ''), 
			row_td[7].text.replace(',','')
		]

		# Create string
		challenge_data = ' '.join(challenge_data)

		# Append to text file
		with open('AVA (All)/Challenge Info.txt', "a") as outfile:
			outfile.write(challenge_data + '\n')

	return

# Rules extract 
def extractRules(url):

	# Store in dictionary
	rules_dict = {}

	# Extract page
	page_extract = extractPage(url)

	# Find the rules ID from html
	rules = page_extract.findAll(
		lambda tag:
		'href' in tag.attrs and
		tag.attrs['href'].startswith('challenge_rules.php?')
	)

	for rule in rules:

		# Extract ID
		rule_id = int(re.findall('\d+', rule['href'])[0])

		# Check if in dictionary
		# If not, extract name and store as 'ID: Name'
		if rule_id not in rules_dict:

			rule_name = rule.text

			rules_dict[rule_id] = rule_name.replace(' ','_')

	# Write to text file
	with open("AVA (All)/AVA Rules.txt", "w", encoding='utf-8') as outfile:
		for key, value in rules_dict.items():
			outfile.write(str(key) + " " + value + "\n")

# Get the last ID
#ava_last_id = getLastChallenge()

# Scrape Challenge Page
#scrapeChallengePage(challenge_url, 1080)

# Scrape Gallery Page
#scrapeGalleryPage(gallery_url)

# Scrape Challenge Page
extractRules(challenge_url)