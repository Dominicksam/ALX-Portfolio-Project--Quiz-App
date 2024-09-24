def calculate_score(user_answers, correct_answers):
    score = 0
    for user_answer, correct_answer in zip(user_answers, correct_answers):
        if user_answer == correct_answer:
            score += 1
    return score
