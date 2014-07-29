from test_api import scenarios as s
from test_api.helpers.voicemail import generate_voicemail


REQUIRED = ['name', 'number', 'context']

BOGUS = [
    ('name', 123, 'unicode string'),
    ('number', 123, 'unicode string'),
    ('context', 123, 'unicode string'),
    ('password', 123, 'unicode string'),
    ('email', 123, 'unicode string'),
    ('language', 123, 'unicode string'),
    ('timezone', 123, 'unicode string'),
    ('max_messages', '3', 'integer'),
    ('attach_audio', 'true', 'boolean'),
    ('delete_messages', 'false', 'boolean'),
    ('ask_password', 'true', 'boolean')
]


class TestVoicemailResource(s.GetScenarios, s.CreateScenarios, s.EditScenarios, s.DeleteScenarios):

    url = "/voicemails"
    resource = "Voicemail"
    required = REQUIRED
    bogus_fields = BOGUS

    def create_resource(self):
        voicemail = generate_voicemail()
        return voicemail['id']
