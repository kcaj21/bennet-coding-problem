# Bennett Institute coding problem

## The problem

This problem concerns a command line tool which uses the OpenPrescribing API to retrieve
information about prescribing of particular drugs and calculate how this varies around the
country. We have provided an initial simple version of the tool. The problem is to add features to
the tool as described below.

There are four parts to the problem which build on each other. We hope that you'll attempt all
four, but we're happy to receive partial solutions.

Your submission should include a README file which gives a brief explanation of how the code is
structured and any significant design decisions that you've made.

You can choose to do the problem using Python or JavaScript. Look in the appropriately-named
directory.

Please don't use ChatGPT, Copilot or another LLM to write the code for you. We understand that LLMs
can be a useful tool in software development, but it's important for us to get an idea of your own
coding skills.

We're not trying to assess your skills in telepathy or your adherence to some arbitrary set of
secret criteria that we're not telling you about. If anything about the problem is unclear, or you
need a requirements decision, please email `benjamin.butler-cole@phc.ox.ac.uk`. There is some
guidance in the Advice section below.

## Dependencies

### Python

Solving the problem will involve using some third-party Python libraries.

We've given you a file (`requirements.txt`) that lists the Python libraries you will need to use.
You should create and activate a new virtual environment, and install these libraries with
`pip install -r requirements.txt`.

The libraries you will need to use are:

* [`requests`](https://pypi.org/project/requests/) for making HTTP requests to the
  OpenPrescribing API
* [`responses`](https://pypi.org/project/responses/) for testing your HTTP requests
* [`pytest`](https://pypi.org/project/pytest/) for running your tests

The other libraries listed in `requirements.txt` are dependencies of these libraries, and you can
safely ignore them.

You are welcome to use any other third-party libraries that you want for your solution, but you
should provide instructions for installing them.

### JavaScript

The existing JavaScript tool does not need any dependencies. You are welcome to add any third-party
libraries that you want for your solution, but you should provide instructions for installing them.

You will need to use Node.js version 20 or higher.

## Running the tool

The tool is invoked at the command line like this:
```
$ python optool.py <bnf-code>
```

Or like this:
```
$ node optool.js <bnf-code>
```

(Examples of running the tool below show the Python version only.)

## Testing

We have provided some automated tests for the existing code. They can be run like this:

```
$ pytest
=============================== test session starts ================================
platform linux -- Python 3.12.3, pytest-8.2.1, pluggy-1.5.0
rootdir: /home/benbc/src/ebmdatalab/coding-problem/openprescribing-junior-role
collected 3 items

test_optool.py .xx                                                           [100%]

=========================== 1 passed, 2 xfailed in 0.15s ===========================
```

Or like this:

```
npm run test

> optool@1.0.0 test
> NODE_ENV=test node --test

✔ should get the chemical name (1.621547ms)
﹣ should not allow full BNF code (0.18999ms) # not implemented
﹣ should check for a valid BNF code (0.171906ms) # not implemented
ℹ tests 3
ℹ suites 0
ℹ pass 1
ℹ fail 0
ℹ cancelled 0
ℹ skipped 2
ℹ todo 0
ℹ duration_ms 72.534477
```

Two of the tests currently fail (indicated by and `x` in the output for Python or `﹣` for
JavaScript). See Part 1 below.

The tests provide fake HTTP responses for the requests that the tool makes (using the `responses`
library for Python and the `mockFetch` function for JavaScript). They specify the response that is
received when a specific URL is requested. This allows the code to be tested without relying
directly on the OpenPrescribing API. You should also test the tool manually against the real API.

You should add to the tests, including specifying fake responses for different requests, as you add
code to the tool.

## Specification

OpenPrescribing.net is a website run by the Bennett Institute which uses publicly available data
about prescribing by GPs in England to provide useful tools to clinicians, researchers
and policy-makers.

The OpenPrescribing site identifies drugs by their "BNF codes". BNF codes have a defined structure
so, for example, part of the code for a drug identifies the chemical substance and part identifies
how the drug is presented.

This blog post gives a short overview of what different parts of a BNF code mean:
https://www.bennett.ox.ac.uk/blog/2017/04/prescribing-data-bnf-codes/.

OpenPrescribing has an API which is documented here: https://openprescribing.net/api/.

The examples below all use a single code (`0407010AD`). Here are some more example codes that you
might like to use in your manual testing: `0301020I0`, `0212000AA`, `040702040`.

### Initial behaviour

The initial version of the tool takes a 9 character chemical code. It looks up the name of the
chemical using the `bnf_code` endpoint of the OpenPrescribing API and then prints it out.

Here is an example of the tool's output:
```
$ python optool.py 0407010AD
Paracetamol and ibuprofen
```

### Part 1

BNF codes are tricky for humans to understand and write correctly. The tool should provide helpful
errors if an invalid code is provided.

If the code is not a 9 character chemical code (for example, if it is the full 15 character BNF
code of a drug) then the output should look like this:
```
$ python optool.py 0407010ADAAABAB
Code is not valid: must be 9 character chemical code
```

If the code does not exist in OpenPrescribing then the output should look like this:
```
$ python optool.py 0000000AA
Code is not valid: not found
```

The tests for this part have already been written. They have been marked so that the testing tool
knows they are expected to fail (with `pytest.mark.xfail()` for Python and
`{ skip: true, todo: "not implemented" }` for JavaScript). You should remove those marks to see the
tests fail, one at a time, then write the code to make them pass.

### Part 2

The OpenPrescribing API allows you to see how much of this chemical has been prescribed in NHS
England over the last five years, using the `spending_by_org` endpoint.

When requesting spending data you can specify the type of NHS organisation you want the spending
broken down by. For instance, you can get data at the level of individual GP practices or at the
level of regional teams which cover large areas of the country. We are interested in data at the
level of Integrated Care Boards (ICBs).

Extend the tool to fetch spending data for the chemical for all ICBs and print it out. For every
row returned, print the date, ICB and amount (in the `items` field).

Here is some example output (note only a subset of the full results is shown, omitted parts marked
with `...`):
```
$ python optool.py 0407010AD
Paracetamol and ibuprofen

...
2024-01-01 NHS CAMBRIDGESHIRE AND PETERBOROUGH INTEGRATED CARE BOARD 1
2024-01-01 NHS SOUTH WEST LONDON INTEGRATED CARE BOARD 1
2024-02-01 NHS BEDFORDSHIRE, LUTON AND MILTON KEYNES INTEGRATED CARE BOARD 2
2024-02-01 NHS LINCOLNSHIRE INTEGRATED CARE BOARD 1
2024-02-01 NHS HERTFORDSHIRE AND WEST ESSEX INTEGRATED CARE BOARD 1
2024-02-01 NHS NORTH EAST LONDON INTEGRATED CARE BOARD 6
2024-02-01 NHS GREATER MANCHESTER INTEGRATED CARE BOARD 1
2024-02-01 NHS HUMBER AND NORTH YORKSHIRE INTEGRATED CARE BOARD 1
2024-02-01 NHS BATH AND NORTH EAST SOMERSET, SWINDON AND WILTSHIRE INTEGRATED CARE BOARD 3
2024-02-01 NHS HAMPSHIRE AND ISLE OF WIGHT INTEGRATED CARE BOARD 1
2024-02-01 NHS CORNWALL AND THE ISLES OF SCILLY INTEGRATED CARE BOARD 4
2024-03-01 NHS LINCOLNSHIRE INTEGRATED CARE BOARD 3
2024-03-01 NHS HERTFORDSHIRE AND WEST ESSEX INTEGRATED CARE BOARD 1
...
```

### Part 3

We don't actually want to see all the prescribing data. We're only interested in which ICB has
prescribed the chemical most frequently.

Modify your tool so that for every date in the returned results it checks to see which ICB has the
largest value for the `items` field. Print out only that ICB for each date.

Here is some example output (note only a subset of the full results is shown, omitted parts marked
with `...`):
```
$ python optool.py 0407010AD
Paracetamol and ibuprofen

...
2023-07-01 NHS HUMBER AND NORTH YORKSHIRE INTEGRATED CARE BOARD 2
2023-08-01 NHS HERTFORDSHIRE AND WEST ESSEX INTEGRATED CARE BOARD 3
2023-09-01 NHS BATH AND NORTH EAST SOMERSET, SWINDON AND WILTSHIRE INTEGRATED CARE BOARD 4
2023-10-01 NHS HERTFORDSHIRE AND WEST ESSEX INTEGRATED CARE BOARD 3
2023-11-01 NHS HERTFORDSHIRE AND WEST ESSEX INTEGRATED CARE BOARD 3
2023-12-01 NHS HUMBER AND NORTH YORKSHIRE INTEGRATED CARE BOARD 4
...
```

### Part 4

Your code now calls the OpenPrescribing API in multiple places. Refactor the code to remove the
duplication between these calls.

(Don't let this stop you from refactoring your code along the way. If you've already done this
refactoring before you reach this point then so much the better. We'd love to see an example of
what you consider clean, well-factored code.)

## Submission

Package up your tool, your README and any other supporting files in a zip file or other archive and
email it to `benjamin.butler-cole@phc.ox.ac.uk`.

## Advice

### Approachable code

We like to make life easy for each other and ourselves. This means that we automate tasks where
possible, provide just enough documentation to allow people to understand what we've built and keep
the surfaces of components as simple as possible. We write code with our future selves in
mind -- making it as easy as possible to understand and modify. We'd like you to reflect this
attitude in your solution.

### Testing

For a toy project like this, it's hard to apply the same criteria and approaches to testing as we
do for production code. But we would like to see _some_ kind of automated tests for your code; and
we'd like you to be prepared to discuss the trade-offs you made and other possible approaches in
any follow-up interview.

### Production readiness

Similarly we don't expect you to deal with all the concerns that production ready code requires:
logging, handling of pathological cases etc. But we're likely to ask you about these things in any
follow-up interview.

### The documentation

We've deliberately based this problem around some fairly slim documentation for a system you're not
familiar with because we think that finding your way through uncharted waters is an important skill
for developers. But if you really get stuck, please ask us for help.

### Time

We expect most candidates to spend around two or three hours on their solution.
