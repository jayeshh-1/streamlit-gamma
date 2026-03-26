import streamlit as st
from PIL import Image
import os

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Microstructure of 0DTE | Quant Research",
    page_icon="line_chart",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a stark, academic, highly readable institutional whitepaper
st.markdown("""
    <style>
    /* Main container width and font stack */
    .main { max-width: 1050px; margin: 0 auto; font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    
    /* Typography Upgrades for Maximum Readability (Perfectly Balanced) */
    h1 { text-align: center; font-size: 3.0rem !important; font-weight: 900 !important; margin-bottom: 0.5rem !important; line-height: 1.25 !important; color: var(--text-color) !important; opacity: 0.95 !important; letter-spacing: -0.02em !important; }
    .subtitle { text-align: center; font-size: 1.3rem !important; color: var(--text-color) !important; opacity: 0.75 !important; font-style: italic !important; margin-bottom: 1.8rem !important; font-weight: 400 !important; }
    
    /* Elegant section spacing */
    h2 { font-weight: 800 !important; font-size: 2.2rem !important; margin-top: 2.8rem !important; border-bottom: 1px solid rgba(128, 128, 128, 0.2) !important; padding-bottom: 0.5rem !important; margin-bottom: 1.5rem !important; color: var(--text-color) !important; opacity: 0.95 !important; letter-spacing: -0.01em !important; }
    h3 { font-weight: 700 !important; font-size: 1.6rem !important; margin-top: 2rem !important; margin-bottom: 1rem !important; color: var(--text-color) !important; opacity: 0.95 !important; }
    
    /* Perfectly scaled body text (1.25rem is the sweet spot for long-form reading) */
    div[data-testid="stMarkdownContainer"] p, 
    div[data-testid="stMarkdownContainer"] li { 
        font-size: 1.25rem !important; 
        line-height: 1.6 !important; 
        font-weight: 400 !important; 
        color: var(--text-color) !important; 
        opacity: 0.9 !important; 
    } 
    div[data-testid="stMarkdownContainer"] strong { font-weight: 700 !important; color: var(--text-color) !important; opacity: 1 !important; }
    
    /* Elegant blockquotes instead of tinted background boxes */
    .callout { 
        border-left: 5px solid #3B82F6 !important; 
        padding-left: 1.25rem !important; 
        margin: 1.4rem 0 !important; 
        color: var(--text-color) !important; 
        font-size: 1.25rem !important; 
        background-color: transparent !important;
    }
    
    .quant-note { 
        border-left: 5px solid #10B981 !important; 
        padding-left: 1.25rem !important; 
        margin: 2rem 0 !important; 
        font-family: 'Courier New', Courier, monospace !important; 
        color: var(--text-color) !important; 
        font-size: 1.15rem !important;
        background-color: transparent !important;
    }
    
    .limitation-note {
        border-left: 5px solid #F59E0B !important; 
        padding-left: 1.25rem !important; 
        margin: 2rem 0 !important; 
        color: var(--text-color) !important; 
        font-size: 1.25rem !important;
        background-color: transparent !important;
    }
    
    /* Premium Regime Cards for Section 5 */
    .regime-card {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.15) !important;
        border-radius: 8px !important;
        padding: 18px 22px !important;
        margin: 15px 0 !important;
        height: 100% !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
    }
    .regime-pin { border-top: 5px solid #3B82F6 !important; }
    .regime-break { border-top: 5px solid #EF4444 !important; }
    
    /* Custom Stat Boxes for KPI framing */
    .stat-box {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-radius: 8px !important;
        padding: 20px 15px !important;
        text-align: center !important;
        margin-bottom: 20px !important;
    }
    
    .insight-box {
    border-left: 5px solid #8B5CF6 !important;
    padding-left: 1.25rem !important;
    margin: 1.4rem 0 !important;
    font-size: 1.25rem !important;
    }
    
    .stat-value { font-size: 2.4rem !important; font-weight: 800 !important; color: #3B82F6 !important; margin-bottom: 6px !important; line-height: 1 !important;}
    .stat-label { font-size: 0.95rem !important; font-weight: 600 !important; color: var(--text-color) !important; opacity: 0.7 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important;}
    
    /* Table of Contents Links */
    .toc-link { text-decoration: none !important; font-size: 1rem !important; display: block !important; padding: 6px 0 !important; font-weight: 500 !important; color: var(--text-color) !important; opacity: 0.85 !important; transition: all 0.2s ease-in-out !important; }
    .toc-link:hover { color: #3B82F6 !important; opacity: 1 !important; }
    
    /* Image Styling */
    img { border-radius: 6px !important; border: 1px solid rgba(128, 128, 128, 0.15) !important; margin-bottom: 8px !important; }
    </style>
    
    
""", unsafe_allow_html=True)



# Helper function to load images safely
def load_image(image_name):
    try:
        return Image.open(image_name)
    except FileNotFoundError:
        return None

# ==========================================
# SIDEBAR: TABLE OF CONTENTS & AUTHOR
# ==========================================
st.sidebar.title("Table of Contents")
st.sidebar.markdown("""
<a href="#0-whats-really-happening-in-the-market" class="toc-link">0. Intuition</a>
<a href="#1-executive-summary" class="toc-link">1. Executive Summary</a>
<a href="#2-data-engineering-sanity-checks" class="toc-link">2. Data Engineering & Sanity Checks</a>
<a href="#3-execution-friction-exposure-model" class="toc-link">3. Execution Friction & Exposure Model</a>
<a href="#4-synthetic-volatility-surfaces" class="toc-link">4. Synthetic Volatility Surfaces</a>
<a href="#5-regime-definitions-the-short-gamma-paradox" class="toc-link">5. Regime Definitions & The Gamma Paradox</a>
<a href="#6-statistical-proof-signal-agreement" class="toc-link">6. Statistical Proof & Signal Agreement</a>
<a href="#7-time-of-day-dynamics-theta-burnout" class="toc-link">7. Time-of-Day Dynamics (Theta)</a>
<a href="#8-model-limitations" class="toc-link">8. Model Limitations</a>
<a href="#9-conclusion-tech-stack" class="toc-link">9. Conclusion & Tech Stack</a>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Author:** [Your Name]\n\n"
    "**Role:** Quantitative Researcher\n\n"
    "**Focus:** Options Market Microstructure & Volatility Modeling"
)

# ==========================================
# MAIN DOCUMENT: TITLE (HERO SECTION)
# ==========================================
st.markdown("<h1>The Microstructure of 0DTE: Quantifying Market Maker Gamma Pins and Volatility Expansion</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>An Empirical Analysis of Dealer Positioning and Intraday Volatility.</p>", unsafe_allow_html=True)


# ==========================================
# SECTION 0: TLDR / INTUITION (CRITICAL)
# ==========================================
st.markdown("## 0. What’s Really Happening in the Market?")

st.markdown("""
Intraday price action often looks random, but when viewed through dealer positioning, clear structure emerges. Markets typically behave in two simple ways:

- **They remain near a high open-interest strike (price clustering behavior)**    
- **They break away and trend, with regime-dependent volatility behavior**

### Why this happens

It comes down to how **options dealers hedge risk**:

- When a large amount of options sit at a strike →  
  price tends to stay near that level as hedging activity stabilizes it

- When price moves far enough →  
  hedging flips → market **breaks and trends**
""")

st.markdown("""
<div class="callout">
<strong>What the Data Shows:</strong><br>

- **Pinned markets** → localized oscillation with lower realized variance  
- **Breakouts** → regime-dependent behavior, with both variance expansion and compression depending on time-of-day and liquidity

- **Gamma exposure** does not always increase volatility — its effect depends on the regime.  
  → it can suppress movement before a break, depending on regime

- **Theta** → dominates near the close  
  → forced unwinding creates volatility spikes

 In short: the market is usually being stabilized until it suddenly isn’t.
</div>
""", unsafe_allow_html=True)


st.markdown("""
**Key Takeaways:**

• Dealer positioning creates measurable intraday structure in price behavior<br>
• Pinning regimes are associated with variance compression (<1)<br>
• Breakout regimes are non-uniform and strongly time-of-day dependent<br>
• Static EOD gamma misses important intraday dynamics captured by synthetic repricing
""", unsafe_allow_html=True)

# ==========================================
# SECTION 1: EXECUTIVE SUMMARY
# ==========================================
st.header("1. What This Project Does", anchor="1-executive-summary")

st.markdown("""
0DTE options now dominate intraday index trading, which makes dealer hedging flows a measurable component of intraday price dynamics.
Market makers are constantly adjusting their positions, and this hedging flow directly interacts with the underlying futures market.
This project measures how dealer hedging affects intraday volatility.

""")

st.markdown("""
The empirical study spans 107 trading days (~37k intraday observations), allowing regime behavior to be evaluated across both microstructure and session-level dynamics.
""")


# ==========================================
# SECTION 2: DATA ENGINEERING
# ==========================================





st.header("2. Data Engineering & Sanity Checks", anchor="2-data-engineering-sanity-checks")

st.markdown("""
The pipeline reconstructs intraday dealer positioning from EOD options data and futures prices.
""")

with st.expander("Pipeline Overview (Click to Expand)"):
    st.markdown("""
    The workflow follows a strict intraday reconstruction pipeline:

    **1. EOD Initialization**  
    Start with previous-day options chain (open interest + IV surface)

    **2. Intraday Alignment**  
    Map to 1-minute ES futures price path

    **3. Dynamic Repricing**  
    Reprice the entire options surface using sticky moneyness

    **4. Gamma Construction**  
    Compute intraday gamma exposure across all strikes

    **5. Regime Identification**  
    - OI proximity (dealer concentration)  
    - IV curvature (surface convexity)

    **6. Statistical Evaluation**  
    Evaluate forward return distributions (1m–30m horizons)

    ---
    This ensures all signals are forward-looking and free from look-ahead bias.
    """)

st.markdown("""
Microstructure models are highly sensitive to data quality, so the pipeline enforces strict filtering and validation before any modeling.

""")

with st.expander("View Data Cleaning & Validation Details"):
    st.markdown("""
    **Transformations & Validations Applied:**
    * **Strict Lookback Logic:** To prevent look-ahead bias, the options universe was built using the prior day's End-of-Day (EOD) snapshot, filtering out any contracts that had already expired (DTE < 1).
    * **Arbitrage Bounds:** Eliminated 14,027 records that violated standard pricing physics (e.g., Deltas > 1.0, negative Gamma, Implied Volatility > 500%).
    * **Strike Scaling:** Automatically detected and normalized pricing artifacts to ensure realistic bounds (Median Strike anchored at 3825.0).
    * **Skew Confirmation:** Verified that Out-of-the-Money (OTM) Puts traded at a premium to At-the-Money (ATM) options, confirming a sane volatility structure before proceeding.
    """)

st.markdown("""
<div class="quant-note">
<strong>Exogenous Event Filter:</strong><br>
The pipeline explicitly removed 18 macro events spanning 15 trading days (e.g., FOMC rate decisions, CPI prints). Fundamental macro news naturally overrides normal order book dynamics. Blacking out these dates ensures the variance observed is mechanically driven by the options market, rather than fundamental repricing.
</div>
""", unsafe_allow_html=True)


# ==========================================
# SECTION 3: EXECUTION FRICTION
# ==========================================
st.header("3. Execution Friction & Exposure Model", anchor="3-execution-friction-exposure-model")

st.markdown("""
Dealer hedging is discrete, not continuous. Execution is constrained by transaction costs and liquidity, so small price moves are often ignored.
""")

st.markdown("""
Empirically, this matters: hedging is triggered in only ~50% of observed minutes, with the remaining price movement absorbed inside the friction band.
""")

with st.expander("View Exposure Normalization & Friction Model Details"):
    st.markdown("""
    ### Exposure Normalization
    During model initialization (August 17, 2022), portfolio aggregation revealed that dealer exposure was strongly skewed toward downside protection:
    * **Call Gamma Exposure:** -$177.19 Million
    * **Put Gamma Exposure:** -$3.80 Billion
    * **Net Dealer Gamma:** -$3.98 Billion

    To quantify the actual market impact, I normalized this exposure against the day's ES Futures volume. The result was -294,316%. This indicates extremely large relative exposure compared to futures volume, suggesting that even small price moves could require significant hedging activity.

    ### Friction Mechanics
    Dealers execute hedges solely when their directional risk exceeds the cost of crossing the spread:
    * `Starting Anchor Price: 4000.00`
    * `Friction Band: +/- 1.00 points` (Dealers ignore minor fluctuations inside this band).
    * `Market moves to 4000.50 -> Hedge Triggered?` **False**
    * `Market moves to 4001.10 -> Hedge Triggered?` **True** (New Anchor Price is set, and hedging flow reaches the order book).
    """)
    
st.markdown("""
<div class="quant-note">
<strong>Scale of Exposure:</strong><br>
On representative days, aggregate dealer gamma is on the order of billions of dollars notional, often exceeding underlying futures volume when normalized.<br><br>
→ This creates conditions where relatively small price changes can require disproportionately large hedge adjustments.
</div>
""", unsafe_allow_html=True)

# # Custom Dashboard Metrics
# col5, col6, col7 = st.columns(3)
# with col5:
#     st.markdown("<div class='stat-box'><div class='stat-value'>361</div><div class='stat-label'>Total Trading Minutes</div></div>", unsafe_allow_html=True)
# with col6:
#     st.markdown("<div class='stat-box'><div class='stat-value'>190</div><div class='stat-label'>Forced Hedge Triggers</div></div>", unsafe_allow_html=True)
# with col7:
#     st.markdown("<div class='stat-box'><div class='stat-value'>171</div><div class='stat-label'>Dealer Holding (Ignored)</div></div>", unsafe_allow_html=True)




# ==========================================
# SECTION 4: SYNTHETIC VOLATILITY SURFACES
# ==========================================
st.header("4. Synthetic Volatility Surfaces", anchor="4-synthetic-volatility-surfaces")

st.markdown("""
<div class="callout">
<strong>Core Problem:</strong> Static EOD gamma is stale intraday.  
This section builds a dynamic repricing engine to track real-time exposure.
</div>
""", unsafe_allow_html=True)

st.markdown("""
EOD gamma becomes unreliable intraday because implied volatility changes continuously, so the model reprices the surface each minute to maintain consistent exposure estimates.

### 1. Sticky Moneyness
I constructed a dynamic Volatility Surface that shifts concurrently with the underlying spot price. The engine recalculates Black-Scholes Gamma for every option each minute using vectorized repricing.
""")

col_img1, col_img2 = st.columns([1.5, 1])
with col_img1:
    img = load_image("images/vol_smile.png")
    if img: st.image(img, caption="Put Volatility Smile properly extrapolated with flat wings and IV floors.", use_container_width=True)
with col_img2:
    st.markdown("""
    ### 2. Identifying "Pins" via Curvature
    To mathematically locate where dealers are most concentrated, I calculated the local curvature of the IV surface using a discrete second derivative approximation:
    """)
    st.latex(r"Curvature = IV_{K-\Delta K} + IV_{K+\Delta K} - 2 \cdot IV_{K}")
    st.markdown("""
    A highly convex curve indicates heavy dealer concentration at a specific strike price. This creates a gravitational pull on the underlying asset, often referred to mechanically as a **"Pin."**
    """)


# ==========================================
# SECTION 5: REGIME DEFINITION
# ==========================================
st.header("5. Regime Definitions & The Gamma Paradox", anchor="5-regime-definitions-the-short-gamma-paradox")



col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="regime-card regime-pin">
        <h3 style="margin-top: 0;">🧲 Synthetic Pinning (price clusters near a high open-interest strike)</h3>
        
    <p><strong>Definition:</strong> Price remains near a high-interest strike</p>
    <p><strong>Behavior:</strong> Short-term oscillation, but overall movement constrained</p>
    <p><strong>Data:</strong> Variance compression (lower than normal volatility) across most horizons</p>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
    <div class="regime-card regime-break">
        <h3 style="margin-top: 0;">💥 Synthetic Breaking (price escapes and trends)</h3>
        
    <p><strong>Definition:</strong> Price escapes a concentrated strike region</p>
    <p><strong>Behavior:</strong> Directional moves with regime-dependent volatility</p>
    <p><strong>Data:</strong> Strong expansion at the open (peaking near ~3x in intraday buckets), neutral/compressive later</p>
    </div>
    """, unsafe_allow_html=True)
    

    
st.markdown("""
<div class="insight-box">
<strong>Strike Gravity Observation:</strong><br>
The majority of observations occur near high open-interest strikes, indicating that price spends most of its time in "pinned" regions rather than freely trending.
</div>
""", unsafe_allow_html=True)
    




# ==========================================
# SECTION 6: STATISTICAL PROOF
# ==========================================
st.header("6. Statistical Proof & Signal Agreement", anchor="6-statistical-proof-signal-agreement")

with st.expander("Methodology Note: Ensuring Statistical Rigor"):
    st.markdown("""
    * **Discarding Mean Return Tests:** Forward mean returns in High-Frequency Trading (HFT) data approach zero. This model tests the shape and variance of the distribution exclusively.
    * **No Reversal Bias:** I explicitly rejected `shift(1)` transition matrices. Applying sequential time-shifts across non-continuous filtered data (e.g., overnight gaps) introduces time-series corruption.
    * **Multi-Horizon Testing:** 1m, 5m, 15m, and 30m forward returns were analyzed concurrently to eliminate localized curve-fitting.
    """)

st.markdown("""
**Active Gamma:** minutes where dealer hedging is triggered  
**Baseline:** normal minutes with no forced hedging
""")

st.markdown("### Core Result: Active Gamma vs Baseline (Forward Returns: 1m–30m)")
st.markdown("""
**Each row shows forward returns over that horizon** (e.g., 5m = next 5-minute return)
""")

st.markdown("""
| Horizon | N Active | N Baseline | Var Ratio | KS p | Levene p | Kurtosis Δ | Mean (bps) | T-test p |
|--------|----------|------------|----------|------|----------|------------|------------|----------|
| 1m | 3540 | 33551 | 0.66 | 0.005 | 0.004 | -834 | -0.05 | 0.706 |
| 5m | 3538 | 33545 | 0.87 | 0.212 | 0.008 | -169 | 0.35 | 0.253 |
| 15m | 3530 | 33533 | 0.76 | 0.087 | 0.402 | -55 | 0.87 | 0.084 |
| 30m | 3517 | 33516 | 0.79 | 0.054 | 0.670 | -25 | 2.57 | 0.0004 |
""")

st.markdown("""
<div class="callout">

<strong>How to Read This:</strong><br>

Values compare volatility during Active Gamma periods vs normal periods.

• 0.66 → 34% lower than normal  
• 1.30 → 30% higher than normal  
</div>
""", unsafe_allow_html=True)


st.markdown("""
At the 1-minute level, volatility during active hedging is ~34% lower than normal (0.66x), indicating short-term stabilization.
""")

img_dist = load_image("images/kde_grid.png")
if img_dist: 
    st.image(img_dist, caption="KDE Distributions across horizons. Notice the structural differences in tail risk between regimes.", use_container_width=True)



st.markdown("### Strike Gravity Distribution")

st.markdown("""
| Location | Count |
|----------|------|
| Near Heavy Strike | 36,250 |
| Far From Heavy Strike | 843 |
| Unknown | 90 |
""")

st.markdown("""
Most observations occur near high open-interest strikes, confirming that the dataset is dominated by pinned regimes rather than free-trending behavior.
""")

    
st.markdown("### EOD vs. Synthetic Gamma Agreement")
st.markdown("""
Static EOD gamma can lag the market.
In about 20% of observations, the EOD and synthetic regime labels do not match.
When they match, the reading is cleaner.
Synthetic gamma updates intraday, so it captures changes that EOD data misses.
""")

col3, col4 = st.columns(2)
with col3:
    img_line = load_image("images/eod_vs_syn_line.png")
    if img_line: st.image(img_line, use_container_width=True)
with col4:
    img_bar = load_image("images/syn_bar_chart.png")
    if img_bar: st.image(img_bar, use_container_width=True)
    
    
st.markdown("""
### Pinning vs Breaking (15-minute horizon)

<div class="callout">
<strong>Results (based on 15-minute forward returns):</strong><br>

<strong>Pinning:</strong><br>
• Variance ≈ 0.36x (≈64% lower than normal)<br>
• KS p ≈ 0.085 (weak significance)<br>
• Levene p ≈ 0.187 (no strong variance difference)<br><br>

<strong>Breaking:</strong><br>
• Variance ≈ 0.64x to 1.0x (depends on time-of-day)<br>
• KS p ≈ 0.002 (statistically significant)<br>
• Levene p ≈ 0.001 (clear variance difference)<br><br>

👉 Interpretation:<br>
Breakouts show statistically meaningful distribution changes,  
while pinning mainly reduces volatility without strong significance.
</div>
""", unsafe_allow_html=True)    


st.markdown("""
The common assumption is that short gamma leads to higher volatility, but the data does not support this uniformly.

• Short-horizon volatility is ~0.66x of normal (≈34% lower than non-hedging periods)  
• Expansion occurs only in specific contexts (e.g. breakouts, open)  

Gamma-driven hedging is active in ~10% of observations, implying most intraday price action occurs in passive regimes.
Delta (linear exposure) shows limited impact on variance relative to gamma (convexity) and theta (decay).
""")


with st.expander("Delta Dominance Results (Linear Exposure)"):
    st.markdown("""
This tests whether **delta (linear hedging)** changes volatility.

Result: delta has minimal impact compared to gamma.

| Horizon | Var Ratio | KS p | Levene p | Mean (bps) |
|--------|----------|------|----------|------------|
| 1m | 0.92 | 0.000 | 0.0012 | 0.09 |
| 5m | 0.92 | 0.000 | 0.0049 | 0.49 |
| 15m | 0.92 | 0.000 | 0.0032 | 1.36 |
| 30m | 1.06 | 0.000 | 0.3159 | 3.14 |

→ Interpretation: delta slightly shifts distribution but does not materially change volatility.
""")

with st.expander("Theta Dominance (Expiry Effect)"):
    st.markdown("""
This isolates **time decay effects near expiry**.

| Horizon | Var Ratio | KS p | Levene p |
|--------|----------|------|----------|
| 1m | ~1.4–1.6 | ~0.000 | ~0.001 |
| 30m | ~1.7 | ~0.000 | ~0.001 |

→ Interpretation: volatility increases significantly near close due to forced position unwinding.
""")




st.markdown("""
<div class="insight-box">
<strong>Key Insight:</strong><br>

Variance compression is strongest at microstructure horizons (1–5 minutes) and weakens with time aggregation, confirming that dealer-driven effects are short-lived rather than persistent.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="callout">
<strong>Model Validation Perspective:</strong><br>

• Synthetic gamma aligns with observed intraday variance behavior  
• EOD gamma disagrees in ~20% of observations, reflecting stale positioning  
• Signals are strongest when both agree, and weaker when they diverge  

👉 Interpretation:  
Intraday repricing is necessary to capture real market dynamics.
</div>
""", unsafe_allow_html=True)




with st.expander("Detailed Statistical Results (KS & Levene Tests)"):
    st.markdown("""
    **Statistical Significance Highlights (15-Minute Synthetic Data):**
    * **Synthetic Pinning:** Variance Ratios vary by context but are predominantly <1, indicating compression in most regimes. KS p-value = `0.0000`, verifying that the distribution shape statistically broadens.
    * **Synthetic Breaking:** Variance ratios are regime-dependent (≈0.8–3.0 across contexts). KS p-value = `0.0001`, verifying statistically significant distribution shifts.
    """)


st.markdown("""
**Breakout regimes exhibit stronger distributional shifts than pinning regimes** — which is why breakout regimes tend to show stronger statistical significance.
""")

# ==========================================
# SECTION 7: TIME-OF-DAY DYNAMICS
# ==========================================
st.header("7. Time-of-Day Dynamics (Theta Burnout)", anchor="7-time-of-day-dynamics-theta-burnout")

st.markdown("""
Because 0DTE options decay to zero by 4:00 PM, dealers have less room to carry risk into the close. That makes late-session hedging more forced and more volatile.
""")


st.markdown("""
<div class="callout" style="border-left-color: #EF4444;">
<strong>The Impact of Theta (Time Decay):</strong><br>
Isolating regimes dominated by Theta revealed some of the highest realized variance in the dataset:
<ul style="margin-top: 5px; margin-bottom: 5px;">
    <li><strong>Volatility Multiplier:</strong> Expanded to 1.70x at the 30-minute horizon.</li>
    <li><strong>Kurtosis (Tail Risk):</strong> Increased by +585.38 at the 1-minute horizon (p-value = 0.0004).</li>
</ul>
As expiry approaches, dealers unwind positions, increasing volatility. The effect is strongest near close and depends on liquidity conditions.
</div>
""", unsafe_allow_html=True)

st.markdown("""
These effects are not uniform — they vary significantly across time-of-day and global trading sessions.
""")


col5, col6 = st.columns(2)
with col5:
    img_h1 = load_image("images/heatmap_intra_squeeze.png")
    if img_h1: st.image(img_h1, caption="Intraday Trend/Breakout Variance", use_container_width=True)
    
    img_h2 = load_image("images/heatmap_global_squeeze.png")
    if img_h2: st.image(img_h2, caption="Global Session Trend Variance", use_container_width=True)
    
with col6:
    img_h3 = load_image("images/heatmap_intra_pin.png")
    if img_h3: st.image(img_h3, caption="Intraday Pin/Chop Variance", use_container_width=True)
    
    img_h4 = load_image("images/heatmap_global_pin.png")
    if img_h4: st.image(img_h4, caption="Global Session Pin Variance", use_container_width=True)


st.markdown("""
**Session read:** Asia handoff shows the clearest pinning compression, London/US overlap is mixed, and US-only is the least pinned and often expansionary in this sample. So the same regime behaves differently depending on the session — the label alone is not enough.
""")

st.markdown("""
*Observation: Breakout volatility multipliers are notably amplified right at the OPEN. Dealers must actively hedge structural gaps from the overnight session before intraday liquidity normalizes.*
""")

st.markdown("""
### Key Structural Observation

The strength of these effects is highly time-dependent:

- **Market Open:** strongest breakout expansion (consistent with hedging of overnight gaps)  
- **Midday:** weakest signal (liquidity stabilizes flows)  
- **Late Session:** pinning and theta-driven effects dominate  

👉 This shows that dealer-driven microstructure is not constant, it depends on liquidity regime and time-of-day.
""")

# ==========================================
# SECTION 8: MODEL LIMITATIONS
# ==========================================
st.header("8. Model Limitations", anchor="8-model-limitations")

st.markdown("""
<div class="limitation-note">
<strong>What This Model Cannot Infer:</strong><br>
To maintain structural rigor, it is critical to explicitly define the boundaries of this research:
<ul style="margin-top: 5px; margin-bottom: 5px;">
    <li><strong>Non-Directionality:</strong> Gamma is a non-directional, second-order Greek. This model predicts the <em>compression or expansion of variance</em>, not the <em>directional vector</em> (up or down) of the breakout.</li>
    <li><strong>Macroeconomic Overrides:</strong> The model is purely microstructural. It fails during macroeconomic surprises where fundamental repricing overrides order book gravity (which necessitated the strict blackout filter).</li>
    <li><strong>Causality vs. Catalyst:</strong> While dealer positioning dictates the "pinning gravity" of the market, exogenous directional flow (e.g., institutional or retail buying) remains the ultimate catalyst required to break a pin.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="callout">
<strong>Overall Interpretation:</strong><br>
• Intraday volatility is not uniform — it depends on dealer positioning<br>
• Pinning stabilizes price behavior (compression)<br>
• Breakouts introduce regime-dependent volatility shifts<br>
• Time-of-day plays a critical role in shaping these effects
</div>
""", unsafe_allow_html=True)

# ==========================================
# SECTION 9: CONCLUSION
# ==========================================
st.header("9. Conclusion & Tech Stack", anchor="9-conclusion-tech-stack")



st.markdown("### Key Results")

st.markdown("""
• Gamma exposure → short-horizon variance compression (~0.66x at 1m)  
• Pinning → constrained price behavior with lower realized volatility  
• Breakouts → strongly time-dependent (expansion at open, weaker later)  
• Theta → late-session volatility expansion (~1.7x)  
""")

st.markdown("""
Dealer positioning directly affects intraday volatility.

This model separates stable (pinned) periods from breakout periods using intraday gamma and execution constraints.
""")

st.markdown("### Core Competencies & Tech Stack")

st.markdown("""
* **Languages & Frameworks:** Python, Pandas, NumPy (Matrix Broadcasting), SciPy (Statistical Testing), Seaborn, Streamlit.
* **Quantitative Concepts:** * Black-Scholes-Merton Pricing & Option Greeks (Gamma/Delta/Theta).
  * Volatility Surface Interpolation, Extrapolation & Curvature Math.
  * Discrete Derivatives & Market Microstructure (Friction/Bid-Ask Modeling).
* **Statistical Methods:** * Levene’s Test for Homogeneity of Variance.
  * Kolmogorov-Smirnov (KS-2Samp) Distribution Shape Testing.
  * Out-of-Sample Forward Log Returns.
* **Data Engineering:** * Efficient vectorized data processing and simulation pipelines.
  * Strict avoidance of time-series look-ahead and reversal bias corruption.
""")

st.markdown("""
👉 Intraday volatility is not purely random — a meaningful part of it reflects how dealers manage risk and rebalance exposure in real time.
""")

st.markdown("""
In other words, intraday price behavior is not just noise — it reflects the mechanics of how risk is transferred and managed in the options market.
""")

st.markdown("<p style='text-align: center; font-size: 1.15rem; color: #6B7280;'><em>Thank you for reviewing this pipeline. The goal of this pipeline is to isolate mechanically driven intraday behavior and evaluate it with statistically robust methods.</em></p>", unsafe_allow_html=True)