import os
import json
import pandas as pd

def read_data(folder_path):
	master_list = []
	failure_count = 0
	success_count = 0
	# Iterate over the files in the folder
	for filename in os.listdir(folder_path):
		if filename.endswith('.json'):
			# print(f'Processing file: {filename}')
			file_path = os.path.join(folder_path, filename)

			# Load the JSON file
			try:
				with open(file_path) as f:
					# remove any preceding or trailing whitespace
					json_String = f.read().strip()
					data = json.loads(json_String)
					master_list.extend(data) # Combine the lengths into the master list
					success_count += 1
			except Exception as e:
				# print(f'Error processing file: {filename}')
				failure_count += 1

	# Print the lengths of replayDetailList for each JSON file
	print(f'Read {len(master_list)} games from {success_count} files')
	print(f'{failure_count} files were unable to be read')

	return master_list

def read_data_into_dataframe(folder_path):
	master_list = read_data(folder_path)
	master_df = pd.DataFrame(master_list)
	return master_df.drop_duplicates(subset='battle_id', keep="last")


def read_data_v2(folder_path):
	master_list = []
	failure_count = 0
	success_count = 0
	# Iterate over the files in the folder
	for filename in os.listdir(folder_path):
		if filename.endswith('.json'):
			# print(f'Processing file: {filename}')
			file_path = os.path.join(folder_path, filename)

			# Load the JSON file
			try:
				master_list.append(pd.read_json(file_path))
			except Exception as e:
				# print(f'Error processing file: {filename}')
				failure_count += 1

	# Print the lengths of replayDetailList for each JSON file
	print(f'Read {len(master_list)} games from {success_count} files')
	print(f'{failure_count} files were unable to be read')

	return master_list

def read_data_into_dataframe_v2(folder_path):
	master_list = read_data_v2(folder_path)
	master_df = pd.concat(master_list)
	return master_df.drop_duplicates(subset='battle_id', keep="last")


# Example of a match
# {
#     "battleId": "f7c4c3ba9d9d4484a14d08c9eb1e1f9a",
#     "battleType": 2,
#     "gameVersion": 10104,
#     "winResult": 2,
#     "totalRoundNum": 4,
#     "battleAt": 1707948450,
#     "viewNum": 0,
#     "stageId": "stg_1600",
#     "highlightFlag": false,
#     "1pUserId": "023591240125230934",
#     "1pPlayerName": "Shadowmane",
#     "1pPolarisId": "33Ge2NF493EJ",
#     "1pOnlineId": "Ghetto63zoo",
#     "1pNgWordFlag": 0,
#     "1pPlatform": 8,
#     "1pRank": 13,
#     "1pTekkenPower": 92575,
#     "1pCharaId": "chr_0029",
#     "1pWinRoundNum": 1,
#     "1pTagType01": 0,
#     "1pTagType02": 0,
#     "1pTagType03": 0,
#     "2pUserId": "894212240204104936",
#     "2pPlayerName": "Ramma",
#     "2pPolarisId": "3dJhi33AmJHn",
#     "2pOnlineId": "Ramazan123-",
#     "2pNgWordFlag": 0,
#     "2pPlatform": 8,
#     "2pRank": 10,
#     "2pTekkenPower": 74847,
#     "2pCharaId": "chr_0006",
#     "2pWinRoundNum": 3,
#     "2pTagType01": 0,
#     "2pTagType02": 0,
#     "2pTagType03": 0
# },