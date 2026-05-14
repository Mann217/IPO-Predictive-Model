# Model coefficients and constants for IPO prediction

MODEL_A = {
    "intercept": 0.21058,
    "Subscription": 0.00453,
    "VIX": -0.00851,
}

MODEL_B_1Y = {
    "intercept": -0.03621,
    "ROCE": 0.03786,
    "D/E Ratio": 0.28618,
}

MODEL_B_3Y = {
    "intercept": 0.7859,
    "ROCE": 0.06674,
    "D/E Ratio": 0.50757,
}

# Expected return ranges for different prediction modes
RANGES = {
    "listing": (-0.15, 0.60),
    "long_term": (-0.20, 2.50),
}

# Verdict thresholds and labels
VERDICTS = [
    (80, "STRONG BUY"),
    (65, "BUY"),
    (50, "MODERATE"),
    (35, "WEAK"),
    (0, "AVOID"),
]