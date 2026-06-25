# ─────────────────────────────────────────────
# SafeSend — Keyword Engine
# Keywords grouped by weight (how dangerous they are)
# HIGH   = 0.6  (very strong scam signal)
# MEDIUM = 0.3  (suspicious but not certain)
# LOW    = 0.1  (minor indicator)
# ─────────────────────────────────────────────

# HIGH weight — almost always a scam
HIGH_WEIGHT_KEYWORDS = [
    "send pin",
    "send your pin",
    "tuma pin",          # Swahili/Luganda: "send pin"
    "send otp",
    "share your pin",
    "enter your pin",
    "your account is blocked",
    "akaunti imezuiwa",  # Swahili: "account is blocked"
    "account will be closed",
    "reverse the transaction",
    "you have won",
    "umeshinda",         # Swahili: "you have won"
    "call to claim",
    "click to claim",
    "you are a winner",
    "send money to activate",
    "send money to unlock",
]

# MEDIUM weight — suspicious, check further
MEDIUM_WEIGHT_KEYWORDS = [
    "urgent",
    "act now",
    "haraka",            # Swahili: "hurry"
    "jangu mangu",       # Luganda: "come quickly"
    "limited time",
    "verify your account",
    "thibitisha",        # Swahili: "verify"
    "claim your",
    "congratulations",
    "free money",
    "guaranteed",
    "risk free",
    "click here",
    "bonyeza hapa",      # Swahili: "click here"
    "reactivate",
    "suspended",
    "confirm your details",
]

# LOW weight — weak signals, only matter alongside others
LOW_WEIGHT_KEYWORDS = [
    "winner",
    "prize",
    "gift",
    "reward",
    "bonus",
    "offer",
    "pesa",              # Swahili: "money"
    "sente",             # Luganda: "money"
    "foseka",            # Luganda slang
]

# Flat list for simple scan
ALL_KEYWORDS = (
    HIGH_WEIGHT_KEYWORDS +
    MEDIUM_WEIGHT_KEYWORDS +
    LOW_WEIGHT_KEYWORDS
)
