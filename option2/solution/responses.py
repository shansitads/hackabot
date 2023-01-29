from setup import sentence_comparer, cos_sim, faq_data, judging_schedule, teams_list

def similarity_score(sentence1, sentence2) -> float:
    embeddings = sentence_comparer.encode([sentence1, sentence2])

    # convert tensor array to float
    score = float(cos_sim(embeddings[1], embeddings[0])[0][0])

    return score

# Prerequisite: Users must take roles according to team names
def find_judging_time(team_name):
    for team in judging_schedule['schedule']:
        if team['team'] == team_name:
            return team['time']
    return 'The schedule is not decided yet.'


def get_user_team(user):
    user_roles = [role.name for role in user.roles]
    print(user_roles)
    print(teams_list)
    # assert that the user has selected their team as a role
    team_name = [role for role in user_roles if role in teams_list]
    print(team_name)

    assert(len(team_name) != 0), 'User has not selected a team role'

    print(team_name[0])
    return team_name[0]


def handle_response(message, usermessage) -> str:

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
            answer[0] = 'Please select your team role in the roles channel to know your schedule.'
        answer[1] = score

    
    if answer != ['', 0.0]:
        print(answer)
        return answer[0]
    else:
        return 'What?'