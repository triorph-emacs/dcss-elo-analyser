import pickle
import operator
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
			if tmp['v'].startswith('0.14') or tmp['v'].startswith('0.15') or tmp['v'].startswith('0.16'):
				data.append((tmp['end'], tmp['name'], tmp['char'], tmp['ktyp']))

print "Sorting data by date"

data2 = sorted(data, key=operator.itemgetter(0))

charelo = {}
nameelo = {}

player_counts = {}

k_factor = 32

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

print "Starting ELO calculations"
for time, name, char, ktyp in data2:
	if name not in nameelo:
		nameelo[name] = [1200.0]
	if char not in charelo:
		charelo[char] = [1729.0] # 4.54% chance of success on average by default
	probability_of_win = 1.0 / (1.0 + 10.0 ** ((charelo[char][-1] - nameelo[name][-1])/400.0))
	if ktyp == 'winning':
		# increase player ELO and decrease char ELO.
		nameelo[name].append(nameelo[name][-1] + k_factor * (1.0 - probability_of_win))
		if player_counts[name][1] >= 5:	# only update char elo if the player is good(ish)
			charelo[char].append(charelo[char][-1] - k_factor * (1.0 - probability_of_win))
	else:
		#decrease player ELO and increase char ELO.
		nameelo[name].append(nameelo[name][-1] - k_factor * (probability_of_win))
		if player_counts[name][1] >= 5:	# only update char elo if the player is good(ish)	
			charelo[char].append(charelo[char][-1] + k_factor * (probability_of_win))
		
elo_scores = {"players":nameelo, "characters":charelo}

with open("eloscores.pickle", "w") as f:
	pickle.dump(elo_scores, f)
		
