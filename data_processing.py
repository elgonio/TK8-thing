from enums import char_dict, dan_names_dict
from collections import Counter
import math

# pandas dataframe columns
# Data columns (total 35 columns):
#  #   Column         Dtype 
# ---  ------         ----- 
#  0   battleId       object
#  1   battleType     int64 
#  2   gameVersion    int64 
#  3   winResult      int64 
#  4   totalRoundNum  int64 
#  5   battleAt       int64 
#  6   viewNum        int64 
#  7   stageId        object
#  8   highlightFlag  bool  
#  9   1pUserId       object
#  10  1pPlayerName   object
#  11  1pPolarisId    object
#  12  1pOnlineId     object
#  13  1pNgWordFlag   int64 
#  14  1pPlatform     int64 
#  15  1pRank         int64 
#  16  1pTekkenPower  int64 
#  17  1pCharaId      object
#  18  1pWinRoundNum  int64 
#  19  1pTagType01    int64 
#  20  1pTagType02    int64 
#  21  1pTagType03    int64 
#  22  2pUserId       object
#  23  2pPlayerName   object
#  24  2pPolarisId    object
#  25  2pOnlineId     object
#  26  2pNgWordFlag   int64 
#  27  2pPlatform     int64 
#  28  2pRank         int64 
#  29  2pTekkenPower  int64 
#  30  2pCharaId      object
#  31  2pWinRoundNum  int64 
#  32  2pTagType01    int64 
#  33  2pTagType02    int64 
#  34  2pTagType03    int64 
# dtypes: bool(1), int64(22), object(12)


# get unique players with their highest rank and character
def get_unique_players(df):
	# get unique players
	# first iterate over the df and get unique players
	unique_players = {}
	for index, row in df.iterrows():
		# 1p
		if row['1pUserId'] not in unique_players:
			unique_players[row['1pUserId']] = {
				'rank': row['1pRank'],
				'char': row['1pCharaId'],
				'platform': row['1pPlatform'],
				'tekken_power': row['1pTekkenPower'],
				'characters': {row['1pCharaId']},
			}
		else:
			# we have seen this player before but we want to capture all the characters they have played
			unique_players[row['1pUserId']]['characters'].add(row['1pCharaId'])

			# if the current rank is higher than the previous rank, update the rank and character
			if row['1pRank'] > unique_players[row['1pUserId']]['rank']:
				unique_players[row['1pUserId']]['rank'] = row['1pRank']
				unique_players[row['1pUserId']]['char'] = row['1pCharaId']

			# Let's also capture the highest tekken power
			if row['1pTekkenPower'] > unique_players[row['1pUserId']]['tekken_power']:
				unique_players[row['1pUserId']]['tekken_power'] = row['1pTekkenPower']
		# 2p
		if row['2pUserId'] not in unique_players:
			unique_players[row['2pUserId']] = {
				'rank': row['2pRank'],
				'char': row['2pCharaId'],
				'platform': row['2pPlatform'],
				'tekken_power': row['2pTekkenPower'],
				'characters': {row['2pCharaId']},
			}
		else:
			# we have seen this player before but we want to capture all the characters they have played
			unique_players[row['2pUserId']]['characters'].add(row['2pCharaId'])

			# if the current rank is higher than the previous rank, update the rank and character
			if row['2pRank'] > unique_players[row['2pUserId']]['rank']:
				unique_players[row['2pUserId']]['rank'] = row['2pRank']
				unique_players[row['2pUserId']]['char'] = row['2pCharaId']

			# Let's also capture the highest tekken power
			if row['2pTekkenPower'] > unique_players[row['2pUserId']]['tekken_power']:
				unique_players[row['1pUserId']]['tekken_power'] = row['2pTekkenPower']


	return unique_players

# split the unique players into 3 categories according to their highest rank
def split_unique_players(unique_players):
    # split the unique players into 3 categories according to their highest rank
    # 1. Beginners: rank 1 - 11
    # 2. Intermediate: rank 12 - 17
    # 3. Advanced: rank 18+
	
    beginners = {}
    intermediate = {}
    advanced = {}
    for user_id, data in unique_players.items():
        if data['rank'] <= 11:
            beginners[user_id] = data
        elif data['rank'] <= 17:
            intermediate[user_id] = data
        else:
            advanced[user_id] = data
			
    return beginners, intermediate, advanced

# get the most popular characters for a given category
def get_most_popular_characters(unique_players):
    # get the most popular characters for a given category
    character_counts = {}
    for user_id, data in unique_players.items():
        char = char_dict[data['char']]
        if char not in character_counts:
            character_counts[char] = 1
        else:
            character_counts[char] += 1
    return character_counts

# get the distribution of ranks for a given category
def get_rank_distribution(unique_players):
    rank_counts = {}
    for user_id, data in unique_players.items():
        rank = data['rank']
        if rank not in rank_counts:
            rank_counts[rank] = 1
        else:
            rank_counts[rank] += 1
    return rank_counts

def calculate_percentiles(rank_counts):
    total_players = sum(rank_counts.values())
    percentiles = {}
    cumulative_count = 0

    for rank, count in sorted(rank_counts.items()):
        percentile = (cumulative_count / total_players) * 100
        percentiles[dan_names_dict[rank]] = percentile
        cumulative_count += count

    return percentiles


# split replays into 3 categories according to the rank of the players
def split_replays_into_categories(master_df):
    # split replays into 3 categories according to the rank of the players
    # get games where both gamers are beginners i.e rank 1 - 11
    beginners = master_df[(master_df['1pRank'] <= 11) & (master_df['2pRank'] <= 11)]
    # get games where both gamers are intermediate i.e rank 12 - 17
    intermediate = master_df[((master_df['1pRank'] > 11) & (master_df['1pRank'] <= 17)) & ((master_df['2pRank'] > 11) & (master_df['2pRank'] <= 17))]
    # get games where both gamers are advanced i.e rank 18+
    advanced = master_df[(master_df['1pRank'] > 17) & (master_df['2pRank'] > 17)]
    return beginners, intermediate, advanced
    
def calculate_win_rates(master_df):
    # remove mirror matches
    mirror_matches = master_df[master_df['1pCharaId'] == master_df['2pCharaId']]
    master_df = master_df[master_df['1pCharaId'] != master_df['2pCharaId']]

    print(f"Number of mirror matches: {len(mirror_matches)}")

    # remove matches with draws
    master_df = master_df[master_df['winResult'] != 3]
    draws = master_df[master_df['winResult'] == 3]
    print(f"Number of matches with draws: {len(draws)}")

    # count the number of times each character appears in the 1pCharaId and 2pCharaId columns
    char1_counts = Counter(master_df['1pCharaId'])
    char2_counts = Counter(master_df['2pCharaId'])
    char_counts = char1_counts + char2_counts

    # count the number of times each character wins
    win_counts = Counter(master_df[master_df['winResult'] == 1]['1pCharaId'])
    win_counts += Counter(master_df[master_df['winResult'] == 2]['2pCharaId'])

    # calculate the win rates
    win_rates = {char_dict[k]: 0 for k in char_counts.keys()}
    for char, count in char_counts.items():
        if count != 0:
            win_rates[char_dict[char]] = win_counts[char] / count

    # sort the win rates dictionary
    win_rates = {k: v for k, v in sorted(win_rates.items(), key=lambda item: item[1], reverse=True)}

    # replace character ids with character names for char_counts
    char_counts_human_readable_names = {char_dict[k]: v for k, v in char_counts.items()} 
    confidence_intervals = calculate_confidence(win_rates, char_counts_human_readable_names)
    
    return win_rates, confidence_intervals

def calculate_confidence(win_rates, char_counts):
    confidence_intervals = {}
    z = 1.96  # Z-score for 95% confidence level
    

    for char, win_rate in win_rates.items():
        count = char_counts[char]
        if count != 0:
            standard_error = math.sqrt((win_rate * (1 - win_rate)) / count)
            margin_of_error = z * standard_error
            lower_bound = win_rate - margin_of_error
            upper_bound = win_rate + margin_of_error
            confidence_intervals[char] = (lower_bound, upper_bound)

    return confidence_intervals