import pickle
import operator

import sys
chartype = "char"
if "char" in sys.argv:
	chartype = "char"
elif "race" in sys.argv or "species" in sys.argv:
	chartype = "race"
elif "class" in sys.argv or "role" in sys.argv or "background" in sys.argv:
	chartype = "role"
try:
	print "Opening previously sorted logs.."
	with open("sortedlogs.pickle", 'r') as f:
		data2 = pickle.load(f)
except:
	print "No logs sorted.. sorting now."
	with open('dcsslogs.pickle', 'r') as f:
		logfiles = pickle.load(f)

	data = []

	print "Getting data from logfiles"
	for logname in logfiles:
		print "in log:", logname
		lines = logfiles[logname].split('\n')
		for line in lines:
			if ":" in line:
				tmp = {}
				keyvals = line.split(':')
				for keyval in keyvals:
					if '=' in keyval:
						try:
							tmp2 = keyval.split('=')
							tmp[tmp2[0]] = tmp2[1]
						except Exception as msg:
							print msg
							print keyval
				if 'v' in tmp.keys() and (tmp['v'].startswith('0.15') or tmp['v'].startswith('0.16') or tmp['v'].startswith('0.17')):
					data.append((tmp['end'], tmp['name'], tmp['char'], tmp['ktyp']))

	print "Sorting data by date"

	data2 = sorted(data, key=operator.itemgetter(0))

	with open("sortedlogs.pickle", 'w') as f:
		pickle.dump(data2, f)
	

charelo = {}
nameelo = {}

player_counts = {}

k_factor = 20

print "Getting player list"
for time, name, char, ktyp in data2:
	if name not in player_counts:
		if ktyp == 'winning':
			player_counts[name] = [1,1]
		else:
			player_counts[name] = [1,0]
	else:
		player_counts[name][0] += 1
		if ktyp == 'winning':
			player_counts[name][1] += 1

print "Starting ELO calculations for", chartype
def workout_ELO(charelo_skip = False, nameelo_skip = False):
	for time, name, char, ktyp in data2:
		if chartype == "char":
			char = char
		elif chartype == "role":
			char = char[2:4]
		elif chartype == "race":
			char = char[0:2]
		if name not in nameelo:
			nameelo[name] = [1200.0]
		if char not in charelo:
			charelo[char] = [1729.0] # 4.54% chance of success on average by default
		probability_of_win = 1.0 / (1.0 + 10.0 ** ((charelo[char][-1] - nameelo[name][-1])/400.0))
		if ktyp == 'winning':
			# increase player ELO and decrease char ELO.
			change = k_factor * (1.0 - probability_of_win)
			if change > 100.0:
				print "huge change detected: time, name, char, ktyp, charelo, nameelo:", time, name, char, ktyp, charelo[char][-1], nameelo[name][-1]
			if not nameelo_skip: nameelo[name].append(nameelo[name][-1] + change)
			if player_counts[name][1] >= 5:	# only update char elo if the player is good(ish)
				if not charelo_skip: charelo[char].append(charelo[char][-1] - change)
		else:
			change = k_factor * (probability_of_win)
			if change > 100.0:
				print "huge change detected: time, name, char, ktyp, charelo, nameelo:", time, name, char, ktyp, charelo[char][-1], nameelo[name][-1]
			#decrease player ELO and increase char ELO.
			if not nameelo_skip: nameelo[name].append(nameelo[name][-1] - change)
			if player_counts[name][1] >= 5:	# only update char elo if the player is good(ish)	
				if not charelo_skip: charelo[char].append(charelo[char][-1] + change)

# reset the ELOs to defaults a few times and see if it converges away any timing effects
workout_ELO()
nameelo = {}
workout_ELO(charelo_skip=True)
charelo = {}
workout_ELO(nameelo_skip=True)
nameelo = {}
workout_ELO(charelo_skip=True)
charelo = {}
workout_ELO(nameelo_skip=True)
		
elo_scores = {"players":nameelo, "characters":charelo}

with open("eloscores.pickle", "w") as f:
	pickle.dump(elo_scores, f)
		
