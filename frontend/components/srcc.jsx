import { useState, useEffect } from "react";
import Toggle from "./toggle.jsx";
import Gauge from "./gauge.jsx";
import Bar_Chart from "./bar_chart.jsx";
const API_BASE = import.meta.env.VITE_API_BASE;
const WS_BASE = import.meta.env.VITE_WS_BASE;

// Component to display prediction results
const ResultCard = ({ mode, result }) => {
  const { score, short, one, three } = result;

  const row = (label, value, isPercent = false) => (
    <div className="flex justify-between">
      <span className="text-[#848E9C] text-sm">{label}</span>
      <span className="text-[#F0B90B] font-medium">
        {value}
        {isPercent ? "%" : ""}
      </span>
    </div>
  );

  return (
    <div className="bg-[#0B0E11]/80 border border-white/10 rounded-2xl p-4 w-64 mb-4">
      {row("Score", score)}

      {mode === 0 ? (
        row("Short Term Return", short, true)
      ) : (
        <>
          {row("1 Year Return", one, true)}
          {row("3 Year Return", three, true)}
        </>
      )}
    </div>
  );
};

export default function Srcc() {
  // IPO prediction component with short/long term modes
  const [mode, setMode] = useState(0);

  const [form, setForm] = useState({
    subscription: "",
    vix: "",
    roce: "",
    de: "", //debt/equity
  });

  const [result, setResult] = useState({
    score: 0,// score of regression model
    short: 0, //short term returns in percent
    one: 0, //one year returns in percent
    three: 0, // three year returns in percent
    contributions: {
      subscription: 20,
      vix: -10,
      roce: 15,
      de: -5,
    },
  });

  const config = {
    0: {
      param1: "subscription",
      param2: "vix",
      label1: "Subscription",
      label2: "VIX",
    },
    1: { param1: "roce", param2: "de", label1: "ROCE(%)", label2: "D/E(%)" },
  };

  const { param1, param2, label1, label2 } = config[mode];

  useEffect(() => {
    setForm({ subscription: "", vix: "", roce: "", de: "" });
  }, [mode]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const getResponse = async () => {
    // Send prediction request to backend
    try {
      console.log("button clicked");

      let payload;

      if (mode === 0) {
        payload = {
          mode: "short_term",
          subscription: Number(form.subscription),
          vix: Number(form.vix),
        };
      } else {
        payload = {
          mode: "long_term",
          roce: Number(form.roce),
          de_ratio: Number(form.de),
        };
      }

      console.log("payload:", payload);

      const res = await fetch(`${API_BASE}/ipo/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      console.log("status:", res.status);

      const data = await res.json();
      console.log("response data:", data);

      if (!res.ok) {
        throw new Error(data.detail || "Error");
      }

      setResult({
        score: data.score,
        short: data.predicted_return_percent,
        one: data.breakdown?.one_year_return || 0,
        three: data.breakdown?.three_year_return || 0,
        contributions: {
          subscription: data.contributions?.Subscription || 0,
          vix: data.contributions?.VIX || 0,
          roce: data.contributions?.ROCE || 0,
          de: data.contributions?.["D/E Ratio"] || 0,
        },
      });
    } catch (err) {
      console.error("getResponse error:", err);
      alert(err.message);
    }
  };

  const inputClass = `
  mt-1 w-full bg-[#0B0E11]/90 text-[#EAECEF]
  px-4 py-3 rounded-2xl border border-[#2B3139]
  hover:border-[#444C56]
  focus:border-[#F0B90B]
  outline-none
`;

  const btnClass = `
  mt-5 py-2 rounded-2xl font-medium text-black
  bg-[#F0B90B]
  hover:bg-[#ffd24d]
  transition
`;

  const cardClass = `
  w-full relative bg-[#111417]/65 backdrop-blur-2xl 
  rounded-3xl p-6 border border-white/10
  overflow-hidden
`;

  const glowLayer1 = `
  absolute inset-0 rounded-3xl pointer-events-none
  bg-gradient-to-b from-white/5 via-transparent to-transparent
`;

  const glowLayer2 = `
  absolute inset-0 rounded-3xl pointer-events-none
  bg-gradient-to-b from-[#F0B90B]/12 via-transparent to-transparent
`;

  return (
    <div className="w-full min-h-screen bg-black flex items-center justify-center p-4">
      <div className={`${cardClass} max-w-6xl w-full`}>
        <div className={glowLayer1}></div>
        <div className={glowLayer2}></div>

        <h2 className="text-[#EAECEF] text-2xl md:text-3xl mb-8">
          Predict Future Returns
        </h2>

        {/* MAIN LAYOUT */}
        <div className="flex flex-col md:flex-row gap-8 md:gap-12 items-center justify-center">
          {/* INPUT SECTION */}
          <div className="w-full max-w-sm md:w-[320px]">
            <Toggle mode={mode} setMode={setMode} />

            <form className="p-4 md:p-6 flex flex-col gap-4">
              <input
                name={param1}
                placeholder={label1}
                value={form[param1]}
                onChange={handleChange}
                className={inputClass}
              />

              <input
                name={param2}
                placeholder={label2}
                value={form[param2]}
                onChange={handleChange}
                className={inputClass}
              />

              <button
                type="button"
                onClick={getResponse}
                disabled={!form[param1] || !form[param2]}
                className={btnClass}
              >
                Get IPO Score
              </button>
            </form>
          </div>

          {/* RESULTS SECTION */}
          <div className="flex-1 w-full flex flex-col items-center gap-12 md:gap-24">
            {/* SCORE + GAUGE */}
            <div className="flex flex-col md:flex-row items-center gap-6 md:gap-24">
              <ResultCard mode={mode} result={result} />
              <Gauge value={result.score} />
            </div>

            {/* BAR CHART */}
            <div className="w-full">
              <Bar_Chart contributions={result.contributions} mode={mode} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
