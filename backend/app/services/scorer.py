from app.constants import MODEL_A, MODEL_B_1Y, MODEL_B_3Y, RANGES, VERDICTS

# IPO prediction scoring service

def normalise(raw: float, lo: float, hi: float) -> int:
    # Normalize raw prediction to 0-100 score
    score = (raw - lo) / (hi - lo) * 100
    score = max(0, min(100, score))
    return int(score)


def get_verdict(score: int) -> str:
    # Get investment verdict based on score
    for threshold, label in VERDICTS:
        if score >= threshold:
            return label
    return "AVOID"


def compute_short_term(subscription: float, vix: float) -> dict:
    # Compute short-term IPO prediction using subscription and VIX
    contributions = {
        "Subscription": MODEL_A["Subscription"] * subscription,
        "VIX": MODEL_A["VIX"] * vix,
    }

    raw = MODEL_A["intercept"] + sum(contributions.values())
    score = normalise(raw, *RANGES["listing"])
    verdict = get_verdict(score)

    return {
        "mode": "short_term",
        "score": score,
        "predicted_return": raw,
        "predicted_return_percent": round(raw * 100, 2),
        "verdict": verdict,
        "contributions": contributions,
        "inputs_used": {
            "subscription": subscription,
            "vix": vix,
        },
    }


def compute_long_term(roce: float, de_ratio: float) -> dict:
    # Compute long-term IPO prediction using ROCE and D/E ratio
    raw_1y = (
        MODEL_B_1Y["intercept"]
        + MODEL_B_1Y["ROCE"] * roce
        + MODEL_B_1Y["D/E Ratio"] * de_ratio
    )

    raw_3y = (
        MODEL_B_3Y["intercept"]
        + MODEL_B_3Y["ROCE"] * roce
        + MODEL_B_3Y["D/E Ratio"] * de_ratio
    )

    raw = 0.5 * raw_1y + 0.5 * raw_3y
    score = normalise(raw, *RANGES["long_term"])
    verdict = get_verdict(score)

    contributions = {
        "ROCE": (
            MODEL_B_1Y["ROCE"] * roce * 0.5
            + MODEL_B_3Y["ROCE"] * roce * 0.5
        ),
        "D/E Ratio": (
            MODEL_B_1Y["D/E Ratio"] * de_ratio * 0.5
            + MODEL_B_3Y["D/E Ratio"] * de_ratio * 0.5
        ),
    }

    return {
        "mode": "long_term",
        "score": score,
        "predicted_return": raw,
        "predicted_return_percent": round(raw * 100, 2),
        "verdict": verdict,
        "contributions": contributions,
        "inputs_used": {
            "roce": roce,
            "de_ratio": de_ratio,
        },
        "breakdown": {
            "one_year_return": round(raw_1y * 100, 2),
            "three_year_return": round(raw_3y * 100, 2),
        },
    }


def predict(payload: dict) -> dict:
    # Main prediction function that routes to appropriate computation
    mode = payload.get("mode")

    if mode == "short_term":
        subscription = payload.get("subscription")
        vix = payload.get("vix")

        if subscription is None or vix is None:
            raise ValueError("short_term mode requires subscription and vix")

        return compute_short_term(subscription, vix)

    if mode == "long_term":
        roce = payload.get("roce")
        de_ratio = payload.get("de_ratio")

        if roce is None or de_ratio is None:
            raise ValueError("long_term mode requires roce and de_ratio")

        return compute_long_term(roce, de_ratio)

    raise ValueError("Invalid mode")