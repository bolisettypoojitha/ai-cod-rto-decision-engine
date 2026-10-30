
import streamlit as st
from decision_engine import decide, CONFIG

st.set_page_config(page_title="COD RTO Decision Engine", layout="wide")
st.title("COD RTO Decision Engine")
st.caption("Take-home prototype • configurable thresholds • AI-assisted address/name review")

tab1, tab2, tab3 = st.tabs(["Decision engine","WhatsApp simulator","Founder dashboard"])

with tab1:
    st.subheader("Score a new COD order")
    c1,c2=st.columns(2)
    with c1:
        name=st.text_input("Customer name","Lakshmi Shaikh")
        phone=st.text_input("Phone","6007018646")
        address=st.text_area("Address","399/13, Station Nagar, Opp. Railway Crossing")
        city=st.text_input("City","Chennai")
        pincode=st.text_input("Pincode","600092")
        order_value=st.number_input("Order value (₹)",100,10000,649)
    with c2:
        items=st.number_input("Number of items",1,20,1)
        prior_orders=st.number_input("Previous orders",0,50,0)
        prior_rto=st.number_input("Previous RTOs",0,50,0)
        source=st.selectbox("Acquisition source",["direct","meta_ads","google_ads"])
        courier=st.selectbox("Courier",["Delhivery","Xpressbees","Ecom Express","BlueDart"])
    if st.button("Evaluate order",type="primary"):
        result=decide({"customer_name":name,"phone":phone,"address":address,"city":city,
                       "pincode":pincode,"order_value":order_value,"num_items":items,
                       "customer_prior_orders":prior_orders,"customer_prior_rto":prior_rto,
                       "utm_source":source,"courier":courier})
        st.metric("Estimated RTO risk",f"{result['risk_score']:.1%}")
        st.success(result["action"])
        st.write("**Reason:**",result["reason"])
        st.info("AI quality check: "+result["ai_quality"]["reason"])

with tab2:
    st.subheader("Mock WhatsApp flow")
    st.write("Select an action and simulate the customer's reply.")
    action=st.selectbox("Action",["Ship after confirmation","Nudge to prepaid"])
    if action=="Ship after confirmation":
        st.code("""Hi Lakshmi 👋\nYour order #KT100193 for ₹649 is ready to ship.\nReply YES to confirm or NO to cancel. We’ll hold it for 24 hours.""")
        reply=st.selectbox("Customer reply",["YES","NO","Something random","No reply after 24h"])
        if reply=="YES": st.success("Confirmed → ship the order.")
        elif reply=="NO": st.warning("Cancelled → do not ship.")
        elif reply=="Something random": st.info("Send one clarification message; if still unclear, hold/cancel after 24h.")
        else: st.warning("24 hours passed → hold/cancel.")
    else:
        st.code("""Hi Lakshmi 👋\nPay online and get ₹30 OFF your ₹649 order.\nPrepaid price: ₹619.\nReply PAY to switch to prepaid or COD to keep Cash on Delivery.""")
        reply=st.selectbox("Customer reply",["PAY","COD","Something random","No reply after 24h"])
        if reply=="PAY": st.success("Generate payment link → prepaid → ship.")
        elif reply=="COD": st.success("Keep COD → continue with risk policy.")
        elif reply=="Something random": st.info("Clarify once; preserve the original COD option.")
        else: st.info("No response → continue original risk policy; do not silently cancel.")

with tab3:
    st.subheader("Founder dashboard")
    st.write("Use `last_month_policy_buckets.csv` generated from the supplied dataset for the historical policy simulation.")
    import pandas as pd, json
    buckets=pd.read_csv("last_month_policy_buckets.csv")
    st.dataframe(buckets,use_container_width=True)
    m=json.load(open("metrics.json"))["metrics"]
    a,b,c=st.columns(3)
    a.metric("Estimated RTO cost avoided",f"₹{m['estimated_avoided_rto_cost']:,.0f}")
    b.metric("Estimated genuine-cancel loss",f"₹{m['estimated_genuine_cancel_loss']:,.0f}")
    c.metric("Net estimated impact",f"₹{m['net_impact']:,.0f}")
    st.caption("Historical impact uses explicit conservative assumptions in config.yaml; it is not presented as observed causal uplift.")
