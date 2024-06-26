# GovernmentGPT
_An LLM fine-tuned on the British Commons Parliamentary Hansard to simulate the debate of political topics like members of parliament._

I wanted to see whether I could teach an LLM to do the job of elected British Members of Parliament (MPs) and debate any issue like they do in the House of Commons. You can read my post about that here: xxxxx. This repo contains all code necessary to reproduce the work. 

If you're looking to see an interesting end-to-end example of an LLM fine-tuning pipeline on real-world data, then look no further!

The key parts of the data processing pipeline are described in the following sections:

## Raw Data Extraction
The raw Hansard transcript and speaker data needed to create the training datasets sits in a few places and needs to be processed and linked together, ready to prepare the final training dataset. We only used Hansard data from 1997 onwards because it was easiest to link to the speaker data. The code to do that is here: XXXXXXX.

## Training Dataset Preparation
The code samples 'sequences' of real British Commons Parlimentary Hansard debate transcripts. It attaches the speaker data (eg affiliation, location, additional roles such as committee memberships), and then structures it in a format ready for LLM fine-tuning. It strips dates, MP names and some numeric linking identifiers present in the text to try and avoid the LLM reproducing with bias. There is much more work that can be done to aid generalisability in this regard.

You can download the final prepared JSONL datasets ready for fine-tuning here:
- [100k instances (700mb compressed)](https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/datasets/HansardSequences_100k.big.txt.zip)
- [250k instances (1.7gb compressed)](https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/datasets/HansardSequences_250k.big.txt.zip)

## Fine-tuning
All code for fine-tuning is in this [[link](https://github.com/stewhsource/GovernmentGPT/blob/main/FineTuning/GovernmentGPT_FineTune_Mistral_7b.ipynb)](notebook). You can easily run this on your local machine if it has a GPU, or on Google Colab.

## Inference
You can run the fine-tuned model easily to generate your own debates using this [[link](https://github.com/stewhsource/GovernmentGPT/blob/main/Inference/GovernmentGPT_Inference.ipynb)](notebook). As with fine-tuning, you can easily run this on your local machine if it has a GPU, or on Google Colab.

## Acknowledgements
This work has been made possible through the hard work of others - thank you.


*Parlimentary Hansard data*

We make heavy use of [British Commons Parliamentary Hansard](https://hansard.parliament.uk) data. While this data is openly available to use, a number of individual and organisations have kindly worked hard to make this data more accessible for machine processing:

- [mySociety](https://www.mysociety.org) (eg their data in: https://github.com/mysociety/parlparse/blob/master/members/ministers-2010.json)
- [mySociety TheyWorkForYou](https://www.theyworkforyou.com) - Data APIs and dumps at https://data.theyworkforyou.com
- [Parlparse](https://github.com/mysociety/parlparse) - Extracting structured data from the published Hansard
- [Government datasets](https://www.parliament.uk/business/publications/research/parliament-facts-and-figures/members-of-parliament/)


*LLM*

In this project I used the opensource [Mistral 7B LLM](https://mistral.ai/news/announcing-mistral-7b/). This is a fantastic high-performing 7B LLM that is very amenable to fine-tuning on modest GPU hardware. This means you generally can fine-tune it on lower-memory consumer grade hardware (eg a 24gb RTX 4090) as well as lesser instances in Colab. I used the [mistral-finetune codebase](https://github.com/mistralai/mistral-finetune) to get started with fine-tuning.
