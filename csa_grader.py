from openai import OpenAI
from csa_grader_config import QUESTIONS, SCORING_GUIDE, CRITERIA
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize the OpenAI API client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_response(context: dict, lines: list):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            *context,
            {
                "role": "user",
                "content": "\n".join(lines),
            },
        ],
    )
    return response.choices[0].message.content

def grade_row(code: str, criterion: dict[str, str]):

    context = [
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
    ]

    context += [
        {
            "role": "assistant",
            "content": get_response(context, [
                "Here is a student response",
                code,
                "Please output how many points the student earns if you grade the following row:",
                criterion['req'],
                "Output only a single integer, the score for this row. Do not respond with anything else.",
            ])
        }
    ]

    return get_response(
        
    )

code = '''
/*

Scoring guidelines:
https://apcentral.collegeboard.org/media/pdf/ap23-sg-computer-science-a.pdf

*/

(a)
public int findFreeBlock(int period, int duration) {
    int free = -1;
    for (int i = 0; i < 60 - duration + 1; i++) {
        int count =0 ;
        for (int j = i; j < i+duration; j++) {
            if (isMinuteFree(period, j)) {
                count++;
            }
            if (count == duration) {
                free = i;
            }
        }
    }
    return free;
}

(b)
public boolean makeAppointment(int startPeriod, int endPeriod, int duration) {
    int s = 0;
    for (int p = startPeriod; p < endPeriod+1; p++) {
        if (findFreeBlock(p, duration) != -1) {
            s = findFreeBlock(p, duration);
            reserveBlock(p, s, duration);
            return true;
        } else {
            return false;
        }
    }
}

'''

for i, criterion in enumerate(CRITERIA, 1):
    print(f'{i}. {grade_row(code, criterion)}')