import json
import random
import re
import os
import sys
import HansardConfig

DEBUG = False

# Parameters for output data  - these are used to control the volume of the training data to make it manageable for the LLM context window.
# Default values are intended for a smallish context window
n_instances = 10000 * 25 # Default to 50k instances
if len(sys.argv) > 1:
    n_instances = int(sys.argv[1].replace("--n_instances=", "").strip())

min_speech_sequence_length = 32
max_speech_sequence_length = 64

max_speech_chars_length = 2000 # Ensure wildly long speeches are not included as they may overflow the usable context window of the LLM (different LLMs may have better or worse performance with long sequences - so we'll leave this for the user to adjust as needed)


#start_speech_output_special_token = "<|start_speech|>"
#start_speech_output_special_token = "<|start_speech|>"
#end_speech_output_special_token = "<|end_speech|>"

# Extract and output debate transcript, ready for LLM training
# A debate transcript is a sequence of Hansard speeches that were made in order on a given day.

# Each speech comprises the elected position of the speaker (eg MP for X),
# any additional roles they hold (eg Chancellor of the Exchequer), and the transcript of their speech.

def display_speech(speech_text, speaker_details):
    """Output the speech in structured text ready for the LLM"""
    output = ""
    output += f"Speaker: {speaker_details['party']} {speaker_details['constituency']}"
    if len(speaker_details["holding_roles"]) > 0:
        output += f" (additional roles: {', '.join(speaker_details['holding_roles'])}.)"

    output += ": \n Speech transcript: "
    output += speech_text.strip().replace('\n', '')

    return output

if __name__ == "__main__":
    # Load the json file into memory
    file_path = f'{HansardConfig.root_path}/1998OnwardsHansardData.big.tsv'

    data = []

    # Load the data in memory (needs 2-3gb of memory, but makes it easy to permute the data for training and testing)
    with (open(file_path) as f):
        lines = f.readlines()
        for line in lines:

            # Debug out
            if DEBUG: print(line)

            cols = line.split("\t")
            day = cols[0]
            speech_id = cols[1]

            if cols[2].endswith("'"):
                cols[2] = cols[2][:-1] # Remove trailing single quote - this was a glitch from early processing that is now fixed in the pipeline
            speaker_details = json.loads(cols[2])

            if cols[3].startswith("'"):
                cols[3] = cols[3][1:] # Remove leading single quote - this was a glitch from early processing that is now fixed in the pipeline

            # Remove numeric reference tags (not entirely sure what these are - but they're just noise to an LLM)
            tag_pattern = "\[[0-9]+\]"
            cols[3] = re.sub(tag_pattern, '', cols[3])
            speech_text = cols[3]

            speech_item = {
                    "day": day,
                    "speech_id": speech_id,
                    "speaker_details": speaker_details,
                    "speech_text": speech_text
                }

            data.append(speech_item)

            # Debug
            if DEBUG: print(display_speech(speech_text, speaker_details))

    # Sample the sequences
    output_sequence_counter = 0

    while (output_sequence_counter < n_instances):

        # Start offset
        start_i = random.randint(0, len(data) - 1)
        sequence_len = random.randint(min_speech_sequence_length, max_speech_sequence_length)
        if (start_i + sequence_len) > len(data) - 1: continue # Skip as rolls over the end of available data

        if DEBUG:
            print(f"data_len: {len(data)}")
            print(f"start_i: {start_i}, sequence_len: {sequence_len}")

        output_sequence = []
        for i in range(0, sequence_len):
            output_sequence.append(data[start_i + i])

        # Verify data constraints
        ignore_sequence = False

        # Ensure same-day debate
        for i in range(0, sequence_len):
            if output_sequence[i-1]["day"] != output_sequence[i]["day"]:
                # Skip output sequence - not all on the same day
                ignore_sequence = True
                break

        # Ensure length of each speech is within max allowed
        for i in range(0, sequence_len):
            if len(output_sequence[i-1]["speech_text"]) > max_speech_chars_length:
                # Skip output sequence - text too long
                ignore_sequence = True
                break

        # Skip this sequence if constraints not met
        if ignore_sequence is True:
            debug_text = ""
            for i in range(0, sequence_len):
                debug_text += f" {len(output_sequence[i-1]['speech_text'])}"

            if DEBUG:
                print(debug_text)
                print("Skipping sequence, constraints not met.")
            continue

        # Prepare output
        def sequence_to_string(output_sequence):
            output_instance = ""

            for output_speech in output_sequence:
                output_instance += (f"{display_speech(output_speech['speech_text'], output_speech['speaker_details'])} \n\n ")

            return output_instance

        output_instance_text = sequence_to_string(output_sequence)

        output_instance_json = {
            "text": output_instance_text
        }

        # Verify json is valid and output
        json_string = json.dumps(output_instance_json)


        def is_json(my_json):
            try:
                json.loads(my_json)
            except ValueError as e:
                return False
            return True

        if is_json(json_string):
            print(json_string)

        output_sequence_counter += 1


