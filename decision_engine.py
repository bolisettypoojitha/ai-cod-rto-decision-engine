
import json, yaml, joblib, re
import pandas as pd
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CONFIG=yaml.safe_load((ROOT/"config.yaml").read_text())
STATS=json.loads((ROOT/"reference_stats.json").read_text())
MODEL=joblib.load(ROOT/"rto_model.joblib")

def llm_quality_check(name, address):
    """Optional LLM adapter boundary. Uses deterministic fallback if no LLM is configured."""
    text=(name+" "+address).lower()
    suspicious=bool(re.search(r"\b(test|asdf|dummy|fake|xyz|abc)\b", text))
    address_ok=len(address.strip())>=18 and any(ch.isdigit() for ch in address)
    if suspicious:
        return {"name_quality":"suspicious","address_quality":"review","reason":"Name contains a common test/fake placeholder."}
    if not address_ok:
        return {"name_quality":"normal","address_quality":"weak","reason":"Address is short or lacks a house/number signal; confirmation is safer."}
    return {"name_quality":"normal","address_quality":"good","reason":"No obvious placeholder name or weak-address pattern detected."}

def lookup_rate(kind, value):
    return float(STATS.get(kind,{}).get(str(value), STATS["global_rto"]))

def build_features(order):
    prior_orders=float(order.get("customer_prior_orders",0) or 0)
    prior_rto=float(order.get("customer_prior_rto",0) or 0)
    return {
      "order_value":float(order.get("order_value",649) or 649),
      "num_items":float(order.get("num_items",1) or 1),
      "customer_prior_orders":prior_orders,
      "customer_prior_rto_rate":prior_rto/prior_orders if prior_orders else 0,
      "city_prior_rto_rate":lookup_rate("city",order.get("city","")),
      "pincode_prior_rto_rate":lookup_rate("pincode",order.get("pincode","")),
      "courier_prior_rto_rate":lookup_rate("courier",order.get("courier","Xpressbees")),
      "utm_source_prior_rto_rate":lookup_rate("utm_source",order.get("utm_source","direct")),
      "address_len":len(str(order.get("address",""))),
      "name_len":len(str(order.get("customer_name",""))),
      "suspicious_text":int(bool(re.search(r"\b(test|asdf|xyz|dummy|fake|abc)\b",str(order.get("customer_name","")).lower()))),
      "has_phone":int(bool(order.get("phone"))),
      "has_pincode":int(bool(order.get("pincode")))
    }

def decide(order):
    f=build_features(order)
    risk=float(MODEL.predict_proba(pd.DataFrame([f]))[0][1])
    q=llm_quality_check(str(order.get("customer_name","")),str(order.get("address","")))
    t=CONFIG["thresholds"]
    if q["name_quality"]=="suspicious" and risk>=t["confirmation_max"]:
        action="Hold / cancel"
        reason=f"Estimated RTO risk is {risk:.0%} and the customer name looks like a test/placeholder."
    elif risk<t["ship_as_is_max"]:
        action="Ship as-is"
        reason=f"Estimated RTO risk is {risk:.0%}, below the {t['ship_as_is_max']:.0%} low-risk threshold."
    elif risk<t["confirmation_max"]:
        action="Ship after confirmation"
        reason=f"Estimated RTO risk is {risk:.0%}; confirmation adds a safety check without cancelling the sale."
    elif risk<t["prepaid_max"]:
        action="Nudge to prepaid"
        reason=f"Estimated RTO risk is {risk:.0%}; prepaid is cheaper than accepting the COD risk."
    else:
        action="Hold / cancel"
        reason=f"Estimated RTO risk is {risk:.0%}, above the {t['prepaid_max']:.0%} cancellation threshold."
    return {"action":action,"risk_score":risk,"reason":reason,"ai_quality":q,"features":f}
