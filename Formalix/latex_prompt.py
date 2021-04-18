import os
import openai
import numpy as np

openai.organization = "org-H4cBZkrQYgaFP4vqmvvL7PCP"
openai.api_key = os.getenv("OPEN_API_KEY")
openai.Engine.list()

trials = 3

primer = """
Write \"4 times (x to the n) minus 2 times (2 to the x)\" as a latex formula:
$4 \\times x^{n} - 2 \\times 2^{x}$

Write \"log of x base 4\" as a latex formula:
$log_{4}({x})$

Write \"partial derivative of the nth root of x wrt x\" as a latex formula:
$\\frac{\\partial}{\\partial x} (\\sqrt[n]{x})$

Write \"derivative of the nth root of x wrt x\" as a latex formula:
$\\frac{d}{dx} (\\sqrt[n]{x})$

"""

#user_input = "3 minus the nth root of x"
#user_input = "partial derivative of f wrt x"
#user_input = "n choose 2"
#user_input = "partial derivative of the nth root of x wrt x"
#user_input = "partial derivative of 4 times x cubed minus y to the 6 wrt x"
#user_input = "3 times (y to the z) plus 7 times (3 to the 4)"
#user_input = "3x over y"
#user_input = "natural logarithm of x"
#user_input = "ln x"
#user_input = "log 4117 base 3"
#user_input = "derivative of f wrt x"
#user_input = "integral of f wrt x"
user_input = "integral from 0 to infinity of f wrt x"

max_tokens = len(user_input)


def logprob_to_prob(logits):
    odds = np.exp(logits)
    return odds / (1 + odds)


def try_instruct_request():
    req_input = primer + "Write \"" + user_input + "\" as a latex formula:\n$"
    result = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt=req_input,
        max_tokens=max_tokens,
        temperature=0.2,
        top_p=1,
        stop="$",
        #frequency_penalty=0.8,
        logprobs=4,
        n=trials)
    return result


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


result = try_instruct_request()

confidence_per_result = compute_confidence_per_result(result)

for i in range(trials):
    print(result['choices'][i]['text'])
    print("GPT-3 returned the result with confidence {}\n".format((confidence_per_result[i])))

best_result = result['choices'][np.argmax(confidence_per_result)]['text']
print(best_result)
