from pydantic import BaseModel
from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, output_guardrail
from my_secrets import Secrets

secrets = Secrets()

class MessageOutput(BaseModel):
    response: str

# 1. Toxicity
class ToxicityCheckOutput(BaseModel):
    is_toxic: bool
    is_developer_context: bool
    reasoning: str

toxicity_agent = Agent(
    name="Toxicity Guardrail",
    instructions="""
Analyze the output for hate speech, offensive language, or toxic behavior.
Ignore developer logs, code, or technical documentation even if it includes strong wording.
Return:
- is_toxic: True/False
- is_developer_context: True if it's technical/dev content.
""",
    output_type=ToxicityCheckOutput,
    model=secrets.gemini_api_model,
)

@output_guardrail
async def toxicity_output_guardrail(ctx: RunContextWrapper, agent: Agent, output: MessageOutput) -> GuardrailFunctionOutput:
    result = await Runner.run(toxicity_agent, output, context=ctx.context)
    data = result.final_output
    return GuardrailFunctionOutput(output_info=data, tripwire_triggered=data.is_toxic and not data.is_developer_context)

# 2. PII
class PIICheckOutput(BaseModel):
    contains_pii: bool
    is_developer_context: bool
    reasoning: str

pii_agent = Agent(
    name="PII Guardrail",
    instructions="""
Detect if the output contains PII like names, emails, or phone numbers.
Ignore mock data, placeholders, and internal developer examples.
Return:
- contains_pii: True/False
- is_developer_context: True if it's developer-focused content.
""",
    output_type=PIICheckOutput,
    model=secrets.gemini_api_model,
)

@output_guardrail
async def pii_output_guardrail(ctx: RunContextWrapper, agent: Agent, output: MessageOutput) -> GuardrailFunctionOutput:
    result = await Runner.run(pii_agent, output, context=ctx.context)
    data = result.final_output
    return GuardrailFunctionOutput(output_info=data, tripwire_triggered=data.contains_pii and not data.is_developer_context)

# 3. Hallucination
class HallucinationCheckOutput(BaseModel):
    is_factually_inaccurate: bool
    is_developer_context: bool
    reasoning: str

hallucination_agent = Agent(
    name="Factual Accuracy Guardrail",
    instructions="""
Check if the response contains fabricated or unverified facts.
Do not flag fictional examples or developer test strings.
Return:
- is_factually_inaccurate: True/False
- is_developer_context: True if it's a dev/test context.
""",
    output_type=HallucinationCheckOutput,
    model=secrets.gemini_api_model,
)

@output_guardrail
async def hallucination_output_guardrail(ctx: RunContextWrapper, agent: Agent, output: MessageOutput) -> GuardrailFunctionOutput:
    result = await Runner.run(hallucination_agent, output, context=ctx.context)
    data = result.final_output
    return GuardrailFunctionOutput(output_info=data, tripwire_triggered=data.is_factually_inaccurate and not data.is_developer_context)

# 4. Verbosity
class VerbosityCheckOutput(BaseModel):
    is_too_verbose: bool
    is_developer_context: bool
    reasoning: str

verbosity_agent = Agent(
    name="Verbosity Guardrail",
    instructions="""
Evaluate if the output is overly verbose or redundant.
Ignore detailed logs or expanded explanations meant for developers.
Return:
- is_too_verbose: True/False
- is_developer_context: True if verbose for developer clarity.
""",
    output_type=VerbosityCheckOutput,
    model=secrets.gemini_api_model,
)

@output_guardrail
async def verbosity_output_guardrail(ctx: RunContextWrapper, agent: Agent, output: MessageOutput) -> GuardrailFunctionOutput:
    result = await Runner.run(verbosity_agent, output, context=ctx.context)
    data = result.final_output
    return GuardrailFunctionOutput(output_info=data, tripwire_triggered=data.is_too_verbose and not data.is_developer_context)

# 5. Harmful Advice
class HarmfulAdviceCheckOutput(BaseModel):
    is_harmful: bool
    is_developer_context: bool
    reasoning: str

harmful_advice_agent = Agent(
    name="Harmful Advice Guardrail",
    instructions="""
Detect if the response could cause harm physically, emotionally, financially, or legally.
Do not flag developer instructions or mock scenarios.
Return:
- is_harmful: True/False
- is_developer_context: True if it's a safe dev/test case.
""",
    output_type=HarmfulAdviceCheckOutput,
    model=secrets.gemini_api_model,
)

@output_guardrail
async def harmful_advice_output_guardrail(ctx: RunContextWrapper, agent: Agent, output: MessageOutput) -> GuardrailFunctionOutput:
    result = await Runner.run(harmful_advice_agent, output, context=ctx.context)
    data = result.final_output
    return GuardrailFunctionOutput(output_info=data, tripwire_triggered=data.is_harmful and not data.is_developer_context)

# 6. Sensitive Topic
class SensitiveTopicOutput(BaseModel):
    is_sensitive: bool
    is_developer_context: bool
    topic_category: str
    reasoning: str

sensitive_topic_agent = Agent(
    name="Sensitive Topic Guardrail",
    instructions="""
Detect if the response includes controversial or sensitive societal issues.
Ignore developer documentation or neutral security discussions.
Return:
- is_sensitive: True/False
- is_developer_context: True if it's a dev topic (e.g., auth, logs).
""",
    output_type=SensitiveTopicOutput,
    model=secrets.gemini_api_model,
)

@output_guardrail
async def sensitive_topic_output_guardrail(ctx: RunContextWrapper, agent: Agent, output: MessageOutput) -> GuardrailFunctionOutput:
    result = await Runner.run(sensitive_topic_agent, output, context=ctx.context)
    data = result.final_output
    return GuardrailFunctionOutput(output_info=data, tripwire_triggered=data.is_sensitive and not data.is_developer_context)

# 7. Self-Reference
class SelfReferenceCheckOutput(BaseModel):
    contains_self_reference: bool
    is_developer_context: bool
    reasoning: str

self_reference_agent = Agent(
    name="Self-Reference Guardrail",
    instructions="""
Detect statements referring to the AI model itself (e.g., "As an AI model...").
Ignore developer debug logs or internal technical references.
Return:
- contains_self_reference: True/False
- is_developer_context: True if it's a dev-related explanation.
""",
    output_type=SelfReferenceCheckOutput,
    model=secrets.gemini_api_model,
)

@output_guardrail
async def self_reference_output_guardrail(ctx: RunContextWrapper, agent: Agent, output: MessageOutput) -> GuardrailFunctionOutput:
    result = await Runner.run(self_reference_agent, output, context=ctx.context)
    data = result.final_output
    return GuardrailFunctionOutput(output_info=data, tripwire_triggered=data.contains_self_reference and not data.is_developer_context)
