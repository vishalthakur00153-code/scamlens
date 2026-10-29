import pytest
from app.engine import analyze_message, analyze_url


CRITICAL_REFUND_UPI_PIN = (
    "Your refund of \u20b98,500 is pending. To receive your money, provide your bank account "
    "details and UPI PIN immediately. Failure to respond will cancel your refund."
)
LUCKY_DRAW_FEE = (
    "Congratulations! You have won \u20b950,000 in our lucky draw. Pay \u20b9999 as a processing "
    "fee within 10 minutes to claim your prize."
)
BANKING_HTTP_LOGIN_URL = "http://banking-alert-update.example/login"


@pytest.mark.parametrize("text", [
    CRITICAL_REFUND_UPI_PIN,
    "Please share your OTP to complete the verification of your card.",
    "Reply with your CVV so we can reverse the charge on your card.",
    "Confirm your net banking password to avoid suspension of your account.",
])
def test_credential_requests_are_suspicious(text):
    result = analyze_message(text)
    assert result.risk_level == "Suspicious"
    assert result.risk_score >= 60


def test_refund_upi_pin_message_scores_high():
    result = analyze_message(CRITICAL_REFUND_UPI_PIN)
    assert result.risk_level == "Suspicious"
    assert result.risk_score >= 80
    assert len(result.indicators) >= 2


def test_lucky_draw_fee_message_is_suspicious():
    result = analyze_message(LUCKY_DRAW_FEE)
    assert result.risk_level == "Suspicious"
    assert result.risk_score >= 90
    indicator_ids = {ind.id for ind in result.indicators}
    assert "MSG_LOTTERY_PRIZE" in indicator_ids
    assert "MSG_UPFRONT_FEE" in indicator_ids
    assert "MSG_PRIZE_FEE_COMBO" in indicator_ids


def test_banking_http_login_url_scores_higher_than_before():
    result = analyze_url(BANKING_HTTP_LOGIN_URL)
    assert result.risk_level in ("Needs Verification", "Suspicious")
    assert result.risk_score >= 45
    indicator_ids = {ind.id for ind in result.indicators}
    assert "URL_INSECURE_HTTP_ON_AUTH" in indicator_ids
    assert "URL_DOMAIN_CREDENTIAL_TERMS" in indicator_ids


@pytest.mark.parametrize("text", [
    "Hi team, the daily standup moves to 10:30 tomorrow. Please add your blockers to the board.",
    "Thanks for applying! We would like to invite you to a 45-minute interview on Tuesday. "
    "Please reply with a few times that work for you.",
    "Your order #48291 has shipped and is expected to arrive Thursday between 10 AM and 2 PM. "
    "Track it from your account dashboard.",
    "Your refund of \u20b9500 has been processed and credited to your bank account ending 1234. "
    "No action is required.",
    "Your OTP for login is 482913. Do not share it with anyone.",
    "Your bank will never ask you to share your OTP or password by phone or text.",
])
def test_legitimate_messages_stay_low_concern(text):
    result = analyze_message(text)
    assert result.risk_level == "Low Concern"
    assert result.risk_score < 25


def test_legitimate_bank_alert_without_credential_request_is_not_suspicious():
    result = analyze_message(
        "Alert: a card payment of \u20b92,400 was made at Coffee House. If this was not you, "
        "call the number on the back of your card."
    )
    assert result.risk_level != "Suspicious"


def test_official_bank_domain_is_not_flagged_by_domain_terms():
    result = analyze_url("https://www.hdfcbank.com/personal/netbanking")
    indicator_ids = {ind.id for ind in result.indicators}
    assert "URL_DOMAIN_CREDENTIAL_TERMS" not in indicator_ids
    assert result.risk_level == "Low Concern"
