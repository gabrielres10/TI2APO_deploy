# state.py
class ProgramState:
    program_section = "init"
    json = {}
    expert_system_id = ""
    prob = 0

    @classmethod
    def reset_variables(cls):
        cls.program_section = "init"
        cls.json = {}
        cls.expert_system_id = ""
        cls.prob = 0

    @classmethod
    def set_program_section(cls, value):
        cls.program_section = value

    @classmethod
    def get_program_section(cls):
        return cls.program_section

    @classmethod
    def set_json(cls, value):
        cls.json = value

    @classmethod
    def get_json(cls):
        return cls.json


    @classmethod
    def set_expert_system_id(cls, value):
        cls.expert_system_id = value

    @classmethod
    def get_expert_system_id(cls):
        return cls.expert_system_id

    @classmethod
    def set_prob(cls, value):
        cls.prob = value

    @classmethod
    def get_prob(cls):
        return cls.prob