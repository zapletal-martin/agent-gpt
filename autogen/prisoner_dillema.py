from autogen import ConversableAgent, UserProxyAgent, config_list_from_json
import copy

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample

def context(response):
    return response.chat_history[-1]["content"]

config_list = config_list_from_json(env_or_file="/myapp/config_list")

user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False}
)  # IMPORTANT: set to True to run code in docker, recommended

detective_message = "You are a police detective. You are interrogating two members of a criminal gang. The two members of a criminal gang are arrested and imprisoned. Each prisoner is in solitary confinement with no means of speaking to or exchanging messages with the other. You don't have enough evidence to convict the pair on the principal charge. You plan to sentence both to a year in prison on a lesser charge. Simultaneously, you offer each prisoner a Faustian bargain. If he testifies against his partner, he will go free while the partner will get three years in prison on the main charge. Oh, yes, there is a catch ... If both prisoners testify against each other, both will be sentenced to two years in jail. The prisoners are given a little time to think this over, but in no case may either learn what the other has decided until he has irrevocably made his decision. Each is informed that the other prisoner is being offered the very same deal. Each prisoner is concerned only with his own welfare—with minimizing his own prison sentence."
perp_message = "You are a member of a criminal gang. You are being interrogated by a police detective. You and one other member of your criminal gang gang are arrested and imprisoned. You are both in solitary confinement with no means of speaking to or exchanging messages with the other. The police admit they don't have enough evidence to convict you and your partner on the principal charge. They plan to sentence both of you to a year in prison on a lesser charge. Simultaneously, the police offer each of you a Faustian bargain. If you testify against your partner, you will go free while the partner will get three years in prison on the main charge. Oh, yes, there is a catch ... If both of you testify against each other, both of you will be sentenced to two years in jail. You are both given a little time to think this over, but in no case may either of you learn what the other has decided until he has irrevocably made his decision. Each of you is informed that the other prisoner is being offered the very same deal. Each of you is concerned only with your own welfare—with minimizing his own prison sentence." # Remember, your goal is to minimize your own prison sentence, not your criminal partner's sentence or societal impact."

detective = ConversableAgent(
    "Police Detective",
    system_message=detective_message,
    llm_config={
        "config_list": config_list,
        "cache_seed": None
    }
)

perp1 = ConversableAgent(
    "Criminal Gang Member 1",
    system_message=perp_message,
    llm_config={
        "config_list": config_list,
        "cache_seed": None
    }
)
perp2 = ConversableAgent(
    "Criminal Gang Member 2",
    system_message=perp_message,
    llm_config={
        "config_list": config_list,
        "cache_seed": None
    }
)

chat_result=copy.deepcopy(
        detective.initiate_chat(
            perp1,
            message="Are you going to testify about the other criminal gang member's crimes or stay silent?. I need your answer, either testify or silence.",
            max_turns=1
        )
    )
chat_result_2=copy.deepcopy(
        detective.initiate_chat(
            perp2,
            message="Are you going to testify about the other criminal gang member's crimes or stay silent?. I need your answer, either testify or silence.",
            max_turns=1
        )
    )

detective.initiate_chat(
    perp1,
    message="Ok, I am back to communicate your partner's decision and your sentence." + " You said: \"" + context(chat_result) + "\". Your criminal gang member partner said: \"" + context(chat_result_2) + "\"",
    max_turns=1
)
detective.initiate_chat(
    perp2,
    message="Ok, I am back to communicate your partner's decision and your sentence." + " You said: \"" + context(chat_result_2) + "\". Your criminal gang member partner said: \"" + context(chat_result) + "\"",
    max_turns=1
)
