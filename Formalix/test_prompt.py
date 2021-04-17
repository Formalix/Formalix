import os
import openai
import numpy as np

openai.organization = "org-H4cBZkrQYgaFP4vqmvvL7PCP"
openai.api_key = os.getenv("OPEN_API_KEY")
openai.Engine.list()

trials = 3
max_tokens = 64


def logprob_to_prob(logits):
    odds = np.exp(logits)
    return odds / (1 + odds)


def try_instruct_request():
    prompt = "Write a paragraph in academic style that includes the terms "
    user_input = "CM-SAF, SARAH-2 dataset, solar parameters, Meteosat observations, daily means, 30min instantaneous values, 0.05 degree lat/lon resolution"
    result = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt=prompt + user_input + "\n",
        max_tokens=max_tokens,
        temperature=0.3,
        top_p=1,
        # stop="###",
        frequency_penalty=0.8,
        logprobs=4,
        n=trials)
    # logprobs = [result['choices'][i]['logprobs'] for i in range(trials)]
    # print(len(logprobs[0]))
    # print(logprobs[0])
    # print(result)
    return result


desired_result = """
The NASA Prediction Of Worldwide Energy Resources project (POWER) provides plenty of solar and meteorological data sets that can be accessed through a restful API.
The currently available version is its Release 8.
Solar parameters are available from July 1983 onwards, although from different data sources.
"""


def tryRequest():
    prompt = """
    Keywords:
    mt everest 8848m
    india nepal
    ###
    Paragraph:
    Mount Everest has a height of 8848m above sea level and is located in the border region of India and Nepal.
    ###
    Keywords:
    network large device number
    tested with 10, no errors
    50% less power usage
    ###
    Paragraph:
    The network architecture was designed to be used for a large number of devices. We tested it with 10 devices at our lab, during the test, we encountered no errors. This implementation also reduces power consumption by 50% when compared to the previous solution.
    ###
    Keywords:
    oskar bolza
    German mathematician
    calculus of variations
    ###
    Paragraph:
    Oskar Bolza was a German mathematician. He made significant contributions to the field of calculus of variations.
    """

    user_input = """
    oskar bolza
    mathematician
    calculus of variations
    """

    result = openai.Completion.create(
        engine="davinci",
        prompt=prompt + user_input + "\n###\n",
        max_tokens=64,
        temperature=0.3,
        top_p=1,
        stop="###",
        frequency_penalty=0.8,
        # logprobs=2,
        n=3)
    print(result)
    print(result['choices'])


# Calculates how confident GPT-3 is about each response,
# i.e. the average probability of the tokens in each response.
# high value = high probability = high confidence
def compute_confidence_per_result(response, trials=trials, max_tokens=max_tokens):
    token_logprobs = []
    for i in range(trials):
        logprobs_i = np.asarray(result['choices'][i]['logprobs']['token_logprobs'])
        # some results stop before consuming all tokens.
        # fill that up with zeros, so we don't confuse numpy
        logprobs_i.resize(max_tokens)
        token_logprobs.append(logprobs_i)
    logprobs = np.asarray(token_logprobs).reshape(trials, -1)
    # Shouldn't use np.mean(1) here, because that'd include the padding zeros from above
    log_confidence = np.true_divide(logprobs.sum(axis=1), (logprobs != 0).sum(axis=1))
    return logprob_to_prob(log_confidence)


# tryRequest()
result = try_instruct_request()

confidence_per_result = compute_confidence_per_result(result)

for i in range(trials):
    print(result['choices'][i]['text'])
    print("\nGPT-3 returned the result with confidence {}".format((confidence_per_result[i])))
