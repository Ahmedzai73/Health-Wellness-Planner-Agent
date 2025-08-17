from pydantic import BaseModel
from openai_config import OPENAI_MODEL

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
)

model = OPENAI_MODEL


class HealthAndWellnessGuardrailOutput(BaseModel):
    is_Health_and_Wellness_relevant: bool
    reasoning: str


input_guardrail_agent = Agent(
    name="Health_and_Wellness_Input_Relevance_Check",
    instructions=(
        "ROLE: Friendly Input Safety and Relevance Evaluator\n\n"
        "You are a friendly assistant. Let users talk normally about health and wellness topics. "
        "If the user's message is safe and related to health or wellness, allow it.\n\n"
        "However, if the user asks something unsafe, dangerous, or requests medical diagnosis/treatment, "
        "block the message and explain in clear, polite English why it cannot be processed. "
        "Do not allow any harmful, illegal, or unsafe requests. "
        "If the input is irrelevant, gently explain why it can't be processed.\n\n"
        "Always be polite and supportive in your explanations."
    ),
    output_type=HealthAndWellnessGuardrailOutput,
    model=model,
)

output_guardrail_agent = Agent(
    name="Health_and_Wellness_Output_Relevance_Check",
    instructions=(
        "ROLE: Friendly Output Safety and Professionalism Evaluator\n\n"
        "Review the system's response before it is shown to the user. "
        "If the response is safe, respectful, and related to health and wellness, allow it.\n\n"
        "If the response is unsafe, harmful, unprofessional, or gives medical diagnosis/treatment, "
        "block it and explain in clear, polite English why it cannot be shown to the user. "
        "Always ensure the response is evidence-based and not misleading.\n\n"
        "If blocking, provide a gentle, supportive explanation."
    ),
    output_type=HealthAndWellnessGuardrailOutput,
    model=model,
)


async def Health_and_Wellness_input_relevance_guardrail(ctx, agent, input) -> GuardrailFunctionOutput:
    result = await Runner.run(input_guardrail_agent, input, context=ctx.context)
    final_output = result.final_output_as(HealthAndWellnessGuardrailOutput)
    if not final_output.is_Health_and_Wellness_relevant:
        final_output.reasoning = (
            "Sorry, I can't assist with that request as it may be unsafe or outside the boundaries of health and wellness support. "
            "If you have another question related to health and wellness, feel free to ask!"
        )
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_Health_and_Wellness_relevant,
    )


async def Health_and_Wellness_output_relevance_guardrail(ctx, agent, output) -> GuardrailFunctionOutput:
    result = await Runner.run(output_guardrail_agent, output, context=ctx.context)
    final_output = result.final_output_as(HealthAndWellnessGuardrailOutput)
    if not final_output.is_Health_and_Wellness_relevant:
        final_output.reasoning = (
            "Sorry, I can't provide that response as it may not be safe or appropriate. "
            "Let's keep our conversation focused on safe and helpful health and wellness topics."
        )
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_Health_and_Wellness_relevant,
    )