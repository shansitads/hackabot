from setup import sentence_comparer, cos_sim, faq_data, judging_schedule, teams_list


def similarity_score(sentence1, sentence2) -> float:
    '''use STS to determine how similar two texts are'''

    embeddings = sentence_comparer.encode([sentence1, sentence2])

    # Compute cosine similarities of the sentences.
    # The cos_sim function will return a 2 x 2 matrix of similarity scores, 
    # but we only need the index at which the distinct sentences are commpared.
    # Then convert tensor array to float
    score = float(cos_sim(embeddings[1], embeddings[0])[0][0])

    return score



def find_judging_time(team_name):
    '''Prerequisite: Users must take roles according to team names'''

    for team in judging_schedule['schedule']:
        if team['team'] == team_name:
            return team['time']
    return 'Your team\'s schedule is not decided yet.'



def get_user_team(user) -> str:
    '''find a user's team name from their Discord roles'''

    # user may have multiple roles, find team name using list of teams provided in team_list.csv
    user_roles = [role.name for role in user.roles]
    team_name = [role for role in user_roles if role in teams_list]

    # assert that the user has selected their team as a role
    assert(len(team_name) != 0), 'User has not selected a team role'

    assert(len(team_name) <= 1), 'User has selected multiple team roles'
    
    return team_name[0]



def handle_response(message, usermessage) -> str:
    '''if question is identified, return a text response, else None'''

    # minimum similarity score required for two textx to be considered similar
    MIN_SCORE = 0.5
    
    # answer = [response text, similarity score of associated question]
    answer = ['', 0.0]
    
    for row in faq_data:
        score = similarity_score(row[0], usermessage)
        if score > MIN_SCORE and score > answer[1]:
            answer[0] = row[1]
            answer[1] = score
    

    # if question is about judging schedule
    score = similarity_score('When will my team be judged?', usermessage)
    if score > MIN_SCORE:
        # judging timings are assigned by team in judging_schedule.json
        # so message sender must have selected a team role in discord first
        try:
            answer[0] = find_judging_time(get_user_team(message.author))
        except AssertionError:
            answer[0] = 'Please select your team role in the roles channel to know your schedule. Only one team must be selected.'
        answer[1] = score

    
    if answer != ['', 0.0]:
        return answer[0]
    else:
        return None