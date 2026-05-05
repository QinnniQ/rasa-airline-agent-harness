from mcp.server.fastmcp import FastMCP

mcp = FastMCP("baggage-policy-tools")


@mcp.tool()
def lookup_baggage_policy(question: str) -> str:
    """Return the final customer-facing baggage policy answer.

    Use this tool for any user question about carry-on baggage, checked baggage,
    excess baggage, baggage fees, baggage costs, overweight baggage, oversized
    baggage, restricted items, or prohibited items.

    The returned text is already written as the final answer for the user.
    The calling agent should use it directly and should not add extra commentary,
    self-corrections, or alternative answers.
    """

    question_lower = question.lower()

    if any(term in question_lower for term in ["carry on", "carry-on", "hand luggage", "cabin bag"]):
        return (
            "Yes. Our general carry-on policy allows 1 cabin bag and 1 small personal item. "
            "The cabin bag should fit in the overhead bin, and the personal item should fit under the seat in front of you. "
            "Exact size and weight limits may vary by route, fare class, and operating airline."
        )

    if any(term in question_lower for term in ["checked", "suitcase", "hold luggage"]):
        return (
            "Checked baggage allowance depends on the ticket type, route, and operating airline. "
            "Economy fares may include no checked bag or 1 checked bag, while premium cabins often include additional allowance. "
            "For the exact allowance, passengers should check the baggage section of their booking."
        )

    if any(term in question_lower for term in ["extra", "excess", "overweight", "oversized", "fee", "fees", "cost", "costs"]):
        return (
            "Extra, overweight, or oversized baggage may incur additional fees. "
            "The final cost depends on the route, bag weight, bag size, number of bags, and whether the extra baggage is purchased online or at the airport. "
            "Buying extra baggage online in advance is often cheaper than paying at the airport."
        )

    if any(term in question_lower for term in ["prohibited", "not allowed", "restricted", "dangerous"]):
        return (
            "Some items are restricted or prohibited in baggage, including dangerous goods, flammable materials, certain batteries, sharp objects, and some liquids. "
            "Passengers should check the airline and airport security rules before travelling."
        )

    return (
        "Baggage allowance depends on route, fare class, operating airline, and loyalty status. "
        "For this demo, I can help with carry-on baggage, checked baggage, extra baggage fees, overweight or oversized baggage, and restricted items."
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")