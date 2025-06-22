from openai import OpenAI
from csa_grader_config import QUESTIONS, SCORING_GUIDE, CRITERIA
import os
import json
from copy import deepcopy
import threading
import concurrent.futures
from dotenv import load_dotenv
load_dotenv()

# Initialize the OpenAI API client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_response(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.0,
        messages=messages,
    )
    return response.choices[0].message.content

explanations = []

with open('csa_grader_testcases.json') as f:
    csa_data = json.load(f)

def run_in_parallel(fn, *argses: list):
    res = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fn, *args) for args in zip(*argses)]
        for future in concurrent.futures.as_completed(futures):
            res.append(future.result())
    return res

class CSAGrader:
    def __init__(self, test_data: dict):
        self.test = test_data['test']
        self.questions = test_data['questions']
        self.scoring_guide = test_data['scoring_guide']
        self.rubric = deepcopy(test_data['rubric'])
        self.examples = deepcopy(test_data['examples'])
        pass

    def grade_code(self, code: str):
        # threads = []
        # res = {}
        # # for question_data in self.rubric:
        # #     threads.append([])
        # #     cur = res[question_data['question']] = [None] * len(question_data['rows'])
        # #     for row in question_data['rows']:
        # #         t = threading.Thread(target=self._grade_row, args=(code, row, lambda: cur[] := 2))
        # #         t.daemon = True
        # #         t.run()
        # #         threads[-1].append(t)

        res_list = run_in_parallel(
            self._grade_row,
            [code]*1000,
            [row for question_data in self.rubric for row in question_data['rows'][4:5]],
        )
        
        res = {}
        i = 0
        for question_data in self.rubric:
            cur = []
            for row in question_data['rows'][4:5]:
                cur.append(res_list[i])
                i += 1
            res[question_data['question']] = cur
        return res

    def _grade_row(self, code: str, row: dict[str, str]):
        messages = [
            {
                "role": "system",
                "content": "You are a CS A FRQ grader. Please grade responses as accurately as possible and explain uncertainty if uncertain about a point.",
            },
            {
                "role": "user",
                "content": "Here are the AP CS A 2023 questions\n" + QUESTIONS,
            },
            {
                "role": "user",
                "content": "Here are the scoring guidelines for AP CS A 2023 FRQ\n" + SCORING_GUIDE,
            },
            {
                "role": "user",
                "content": "Here is a student response\n" + code,
            },
            {
                "role": "user",
                "content": "\n".join([
                    f"WITHOUT MENTIONING THE GRADE YOU WOULD GIVE, WITHOUT MENTIONING ANY SCORE, please describe to a grader how to grade whether the student's code (maybe more inefficient) meets the following row ({row['part']}):",
                    row['req'],
                ])
            },
        ]

        
        resp = get_response(messages[:-1])
        # print(f'{resp=}')
        explanations.append(resp)
        print(resp)
        messages += [
            {
                "role": "assistant",
                "content": resp,
            },
            {
                "role": "user",
                "content": "\n".join([
                    # f"Please output how many points the student earns if you grade the following row ({criterion['part']}):",
                    # criterion['req'],
                    "Please output ONLY A SINGLE INTEGER, the score for this row. Do not respond with anything else, any more, or any less.",
                ])
            },
        ]
        res = get_response(messages)
        return res

# https://apcentral.collegeboard.org/media/pdf/ap23-sg-computer-science-a.pdf

if __name__ == '__main__':
    grader = CSAGrader(csa_data['2023'])

    print(csa_data['2023']['examples'][0]['score'])
    print(grader.grade_code(csa_data['2023']['examples'][0]['code']))

    # for i, criterion in enumerate(CRITERIA, 1):
    #     print(f'{i}. {grade_row(code, criterion)}')

    print(explanations)