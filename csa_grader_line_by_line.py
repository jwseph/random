from csa_grader import get_response

messages = []

while True:
    cur = []
    line = input()
    cnt = 0
    while True:
        cnt += 1
        if line: cnt = 0
        if cnt == 2: break
        cur.append(line)
        line = input()
    messages.append({
        'role': 'user',
        'content': '\n'.join(cur).strip()
    })
    text = get_response(messages)
    print(text)
    messages.append({
        'role': 'assistant',
        'content': text,
    })