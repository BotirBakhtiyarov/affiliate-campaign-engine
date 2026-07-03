import streamlit as st


def render_brief_form() -> tuple[dict[str, str], bool]:
    """Render the campaign brief form and return the brief dict plus completion flag."""
    st.header("📝 Campaign Brief")

    with st.form("brief_form"):
        product_name = st.text_input("Product Name *", value="")
        description = st.text_area("Product Description *", height=100)
        col1, col2 = st.columns(2)
        with col1:
            price = st.text_input("Price *")
            commission_rate = st.text_input("Commission Rate *", placeholder="e.g. 30%")
            campaign_duration = st.text_input("Campaign Duration *", placeholder="e.g. 14 days")
        with col2:
            audience = st.text_input("Target Audience *")
            promo_code = st.text_input("Promo Code")
            competitor_notes = st.text_area("Competitor Notes (optional)", height=68)
        unique_selling_points = st.text_area("Unique Selling Points *", height=80)

        submitted = st.form_submit_button("🔍 Analyze Brief")

    brief = {
        "product_name": product_name.strip(),
        "description": description.strip(),
        "price": price.strip(),
        "audience": audience.strip(),
        "commission_rate": commission_rate.strip(),
        "promo_code": promo_code.strip(),
        "campaign_duration": campaign_duration.strip(),
        "unique_selling_points": unique_selling_points.strip(),
        "competitor_notes": competitor_notes.strip(),
    }

    required_fields = ["product_name", "description", "price", "audience", "commission_rate", "campaign_duration", "unique_selling_points"]
    is_complete = all(brief[field].strip() for field in required_fields)

    if submitted and not is_complete:
        st.error("Please fill in all required fields.")

    return brief, submitted and is_complete
