from jsonschema import Draft202012Validator
from .escalation import QUEUES

def terminal_schema(types):
    deadline = {'type':'object','additionalProperties':False,'required':['kind','raw_text'], 'properties': {
      'kind':{'enum':['absolute','relative','recurring','none']}, 'raw_text':{'type':['string','null']},
      'resolved_date':{'type':['string','null']}, 'anchor_event':{'type':['string','null']},
      'offset_days':{'type':['integer','null']}, 'recurring_rule':{'type':['string','null']}}}
    ob = {'type':'object','additionalProperties':False,'required':['type','description','owed_by','clause_category','clause_quote','consequence','deadline','confidence'], 'properties':{
      'type':{'enum':list(types)}, 'description':{'type':'string','minLength':1}, 'owed_by':{'enum':['provider','customer','both','unclear']},
      'clause_category':{'type':'string','minLength':1},'clause_quote':{'type':'string','minLength':1},'consequence':{'type':['string','null']},
      'deadline':deadline, 'confidence':{'type':'number','minimum':0,'maximum':1}}}
    return {'type':'object','additionalProperties':False,'required':['obligations','confidence','escalate','escalation_codes'], 'properties':{
      'obligations':{'type':'array','items':ob}, 'confidence':{'type':'number','minimum':0,'maximum':1},
      'escalate':{'type':'boolean'}, 'escalation_codes':{'type':'array','uniqueItems':True,'items':{'enum':list(QUEUES)}}},
      'allOf':[{'if':{'properties':{'escalate':{'const':True}},'required':['escalate']},'then':{'properties':{'escalation_codes':{'minItems':1}}}},
               {'if':{'properties':{'escalate':{'const':False}},'required':['escalate']},'then':{'properties':{'escalation_codes':{'maxItems':0}}}}]}

def validate_terminal(args, types):
    Draft202012Validator(terminal_schema(types)).validate(args)
