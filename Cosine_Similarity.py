# the inspiration for the topic segmentation algorithm below was taken from the following research paper: 
# http://icsvideos.cs.uh.edu/intro/Topic%20Based%20Segmentation%20of%20Classroom%20Videos.pdf
# Titled: Topic Based Segmentation of Lecture Videos. See section IV, parts B and C, which discuss cosine similarity and text-based indexing algorithms. 
import webvtt as vt
from datetime import datetime, timedelta
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def build_vtt_dict(lecture_transcript):

    # setting up for lecture formatting -> dictionary
    sentence_timestamp = {} # dictionary - {start_time: [sentence, end_time, duration]}

    sentence = ""
    start_time = ""
    end_time = ""

    for caption in vt.read(lecture_transcript):
        if (sentence == ""): # just started the sentence so note down start_time
            start_time = caption.start

        curr_text = caption.text
        sentence += " " + curr_text

        if ("." in curr_text): # if the sentence has ended (we've found a period)
            end_time = caption.end

            # convert start time and end time strings into date time objects 
            start_time, sep, extra = start_time.partition('.')
            end_time, sep, extra = end_time.partition('.')

            start_datetime = datetime.strptime(start_time, '%H:%M:%S')
            end_datetime = datetime.strptime(end_time, '%H:%M:%S')

            # calculate duration of the current sentence
            duration = end_datetime - start_datetime

            sentence_timestamp[start_datetime.time()] = [sentence.lower(), end_datetime.time(), duration]
            sentence = ""

    return sentence_timestamp

def get_transition_points(sentence_timestamp):
    transition_words = ["in this lecture", "and then", "so first", "first", "and in this case", "so this", "so", "now", "for example", "but", "to summarize", "second", "finally", "and", "because", "another", "in terms of", "as a result", "on the other hand", "well", "of course", "now", "however", "or", "in sum", "in summary", "we will be", "we're going", "we are going", "finally", "okay", "so now", "in general", "now in general", "the first", "the second", "next", "last", "as a result", "in this case", "in such a case", "so for example", "in the case of", "again"]
    transition_words = set(transition_words)
    transition_points = []

    for key, value in sentence_timestamp.items():
        sentence = value[0]
        first_four_words = sentence.split()[:4] 
        first_four_words = ' '.join(first_four_words) # first 4 words

        for phrase in transition_words:
            if phrase in first_four_words:
                start_time = key
                transition_points.append(start_time)
                break
    return transition_points

def combine_segments(start_time1, start_time2, sentence_timestamp):
    sentence1, end_time1, duration1 = sentence_timestamp[start_time1]
    sentence2, end_time2, duration2 = sentence_timestamp[start_time2]

    # put all info from second starttime into first
    updated_sentence = sentence1 + sentence2
    updated_end_time = end_time2
    updated_duration = duration1 + duration2
    
    updated_value = [updated_sentence, updated_end_time, updated_duration]
    sentence_timestamp[start_time1] = updated_value
    
    # delete second start time, and
    success = sentence_timestamp.pop(start_time2, None)
   
    return sentence_timestamp


def get_next_segment(start_time, sentence_timestamp):
    for key, value in sentence_timestamp.items():
        if key > start_time:
            return key
    return None

def get_previous_segment(start_time, sentence_timestamp):
    previous_key = None
    for key, value in sentence_timestamp.items():
        if key == start_time:
            return previous_key
        previous_key = key
    return None

def get_smallest_segment(sentence_timestamp): # takes the dictionary of {sentence: [start_time, end_time, duration]} as the parameter
    key_of_smallest_segment = ""
    min_duration = timedelta(10) # 10 days is max duration for comparison purposes 
    for key, value in sentence_timestamp.items():
        duration = value[2]
        if (duration < min_duration):
            min_duration = duration
            key_of_smallest_segment = key
    return key_of_smallest_segment

# lastly, define a function for cosine similarity
# for this function, i used https://www.geeksforgeeks.org/python-measure-similarity-between-two-sentences-using-cosine-similarity/
def cosine_similarity(start_time1, start_time2, sentence_timestamp):
    sentence1, endtime1, duration1 = sentence_timestamp[start_time1]
    sentence2, endtime2, duration2 = sentence_timestamp[start_time2]

    X_list = word_tokenize(sentence1) 
    Y_list = word_tokenize(sentence2)

    sw = stopwords.words('english') 
    l1 =[];l2 =[]

    X_set = {w for w in X_list if not w in sw} 
    Y_set = {w for w in Y_list if not w in sw}

    # form a set containing keywords of both strings 
    rvector = X_set.union(Y_set) 
    for w in rvector:
        if w in X_set: l1.append(1) # create a vector
        else: l1.append(0)
        if w in Y_set: l2.append(1)
        else: l2.append(0)
    c = 0

    # cosine formula 
    for i in range(len(rvector)):
            c+= l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)

    return cosine

def find_lecture_segments(transcript, num_topics):
    lecture_transcript = transcript

    # first, get the lecture in a format that we can work with
    sentence_timestamp = build_vtt_dict(lecture_transcript)

    # second, find the points of transition in the lecture
    transition_points = get_transition_points(sentence_timestamp)
    num_transition_segments = len(transition_points)

    # third, create as many segments as there are transition points
    for i in range(len(transition_points) - 1):
        start_time1 = transition_points[i]
        next_segment_start_time = transition_points[i + 1]

        next_start_time = get_next_segment(start_time1, sentence_timestamp)
        while(next_start_time != None and next_start_time != next_segment_start_time):
            combine_segments(start_time1, next_start_time, sentence_timestamp)
            next_start_time = get_next_segment(next_start_time, sentence_timestamp)

    # fourth, and finally, run text-based indexing algorithm
    num_segments = num_transition_segments


    while (num_segments != num_topics):
        curr_segment = get_smallest_segment(sentence_timestamp)
        prev_segment = get_previous_segment(curr_segment, sentence_timestamp)
        next_segment = get_next_segment(curr_segment, sentence_timestamp)
        if (prev_segment == None and next_segment == None):
            break
        elif (prev_segment == None):
            combine_segments(curr_segment, next_segment, sentence_timestamp)
        elif (next_segment == None):
            combine_segments(prev_segment, curr_segment, sentence_timestamp)
        else:
            sim_with_prev_text = cosine_similarity(curr_segment, prev_segment, sentence_timestamp)
            sim_with_next_text = cosine_similarity(curr_segment, next_segment, sentence_timestamp)

            if (sim_with_prev_text > sim_with_next_text):
                combine_segments(prev_segment, curr_segment, sentence_timestamp)
            else:
                combine_segments(curr_segment, next_segment, sentence_timestamp)

        num_segments -= 1
    
    return sentence_timestamp

# sentence_timestamp = find_lecture_segments("lecture-2-transcript.vtt", 4)

# # check resulting transcript 
# for key, value in sentence_timestamp.items():
#     print(key, ' : ', value)