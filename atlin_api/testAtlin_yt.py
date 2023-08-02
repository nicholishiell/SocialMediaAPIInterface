from AtlinAPI import JobStatus, JobPlatform, AtlinYoutube, YoutubeToken
from AtlinAPI import YoutubeJobDetails
from AtlinAPI import Job
import pprint

import json

job_status = JobStatus()
job_platform = JobPlatform()

# valid values from test database
user_uid = "b1d93700-aee5-4eca-939d-cf8b866f2be4"
# job_uid = "9ef8b11b-0d51-4303-ada0-111ed9f6fbaa"



atlin = AtlinYoutube("http://localhost:6010")


#Create a token
def create_youtube_token(user_uid, token_name, api_token, token_quota):
    token_yt = YoutubeToken()
    token_yt.user_uid = user_uid
    token_yt.token_name = token_name

    token_details_yt = dict(
        api_token = api_token,
        token_quota = token_quota,
        modify_date = "",
    )

    token_yt.token_detail = token_details_yt
    print(token_yt.to_json())

    response = atlin.token_create(token_yt.token_uid, token_yt.to_dict())
    if response.status_code == 201:
        token_yt.from_json(response.json())
        print(token_yt.to_dict())
    else:
        raise response.raise_for_status()

    return response.status_code

create_youtube_token(user_uid=user_uid, token_name="scrapper1", api_token="", token_quota=0)


def get_token(user_uid=None, token_uid=None, social_platform=None):
    if user_uid:
        response = atlin.token_get(user_uid=user_uid)
        if response:
            print(f"returned {len(response.json())} tokens for user {user_uid}")
        response.raise_for_status()

    if token_uid:
        response = atlin.token_get(token_uid=token_uid)
        if response:
            print(f"returned token for id {token_uid}\n{response.json()}")
        response.raise_for_status()

    if social_platform:
        response = atlin.token_get(social_platform=social_platform)
        if response:
            print(f"got {len(response.json())} tokens for social_platform 'YOUTUBE'")
        response.raise_for_status()


#get_token(user_uid=user_uid)
#get_token(token_uid='1574d0b4-36b1-4137-a679-cc79503035ea')

# PUT - set quota
token_uid = '1574d0b4-36b1-4137-a679-cc79503035ea'
#response = atlin.token_set_quota(token_uid, job_platform.youtube, 0)
#response.raise_for_status()
#get_token(token_uid='1574d0b4-36b1-4137-a679-cc79503035ea')


# POST create a job
def create_sample_playlist_job():
    youtube_job_details = YoutubeJobDetails()
    youtube_job_details.job_submit.actions=["COMMENTS"]
    youtube_job_details.job_submit.option_type="PLAYLIST"
    youtube_job_details.job_submit.option_value="https://www.youtube.com/playlist?list=PLADighMnAG4DczAOY7i6-nJhB9sQDhIoR"

    response = atlin.job_create(
        user_uid=user_uid,
        token_uid=token_uid,
        job_status=job_status.created,
        social_platform=job_platform.youtube,
        job_tag=["tag1", "tag2"],
        job_detail=youtube_job_details.to_dict(),
        # token_uid,
        # job_status.created,
        # job_platform.youtube,
    )
    if response:
        print(f"Job with uid {response.json()['job_uid']} created.")
        print(json.dumps(response.json(), indent=2))
        job = Job(response.json())
    response.raise_for_status()


def create_sample_query_job():
    youtube_job_details = YoutubeJobDetails()
    youtube_job_details.job_submit.actions=["METADATA"]
    youtube_job_details.job_submit.option_type="QUERY"
    youtube_job_details.job_submit.option_value="ottawa lrt"
    youtube_job_details.job_submit.video_count = 50

    response = atlin.job_create(
        user_uid=user_uid,
        token_uid=token_uid,
        job_status=job_status.created,
        social_platform=job_platform.youtube,
        job_tag=["tag1", "tag2"],
        job_detail=youtube_job_details.to_dict(),
        # token_uid,
        # job_status.created,
        # job_platform.youtube,
    )
    if response:
        print(f"Job with uid {response.json()['job_uid']} created.")
        print(json.dumps(response.json(), indent=2))
        job = Job(response.json())
    response.raise_for_status()

#create_sample_query_job()

def extract_jobs(response):
    jobs = []
    if response.status_code == 200:
        jobs = response.json()
    return jobs

def print_jobs(jobs):
    for job in jobs:
        pprint.pprint(json.dumps(job, indent=2))

#job_uid = "706ae95f-cd46-4b29-a9bd-40e0ab6ba3b6"
#response = atlin.job_get_by_uid(job_uid)
#response.raise_for_status()

#print_jobs(extract_jobs(response))

#my_job = Job(response.json())
#def modify_job_details(job_uid, job):
#    youtube_job_details = YoutubeJobDetails()
#    youtube_job_details.job_submit.actions = ["METADATA"]
#    youtube_job_details.job_submit.option_type = "VIDEO"
#    youtube_job_details.job_submit.option_value = "https://www.youtube.com/watch?v=3l0xWPPwmws"

#    job.job_detail = youtube_job_details.to_dict()

#    atlin.job_update(job_uid, job.to_dict())

#modify_job_details(job_uid,my_job)

print ("\nJOB INFO================================================================ \n")

def print_job(job_uid):
    response = atlin.job_get_by_uid(job_uid)
    response.raise_for_status()
    print_jobs(extract_jobs(response))

job_uid = "4d8605d5-6b85-4f6c-a89a-c3d96f2cb908"
#response = atlin.job_get_by_uid(job_uid)"
print_job(job_uid)

print ("\nTOKEN INFO================================================================ \n")
token_uid="1574d0b4-36b1-4137-a679-cc79503035ea"
response = atlin.token_get(token_uid=token_uid)
if response.status_code == 200:
    try:
        pprint.pprint(response.json())
    except Exception as e:
        print(f"Could not fetch token quota. {e}")
response.raise_for_status()

if False:

    token_yt.token_name = "New token name"
    response = atlin.token_update(token_yt.token_uid, token_yt.to_dict())
    if response.ok:
        token_yt.from_json(response.json())
        print(f"Token name updated to '{token_yt.token_name}'")
    response.raise_for_status()

    # Example of token deletion at the end.

    response = atlin.token_set_quota(token_yt.token_uid, token_yt.social_platform, 9213)
    if response:
        print(response.json())
    response.raise_for_status()


    def extract_jobs(response):
        jobs = []
        if response.status_code == 200:
            jobs = response.json()
        return jobs


    def print_jobs(jobs):
        for job in jobs:
            print(json.dumps(job, indent=2))


    # POST create a job
    youtube_job_details = YoutubeJobDetails()

    response = atlin.job_create(
        user_uid=user_uid,
        token_uid=token_yt.token_uid,
        job_status=job_status.created,
        social_platform=job_platform.youtube,
        job_tag=["tag1", "tag2"],
        job_detail=youtube_job_details.to_dict(),
        # token_uid,
        # job_status.created,
        # job_platform.youtube,
    )
    if response:
        print(f"Job with uid {response.json()['job_uid']} created.")
        print(json.dumps(response.json(), indent=2))
        job = Job(response.json())
    response.raise_for_status()

    # GET all the jobs in the database .
    response = atlin.job_get()
    print_jobs(extract_jobs(response))
    response.raise_for_status()

    # GET only jobs with job_status = "CREATED"
    response = atlin.job_get(job_status=[job_status.created])
    print_jobs(extract_jobs(response))
    response.raise_for_status()

    # GET only jobs with job_status = "CREATED" or "PAUSED"
    response = atlin.job_get(job_status=[job_status.created, job_status.paused])
    print_jobs(extract_jobs(response))
    jobs = extract_jobs(response)
    response.raise_for_status()

    # GET job  by job_uid
    # http://localhost:6010/api/v1/job/9978d901-96e6-4a80-bfec-3a7dd87d81ad
    response = atlin.job_get_by_uid(jobs[0]['job_uid'])
    response.raise_for_status()

    print_jobs(extract_jobs(response))

    job = Job(response.json())

    # PUT - update the status of a job to running
    response = atlin.job_set_status(job.job_uid, job_status.running)
    job.from_json(response.json())
    response.raise_for_status()

    # GET - get quota
    response = atlin.token_get(job.token_uid)
    if response.status_code == 200:
        try:
            quota = response.json()['token_detail']['token_quota']
        except Exception as e:
            print(f"Could not fetch token quota. {e}")
    response.raise_for_status()

    # PUT - set quota
    response = atlin.token_set_quota(job.token_uid, job.social_platform, 300)
    response.raise_for_status()

    response = atlin.token_delete(job.token_uid)
    if response:
        print(f"Deleted token with token id {token_yt.token_uid}")
    response.raise_for_status()

    # DEL - delete a job
    response = atlin.job_delete(job.job_uid)
    if response:
        print(f"Deleted job with job_uid '{job.job_uid}'")
    response.raise_for_status()

    pass