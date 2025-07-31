import enum

class ChatModel(enum.Enum):
    DEEPSEEK_R1 = "DeepSeek-R1"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    COHERE_COMMAND_R = "Cohere-command-r"
    O1_MINI = "o1-mini"
    O1_PREVIEW = "o1-preview"
    O3_MINI = "o3-mini"
    COHERE_COMMAND_R_PLUS_08_2024 = "Cohere-command-r-plus-08-2024"
    COHERE_COMMAND_R_08_2024 = "Cohere-command-r-08-2024"
    COHERE_COMMAND_R_PLUS = "Cohere-command-r-plus"
    LLAMA_4_MAVERICK = "meta/Llama-4-Maverick-17B-128E-Instruct-FP8"



    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
    
    @classmethod
    def get_all_models(cls):
        return [item.value for item in cls]
    
    @classmethod
    def get_model(cls, model_name):
        for item in cls:
            if model_name == item.value:
                return item
        return None


## how to call this class
# print(ChatModel.DEEPSEEK_R1)
# print(ChatModel.DEEPSEEK_R1.value)
# print(ChatModel.has_value("DeepSeek-R1"))
# print(ChatModel.get_all_models())
# print(ChatModel.get_model("DeepSeek-R1"))
