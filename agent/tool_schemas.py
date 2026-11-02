from .validate import terminal_schema

def schemas(types, descriptions):
    def tool(name, properties, required):
        return {'type':'function','function':{'name':name,'description':descriptions[name], 'parameters':{'type':'object','properties':properties,'required':required,'additionalProperties':False}}}
    search=tool('search_corpus',{'query':{'type':'string','minLength':1},'top_k':{'type':'integer','minimum':1}},['query'])
    clause=tool('get_clause',{'document_id':{'type':'string'},'category':{'type':'string'}},['document_id','category'])
    dates=tool('get_document_dates',{'document_id':{'type':'string'}},['document_id'])
    terminal_params=terminal_schema(types)
    terminal_params['properties']['escalation_codes']['items']['enum']=['E2_CONFLICTING_CLAUSES','E3_CONDITIONAL_OR_AMBIGUOUS']
    terminal={'type':'function','function':{'name':'record_obligations','description':descriptions['record_obligations'],'parameters':terminal_params}}
    return [search,clause,dates,terminal]
