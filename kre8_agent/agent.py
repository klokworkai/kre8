class Kre8Agent:
    """
    Stub agent for kre8.

    This class will later be extended to integrate with AWS Bedrock
    or another LLM provider. For now, it returns deterministic
    placeholder responses so the rest of the pipeline can be built.
    """

    def call_llm(self, prompt: str) -> dict:
        """
        Legacy stub method for pre-baked design/plan-like output.
        Kept for compatibility with the current flow until I2D2 is
        fully switched to the new intent extraction pipeline.
        """
        # TODO: Integrate AWS Bedrock
        return {
            "workload_type": "eks-dev",
            "region": "us-east-1",
            "node_type": "t3.small",
            "node_count": 1,
            "estimated_monthly_cost": 72,
        }

    def extract_intent(self, raw_input: str) -> dict:
        """
        Stub intent extraction method.

        Converts raw natural language input into a StructuredIntent-like
        dictionary. This is a placeholder until real LLM-backed intent
        extraction is implemented.
        """
        return {
            "raw_input": raw_input,
            "goal": "Enable communication between infrastructure components",
            "signals": {},
            "constraints_hint": {},
            "questions": [],
            "confidence": 0.5,
        }