def call_llm(prompt: str) -> dict:
    # TODO: Integrate AWS Bedrock
    return {
        "workload_type": "eks-dev",
        "region": "us-east-1",
        "node_type": "t3.small",
        "node_count": 1,
        "estimated_monthly_cost": 72
    }
