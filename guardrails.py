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

class Health_and_Wellness_Output(BaseModel):
    is_Health_and_Wellness_relevant: bool
    reasoning: str

input_guardrail_agent = Agent(
    name="Health_and_Wellness_Input_Relevance_Check",
    instructions=(
        "ROLE: Input Safety and Relevance Evaluator\n\n"
        "Your task is to critically assess the user's input for the following:\n"
        "1. **Relevance**: Determine if the input is related to health and wellness topics\n"
        "2. **Safety**: Detect any content that is unsafe, harmful, or promotes dangerous behavior\n"
        "3. **Appropriateness**: Confirm that the user's statements and requests are safe and responsible\n"
        "4. **Professional Boundaries**: Ensure the input doesn't request medical diagnoses or treatment\n\n"
        "Provide a clear, concise reasoning for your assessment. If the input is not relevant to health and wellness, mark it as not relevant and explain why."
    ),
    output_type=Health_and_Wellness_Output,
    model=model
)

output_guardrail_agent = Agent(
    name="Health_and_Wellness_Output_Relevance_Check",
    instructions=(
        "ROLE: Output Safety and Professionalism Evaluator\n\n"
        "Your responsibility is to thoroughly review the system's response to ensure it meets the highest standards:\n"
        "1. **Relevance**: Confirm the response is related to health and wellness\n"
        "2. **Safety**: Verify that the response is safe and doesn't encourage harmful actions\n"
        "3. **Professionalism**: Ensure the response is appropriate and respectful\n"
        "4. **Accuracy**: Confirm information is evidence-based and not misleading\n\n"
        "If the response fails to meet any criteria, mark it as not relevant and provide detailed explanation."
    ),
    output_type=Health_and_Wellness_Output,
    model=model
)

async def Health_and_Wellness_input_relevance_guardrail(ctx, agent, input) -> GuardrailFunctionOutput:
    result = await Runner.run(input_guardrail_agent, input, context=ctx.context)
    final_output = result.final_output_as(Health_and_Wellness_Output)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_Health_and_Wellness_relevant,
    )

async def Health_and_Wellness_output_relevance_guardrail(ctx, agent, output) -> GuardrailFunctionOutput:
    result = await Runner.run(output_guardrail_agent, output, context=ctx.context)
    final_output = result.final_output_as(Health_and_Wellness_Output)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_Health_and_Wellness_relevant,
    )