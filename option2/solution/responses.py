from setup import sentence_comparer, cos_sim, faq_data


def similarity_score(sentence1, sentence2):
    embeddings = sentence_comparer.encode([sentence1, sentence2])

    # convert tensor array to float
    score = float(cos_sim(embeddings[1], embeddings[0])[0][0])

    return score


def handle_response(message) -> str:

    MIN_SCORE = 0.5

    # answer = [response text, similarity score of associated question to message]
    answer = ['', 0.0]

    print(faq_data)

    for row in faq_data:
        score = similarity_score(row[0], message)
        if score > MIN_SCORE and score > answer[1]:
            answer[0] = row[1]
            answer[1] = score
    
    if answer != ['', 0.0]:
        print(answer)
        return answer[0]
    else:
        return 'What?'