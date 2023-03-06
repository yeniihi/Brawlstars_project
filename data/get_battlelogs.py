import brawlstats
from pathlib import Path
import pandas as pd
import datetime

def parse_single_user(tag):
    parsed_logs = []
    battles = client.get_battle_logs(tag)
    for battle in battles:

        # 배틀모드가 3대3인 경우만 추출합니다. 그외 클럽리그, 파워리그, 보스전, 빅게임, 로보럼블까지 총 5개의 모드는 배틀로그 형태가 달라서 일단 제외합니다.
        if battle['event']['mode'] in ['gemGrab', 'brawlBall', 'knockout', 'heist', 'bounty', 'hotZone', 'basketBrawl']:

            battle_info = {
                "battle_time": battle['battle_time'],
                "mode": battle['event']['mode'],
                "map": battle['event']['map'],
                "type": battle['battle']['type'],
                "duration": battle['battle']['duration'],
            }

            # 배틀결과가 무승부인 경우와 같이 스타플레이어가 없는 경우 오류를 피하기 위해 if 조건문을 사용합니다.
            if battle['battle']['star_player'] != None:
                try:
                    star_player_tag = battle['battle']['star_player']['tag'][1:]
                except:
                    pass

                teams = battle['battle']['teams']

                for team in teams:
                    players_tag = [member['tag'][1:] for member in team]
                    side = 1 if tag in players_tag else 2

                    for player in team:
                        player_info = client.get_profile(player['tag'][1:])
                        player_brawlers = sorted(player_info.brawlers, key= lambda x: x['trophies'], reverse=True)

                        for brawler in player_brawlers:
                            if brawler['id']==player['brawler']['id']:
                                gadget = 1 if ['gadgets'] else 0
                                star_power = 1 if brawler['star_powers'] else 0
                        
                        team_info = {
                            'player_tag': player['tag'],
                            'player_name': player['name'],
                            'player_trophies': player_info.trophies,
                            'player_top_brawler': player_brawlers[0]['name'],
                            'star_player': 1 if player['tag'][1:] == star_player_tag else 0,
                            'team': side,
                            'result': battle['battle']['result'],
                            'rank': None,
                            'brawler_id': player['brawler']['id'],
                            'brawler_name': player['brawler']['name'],
                            'brawler_power': player['brawler']['power'],
                            'brawler_star_power': star_power,
                            'brawler_gadget': gadget,
                            'brawler_trophies': player['brawler']['trophies'],
                        }

                        parsed_logs.append({**battle_info, **team_info})

        elif battle['event']['mode'] == 'duoShowdown':
            
            battle_info = {
                "battle_time": battle['battle_time'],
                "mode": battle['event']['mode'],
                "map": battle['event']['map'],
                "type": battle['battle']['type'],
                "duration": None,
            }

            teams = battle['battle']['teams']

            for team in teams:
                players_tag = [member['tag'][1:] for member in team]
                side = 1 if tag in players_tag else teams.index(team) + 2

                for player in team:
                    player_info = client.get_profile(player['tag'][1:])
                    player_brawlers = sorted(player_info.brawlers, key= lambda x: x['trophies'], reverse=True)

                    for brawler in player_brawlers:
                        if brawler['id']==player['brawler']['id']:
                            gadget = 1 if ['gadgets'] else 0
                            star_power = 1 if brawler['star_powers'] else 0
                    
                    team_info = {
                        'player_tag': player['tag'],
                        'player_name': player['name'],
                        'player_trophies': player_info.trophies,
                        'player_top_brawler': player_brawlers[0]['name'],
                        'star_player': 1 if player['tag'][1:] == star_player_tag else 0,
                        'team': side,
                        'result': None,
                        'rank': battle['battle']['rank'] if tag in players_tag else 0,
                        'brawler_id': player['brawler']['id'],
                        'brawler_name': player['brawler']['name'],
                        'brawler_power': player['brawler']['power'],
                        'brawler_star_power': star_power,
                        'brawler_gadget': gadget,
                        'brawler_trophies': player['brawler']['trophies'],
                    }

                    parsed_logs.append({**battle_info, **team_info})
    

    return parsed_logs