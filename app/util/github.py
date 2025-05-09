import requests
import os, glueops.setup_logging, traceback, json

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logger = glueops.setup_logging.configure(level=LOG_LEVEL)


URL_SUFFIX = os.environ['URL_SUFFIX']

def call_github_workflow(github_dispatch_url: str, workflow_inputs: dict = None):
    """Calls the github user management workflow

    Returns:
        int: status code
    """
    github_token = os.environ["GITHUB_TOKEN"]
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {github_token}", "X-GitHub-Api-Version": "2022-11-28"}
    payload = {"ref": "refs/heads/main"}
    
    if workflow_inputs:
        payload["inputs"] = workflow_inputs
    payload_json = json.dumps(payload)
    response = requests.post(url=github_dispatch_url, data=payload_json, headers=headers)
    logger.info(f"Response code: {response.status_code} Submitting GitHub Workflow to:{github_dispatch_url} with inputs: {workflow_inputs}")
    return response.status_code  

def create_cloud_development_environment(cloud_development_environment_request):
    data = cloud_development_environment_request.dict()
    github_dispatch_url = "https://api.github.com/repos/internal-GlueOps/gha-tools-api/actions/workflows/create-new-cde.yml/dispatches"
    data['url'] = f"https://{data['dns_name']}-{URL_SUFFIX}/?tkn={data['password']}&folder=/workspaces/glueops"
    call_github_workflow(github_dispatch_url, { "CDE_TOKEN": data['password'], "CDE_NAME": data['dns_name']})
    return data['url']